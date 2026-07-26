import pytest

from polyphony.data.loaders import has_real_food, load_real_food
from polyphony.experiments.real_land_tournament import run_real_land_tournament

pytestmark = pytest.mark.skipif(
    not has_real_food(), reason="real food dataset not fetched; run `python -m polyphony.data.fetch_real`"
)


def test_real_food_dataset_loads_and_is_not_synthetic():
    ds = load_real_food()
    assert not ds.synthetic
    assert len(ds) >= 40
    assert "cereal_yield" in ds.series and "temp" in ds.series


def test_real_land_coupling_is_cut_on_real_data():
    r = run_real_land_tournament()
    # The warming term appears to beat the plain trend…
    assert r.synergy_delta > 0.0
    # …but it fails the placebo control (a generic time trend does as well or better)…
    assert not r.beats_placebo
    # …AND it has the wrong sign: real cereal yield rose WITH warming (technology dominates),
    # contradicting the coupling's warming→lower-yield assumption.
    assert r.temp_yield_corr > 0.5
    assert not r.sign_as_assumed
    assert r.verdict() == "cut"
