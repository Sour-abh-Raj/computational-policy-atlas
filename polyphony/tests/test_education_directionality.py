"""Directional attribution + the lead-lag test's low power (Iters 61–62, a self-correction).

Iter 61 read education⇄income's symmetric lead-lag as distinguishing evidence of bidirectionality. Iter 62
runs the *same* lead-lag on the three income→X survivors and finds they are ALSO near-symmetric — so the test
does not discriminate direction for these persistent series (it is low-powered). The tests pin the corrected
reading: the lead-lag is near-symmetric for everything, so directional attribution rests on an external
manipulability argument, not on a data lead-lag.
"""

from __future__ import annotations

import pytest

from polyphony.data.loaders import (
    has_real_demographic_panel,
    has_real_education_panel,
    has_real_poverty_panel,
    has_real_preston_panel,
)
from polyphony.experiments.education_directionality import (
    DirectionalityResult,
    directional_attribution_summary,
    leadlag_test_is_low_power,
    run_education_directionality,
    survivor_directionality,
)

_HAVE_ALL = (
    has_real_education_panel()
    and has_real_preston_panel()
    and has_real_demographic_panel()
    and has_real_poverty_panel()
)


def test_symmetry_logic():
    # Structural: near-equal absolute lead-lags => symmetric.
    r = DirectionalityResult(within_corr=0.22, oos_within_corr=0.38, lead_forward=0.37, lead_reverse=0.38)
    assert r.within_survives and r.leadlag_symmetric


@pytest.mark.skipif(not has_real_education_panel(), reason="real education panel not fetched")
def test_education_survives_but_leadlag_is_symmetric():
    r = run_education_directionality()
    assert r.within_survives
    assert r.leadlag_symmetric


@pytest.mark.skipif(
    not (has_real_preston_panel() and has_real_demographic_panel() and has_real_poverty_panel()),
    reason="real survivor panels not fetched",
)
def test_the_survivors_are_also_leadlag_symmetric_the_correction():
    # The Iter-62 correction: the reliable-finding survivors show the SAME near-symmetric lead-lag as education,
    # so the lead-lag does NOT single out education — it is low-powered for these persistent series.
    for name, r in survivor_directionality().items():
        assert r.within_survives, name
        assert r.leadlag_symmetric, name  # reverse ≈ forward, just like education


@pytest.mark.skipif(not _HAVE_ALL, reason="real panels not fetched")
def test_leadlag_test_is_demonstrably_low_power():
    assert leadlag_test_is_low_power()  # near-symmetric for all four pairs (survivors + education)


def test_summary_states_direction_rests_on_manipulability_not_leadlag():
    s = directional_attribution_summary().lower()
    assert "manipulability" in s
    assert "low-power" in s or "cannot certify" in s
