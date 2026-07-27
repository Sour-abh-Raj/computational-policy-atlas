"""Probabilistic-calibration tests for the Energy⇄Inflation keep (Iter 49).

Completes the uncertainty picture: the *cut* couplings were inaccurate AND grossly overconfident (Iter 24);
the one coupling that clears the bar is accurate AND calibrated — its predictive distribution beats a naive
one on CRPS and its PIT is centred with roughly nominal coverage. Skill and honest uncertainty travel
together here.
"""

from __future__ import annotations

import pytest

from polyphony.data.loaders import has_real_inflation
from polyphony.experiments.inflation_probabilistic import score_inflation_keep

pytestmark = pytest.mark.skipif(not has_real_inflation(), reason="real inflation dataset not fetched")


def test_the_keep_is_accurate_and_calibrated():
    r = score_inflation_keep()
    # Accurate: the coupled predictive distribution beats a naive one on CRPS…
    assert r.crps_beats_naive
    # …and calibrated: PIT centred (mean near 0.5) with a healthy central coverage — the opposite of the
    # cut couplings' tail-piled, overconfident PITs.
    assert abs(r.pit_mean - 0.5) < 0.15
    assert r.pit_in_iqr >= 0.35
    assert r.calibrated
