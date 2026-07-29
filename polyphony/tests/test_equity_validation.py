"""Equity-validation tests (Iters 57–58) — the welfare/equity dimension, held to the panel-survivor bar.

Two distributional/welfare couplings are put through the *same* two-way fixed-effects + out-of-sample
instrument that separated the panel survivors, and the honest nuanced pair is pinned:

- income → *relative* inequality (Kuznets) is a **cut** (confounded-away within countries), and
- income → *absolute* poverty is a **survivor** (strong within effect that forecasts held-out years).

So growth is a validated within-country lever on absolute poverty but not on relative inequality.
"""

from __future__ import annotations

import pytest

from polyphony.data.loaders import (
    has_real_inequality_panel,
    has_real_poverty_panel,
    has_real_shared_prosperity_panel,
)
from polyphony.experiments.equity_validation import (
    EquityFinding,
    equity_dimension_summary,
    run_inequality_equity_test,
    run_poverty_equity_test,
    run_shared_prosperity_equity_test,
)


def test_equity_finding_cut_and_survivor_logic_is_consistent():
    # Structural (no network): a collapsed within-corr with ~0 OOS is a cut...
    cut = EquityFinding("q", "income↑→Gini↓", -1, -0.35, 0.07, -0.02, "cut", "l")
    assert cut.is_cut and not cut.is_survivor and cut.pooled_is_optimistic
    # ...and a strong within-corr with the assumed sign that forecasts is a survivor.
    surv = EquityFinding("q", "income↑→poverty↓", -1, -0.72, -0.48, 0.58, "survives", "l")
    assert surv.is_survivor and not surv.is_cut and surv.pooled_is_optimistic


@pytest.mark.skipif(not has_real_inequality_panel(), reason="real inequality panel not fetched")
def test_relative_inequality_is_a_confounded_away_cut_on_real_data():
    f = run_inequality_equity_test()
    assert f.pooled_is_optimistic  # richer countries more equal cross-sectionally...
    assert f.is_cut  # ...but the within-country effect collapses and does not forecast
    assert "cut" in f.verdict.lower()
    # ~80% of the pooled association is a between-country level artifact.
    assert abs(f.within_corr) < 0.4 * abs(f.pooled_corr)


@pytest.mark.skipif(not has_real_poverty_panel(), reason="real poverty panel not fetched")
def test_absolute_poverty_survives_and_forecasts_on_real_data():
    f = run_poverty_equity_test()
    assert f.pooled_is_optimistic
    assert f.is_survivor  # strong within effect, assumed sign, forecasts out of sample
    assert f.within_corr < -0.2  # income up -> poverty down, and non-trivial within countries
    assert f.oos_within_corr > 0.2  # genuinely forecasts held-out years


@pytest.mark.skipif(not has_real_shared_prosperity_panel(), reason="real shared-prosperity panel not fetched")
def test_shared_prosperity_share_is_also_a_cut_a_second_relative_measure():
    # A second, independent RELATIVE measure (bottom-40 income share) behaves like the Gini cut, not poverty.
    f = run_shared_prosperity_equity_test()
    assert f.pooled_is_optimistic  # richer countries give the bottom 40% a larger share (cross-sectionally)
    assert f.is_cut and not f.is_survivor  # ...but confounded-away within countries
    assert "cut" in f.verdict.lower()


@pytest.mark.skipif(
    not (has_real_inequality_panel() and has_real_shared_prosperity_panel() and has_real_poverty_panel()),
    reason="real equity panels not fetched",
)
def test_summary_states_the_nuanced_welfare_message():
    s = equity_dimension_summary().lower()
    assert "poverty" in s and "survives" in s
    assert "inequality" in s and "cut" in s
    assert "shared-prosperity share" in s  # both relative measures reported as cut
