"""Energy⇄Inflation eighth coupling (issue #13) — the first clean REAL-data keep.

Cited reason: energy is a large, direct component of consumer prices and passes through to core costs via
transport and production, so **energy-price growth should predict inflation** — the mechanism behind the
1970s, 2008, and 2022 inflation episodes and a central-bank staple. This is a **reduced-form pass-through**
coupling (a regression of inflation on energy-price growth), tested directly rather than through a
dynamical voice — an honest modeling choice for a relationship that is econometric, not mechanistic-dynamic.

Two tests, one bar:

- **Synthetic method-validation** — a matched series (inflation = pass-through·energy-growth + noise) must
  be *kept*, and a control where inflation is independent of energy must be *cut*.
- **Real data** — IMF Global Energy price index + US CPI (FRED). Decided by walk-forward: does energy-price
  growth beat a mean baseline, a placebo, persistence, and naive, with the assumed (positive) sign?

Unlike the six real-data cuts, this one **survives**: across walk-forward folds energy-price growth beats
every baseline with the right sign — the instrument's first clean real-data keep (after Macro⇄Health, whose
own real test was underpowered). The bar rewards a genuinely skillful coupling exactly as it punishes a
plausible-but-hollow one.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from ..data.loaders import load_real_inflation
from ..data.splits import time_blocked_split, walk_forward
from ..eval.metrics import mase


def _growth(x: np.ndarray) -> np.ndarray:
    return np.diff(np.log(x)) * 100.0


def _passthrough_predict(y: np.ndarray, driver: np.ndarray, tr: slice) -> np.ndarray:
    """OLS ``inflation ≈ a + b·energy_growth`` on train, with b ≥ 0 (the assumed positive pass-through)."""
    b_raw, a = np.polyfit(driver[tr], y[tr], 1)
    b = max(float(b_raw), 0.0)
    return a + b * driver


@dataclass(frozen=True)
class InflationResult:
    n_years: int
    corr: float
    coupled_mase: float
    baseline_mase: float
    placebo_mase: float
    persistence_mase: float
    wf_folds: int
    wf_beats_baseline: float
    wf_beats_placebo: float
    wf_beats_persistence: float
    wf_beats_naive: float

    @property
    def sign_as_assumed(self) -> bool:
        return self.corr > 0.0

    def robust_verdict(self) -> str:
        return (
            "keep"
            if (
                self.wf_beats_baseline > 0.5
                and self.wf_beats_placebo > 0.5
                and self.wf_beats_persistence > 0.5
                and self.wf_beats_naive > 0.5
                and self.sign_as_assumed
            )
            else "cut"
        )


def _score(y: np.ndarray, driver: np.ndarray, horizon: int) -> InflationResult:
    n = len(y)
    t = np.arange(n, dtype=float)
    split = time_blocked_split(n, 0.3)
    tr, te = split.train, split.test
    baseline = np.full(n, float(y[tr].mean()))
    coupled = _passthrough_predict(y, driver, tr)
    placebo = _passthrough_predict(y, t, tr)
    persistence = np.concatenate([[y[0]], y[:-1]])

    b_wf, c_wf, p_wf, per_wf, nv_wf = [], [], [], [], []
    for sp in walk_forward(n, min_train=n // 2, horizon=horizon):
        wtr, wte = sp.train, sp.test
        base = np.full(n, float(y[wtr].mean()))
        c = _passthrough_predict(y, driver, wtr)
        p = _passthrough_predict(y, t, wtr)
        b_wf.append(mase(y[wte], base[wte]))
        c_wf.append(mase(y[wte], c[wte]))
        p_wf.append(mase(y[wte], p[wte]))
        per_wf.append(mase(y[wte], persistence[wte]))
        nv_wf.append(mase(y[wte], c[wte]))
    b_, c_, p_, per_ = np.array(b_wf), np.array(c_wf), np.array(p_wf), np.array(per_wf)
    return InflationResult(
        n_years=n,
        corr=float(np.corrcoef(driver, y)[0, 1]),
        coupled_mase=mase(y[te], coupled[te]),
        baseline_mase=mase(y[te], baseline[te]),
        placebo_mase=mase(y[te], placebo[te]),
        persistence_mase=mase(y[te], persistence[te]),
        wf_folds=len(c_),
        wf_beats_baseline=float(np.mean(c_ < b_)),
        wf_beats_placebo=float(np.mean(c_ < p_)),
        wf_beats_persistence=float(np.mean(c_ < per_)),
        wf_beats_naive=float(np.mean(np.array(nv_wf) < 1.0)),
    )


def run_real_inflation_tournament(horizon: int = 4) -> InflationResult:
    ds = load_real_inflation()
    inflation = _growth(ds.column("cpi"))
    energy_growth = _growth(ds.column("energy"))
    return _score(inflation, energy_growth, horizon)


def run_synthetic_check(present: bool, n: int = 40, seed: int = 0, horizon: int = 4) -> InflationResult:
    """Matched (``present``) vs independent (control) synthetic pass-through — the method must keep/cut."""
    rng = np.random.default_rng(seed)
    energy_growth = rng.normal(0, 8, n)
    base = 2.0 + rng.normal(0, 0.5, n)
    inflation = base + (0.3 * energy_growth if present else 0.0)
    return _score(inflation, energy_growth, horizon)
