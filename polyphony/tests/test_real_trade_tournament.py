"""Real Trade⇄Emissions tournament tests (issue #12-real).

The synthetic leakage coupling was kept (Iter 29); this checks the real-data verdict on the UK (the
textbook leakage case). The honest outcome is a **CUT of the confounded-away kind**: the UK's
consumption/production gap really grew with trade openness (corr ≈ +0.8, right sign), but out of sample the
openness-leakage term does not beat a production-blind baseline or a placebo — the openness↔gap correlation
is a shared trend, not independent predictive information.
"""

from __future__ import annotations

import pytest

from polyphony.data.loaders import has_real_trade, load_real_trade
from polyphony.experiments.real_trade_tournament import run_real_trade_tournament

pytestmark = pytest.mark.skipif(
    not has_real_trade(),
    reason="real trade dataset not fetched; run `python -m polyphony.data.fetch_real`",
)


def test_real_trade_dataset_loads_and_is_not_synthetic():
    ds = load_real_trade()
    assert not ds.synthetic
    assert len(ds) >= 20
    assert {"production_co2", "consumption_co2", "openness"} <= set(ds.series)


def test_real_leakage_is_cut_confounded_away():
    r = run_real_trade_tournament()
    # The gap really grew with openness (right sign, strong correlation)…
    assert r.openness_ratio_corr > 0.5
    assert r.sign_as_assumed
    # …but the openness-leakage mechanism beats neither a production-blind baseline nor a placebo out of
    # sample (a shared trend, not independent information) ⇒ cut.
    assert r.wf_beats_blind <= 0.5
    assert r.wf_beats_placebo <= 0.5
    assert r.robust_verdict() == "cut"
