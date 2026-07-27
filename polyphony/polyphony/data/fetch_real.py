"""Fetch REAL historical data for the tournament — closes honesty-debt issue #9.

Two public, citable sources, merged by year:

- **World GDP** (constant 2015 US$): World Bank indicator ``NY.GDP.MKTP.KD``, aggregate ``WLD``
  (https://api.worldbank.org).
- **Global CO₂ emissions** (Mt CO₂/yr): Our World in Data ``owid-co2-data.csv``, ``country == "World"``
  (https://github.com/owid/co2-data).
- **Global temperature anomaly** (°C vs pre-industrial, Hadley Centre median): OWID datasets mirror
  (https://github.com/owid/owid-datasets). The *observed* warming — a more honest damage driver than
  cumulative CO₂.

Writes ``datasets/real_gdp_co2.csv`` (columns: ``year``, ``gdp``, ``co2``, ``temp``). Network egress is
intermittent in the loop; run this when it is up. The loader falls back to synthetic when the CSV is
absent, so the suite never depends on the network.
"""

from __future__ import annotations

import csv
import io
import json
import pathlib
import urllib.request

DATASETS = pathlib.Path(__file__).resolve().parent / "datasets"
WB_GDP = "https://api.worldbank.org/v2/country/WLD/indicator/NY.GDP.MKTP.KD?format=json&per_page=400"
OWID_CO2 = "https://raw.githubusercontent.com/owid/co2-data/master/owid-co2-data.csv"
OWID_TEMP = (
    "https://raw.githubusercontent.com/owid/owid-datasets/master/datasets/"
    "Global%20average%20temperature%20anomaly%20-%20Hadley%20Centre/"
    "Global%20average%20temperature%20anomaly%20-%20Hadley%20Centre.csv"
)


def _fetch_worldbank_gdp() -> dict[int, float]:
    with urllib.request.urlopen(WB_GDP, timeout=30) as r:
        payload = json.load(r)
    return {int(x["date"]): float(x["value"]) for x in payload[1] if x["value"] is not None}


def _fetch_owid_co2() -> dict[int, float]:
    with urllib.request.urlopen(OWID_CO2, timeout=60) as r:
        text = r.read().decode("utf-8")
    reader = csv.DictReader(io.StringIO(text))
    return {int(row["year"]): float(row["co2"]) for row in reader if row["country"] == "World" and row["co2"]}


def _fetch_owid_temp() -> dict[int, float]:
    with urllib.request.urlopen(OWID_TEMP, timeout=30) as r:
        text = r.read().decode("utf-8")
    reader = csv.DictReader(io.StringIO(text))
    col = (reader.fieldnames or [])[-1]  # the anomaly column
    return {int(row["Year"]): float(row[col]) for row in reader if row["Entity"] == "median" and row[col]}


WB_CEREAL_YIELD = "https://api.worldbank.org/v2/country/WLD/indicator/AG.YLD.CREL.KG?format=json&per_page=400"


def _fetch_worldbank_cereal_yield() -> dict[int, float]:
    with urllib.request.urlopen(WB_CEREAL_YIELD, timeout=30) as r:
        payload = json.load(r)
    return {int(x["date"]): float(x["value"]) for x in payload[1] if x["value"] is not None}


WB_PM25 = "https://api.worldbank.org/v2/country/WLD/indicator/EN.ATM.PM25.MC.M3?format=json&per_page=400"
WB_DEATH_RATE = "https://api.worldbank.org/v2/country/WLD/indicator/SP.DYN.CDRT.IN?format=json&per_page=400"


def _fetch_worldbank(url: str) -> dict[int, float]:
    """Fetch a World Bank WLD indicator as {year: value}, retrying transient network errors."""
    last: Exception | None = None
    for _ in range(3):
        try:
            with urllib.request.urlopen(url, timeout=60) as r:
                payload = json.load(r)
            return {int(x["date"]): float(x["value"]) for x in payload[1] if x["value"] is not None}
        except Exception as e:  # transient egress failures are common in the loop; retry
            last = e
    raise RuntimeError(f"World Bank fetch failed after retries: {url}") from last


