"""Urban⇄Transport⇄Energy⇄Health fourth synergy loop (issue #7): the air-quality co-benefits channel.

Cited reason (why this coupling should exist): decarbonizing transport is not only a climate lever — by
cutting traffic-related fine particulate (PM2.5) it lowers premature mortality *now and locally*. This
**health co-benefit** is one of the best-documented cross-domain couplings in policy science (Haines et
al. 2009, *Lancet*; the Lancet Countdown), resting on concentration-response functions that are among the
most robust dose-response relationships in environmental epidemiology (Dockery et al. 1993 Harvard Six
Cities; Burnett et al. 2018 GEMM). If any coupling earns its keep, a well-identified co-benefit should.

We predict a **health-burden** (excess-mortality index) track two ways — a **transport-coupled** ensemble
(carbon price → lower vehicle-km → lower PM2.5 → lower mortality) vs a **policy-blind** air-health baseline
(constant reference exposure ⇒ flat burden) — and measure synergy on a coupled DGP vs a flat negative
control. Fourth domain, same harness, same honesty bar: a synthetic keep is *machinery*, not skill; the
real-data placebo test (real PM2.5 + mortality) is the eventual bar (tracked as the open real-data gap).
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

import numpy as np

from ..core.interface import Model
from ..core.orchestrator import Orchestrator
from ..data.loaders import Dataset, synthetic_cobenefit_series, synthetic_flat_health_series
from ..data.splits import time_blocked_split
from ..engines.calibration import calibrate_scale_offset, calibrated_track
from ..eval.metrics import mase
from ..models import ReducedFormAirHealth, ReducedFormTransport
from ..tournament.synergy import SynergyResult, measure_synergy


def health_burden_track(
    cp: float,
    steps: int,
    coupled: bool,
    resolve: str = "contemporaneous",
) -> np.ndarray:
    """Predicted health-burden track. The coupled chain transport→airhealth is **acyclic**, so
    ``resolve='contemporaneous'`` (default) solves it in topological order within the step — the health
    voice reads the same-step PM2.5 with no coupling lag (ADR-0005)."""
    if coupled:
        voices: list[Model] = [ReducedFormTransport(), ReducedFormAirHealth()]
        routing = {"vkt": "transport", "pm25": "transport", "health_burden": "airhealth"}
    else:
        voices = [ReducedFormAirHealth()]
        routing = {"health_burden": "airhealth"}
    dials = {"carbon_price": cp, "vkt_elasticity": 0.4, "crf_beta": 0.02}
    mode: Literal["lagged", "contemporaneous"] = "contemporaneous" if resolve == "contemporaneous" else "lagged"
    r = Orchestrator(voices, routing).run(steps=steps, dials=dials, seed=1, resolve=mode)
    return np.array([r.history[t]["health_burden"] for t in range(steps)], float)


@dataclass(frozen=True)
class UrbanHealthResult:
    dataset: str
    coupled_error: float
    airhealth_only_error: float
    synergy: SynergyResult


def backtest(dataset: Dataset, test_frac: float = 0.3) -> UrbanHealthResult:
    y = dataset.column("health_burden")
    n = len(y)
    cp = float(dataset.meta.get("carbon_price", 0.0))
    te = time_blocked_split(n, test_frac).test
    coupled = health_burden_track(cp, n, coupled=True)
    blind = health_burden_track(cp, n, coupled=False)
    err_c = mase(y[te], coupled[te])
    err_b = mase(y[te], blind[te])
    return UrbanHealthResult(dataset.name, err_c, err_b, measure_synergy(err_c, {"airhealth_only": err_b}))


def run_two_regime_tournament(n: int = 40, seed: int = 0) -> dict[str, UrbanHealthResult]:
    """Co-benefit present (carbon price cuts PM2.5→mortality) vs a flat negative control (no coupling)."""
    return {
        "cobenefit_regime": backtest(synthetic_cobenefit_series(n=n, seed=seed, carbon_price=100.0)),
        "flat_regime": backtest(synthetic_flat_health_series(n=n, seed=seed)),
    }


@dataclass(frozen=True)
class UrbanHealthCalibratedSynergyResult:
    """Co-benefits synergy re-scored after a **fair** affine calibration of BOTH sides (Iter 13 method).

    The decisive honesty test: give the policy-blind air-health baseline its *own* train-block affine fit
    — its strongest form — then ask whether the transport coupling *still* helps. A level artifact would
    be erased (as energy's was, Iter 12); a real coupling keeps a positive Δ. We also report the exposure
    sign: the coupling assumes more PM2.5 → more mortality, so a real co-benefit needs corr(pm25, burden)
    to be **positive** (Iter 18's sign discipline, learned when real crop yield had the wrong sign).
    """

    dataset: str
    coupled_cal_mase: float
    blind_cal_mase: float
    delta: float
    coupled_beats_naive: bool
    pm25_burden_corr: float

    @property
    def sign_as_assumed(self) -> bool:
        """The coupling assumes PM2.5 RAISES the mortality burden; true only if the correlation is positive."""
        return self.pm25_burden_corr > 0.0

    def verdict(self) -> str:
        return "keep" if (self.delta > 0.05 and self.sign_as_assumed) else "cut"


def calibrated_synergy(dataset: Dataset, test_frac: float = 0.3) -> UrbanHealthCalibratedSynergyResult:
    """Score coupled vs policy-blind after each is affine-calibrated on the **train block only**."""
    y = dataset.column("health_burden")
    n = len(y)
    cp = float(dataset.meta.get("carbon_price", 0.0))
    split = time_blocked_split(n, test_frac)
    tr, te = split.train, split.test

    coupled = health_burden_track(cp, n, coupled=True)
    blind = health_burden_track(cp, n, coupled=False)
    ac, bc = calibrate_scale_offset(coupled[tr], y[tr])
    ab, bb = calibrate_scale_offset(blind[tr], y[tr])
    mc = mase(y[te], calibrated_track(coupled, ac, bc)[te])
    mb = mase(y[te], calibrated_track(blind, ab, bb)[te])
    pm25 = dataset.column("pm25") if "pm25" in dataset.series else np.zeros(n)
    corr = float(np.corrcoef(pm25, y)[0, 1]) if np.std(pm25) > 0 else 0.0
    return UrbanHealthCalibratedSynergyResult(dataset.name, mc, mb, mb - mc, mc < 1.0, corr)
