"""Trade⇄Emissions seventh synergy loop (carbon leakage, issue #12).

Cited reason: a unilateral carbon price can shift emission-intensive production abroad, so a country's
**consumption-based** emissions fall less than its **production-based** emissions — the carbon-leakage /
pollution-haven hypothesis (Copeland-Taylor), central to border-carbon-adjustment policy. The gap is
**embodied carbon in trade** (measured by multi-regional input-output databases like EXIOBASE/Eora).

Predicts a **consumption-emissions** track two ways — a **trade-coupled** ensemble (energy production +
a trade voice that adds embodied imports as globalisation builds) vs a **leakage-blind** baseline
(consumption = production ⇒ flat) — and measures synergy on a leakage DGP vs a no-leakage control. Seventh
domain, same harness, same honesty bar: a synthetic keep is machinery; the real-data test (OWID
production vs consumption CO₂, whose gap is ``trade_co2``) is the eventual bar (issue #12-real).
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

import numpy as np

from ..core.interface import Model
from ..core.orchestrator import Orchestrator
from ..data.loaders import Dataset, synthetic_leakage_series, synthetic_no_leakage_series
from ..data.splits import time_blocked_split
from ..engines.calibration import calibrate_scale_offset, calibrated_track
from ..eval.metrics import mase
from ..models import ReducedFormEnergy, ReducedFormTrade
from ..tournament.synergy import SynergyResult, measure_synergy


def consumption_emissions_track(
    openness: float,
    steps: int,
    coupled: bool,
    carbon_price: float = 50.0,
    resolve: str = "contemporaneous",
) -> np.ndarray:
    """Predicted consumption-emissions track. The coupled chain energy→trade is **acyclic**, so
    ``resolve='contemporaneous'`` (default) solves it in topological order within the step (ADR-0005).
    The leakage-blind baseline assumes consumption = production (the energy voice's ``emissions``)."""
    dials = {"carbon_price": carbon_price, "openness": openness}
    if coupled:
        voices: list[Model] = [ReducedFormEnergy(), ReducedFormTrade()]
        routing = {"emissions": "energy", "consumption_emissions": "trade", "leakage_frac": "trade"}
        key = "consumption_emissions"
    else:
        voices = [ReducedFormEnergy()]
        routing = {"emissions": "energy"}
        key = "emissions"
    mode: Literal["lagged", "contemporaneous"] = "contemporaneous" if resolve == "contemporaneous" else "lagged"
    r = Orchestrator(voices, routing).run(steps=steps, dials=dials, seed=1, resolve=mode)
    return np.array([r.history[t][key] for t in range(steps)], float)


@dataclass(frozen=True)
class TradeEmissionsResult:
    dataset: str
    coupled_error: float
    blind_error: float
    synergy: SynergyResult


def backtest(dataset: Dataset, test_frac: float = 0.3) -> TradeEmissionsResult:
    y = dataset.column("consumption_emissions")
    n = len(y)
    openness = float(dataset.meta.get("openness", 0.0))
    te = time_blocked_split(n, test_frac).test
    coupled = consumption_emissions_track(openness, n, coupled=True)
    blind = consumption_emissions_track(openness, n, coupled=False)
    err_c = mase(y[te], coupled[te])
    err_b = mase(y[te], blind[te])
    return TradeEmissionsResult(dataset.name, err_c, err_b, measure_synergy(err_c, {"blind": err_b}))


def run_two_regime_tournament(n: int = 40, seed: int = 0) -> dict[str, TradeEmissionsResult]:
    """Leakage present (globalisation lifts consumption above production) vs a no-leakage control."""
    return {
        "leakage_regime": backtest(synthetic_leakage_series(n=n, seed=seed, openness=0.6)),
        "no_leakage_regime": backtest(synthetic_no_leakage_series(n=n, seed=seed)),
    }


@dataclass(frozen=True)
class TradeCalibratedSynergyResult:
    """Trade⇄Emissions synergy re-scored after a **fair** affine calibration of BOTH sides (Iter 13 method).

    Give the leakage-blind baseline its own train-block affine fit; a level artifact vanishes, a real
    coupling keeps a positive Δ. The coupling assumes leakage RAISES consumption above production, so a
    real signal needs corr(leakage_frac, consumption) > 0.
    """

    dataset: str
    coupled_cal_mase: float
    blind_cal_mase: float
    delta: float
    coupled_beats_naive: bool
    leakage_consumption_corr: float

    @property
    def sign_as_assumed(self) -> bool:
        return self.leakage_consumption_corr > 0.0

    def verdict(self) -> str:
        return "keep" if (self.delta > 0.05 and self.sign_as_assumed) else "cut"


def calibrated_synergy(dataset: Dataset, test_frac: float = 0.3) -> TradeCalibratedSynergyResult:
    """Score coupled vs leakage-blind after each is affine-calibrated on the **train block only**."""
    y = dataset.column("consumption_emissions")
    n = len(y)
    openness = float(dataset.meta.get("openness", 0.0))
    split = time_blocked_split(n, test_frac)
    tr, te = split.train, split.test

    coupled = consumption_emissions_track(openness, n, coupled=True)
    blind = consumption_emissions_track(openness, n, coupled=False)
    ac, bc = calibrate_scale_offset(coupled[tr], y[tr])
    ab, bb = calibrate_scale_offset(blind[tr], y[tr])
    mc = mase(y[te], calibrated_track(coupled, ac, bc)[te])
    mb = mase(y[te], calibrated_track(blind, ab, bb)[te])
    leak = dataset.column("leakage_frac") if "leakage_frac" in dataset.series else np.zeros(n)
    corr = float(np.corrcoef(leak, y)[0, 1]) if np.std(leak) > 0 else 0.0
    return TradeCalibratedSynergyResult(dataset.name, mc, mb, mb - mc, mc < 1.0, corr)
