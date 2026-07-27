"""Panel-validation tests (Iter 33) — the two-way-FE method, and its real-data confirmation.

Two levels: (1) the fixed-effects estimator itself is validated on synthetic panels where the truth is
known (a pure confound must demean to ≈0; a real within-effect must survive); (2) on the real 100+ country
carbon-leakage panel, the pooled openness↔gap correlation nearly vanishes under two-way FE — confirming the
Iter-30 "confounded-away" cut with far more power than one UK time series.
"""

from __future__ import annotations

import numpy as np
import pytest

from polyphony.data.loaders import has_real_leakage_panel
from polyphony.experiments.panel_validation import run_leakage_panel, two_way_within


def _make_panel(units: int, years: int):
    u, t = [], []
    for ui in range(units):
        for yi in range(years):
            u.append(f"U{ui}")
            t.append(yi)
    return np.array(u, dtype=object), np.array(t, dtype=int)


def test_pure_confound_demeans_to_zero():
    """Driver = a common year trend, value = the same trend + a unit level ⇒ NO within relationship."""
    unit, year = _make_panel(8, 12)
    driver = year.astype(float)  # identical trend in every unit
    value = year.astype(float) + np.array([hash(u) % 5 for u in unit], dtype=float)  # trend + unit offset
    pooled = float(np.corrcoef(driver, value)[0, 1])
    within = two_way_within(value, driver, unit, year)
    assert pooled > 0.5  # pooled looks strongly related
    assert abs(within) < 0.05  # …but two-way FE reveals no within-unit mechanism


def test_real_within_effect_survives_fixed_effects():
    """A genuine within-unit effect (plus confounds) must be recovered by two-way FE."""
    unit, year = _make_panel(10, 15)
    rng = np.random.default_rng(0)
    driver_within = rng.normal(0, 1, len(unit))
    year_confound = year.astype(float)
    unit_level = np.array([hash(u) % 7 for u in unit], dtype=float)
    driver = driver_within + year_confound
    value = 1.5 * driver_within + year_confound + unit_level  # real within slope 1.5 + confounds
    within = two_way_within(value, driver, unit, year)
    assert within > 0.5  # the within mechanism survives the fixed effects


@pytest.mark.skipif(not has_real_leakage_panel(), reason="real leakage panel not fetched")
def test_real_leakage_panel_confirms_confounded_away():
    r = run_leakage_panel()
    assert r.n_countries >= 50 and r.n_obs >= 1000  # a genuine panel
    assert r.pooled_corr > 0.2  # the naive leakage story (a positive pooled correlation)
    assert abs(r.within_corr) < 0.1  # …vanishes under two-way fixed effects
    assert r.attenuation > 0.7  # most of the correlation was the shared trend
    assert r.verdict() == "cut-confirmed (confounded-away)"
