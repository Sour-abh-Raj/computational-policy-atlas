"""Reduced-form nexus-food voice — the food pillar of the Water⇄Energy⇄Food nexus (issue #10).

A minimal partial-equilibrium reduction linking **water scarcity to food price**: irrigation-dependent
yield falls with water stress, and the energy needed to pump replacement water rises with it, so food
price climbs on both counts (the water→food and energy→food legs of the nexus; Hoff 2011). Consumes
``water_stress`` (from the water voice), emits ``food_price`` — closing **water ⇄ food**. Distinct from
the climate-driven land voice ([land_crop](land_crop.py)): the driver here is **water**, not temperature.
Toy scaffold (NOT the full model); it tests whether coupling water scarcity into food production predicts
food price better than a water-blind baseline.
"""

from __future__ import annotations

from typing import Any, Mapping

from ..core.dials import Dial, DialsSpec
from ..core.interface import StepResult
from ..core.provenance import Provenance


class ReducedFormNexusFood:
    name: str = "nexusfood"
    version: str = "0.1-reduced"
    paradigm: str = "optimization"  # partial-equilibrium food price (reduced)
    engines: tuple[str, ...] = ("land", "integration")
    provides: tuple[str, ...] = ("food_price",)
    requires: tuple[str, ...] = ("water_stress",)

    BASE_PRICE = 100.0
    MIN_YIELD = 0.2
    PUMP_COST = 0.15  # energy-for-water surcharge per unit stress (the energy pillar)

    def __init__(self) -> None:
        self._seed = 0

    def dials_spec(self) -> DialsSpec:
        return DialsSpec(
            (
                Dial(
                    "irrigation_sensitivity",
                    0.6,
                    low=0.0,
                    high=1.0,
                    description="fractional yield loss at full water stress (irrigation dependence)",
                    provenance="model-families/water/weap.md",
                ),
            )
        )

    def init_state(self, dials: Mapping[str, Any], seed: int) -> dict[str, float]:
        self._seed = seed
        return {"food_price": self.BASE_PRICE, "yield": 1.0}

    def step(
        self,
        state: Mapping[str, float],
        inputs: Mapping[str, float],
        dt: float,
        dials: Mapping[str, Any],
    ) -> StepResult:
        stress = float(inputs.get("water_stress", 0.0))
        yld = max(1.0 - float(dials["irrigation_sensitivity"]) * stress, self.MIN_YIELD)
        food_price = self.BASE_PRICE / yld * (1.0 + self.PUMP_COST * stress)  # yield loss + pumping energy
        prov = Provenance.make(
            model=self.name, version=self.version, paradigm=self.paradigm, solver="closed-form",
            seed=self._seed, dials=dials, inputs=inputs,
        )
        return StepResult(
            state={"food_price": food_price, "yield": yld},
            outputs={"food_price": food_price},
            provenance=prov,
            diagnostics={"yield": yld},
        )

    def observe(self, state: Mapping[str, float], keys: tuple[str, ...]) -> dict[str, float]:
        return {k: float(state.get(k, 0.0)) for k in keys}
