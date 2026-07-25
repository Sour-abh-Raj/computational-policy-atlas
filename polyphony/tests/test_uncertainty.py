import numpy as np

from polyphony.data.loaders import synthetic_policy_series
from polyphony.experiments.uncertainty import ensemble_crps, ensemble_gdp_tracks


def test_ensemble_has_shape_and_nondegenerate_spread():
    s = ensemble_gdp_tracks(cp=50.0, steps=30, members=40, seed=0)
    assert s.shape == (30, 40)
    assert float(s[-1].std()) > 0.0  # parametric uncertainty produced a real ensemble


def test_crps_finite_and_calibrated_input_beats_biased():
    y = synthetic_policy_series(n=30, seed=0, carbon_price=50.0).column("gdp")
    centered = ensemble_crps(y, cp=50.0, members=40, seed=1)
    biased = ensemble_crps(y, cp=400.0, members=40, seed=1)
    assert np.isfinite(centered)
    assert centered < biased
