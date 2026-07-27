"""Macro⇄Health underpower-demonstration tests (Iter 47).

Turns the "real test underpowered" claim from asserted to demonstrated: the modern GDP era has exactly one
pandemic episode (so the coupling cannot be learned-on-one-and-tested-on-another), and at annual resolution
the severity↔growth relationship is itself near zero (a lockdown-vs-deaths timing confound). The synthetic
keep is honest machinery; the real footing is genuinely thin.
"""

from __future__ import annotations

import pytest

from polyphony.data.loaders import has_real_finance
from polyphony.experiments.real_macrohealth import demonstrate_underpower

pytestmark = pytest.mark.skipif(not has_real_finance(), reason="real GDP series not fetched")


def test_one_pandemic_episode_cannot_be_cross_validated():
    r = demonstrate_underpower()
    assert r.n_pandemic_episodes == 1  # COVID is the one modern-era output-shock pandemic
    assert not r.identifiable_out_of_sample  # need >= 2 independent episodes; one cannot be validated
    assert r.underpowered


def test_annual_relationship_is_also_weak_in_sample():
    r = demonstrate_underpower()
    # A second, independent reason: at annual resolution severity and growth barely correlate (2021 had the
    # most deaths AND strong recovery growth) — the 2020 collapse came from lockdowns, not deaths directly.
    assert abs(r.insample_corr) < 0.3
    assert r.weak_in_sample
