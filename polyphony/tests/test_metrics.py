import numpy as np

from polyphony.eval.metrics import crps_ensemble, crps_series, mae, mase, pit_values, rmse


def test_point_metrics_zero_on_perfect():
    y = [1.0, 2.0, 3.0]
    assert mae(y, y) == 0.0
    assert rmse(y, y) == 0.0
    assert mase(y, y) == 0.0


def test_crps_point_ensemble_equals_absolute_error():
    s = np.array([3.0, 3.0, 3.0])
    assert abs(crps_ensemble(s, 5.0) - 2.0) < 1e-9


def test_crps_rewards_sharp_correct_spread():
    obs = 0.0
    sharp = np.array([-0.1, 0.0, 0.1])
    wide = np.array([-5.0, 0.0, 5.0])
    assert crps_ensemble(sharp, obs) < crps_ensemble(wide, obs)


def test_crps_series_shape_and_zero():
    s = np.zeros((4, 10))
    y = np.zeros(4)
    assert crps_series(s, y) == 0.0


def test_pit_is_uniform_for_calibrated_ensemble():
    rng = np.random.default_rng(0)
    truth = rng.normal(0, 1, 300)
    samples = rng.normal(0, 1, (300, 60))
    p = pit_values(samples, truth)
    assert 0.3 < float(p.mean()) < 0.7
