"""Reduced-form epidemic voice (SIR) — the health side of the Macro⇄Health loop (issue #8).

A compartmental **SIR** reduction of an epidemic ABM ([Covasim](../model-families/health/covasim.md)):
susceptible→infected→recovered dynamics driven by a reproduction-number dial ``r0`` and an NPI
(non-pharmaceutical intervention) dial. It emits an ``output_penalty`` — the economic drag from illness
plus lockdown — which the economy voices subtract from GDP, closing **health ⇄ macro**. Toy scaffold
(NOT the full model); it exists to test whether coupling a health shock into the economy earns its keep.
Grounding: Kermack–McKendrick (1927) SIR; Eichenbaum-Rebelo-Trabandt (2021) epidemic-macro coupling.
"""

from __future__ import annotations

from typing import Any, Mapping

from ..core.dials import Dial, DialsSpec
from ..core.interface import StepResult
from ..core.provenance import Provenance


class ReducedFormEpidemic:
    name: str = "epidemic"
    version: str = "0.1-reduced"
    paradigm: str = "system-dynamics"  # compartmental SIR; a reduced form of the Covasim ABM
    engines: tuple[str, ...] = ("integration", "behavior")
    provides: tuple[str, ...] = ("output_penalty", "infected_frac")
    requires: tuple[str, ...] = ()

    GAMMA = 0.2  # recovery rate
    PENALTY_COEF = 2.0  # output drag per unit infected fraction
    NPI_COST = 0.1  # output cost of a full lockdown
    MAX_PENALTY = 0.6

    def __init__(self) -> None:
        self._seed = 0

    def dials_spec(self) -> DialsSpec:
        return DialsSpec(
            (
                Dial("r0", 2.5, low=0.0, high=10.0, description="basic reproduction number",
                     provenance="model-families/health/covasim.md"),
                Dial("npi_strength", 0.0, low=0.0, high=1.0,
                     description="non-pharmaceutical intervention strength (reduces effective beta)",
                     provenance="patterns/policy-engine.md"),
            )
        )

    def init_state(self, dials: Mapping[str, Any], seed: int) -> dict[str, float]:
        self._seed = seed
        return {"S": 0.999, "I": 0.001, "R": 0.0, "output_penalty": 0.0, "infected_frac": 0.001}

    def step(
        self,
        state: Mapping[str, float],
        inputs: Mapping[str, float],
        dt: float,
        dials: Mapping[str, Any],
    ) -> StepResult:
        s, i, r = float(state["S"]), float(state["I"]), float(state["R"])
        npi = float(dials["npi_strength"])
        beta = float(dials["r0"]) * self.GAMMA * (1.0 - npi)
        new_inf = beta * s * i
        s = max(s - new_inf, 0.0)
        i = max(i + new_inf - self.GAMMA * i, 0.0)
        r = r + self.GAMMA * i
        penalty = min(self.PENALTY_COEF * i + self.NPI_COST * npi, self.MAX_PENALTY)
        prov = Provenance.make(
            model=self.name, version=self.version, paradigm=self.paradigm, solver="closed-form-sir",
            seed=self._seed, dials=dials, inputs=inputs,
        )
        return StepResult(
            state={"S": s, "I": i, "R": r, "output_penalty": penalty, "infected_frac": i},
            outputs={"output_penalty": penalty, "infected_frac": i},
            provenance=prov,
            diagnostics={"infected_frac": i},
        )

    def observe(self, state: Mapping[str, float], keys: tuple[str, ...]) -> dict[str, float]:
        return {k: float(state.get(k, 0.0)) for k in keys}
