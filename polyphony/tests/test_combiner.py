from polyphony.core.combiner import VoiceAnswer, attribute_to_dial, combine


def test_consensus_gives_zero_disagreement():
    d = combine("gdp", [VoiceAnswer("a", 100.0), VoiceAnswer("b", 100.0)])
    assert d.index_D == 0.0
    assert d.spread == 0.0
    assert d.consensus


def test_disagreement_is_positive_and_not_averaged_away():
    d = combine("gdp", [VoiceAnswer("cge", 87.0), VoiceAnswer("e3me", 109.0)])
    assert d.spread == 22.0
    assert d.index_D > 0.0
    assert not d.consensus
    # both original answers are preserved (never collapsed)
    assert {a.value for a in d.answers} == {87.0, 109.0}
    assert 97.0 < d.weighted_mean < 99.0


def test_skill_weights_shift_the_mean():
    d = combine("gdp", [VoiceAnswer("a", 0.0, weight=3.0), VoiceAnswer("b", 100.0, weight=1.0)])
    assert abs(d.weighted_mean - 25.0) < 1e-9


def test_attribution_identifies_the_driving_dial():
    answers = [VoiceAnswer("cge", 87.0), VoiceAnswer("e3me", 109.0)]
    attr = attribute_to_dial(
        "gdp", answers, {"cge": "equilibrium", "e3me": "disequilibrium"}
    )
    # split perfectly explained by the closure dial (each group a singleton)
    assert attr["explained_fraction"] == 1.0
    assert attr["overall_D"] > 0.0
