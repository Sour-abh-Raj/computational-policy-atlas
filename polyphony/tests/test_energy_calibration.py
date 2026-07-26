from polyphony.data.loaders import synthetic_policy_series
from polyphony.experiments.slice_tournament import calibrated_synergy
from polyphony.tournament.redteam import run_red_team


def test_calibration_closes_the_energy_naive_break():
    # Raw, the energy champion loses to naive (MASE > 1)…
    assert not run_red_team(calibrate=False).survived
    # …but after a train-block affine calibration it beats naive and survives the full round.
    assert run_red_team(calibrate=True).survived


def test_a_fair_calibration_erases_the_energy_synergy():
    # Give the economy-only baseline its OWN train-block calibration (its strongest form):
    result = calibrated_synergy(synthetic_policy_series(n=40, seed=0, carbon_price=50.0))
    # the calibrated champion beats naive…
    assert result.coupled_beats_naive
    # …but the coupling's advantage collapses — Δ ≈ 0 ⇒ CUT. The raw Round-1 synergy was a
    # level artifact a fair calibration of the baseline absorbs (contrast Macro⇄Health, which survives).
    assert abs(result.delta) < 0.05
    assert result.verdict() == "cut"
