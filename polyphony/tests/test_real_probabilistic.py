"""Probabilistic (CRPS/PIT) scoring tests for the real couplings (Iter 24 — foreground uncertainty).

The point tournaments showed the real couplings don't beat naive. Probabilistic scoring adds the second,
distinct verdict: their predictive *bands* (built from in-sample residuals) are **grossly overconfident**
out-of-sample — the PIT piles at the tails (almost no coverage), because out-of-sample error is dominated
by trend-extrapolation bias the train residuals never saw. Inaccurate AND overconfident is exactly what a
single-confident-number simulator would hide; naming it is the point.
"""

from __future__ import annotations

import pytest

from polyphony.data.loaders import (
    has_real_cobenefit,
    has_real_food,
    has_real_gdp_co2,
    has_real_nexus,
)
from polyphony.experiments.real_probabilistic import run_all_probabilistic

pytestmark = pytest.mark.skipif(
    not (has_real_gdp_co2() and has_real_food() and has_real_cobenefit() and has_real_nexus()),
    reason="real datasets not all fetched; run `python -m polyphony.data.fetch_real`",
)


def test_probabilistic_scores_cover_all_couplings():
    scores = run_all_probabilistic()
    assert set(scores) == {"climate->GDP", "warming->yield", "PM2.5->mortality", "energy->food"}


def test_real_couplings_are_inaccurate_and_overconfident():
    for name, s in run_all_probabilistic().items():
        # (1) Inaccurate: the coupled predictive distribution does not beat a probabilistic naive on CRPS.
        assert not s.crps_beats_naive, f"{name}: unexpectedly beats naive on CRPS"
        # (2) Overconfident: the PIT is piled at the tails — the bands almost never contain the truth.
        assert s.pit_in_iqr_coupled < 0.2, f"{name}: unexpectedly well-dispersed"
        assert not s.calibrated, f"{name}: unexpectedly calibrated"
