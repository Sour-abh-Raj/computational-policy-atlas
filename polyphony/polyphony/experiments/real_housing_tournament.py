"""Real Interest-Rate⇄Housing tournament (issue #14) — a CUT via reverse causation + momentum.

Higher interest rates should slow house-price growth. But this coupling is a textbook **identification
trap**: rates and house-price growth **co-move contemporaneously** with the *wrong* (positive) sign, because
the central bank **hikes into booms** — the policy responds to the outcome (reverse causation). So the
honest test uses the **lagged** rate to forecast next-year house-price growth, with the assumed *negative*
sign.

Tested on real FRED data (30-yr mortgage rate + Case-Shiller HPI), decided by walk-forward. The verdict is a
**CUT** on two counts a bare correlation would hide:

1. **Reverse causation** — the contemporaneous correlation is **positive** (rate up ↔ growth up), the
   opposite of the mechanism; using it would badly mislead.
2. **Momentum beats it** — the correctly-signed *lagged* rate does not beat a **persistence** (momentum)
   baseline: house-price growth is highly autocorrelated, and last year's growth predicts this year's better
   than the rate does. Failing to beat the honest baseline is decisive (the Iter-37 meta-analysis rule).
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from ..data.loaders import load_real_housing
from ..data.splits import walk_forward
from ..eval.metrics import mase


def _growth(x: np.ndarray) -> np.ndarray:
    return np.diff(np.log(x)) * 100.0


def _lag_fit(y: np.ndarray, driver: np.ndarray, tr: slice) -> np.ndarray:
    """OLS ``growth ≈ a + b·rate_lagged`` on train with b ≤ 0 (the assumed sign: higher rates ⇒ lower growth)."""
    b_raw, a = np.polyfit(driver[tr], y[tr], 1)
    b = min(float(b_raw), 0.0)
    return a + b * driver


@dataclass(frozen=True)
class RealHousingResult:
    n_years: int
    contemp_corr: float  # d_rate_t vs growth_t — expected positive (reverse causation)
    lead_corr: float  # rate_{t-1} vs growth_t — assumed negative
    wf_beats_baseline: float
    wf_beats_persistence: float
    wf_beats_naive: float

    @property
    def reverse_causation(self) -> bool:
        """The contemporaneous sign contradicts the mechanism (policy reacts to the outcome)."""
        return self.contemp_corr > 0.0

    @property
    def lead_sign_as_assumed(self) -> bool:
        return self.lead_corr < 0.0

    def robust_verdict(self) -> str:
        # Keep only if the lagged rate beats the baseline, momentum (persistence), and naive with the
        # assumed sign. Housing momentum defeats it ⇒ cut.
        return (
            "keep"
            if (
                self.wf_beats_baseline > 0.5
                and self.wf_beats_persistence > 0.5
                and self.wf_beats_naive > 0.5
                and self.lead_sign_as_assumed
            )
            else "cut"
        )


def run_real_housing_tournament(horizon: int = 4) -> RealHousingResult:
    ds = load_real_housing()
    rate = ds.column("rate")
    growth = _growth(ds.column("hpi"))
    d_rate = np.diff(rate)  # aligned with growth (both start at the second year)

    contemp_corr = float(np.corrcoef(d_rate, growth)[0, 1])
    # Lead test: last year's rate LEVEL predicts this year's growth.
    y = growth[1:]
    rate_lag = rate[1:-1]  # rate in year t-1 aligned with growth in year t
    lead_corr = float(np.corrcoef(rate_lag, y)[0, 1])

    n = len(y)
    persistence = np.concatenate([[y[0]], y[:-1]])
    base_wf, coup_wf, per_wf, nv_wf = [], [], [], []
    for sp in walk_forward(n, min_train=n // 2, horizon=horizon):
        tr, te = sp.train, sp.test
        base = np.full(n, float(y[tr].mean()))
        coup = _lag_fit(y, rate_lag, tr)
        base_wf.append(mase(y[te], base[te]))
        coup_wf.append(mase(y[te], coup[te]))
        per_wf.append(mase(y[te], persistence[te]))
        nv_wf.append(mase(y[te], coup[te]))
    b_, c_, per_ = np.array(base_wf), np.array(coup_wf), np.array(per_wf)
    return RealHousingResult(
        n_years=n,
        contemp_corr=contemp_corr,
        lead_corr=lead_corr,
        wf_beats_baseline=float(np.mean(c_ < b_)),
        wf_beats_persistence=float(np.mean(c_ < per_)),
        wf_beats_naive=float(np.mean(np.array(nv_wf) < 1.0)),
    )
