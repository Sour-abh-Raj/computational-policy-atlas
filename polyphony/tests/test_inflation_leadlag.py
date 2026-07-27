"""Energy⇄Inflation lead-lag tests (Iter 36) — a short-horizon forecaster with a base-effect reversal.

The keep is not just a nowcast: energy-price growth forecasts inflation one year ahead (right sign, beats
baselines), but skill decays and the correlation flips negative by year 2 (the classic base effect). The
study reports *how far ahead* the skill reaches and where it reverses.
"""

from __future__ import annotations

import pytest

from polyphony.data.loaders import has_real_inflation
from polyphony.experiments.inflation_leadlag import run_lead_lag_study

pytestmark = pytest.mark.skipif(not has_real_inflation(), reason="real inflation dataset not fetched")


def test_forecast_skill_reaches_one_year_ahead():
    s = run_lead_lag_study()
    by_lag = {r.lag: r for r in s.lags}
    assert by_lag[0].verdict() == "keep"  # nowcast
    assert by_lag[1].verdict() == "keep"  # genuine one-year-ahead forecast
    assert s.forecast_horizon == 1


def test_skill_decays_and_sign_flips_by_two_years():
    s = run_lead_lag_study()
    by_lag = {r.lag: r for r in s.lags}
    assert by_lag[2].verdict() == "cut"  # skill gone by year 2
    assert by_lag[2].corr < 0.0  # base effect: a spike now ⇒ lower inflation two years later
    assert s.sign_flips
