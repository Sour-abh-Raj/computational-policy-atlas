"""The panel instrument's second boundary (Iter 61) — direction-blindness under simultaneity.

Education⇄income survives the within-FE + out-of-sample bar, but the within-country lead-lag is symmetric
(schooling→income ≈ income→schooling), so the survival cannot be assigned a direction. The test pins that
honest reading: it survives, it is directionally ambiguous, and it is therefore NOT a reliable finding.
"""

from __future__ import annotations

import pytest

from polyphony.data.loaders import has_real_education_panel
from polyphony.experiments.education_directionality import (
    DirectionalityResult,
    boundary_summary,
    run_education_directionality,
)


def test_directionality_logic_is_consistent():
    # Structural (no network): symmetric lead-lag => ambiguous => not a reliable finding, even though it survives.
    ambiguous = DirectionalityResult(within_corr=0.22, oos_within_corr=0.38, lead_school_to_income=0.37, lead_income_to_school=0.38)
    assert ambiguous.within_survives
    assert ambiguous.directionally_ambiguous
    assert not ambiguous.is_reliable_finding
    # A resolved direction (one lead-lag clearly dominant) would instead be a usable finding.
    resolved = DirectionalityResult(within_corr=0.30, oos_within_corr=0.40, lead_school_to_income=0.40, lead_income_to_school=0.10)
    assert resolved.is_reliable_finding and not resolved.directionally_ambiguous


@pytest.mark.skipif(not has_real_education_panel(), reason="real education panel not fetched")
def test_education_survives_but_is_directionally_ambiguous_on_real_data():
    r = run_education_directionality()
    assert r.within_survives  # a real within-country co-movement that forecasts
    assert r.directionally_ambiguous  # ...but neither direction dominates the lead-lag
    assert not r.is_reliable_finding  # so it is NOT promoted to a reliable finding (necessary != sufficient)
    assert "ambiguous" in r.verdict().lower()


@pytest.mark.skipif(not has_real_education_panel(), reason="real education panel not fetched")
def test_reverse_channel_is_not_weaker_than_the_assumed_one():
    # The optimistic "schooling drives income" channel is not stronger than the reverse (income funds schooling).
    r = run_education_directionality()
    assert r.lead_income_to_school >= r.lead_school_to_income - 0.1


@pytest.mark.skipif(not has_real_education_panel(), reason="real education panel not fetched")
def test_boundary_summary_states_necessary_not_sufficient():
    s = boundary_summary().lower()
    assert "not sufficient" in s and "directional" in s
