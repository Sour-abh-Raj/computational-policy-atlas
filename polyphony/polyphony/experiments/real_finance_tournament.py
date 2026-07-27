"""Real Macro⇄Finance tournament (closes the Iter-26 gap, issue #11-real) — the closest real-data call yet.

The finance voice models credit stress → weaker output. Tested on **real** FRED data: the Baa−10Y credit
spread vs annual real-GDP **growth** (the natural target — financial conditions predict *activity*, not
the smooth GDP level; Gilchrist-Zakrajšek 2012). Because financial conditions are observed in real time
while GDP is released with a lag, using the current spread to nowcast current growth is a legitimate,
useful decision-support task — and it matches the voice's contemporaneous drag.

The honest verdict is a **narrow CUT — but the strongest real signal of any coupling**, and it names a
*sixth, distinct* failure mode. Across expanding-window walk-forward folds the spread:

- has the **right sign** contemporaneously (corr ≈ −0.6; higher spread ⇒ lower growth),
- **beats a placebo** in most folds (genuine, non-spurious information), and **beats naive** in a majority,
- but **does not robustly beat a mean-growth climatology** — it helps in/around **crises** (it caught the
  2008 and COVID growth collapses) yet *hurts* in calm years, and overshoots the **2022** spread-widening
  that did *not* bring a recession.

So the reduced-form annual coupling has **regime-dependent skill**: real and valuable near crises, noise
in calm times, and therefore not a keep against an unconditional baseline. Both the single 30% split and
the walk-forward agree on cut — reported together so the (modest) signal and the honest verdict are both
visible. That a coupling *this* well-motivated (the Gilchrist-Zakrajšek channel is real) is still cut on
the strict bar is the point: the bar does not bend for a good story.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from ..data.loaders import load_real_finance
from ..data.splits import time_blocked_split, walk_forward
from ..eval.metrics import mase


def _growth_and_spread(gdp: np.ndarray, spread: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """Annual real-GDP growth (%) and the contemporaneous spread aligned to it."""
    growth = np.diff(np.log(gdp)) * 100.0
    return growth, spread[1:]


def _nowcast_predict(y: np.ndarray, spread: np.ndarray, tr: slice) -> np.ndarray:
    """OLS growth ≈ a + b·spread fit on train, with b ≤ 0 enforced (the assumed sign: stress lowers growth)."""
    b_raw, a = np.polyfit(spread[tr], y[tr], 1)
    b = min(float(b_raw), 0.0)
    return a + b * spread


def _trend_predict(y: np.ndarray, t: np.ndarray, tr: slice) -> np.ndarray:
    b, a = np.polyfit(t[tr], y[tr], 1)
    return a + b * t


@dataclass(frozen=True)
class RealFinanceResult:
    n_years: int
    contemp_corr: float
    # single time-blocked split (deliberately shown to be misleading here)
    coupled_mase: float
    baseline_mase: float
    placebo_mase: float
    # expanding-window walk-forward (the robust verdict)
    wf_folds: int
    wf_beats_baseline: float
    wf_beats_placebo: float
    wf_beats_naive: float

    @property
    def sign_as_assumed(self) -> bool:
        return self.contemp_corr < 0.0

    def single_split_verdict(self) -> str:
        beats = self.coupled_mase < self.baseline_mase and self.coupled_mase < self.placebo_mase
        return "keep" if (beats and self.coupled_mase < 1.0 and self.sign_as_assumed) else "cut"

    def robust_verdict(self) -> str:
        return (
            "keep"
            if (
                self.wf_beats_baseline > 0.5
                and self.wf_beats_placebo > 0.5
                and self.wf_beats_naive > 0.5
                and self.sign_as_assumed
            )
            else "cut"
        )


def run_real_finance_tournament(test_frac: float = 0.3, horizon: int = 4) -> RealFinanceResult:
    ds = load_real_finance()
    growth, spread = _growth_and_spread(ds.column("gdp"), ds.column("spread"))
    n = len(growth)
    t = np.arange(n, dtype=float)

    split = time_blocked_split(n, test_frac)
    tr, te = split.train, split.test
    baseline = np.full(n, float(growth[tr].mean()))
    coupled = _nowcast_predict(growth, spread, tr)
    placebo = _trend_predict(growth, t, tr)

    base_wf, coup_wf, plac_wf = [], [], []
    for sp in walk_forward(n, min_train=n // 2, horizon=horizon):
        wtr, wte = sp.train, sp.test
        b = np.full(n, float(growth[wtr].mean()))
        c = _nowcast_predict(growth, spread, wtr)
        p = _trend_predict(growth, t, wtr)
        base_wf.append(mase(growth[wte], b[wte]))
        coup_wf.append(mase(growth[wte], c[wte]))
        plac_wf.append(mase(growth[wte], p[wte]))
    b_, c_, p_ = np.array(base_wf), np.array(coup_wf), np.array(plac_wf)

    return RealFinanceResult(
        n_years=n,
        contemp_corr=float(np.corrcoef(spread, growth)[0, 1]),
        coupled_mase=mase(growth[te], coupled[te]),
        baseline_mase=mase(growth[te], baseline[te]),
        placebo_mase=mase(growth[te], placebo[te]),
        wf_folds=len(c_),
        wf_beats_baseline=float(np.mean(c_ < b_)),
        wf_beats_placebo=float(np.mean(c_ < p_)),
        wf_beats_naive=float(np.mean(c_ < 1.0)),
    )
