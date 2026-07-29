"""Equity-validation tests (Iter 57) — the first distributional outcome, held to the panel-survivor bar.

The income→inequality (Kuznets) coupling is put through the *same* two-way fixed-effects + out-of-sample
instrument that separated the panel survivors. On real World Bank data the honest verdict is a **cut**: the
pooled cross-country correlation is optimistic (negative), but it is confounded-away within countries and does
not forecast — so 'growth reduces inequality' is a between-country level artifact, not a within-country lever.
"""

from __future__ import annotations

import pytest

from polyphony.data.loaders import has_real_inequality_panel
from polyphony.experiments.equity_validation import (
    EquityFinding,
    equity_dimension_summary,
    run_inequality_equity_test,
)


def test_equity_finding_cut_logic_is_consistent():
    # Structural (no network): a finding with a collapsed within-corr and ~0 OOS is a cut with an optimistic pool.
    f = EquityFinding(
        question="q",
        optimistic_claim="income up -> Gini down",
        pooled_corr=-0.35,
        within_corr=0.07,
        oos_within_corr=-0.02,
        verdict="cut-confirmed (confounded-away)",
        lesson="l",
    )
    assert f.is_cut
    assert f.pooled_is_optimistic


@pytest.mark.skipif(not has_real_inequality_panel(), reason="real inequality panel not fetched")
def test_income_inequality_is_a_confounded_away_cut_on_real_data():
    f = run_inequality_equity_test()
    # The optimistic story shows up cross-country...
    assert f.pooled_is_optimistic  # pooled corr negative (richer countries more equal)
    # ...but collapses within countries and does not forecast: an honest CUT on the equity dimension.
    assert f.is_cut
    assert "cut" in f.verdict.lower()


@pytest.mark.skipif(not has_real_inequality_panel(), reason="real inequality panel not fetched")
def test_within_effect_is_far_smaller_than_pooled():
    # ~80% of the pooled association is a between-country level artifact.
    f = run_inequality_equity_test()
    assert abs(f.within_corr) < 0.4 * abs(f.pooled_corr)


@pytest.mark.skipif(not has_real_inequality_panel(), reason="real inequality panel not fetched")
def test_equity_summary_mentions_the_lever_conclusion():
    s = equity_dimension_summary().lower()
    assert "inequality" in s and "within-country lever" in s
