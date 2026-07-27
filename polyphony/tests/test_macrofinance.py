"""Macro⇄Finance (financial-accelerator) sixth-loop tests (issue #11).

Same three-way honesty machinery as the other domains: a real coupling must (a) beat its sum-of-parts
under a fair calibration, (b) be cut on a decoupled negative control, and (c) have the assumed sign
(more credit stress ⇒ lower GDP). Synthetic keep proves the machinery; the real-data placebo test (a
credit-spread → output series) is tracked as the open gap.
"""

from __future__ import annotations

from polyphony.core.interface import conforms
from polyphony.data.loaders import synthetic_decoupled_series, synthetic_financial_crisis_series
from polyphony.experiments.macrofinance import (
    calibrated_synergy,
    gdp_track,
    run_two_regime_tournament,
)
from polyphony.models import ReducedFormFinance


def test_finance_voice_conforms_to_model_protocol():
    assert conforms(ReducedFormFinance())


def test_credit_shock_produces_a_delayed_gdp_trough():
    """A credit shock should build to a delayed GDP trough (the leverage cycle), not an instant drop."""
    calm = gdp_track(0.0, 40, coupled=True)
    crisis = gdp_track(0.3, 40, coupled=True)
    trough = int(crisis.argmin())
    assert 8 <= trough <= 32, f"expected a mid-horizon trough, got t={trough}"
    assert crisis.min() < calm.min() - 5.0  # the crisis clearly drags output


def test_crisis_coupling_beats_baseline_and_control_is_cut():
    res = run_two_regime_tournament()
    assert res["crisis_regime"].synergy.delta > 0  # coupled tracks the crisis; flat baseline can't
    assert res["decoupled_regime"].synergy.delta == 0.0  # no coupling in the control


def test_crisis_coupling_survives_fair_calibration_with_right_sign():
    cs = calibrated_synergy(synthetic_financial_crisis_series())
    assert cs.delta > 0.05  # still helps after the baseline gets its own affine fit
    assert cs.coupled_beats_naive
    assert cs.spread_gdp_corr < -0.5  # more credit stress ⇒ lower GDP, as assumed
    assert cs.sign_as_assumed
    assert cs.verdict() == "keep"


def test_negative_control_is_cut_under_fair_calibration():
    dd = calibrated_synergy(synthetic_decoupled_series())
    assert dd.delta <= 0.05
    assert dd.verdict() == "cut"
