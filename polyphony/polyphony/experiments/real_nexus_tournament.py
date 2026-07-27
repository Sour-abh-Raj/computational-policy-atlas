"""Real Water⇄Energy⇄Food nexus tournament (closes the Iter-21 gap, issue #10-real).

The nexus-food voice models scarcity → higher food price, carrying an **energy** pass-through (the pumping
surcharge) alongside the water leg. A clean global water-scarcity driver is not readily available as an
annual series, so we test the nexus's **most data-rich, best-documented leg — energy → food price**
(natural gas → nitrogen fertilizer; diesel → machinery/transport; electricity → irrigation pumping) on
**real** IMF Global Food and Energy price indices (FRED), 1992–2025.

Honesty checks, the same bar every real-data coupling faced:

1. **Placebo control** — an energy pass-through ``(1 + k·energy)`` (k ≥ 0) fit on train, vs the SAME form
   driven by a generic time trend. A real cross-sector link must beat the placebo, not just the trend.
2. **Sign** — the pass-through is assumed positive (energy up ⇒ food up); we report the correlation.
3. **Skill vs naive** — food prices are a volatile near-random-walk, so we also report whether the
   coupling beats a naive one-step baseline (MASE < 1). A "real signal, no forecast skill" outcome is a
   distinct and publishable failure mode.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from ..data.loaders import load_real_nexus
from ..data.splits import time_blocked_split
from ..eval.metrics import mase
from .real_tournament import _fit_log_trend
from .real_urbanhealth_tournament import _hazard_fit_predict


@dataclass(frozen=True)
class RealNexusResult:
    n_years: int
    trend_mase: float
    coupled_mase: float
    placebo_mase: float
    energy_food_corr: float
    passthrough_coef: float

    @property
    def synergy_delta(self) -> float:
        return self.trend_mase - self.coupled_mase

    @property
    def beats_placebo(self) -> bool:
        return self.coupled_mase < self.placebo_mase

    @property
    def coupled_beats_naive(self) -> bool:
        return self.coupled_mase < 1.0

    @property
    def sign_as_assumed(self) -> bool:
        """The pass-through is assumed positive: energy up ⇒ food up."""
        return self.energy_food_corr > 0.0

    def verdict(self) -> str:
        # Keep only if energy improves out-of-sample food prediction over the trend AND the placebo AND
        # earns actual skill (beats naive), with the assumed sign.
        return (
            "keep"
            if (
                self.synergy_delta > 0.05
                and self.beats_placebo
                and self.sign_as_assumed
                and self.coupled_beats_naive
            )
            else "cut"
        )


def run_real_nexus_tournament(test_frac: float = 0.3) -> RealNexusResult:
    ds = load_real_nexus()
    y = ds.column("food_price")
    energy = ds.column("energy_price")
    n = len(y)
    t = np.arange(n, dtype=float)
    split = time_blocked_split(n, test_frac)
    tr, te = split.train, split.test

    a, b = _fit_log_trend(y[tr], t[tr])
    trend = np.exp(a * t + b)

    coupled, k = _hazard_fit_predict(y, trend, energy, tr)  # (1 + k·energy), k≥0 — the assumed pass-through
    placebo, _ = _hazard_fit_predict(y, trend, t**1.5, tr)

    return RealNexusResult(
        n_years=n,
        trend_mase=mase(y[te], trend[te]),
        coupled_mase=mase(y[te], coupled[te]),
        placebo_mase=mase(y[te], placebo[te]),
        energy_food_corr=float(np.corrcoef(energy, y)[0, 1]),
        passthrough_coef=k,
    )
