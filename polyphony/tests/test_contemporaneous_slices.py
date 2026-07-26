import pytest

from polyphony.core.orchestrator import Orchestrator
from polyphony.data.loaders import synthetic_pandemic_series
from polyphony.data.splits import time_blocked_split
from polyphony.eval.metrics import mase
from polyphony.experiments.macrohealth import gdp_track
from polyphony.models import (
    DisequilibriumEconomy,
    EquilibriumEconomy,
    ReducedFormClimate,
    ReducedFormEnergy,
)


def test_contemporaneous_sharpens_the_macrohealth_champion():
    # The epidemic->economy chain is acyclic, so removing the coupling lag is legitimate and helps a lot.
    n = 40
    te = time_blocked_split(n).test
    y = synthetic_pandemic_series(n=n, seed=0, r0=2.5).column("gdp")
    lagged = mase(y[te], gdp_track(2.5, n, coupled=True, resolve="lagged")[te])
    contemp = mase(y[te], gdp_track(2.5, n, coupled=True, resolve="contemporaneous")[te])
    assert contemp < 0.2  # decisively beats naive
    assert contemp < lagged / 2  # markedly sharper than the lagged champion


def test_energy_slice_is_cyclic_so_contemporaneous_is_refused():
    # The energy slice has a genuine energy<->economy feedback loop; the no-lag mode must refuse it.
    voices = [ReducedFormEnergy(), ReducedFormClimate(), EquilibriumEconomy(), DisequilibriumEconomy()]
    routing = {
        "energy_cost": "energy", "emissions": "energy", "temperature": "dice",
        "damage_frac": "dice", "demand": "cge", "gdp": "cge",
    }
    orch = Orchestrator(voices, routing)
    orch.run(steps=5, dials={"carbon_price": 50.0, "tcre": 0.001}, resolve="lagged")  # lagged is fine
    with pytest.raises(ValueError, match="cycle"):
        orch.run(steps=5, dials={"carbon_price": 50.0, "tcre": 0.001}, resolve="contemporaneous")
