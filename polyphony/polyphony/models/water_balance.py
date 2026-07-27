"""Reduced-form water voice — the water pillar of the Water⇄Energy⇄Food nexus (issue #10).

A minimal reservoir/storage reduction of a water-allocation model
([WEAP](../model-families/water/weap.md)) / integrated nexus framework
([CLEWs](../model-families/water/clews.md)): a ``precipitation`` dial drives inflow into a buffer store
against a constant demand; when inflow < demand the store draws down and **water stress** rises (and
saturates when the store empties). Storage is what makes a *sustained* precipitation deficit produce a
*time-varying* stress path — the drought signal a downstream food/energy voice can track. Consumes
nothing, emits ``water_stress`` ∈ [0, 1] — the scarcity that irrigation-dependent food production and
hydropower both feel (the nexus; Hoff 2011, Bonn Nexus Conference). Toy scaffold (NOT the full model).
"""

from __future__ import annotations

from typing import Any, Mapping

from ..core.dials import Dial, DialsSpec
from ..core.interface import StepResult
from ..core.provenance import Provenance


class ReducedFormWater:
    name: str = "water"
    version: str = "0.1-reduced"
    paradigm: str = "optimization"  # water allocation / reservoir operation (reduced)
    engines: tuple[str, ...] = ("integration", "spatial")
    provides: tuple[str, ...] = ("water_stress", "storage")
    requires: tuple[str, ...] = ()

    STORE_MAX = 2.0  # buffer capacity (years of demand)
    DEMAND = 1.0  # constant abstraction demand

    def __init__(self) -> None:
        self._seed = 0

    def dials_spec(self) -> DialsSpec:
        return DialsSpec(
            (
                Dial(
                    "precipitation",
                    1.0,
                    low=0.0,
                    high=2.0,
                    description="inflow relative to normal (1.0 = normal; <1 = drought)",
                    provenance="model-families/water/weap.md",
                ),
            )
        )

    def init_state(self, dials: Mapping[str, Any], seed: int) -> dict[str, float]:
        self._seed = seed
        return {"storage": self.STORE_MAX, "water_stress": 0.0}

    def step(
        self,
        state: Mapping[str, float],
        inputs: Mapping[str, float],
        dt: float,
        dials: Mapping[str, Any],
    ) -> StepResult:
        precip = float(dials["precipitation"])
        store_prev = float(state.get("storage", self.STORE_MAX))
        storage = min(max(store_prev + precip - self.DEMAND, 0.0), self.STORE_MAX)
        water_stress = min(max(1.0 - storage / self.STORE_MAX, 0.0), 1.0)  # empty store ⇒ full stress
        prov = Provenance.make(
            model=self.name, version=self.version, paradigm=self.paradigm, solver="closed-form-reservoir",
            seed=self._seed, dials=dials, inputs=inputs,
        )
        return StepResult(
            state={"storage": storage, "water_stress": water_stress},
            outputs={"water_stress": water_stress, "storage": storage},
            provenance=prov,
            diagnostics={"storage": storage, "water_stress": water_stress},
        )

    def observe(self, state: Mapping[str, float], keys: tuple[str, ...]) -> dict[str, float]:
        return {k: float(state.get(k, 0.0)) for k in keys}
