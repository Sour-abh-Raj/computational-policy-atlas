"""Reduced-form DICE-style climate voice (toy scaffold, NOT the full model).

Closes the energy ⇄ economy ⇄ **climate** loop: consumes ``emissions``, accumulates a carbon
stock, maps cumulative emissions to a temperature anomaly via a **TCRE**-style linear response
(Matthews et al. 2009), and returns a Nordhaus-style quadratic ``damage_frac`` that the economy
voices apply to GDP. Fidelity is intentionally minimal — it exists to make the climate feedback
*present and switchable*, not to project climate. The atlas dossier is
`docs/model-families/climate-iam/dice.md`.
"""

from __future__ import annotations

from typing import Any, Mapping

from ..core.dials import Dial, DialsSpec
from ..core.interface import StepResult
from ..core.provenance import Provenance


class ReducedFormClimate:
    name: str = "dice"
    version: str = "0.1-reduced"
    paradigm: str = "optimization"  # DICE is optimal-control; here its climate core runs forward
    engines: tuple[str, ...] = ("climate", "integration")
    provides: tuple[str, ...] = ("temperature", "damage_frac")
    requires: tuple[str, ...] = ("emissions",)

    DAMAGE_COEFF = 0.005  # damage_frac = coeff * T^2  (~2% of GDP at T=2°C)
    MAX_DAMAGE = 0.9

    def __init__(self) -> None:
        self._seed = 0

    def dials_spec(self) -> DialsSpec:
        return DialsSpec(
            (
                Dial(
                    "tcre",
                    0.001,
                    low=0.0,
                    high=0.01,
                    description="transient climate response to cumulative emissions (°C per unit)",
                    provenance="model-families/climate-iam/dice.md",
                ),
            )
        )

    def init_state(self, dials: Mapping[str, Any], seed: int) -> dict[str, float]:
        self._seed = seed
        return {"carbon_stock": 0.0, "temperature": 0.0, "damage_frac": 0.0}

    def step(
        self,
        state: Mapping[str, float],
        inputs: Mapping[str, float],
        dt: float,
        dials: Mapping[str, Any],
    ) -> StepResult:
        emissions = float(inputs.get("emissions", 0.0))
        stock = float(state.get("carbon_stock", 0.0)) + emissions * dt
        temperature = float(dials["tcre"]) * stock
        damage_frac = min(self.DAMAGE_COEFF * temperature * temperature, self.MAX_DAMAGE)
        prov = Provenance.make(
            model=self.name,
            version=self.version,
            paradigm=self.paradigm,
            solver="closed-form-tcre",
            seed=self._seed,
            dials=dials,
            inputs=inputs,
        )
        return StepResult(
            state={
                "carbon_stock": stock,
                "temperature": temperature,
                "damage_frac": damage_frac,
            },
            outputs={"temperature": temperature, "damage_frac": damage_frac},
            provenance=prov,
        )

    def observe(self, state: Mapping[str, float], keys: tuple[str, ...]) -> dict[str, float]:
        return {k: float(state.get(k, 0.0)) for k in keys}
