"""Honest predictive uncertainty for the real couplings (Iter 25 — turn the overconfidence diagnosis into a fix).

Round 19 measured that the real couplings are **grossly overconfident**: bands built from *in-sample*
residuals almost never contain the out-of-sample truth (PIT at the tails). The diagnosed causes were (1)
the coupled point forecast **overshoots** out of sample (trend-extrapolation bias) and (2) in-sample
residuals **ignore how error grows with forecast horizon**. This module builds an *honest* predictive
distribution that addresses both, using only training information:

- **Bias correction** from a walk-forward backtest on the train block — collect genuine *out-of-sample*
  one-step residuals and shift the point by their mean.
- **Horizon-fanning bands** — size the spread from those OOS residuals and grow it as ``√h`` with the
  forecast lead ``h`` (random-walk-like variance accumulation), instead of a flat in-sample width.

The claim is **not** that this makes the coupling accurate (it does not — nothing beats naive here); it is
that honest uncertainty is *achievable* — a calibrated predictive distribution (PIT covering nominally)
even for a coupling with no point skill. Reporting *earned* confidence is the north star.
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
from ..data.splits import time_blocked_split, walk_forward
from ..eval.metrics import crps_series, pit_values
from .real_tournament import _fit_log_trend
from .walkforward import _sign_aware_predict


def _coupled_point(y: np.ndarray, driver: np.ndarray, direction: int, tr: slice) -> np.ndarray:
    n = len(y)
    t = np.arange(n, dtype=float)
    a, b = _fit_log_trend(y[tr], t[tr])
    trend = np.exp(a * t + b)
    return _sign_aware_predict(y, trend, driver, tr, direction)


def _oos_residuals(y: np.ndarray, driver: np.ndarray, direction: int, train_end: int) -> np.ndarray:
    """One-step out-of-sample residuals from an expanding-window backtest *within* the train block."""
    mt = max(8, train_end // 2)
    res = []
    for sp in walk_forward(train_end, min_train=mt, horizon=1):
        pred = _coupled_point(y[:train_end], driver[:train_end], direction, sp.train)
        i = sp.test.start
        res.append(float(y[i] - pred[i]))
    return np.asarray(res, dtype=float) if res else np.array([0.0])


@dataclass(frozen=True)
class UncertaintyScore:
    coupling: str
    n_test: int
    pit_in_iqr_overconfident: float  # in-sample bands (Round 19 style)
    pit_in_iqr_honest: float  # OOS bias-corrected, horizon-fanning bands
    pit_mean_honest: float
    crps_honest: float

    @property
    def calibration_improved(self) -> bool:
        return self.pit_in_iqr_honest > self.pit_in_iqr_overconfident

    @property
    def honest_is_calibrated(self) -> bool:
        """Roughly calibrated: PIT centred (mean near 0.5) and a healthy share in the central half."""
        return abs(self.pit_mean_honest - 0.5) < 0.2 and self.pit_in_iqr_honest >= 0.35


def score_honest_uncertainty(
    coupling: str, y: np.ndarray, driver: np.ndarray, direction: int, test_frac: float = 0.3, seed: int = 0, m: int = 400
) -> UncertaintyScore:
    n = len(y)
    split = time_blocked_split(n, test_frac)
    tr, te = split.train, split.test
    cut = te.start
    rng = np.random.default_rng(seed)

    point = _coupled_point(y, driver, direction, tr)

    # Overconfident reference (Round 19): flat in-sample residual spread.
    in_resid = y[tr] - point[tr]
    samp_over = point[te][:, None] + rng.choice(in_resid, size=(n - cut, m), replace=True)
    pit_over = pit_values(samp_over, y[te])

    # Honest: OOS bias correction + horizon-fanning bands from OOS residuals.
    oos = _oos_residuals(y, driver, direction, cut)
    bias = float(np.mean(oos))
    centered = oos - bias
    leads = np.arange(1, n - cut + 1, dtype=float)
    draws = rng.choice(centered, size=(n - cut, m), replace=True)
    samp_honest = (point[te] + bias)[:, None] + np.sqrt(leads)[:, None] * draws
    pit_honest = pit_values(samp_honest, y[te])

    return UncertaintyScore(
        coupling=coupling,
        n_test=int(n - cut),
        pit_in_iqr_overconfident=float(np.mean((pit_over >= 0.25) & (pit_over <= 0.75))),
        pit_in_iqr_honest=float(np.mean((pit_honest >= 0.25) & (pit_honest <= 0.75))),
        pit_mean_honest=float(np.mean(pit_honest)),
        crps_honest=crps_series(samp_honest, y[te]),
    )


def run_all_honest_uncertainty() -> dict[str, UncertaintyScore]:
    gdp = load_real_gdp_co2()
    food = load_real_food()
    cob = load_real_cobenefit()
    nex = load_real_nexus()
    return {
        "climate->GDP": score_honest_uncertainty("climate->GDP", gdp.column("gdp"), gdp.column("cum_co2"), -1),
        "warming->yield": score_honest_uncertainty("warming->yield", food.column("cereal_yield"), food.column("temp"), -1),
        "PM2.5->mortality": score_honest_uncertainty("PM2.5->mortality", cob.column("death_rate"), cob.column("pm25"), +1),
        "energy->food": score_honest_uncertainty("energy->food", nex.column("food_price"), nex.column("energy_price"), +1),
    }
