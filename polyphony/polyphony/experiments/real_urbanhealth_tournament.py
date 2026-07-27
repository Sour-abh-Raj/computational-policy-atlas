"""Real Urban⇄Transport⇄Energy⇄Health tournament (closes the Iter-19 gap, issue #7-real).

The air-quality voice models **more PM2.5 → higher mortality**. On synthetic data that coupling was
*kept* (fair-calibrated Δ+13.5, Iter 19). Here we test it on **real** World Bank world PM2.5 exposure
(µg/m³) vs an **independent** all-cause crude death rate (per 1000), 1990–2023.

Three honesty checks, the same bar every other real-data coupling faced:

1. **Non-circular outcome.** The outcome is *all-cause* mortality, NOT GBD "mortality attributed to
   ambient PM2.5" — the latter is *computed from* PM2.5 by a concentration-response function, so it would
   confirm the mechanism by construction. Independence is what makes the test able to fail.
2. **Placebo control.** A hazard term ``(1 + k·pm25)`` (k ≥ 0, the assumed direction) fit on train, vs
   the SAME form driven by a generic time trend. The coupling is kept only if PM2.5 beats the trend
   baseline **and** the placebo.
3. **Sign / confounding.** We report the raw correlation *and* the fitted partial coefficient: a positive
   raw correlation that vanishes once a trend is removed (k→0) is confounding, not a co-benefit.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from ..data.loaders import load_real_cobenefit
from ..data.splits import time_blocked_split
from ..eval.metrics import mase
from .real_tournament import _fit_log_trend


def _hazard_fit_predict(y: np.ndarray, trend: np.ndarray, reg: np.ndarray, tr: slice) -> tuple[np.ndarray, float]:
    """Fit ``y ≈ trend·(1 + k·z)`` on train with k ≥ 0, where ``z`` is ``reg`` standardized on the train
    block. k ≥ 0 encodes the coupling's assumed direction (more exposure ⇒ more mortality): if the
    train-block partial relationship is non-positive, k clamps to 0 and the coupling adds nothing."""
    mu, sd = float(reg[tr].mean()), float(reg[tr].std())
    z = (reg - mu) / (sd if sd != 0 else 1.0)
    ratio = y[tr] / trend[tr]
    denom = float(np.sum(z[tr] ** 2))
    k = max(float(np.sum((ratio - 1.0) * z[tr]) / denom), 0.0) if denom != 0 else 0.0
    return trend * (1.0 + k * z), k


@dataclass(frozen=True)
class RealCobenefitResult:
    n_years: int
    trend_mase: float
    coupled_mase: float
    placebo_mase: float
    pm25_death_corr: float
    hazard_coef: float

    @property
    def synergy_delta(self) -> float:
        return self.trend_mase - self.coupled_mase

    @property
    def beats_placebo(self) -> bool:
        return self.coupled_mase < self.placebo_mase

    @property
    def sign_as_assumed(self) -> bool:
        """The coupling assumes PM2.5 RAISES mortality; the raw correlation must be positive to be even
        the right sign. (A positive raw sign that a train-block fit erases, k→0, is confounding.)"""
        return self.pm25_death_corr > 0.0

    def verdict(self) -> str:
        return "keep" if (self.synergy_delta > 0.05 and self.beats_placebo and self.sign_as_assumed) else "cut"


def run_real_cobenefit_tournament(test_frac: float = 0.3) -> RealCobenefitResult:
    ds = load_real_cobenefit()
    y = ds.column("death_rate")
    pm25 = ds.column("pm25")
    n = len(y)
    t = np.arange(n, dtype=float)
    split = time_blocked_split(n, test_frac)
    tr, te = split.train, split.test

    a, b = _fit_log_trend(y[tr], t[tr])
    trend = np.exp(a * t + b)

    coupled, k = _hazard_fit_predict(y, trend, pm25, tr)
    placebo, _ = _hazard_fit_predict(y, trend, t**1.5, tr)

    return RealCobenefitResult(
        n_years=n,
        trend_mase=mase(y[te], trend[te]),
        coupled_mase=mase(y[te], coupled[te]),
        placebo_mase=mase(y[te], placebo[te]),
        pm25_death_corr=float(np.corrcoef(pm25, y)[0, 1]),
        hazard_coef=k,
    )
