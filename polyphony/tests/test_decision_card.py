"""Decision-card tests (Iter 28 — the north star: help a human choose, honestly).

The card must foreground the three things a single confident number hides: that the recommendation
depends on **values**, that **paradigms disagree** on the key outcome (and both answers are shown, not
averaged), and that the ensemble's couplings mostly **failed real-data validation** — so it is
decision-support under deep uncertainty, not a forecast.
"""

from __future__ import annotations

from polyphony.experiments.decision_card import build_decision_card


def test_recommendation_depends_on_values():
    c = build_decision_card()
    assert set(c.recommendation_by_value) == {"utilitarian", "prioritarian", "rawlsian_tail_averse"}
    # The whole point of exposing values as a dial: the recommendation is not value-invariant here.
    assert not c.values_agree


def test_paradigms_disagree_on_gdp_and_both_answers_are_kept():
    c = build_decision_card()
    assert c.paradigms_disagree_on_gdp
    assert c.gdp_disagreement_D > 0.0
    # Equilibrium (CGE) and disequilibrium (E3ME) give opposite-signed GDP responses to carbon pricing —
    # one below the 100 base, one above — and BOTH are reported, never silently averaged.
    vals = c.gdp_paradigm_answers
    assert "cge" in vals and "e3me" in vals
    assert min(vals.values()) < 100.0 < max(vals.values())


def test_validation_status_is_disclosed_and_honest():
    c = build_decision_card()
    # Two couplings kept (Macro⇄Health, Energy⇄Inflation), eight cut — the card discloses this, not hides it.
    assert len(c.kept_couplings) == 2
    assert len(c.cut_couplings) == 8
    summary = c.honest_summary()
    assert "NOT a forecast" in summary
    assert "failed real-data validation" in summary


def test_pareto_front_is_reported():
    c = build_decision_card()
    assert len(c.pareto_front) >= 1
    assert all(name.startswith("cp=") for name in c.pareto_front)
