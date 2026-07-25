"""Red Team tests — including the honest finding that the champion does NOT yet survive."""

from polyphony.tournament.redteam import (
    attack_edge_dials,
    attack_naive_baseline,
    run_red_team,
)


def test_red_team_runs_all_attacks():
    rep = run_red_team(n=40, seed=0)
    assert len(rep.attacks) == 5
    for a in rep.attacks:
        assert isinstance(a.broke, bool)
        assert isinstance(a.evidence, dict)


def test_edge_dials_stay_finite():
    a = attack_edge_dials()
    assert not a.broke
    assert a.evidence["nonfinite_at"] == []


def test_naive_baseline_breaks_the_uncalibrated_champion():
    # Honest finding: the reduced-form champion loses to a naive random-walk forecast (MASE > 1),
    # so its "synergy" vs a weak baseline is not evidence of real skill.
    a = attack_naive_baseline(n=40, seed=0)
    assert a.broke
    assert a.evidence["coupled_mase"] > 1.0


def test_champion_does_not_yet_survive_sustained_attack():
    rep = run_red_team(n=40, seed=0)
    assert not rep.survived
    assert "naive_baseline" in [b.name for b in rep.breaks()]
