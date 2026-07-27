"""Real Trade⇄Emissions tournament (closes the Iter-29 gap, issue #12-real).

The trade voice models carbon leakage: consumption-based emissions exceed production-based as trade opens.
Tested on the **United Kingdom** — the textbook case (production CO₂ ~halved since 1990 while consumption
CO₂ fell far less). Target: real **consumption** CO₂. Three predictors, all fit on train:

- **leakage-blind** — an affine map of **production** CO₂ (consumption ≈ a·production + b); this already
  captures the *average* leakage level, so it is a strong, honest baseline.
- **leakage-coupled** — production scaled by an **openness**-driven leakage term ``production·(1 + k·z)``
  (k ≥ 0), where openness (World Bank trade % of GDP) is an **independent** driver — *not* the observed
  gap, which would be circular.
- **placebo** — the same form driven by a generic time trend.

The honest verdict is a **CUT of the "confounded-away" kind**. corr(openness, consumption/production ratio)
is strongly **positive (≈ +0.8)** — the UK gap really did grow as it opened — but out of sample the
openness-leakage term does **not** beat the production-blind baseline or the placebo (the openness↔gap
correlation is a *shared trend*: both rose over 1990–2023). The average leakage is real and trivially
captured by production; its openness-driven *dynamics* are not predictable beyond a trend.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from ..data.loaders import load_real_trade
from ..data.splits import time_blocked_split, walk_forward
from ..eval.metrics import mase


def _blind_predict(production: np.ndarray, consumption: np.ndarray, tr: slice) -> np.ndarray:
    """Affine map consumption ≈ a·production + b fit on train — captures the average leakage level."""
    a, b = np.polyfit(production[tr], consumption[tr], 1)
    return a * production + b


def _leakage_predict(production: np.ndarray, consumption: np.ndarray, driver: np.ndarray, tr: slice) -> np.ndarray:
    """``production·(1 + k·z)`` with z = driver standardized on train and k ≥ 0 (openness raises the gap)."""
    mu, sd = float(driver[tr].mean()), float(driver[tr].std())
    z = (driver - mu) / (sd if sd != 0 else 1.0)
    ratio = consumption[tr] / production[tr]
    denom = float(np.sum(z[tr] ** 2))
    k = max(float(np.sum((ratio - 1.0) * z[tr]) / denom), 0.0) if denom != 0 else 0.0
    return production * (1.0 + k * z)


@dataclass(frozen=True)
class RealTradeResult:
    n_years: int
    openness_ratio_corr: float
    coupled_mase: float
    blind_mase: float
    placebo_mase: float
    wf_folds: int
    wf_beats_blind: float
    wf_beats_placebo: float
    wf_beats_naive: float

    @property
    def sign_as_assumed(self) -> bool:
        return self.openness_ratio_corr > 0.0

    def robust_verdict(self) -> str:
        return (
            "keep"
            if (
                self.wf_beats_blind > 0.5
                and self.wf_beats_placebo > 0.5
                and self.wf_beats_naive > 0.5
                and self.sign_as_assumed
            )
            else "cut"
        )


def run_real_trade_tournament(test_frac: float = 0.3, horizon: int = 4) -> RealTradeResult:
    ds = load_real_trade()
    prod = ds.column("production_co2")
    cons = ds.column("consumption_co2")
    openness = ds.column("openness")
    n = len(cons)
    t = np.arange(n, dtype=float)

    split = time_blocked_split(n, test_frac)
    tr, te = split.train, split.test
    blind = _blind_predict(prod, cons, tr)
    coupled = _leakage_predict(prod, cons, openness, tr)
    placebo = _leakage_predict(prod, cons, t**1.5, tr)

    b_wf, c_wf, p_wf = [], [], []
    for sp in walk_forward(n, min_train=n // 2, horizon=horizon):
        wtr, wte = sp.train, sp.test
        b_wf.append(mase(cons[wte], _blind_predict(prod, cons, wtr)[wte]))
        c_wf.append(mase(cons[wte], _leakage_predict(prod, cons, openness, wtr)[wte]))
        p_wf.append(mase(cons[wte], _leakage_predict(prod, cons, t**1.5, wtr)[wte]))
    b_, c_, p_ = np.array(b_wf), np.array(c_wf), np.array(p_wf)

    return RealTradeResult(
        n_years=n,
        openness_ratio_corr=float(np.corrcoef(openness, cons / prod)[0, 1]),
        coupled_mase=mase(cons[te], coupled[te]),
        blind_mase=mase(cons[te], blind[te]),
        placebo_mase=mase(cons[te], placebo[te]),
        wf_folds=len(c_),
        wf_beats_blind=float(np.mean(c_ < b_)),
        wf_beats_placebo=float(np.mean(c_ < p_)),
        wf_beats_naive=float(np.mean(c_ < 1.0)),
    )
