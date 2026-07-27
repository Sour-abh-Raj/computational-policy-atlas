"""Urban⇄Transport⇄Energy⇄Health (co-benefits) fourth-loop tests (issue #7).

Same three-way honesty machinery as the other domains: a real coupling must (a) beat its sum-of-parts
under a **fair** calibration (not just a level artifact), (b) be **cut** on a negative control where no
coupling exists, and (c) have the **assumed sign** (more PM2.5 ⇒ more mortality). Synthetic keep proves
the machinery, not real skill — the real-data placebo test is tracked as the open gap.
"""

from __future__ import annotations

from polyphony.core.interface import conforms
from polyphony.data.loaders import synthetic_cobenefit_series, synthetic_flat_health_series
from polyphony.experiments.urbanhealth import (
    calibrated_synergy,
    health_burden_track,
    run_two_regime_tournament,
)
from polyphony.models import ReducedFormAirHealth, ReducedFormTransport


def test_new_voices_conform_to_model_protocol():
    assert conforms(ReducedFormTransport())
    assert conforms(ReducedFormAirHealth())


def test_transport_policy_lowers_exposure_over_time():
    """A carbon price should pull PM2.5 below its no-policy path as travel behaviour adjusts (inertia)."""
    no_policy = health_burden_track(0.0, 20, coupled=True)
    with_policy = health_burden_track(200.0, 20, coupled=True)
    # Both start near the same burden, but the priced path ends strictly lower (co-benefit accrues).
    assert with_policy[-1] < no_policy[-1]


def test_raw_synergy_is_a_level_artifact_before_calibration():
    """The policy-blind baseline has no level, so RAW synergy is huge in BOTH regimes — which is exactly
    why the fair-calibration test (below) is the one that decides keep/cut."""
    res = run_two_regime_tournament()
    assert res["cobenefit_regime"].synergy.delta > 0
    assert res["flat_regime"].synergy.delta > 0  # spurious: a level artifact, not real coupling


def test_cobenefit_coupling_survives_fair_calibration_and_has_right_sign():
    cs = calibrated_synergy(synthetic_cobenefit_series())
    assert cs.delta > 0.05  # still helps after the baseline gets its OWN affine fit
    assert cs.coupled_beats_naive
    assert cs.pm25_burden_corr > 0.5  # more PM2.5 ⇒ more mortality, as the mechanism assumes
    assert cs.sign_as_assumed
    assert cs.verdict() == "keep"


def test_negative_control_is_cut_under_fair_calibration():
    fs = calibrated_synergy(synthetic_flat_health_series())
    assert fs.delta <= 0.05  # no coupling in the DGP ⇒ the transport channel earns nothing
    assert fs.verdict() == "cut"
