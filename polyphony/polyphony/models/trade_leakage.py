"""Reduced-form trade voice — the trade side of the Trade⇄Emissions loop (carbon leakage, issue #12).

A minimal reduction of a trade/footprint model (a multi-regional input-output database like
[EXIOBASE/Eora](../model-families/trade/mrio.md); or a trade CGE like [GTAP](../model-families/economics/gtap.md)):
when a country prices carbon, some emission-intensive production relocates abroad, so its **consumption-based**
emissions fall less than its **production-based** emissions — the difference is **embodied carbon in
trade** (the pollution-haven / carbon-leakage hypothesis; Copeland-Taylor). Globalisation builds the
leakage channel over time (openness relaxes toward a target). Consumes ``emissions`` (production, from the
energy voice), emits ``consumption_emissions`` and ``leakage_frac`` — closing **trade ⇄ emissions**. Toy
scaffold (NOT the full model); it tests whether coupling trade leakage in predicts consumption-based
emissions better than a leakage-blind baseline (which assumes consumption = production).
"""

from __future__ import annotations

from typing import Any, Mapping

from ..core.dials import Dial, DialsSpec
from ..core.interface import StepResult
from ..core.provenance import Provenance


class ReducedFormTrade:
    name: str = "trade"
    version: str = "0.1-reduced"
    paradigm: str = "equilibrium"  # trade / input-output reallocation (reduced)
    engines: tuple[str, ...] = ("market", "integration")
    provides: tuple[str, ...] = ("consumption_emissions", "leakage_frac")
    requires: tuple[str, ...] = ("emissions",)

    ADJUST = 0.15  # per-step globalisation build-up toward the openness target
    LEAK_INTENSITY = 0.5  # embodied-carbon leakage per unit openness

    def __init__(self) -> None:
        self._seed = 0

    def dials_spec(self) -> DialsSpec:
        return DialsSpec(
            (
                Dial(
                    "openness",
                    0.6,
                    low=0.0,
                    high=1.0,
                    description="trade-openness target (higher ⇒ more scope for carbon leakage)",
                    provenance="model-families/trade/mrio.md",
                ),
            )
        )

    def init_state(self, dials: Mapping[str, Any], seed: int) -> dict[str, float]:
        self._seed = seed
        return {"openness": 0.0, "consumption_emissions": 0.0, "leakage_frac": 0.0}

    def step(
        self,
        state: Mapping[str, float],
        inputs: Mapping[str, float],
        dt: float,
        dials: Mapping[str, Any],
    ) -> StepResult:
        production = float(inputs.get("emissions", 0.0))
        target = float(dials["openness"])
        o_prev = float(state.get("openness", 0.0))
        openness = o_prev + self.ADJUST * (target - o_prev)  # globalisation builds gradually
        leakage_frac = self.LEAK_INTENSITY * openness
        consumption_emissions = production * (1.0 + leakage_frac)  # embodied imports add to the footprint
        prov = Provenance.make(
            model=self.name, version=self.version, paradigm=self.paradigm, solver="closed-form-leakage",
            seed=self._seed, dials=dials, inputs=inputs,
        )
        return StepResult(
            state={
                "openness": openness,
                "consumption_emissions": consumption_emissions,
                "leakage_frac": leakage_frac,
            },
            outputs={"consumption_emissions": consumption_emissions, "leakage_frac": leakage_frac},
            provenance=prov,
            diagnostics={"openness": openness, "leakage_frac": leakage_frac},
        )

    def observe(self, state: Mapping[str, float], keys: tuple[str, ...]) -> dict[str, float]:
        return {k: float(state.get(k, 0.0)) for k in keys}
