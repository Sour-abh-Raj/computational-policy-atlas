"""Energy ⇄ economy ⇄ climate closed-loop tests (adds the reduced-form DICE voice)."""

from polyphony.core.combiner import combine
from polyphony.core.orchestrator import Orchestrator
from polyphony.models import (
    DisequilibriumEconomy,
    EquilibriumEconomy,
    ReducedFormClimate,
    ReducedFormEnergy,
)


def _build() -> Orchestrator:
    voices = [
        ReducedFormEnergy(),
        ReducedFormClimate(),
        EquilibriumEconomy(),
        DisequilibriumEconomy(),
    ]
    routing = {
        "energy_cost": "energy",
        "emissions": "energy",
        "temperature": "dice",
        "damage_frac": "dice",
        "demand": "cge",
        "gdp": "cge",
    }
    return Orchestrator(voices, routing)


def _run(carbon_price: float, steps: int = 30):
    return _build().run(steps=steps, dials={"carbon_price": carbon_price, "tcre": 0.001}, seed=1)


def test_climate_loop_warms_and_damages_gdp():
    r = _run(0.0)
    last = r.history[-1]
    assert last["temperature"] > 0.0
    assert last["damage_frac"] > 0.0
    # with damages, CGE GDP is pulled below its no-damage (~102.7) level at low energy cost
    cge_gdp = {a.voice: a.value for a in r.answers_for("gdp")}["cge"]
    assert cge_gdp < 102.7


def test_carbon_price_reduces_warming():
    t_low_price = _run(0.0).history[-1]["temperature"]
    t_high_price = _run(100.0).history[-1]["temperature"]
    assert t_high_price < t_low_price


def test_disagreement_survives_climate_coupling():
    d = combine("gdp", _run(50.0).answers_for("gdp"))
    assert d.index_D > 0.0
    assert not d.consensus
