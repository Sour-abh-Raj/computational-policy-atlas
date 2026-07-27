"""Walk-forward cross-validation of the real-data couplings (Iter 23 — robustness of the verdicts).

The single-split real tournaments (Rounds 10, 13, 15, 17) each decide keep/cut on **one** time-blocked
split. That is a legitimate but *fragile* test: the nexus placebo comparison, for instance, flipped
between two reasonable split choices. This module re-runs each real coupling over an **expanding-window
walk-forward** (Hyndman: the honest way to backtest a time series) and reports, across folds, how often
the coupling beats its **baseline**, a **placebo**, and **naive** — turning a single verdict into a
distribution. A cut that holds across most folds is a *robust* cut, not a split artifact.

To compare couplings on one footing, all use a unified **sign-aware reduced form**: fit a log-trend on
each fold's train block, then a one-parameter term ``trend·(1 + direction·k·z)`` where ``z`` is the driver
standardized on train and ``k ≥ 0`` is clamped to the coupling's **assumed direction** (``+1`` more
driver ⇒ more target; ``−1`` less). If the train-block partial relationship has the wrong sign, ``k → 0``
and the coupling collapses to the trend — exactly the honest behaviour we want.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from ..data.loaders import (
    load_real_cobenefit,
    load_real_food,
    load_real_gdp_co2,
    load_real_nexus,
)
from ..data.splits import walk_forward
from ..eval.metrics import mase
from .real_tournament import _fit_log_trend


@dataclass(frozen=True)
class WalkForwardReport:
    coupling: str
    n_folds: int
    baseline_mase_median: float
    coupled_mase_median: float
    placebo_mase_median: float
    frac_beats_baseline: float
    frac_beats_placebo: float
    frac_beats_naive: float

    def robust_verdict(self) -> str:
        """Keep only if the coupling beats baseline AND placebo AND naive in a **majority** of folds."""
        return (
            "keep"
            if (self.frac_beats_baseline > 0.5 and self.frac_beats_placebo > 0.5 and self.frac_beats_naive > 0.5)
            else "cut"
        )


def _sign_aware_predict(y: np.ndarray, trend: np.ndarray, reg: np.ndarray, tr: slice, direction: int) -> np.ndarray:
    """``trend·(1 + direction·k·z)`` with ``z`` = reg standardized on train and ``k ≥ 0`` clamped to the
    assumed ``direction`` (+1 more driver ⇒ more target; −1 less). Wrong-signed fits collapse to trend."""
    mu, sd = float(reg[tr].mean()), float(reg[tr].std())
    z = (reg - mu) / (sd if sd != 0 else 1.0)
    ratio = y[tr] / trend[tr]
    denom = float(np.sum(z[tr] ** 2))
    coef = float(np.sum((ratio - 1.0) * z[tr]) / denom) if denom != 0 else 0.0
    k = max(direction * coef, 0.0)
    return trend * (1.0 + direction * k * z)


def evaluate_walk_forward(
    coupling: str,
    y: np.ndarray,
    driver: np.ndarray,
    direction: int,
    min_train: int | None = None,
    horizon: int = 4,
) -> WalkForwardReport:
    n = len(y)
    t = np.arange(n, dtype=float)
    mt = min_train if min_train is not None else max(10, n // 2)
    folds = walk_forward(n, min_train=mt, horizon=horizon)
    base, coup, plac = [], [], []
    for sp in folds:
        tr, te = sp.train, sp.test
        a, b = _fit_log_trend(y[tr], t[tr])
        trend = np.exp(a * t + b)
        coupled = _sign_aware_predict(y, trend, driver, tr, direction)
        placebo = _sign_aware_predict(y, trend, t**1.5, tr, +1)
        base.append(mase(y[te], trend[te]))
        coup.append(mase(y[te], coupled[te]))
        plac.append(mase(y[te], placebo[te]))
    b_, c_, p_ = np.array(base), np.array(coup), np.array(plac)
    return WalkForwardReport(
        coupling=coupling,
        n_folds=len(folds),
        baseline_mase_median=float(np.median(b_)),
        coupled_mase_median=float(np.median(c_)),
        placebo_mase_median=float(np.median(p_)),
        frac_beats_baseline=float(np.mean(c_ < b_)),
        frac_beats_placebo=float(np.mean(c_ < p_)),
        frac_beats_naive=float(np.mean(c_ < 1.0)),
    )


def run_all_walk_forward() -> dict[str, WalkForwardReport]:
    """Walk-forward every real coupling with a champion mechanism, on its committed real dataset.

    ``direction`` encodes each coupling's assumed sign: climate→GDP and warming→yield are **−1** (the
    driver lowers the target); PM2.5→mortality and energy→food are **+1** (raises it).
    """
    out: dict[str, WalkForwardReport] = {}

    gdp = load_real_gdp_co2()
    out["climate->GDP"] = evaluate_walk_forward(
        "climate->GDP", gdp.column("gdp"), gdp.column("cum_co2"), direction=-1
    )

    food = load_real_food()
    out["warming->yield"] = evaluate_walk_forward(
        "warming->yield", food.column("cereal_yield"), food.column("temp"), direction=-1
    )

    cob = load_real_cobenefit()
    out["PM2.5->mortality"] = evaluate_walk_forward(
        "PM2.5->mortality", cob.column("death_rate"), cob.column("pm25"), direction=+1
    )

    nex = load_real_nexus()
    out["energy->food"] = evaluate_walk_forward(
        "energy->food", nex.column("food_price"), nex.column("energy_price"), direction=+1
    )

    return out
