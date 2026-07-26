"""First real tournament: does coupling energy⇄climate⇄economy earn its keep?

We predict a GDP track two ways and score both on a **held-out** block:

* **coupled** — the 4-voice ensemble (energy + climate + CGE + E3ME); the energy⇄climate⇄economy
  feedback is active. Point prediction = the disagreement combiner's skill-weighted mean of the
  economics voices' GDP.
* **economy-only** — the 2 economics voices with the feedback switched **off** (no energy/climate
  coupling: energy cost at base, zero climate damage). This is the "sum-of-parts" baseline.

Synergy Δ = economy-only error − coupled error (blueprint §7). We run it on **two synthetic
regimes**: one whose data-generating process *has* the coupling, one that does *not*. A correct
method must show **Δ > 0 when coupling is real** and **Δ ≤ 0 (cut) when it is not** — validating
the *method*, honestly separate from any claim of real-world skill (awaiting real data, issue #9).
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from ..core.combiner import combine
from ..core.interface import Model
from ..core.orchestrator import Orchestrator
from ..data.loaders import Dataset, synthetic_decoupled_series, synthetic_policy_series
from ..data.splits import time_blocked_split
from ..engines.calibration import calibrate_scale_offset, calibrated_track
from ..eval.metrics import mase
from ..models import (
    DisequilibriumEconomy,
    EquilibriumEconomy,
    ReducedFormClimate,
    ReducedFormEnergy,
)
from ..tournament.synergy import SynergyResult, measure_synergy


def gdp_track(carbon_price: float, steps: int, coupled: bool, tcre: float = 0.001) -> np.ndarray:
    """Predicted GDP track = skill-weighted mean of the economics voices' GDP each step."""
    voices: list[Model]
    if coupled:
        voices = [
            ReducedFormEnergy(),
            ReducedFormClimate(),
            EquilibriumEconomy(),
            DisequilibriumEconomy(),
        ]
        routing = {
            "energy_cost": "energy",
            "emissions": "energy",
            "temperature": "dice",
            "damage_frac": "dice",
            "demand": "cge",
            "gdp": "cge",
        }
    else:
        voices = [EquilibriumEconomy(), DisequilibriumEconomy()]
        routing = {"demand": "cge", "gdp": "cge"}
    orch = Orchestrator(voices, routing)
    r = orch.run(steps=steps, dials={"carbon_price": carbon_price, "tcre": tcre}, seed=1)
    return np.array(
        [combine("gdp", r.answers_for("gdp", t)).weighted_mean for t in range(steps)], float
    )


@dataclass(frozen=True)
class BacktestResult:
    dataset: str
    coupled_error: float
    econ_only_error: float
    synergy: SynergyResult

    def as_row(self) -> dict:
        return {
            "dataset": self.dataset,
            "coupled_mase": self.coupled_error,
            "econ_only_mase": self.econ_only_error,
            "synergy_delta": self.synergy.delta,
            "verdict": self.synergy.verdict(),
        }


def backtest_gdp(dataset: Dataset, test_frac: float = 0.3) -> BacktestResult:
    y = dataset.column("gdp")
    n = len(y)
    cp = float(dataset.meta.get("carbon_price", 50.0))
    split = time_blocked_split(n, test_frac)
    te = split.test

    coupled = gdp_track(cp, n, coupled=True)
    econ_only = gdp_track(cp, n, coupled=False)
    err_coupled = mase(y[te], coupled[te])
    err_econ = mase(y[te], econ_only[te])
    syn = measure_synergy(err_coupled, {"economy_only": err_econ})
    return BacktestResult(dataset.name, err_coupled, err_econ, syn)


def run_two_regime_tournament(n: int = 40, seed: int = 0) -> dict[str, BacktestResult]:
    """Run the backtest on the coupled and decoupled synthetic regimes."""
    coupled_regime = backtest_gdp(synthetic_policy_series(n=n, seed=seed, carbon_price=50.0))
    decoupled_regime = backtest_gdp(synthetic_decoupled_series(n=n, seed=seed, carbon_price=50.0))
    return {"coupled_regime": coupled_regime, "decoupled_regime": decoupled_regime}


@dataclass(frozen=True)
class CalibratedSynergyResult:
    """The energy synergy re-scored **after a fair affine calibration of BOTH sides**.

    The Round-1 synergy (+2.22) was measured on *raw* reduced-form tracks whose levels are miscalibrated
    (MASE ≈ 8, worse than naive). The honest test gives the **economy-only baseline its own** train-block
    affine fit too — its strongest form — then asks whether the coupling *still* helps. If the advantage
    was merely a level artifact, a calibrated baseline erases it and Δ collapses to ≈ 0 ⇒ **cut**.
    """

    dataset: str
    coupled_cal_mase: float
    econ_cal_mase: float
    delta: float
    coupled_beats_naive: bool

    def verdict(self) -> str:
        # A real coupling must still beat the *calibrated* sum-of-parts by a non-trivial margin.
        return "keep" if self.delta > 0.05 else "cut"


def calibrated_synergy(dataset: Dataset, test_frac: float = 0.3) -> CalibratedSynergyResult:
    """Score coupled vs economy-only after each is affine-calibrated on the **train block only**."""
    y = dataset.column("gdp")
    n = len(y)
    cp = float(dataset.meta.get("carbon_price", 50.0))
    split = time_blocked_split(n, test_frac)
    tr, te = split.train, split.test

    coupled = gdp_track(cp, n, coupled=True)
    econ = gdp_track(cp, n, coupled=False)
    ac, bc = calibrate_scale_offset(coupled[tr], y[tr])
    ae, be = calibrate_scale_offset(econ[tr], y[tr])
    mc = mase(y[te], calibrated_track(coupled, ac, bc)[te])
    me = mase(y[te], calibrated_track(econ, ae, be)[te])
    return CalibratedSynergyResult(dataset.name, mc, me, me - mc, mc < 1.0)
