"""Water⇄Energy⇄Food nexus fifth-loop tests (issue #10).

Same three-way honesty machinery as the other domains: a real coupling must (a) beat its sum-of-parts
under a **fair** calibration (not just a level artifact), (b) be **cut** on a negative control where no
coupling exists, and (c) have the **assumed sign** (more water stress ⇒ higher food price). Synthetic
keep proves the machinery, not real skill — the real-data placebo test is tracked as the open gap.
"""

from __future__ import annotations

from polyphony.core.interface import conforms
from polyphony.data.loaders import synthetic_flat_nexus_series, synthetic_nexus_series
from polyphony.experiments.waternexus import (
    calibrated_synergy,
    nexus_price_track,
    run_two_regime_tournament,
)
from polyphony.models import ReducedFormNexusFood, ReducedFormWater


def test_new_voices_conform_to_model_protocol():
    assert conforms(ReducedFormWater())
    assert conforms(ReducedFormNexusFood())


def test_drought_raises_food_price_over_time():
    """A sustained precipitation deficit should push food price above its no-drought path as the store
    draws down (storage dynamics turn a constant deficit into a rising stress path)."""
    normal = nexus_price_track(1.0, 20, coupled=True)
    drought = nexus_price_track(0.7, 20, coupled=True)
    assert drought[-1] > normal[-1]
    assert drought[-1] > drought[0]  # price climbs as the buffer empties


def test_raw_synergy_is_a_level_artifact_before_calibration():
    """The water-blind baseline has no level, so RAW synergy is huge in the drought regime — which is why
    the fair-calibration test (below) is the one that decides keep/cut."""
    res = run_two_regime_tournament()
    assert res["drought_regime"].synergy.delta > 0
    assert res["flat_regime"].synergy.delta == 0.0  # no coupling in the DGP ⇒ nothing to gain


def test_nexus_coupling_survives_fair_calibration_and_has_right_sign():
    cs = calibrated_synergy(synthetic_nexus_series())
    assert cs.delta > 0.05  # still helps after the baseline gets its OWN affine fit
    assert cs.coupled_beats_naive
    assert cs.stress_price_corr > 0.5  # more water stress ⇒ higher food price, as assumed
    assert cs.sign_as_assumed
    assert cs.verdict() == "keep"


def test_negative_control_is_cut_under_fair_calibration():
    fs = calibrated_synergy(synthetic_flat_nexus_series())
    assert fs.delta <= 0.05
    assert fs.verdict() == "cut"
