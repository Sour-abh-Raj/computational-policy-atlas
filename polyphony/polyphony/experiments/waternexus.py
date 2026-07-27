"""Water⇄Energy⇄Food nexus fifth synergy loop (issue #10).

Cited reason (why this coupling should exist): water, energy, and food are physically interdependent —
irrigation and hydropower both draw on water, pumping and desalination draw on energy, and food
production draws on both. The **nexus** framing (Hoff 2011, Bonn Nexus Conference; integrated tools like
[CLEWs](../model-families/water/clews.md)) argues these must be modeled jointly, because a drought
propagates into food *and* energy prices. We test the sharpest reduced-form leg: **water scarcity →
higher food price** (irrigation yield loss + pumping-energy surcharge).

We predict a **food-price** track two ways — a **water-coupled** ensemble (drought → water stress →
higher food price) vs a **water-blind** baseline (no stress ⇒ flat price) — and measure synergy on a
drought DGP vs a flat negative control. Fifth domain, same harness, same honesty bar: a synthetic keep
is machinery, not skill; the real-data placebo test is the eventual bar (tracked as the open gap, #10-real).
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

import numpy as np

from ..core.interface import Model
from ..core.orchestrator import Orchestrator
from ..data.loaders import Dataset, synthetic_flat_nexus_series, synthetic_nexus_series
from ..data.splits import time_blocked_split
from ..engines.calibration import calibrate_scale_offset, calibrated_track
from ..eval.metrics import mase
from ..models import ReducedFormNexusFood, ReducedFormWater
from ..tournament.synergy import SynergyResult, measure_synergy


def nexus_price_track(
    precipitation: float,
    steps: int,
    coupled: bool,
    resolve: str = "contemporaneous",
) -> np.ndarray:
    """Predicted food-price track. The coupled chain water→nexusfood is **acyclic**, so
    ``resolve='contemporaneous'`` (default) solves it in topological order within the step (ADR-0005)."""
    if coupled:
        voices: list[Model] = [ReducedFormWater(), ReducedFormNexusFood()]
        routing = {"water_stress": "water", "storage": "water", "food_price": "nexusfood"}
    else:
        voices = [ReducedFormNexusFood()]
        routing = {"food_price": "nexusfood"}
    dials = {"precipitation": precipitation, "irrigation_sensitivity": 0.6}
    mode: Literal["lagged", "contemporaneous"] = "contemporaneous" if resolve == "contemporaneous" else "lagged"
    r = Orchestrator(voices, routing).run(steps=steps, dials=dials, seed=1, resolve=mode)
    return np.array([r.history[t]["food_price"] for t in range(steps)], float)


@dataclass(frozen=True)
class WaterNexusResult:
    dataset: str
    coupled_error: float
    nexusfood_only_error: float
    synergy: SynergyResult


def backtest(dataset: Dataset, test_frac: float = 0.3) -> WaterNexusResult:
    y = dataset.column("food_price")
    n = len(y)
    precip = float(dataset.meta.get("precipitation", 1.0))
    te = time_blocked_split(n, test_frac).test
    coupled = nexus_price_track(precip, n, coupled=True)
    blind = nexus_price_track(precip, n, coupled=False)
    err_c = mase(y[te], coupled[te])
    err_b = mase(y[te], blind[te])
    return WaterNexusResult(dataset.name, err_c, err_b, measure_synergy(err_c, {"nexusfood_only": err_b}))


def run_two_regime_tournament(n: int = 40, seed: int = 0) -> dict[str, WaterNexusResult]:
    """Drought present (scarcity raises food price) vs a flat negative control (no coupling)."""
    return {
        "drought_regime": backtest(synthetic_nexus_series(n=n, seed=seed, precipitation=0.7)),
        "flat_regime": backtest(synthetic_flat_nexus_series(n=n, seed=seed)),
    }


@dataclass(frozen=True)
class WaterNexusCalibratedSynergyResult:
    """Nexus synergy re-scored after a **fair** affine calibration of BOTH sides (Iter 13 method).

    Give the water-blind baseline its *own* train-block affine fit; a level artifact would then vanish, a
    real coupling keeps a positive Δ. We also report the sign: the coupling assumes water stress RAISES
    food price, so a real signal needs corr(stress, price) > 0.
    """

    dataset: str
    coupled_cal_mase: float
    blind_cal_mase: float
    delta: float
    coupled_beats_naive: bool
    stress_price_corr: float

    @property
    def sign_as_assumed(self) -> bool:
        return self.stress_price_corr > 0.0

    def verdict(self) -> str:
        return "keep" if (self.delta > 0.05 and self.sign_as_assumed) else "cut"


def calibrated_synergy(dataset: Dataset, test_frac: float = 0.3) -> WaterNexusCalibratedSynergyResult:
    """Score coupled vs water-blind after each is affine-calibrated on the **train block only**."""
    y = dataset.column("food_price")
    n = len(y)
    precip = float(dataset.meta.get("precipitation", 1.0))
    split = time_blocked_split(n, test_frac)
    tr, te = split.train, split.test

    coupled = nexus_price_track(precip, n, coupled=True)
    blind = nexus_price_track(precip, n, coupled=False)
    ac, bc = calibrate_scale_offset(coupled[tr], y[tr])
    ab, bb = calibrate_scale_offset(blind[tr], y[tr])
    mc = mase(y[te], calibrated_track(coupled, ac, bc)[te])
    mb = mase(y[te], calibrated_track(blind, ab, bb)[te])
    stress = dataset.column("water_stress") if "water_stress" in dataset.series else np.zeros(n)
    corr = float(np.corrcoef(stress, y)[0, 1]) if np.std(stress) > 0 else 0.0
    return WaterNexusCalibratedSynergyResult(dataset.name, mc, mb, mb - mc, mc < 1.0, corr)
