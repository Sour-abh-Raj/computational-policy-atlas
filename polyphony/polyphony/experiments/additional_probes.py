"""Additional probes (Iter 50) — even famous macro relationships don't beat climatology on annual growth.

After ten couplings, the project's deepest empirical finding is worth stress-testing with two of the most
celebrated macro relationships there are:

- **Okun's law** — Δunemployment ↔ GDP growth, one of the strongest *contemporaneous* correlations in
  macro (≈ −0.8). But unemployment is **coincident** (two measures of one business cycle), so it does not
  *forecast* growth better than a mean-growth climatology.
- **The yield curve** — the 10Y−3M term spread, the classic *leading* recession indicator. It genuinely
  leads by ~a year, yet at **annual** resolution the signal is washed out: it does not beat climatology for
  continuous growth either.

Both are **cut** on the standard test (beat the mean-growth baseline in a majority of walk-forward folds),
reinforcing the generalization the whole project has been circling: *reduced-form couplings on annual
aggregate growth almost never beat a climatology baseline.* The sole exception — **Energy⇄Inflation** — is
the exception that proves the rule: it works because energy is a **large, mechanical, contemporaneous
component of the CPI**, not because it forecasts an otherwise-unforecastable series.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from ..data.loaders import load_real_okun, load_real_yieldcurve
from ..data.splits import walk_forward
from ..eval.metrics import mase


def _growth(x: np.ndarray) -> np.ndarray:
    return np.diff(np.log(x)) * 100.0


def _beats_baseline_frac(y: np.ndarray, driver: np.ndarray, sign: int, horizon: int = 4) -> float:
    """Fraction of walk-forward folds in which an OLS ``y ≈ a + b·driver`` (b sign-constrained) beats the
    mean-``y`` climatology baseline."""
    n = len(y)
    coup, base = [], []
    for sp in walk_forward(n, min_train=n // 2, horizon=horizon):
        tr, te = sp.train, sp.test
        b_raw, a = np.polyfit(driver[tr], y[tr], 1)
        b = min(b_raw, 0.0) if sign < 0 else max(b_raw, 0.0)
        c = a + b * driver
        coup.append(mase(y[te], c[te]))
        base.append(mase(y[te], np.full(n, float(y[tr].mean()))[te]))
    return float(np.mean(np.array(coup) < np.array(base)))


@dataclass(frozen=True)
class ProbeResult:
    name: str
    kind: str  # "coincident" | "leading"
    corr: float
    beats_baseline_frac: float

    @property
    def verdict(self) -> str:
        return "keep" if self.beats_baseline_frac > 0.5 else "cut"


def run_okun_probe() -> ProbeResult:
    ds = load_real_okun()
    growth = _growth(ds.column("gdp"))
    d_unrate = np.diff(ds.column("unrate"))  # contemporaneous with growth
    return ProbeResult(
        "Okun (Δunemployment→growth)",
        "coincident",
        float(np.corrcoef(d_unrate, growth)[0, 1]),
        _beats_baseline_frac(growth, d_unrate, sign=-1),
    )


def run_yieldcurve_probe() -> ProbeResult:
    ds = load_real_yieldcurve()
    spread = ds.column("spread")
    growth = _growth(ds.column("gdp"))
    lead = spread[:-1]  # spread in year t predicts growth in year t+1
    return ProbeResult(
        "Yield curve (term spread→next-year growth)",
        "leading",
        float(np.corrcoef(lead, growth)[0, 1]),
        _beats_baseline_frac(growth, lead, sign=+1),
    )


def only_mechanical_component_keeps() -> bool:
    """Both celebrated relationships are cut on annual growth — the generalization holds: neither a
    coincident (Okun) nor a leading (yield-curve) indicator beats climatology for annual growth."""
    return run_okun_probe().verdict == "cut" and run_yieldcurve_probe().verdict == "cut"
