"""Disequilibrium economy voice (E3ME-style, reduced form).

Toy scaffold (NOT the full model): a demand-led, spare-capacity closure with revenue
recycling / green-investment multiplier, so costlier energy from a carbon price can **raise**
output (the "double dividend"). Provides ``gdp`` and ``demand``; consumes ``energy_cost``.
Deliberately gives the *opposite* sign to :class:`~polyphony.models.econ_cge.EquilibriumEconomy`
— the disagreement is the point, not an error (comparative/equilibrium-vs-disequilibrium.md).
"""

from __future__ import annotations

from typing import Any, Mapping

from ..core.dials import Dial, DialsSpec
from ..core.interface import StepResult
from ..core.provenance import Provenance


class DisequilibriumEconomy:
    name = "e3me"
    version = "0.1-reduced"
    paradigm = "disequilibrium"
    engines = ("market", "technology-adoption", "calibration")
    provides = ("gdp", "demand")
    requires = ("energy_cost",)

    BASE_GDP = 100.0
    BASE_COST = 25.0
    DEMAND_BASE = 100.0
    MULTIPLIER = 0.2

    def __init__(self) -> None:
        self._seed = 0

    def dials_spec(self) -> DialsSpec:
        return DialsSpec(
            (
                Dial(
                    "closure",
                    "disequilibrium",
                    choices=("disequilibrium",),
                    description="market closure — this voice is the demand-led closure",
                    provenance="comparative/equilibrium-vs-disequilibrium.md",
                ),
            )
        )

    def init_state(self, dials: Mapping[str, Any], seed: int) -> dict[str, float]:
        self._seed = seed
        return {"gdp": self.BASE_GDP, "demand": self.DEMAND_BASE}

    def step(
        self,
        state: Mapping[str, float],
        inputs: Mapping[str, float],
        dt: float,
        dials: Mapping[str, Any],
    ) -> StepResult:
        ec = inputs.get("energy_cost", self.BASE_COST) or self.BASE_COST
        gdp = self.BASE_GDP * (1.0 + self.MULTIPLIER * (ec - self.BASE_COST) / self.BASE_COST)
        demand = self.DEMAND_BASE * (gdp / self.BASE_GDP)
        prov = Provenance.make(
            model=self.name,
            version=self.version,
            paradigm=self.paradigm,
            solver="closed-form",
            seed=self._seed,
            dials=dials,
            inputs=inputs,
        )
        return StepResult(
            state={"gdp": gdp, "demand": demand},
            outputs={"gdp": gdp, "demand": demand},
            provenance=prov,
        )

    def observe(self, state: Mapping[str, float], keys: tuple[str, ...]) -> dict[str, float]:
        return {k: float(state.get(k, 0.0)) for k in keys}
