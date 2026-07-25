import numpy as np

from polyphony.engines.calibration import calibrate_scale_offset, calibrated_track


def test_recovers_affine_transform():
    track = np.linspace(1, 10, 20)
    target = 2.5 * track - 7.0
    a, b = calibrate_scale_offset(track, target)
    assert abs(a - 2.5) < 1e-6
    assert abs(b + 7.0) < 1e-6


def test_calibration_reduces_bias():
    rng = np.random.default_rng(0)
    track = np.linspace(90, 110, 30)
    target = 0.8 * track + 15.0 + rng.normal(0, 0.5, 30)
    a, b = calibrate_scale_offset(track, target)
    raw_err = float(np.mean((target - track) ** 2))
    cal_err = float(np.mean((target - calibrated_track(track, a, b)) ** 2))
    assert cal_err < raw_err
