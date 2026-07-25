"""Reduced-form energy voice — logit-smoothed least-cost technology choice.

Toy scaffold (NOT the full model): two technologies (fossil, clean) compete on marginal
cost; a carbon price raises the fossil cost; a logit share (the atlas Technology-Adoption
Engine) smooths the switch. Provides a unit ``energy_cost`` and ``emissions`` to the
economy voices; consumes ``demand``. Fidelity is intentionally minimal — it exists to
drive the coupling, not to forecast energy systems.
"""

from __future__ import annotations

import math
from typing import Any, Mapping

from ..core.dials import Dial, DialsSpec
from ..core.interface import StepResult
from ..core.provenance import Provenance


class ReducedFormEnergy:
    name = "energy"
    version = "0.1-reduced"
    paradigm = "optimization"
    engines = ("energy-dispatch", "technology-adoption")
    provides = ("energy_cost", "emissions")
    requires = ("demand",)

    C_FOSSIL_BASE = 20.0
    C_CLEAN = 35.0
    EMIT_FACTOR = 1.0
    BETA = 0.1

    def __init__(self) -> None:
        self._seed = 0

    def dials_spec(self) -> DialsSpec:
        return DialsSpec(
            (
                Dial(
                    "carbon_price",
                    0.0,
                    low=0.0,
                    high=1000.0,
                    description="$/t carbon price added to fossil marginal cost",
                    provenance="patterns/policy-engine.md",
                ),
            )
        )

    def init_state(self, dials: Mapping[str, Any], seed: int) -> dict[str, float]:
        self._seed = seed
        return {"energy_cost": self.C_CLEAN, "emissions": 0.0, "share_fossil": 1.0}

    def _shares(self, carbon_price: float) -> tuple[float, float, float]:
        c_f = self.C_FOSSIL_BASE + carbon_price * self.EMIT_FACTOR
        c_c = self.C_CLEAN
        ef, ec = math.exp(-self.BETA * c_f), math.exp(-self.BETA * c_c)
        return ef / (ef + ec), c_f, c_c

    def step(
        self,
        state: Mapping[str, float],
        inputs: Mapping[str, float],
        dt: float,
        dials: Mapping[str, Any],
    ) -> StepResult:
        demand = inputs.get("demand", 100.0) or 100.0
        s_f, c_f, c_c = self._shares(float(dials["carbon_price"]))
        unit_cost = s_f * c_f + (1.0 - s_f) * c_c
        emissions = s_f * demand * self.EMIT_FACTOR
        prov = Provenance.make(
            model=self.name,
            version=self.version,
            paradigm=self.paradigm,
            solver="closed-form-logit",
            seed=self._seed,
            dials=dials,
            inputs=inputs,
        )
        return StepResult(
            state={"energy_cost": unit_cost, "emissions": emissions, "share_fossil": s_f},
            outputs={"energy_cost": unit_cost, "emissions": emissions},
            provenance=prov,
            diagnostics={"share_fossil": s_f},
        )

    def observe(self, state: Mapping[str, float], keys: tuple[str, ...]) -> dict[str, float]:
        return {k: float(state.get(k, 0.0)) for k in keys}
