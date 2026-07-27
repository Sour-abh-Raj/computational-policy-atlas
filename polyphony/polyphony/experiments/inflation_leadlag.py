"""Energy⇄Inflation lead-lag study (Iter 36) — does it *forecast*, or only *nowcast*?

The Iter-35 keep tested the **contemporaneous** pass-through (energy-price growth vs same-year inflation).
That is a legitimate nowcast (energy is observed before CPI is finalized), but the decision-relevant
question is whether energy prices carry genuine **leading** information — do they forecast inflation *ahead*?
This study lags energy-price growth by h = 0, 1, 2, 3 years and re-runs the walk-forward test at each
horizon.

The honest finding has real economic content: skill is strong at **h = 0** and **survives at h = 1** (a
genuine one-year-ahead forecast, right sign), then **decays and the sign flips by h = 2** — the classic
**base effect** (a price spike raises inflation now and *lowers* it a couple of years later when the level
drops out). So the coupling is a real short-horizon forecaster, not a long-horizon one — consistent with
central banks' doctrine of "looking through" transitory energy shocks. Reporting *how far ahead* the skill
reaches, and where it reverses, is more honest than a single "it predicts inflation".
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from ..data.loaders import load_real_inflation
from ..data.splits import walk_forward
from ..eval.metrics import mase
from .inflation_tournament import _growth, _passthrough_predict


@dataclass(frozen=True)
class LagResult:
    lag: int
    corr: float
    wf_beats_baseline: float
    wf_beats_naive: float

    @property
    def sign_as_assumed(self) -> bool:
        return self.corr > 0.0

    def verdict(self) -> str:
        return "keep" if (self.wf_beats_baseline > 0.5 and self.wf_beats_naive > 0.5 and self.sign_as_assumed) else "cut"


def _score_lag(inflation: np.ndarray, energy_growth: np.ndarray, lag: int, horizon: int = 4) -> LagResult:
    y = inflation[lag:] if lag > 0 else inflation
    drv = energy_growth[:-lag] if lag > 0 else energy_growth
    n = len(y)
    base_wf, coup_wf = [], []
    for sp in walk_forward(n, min_train=n // 2, horizon=horizon):
        tr, te = sp.train, sp.test
        base = np.full(n, float(y[tr].mean()))
        coup = _passthrough_predict(y, drv, tr)
        base_wf.append(mase(y[te], base[te]))
        coup_wf.append(mase(y[te], coup[te]))
    b_, c_ = np.array(base_wf), np.array(coup_wf)
    return LagResult(
        lag=lag,
        corr=float(np.corrcoef(drv, y)[0, 1]),
        wf_beats_baseline=float(np.mean(c_ < b_)),
        wf_beats_naive=float(np.mean(c_ < 1.0)),
    )


@dataclass(frozen=True)
class LeadLagStudy:
    lags: tuple[LagResult, ...]

    @property
    def forecast_horizon(self) -> int:
        """The largest lead (in years) at which the coupling still keeps (0 ⇒ nowcast only)."""
        kept = [r.lag for r in self.lags if r.verdict() == "keep"]
        return max(kept) if kept else -1

    @property
    def sign_flips(self) -> bool:
        """True if the correlation turns negative at some longer lag (a base-effect reversal)."""
        return any(r.corr < 0 for r in self.lags)


def run_lead_lag_study(max_lag: int = 3) -> LeadLagStudy:
    ds = load_real_inflation()
    inflation = _growth(ds.column("cpi"))
    energy_growth = _growth(ds.column("energy"))
    return LeadLagStudy(tuple(_score_lag(inflation, energy_growth, h) for h in range(max_lag + 1)))
