from polyphony.tournament.leaderboard import Leaderboard, LeaderboardRow
from polyphony.tournament.race import Contender, race
from polyphony.tournament.synergy import measure_synergy


def test_positive_synergy_when_coupled_beats_best_part():
    r = measure_synergy(coupled_error=1.0, part_errors={"cge": 2.0, "e3me": 1.5})
    assert r.best_part == "e3me"
    assert r.best_part_error == 1.5
    assert r.delta == 0.5
    assert r.positive
    assert "keep" in r.verdict()


def test_no_synergy_is_a_valid_result():
    r = measure_synergy(coupled_error=1.5, part_errors={"cge": 1.0})
    assert not r.positive
    assert r.delta == -0.5
    assert "cut" in r.verdict()


def test_race_ranks_by_adjusted_score():
    res = race([Contender("a", 1.0), Contender("b", 2.0, penalty=0.5), Contender("c", 2.0)])
    assert res.winner.name == "c"
    assert res.margin() > 0.0


def test_penalty_can_dethrone_a_bloated_candidate():
    res = race([Contender("big", 3.0, penalty=2.0), Contender("lean", 1.5)])
    assert res.winner.name == "lean"


def test_leaderboard_roundtrip(tmp_path):
    lb = Leaderboard(tmp_path / "lb.json")
    lb.add(
        LeaderboardRow(
            question="gdp track 2000-2020",
            champion="coupled",
            beat=["cge", "e3me"],
            metric="mae",
            value=0.5,
            synergy_delta=0.2,
            data="synthetic",
            why="lower held-out MAE",
        )
    )
    rows = lb.rows()
    assert len(rows) == 1
    assert rows[0].champion == "coupled"
    md = lb.to_markdown()
    assert "coupled" in md
    assert "+0.2" in md
