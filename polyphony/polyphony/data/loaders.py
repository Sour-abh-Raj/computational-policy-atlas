"""Dataset loading — real CSV if present, else a clearly-labeled synthetic fallback."""

from __future__ import annotations

import csv
import pathlib
from dataclasses import dataclass, field

import numpy as np

DATASETS = pathlib.Path(__file__).resolve().parent / "datasets"


@dataclass
class Dataset:
    name: str
    series: dict[str, np.ndarray]
    synthetic: bool
    note: str = ""
    meta: dict = field(default_factory=dict)

    def __len__(self) -> int:
        return len(next(iter(self.series.values()))) if self.series else 0

    def column(self, key: str) -> np.ndarray:
        return self.series[key]


def load_csv(path: pathlib.Path) -> Dataset:
    """Load a wide CSV: first row headers, one numeric column per series."""
    with path.open(newline="", encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        cols: dict[str, list[float]] = {k: [] for k in (reader.fieldnames or [])}
        for row in reader:
            for k, v in row.items():
                cols[k].append(float(v))
    series = {k: np.asarray(v, dtype=float) for k, v in cols.items()}
    return Dataset(name=path.stem, series=series, synthetic=False, note=f"loaded {path.name}")


def synthetic_policy_series(n: int = 30, seed: int = 0, carbon_price: float = 50.0) -> Dataset:
    """A synthetic 'observed' GDP+emissions path for harness testing. NOT real data.

    Generated so the backtesting/synergy machinery has a target offline; it deliberately
    contains a mild energy⇄economy⇄climate signal plus noise so that a *coupled* predictor can,
    in principle, beat isolated parts — but any such result on THIS series proves the machinery,
    not real-world skill (see docs/polyphony/related-work.md).
    """
    rng = np.random.default_rng(seed)
    t = np.arange(n)
    emissions = 80.0 * np.exp(-0.02 * carbon_price) * (1.0 - 0.01 * t) + rng.normal(0, 1.5, n)
    cum = np.cumsum(np.clip(emissions, 0, None))
    temperature = 0.001 * cum
    damage = 0.005 * temperature**2
    gdp = 100.0 * (1.0 - 0.002 * (carbon_price)) * (1.0 - damage) + rng.normal(0, 0.6, n)
    return Dataset(
        name="synthetic-policy",
        series={
            "emissions": np.clip(emissions, 0, None),
            "temperature": temperature,
            "gdp": gdp,
        },
        synthetic=True,
        note="SYNTHETIC fallback — replace with real data (issue: sourcing datasets).",
        meta={"carbon_price": carbon_price, "seed": seed},
    )


def synthetic_decoupled_series(n: int = 30, seed: int = 0, carbon_price: float = 50.0) -> Dataset:
    """A synthetic **negative control**: GDP is *independent* of emissions (no coupling in the DGP).

    Emissions still evolve, but GDP is a flat noisy process. A coupled predictor that imposes a
    climate→economy damage feedback should therefore **fail to beat** an economy-only baseline
    here — i.e. synergy Δ ≤ 0 and the coupling is correctly **cut**. Pairing this with
    :func:`synthetic_policy_series` validates the *method*: synergy detected when present, cut when
    absent (docs/polyphony/04-validation.md).
    """
    rng = np.random.default_rng(seed)
    t = np.arange(n)
    emissions = 80.0 * (1.0 - 0.01 * t) + rng.normal(0, 1.5, n)
    gdp = 100.0 + rng.normal(0, 0.6, n)  # independent of emissions/carbon price
    return Dataset(
        name="synthetic-decoupled",
        series={"emissions": np.clip(emissions, 0, None), "gdp": gdp},
        synthetic=True,
        note="SYNTHETIC negative control — GDP independent of emissions (no coupling).",
        meta={"carbon_price": carbon_price, "seed": seed, "coupling": False},
    )


def synthetic_pandemic_series(n: int = 40, seed: int = 0, r0: float = 2.5) -> Dataset:
    """Synthetic Macro⇄Health target: GDP dips during an SIR epidemic wave, then recovers.

    Generated with the same reduced-form SIR the epidemic voice uses (so a matching health-coupled
    predictor *can* track the dip), while an economy-only baseline (flat GDP) cannot. Its negative
    control is :func:`synthetic_decoupled_series` (GDP independent of the epidemic). SYNTHETIC — proves
    the coupling machinery, not real pandemic-economics skill.
    """
    rng = np.random.default_rng(seed)
    s, i, r, gamma = 0.999, 0.001, 0.0, 0.2
    penalty = np.empty(n)
    infected = np.empty(n)
    for t in range(n):
        beta = r0 * gamma
        new_inf = beta * s * i
        s = max(s - new_inf, 0.0)
        i = max(i + new_inf - gamma * i, 0.0)
        r = r + gamma * i
        penalty[t] = min(2.0 * i, 0.6)
        infected[t] = i
    gdp = 100.0 * (1.0 - penalty) + rng.normal(0, 0.6, n)
    return Dataset(
        name="synthetic-pandemic",
        series={"gdp": gdp, "infected": infected},
        synthetic=True,
        note="SYNTHETIC Macro⇄Health target (SIR-driven GDP dip).",
        meta={"r0": r0, "seed": seed, "coupling": True},
    )


def synthetic_food_series(n: int = 40, seed: int = 0, carbon_price: float = 0.0) -> Dataset:
    """Synthetic Land⇄Climate⇄Food target: food price rises as warming cuts crop yield.

    Emissions → cumulative warming → yield loss → higher food price (matched to the reduced-form land
    voice so a climate-coupled predictor can track it; a climate-blind baseline predicts a flat price).
    Negative control: :func:`synthetic_flat_food_series`. SYNTHETIC — machinery, not real skill.
    """
    rng = np.random.default_rng(seed)
    t = np.arange(n)
    emissions = 80.0 * np.exp(-0.02 * carbon_price) * (1.0 - 0.01 * t)
    temperature = 0.001 * np.cumsum(np.clip(emissions, 0, None))
    yld = np.clip(1.0 - 0.1 * temperature, 0.2, None)
    price = 100.0 / yld + rng.normal(0, 0.5, n)
    return Dataset(
        name="synthetic-food",
        series={"food_price": price, "temperature": temperature},
        synthetic=True,
        note="SYNTHETIC Land⇄Climate⇄Food target (warming raises food price).",
        meta={"carbon_price": carbon_price, "seed": seed, "coupling": True},
    )


def synthetic_flat_food_series(n: int = 40, seed: int = 0) -> Dataset:
    """Negative control for the food loop: food price independent of climate (flat + noise)."""
    rng = np.random.default_rng(seed)
    return Dataset(
        name="synthetic-flat-food",
        series={"food_price": 100.0 + rng.normal(0, 0.5, n)},
        synthetic=True,
        note="SYNTHETIC negative control — food price independent of climate.",
        meta={"carbon_price": 0.0, "seed": seed, "coupling": False},
    )


def synthetic_cobenefit_series(n: int = 40, seed: int = 0, carbon_price: float = 100.0) -> Dataset:
    """Synthetic Urban⇄Transport⇄Energy⇄Health target: a carbon price cuts traffic PM2.5 and thus mortality.

    Matched to the reduced-form transport + air-quality voices — carbon price → lower vehicle-km → lower
    ambient ``pm25`` → lower ``health_burden`` (excess mortality) via a log-linear concentration-response
    (Dockery 1993; Burnett 2018 GEMM). A policy-blind baseline (constant reference exposure) predicts a
    flat burden and cannot track the co-benefit. Negative control: :func:`synthetic_flat_health_series`.
    SYNTHETIC — proves the coupling machinery, not real air-quality-health skill.
    """
    rng = np.random.default_rng(seed)
    target = 100.0 * np.exp(-0.4 * carbon_price / 100.0)  # price-implied long-run vehicle-km
    vkt = np.empty(n)
    v = 100.0  # start at the pre-policy baseline; travel behaviour adjusts gradually (inertia)
    for k in range(n):
        v = v + 0.15 * (target - v)
        vkt[k] = v
    pm25 = 8.0 + 0.20 * vkt
    burden = 100.0 * (np.exp(0.02 * np.clip(pm25 - 5.0, 0.0, None)) - 1.0) + rng.normal(0, 0.4, n)
    return Dataset(
        name="synthetic-cobenefit",
        series={"health_burden": burden, "pm25": pm25},
        synthetic=True,
        note="SYNTHETIC Urban⇄Transport⇄Energy⇄Health target (carbon price cuts PM2.5 and mortality).",
        meta={"carbon_price": carbon_price, "seed": seed, "coupling": True},
    )


def synthetic_flat_health_series(n: int = 40, seed: int = 0) -> Dataset:
    """Negative control for the co-benefits loop: mortality burden independent of policy (flat + noise)."""
    rng = np.random.default_rng(seed)
    burden = 55.0 + rng.normal(0, 0.4, n)
    return Dataset(
        name="synthetic-flat-health",
        series={"health_burden": burden, "pm25": 30.0 + rng.normal(0, 0.4, n)},
        synthetic=True,
        note="SYNTHETIC negative control — mortality burden independent of transport policy.",
        meta={"carbon_price": 0.0, "seed": seed, "coupling": False},
    )


def synthetic_leakage_series(n: int = 40, seed: int = 0, openness: float = 0.6) -> Dataset:
    """Synthetic Trade⇄Emissions target: consumption-based emissions diverge above production as trade opens.

    Production emissions are ~flat (a fixed policy), but globalisation builds an embodied-carbon leakage
    channel over time, so **consumption-based** emissions rise above production — the carbon-leakage gap. A
    leakage-blind baseline (consumption = production ⇒ flat) cannot track the divergence. Negative control:
    :func:`synthetic_no_leakage_series` (openness 0). SYNTHETIC — proves the coupling machinery, not skill.
    """
    rng = np.random.default_rng(seed)
    production = 80.0
    o, leak = 0.0, np.empty(n)
    for k in range(n):
        o = o + 0.15 * (openness - o)
        leak[k] = 0.5 * o
    consumption = production * (1.0 + leak) + rng.normal(0, 0.4, n)
    return Dataset(
        name="synthetic-leakage",
        series={"consumption_emissions": consumption, "leakage_frac": leak},
        synthetic=True,
        note="SYNTHETIC Trade⇄Emissions target (carbon leakage lifts consumption above production).",
        meta={"openness": openness, "seed": seed, "coupling": True},
    )


def synthetic_no_leakage_series(n: int = 40, seed: int = 0) -> Dataset:
    """Negative control for the trade loop: consumption = production (no leakage; flat + noise)."""
    rng = np.random.default_rng(seed)
    return Dataset(
        name="synthetic-no-leakage",
        series={"consumption_emissions": 80.0 + rng.normal(0, 0.4, n), "leakage_frac": np.zeros(n)},
        synthetic=True,
        note="SYNTHETIC negative control — consumption emissions equal production (no carbon leakage).",
        meta={"openness": 0.0, "seed": seed, "coupling": False},
    )


def synthetic_financial_crisis_series(n: int = 40, seed: int = 0, credit_shock: float = 0.3) -> Dataset:
    """Synthetic Macro⇄Finance target: GDP dips during a financial-accelerator crisis wave, then recovers.

    Generated with the same leverage-cycle the finance voice uses (a credit shock is amplified into a
    boom-bust hump of ``output_penalty``), so a matching finance-coupled predictor *can* track the dip
    while an economy-only baseline (flat GDP) cannot. Negative control: :func:`synthetic_decoupled_series`
    (GDP independent of finance). SYNTHETIC — proves the coupling machinery, not real macro-finance skill.
    """
    rng = np.random.default_rng(seed)
    a = 0.95  # matches ReducedFormFinance.DECAY: stress ∝ t·aᵗ, a smooth delayed crisis hump
    xpeak = (1.0 / (-np.log(a))) * np.exp(-1.0)
    t = np.arange(n, dtype=float)
    x = t * a**t  # t·aᵗ
    spread = np.clip(credit_shock * x / xpeak, 0.0, 0.5)
    gdp = 100.0 * (1.0 - spread) + rng.normal(0, 0.6, n)
    return Dataset(
        name="synthetic-financial-crisis",
        series={"gdp": gdp, "credit_spread": spread},
        synthetic=True,
        note="SYNTHETIC Macro⇄Finance target (financial-accelerator crisis drags GDP).",
        meta={"credit_shock": credit_shock, "seed": seed, "coupling": True},
    )


def synthetic_nexus_series(n: int = 40, seed: int = 0, precipitation: float = 0.7) -> Dataset:
    """Synthetic Water⇄Energy⇄Food nexus target: a sustained drought raises food price over time.

    Matched to the reduced-form water + nexus-food voices — precipitation < demand drains a buffer store,
    water stress rises (and saturates), irrigation-dependent yield falls and pumping energy rises, so food
    price climbs then plateaus. A water-blind baseline (no stress) predicts a flat price and cannot track
    the drought. Negative control: :func:`synthetic_flat_nexus_series`. SYNTHETIC — proves the coupling
    machinery, not real nexus skill.
    """
    rng = np.random.default_rng(seed)
    store, stress = 2.0, np.empty(n)
    for k in range(n):
        store = min(max(store + precipitation - 1.0, 0.0), 2.0)
        stress[k] = min(max(1.0 - store / 2.0, 0.0), 1.0)
    yld = np.clip(1.0 - 0.6 * stress, 0.2, None)
    price = 100.0 / yld * (1.0 + 0.15 * stress) + rng.normal(0, 0.4, n)
    return Dataset(
        name="synthetic-nexus",
        series={"food_price": price, "water_stress": stress},
        synthetic=True,
        note="SYNTHETIC Water⇄Energy⇄Food nexus target (drought raises food price).",
        meta={"precipitation": precipitation, "seed": seed, "coupling": True},
    )


def synthetic_flat_nexus_series(n: int = 40, seed: int = 0) -> Dataset:
    """Negative control for the nexus loop: food price independent of water (flat + noise)."""
    rng = np.random.default_rng(seed)
    return Dataset(
        name="synthetic-flat-nexus",
        series={"food_price": 100.0 + rng.normal(0, 0.4, n), "water_stress": rng.normal(0, 0.01, n)},
        synthetic=True,
        note="SYNTHETIC negative control — food price independent of water stress.",
        meta={"precipitation": 1.0, "seed": seed, "coupling": False},
    )


def load(name: str = "synthetic") -> Dataset:
    """Load dataset ``name`` from datasets/ if a CSV exists, else the synthetic fallback."""
    path = DATASETS / f"{name}.csv"
    if path.exists():
        return load_csv(path)
    return synthetic_policy_series()


REAL_GDP_CO2 = DATASETS / "real_gdp_co2.csv"
REAL_FOOD = DATASETS / "real_food.csv"
REAL_COBENEFIT = DATASETS / "real_cobenefit.csv"
REAL_NEXUS = DATASETS / "real_nexus.csv"
REAL_FINANCE = DATASETS / "real_finance.csv"
REAL_TRADE = DATASETS / "real_trade.csv"
REAL_LEAKAGE_PANEL = DATASETS / "real_leakage_panel.csv"
REAL_PM25_MORTALITY_PANEL = DATASETS / "real_pm25_mortality_panel.csv"
REAL_INFLATION = DATASETS / "real_inflation.csv"
REAL_INFLATION_Q = DATASETS / "real_inflation_q.csv"
REAL_HOUSING = DATASETS / "real_housing.csv"


def has_real_gdp_co2() -> bool:
    """Whether the real World-Bank-GDP / OWID-CO₂ CSV has been fetched (``data.fetch_real``)."""
    return REAL_GDP_CO2.exists()


def has_real_food() -> bool:
    """Whether the real cereal-yield / temperature CSV has been fetched (``data.fetch_real.fetch_food``)."""
    return REAL_FOOD.exists()


def has_real_cobenefit() -> bool:
    """Whether the real PM2.5 / death-rate CSV has been fetched (``data.fetch_real.fetch_cobenefit``)."""
    return REAL_COBENEFIT.exists()


def has_real_nexus() -> bool:
    """Whether the real food / energy price-index CSV has been fetched (``data.fetch_real.fetch_nexus``)."""
    return REAL_NEXUS.exists()


def has_real_finance() -> bool:
    """Whether the real credit-spread / GDP CSV has been fetched (``data.fetch_real.fetch_finance``)."""
    return REAL_FINANCE.exists()


def has_real_trade() -> bool:
    """Whether the real UK production/consumption-CO₂ + openness CSV has been fetched (``fetch_real.fetch_trade``)."""
    return REAL_TRADE.exists()


def has_real_inflation() -> bool:
    """Whether the real energy-price / CPI CSV has been fetched (``fetch_real.fetch_inflation``)."""
    return REAL_INFLATION.exists()


def has_real_inflation_q() -> bool:
    """Whether the quarterly energy-price / CPI CSV has been fetched (``fetch_real.fetch_inflation_quarterly``)."""
    return REAL_INFLATION_Q.exists()


def load_real_inflation_q() -> Dataset:
    """REAL quarterly Energy⇄Inflation series: IMF Global Energy price index + US CPI (FRED), quarterly means.

    More observations than the annual series ⇒ more walk-forward folds for a higher-power confirmation of the
    keep. Series are in chronological order. Raises if the CSV is absent — call ``data.fetch_real``.
    """
    if not REAL_INFLATION_Q.exists():
        raise FileNotFoundError(f"{REAL_INFLATION_Q} missing; run `python -m polyphony.data.fetch_real`")
    raw = load_csv(REAL_INFLATION_Q)
    return Dataset(
        name="real-inflation-quarterly",
        series={"energy": raw.column("energy"), "cpi": raw.column("cpi")},
        synthetic=False,
        note="REAL quarterly IMF Global Energy price index (FRED PNRGINDEXM) + US CPI (CPIAUCSL).",
        meta={"frequency": "quarterly"},
    )


def has_real_housing() -> bool:
    """Whether the real mortgage-rate / house-price CSV has been fetched (``fetch_real.fetch_housing``)."""
    return REAL_HOUSING.exists()


def load_real_housing() -> Dataset:
    """REAL Interest-Rate⇄Housing series: 30-yr mortgage rate (FRED MORTGAGE30US) + Case-Shiller HPI.

    The tournament derives house-price growth from the HPI and tests the **lagged** rate against it (rates
    and growth co-move contemporaneously via reverse causation). Raises if the CSV is absent.
    """
    if not REAL_HOUSING.exists():
        raise FileNotFoundError(f"{REAL_HOUSING} missing; run `python -m polyphony.data.fetch_real`")
    raw = load_csv(REAL_HOUSING)
    return Dataset(
        name="real-housing",
        series={"year": raw.column("year"), "rate": raw.column("rate"), "hpi": raw.column("hpi")},
        synthetic=False,
        note="REAL 30-yr mortgage rate (FRED MORTGAGE30US) + Case-Shiller national HPI (CSUSHPINSA), annual.",
        meta={"source_rate": "FRED MORTGAGE30US", "source_hpi": "FRED CSUSHPINSA"},
    )


def load_real_inflation() -> Dataset:
    """REAL Energy⇄Inflation series: IMF Global Energy price index (FRED PNRGINDEXM) + US CPI (CPIAUCSL).

    The tournament derives energy-price growth and CPI inflation from these levels. Raises if the CSV is
    absent — call ``data.fetch_real``.
    """
    if not REAL_INFLATION.exists():
        raise FileNotFoundError(f"{REAL_INFLATION} missing; run `python -m polyphony.data.fetch_real`")
    raw = load_csv(REAL_INFLATION)
    return Dataset(
        name="real-inflation",
        series={"year": raw.column("year"), "energy": raw.column("energy"), "cpi": raw.column("cpi")},
        synthetic=False,
        note="REAL IMF Global Energy price index (FRED PNRGINDEXM) + US CPI (FRED CPIAUCSL), annual means.",
        meta={"source_energy": "FRED PNRGINDEXM", "source_cpi": "FRED CPIAUCSL"},
    )


def _load_panel_csv(path: pathlib.Path, col_a: str, col_b: str) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """Load a panel CSV with an ``iso`` (str), ``year`` (int), and two float columns → four arrays."""
    if not path.exists():
        raise FileNotFoundError(f"{path} missing; run `python -m polyphony.data.fetch_real`")
    iso: list[str] = []
    year: list[int] = []
    a: list[float] = []
    b: list[float] = []
    with path.open(newline="", encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            iso.append(row["iso"])
            year.append(int(row["year"]))
            a.append(float(row[col_a]))
            b.append(float(row[col_b]))
    return (
        np.asarray(iso, dtype=object),
        np.asarray(year, dtype=int),
        np.asarray(a, dtype=float),
        np.asarray(b, dtype=float),
    )


def has_real_leakage_panel() -> bool:
    """Whether the multi-country carbon-leakage panel has been fetched (``fetch_real.fetch_leakage_panel``)."""
    return REAL_LEAKAGE_PANEL.exists()


def load_real_leakage_panel() -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """REAL multi-country carbon-leakage panel: ``(iso, year, cons_prod_ratio, openness)`` arrays."""
    return _load_panel_csv(REAL_LEAKAGE_PANEL, "cons_prod_ratio", "openness")


def has_real_pm25_mortality_panel() -> bool:
    """Whether the PM2.5 / mortality panel has been fetched (``fetch_real.fetch_pm25_mortality_panel``)."""
    return REAL_PM25_MORTALITY_PANEL.exists()


def load_real_pm25_mortality_panel() -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """REAL multi-country PM2.5 / all-cause-mortality panel: ``(iso, year, pm25, death_rate)`` arrays."""
    return _load_panel_csv(REAL_PM25_MORTALITY_PANEL, "pm25", "death_rate")


def load_real_trade() -> Dataset:
    """REAL Trade⇄Emissions series (United Kingdom): OWID production + consumption CO₂ + WB trade openness.

    The UK is the textbook carbon-leakage case. ``openness`` is an **independent** leakage driver (using the
    observed gap would be circular). Raises if the CSV is absent — call ``data.fetch_real``.
    """
    if not REAL_TRADE.exists():
        raise FileNotFoundError(f"{REAL_TRADE} missing; run `python -m polyphony.data.fetch_real`")
    raw = load_csv(REAL_TRADE)
    return Dataset(
        name="real-trade",
        series={
            "year": raw.column("year"),
            "production_co2": raw.column("production_co2"),
            "consumption_co2": raw.column("consumption_co2"),
            "openness": raw.column("openness"),
        },
        synthetic=False,
        note="REAL United Kingdom OWID production + consumption CO₂ + World Bank trade openness "
        "(NE.TRD.GNFS.ZS), merged by year — the classic carbon-leakage case.",
        meta={"country": "United Kingdom", "source_co2": "OWID", "source_openness": "World Bank NE.TRD.GNFS.ZS"},
    )


def load_real_finance() -> Dataset:
    """REAL Macro⇄Finance series: Baa−10Y credit spread (FRED BAA10Y) + real GDP (FRED GDPC1), annual.

    Tests the financial-accelerator mechanism (credit stress → weaker output). ``gdp`` is the real GDP
    level; the tournament derives annual growth from it. Raises if the CSV is absent — call ``data.fetch_real``.
    """
    if not REAL_FINANCE.exists():
        raise FileNotFoundError(f"{REAL_FINANCE} missing; run `python -m polyphony.data.fetch_real`")
    raw = load_csv(REAL_FINANCE)
    return Dataset(
        name="real-finance",
        series={"year": raw.column("year"), "gdp": raw.column("gdp"), "spread": raw.column("spread")},
        synthetic=False,
        note="REAL Baa−10Y credit spread (FRED BAA10Y) + real GDP (FRED GDPC1), annual means, merged by year.",
        meta={"source_spread": "FRED BAA10Y", "source_gdp": "FRED GDPC1"},
    )


def load_real_nexus() -> Dataset:
    """REAL Water⇄Energy⇄Food nexus series: IMF Global Food and Energy price indices (FRED), annual means.

    Tests the nexus's energy→food leg (fertilizer/fuel/pumping pass-through). A clean global water-scarcity
    driver is not readily available annually, so this is a *partial* nexus test (energy pillar). Raises if
    the CSV is absent — call ``data.fetch_real``.
    """
    if not REAL_NEXUS.exists():
        raise FileNotFoundError(f"{REAL_NEXUS} missing; run `python -m polyphony.data.fetch_real`")
    raw = load_csv(REAL_NEXUS)
    return Dataset(
        name="real-nexus",
        series={
            "year": raw.column("year"),
            "food_price": raw.column("food_price"),
            "energy_price": raw.column("energy_price"),
        },
        synthetic=False,
        note="REAL IMF Global Food Price Index (FRED PFOODINDEXM) + Energy Price Index (PNRGINDEXM), "
        "annual means, merged by year.",
        meta={
            "source_food": "IMF Global Food Price Index (FRED PFOODINDEXM)",
            "source_energy": "IMF Global Energy Price Index (FRED PNRGINDEXM)",
        },
    )


def load_real_cobenefit() -> Dataset:
    """REAL Urban⇄Transport⇄Energy⇄Health series: World Bank world PM2.5 exposure + all-cause death rate.

    The co-benefits voice models PM2.5 → higher mortality; this is the real exposure and an **independent**
    outcome (all-cause crude death rate, NOT GBD air-pollution mortality, which would be circular) to test
    that mechanism against, with a placebo control. Raises if the CSV is absent — call ``data.fetch_real``.
    """
    if not REAL_COBENEFIT.exists():
        raise FileNotFoundError(f"{REAL_COBENEFIT} missing; run `python -m polyphony.data.fetch_real`")
    raw = load_csv(REAL_COBENEFIT)
    return Dataset(
        name="real-cobenefit",
        series={"year": raw.column("year"), "pm25": raw.column("pm25"), "death_rate": raw.column("death_rate")},
        synthetic=False,
        note="REAL World Bank world PM2.5 mean exposure (EN.ATM.PM25.MC.M3) + all-cause crude death rate "
        "(SP.DYN.CDRT.IN, independent of PM2.5 to avoid circularity), merged by year.",
        meta={
            "source_pm25": "World Bank WLD EN.ATM.PM25.MC.M3",
            "source_death_rate": "World Bank WLD SP.DYN.CDRT.IN (all-cause, crude, per 1000)",
        },
    )


def load_real_food() -> Dataset:
    """REAL Land⇄Climate⇄Food series: World Bank world cereal yield (kg/ha) + Hadley temperature anomaly.

    The land voice models warming → lower yield → higher food price; this is the real yield to test that
    mechanism against, with a placebo control. Raises if the CSV is absent — call ``data.fetch_real``.
    """
    if not REAL_FOOD.exists():
        raise FileNotFoundError(f"{REAL_FOOD} missing; run `python -m polyphony.data.fetch_real`")
    raw = load_csv(REAL_FOOD)
    return Dataset(
        name="real-food",
        series={"year": raw.column("year"), "cereal_yield": raw.column("cereal_yield"), "temp": raw.column("temp")},
        synthetic=False,
        note="REAL World Bank world cereal yield (AG.YLD.CREL.KG) + OWID Hadley temperature anomaly, merged by year.",
        meta={"source_yield": "World Bank WLD AG.YLD.CREL.KG", "source_temp": "OWID Hadley Centre temperature anomaly (median)"},
    )


def load_real_gdp_co2() -> Dataset:
    """REAL world GDP (World Bank, constant 2015 US$) + global CO₂ (OWID), merged by year (issue #9).

    Not synthetic: this is historical data. ``gdp`` is indexed to 100 at the first year so it is
    commensurable with the reduced-form voices' base-100 tracks; ``co2`` is Mt CO₂/yr and ``cum_co2``
    its cumulative sum (a warming proxy). Raises if the CSV is absent — call ``data.fetch_real`` first.
    """
    if not REAL_GDP_CO2.exists():
        raise FileNotFoundError(f"{REAL_GDP_CO2} missing; run `python -m polyphony.data.fetch_real`")
    raw = load_csv(REAL_GDP_CO2)
    gdp = raw.column("gdp")
    co2 = raw.column("co2")
    gdp_index = 100.0 * gdp / gdp[0]
    series = {"year": raw.column("year"), "gdp": gdp_index, "co2": co2, "cum_co2": np.cumsum(co2)}
    if "temp" in raw.series:  # observed global temperature anomaly (°C), if the CSV carries it
        series["temp"] = raw.column("temp")
    return Dataset(
        name="real-gdp-co2",
        series=series,
        synthetic=False,
        note="REAL World Bank world GDP (NY.GDP.MKTP.KD) + OWID global CO₂ + Hadley temperature anomaly, merged by year; GDP indexed to 100.",
        meta={
            "source_gdp": "World Bank WLD NY.GDP.MKTP.KD",
            "source_co2": "OWID owid-co2-data World",
            "source_temp": "OWID Hadley Centre global temperature anomaly (median)",
        },
    )
