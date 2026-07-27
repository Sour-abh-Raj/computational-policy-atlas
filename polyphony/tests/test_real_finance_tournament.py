"""Real Macro⇄Finance tournament tests (issue #11-real) — the closest real-data call.

The synthetic coupling was kept (Iter 26); this checks the real-data verdict on the credit-spread → GDP-
growth nowcast. The honest outcome is a **narrow CUT with regime-dependent skill**: the spread has the
right sign (≈ −0.6), beats a placebo and naive in a majority of walk-forward folds (genuine information),
but does **not** robustly beat a mean-growth climatology — it helps near crises and hurts in calm years.
Even this well-motivated (Gilchrist-Zakrajšek) coupling is held to the strict bar.
"""

from __future__ import annotations

import pytest

from polyphony.data.loaders import has_real_finance, load_real_finance
from polyphony.experiments.real_finance_tournament import run_real_finance_tournament

pytestmark = pytest.mark.skipif(
    not has_real_finance(),
    reason="real finance dataset not fetched; run `python -m polyphony.data.fetch_real`",
)


def test_real_finance_dataset_loads_and_is_not_synthetic():
    ds = load_real_finance()
    assert not ds.synthetic
    assert len(ds) >= 20
    assert "gdp" in ds.series and "spread" in ds.series


def test_real_finance_is_a_narrow_cut_with_regime_dependent_skill():
    r = run_real_finance_tournament()
    # Strong, right-signed contemporaneous relationship (credit stress ↔ weaker growth)…
    assert r.contemp_corr < -0.4
    assert r.sign_as_assumed
    # …genuine information: beats a placebo in most folds, and naive in a majority…
    assert r.wf_beats_placebo > 0.5
    assert r.wf_beats_naive >= 0.5
    # …but does NOT robustly beat a mean-growth climatology (regime-dependent skill) ⇒ cut.
    assert r.wf_beats_baseline <= 0.5
    assert r.robust_verdict() == "cut"
    assert r.single_split_verdict() == "cut"
