"""Macro⇄Health second synergy loop (issue #8): does an epidemic ⇄ economy coupling earn its keep?

Predicts a GDP track two ways — a **health-coupled** ensemble (epidemic SIR + economics voices, so an
outbreak drags output) vs an **economy-only** baseline (no health shock) — scores held-out MASE, and
measures synergy on a coupled (pandemic) DGP vs a decoupled negative control. Mirrors the energy-slice
tournament, reusing the same harness (`tournament.synergy`) — the method is domain-general.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from ..core.combiner import combine
from ..core.interface import Model
from ..core.orchestrator import Orchestrator
from ..data.loaders import synthetic_decoupled_series, synthetic_pandemic_series
from ..data.splits import time_blocked_split
from ..eval.metrics import mase
from ..models import DisequilibriumEconomy, EquilibriumEconomy, ReducedFormEpidemic
from ..tournament.synergy import SynergyResult, measure_synergy


def gdp_track(r0: float, steps: int, coupled: bool) -> np.ndarray:
    if coupled:
        voices: list[Model] = [ReducedFormEpidemic(), EquilibriumEconomy(), DisequilibriumEconomy()]
        routing = {"output_penalty": "epidemic", "infected_frac": "epidemic", "demand": "cge", "gdp": "cge"}
    else:
        voices = [EquilibriumEconomy(), DisequilibriumEconomy()]
        routing = {"demand": "cge", "gdp": "cge"}
    r = Orchestrator(voices, routing).run(steps=steps, dials={"r0": r0}, seed=1)
    return np.array([combine("gdp", r.answers_for("gdp", t)).weighted_mean for t in range(steps)], float)


@dataclass(frozen=True)
class MacroHealthResult:
    dataset: str
    coupled_error: float
    econ_only_error: float
    synergy: SynergyResult


def backtest(dataset, test_frac: float = 0.3) -> MacroHealthResult:
    y = dataset.column("gdp")
    n = len(y)
    r0 = float(dataset.meta.get("r0", 2.5))
    te = time_blocked_split(n, test_frac).test
    coupled = gdp_track(r0, n, coupled=True)
    econ_only = gdp_track(r0, n, coupled=False)
    err_c = mase(y[te], coupled[te])
    err_e = mase(y[te], econ_only[te])
    return MacroHealthResult(dataset.name, err_c, err_e, measure_synergy(err_c, {"economy_only": err_e}))


def run_two_regime_tournament(n: int = 40, seed: int = 0) -> dict[str, MacroHealthResult]:
    return {
        "pandemic_regime": backtest(synthetic_pandemic_series(n=n, seed=seed, r0=2.5)),
        "no_pandemic_regime": backtest(synthetic_decoupled_series(n=n, seed=seed)),
    }
