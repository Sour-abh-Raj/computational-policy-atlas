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


if __name__ == "__main__":
    path = fetch()
    print(f"wrote {path} ({sum(1 for _ in path.open()) - 1} rows)")
    food = fetch_food()
    print(f"wrote {food} ({sum(1 for _ in food.open()) - 1} rows)")
