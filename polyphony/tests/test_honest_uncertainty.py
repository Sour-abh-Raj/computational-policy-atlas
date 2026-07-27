"""Honest-uncertainty tests (Iter 25 — turning the overconfidence diagnosis into a fix, honestly).

Out-of-sample bias correction + horizon-fanning bands make the predictive distribution **calibrated where
the future resembles the past** (climate→GDP, warming→yield: central coverage rises from 0), demonstrating
that honest uncertainty is achievable even for a coupling with no point skill. But they **cannot** rescue
couplings whose test block contains a genuine regime break the train backtest never saw (PM2.5→mortality's
aging upturn; energy→food's 2022 shock) — an honesty lesson in its own right: historical residuals cannot
insure against structural breaks.
"""

from __future__ import annotations

import pytest

from polyphony.data.loaders import (
    has_real_cobenefit,
    has_real_food,
    has_real_gdp_co2,
    has_real_nexus,
)
from polyphony.experiments.honest_uncertainty import run_all_honest_uncertainty

pytestmark = pytest.mark.skipif(
    not (has_real_gdp_co2() and has_real_food() and has_real_cobenefit() and has_real_nexus()),
    reason="real datasets not all fetched; run `python -m polyphony.data.fetch_real`",
)


def test_baseline_in_sample_bands_are_overconfident_for_all():
    reports = run_all_honest_uncertainty()
    assert set(reports) == {"climate->GDP", "warming->yield", "PM2.5->mortality", "energy->food"}
    for name, s in reports.items():
        assert s.pit_in_iqr_overconfident == 0.0, f"{name}: in-sample bands unexpectedly cover"


def test_honest_bands_calibrate_where_no_regime_break():
    reports = run_all_honest_uncertainty()
    # Where the future resembles the past, OOS bias-correction + horizon-fanning bands earn calibration:
    for name in ("climate->GDP", "warming->yield"):
        s = reports[name]
        assert s.calibration_improved, f"{name}: honest bands did not improve central coverage"
        assert s.pit_in_iqr_honest >= 0.35, f"{name}: honest bands still under-dispersed"
    assert reports["warming->yield"].honest_is_calibrated


def test_regime_breaks_defeat_historical_uncertainty():
    reports = run_all_honest_uncertainty()
    # …but a genuine structural break in the test block cannot be insured against from train residuals.
    unresolved = [n for n, s in reports.items() if not s.calibration_improved]
    assert unresolved, "expected at least one coupling whose regime break defeats historical uncertainty"
