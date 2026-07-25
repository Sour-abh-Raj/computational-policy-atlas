import numpy as np

from polyphony.engines.welfare import (
    PolicyOutcome,
    WelfareDials,
    atkinson_index,
    ede,
    gini,
    pareto_frontier,
    rank_policies,
    social_welfare_score,
    value_of_information,
)


def test_ede_endpoints():
    c = [50.0, 100.0, 150.0]
    assert abs(ede(c, 0.0) - 100.0) < 1e-9  # utilitarian = mean
    assert ede(c, float("inf")) == 50.0  # Rawlsian = min
    # prioritarian (η>0) sits strictly between min and mean
    assert 50.0 < ede(c, 1.0) < 100.0


def test_gini_and_atkinson_flag_inequality():
    assert abs(gini([10, 10, 10, 10])) < 1e-12
    assert gini([1, 1, 1, 97]) > gini([20, 25, 25, 30])
    assert atkinson_index([10, 10, 10], 1.0) < 1e-9  # no inequality → 0


def _outcome(name, cons, emissions, risk):
    return PolicyOutcome(name, np.array(cons, float), emissions, risk)


def test_values_change_the_ranking():
    # A: higher mean but unequal; B: lower mean but equal
    a = _outcome("A", [40, 40, 220], emissions=80, risk=2.0)  # mean 100, very unequal
    b = _outcome("B", [90, 90, 90], emissions=80, risk=2.0)  # mean 90, equal
    util = WelfareDials(swf="utilitarian")
    rawls = WelfareDials(swf="rawlsian")
    assert rank_policies([a, b], util)[0].name == "A"  # utilitarian prefers the bigger pie
    assert rank_policies([a, b], rawls)[0].name == "B"  # Rawlsian prefers the equal one


def test_pareto_frontier_drops_dominated():
    good = _outcome("good", [100, 100, 100], emissions=10, risk=0.5)
    dominated = _outcome("dominated", [90, 90, 90], emissions=20, risk=1.0)
    other = _outcome("tradeoff", [130, 130, 130], emissions=50, risk=2.0)  # richer but riskier
    front = {o.name for o in pareto_frontier([good, dominated, other])}
    assert "dominated" not in front
    assert "good" in front and "tradeoff" in front  # a genuine trade-off, both non-dominated


def test_tail_risk_aversion_widens_the_safety_margin():
    safe = _outcome("safe", [100, 100, 100], emissions=10, risk=0.2)
    risky = _outcome("risky", [101, 101, 101], emissions=90, risk=3.0)
    neutral = WelfareDials(swf="utilitarian", tail_risk_aversion=0.0)
    averse = WelfareDials(swf="utilitarian", tail_risk_aversion=5.0)
    # even risk-neutral penalizes expected damage, so safe already wins…
    margin_neutral = social_welfare_score(safe, neutral) - social_welfare_score(risky, neutral)
    margin_averse = social_welfare_score(safe, averse) - social_welfare_score(risky, averse)
    assert margin_neutral > 0.0
    assert margin_averse > margin_neutral  # …and aversion widens the preference for safety


def test_value_of_information_nonnegative_and_positive_when_it_matters():
    dials = WelfareDials(swf="utilitarian")
    # two scenarios where different policies are best → resolving uncertainty has value
    by_scenario = {
        "wet": {"P1": _outcome("P1", [120, 120, 120], 50, 1.0), "P2": _outcome("P2", [90, 90, 90], 10, 0.5)},
        "dry": {"P1": _outcome("P1", [80, 80, 80], 50, 3.0), "P2": _outcome("P2", [100, 100, 100], 10, 0.5)},
    }
    evpi = value_of_information(by_scenario, {"wet": 0.5, "dry": 0.5}, dials)
    assert evpi >= 0.0
    assert evpi > 0.0
