"""Macro⇄Finance sixth synergy loop (issue #11): does a financial-accelerator ⇄ economy coupling help?

Cited reason: financial conditions are a leading indicator of output — a credit crunch is amplified by
the leverage cycle (Bernanke-Gertler-Gilchrist 1999; Minsky) and drags GDP, and the excess bond premium
predicts activity out of sample (Gilchrist-Zakrajšek 2012). If any coupling should earn its keep on real
data, a financial-conditions→output channel is a strong candidate.

Predicts a GDP track two ways — a **finance-coupled** ensemble (a credit shock ⇒ output drag) vs an
**economy-only** baseline (no financial shock ⇒ flat GDP) — scores held-out MASE, and measures synergy on
a crisis DGP vs a decoupled negative control. Sixth domain, same harness. Structurally mirrors Macro⇄Health
(a shock voice feeding the economy), with a financial rather than epidemiological accelerator.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

import numpy as np

from ..core.combiner import combine
from ..core.interface import Model
from ..core.orchestrator import Orchestrator
from ..data.loaders import Dataset, synthetic_decoupled_series, synthetic_financial_crisis_series
from ..data.splits import time_blocked_split
from ..engines.calibration import calibrate_scale_offset, calibrated_track
from ..eval.metrics import mase
from ..models import DisequilibriumEconomy, EquilibriumEconomy, ReducedFormFinance
from ..tournament.synergy import SynergyResult, measure_synergy


def gdp_track(credit_shock: float, steps: int, coupled: bool, resolve: str = "contemporaneous") -> np.ndarray:
    """Predicted GDP track. The coupled chain finance→economy is **acyclic**, so
    ``resolve='contemporaneous'`` (default) solves it in topological order within the step (ADR-0005)."""
    if coupled:
        voices: list[Model] = [ReducedFormFinance(), EquilibriumEconomy(), DisequilibriumEconomy()]
        routing = {"output_penalty": "finance", "credit_spread": "finance", "demand": "cge", "gdp": "cge"}
    else:
        voices = [EquilibriumEconomy(), DisequilibriumEconomy()]
        routing = {"demand": "cge", "gdp": "cge"}
    dials = {"credit_shock": credit_shock}
    mode: Literal["lagged", "contemporaneous"] = "contemporaneous" if resolve == "contemporaneous" else "lagged"
    r = Orchestrator(voices, routing).run(steps=steps, dials=dials, seed=1, resolve=mode)
    return np.array([combine("gdp", r.answers_for("gdp", t)).weighted_mean for t in range(steps)], float)


@dataclass(frozen=True)
class MacroFinanceResult:
    dataset: str
    coupled_error: float
    econ_only_error: float
    synergy: SynergyResult


def backtest(dataset: Dataset, test_frac: float = 0.3) -> MacroFinanceResult:
    y = dataset.column("gdp")
    n = len(y)
    shock = float(dataset.meta.get("credit_shock", 0.0))
    te = time_blocked_split(n, test_frac).test
    coupled = gdp_track(shock, n, coupled=True)
    econ_only = gdp_track(shock, n, coupled=False)
    err_c = mase(y[te], coupled[te])
    err_e = mase(y[te], econ_only[te])
    return MacroFinanceResult(dataset.name, err_c, err_e, measure_synergy(err_c, {"economy_only": err_e}))


def run_two_regime_tournament(n: int = 40, seed: int = 0) -> dict[str, MacroFinanceResult]:
    """Crisis present (a credit shock drags GDP) vs a decoupled negative control (GDP independent)."""
    return {
        "crisis_regime": backtest(synthetic_financial_crisis_series(n=n, seed=seed, credit_shock=0.3)),
        "decoupled_regime": backtest(synthetic_decoupled_series(n=n, seed=seed)),
    }


@dataclass(frozen=True)
class MacroFinanceCalibratedSynergyResult:
    """Macro⇄Finance synergy re-scored after a **fair** affine calibration of BOTH sides (Iter 13 method).

    Give the economy-only baseline its own train-block affine fit; a level artifact vanishes, a real
    coupling keeps a positive Δ. The coupling assumes credit stress LOWERS gdp, so a real signal needs
    corr(credit_spread, gdp) < 0 (the sign discipline from Iter 18).
    """

    dataset: str
    coupled_cal_mase: float
    econ_cal_mase: float
    delta: float
    coupled_beats_naive: bool
    spread_gdp_corr: float

    @property
    def sign_as_assumed(self) -> bool:
        return self.spread_gdp_corr < 0.0

    def verdict(self) -> str:
        return "keep" if (self.delta > 0.05 and self.sign_as_assumed) else "cut"


def calibrated_synergy(dataset: Dataset, test_frac: float = 0.3) -> MacroFinanceCalibratedSynergyResult:
    """Score coupled vs economy-only after each is affine-calibrated on the **train block only**."""
    y = dataset.column("gdp")
    n = len(y)
    shock = float(dataset.meta.get("credit_shock", 0.0))
    split = time_blocked_split(n, test_frac)
    tr, te = split.train, split.test

    coupled = gdp_track(shock, n, coupled=True)
    econ = gdp_track(shock, n, coupled=False)
    ac, bc = calibrate_scale_offset(coupled[tr], y[tr])
    ae, be = calibrate_scale_offset(econ[tr], y[tr])
    mc = mase(y[te], calibrated_track(coupled, ac, bc)[te])
    me = mase(y[te], calibrated_track(econ, ae, be)[te])
    spread = dataset.column("credit_spread") if "credit_spread" in dataset.series else np.zeros(n)
    corr = float(np.corrcoef(spread, y)[0, 1]) if np.std(spread) > 0 else 0.0
    return MacroFinanceCalibratedSynergyResult(dataset.name, mc, me, me - mc, mc < 1.0, corr)
