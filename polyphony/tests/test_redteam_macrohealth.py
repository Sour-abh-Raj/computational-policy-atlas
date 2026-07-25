from polyphony.experiments.redteam_macrohealth import attack_naive_baseline, run_red_team


def test_macrohealth_red_team_surfaces_r0_fragility():
    rep = run_red_team(n=40, seed=0)
    assert len(rep.attacks) == 4
    # honest finding: the health coupling is fragile to a mis-specified reproduction number —
    # under an r0 distribution shift it does worse than ignoring health entirely.
    assert not rep.survived
    assert "r0_shift" in [b.name for b in rep.breaks()]


def test_macrohealth_champion_survives_naive_baseline():
    a = attack_naive_baseline(n=40, seed=0)
    assert not a.broke
    assert a.evidence["coupled_mase"] < 1.0
