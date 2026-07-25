"""Welfare/Equity engine — contested values as an inspectable multi-objective dial.

Polyphony's north star is *altruistic* policy choice, so the welfare objective must never be a
buried constant. This engine separates two things cleanly:

* **value-neutral objective axes** — efficiency (mean consumption), equity (−Gini), climate safety
  (−risk) — over which a **Pareto frontier** of policies is computed (atlas
  [Multi-Objective](../paradigms/algorithms/multiobjective.md)); and
* a **value-laden aggregator** — a social welfare function whose parameters are **dials**: the SWF
  form (utilitarian ↔ prioritarian ↔ Rawlsian), inequality aversion η, discount rate, and tail-risk
  aversion — used to *pick a point* on the frontier, plus **value of information** (atlas
  [Bayesian Decision](../paradigms/algorithms/bayesian-decision.md)).

Grounding: Atkinson (1970) inequality/EDE; Fleurbaey (2010) and Adler (2019) on social welfare
functions and prioritarianism. The numbers here are **illustrative** (reduced-form outcomes), but
the *machinery* — values as dials, trade-offs on a frontier, EVPI — is the point.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping, Sequence

import numpy as np
from numpy.typing import ArrayLike


@dataclass(frozen=True)
class WelfareDials:
    swf: str = "prioritarian"  # "utilitarian" | "prioritarian" | "rawlsian"
    inequality_aversion: float = 1.0  # η (Atkinson); used by the prioritarian SWF
    discount_rate: float = 0.02  # per-period, for intertemporal consumption paths
    tail_risk_aversion: float = 0.0  # 0 = risk-neutral; >0 up-weights climate risk

    def eta(self) -> float:
        if self.swf == "utilitarian":
            return 0.0
        if self.swf == "rawlsian":
            return float("inf")
        if self.swf == "prioritarian":
            return max(self.inequality_aversion, 0.0)
        raise ValueError(f"unknown swf {self.swf!r}")


def ede(consumption: ArrayLike, eta: float) -> float:
    """Equally-distributed-equivalent consumption (Atkinson 1970).

    η=0 → mean (utilitarian); η=1 → geometric mean; η→∞ → min (Rawlsian). Higher η ⇒ more weight
    on the worse-off.
    """
    c = np.asarray(consumption, float)
    if np.any(c <= 0):
        raise ValueError("consumption must be strictly positive")
    if np.isinf(eta):
        return float(c.min())
    if abs(eta - 1.0) < 1e-9:
        return float(np.exp(np.mean(np.log(c))))
    if eta == 0.0:
        return float(c.mean())
    return float(np.mean(c ** (1.0 - eta)) ** (1.0 / (1.0 - eta)))


def gini(consumption: ArrayLike) -> float:
    c = np.sort(np.asarray(consumption, float))
    n = c.size
    total = c.sum()
    if total == 0:
        return 0.0
    idx = np.arange(1, n + 1)
    return float((2.0 * np.sum(idx * c)) / (n * total) - (n + 1.0) / n)


def atkinson_index(consumption: ArrayLike, eta: float) -> float:
    c = np.asarray(consumption, float)
    return float(1.0 - ede(c, eta) / c.mean())


@dataclass(frozen=True)
class PolicyOutcome:
    name: str
    consumption_by_group: np.ndarray  # per-capita consumption per group
    emissions: float
    climate_risk: float  # e.g. temperature anomaly or welfare-equivalent damage


def objective_vector(outcome: PolicyOutcome) -> dict[str, float]:
    """Value-neutral axes, all 'higher is better' (for the Pareto frontier)."""
    c = outcome.consumption_by_group
    return {
        "efficiency": float(np.mean(c)),
        "equity": -gini(c),
        "climate_safety": -float(outcome.climate_risk),
    }


def _dominates(a: Mapping[str, float], b: Mapping[str, float]) -> bool:
    ge = all(a[k] >= b[k] for k in a)
    gt = any(a[k] > b[k] for k in a)
    return ge and gt


def pareto_frontier(outcomes: Sequence[PolicyOutcome]) -> list[PolicyOutcome]:
    """Non-dominated policies over the value-neutral objective axes."""
    objs = {o.name: objective_vector(o) for o in outcomes}
    front = []
    for o in outcomes:
        if not any(_dominates(objs[p.name], objs[o.name]) for p in outcomes if p.name != o.name):
            front.append(o)
    return front


def social_welfare_score(outcome: PolicyOutcome, dials: WelfareDials) -> float:
    """Value-laden aggregator used to *pick* from the frontier given a values setting."""
    welfare = ede(outcome.consumption_by_group, dials.eta())
    risk_penalty = outcome.climate_risk * (1.0 + dials.tail_risk_aversion)
    return float(welfare - risk_penalty)


def rank_policies(outcomes: Sequence[PolicyOutcome], dials: WelfareDials) -> list[PolicyOutcome]:
    return sorted(outcomes, key=lambda o: social_welfare_score(o, dials), reverse=True)


def value_of_information(
    outcomes_by_scenario: Mapping[str, Mapping[str, PolicyOutcome]],
    probs: Mapping[str, float],
    dials: WelfareDials,
) -> float:
    """Expected Value of Perfect Information: welfare gain from resolving uncertainty first.

    EVPI = E_s[ max_p W(p,s) ] − max_p E_s[ W(p,s) ] ≥ 0.
    """
    scenarios = list(outcomes_by_scenario)
    policies = list(next(iter(outcomes_by_scenario.values())))
    exp_w = {
        p: sum(probs[s] * social_welfare_score(outcomes_by_scenario[s][p], dials) for s in scenarios)
        for p in policies
    }
    best_under_uncertainty = max(exp_w.values())
    with_perfect_info = sum(
        probs[s] * max(social_welfare_score(outcomes_by_scenario[s][p], dials) for p in policies)
        for s in scenarios
    )
    return float(with_perfect_info - best_under_uncertainty)
