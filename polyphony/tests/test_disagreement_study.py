"""Disagreement-study tests (Iter 32) — paradigm disagreement activates with policy.

Polyphony reports disagreement rather than averaging it. This study shows the equilibrium/disequilibrium
split on GDP is small when no carbon price acts and jumps several-fold once one bites — so the choice of
economic paradigm matters most exactly where a real policy is contemplated.
"""

from __future__ import annotations

from polyphony.experiments.disagreement_study import run_disagreement_study


def test_disagreement_is_small_at_zero_policy():
    s = run_disagreement_study()
    assert s.points[0].carbon_price == 0.0
    assert s.d_at_zero < 0.05  # near-agreement when nothing is happening


def test_disagreement_activates_with_a_carbon_price():
    s = run_disagreement_study()
    assert s.d_peak > 0.1
    assert s.activation_ratio > 3.0
    assert s.activates_with_policy()


def test_paradigms_straddle_the_baseline_at_peak():
    # At the peak-disagreement policy, the equilibrium voice says carbon pricing LOWERS output while the
    # disequilibrium voice says it RAISES output — opposite signs, both reported, never averaged.
    s = run_disagreement_study()
    assert s.paradigms_split_by_sign()
    peak = max(s.points, key=lambda p: p.index_D)
    assert peak.cge_gdp < 100.0 < peak.e3me_gdp
