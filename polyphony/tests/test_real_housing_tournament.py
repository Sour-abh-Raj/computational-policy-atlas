"""Real Interest-Rate⇄Housing tests (issue #14) — a CUT via reverse causation + momentum.

The identification trap: rates and house-price growth co-move contemporaneously with the *wrong* (positive)
sign because the Fed hikes into booms (reverse causation). The correctly-signed lagged rate has the right
sign but cannot beat a persistence (momentum) baseline — housing growth is highly autocorrelated. Failing
to beat the honest baseline is decisive ⇒ cut.
"""

from __future__ import annotations

import pytest

from polyphony.data.loaders import has_real_housing, load_real_housing
from polyphony.experiments.real_housing_tournament import run_real_housing_tournament

pytestmark = pytest.mark.skipif(not has_real_housing(), reason="real housing dataset not fetched")


def test_real_housing_dataset_loads_and_is_not_synthetic():
    ds = load_real_housing()
    assert not ds.synthetic
    assert len(ds) >= 20
    assert "rate" in ds.series and "hpi" in ds.series


def test_reverse_causation_and_momentum_cut_the_coupling():
    r = run_real_housing_tournament()
    # (1) Reverse causation: the contemporaneous correlation is positive — the Fed hikes into booms.
    assert r.contemp_corr > 0.2
    assert r.reverse_causation
    # (2) The correctly-signed lagged rate has the right sign…
    assert r.lead_corr < 0.0
    assert r.lead_sign_as_assumed
    # …but cannot beat a persistence (momentum) baseline ⇒ cut.
    assert r.wf_beats_persistence <= 0.5
    assert r.robust_verdict() == "cut"