def fetch(out: pathlib.Path | None = None) -> pathlib.Path:
    """Fetch, align on common years, and write the merged CSV. Returns the path written."""
    gdp = _fetch_worldbank_gdp()
    co2 = _fetch_owid_co2()
    temp = _fetch_owid_temp()
    years = sorted(set(gdp) & set(co2) & set(temp))
    if len(years) < 20:
        raise RuntimeError(f"too few overlapping years ({len(years)}); refusing to write")
    out = out or (DATASETS / "real_gdp_co2.csv")
    with out.open("w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["year", "gdp", "co2", "temp"])
        for y in years:
            w.writerow([y, gdp[y], co2[y], temp[y]])
    return out


def fetch_food(out: pathlib.Path | None = None) -> pathlib.Path:
    """Fetch the REAL Land⇄Climate⇄Food series: World Bank cereal yield (kg/ha) + Hadley temperature.

    Writes ``datasets/real_food.csv`` (columns: ``year``, ``cereal_yield``, ``temp``). Cereal yield is
    the quantity the land voice models (warming → lower yield → higher food price); this lets us test
    that mechanism on real data with a placebo control.
    """
    yield_ = _fetch_worldbank_cereal_yield()
    temp = _fetch_owid_temp()
    years = sorted(set(yield_) & set(temp))
    if len(years) < 20:
        raise RuntimeError(f"too few overlapping years ({len(years)}); refusing to write")
    out = out or (DATASETS / "real_food.csv")
    with out.open("w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["year", "cereal_yield", "temp"])
        for y in years:
            w.writerow([y, yield_[y], temp[y]])
    return out


FRED_FOOD = "https://fred.stlouisfed.org/graph/fredgraph.csv?id=PFOODINDEXM"  # IMF Global Food Price Index
FRED_ENERGY = "https://fred.stlouisfed.org/graph/fredgraph.csv?id=PNRGINDEXM"  # IMF Global Energy Price Index


def _fetch_fred_annual(url: str, min_obs: int = 12) -> dict[int, float]:
    """Fetch a FRED series (CSV, no API key) and average to calendar-year means, keeping only years with
    at least ``min_obs`` observations (12 for monthly, 4 for quarterly) so partial years don't bias the mean."""
    last: Exception | None = None
    for _ in range(3):
        try:
            with urllib.request.urlopen(url, timeout=60) as r:
                text = r.read().decode("utf-8")
            reader = csv.reader(io.StringIO(text))
            next(reader, None)  # header: observation_date, <series_id>
            by_year: dict[int, list[float]] = {}
            for row in reader:
                if len(row) >= 2 and row[1] not in (".", ""):
                    by_year.setdefault(int(row[0][:4]), []).append(float(row[1]))
            return {y: sum(v) / len(v) for y, v in by_year.items() if len(v) >= min_obs}
        except Exception as e:  # transient egress failures; retry
            last = e
    raise RuntimeError(f"FRED fetch failed after retries: {url}") from last


def fetch_nexus(out: pathlib.Path | None = None) -> pathlib.Path:
    """Fetch the REAL Water⇄Energy⇄Food nexus series (issue #10-real): IMF Global **Food** and **Energy**
    price indices (FRED PFOODINDEXM / PNRGINDEXM), annual means.

    A clean global *water-scarcity* driver is not readily available as an annual series, so we test the
    nexus's most data-rich, best-documented leg — the **energy → food-price** transmission (natural gas →
    nitrogen fertilizer; diesel → machinery/transport; electricity → irrigation pumping) — which the
    ``nexusfood`` voice carries as its pumping-energy surcharge. This is a *partial* test of the nexus
    (the energy pillar, not the water pillar); the water-leg real test remains data-limited.

    Writes ``datasets/real_nexus.csv`` (columns: ``year``, ``food_price``, ``energy_price``).
    """
    food = _fetch_fred_annual(FRED_FOOD)
    energy = _fetch_fred_annual(FRED_ENERGY)
    years = sorted(set(food) & set(energy))
    if len(years) < 20:
        raise RuntimeError(f"too few overlapping years ({len(years)}); refusing to write")
    out = out or (DATASETS / "real_nexus.csv")
    with out.open("w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["year", "food_price", "energy_price"])
        for y in years:
            w.writerow([y, food[y], energy[y]])
    return out


WB_TRADE_OPENNESS = "https://api.worldbank.org/v2/country/GBR/indicator/NE.TRD.GNFS.ZS?format=json&per_page=400"


def _fetch_owid_country_co2(country: str) -> dict[int, tuple[float, float]]:
    """{year: (production_co2, consumption_co2)} for one country from OWID (both columns present)."""
    with urllib.request.urlopen(OWID_CO2, timeout=60) as r:
        text = r.read().decode("utf-8")
    reader = csv.DictReader(io.StringIO(text))
    out: dict[int, tuple[float, float]] = {}
    for row in reader:
        if row["country"] == country and row.get("co2") and row.get("consumption_co2"):
            out[int(row["year"])] = (float(row["co2"]), float(row["consumption_co2"]))
    return out


def fetch_trade(out: pathlib.Path | None = None) -> pathlib.Path:
    """Fetch the REAL Trade⇄Emissions series (issue #12-real): the **United Kingdom** — the textbook
    carbon-leakage case (production emissions ~halved since 1990 while consumption emissions fell far less).

    OWID production (``co2``) + consumption (``consumption_co2``) CO₂, plus World Bank UK **trade openness**
    (``NE.TRD.GNFS.ZS``) as an **independent** leakage driver (using the observed gap itself would be
    circular). The World aggregate is *not* usable — global trade nets to zero, so consumption = production.
    Writes ``datasets/real_trade.csv`` (columns: ``year``, ``production_co2``, ``consumption_co2``, ``openness``).
    """
    co2 = _fetch_owid_country_co2("United Kingdom")
    openness = _fetch_worldbank(WB_TRADE_OPENNESS)
    years = sorted(set(co2) & set(openness))
    if len(years) < 20:
        raise RuntimeError(f"too few overlapping years ({len(years)}); refusing to write")
    out = out or (DATASETS / "real_trade.csv")
    with out.open("w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["year", "production_co2", "consumption_co2", "openness"])
        for y in years:
            w.writerow([y, co2[y][0], co2[y][1], openness[y]])
    return out


WB_OPENNESS_ALL = "https://api.worldbank.org/v2/country/all/indicator/NE.TRD.GNFS.ZS?format=json&per_page=20000"


def fetch_leakage_panel(out: pathlib.Path | None = None, min_years: int = 15) -> pathlib.Path:
    """Fetch a multi-country **panel** for the carbon-leakage mechanism (Iter 33 — panel validation).

    For every country with enough data (1990–2021): the consumption/production CO₂ **ratio** (OWID) and
    **trade openness** (World Bank ``NE.TRD.GNFS.ZS``, one bulk call). A two-way fixed-effects analysis of
    this panel removes country *and* year effects (the shared global trend), isolating the within-country
    mechanism the single UK time series could not. Writes ``datasets/real_leakage_panel.csv`` (columns:
    ``iso``, ``year``, ``cons_prod_ratio``, ``openness``).
    """
    with urllib.request.urlopen(WB_OPENNESS_ALL, timeout=90) as r:
        payload = json.load(r)
    openness: dict[str, dict[int, float]] = {}
    for x in payload[1]:
        if x["value"] is not None:
            openness.setdefault(x["countryiso3code"], {})[int(x["date"])] = float(x["value"])

    with urllib.request.urlopen(OWID_CO2, timeout=60) as r:
        text = r.read().decode("utf-8")
    reader = csv.DictReader(io.StringIO(text))
    co2: dict[str, dict[int, tuple[float, float]]] = {}
    for row in reader:
        iso = row.get("iso_code") or ""
        if len(iso) == 3 and row.get("co2") and row.get("consumption_co2") and float(row["co2"]) > 0:
            co2.setdefault(iso, {})[int(row["year"])] = (float(row["co2"]), float(row["consumption_co2"]))

    out = out or (DATASETS / "real_leakage_panel.csv")
    n = 0
    with out.open("w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["iso", "year", "cons_prod_ratio", "openness"])
        for iso in sorted(set(co2) & set(openness)):
            years = [y for y in sorted(set(co2[iso]) & set(openness[iso])) if 1990 <= y <= 2021]
            if len(years) >= min_years:
                for y in years:
                    prod, cons = co2[iso][y]
                    w.writerow([iso, y, cons / prod, openness[iso][y]])
                    n += 1
    if n < 500:
        raise RuntimeError(f"too few panel observations ({n}); refusing to write")
    return out


WB_PM25_ALL = "https://api.worldbank.org/v2/country/all/indicator/EN.ATM.PM25.MC.M3?format=json&per_page=25000"
WB_DEATH_ALL = "https://api.worldbank.org/v2/country/all/indicator/SP.DYN.CDRT.IN?format=json&per_page=25000"


def _fetch_worldbank_all(url: str) -> dict[str, dict[int, float]]:
    """{iso3: {year: value}} for a World Bank indicator across all countries (one bulk call, retried)."""
    last: Exception | None = None
    for _ in range(4):
        try:
            with urllib.request.urlopen(url, timeout=120) as r:
                payload = json.load(r)
            out: dict[str, dict[int, float]] = {}
            for x in payload[1]:
                iso = x["countryiso3code"]
                if x["value"] is not None and len(iso) == 3:
                    out.setdefault(iso, {})[int(x["date"])] = float(x["value"])
            return out
        except Exception as e:
            last = e
    raise RuntimeError(f"World Bank bulk fetch failed after retries: {url}") from last


def fetch_pm25_mortality_panel(out: pathlib.Path | None = None, min_years: int = 8) -> pathlib.Path:
    """Fetch a multi-country panel for the co-benefit mechanism (Iter 34 — panel validation, 2nd case).

    Per country (1990–2023): PM2.5 exposure (World Bank ``EN.ATM.PM25.MC.M3``) and the all-cause crude
    death rate (``SP.DYN.CDRT.IN``). Unlike the leakage panel, all-cause mortality carries strong
    within-country development/aging trends, so this panel tests whether panel fixed effects can recover
    the (real, micro-level) PM2.5 → mortality effect from aggregate data. Writes
    ``datasets/real_pm25_mortality_panel.csv`` (columns: ``iso``, ``year``, ``pm25``, ``death_rate``).
    """
    pm25 = _fetch_worldbank_all(WB_PM25_ALL)
    death = _fetch_worldbank_all(WB_DEATH_ALL)
    out = out or (DATASETS / "real_pm25_mortality_panel.csv")
    n = 0
    with out.open("w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["iso", "year", "pm25", "death_rate"])
        for iso in sorted(set(pm25) & set(death)):
            years = [y for y in sorted(set(pm25[iso]) & set(death[iso])) if 1990 <= y <= 2023]
            if len(years) >= min_years:
                for y in years:
                    w.writerow([iso, y, pm25[iso][y], death[iso][y]])
                    n += 1
    if n < 500:
        raise RuntimeError(f"too few panel observations ({n}); refusing to write")
    return out


WB_GDP_PCAP = "https://api.worldbank.org/v2/country/all/indicator/NY.GDP.PCAP.KD?format=json&per_page=27000"
WB_LIFE_EXP = "https://api.worldbank.org/v2/country/all/indicator/SP.DYN.LE00.IN?format=json&per_page=27000"


def fetch_preston_panel(out: pathlib.Path | None = None, min_years: int = 15) -> pathlib.Path:
    """Fetch a multi-country panel for the **Preston curve** (Iter 51 — the generalization's boundary):
    log GDP per capita (World Bank ``NY.GDP.PCAP.KD``) + life expectancy (``SP.DYN.LE00.IN``). Unlike carbon
    leakage, income→life-expectancy has a **real within-country mechanism**, so its two-way-FE within
    correlation survives (positive) rather than collapsing — a panel coupling that is *kept*. Writes
    ``datasets/real_preston_panel.csv`` (columns: ``iso``, ``year``, ``log_gdppc``, ``life_exp``).
    """
    import math

    gdp = _fetch_worldbank_all(WB_GDP_PCAP)
    le = _fetch_worldbank_all(WB_LIFE_EXP)
    out = out or (DATASETS / "real_preston_panel.csv")
    n = 0
    with out.open("w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["iso", "year", "log_gdppc", "life_exp"])
        for iso in sorted(set(gdp) & set(le)):
            years = [y for y in sorted(set(gdp[iso]) & set(le[iso])) if gdp[iso][y] > 0]
            if len(years) >= min_years:
                for y in years:
                    w.writerow([iso, y, math.log(gdp[iso][y]), le[iso][y]])
                    n += 1
    if n < 1000:
        raise RuntimeError(f"too few panel observations ({n}); refusing to write")
    return out


FRED_SPREAD = "https://fred.stlouisfed.org/graph/fredgraph.csv?id=BAA10Y"  # Baa − 10Y Treasury credit spread
FRED_REALGDP = "https://fred.stlouisfed.org/graph/fredgraph.csv?id=GDPC1"  # real GDP (chained 2017 $)


def fetch_finance(out: pathlib.Path | None = None) -> pathlib.Path:
    """Fetch the REAL Macro⇄Finance series (issue #11-real): the Baa−10Y **credit spread** (FRED BAA10Y)
    and **real GDP** (FRED GDPC1), annual means.

    Tests the financial-accelerator mechanism (credit stress → weaker output) on real data. The natural
    target is GDP *growth* (financial conditions predict activity, not the smooth level; Gilchrist-Zakrajšek
    2012); the tournament computes growth from the GDP level. Writes ``datasets/real_finance.csv`` (columns:
    ``year``, ``gdp``, ``spread``).
    """
    spread = _fetch_fred_annual(FRED_SPREAD, min_obs=12)  # daily
    gdp = _fetch_fred_annual(FRED_REALGDP, min_obs=4)  # quarterly
    years = sorted(set(spread) & set(gdp))
    if len(years) < 20:
        raise RuntimeError(f"too few overlapping years ({len(years)}); refusing to write")
    out = out or (DATASETS / "real_finance.csv")
    with out.open("w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["year", "gdp", "spread"])
        for y in years:
            w.writerow([y, gdp[y], spread[y]])
    return out


FRED_CPI = "https://fred.stlouisfed.org/graph/fredgraph.csv?id=CPIAUCSL"  # US CPI, all urban consumers
def _fetch_fred_quarterly(url: str) -> dict[tuple[int, int], float]:
    """Fetch a FRED monthly series and average to calendar quarters (full quarters only), keyed (year, q)."""
    last: Exception | None = None
    for _ in range(3):
        try:
            with urllib.request.urlopen(url, timeout=60) as r:
                text = r.read().decode("utf-8")
            reader = csv.reader(io.StringIO(text))
            next(reader, None)
            by_q: dict[tuple[int, int], list[float]] = {}
            for row in reader:
                if len(row) >= 2 and row[1] not in (".", ""):
                    y, m = int(row[0][:4]), int(row[0][5:7])
                    by_q.setdefault((y, (m - 1) // 3 + 1), []).append(float(row[1]))
            return {q: sum(v) / len(v) for q, v in by_q.items() if len(v) >= 3}
        except Exception as e:
            last = e
    raise RuntimeError(f"FRED quarterly fetch failed after retries: {url}") from last


def fetch_inflation_quarterly(out: pathlib.Path | None = None) -> pathlib.Path:
    """Fetch the REAL Energy⇄Inflation series at **quarterly** frequency (Iter 48 — higher-power confirmation):
    IMF Global Energy price index (FRED PNRGINDEXM) + US CPI (CPIAUCSL), quarterly means. More observations
    ⇒ more walk-forward folds. Writes ``datasets/real_inflation_q.csv`` (columns: ``year``, ``quarter``,
    ``energy``, ``cpi``)."""
    energy = _fetch_fred_quarterly(FRED_ENERGY)
    cpi = _fetch_fred_quarterly(FRED_CPI)
    quarters = sorted(set(energy) & set(cpi))
    if len(quarters) < 40:
        raise RuntimeError(f"too few overlapping quarters ({len(quarters)}); refusing to write")
    out = out or (DATASETS / "real_inflation_q.csv")
    with out.open("w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["year", "quarter", "energy", "cpi"])
        for (y, q) in quarters:
            w.writerow([y, q, energy[(y, q)], cpi[(y, q)]])
    return out


FRED_MORTGAGE = "https://fred.stlouisfed.org/graph/fredgraph.csv?id=MORTGAGE30US"  # 30-yr fixed mortgage rate
FRED_HPI = "https://fred.stlouisfed.org/graph/fredgraph.csv?id=CSUSHPINSA"  # Case-Shiller national HPI


def fetch_housing(out: pathlib.Path | None = None) -> pathlib.Path:
    """Fetch the REAL Interest-Rate⇄Housing series (issue #14): the 30-year mortgage **rate** (FRED
    MORTGAGE30US) and the Case-Shiller national **house-price index** (CSUSHPINSA), annual means.

    Higher rates should slow house-price growth — but rates and house-price growth *co-move* contemporaneously
    because the Fed hikes into booms (reverse causation), so the tournament tests the **lagged** rate against
    house-price growth. Writes ``datasets/real_housing.csv`` (columns: ``year``, ``rate``, ``hpi``).
    """
    rate = _fetch_fred_annual(FRED_MORTGAGE, min_obs=12)
    hpi = _fetch_fred_annual(FRED_HPI, min_obs=12)
    years = sorted(set(rate) & set(hpi))
    if len(years) < 20:
        raise RuntimeError(f"too few overlapping years ({len(years)}); refusing to write")
    out = out or (DATASETS / "real_housing.csv")
    with out.open("w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["year", "rate", "hpi"])
        for y in years:
            w.writerow([y, rate[y], hpi[y]])
    return out


def fetch_inflation(out: pathlib.Path | None = None) -> pathlib.Path:
    """Fetch the REAL Energy⇄Inflation series (issue #13-real): the IMF Global **Energy** price index
    (FRED PNRGINDEXM) and US **CPI** (FRED CPIAUCSL), annual means.

    Energy is a large, direct component of consumer prices and passes through to core costs, so energy
    price *growth* should predict inflation — a central-bank-relevant coupling. The tournament derives
    both growth rates from the levels. Writes ``datasets/real_inflation.csv`` (columns: ``year``,
    ``energy``, ``cpi``).
    """
    energy = _fetch_fred_annual(FRED_ENERGY, min_obs=12)
    cpi = _fetch_fred_annual(FRED_CPI, min_obs=12)
    years = sorted(set(energy) & set(cpi))
    if len(years) < 20:
        raise RuntimeError(f"too few overlapping years ({len(years)}); refusing to write")
    out = out or (DATASETS / "real_inflation.csv")
    with out.open("w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["year", "energy", "cpi"])
        for y in years:
            w.writerow([y, energy[y], cpi[y]])
    return out


FRED_UNRATE = "https://fred.stlouisfed.org/graph/fredgraph.csv?id=UNRATE"  # unemployment rate
FRED_TERMSPREAD = "https://fred.stlouisfed.org/graph/fredgraph.csv?id=T10Y3M"  # 10Y − 3M term spread


def fetch_additional_probes(out_dir: pathlib.Path | None = None) -> tuple[pathlib.Path, pathlib.Path]:
    """Fetch two 'additional probe' series (Iter 50) that reinforce the central finding — even famous macro
    relationships don't beat a climatology baseline for **annual GDP growth**:

    - **Okun** (`real_okun.csv`: year, unrate, gdp): Δunemployment vs growth — a *coincident* indicator.
    - **Yield curve** (`real_yieldcurve.csv`: year, spread, gdp): the 10Y−3M term spread vs *next-year* growth
      — a *leading* indicator whose signal is nonetheless washed out at annual resolution.
    """
    d = out_dir or DATASETS
    gdp = _fetch_fred_annual(FRED_REALGDP, min_obs=4)
    unrate = _fetch_fred_annual(FRED_UNRATE, min_obs=12)
    spread = _fetch_fred_annual(FRED_TERMSPREAD, min_obs=12)

    okun_path = d / "real_okun.csv"
    yrs = sorted(set(gdp) & set(unrate))
    with okun_path.open("w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["year", "unrate", "gdp"])
        for y in yrs:
            w.writerow([y, unrate[y], gdp[y]])

    yc_path = d / "real_yieldcurve.csv"
    yrs2 = sorted(set(gdp) & set(spread))
    with yc_path.open("w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["year", "spread", "gdp"])
        for y in yrs2:
            w.writerow([y, spread[y], gdp[y]])
    return okun_path, yc_path


def fetch_cobenefit(out: pathlib.Path | None = None) -> pathlib.Path:
    """Fetch the REAL Urban⇄Transport⇄Energy⇄Health series (issue #7-real): World Bank world PM2.5 mean
    annual exposure (``EN.ATM.PM25.MC.M3``, µg/m³) + an **independent** all-cause crude death rate
    (``SP.DYN.CDRT.IN``, per 1000).

    The outcome is deliberately **all-cause** mortality, NOT the GBD "mortality attributed to ambient air
    pollution" indicator: the latter is *derived from* PM2.5 via a concentration-response function, so
    testing PM2.5 → GBD-mortality would be **circular** (it would confirm the mechanism by construction).
    An independent outcome makes the placebo test meaningful — at the cost that all-cause mortality is
    dominated by demographics, which is exactly the confounding the placebo is there to expose.

    Writes ``datasets/real_cobenefit.csv`` (columns: ``year``, ``pm25``, ``death_rate``).
    """
    pm25 = _fetch_worldbank(WB_PM25)
    death = _fetch_worldbank(WB_DEATH_RATE)
    years = sorted(set(pm25) & set(death))
    if len(years) < 20:
        raise RuntimeError(f"too few overlapping years ({len(years)}); refusing to write")
    out = out or (DATASETS / "real_cobenefit.csv")
    with out.open("w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["year", "pm25", "death_rate"])
        for y in years:
            w.writerow([y, pm25[y], death[y]])
    return out


if __name__ == "__main__":
    path = fetch()
    print(f"wrote {path} ({sum(1 for _ in path.open()) - 1} rows)")
    food = fetch_food()
    print(f"wrote {food} ({sum(1 for _ in food.open()) - 1} rows)")
    cobenefit = fetch_cobenefit()
    print(f"wrote {cobenefit} ({sum(1 for _ in cobenefit.open()) - 1} rows)")
    nexus = fetch_nexus()
    print(f"wrote {nexus} ({sum(1 for _ in nexus.open()) - 1} rows)")
    finance = fetch_finance()
    print(f"wrote {finance} ({sum(1 for _ in finance.open()) - 1} rows)")
    trade = fetch_trade()
    print(f"wrote {trade} ({sum(1 for _ in trade.open()) - 1} rows)")
    panel = fetch_leakage_panel()
    print(f"wrote {panel} ({sum(1 for _ in panel.open()) - 1} rows)")
    pm_panel = fetch_pm25_mortality_panel()
    print(f"wrote {pm_panel} ({sum(1 for _ in pm_panel.open()) - 1} rows)")
    inflation = fetch_inflation()
    print(f"wrote {inflation} ({sum(1 for _ in inflation.open()) - 1} rows)")
    housing = fetch_housing()
    print(f"wrote {housing} ({sum(1 for _ in housing.open()) - 1} rows)")
    inflation_q = fetch_inflation_quarterly()
    print(f"wrote {inflation_q} ({sum(1 for _ in inflation_q.open()) - 1} rows)")
    okun_p, yc_p = fetch_additional_probes()
    print(f"wrote {okun_p} and {yc_p}")
    preston = fetch_preston_panel()
    print(f"wrote {preston} ({sum(1 for _ in preston.open()) - 1} rows)")
