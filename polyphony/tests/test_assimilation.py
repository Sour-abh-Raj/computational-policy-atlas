from polyphony.data.loaders import synthetic_pandemic_series
from polyphony.data.splits import time_blocked_split
from polyphony.engines.assimilation import estimate_r0
from polyphony.experiments.redteam_macrohealth import run_red_team


def test_estimate_r0_recovers_the_true_reproduction_number():
    for true_r0 in (2.0, 3.0, 4.5):
        y = synthetic_pandemic_series(n=40, seed=0, r0=true_r0).column("gdp")
        r0_hat = estimate_r0(y, time_blocked_split(40).train)
        assert abs(r0_hat - true_r0) < 0.5


def test_assimilation_repairs_the_r0_shift_break():
    # Without assimilation the champion breaks under an r0 shift…
    assert not run_red_team(n=40, seed=0, assimilate=False).survived
    # …but assimilating r0 from early data lets it survive the full red-team round.
    assert run_red_team(n=40, seed=0, assimilate=True).survived
