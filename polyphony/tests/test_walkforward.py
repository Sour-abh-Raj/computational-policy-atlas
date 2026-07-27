"""Walk-forward cross-validation tests (Iter 23 — robustness of the real-data verdicts).

Re-runs every real coupling over an expanding-window walk-forward and checks that the **cut** verdicts
hold across folds, not just on one split. The robust, split-independent finding is unified: none of the
four real couplings beats a **naive** random-walk forecast in a majority of folds — that, not the
split-dependent placebo comparison, is why they are all cut.
"""

from __future__ import annotations

import pytest

from polyphony.data.loaders import (
    has_real_cobenefit,
    has_real_food,
    has_real_gdp_co2,
    has_real_nexus,
)
from polyphony.experiments.walkforward import run_all_walk_forward

pytestmark = pytest.mark.skipif(
    not (has_real_gdp_co2() and has_real_food() and has_real_cobenefit() and has_real_nexus()),
    reason="real datasets not all fetched; run `python -m polyphony.data.fetch_real`",
)


def test_all_real_couplings_are_robustly_cut_across_folds():
    reports = run_all_walk_forward()
    assert set(reports) == {"climate->GDP", "warming->yield", "PM2.5->mortality", "energy->food"}
    for name, r in reports.items():
        assert r.n_folds >= 3, f"{name}: too few folds for a robustness check"
        assert r.robust_verdict() == "cut", f"{name}: expected a robust cut"


def test_the_robust_common_reason_is_no_skill_versus_naive():
    reports = run_all_walk_forward()
    # The unified, split-independent reason for every cut: the coupling fails to beat a naive random walk
    # in a majority of folds (MASE ≥ 1), even where it beats a trend or a placebo.
    for name, r in reports.items():
        assert r.frac_beats_naive <= 0.5, f"{name}: unexpectedly beats naive in a majority of folds"
