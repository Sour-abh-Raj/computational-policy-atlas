"""Land⇄Climate⇄Food third synergy loop (issue #6): does coupling climate into land help?

Predicts a **food-price** track two ways — a **climate-coupled** ensemble (energy + climate + land, so
warming raises food price) vs a **climate-blind** land baseline (temperature = 0 ⇒ flat price) — and
measures synergy on a coupled (warming) DGP vs a flat negative control. Third domain, same harness.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from ..core.interface import Model
from ..core.orchestrator import Orchestrator
from ..data.loaders import synthetic_flat_food_series, synthetic_food_series
from ..data.splits import time_blocked_split
from ..eval.metrics import mase
from ..models import ReducedFormClimate, ReducedFormEnergy, ReducedFormLand
from ..tournament.synergy import SynergyResult, measure_synergy


def foodprice_track(cp: float, steps: int, coupled: bool, tcre: float = 0.001) -> np.ndarray:
    if coupled:
        voices: list[Model] = [ReducedFormEnergy(), ReducedFormClimate(), ReducedFormLand()]
        routing = {
            "energy_cost": "energy",
            "emissions": "energy",
            "temperature": "dice",
            "damage_frac": "dice",
            "food_price": "land",
        }
    else:
        voices = [ReducedFormLand()]
        routing = {"food_price": "land"}
    dials = {"carbon_price": cp, "tcre": tcre, "yield_sensitivity": 0.1}
    r = Orchestrator(voices, routing).run(steps=steps, dials=dials, seed=1)
    return np.array([r.history[t]["food_price"] for t in range(steps)], float)


@dataclass(frozen=True)
class LandFoodResult:
    dataset: str
    coupled_error: float
    land_only_error: float
    synergy: SynergyResult


def backtest(dataset, test_frac: float = 0.3) -> LandFoodResult:
    y = dataset.column("food_price")
    n = len(y)
    cp = float(dataset.meta.get("carbon_price", 0.0))
    te = time_blocked_split(n, test_frac).test
    coupled = foodprice_track(cp, n, coupled=True)
    land_only = foodprice_track(cp, n, coupled=False)
    err_c = mase(y[te], coupled[te])
    err_l = mase(y[te], land_only[te])
    return LandFoodResult(dataset.name, err_c, err_l, measure_synergy(err_c, {"land_only": err_l}))


def run_two_regime_tournament(n: int = 40, seed: int = 0) -> dict[str, LandFoodResult]:
    return {
        "warming_regime": backtest(synthetic_food_series(n=n, seed=seed, carbon_price=0.0)),
        "flat_regime": backtest(synthetic_flat_food_series(n=n, seed=seed)),
    }
