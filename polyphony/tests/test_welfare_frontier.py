from polyphony.experiments.welfare_frontier import frontier_and_recommendations


def test_frontier_nonempty_and_values_change_the_recommendation():
    res = frontier_and_recommendations([0.0, 50.0, 100.0, 150.0, 200.0], n=30)
    assert len(res["pareto_front"]) >= 1
    recs = res["recommendations"]
    assert set(recs) == {"utilitarian", "prioritarian", "rawlsian_tail_averse"}
    # the altruism payoff: different value stances recommend different policies
    assert len(set(recs.values())) >= 2


def test_higher_climate_aversion_never_recommends_the_dirtiest_policy():
    res = frontier_and_recommendations([0.0, 50.0, 100.0, 150.0], n=30)
    # cp=0 is the highest-risk policy; a tail-risk-averse Rawlsian must not pick it
    assert res["recommendations"]["rawlsian_tail_averse"] != "cp=0"
