"""Panel validation — attacking the "confounded-away" failure mode with cross-country data (Iter 33).

The modal way a real-data coupling was cut is **confounded-away**: a strong correlation between two
trending series that vanishes once a trend is removed (six of seven cuts touch this; the placebo control
catches it on a single time series). A *panel* of many countries gives a sharper instrument: with **two-way
fixed effects** — removing every country's level *and* every year's common shock (the shared global trend)
— what remains is the **within-country** relationship, the mechanism itself, stripped of the confounding
trend.

We apply it to carbon leakage (the Iter-30 cut). Across 100+ countries × ~30 years, does trade openness
explain the consumption/production CO₂ ratio *within* a country over time, once common year effects are
removed? The pooled correlation is positive (the naive leakage story); the two-way-FE within correlation is
what tests the mechanism. This both **confirms the cut with far more power** than one UK series and
demonstrates a reusable validation method (panel FE) for separating mechanism from shared trend.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from ..data.loaders import load_real_leakage_panel


def _group_demean(v: np.ndarray, group: np.ndarray) -> np.ndarray:
    out = v.astype(float).copy()
    for g in np.unique(group):
        mask = group == g
        out[mask] -= out[mask].mean()
    return out


def two_way_within(value: np.ndarray, driver: np.ndarray, unit: np.ndarray, time: np.ndarray, iters: int = 60) -> float:
    """Correlation of ``value`` and ``driver`` after two-way (unit + time) fixed-effects demeaning."""
    v, d = value.astype(float).copy(), driver.astype(float).copy()
    for _ in range(iters):
        v = _group_demean(_group_demean(v, unit), time)
        d = _group_demean(_group_demean(d, unit), time)
    if np.std(v) == 0 or np.std(d) == 0:
        return 0.0
    return float(np.corrcoef(d, v)[0, 1])


@dataclass(frozen=True)
class PanelLeakageResult:
    n_obs: int
    n_countries: int
    n_years: int
    pooled_corr: float
    within_corr: float

    @property
    def attenuation(self) -> float:
        """Fraction of the pooled correlation that disappears under two-way fixed effects (1 ⇒ fully a trend)."""
        if self.pooled_corr == 0:
            return 0.0
        return 1.0 - abs(self.within_corr) / abs(self.pooled_corr)

    def verdict(self) -> str:
        """The cut is *confirmed* (confounded-away) if a positive pooled correlation nearly vanishes within."""
        confounded = self.pooled_corr > 0.2 and abs(self.within_corr) < 0.1
        return "cut-confirmed (confounded-away)" if confounded else "within-signal survives"


def run_leakage_panel() -> PanelLeakageResult:
    iso, year, ratio, openness = load_real_leakage_panel()
    pooled = float(np.corrcoef(openness, ratio)[0, 1])
    within = two_way_within(ratio, openness, iso, year)
    return PanelLeakageResult(
        n_obs=len(ratio),
        n_countries=int(len(np.unique(iso))),
        n_years=int(len(np.unique(year))),
        pooled_corr=pooled,
        within_corr=within,
    )
