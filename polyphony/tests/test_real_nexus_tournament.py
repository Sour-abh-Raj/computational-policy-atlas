"""Real Water⇄Energy⇄Food nexus tournament tests (issue #10-real).

The synthetic coupling was kept (Iter 21); this checks the real-data verdict on the energy→food leg. The
honest outcome is a **CUT with the right sign but no out-of-sample skill**: food and energy prices are
strongly correlated contemporaneously (+0.90), but a train-fit energy pass-through does *worse* than a
plain trend, worse than a placebo, and far worse than naive — the 2022 energy shock did not pass through
to food proportionally, so the reduced-form pass-through is not a usable predictor.
"""

from __future__ import annotations

import pytest

from polyphony.data.loaders import has_real_nexus, load_real_nexus
from polyphony.experiments.real_nexus_tournament import run_real_nexus_tournament

pytestmark = pytest.mark.skipif(
    not has_real_nexus(),
    reason="real nexus dataset not fetched; run `python -m polyphony.data.fetch_real`",
)


def test_real_nexus_dataset_loads_and_is_not_synthetic():
    ds = load_real_nexus()
    assert not ds.synthetic
    assert len(ds) >= 20
    assert "food_price" in ds.series and "energy_price" in ds.series


def test_real_nexus_coupling_is_cut_right_sign_but_no_skill():
    r = run_real_nexus_tournament()
    # Strong contemporaneous correlation with the assumed (positive) sign…
    assert r.energy_food_corr > 0.5
    assert r.sign_as_assumed
    # …yet the energy pass-through earns NO out-of-sample skill: worse than a plain trend, and far worse
    # than naive (food prices are a volatile near-random-walk the reduced form cannot forecast)…
    assert r.synergy_delta <= 0.05
    assert not r.coupled_beats_naive
    # …and it does not even beat a generic placebo ⇒ cut.
    assert not r.beats_placebo
    assert r.verdict() == "cut"
