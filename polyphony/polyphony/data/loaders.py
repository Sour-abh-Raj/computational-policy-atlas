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


def load(name: str = "synthetic") -> Dataset:
    """Load dataset ``name`` from datasets/ if a CSV exists, else the synthetic fallback."""
    path = DATASETS / f"{name}.csv"
    if path.exists():
        return load_csv(path)
    return synthetic_policy_series()
