import pytest

from polyphony.data.loaders import has_real_gdp_co2, load_real_gdp_co2
from polyphony.experiments.real_tournament import run_real_tournament

pytestmark = pytest.mark.skipif(
    not has_real_gdp_co2(), reason="real dataset not fetched; run `python -m polyphony.data.fetch_real`"
)


def test_real_dataset_loads_and_is_not_synthetic():
    ds = load_real_gdp_co2()
    assert not ds.synthetic
    assert len(ds) >= 40
    assert ds.column("gdp")[0] == pytest.approx(100.0)  # indexed to 100 at first year
    assert (ds.column("cum_co2")[1:] >= ds.column("cum_co2")[:-1]).all()  # cumulative, non-decreasing


def test_real_climate_coupling_fails_the_placebo_control():
    r = run_real_tournament()
    # The CO₂ term appears to beat the plain trend (Δ > 0)…
    assert r.synergy_delta > 0.0
    # …but a generic time-trend placebo does as well or better, so the "synergy" is spurious ⇒ CUT.
    assert not r.beats_placebo
    assert r.verdict() == "cut"
    # And the reduced-form coupled predictor does not beat naive on real GDP either.
    assert not r.naive_beaten_by_coupled
