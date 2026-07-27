"""Quarterly Energy⇄Inflation confirmation tests (Iter 48).

The keep, re-run at quarterly frequency (~8 walk-forward folds vs ~4 annual), holds: energy-price growth
beats baseline, placebo, persistence, and naive in a majority of folds with the right sign. The project's
one solid real-data keep is not an artifact of low-power annual data.
"""

from __future__ import annotations

import pytest

from polyphony.data.loaders import has_real_inflation_q
from polyphony.experiments.inflation_quarterly import run_quarterly_confirmation

pytestmark = pytest.mark.skipif(not has_real_inflation_q(), reason="quarterly inflation dataset not fetched")


def test_keep_holds_at_higher_frequency_with_more_folds():
    r = run_quarterly_confirmation()
    assert r.wf_folds >= 6  # roughly double the annual walk-forward's folds
    assert r.corr > 0.5 and r.sign_as_assumed
    assert r.wf_beats_baseline > 0.5
    assert r.wf_beats_placebo > 0.5
    assert r.wf_beats_persistence > 0.5
    assert r.wf_beats_naive > 0.5
    assert r.robust_verdict() == "keep"
