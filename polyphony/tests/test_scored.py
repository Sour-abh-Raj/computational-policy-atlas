from polyphony.data.loaders import synthetic_policy_series
from polyphony.experiments.scored import scored_backtest


def test_scored_backtest_reports_crps_pit_and_synergy():
    r = scored_backtest(synthetic_policy_series(n=40, seed=0, carbon_price=50.0), members=48, seed=0)
    assert r.coupled_crps > 0.0
    assert 0.0 <= r.pit_mean <= 1.0
    # coupled ensemble beats economy-only on the proper (CRPS) score too, not just point MASE
    assert r.synergy_crps.positive
    assert r.coupled_crps < r.econ_crps


def test_calibration_reduces_error_and_can_beat_naive_on_synthetic():
    r = scored_backtest(synthetic_policy_series(n=40, seed=0, carbon_price=50.0), members=48, seed=0)
    # affine level fit (train-block only) reduces held-out error vs the raw coupled mean…
    assert r.calibrated_mase < r.coupled_mean_mase
    # …and on this synthetic target it drops below 1 (beats naive) — an honest, synthetic-only result
    assert r.beats_naive_after_calibration
