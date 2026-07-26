from polyphony.data.loaders import synthetic_food_series
from polyphony.experiments.landfood import calibrated_synergy
from polyphony.experiments.redteam_landfood import run_red_team


def test_land_coupling_survives_a_fair_calibration_unlike_energy():
    # Give the land-only baseline its OWN train-block affine fit (its strongest form):
    result = calibrated_synergy(synthetic_food_series(n=40, seed=0, carbon_price=0.0))
    # the coupling's advantage is NOT a level artifact — Δ stays large and positive ⇒ KEEP.
    assert result.delta > 1.0
    assert result.verdict() == "keep"


def test_land_champion_still_loses_to_naive_an_honest_split():
    report = run_red_team(n=40, seed=0)
    breaks = {a.name for a in report.breaks()}
    # The level-artifact and policy-shift attacks are SURVIVED (the coupling is real)…
    assert "level_artifact" not in breaks
    assert "policy_shift" not in breaks
    # …but the calibrated champion still loses to naive ⇒ real coupling, no absolute skill claim yet.
    assert "naive_baseline_calibrated" in breaks
    assert not report.survived
