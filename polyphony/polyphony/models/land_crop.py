"""Reduced-form land/crop voice — the food side of the Land⇄Climate⇄Food loop (issue #6).

A minimal partial-equilibrium reduction of a spatial land model
([GLOBIOM](../model-families/agriculture/globiom.md)) + a crop-yield response
([DSSAT](../model-families/agriculture/dssat.md)): warming lowers crop yield, which raises food
price. Consumes ``temperature`` (from the climate voice), emits ``food_price`` — closing
climate ⇄ food. Toy scaffold (NOT the full models); it tests whether coupling climate into the land
sector predicts food price better than a climate-blind baseline.
"""

from __future__ import annotations

from typing import Any, Mapping

from ..core.dials import Dial, DialsSpec
from ..core.interface import StepResult
from ..core.provenance import Provenance


class ReducedFormLand:
    name: str = "land"
    version: str = "0.1-reduced"
    paradigm: str = "optimization"  # partial-equilibrium land use (reduced)
    engines: tuple[str, ...] = ("land", "integration")
    provides: tuple[str, ...] = ("food_price",)
    requires: tuple[str, ...] = ("temperature",)

    BASE_PRICE = 100.0
    MIN_YIELD = 0.2

    def __init__(self) -> None:
        self._seed = 0

    def dials_spec(self) -> DialsSpec:
        return DialsSpec(
            (
                Dial("yield_sensitivity", 0.1, low=0.0, high=1.0,
                     description="fractional crop-yield loss per °C of warming",
                     provenance="model-families/agriculture/dssat.md"),
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
        temperature = float(inputs.get("temperature", 0.0))
        yld = max(1.0 - float(dials["yield_sensitivity"]) * temperature, self.MIN_YIELD)
        food_price = self.BASE_PRICE / yld
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
