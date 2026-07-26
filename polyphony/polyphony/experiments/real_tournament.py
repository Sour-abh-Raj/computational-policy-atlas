"""First tournament on REAL data (issue #9): does a climate coupling help predict world GDP?

The synthetic rounds validated the *method*; this asks the honest real-world question. Target: real
world GDP (World Bank, indexed to 100). Two predictors, both fit on the **train block only**:

- **economy-only** — a log-linear growth trend (GDP is ~exponential); the sum-of-parts baseline.
- **coupled** — the same trend times a climate-damage factor ``(1 − k·cum_co2_norm²)`` driven by
  **observed** cumulative CO₂ (OWID), with ``k ≥ 0`` fit on train. This is the reduced-form
  climate→economy channel applied to real emissions.

Synergy Δ = economy-only MASE − coupled MASE. But a positive Δ is **not enough**: cumulative CO₂ is a
monotone-increasing regressor, so it can improve the fit merely by **proxying the post-2008 growth
slowdown** — not by carrying climate information. So the decisive test is a **placebo control**: refit
the same damage form with a generic time-trend regressor (t^1.5) in place of CO₂. The coupling is
**kept only if it beats BOTH the economy-only baseline AND the placebo** — otherwise the "synergy" is
spurious curvature-fitting and is **cut**. Everything is honest about being a **reduced-form** channel,
not a damage estimate.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from ..data.loaders import load_real_gdp_co2
from ..data.splits import time_blocked_split
from ..eval.metrics import mase


def _fit_log_trend(y: np.ndarray, t: np.ndarray) -> tuple[float, float]:
    """OLS of log(y) on t; returns (a, b) for y ≈ exp(a·t + b)."""
    a, b = np.polyfit(t, np.log(y), 1)
    return float(a), float(b)


def _fit_damage_coef(resid_ratio: np.ndarray, cum_norm: np.ndarray) -> float:
    """Least-squares k ≥ 0 for resid_ratio ≈ 1 − k·cum_norm² (train block); clamped non-negative."""
    x = cum_norm**2
    denom = float(np.sum(x * x))
    if denom == 0.0:
        return 0.0
    k = float(np.sum((1.0 - resid_ratio) * x) / denom)
    return max(k, 0.0)


@dataclass(frozen=True)
class RealResult:
    n_years: int
    econ_mase: float
    coupled_mase: float
    placebo_mase: float
    naive_beaten_by_coupled: bool
    damage_coef: float

    @property
    def synergy_delta(self) -> float:
        return self.econ_mase - self.coupled_mase

    @property
    def beats_placebo(self) -> bool:
        """A real climate signal must beat a generic time-trend regressor, not merely the trend baseline."""
        return self.coupled_mase < self.placebo_mase

    def verdict(self) -> str:
        # Keep only if the CO₂ coupling beats BOTH the economy-only baseline AND the placebo control.
        return "keep" if (self.synergy_delta > 0.05 and self.beats_placebo) else "cut"


def _damage_fit_predict(y: np.ndarray, trend: np.ndarray, reg: np.ndarray, tr: slice) -> tuple[np.ndarray, float]:
    """Fit ``y ≈ trend·(1 − k·reg²)`` on train (k≥0) and return (full prediction, k)."""
    ratio = y[tr] / trend[tr]
    k = _fit_damage_coef(ratio, reg[tr])
    return trend * (1.0 - k * reg**2), k


def run_real_tournament(test_frac: float = 0.3) -> RealResult:
    ds = load_real_gdp_co2()
    y = ds.column("gdp")
    cum = ds.column("cum_co2")
    n = len(y)
    t = np.arange(n, dtype=float)
    split = time_blocked_split(n, test_frac)
    tr, te = split.train, split.test

    # economy-only: log-linear trend fit on train, extrapolated.
    a, b = _fit_log_trend(y[tr], t[tr])
    trend = np.exp(a * t + b)

    # coupled: trend × climate-damage from observed cumulative CO₂ (normalized by last TRAIN value).
    cum_norm = cum / cum[tr][-1]
    coupled, k = _damage_fit_predict(y, trend, cum_norm, tr)

    # placebo control: the SAME damage form driven by a generic monotone time trend, not CO₂.
    t_norm = (t / t[tr][-1]) ** 1.5
    placebo, _ = _damage_fit_predict(y, trend, t_norm, tr)

    return RealResult(
        n_years=n,
        econ_mase=mase(y[te], trend[te]),
        coupled_mase=mase(y[te], coupled[te]),
        placebo_mase=mase(y[te], placebo[te]),
        naive_beaten_by_coupled=mase(y[te], coupled[te]) < 1.0,
        damage_coef=k,
    )
