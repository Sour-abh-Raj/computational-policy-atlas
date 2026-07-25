"""Scored tournament — probabilistic (CRPS/PIT) scoring of the parametric ensemble.

Moves beyond point MASE: scores the **ensemble distribution** with CRPS (proper), reports PIT
calibration, and measures coupled-vs-economy-only synergy **on CRPS** (blueprint §6/§7). Also runs a
calibration check (affine level fit on the train block) and reports — honestly — whether the
calibrated champion beats a naive forecast (MASE < 1).
"""

from __future__ import annotations

from dataclasses import dataclass

from ..data.loaders import Dataset
from ..data.splits import time_blocked_split
from ..engines.calibration import calibrate_scale_offset, calibrated_track
from ..eval.metrics import crps_series, mase, pit_values
from ..tournament.synergy import SynergyResult, measure_synergy
from .uncertainty import ensemble_gdp_tracks


@dataclass(frozen=True)
class ScoredResult:
    coupled_crps: float
    econ_crps: float
    coupled_mean_mase: float
    pit_mean: float
    synergy_crps: SynergyResult
    calibrated_mase: float
    beats_naive_after_calibration: bool


def scored_backtest(dataset: Dataset, members: int = 64, seed: int = 0) -> ScoredResult:
    y = dataset.column("gdp")
    n = len(y)
    cp = float(dataset.meta.get("carbon_price", 50.0))
    split = time_blocked_split(n)
    train, test = split.train, split.test

    coupled = ensemble_gdp_tracks(cp=cp, steps=n, members=members, seed=seed, coupled=True)
    econ = ensemble_gdp_tracks(cp=cp, steps=n, members=members, seed=seed, coupled=False)

    coupled_crps = crps_series(coupled[test], y[test])
    econ_crps = crps_series(econ[test], y[test])
    coupled_mean = coupled.mean(axis=1)
    coupled_mean_mase = mase(y[test], coupled_mean[test])
    pit_mean = float(pit_values(coupled[test], y[test]).mean())
    synergy = measure_synergy(coupled_crps, {"economy_only": econ_crps})

    # Calibration: affine level fit on TRAIN only, then score on TEST (honest, no leakage).
    a, b = calibrate_scale_offset(coupled_mean[train], y[train])
    cal = calibrated_track(coupled_mean, a, b)
    calibrated_mase = mase(y[test], cal[test])

    return ScoredResult(
        coupled_crps=coupled_crps,
        econ_crps=econ_crps,
        coupled_mean_mase=coupled_mean_mase,
        pit_mean=pit_mean,
        synergy_crps=synergy,
        calibrated_mase=calibrated_mase,
        beats_naive_after_calibration=calibrated_mase < 1.0,
    )
