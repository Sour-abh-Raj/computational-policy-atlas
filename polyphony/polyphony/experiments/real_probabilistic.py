"""Probabilistic scoring of the real-data couplings (Iter 24 — foreground uncertainty, not just error).

The point tournaments ask *is the coupled forecast accurate?* (MASE) — and on real aggregate series the
answer was no (Round 18: none beats naive). But the north star is **honesty about uncertainty**, and a
point score can't see whether a model's *bands* are trustworthy. This module turns each real coupling's
point forecast into a **predictive distribution** (point ± resampled train residuals) and scores it with
**CRPS** (Gneiting-Raftery: sharpness + calibration in one number) and the **PIT** (Dawid: uniform ⇒
calibrated). It compares the coupled ensemble to an honest **probabilistic naive** (persistence ± the
train first-difference spread).

Two honest questions, separately reported: (1) does the coupled predictive distribution have lower CRPS
than naive? (usually no, mirroring the point result); (2) is it at least **calibrated** — PIT centred and
covering nominally — or is it **overconfident** (bands too narrow out-of-sample)? Calibration is a
distinct virtue from accuracy, and reporting it is the point.
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
from ..data.splits import time_blocked_split
from ..eval.metrics import crps_series, pit_values
from .real_tournament import _fit_log_trend
from .walkforward import _sign_aware_predict


@dataclass(frozen=True)
class ProbScore:
    coupling: str
    n_test: int
    crps_coupled: float
    crps_naive: float
    pit_mean_coupled: float  # ≈ 0.5 if unbiased
    pit_in_iqr_coupled: float  # fraction of PIT in [0.25, 0.75]; ≈ 0.5 if calibrated

    @property
    def crps_beats_naive(self) -> bool:
        return self.crps_coupled < self.crps_naive

    @property
    def calibrated(self) -> bool:
        """Crude two-sided calibration: PIT roughly centred (mean near 0.5) and not badly under-dispersed
        (a healthy share of PIT values in the central half rather than piled at the 0/1 tails)."""
        return abs(self.pit_mean_coupled - 0.5) < 0.15 and self.pit_in_iqr_coupled >= 0.35


def _ensemble(point: np.ndarray, resid_pool: np.ndarray, rng: np.random.Generator, m: int) -> np.ndarray:
    """(T, M) ensemble = point forecast + resampled residuals (empirical predictive spread)."""
    draws = rng.choice(resid_pool, size=(len(point), m), replace=True)
    return point[:, None] + draws


def score_real_coupling(
    coupling: str,
    y: np.ndarray,
    driver: np.ndarray,
    direction: int,
    test_frac: float = 0.3,
    seed: int = 0,
    m: int = 200,
) -> ProbScore:
    n = len(y)
    t = np.arange(n, dtype=float)
    split = time_blocked_split(n, test_frac)
    tr, te = split.train, split.test
    rng = np.random.default_rng(seed)

    a, b = _fit_log_trend(y[tr], t[tr])
    trend = np.exp(a * t + b)
    coupled = _sign_aware_predict(y, trend, driver, tr, direction)
    resid = y[tr] - coupled[tr]
    samp_c = _ensemble(coupled[te], resid, rng, m)

    # Honest probabilistic naive: persistence (previous observed value) ± the train first-difference spread.
    cut = split.test.start
    persistence = y[cut - 1 : n - 1]
    naive_resid = np.diff(y[tr])
    samp_n = _ensemble(persistence, naive_resid, rng, m)

    pit_c = pit_values(samp_c, y[te])
    return ProbScore(
        coupling=coupling,
        n_test=int(n - cut),
        crps_coupled=crps_series(samp_c, y[te]),
        crps_naive=crps_series(samp_n, y[te]),
        pit_mean_coupled=float(np.mean(pit_c)),
        pit_in_iqr_coupled=float(np.mean((pit_c >= 0.25) & (pit_c <= 0.75))),
    )


def run_all_probabilistic() -> dict[str, ProbScore]:
    """Probabilistic score for every real coupling, on its committed real dataset."""
    gdp = load_real_gdp_co2()
    food = load_real_food()
    cob = load_real_cobenefit()
    nex = load_real_nexus()
    return {
        "climate->GDP": score_real_coupling("climate->GDP", gdp.column("gdp"), gdp.column("cum_co2"), -1),
        "warming->yield": score_real_coupling("warming->yield", food.column("cereal_yield"), food.column("temp"), -1),
        "PM2.5->mortality": score_real_coupling("PM2.5->mortality", cob.column("death_rate"), cob.column("pm25"), +1),
        "energy->food": score_real_coupling("energy->food", nex.column("food_price"), nex.column("energy_price"), +1),
    }
