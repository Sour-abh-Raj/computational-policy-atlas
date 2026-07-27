"""Welfare frontier over policies — the altruism payoff, made concrete.

Maps coupled-ensemble outcomes across candidate carbon prices into welfare
:class:`~polyphony.engines.welfare.PolicyOutcome`s (a stylized 3-group consumption distribution, plus
emissions and climate risk), computes the **Pareto frontier**, and shows how the **recommended
policy changes with the value dials** (utilitarian vs prioritarian vs Rawlsian + tail-risk aversion).

Numbers are **illustrative** (reduced-form outcomes + a stylized incidence assumption); the point is
that the *choice of values visibly changes the recommendation* — exactly what a welfare number that
hides its weights would conceal.
"""

from __future__ import annotations

import numpy as np

from ..core.combiner import combine
from ..core.interface import Model
from ..core.orchestrator import Orchestrator
from ..engines.welfare import PolicyOutcome, WelfareDials, pareto_frontier, rank_policies
from ..models import (
    DisequilibriumEconomy,
    EquilibriumEconomy,
    ReducedFormClimate,
    ReducedFormEnergy,
)

# Stylized fixed inequality across 3 income groups (illustrative), normalized to mean 1.
_BASE_SHARES = np.array([0.6, 1.0, 1.4])
# Climate risk expressed as a welfare-equivalent damage scale so it trades against consumption.
_RISK_TO_CONSUMPTION = 8.0
# Near-term abatement cost of carbon pricing (a stylized quadratic MAC, à la DICE/IAMs): higher
# carbon price buys lower climate risk at a rising consumption cost — the genuine efficiency↔safety
# trade-off that makes the value dials matter.
_ABATE_K = 0.06


def _abatement_cost_frac(cp: float) -> float:
    return float(min(_ABATE_K * (cp / 100.0) ** 2, 0.5))


def slice_outcome(cp: float, n: int = 30, tcre: float = 0.001, paradigm: str = "both") -> PolicyOutcome:
    """Welfare outcome of a carbon price. ``paradigm`` selects the economy voice(s): ``"both"`` (report the
    disagreement-averaged GDP), ``"equilibrium"`` (CGE only), or ``"disequilibrium"`` (E3ME only) — so the
    recommendation can be computed *within* each worldview and compared."""
    econ_by_paradigm: dict[str, list[Model]] = {
        "both": [EquilibriumEconomy(), DisequilibriumEconomy()],
        "equilibrium": [EquilibriumEconomy()],
        "disequilibrium": [DisequilibriumEconomy()],
    }
    econ: list[Model] = econ_by_paradigm[paradigm]
    driver = econ[0].name  # the voice that drives gdp/demand on the bus
    voices: list[Model] = [ReducedFormEnergy(), ReducedFormClimate(), *econ]
    routing = {
        "energy_cost": "energy",
        "emissions": "energy",
        "temperature": "dice",
        "damage_frac": "dice",
        "demand": driver,
        "gdp": driver,
    }
    r = Orchestrator(voices, routing).run(steps=n, dials={"carbon_price": cp, "tcre": tcre}, seed=1)
    mean_gdp = combine("gdp", r.answers_for("gdp")).weighted_mean
    emissions = float(r.history[-1]["emissions"])
    temperature = float(r.history[-1]["temperature"])
    # Near-term abatement cost reduces consumption as the carbon price rises (efficiency side).
    mean_consumption = mean_gdp * (1.0 - _abatement_cost_frac(cp))
    # Mild progressive recycling: higher carbon price slightly compresses the distribution (equity).
    compression = 1.0 - min(cp / 1000.0, 0.3)
    shares = 1.0 + (_BASE_SHARES - 1.0) * compression
    consumption = mean_consumption * shares / shares.mean()
    # Welfare-equivalent climate risk (so tail-risk aversion can trade it against consumption).
    climate_risk = temperature * _RISK_TO_CONSUMPTION
    return PolicyOutcome(f"cp={cp:g}", consumption, emissions, climate_risk)


def policy_outcomes(carbon_prices, n: int = 30, paradigm: str = "both") -> list[PolicyOutcome]:
    return [slice_outcome(cp, n, paradigm=paradigm) for cp in carbon_prices]


def recommendations(outcomes) -> dict[str, str]:
    """Recommended policy (by name) under three value settings — they need not agree."""
    settings = {
        "utilitarian": WelfareDials(swf="utilitarian", tail_risk_aversion=0.0),
        "prioritarian": WelfareDials(swf="prioritarian", inequality_aversion=1.0),
        "rawlsian_tail_averse": WelfareDials(swf="rawlsian", tail_risk_aversion=2.0),
    }
    return {label: rank_policies(outcomes, d)[0].name for label, d in settings.items()}


def frontier_and_recommendations(carbon_prices, n: int = 30, paradigm: str = "both"):
    outcomes = policy_outcomes(carbon_prices, n=n, paradigm=paradigm)
    front = [o.name for o in pareto_frontier(outcomes)]
    return {"outcomes": outcomes, "pareto_front": front, "recommendations": recommendations(outcomes)}
