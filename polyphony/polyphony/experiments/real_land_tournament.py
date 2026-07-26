"""Real Land⇄Climate⇄Food tournament (closes the last convergence gap, issue #9/#6).

The land voice models **warming → lower crop yield → higher food price**. On synthetic data that coupling
was *kept* (Δ+15, Iter 13). Here we test it on **real** World Bank world cereal yield (kg/ha) vs the
observed Hadley temperature anomaly. Two honest checks:

1. **Placebo control** — a warming-damage term ``(1 − k·temp²)`` fit on train vs the SAME form driven by a
   generic time trend. The coupling is kept only if it beats the trend baseline **and** the placebo.
2. **Sign check** — the coupling *assumes* warming lowers yield (negative correlation). We report the
   actual real correlation, because a positive one means the reduced-form mechanism has the **wrong
   sign** on aggregate data (technology/Green-Revolution gains dominate historical yield).
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from ..data.loaders import load_real_food
from ..data.splits import time_blocked_split
from ..eval.metrics import mase
from .real_tournament import _damage_fit_predict, _fit_log_trend


@dataclass(frozen=True)
class RealLandResult:
    n_years: int
    econ_mase: float
    coupled_mase: float
    placebo_mase: float
    temp_yield_corr: float

    @property
    def synergy_delta(self) -> float:
        return self.econ_mase - self.coupled_mase

    @property
    def beats_placebo(self) -> bool:
        return self.coupled_mase < self.placebo_mase

    @property
    def sign_as_assumed(self) -> bool:
        """The coupling assumes warming LOWERS yield; true only if the real correlation is negative."""
        return self.temp_yield_corr < 0.0

    def verdict(self) -> str:
        return "keep" if (self.synergy_delta > 0.05 and self.beats_placebo and self.sign_as_assumed) else "cut"


def run_real_land_tournament(test_frac: float = 0.3) -> RealLandResult:
    ds = load_real_food()
    y = ds.column("cereal_yield")
    temp = ds.column("temp")
    n = len(y)
    t = np.arange(n, dtype=float)
    split = time_blocked_split(n, test_frac)
    tr, te = split.train, split.test

    a, b = _fit_log_trend(y[tr], t[tr])
    trend = np.exp(a * t + b)

    temp_rebased = temp - float(temp[tr][0])
    scale = temp_rebased[tr][-1] if temp_rebased[tr][-1] != 0 else 1.0
    coupled, _ = _damage_fit_predict(y, trend, temp_rebased / scale, tr)

    placebo, _ = _damage_fit_predict(y, trend, (t / t[tr][-1]) ** 1.5, tr)

    return RealLandResult(
        n_years=n,
        econ_mase=mase(y[te], trend[te]),
        coupled_mase=mase(y[te], coupled[te]),
        placebo_mase=mase(y[te], placebo[te]),
        temp_yield_corr=float(np.corrcoef(temp, y)[0, 1]),
    )
