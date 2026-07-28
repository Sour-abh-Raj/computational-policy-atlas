"""Panel-validation tests (Iter 33) — the two-way-FE method, and its real-data confirmation.

Two levels: (1) the fixed-effects estimator itself is validated on synthetic panels where the truth is
known (a pure confound must demean to ≈0; a real within-effect must survive); (2) on the real 100+ country
carbon-leakage panel, the pooled openness↔gap correlation nearly vanishes under two-way FE — confirming the
Iter-30 "confounded-away" cut with far more power than one UK time series.
"""

from __future__ import annotations

import numpy as np
import pytest

from polyphony.data.loaders import (
    has_real_demographic_panel,
    has_real_leakage_panel,
    has_real_pm25_mortality_panel,
    has_real_preston_panel,
)
from polyphony.experiments.panel_validation import (
    run_all_panels,
    run_demographic_panel,
    run_leakage_panel,
    run_pm25_mortality_panel,
    run_preston_panel,
    two_way_within,
)


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


@pytest.mark.skipif(not has_real_pm25_mortality_panel(), reason="real PM2.5/mortality panel not fetched")
def test_pm25_mortality_panel_cannot_recover_the_effect():
    # The PM2.5 → mortality mechanism is real at the cohort level, but all-cause mortality is dominated by
    # within-country development/aging trends, so panel FE cannot recover a positive within-country effect.
    r = run_pm25_mortality_panel()
    assert r.n_countries >= 100  # a large panel
    assert not r.within_has_assumed_sign  # no positive within signal (it is weak / wrong-signed)
    assert r.verdict() == "no within-country mechanism (outcome confounded)"


@pytest.mark.skipif(not has_real_preston_panel(), reason="real Preston panel not fetched")
def test_preston_curve_survives_panel_fe_a_boundary_case():
    # The boundary of the central generalization: a coupling with a REAL within-unit mechanism (income →
    # life expectancy) keeps its positive within-country correlation under two-way fixed effects — unlike the
    # confounded-away leakage panel. The instrument is not a "nothing works" machine.
    r = run_preston_panel()
    assert r.n_countries >= 100
    assert r.pooled_corr > 0.5
    assert r.within_corr > 0.1  # a real within-country effect survives (leakage's was ≈ 0.02)
    assert r.within_has_assumed_sign
    assert r.verdict() == "within-signal survives"


@pytest.mark.skipif(not has_real_demographic_panel(), reason="real demographic panel not fetched")
def test_demographic_transition_survives_a_second_survivor():
    # A second surviving panel coupling (income → fertility, assumed negative): richer countries have fewer
    # children even after two-way fixed effects — a robust within-country mechanism.
    r = run_demographic_panel()
    assert r.pooled_corr < -0.5
    assert r.within_corr < -0.05  # negative within effect survives
    assert r.within_has_assumed_sign
    assert r.verdict() == "within-signal survives"


@pytest.mark.skipif(
    not (has_real_leakage_panel() and has_real_preston_panel()),
    reason="real panels not fetched",
)
def test_panel_fe_discriminates_survivor_from_confounded():
    # Same tool, opposite verdicts: a genuine within-unit mechanism survives; a confounded one is cut.
    assert run_preston_panel().verdict() == "within-signal survives"
    assert run_leakage_panel().verdict() == "cut-confirmed (confounded-away)"


@pytest.mark.skipif(
    not (
        has_real_preston_panel()
        and has_real_demographic_panel()
        and has_real_leakage_panel()
        and has_real_pm25_mortality_panel()
    ),
    reason="real panels not fetched",
)
def test_panel_taxonomy_two_survivors_two_cut():
    # The panel domain's own honest taxonomy, mirroring the aggregate 2-keep/8-cut story: two couplings with
    # a genuine within-unit mechanism survive; two confounded ones do not.
    survive = [r for r in run_all_panels() if r.verdict() == "within-signal survives"]
    assert len(survive) == 2  # Preston + demographic transition


@pytest.mark.skipif(
    not (has_real_leakage_panel() and has_real_pm25_mortality_panel()),
    reason="real panels not fetched",
)
def test_panel_fe_works_only_when_the_outcome_is_clean():
    # The contrast is the lesson: FE isolates a mechanism only when the OUTCOME is not itself dominated by
    # a confounded within-country trajectory. Leakage's ratio is clean (FE confirms the cut); all-cause
    # mortality is not (FE cannot recover the real effect).
    leak = run_leakage_panel()
    pm = run_pm25_mortality_panel()
    assert leak.verdict() == "cut-confirmed (confounded-away)"
    assert pm.verdict() == "no within-country mechanism (outcome confounded)"
