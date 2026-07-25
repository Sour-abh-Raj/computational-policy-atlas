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


def load(name: str = "synthetic") -> Dataset:
    """Load dataset ``name`` from datasets/ if a CSV exists, else the synthetic fallback."""
    path = DATASETS / f"{name}.csv"
    if path.exists():
        return load_csv(path)
    return synthetic_policy_series()
