"""Golden end-to-end integration test for the energy ⇄ economy vertical slice.

Demonstrates the whole Phase-2 machinery: a coupled recursive run under one clock, paradigm
**routing** for the coupled dynamics, **run-both** for the two economics voices, a
first-class **disagreement** that grows with policy and is **attributed to the closure dial**,
and mandatory **provenance**. This is the coupled-scenario acceptance gate for Phase 2.
"""

from polyphony.core.combiner import attribute_to_dial, combine
from polyphony.core.orchestrator import Orchestrator
from polyphony.models import DisequilibriumEconomy, EquilibriumEconomy, ReducedFormEnergy


def _build() -> Orchestrator:
    voices = [ReducedFormEnergy(), EquilibriumEconomy(), DisequilibriumEconomy()]
    # route coupled dynamics: energy drives cost/emissions, CGE drives demand (E3ME is a
    # shadow voice kept for gdp disagreement). gdp routing is bus bookkeeping only.
    routing = {"energy_cost": "energy", "emissions": "energy", "demand": "cge", "gdp": "cge"}
    return Orchestrator(voices, routing)


def _run(carbon_price: float, steps: int = 25):
    return _build().run(steps=steps, dials={"carbon_price": carbon_price}, seed=1)


def test_coupled_run_produces_trajectory_and_provenance():
    r = _run(50.0)
    assert len(r.history) == 25
    last = r.history[-1]
    assert {"energy_cost", "emissions", "demand", "gdp"} <= set(last)
    # every voice logs provenance every step, with a non-empty inputs hash
    assert len(r.provenance[-1]) == 3
    assert all(p.inputs_hash for p in r.provenance[-1])


def test_disagreement_grows_with_policy():
    d0 = combine("gdp", _run(0.0).answers_for("gdp"))
    d1 = combine("gdp", _run(50.0).answers_for("gdp"))
    assert d1.index_D > d0.index_D
    assert d1.spread > d0.spread
    # opposite signs around the baseline: CGE cost, E3ME dividend
    vals = {a.voice: a.value for a in d1.answers}
    assert vals["cge"] < 100.0 < vals["e3me"]


def test_disagreement_attributed_to_closure_dial():
    answers = _run(50.0).answers_for("gdp")
    attr = attribute_to_dial(
        "gdp", answers, {"cge": "equilibrium", "e3me": "disequilibrium"}
    )
    assert attr["explained_fraction"] > 0.9


def test_carbon_price_reduces_emissions():
    e0 = _run(0.0).history[-1]["emissions"]
    e1 = _run(50.0).history[-1]["emissions"]
    assert e1 < e0


def test_routing_and_unique_names_are_validated():
    import pytest

    # duplicate voice names rejected
    with pytest.raises(ValueError):
        Orchestrator([ReducedFormEnergy(), ReducedFormEnergy()], routing={})
    # routing to a non-provided quantity rejected
    with pytest.raises(ValueError):
        Orchestrator([ReducedFormEnergy()], routing={"gdp": "energy"})
