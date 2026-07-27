"""Trade⇄Emissions (carbon leakage) seventh-loop tests (issue #12).

Same three-way honesty machinery: a real coupling must beat its sum-of-parts under a fair calibration,
be cut on a no-leakage control, and have the assumed sign (more leakage ⇒ consumption above production).
Synthetic keep proves the machinery; the real-data test (OWID production vs consumption CO₂) is the gap.
"""

from __future__ import annotations

from polyphony.core.interface import conforms
from polyphony.data.loaders import synthetic_leakage_series, synthetic_no_leakage_series
from polyphony.experiments.tradeemissions import (
    calibrated_synergy,
    consumption_emissions_track,
    run_two_regime_tournament,
)
from polyphony.models import ReducedFormTrade


def test_trade_voice_conforms_to_model_protocol():
    assert conforms(ReducedFormTrade())


def test_leakage_lifts_consumption_above_production_over_time():
    """As globalisation builds, the trade-coupled consumption track should rise above the leakage-blind
    (production) track — the carbon-leakage gap widening."""
    coupled = consumption_emissions_track(0.6, 20, coupled=True)
    blind = consumption_emissions_track(0.6, 20, coupled=False)
    assert coupled[-1] > blind[-1]
    assert coupled[-1] > coupled[0]  # the embodied-carbon gap grows


def test_leakage_coupling_beats_baseline_and_control_is_cut():
    res = run_two_regime_tournament()
    assert res["leakage_regime"].synergy.delta > 0
    assert res["no_leakage_regime"].synergy.delta == 0.0


def test_leakage_coupling_survives_fair_calibration_with_right_sign():
    cs = calibrated_synergy(synthetic_leakage_series())
    assert cs.delta > 0.05
    assert cs.leakage_consumption_corr > 0.5  # more leakage ⇒ higher consumption emissions, as assumed
    assert cs.sign_as_assumed
    assert cs.verdict() == "keep"


def test_no_leakage_control_is_cut_under_fair_calibration():
    ns = calibrated_synergy(synthetic_no_leakage_series())
    assert ns.delta <= 0.05
    assert ns.verdict() == "cut"
