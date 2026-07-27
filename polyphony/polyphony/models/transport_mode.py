"""Reduced-form transport voice — the mobility side of the Urban⇄Transport⇄Energy⇄Health loop (#7).

A minimal reduction of an activity-/agent-based travel model
([MATSim](../model-families/transport/matsim.md), [ActivitySim](../model-families/transport/activitysim.md)):
a carbon/fuel price raises the generalized cost of car travel, so vehicle-kilometres (``vkt``) fall via a
constant-elasticity mode-shift, and tailpipe emissions fall with them. Ambient fine-particulate pollution
``pm25`` is a background level plus a traffic-proportional term. Consumes ``carbon_price`` (a shared policy
dial), emits ``vkt`` and ``pm25`` — the exposure that the air-quality health voice turns into a mortality
burden, closing **transport ⇄ health** (the air-quality co-benefits channel; Haines et al. 2009, Lancet).
Toy scaffold (NOT the full model); it exists to test whether coupling transport policy through to health
predicts the health burden better than a policy-blind baseline.
"""

from __future__ import annotations

import math
from typing import Any, Mapping

from ..core.dials import Dial, DialsSpec
from ..core.interface import StepResult
from ..core.provenance import Provenance


class ReducedFormTransport:
    name: str = "transport"
    version: str = "0.1-reduced"
    paradigm: str = "agent-based"  # activity-/agent-based travel demand (reduced)
    engines: tuple[str, ...] = ("behavior", "spatial")
    provides: tuple[str, ...] = ("vkt", "pm25")
    requires: tuple[str, ...] = ()

    VKT_BASE = 100.0  # baseline vehicle-km (index) before the policy bites
    PM_BACKGROUND = 8.0  # µg/m³ non-traffic background PM2.5
    PM_PER_VKT = 0.20  # µg/m³ per unit vkt (traffic contribution)
    PRICE_REF = 100.0  # $/t reference for the price ratio
    ADJUST = 0.15  # per-step behavioural-adjustment rate toward the price-implied target (inertia)

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
                    description="$/t carbon price; raises the generalized cost of car travel",
                    provenance="patterns/policy-engine.md",
                ),
                Dial(
                    "vkt_elasticity",
                    0.4,
                    low=0.0,
                    high=2.0,
                    description="semi-elasticity of vehicle-km to the carbon-price ratio (mode shift)",
                    provenance="model-families/transport/activitysim.md",
                ),
            )
        )

    def init_state(self, dials: Mapping[str, Any], seed: int) -> dict[str, float]:
        self._seed = seed
        return {"vkt": self.VKT_BASE, "pm25": self.PM_BACKGROUND + self.PM_PER_VKT * self.VKT_BASE}

    def step(
        self,
        state: Mapping[str, float],
        inputs: Mapping[str, float],
        dt: float,
        dials: Mapping[str, Any],
    ) -> StepResult:
        cp = float(dials["carbon_price"])
        elas = float(dials["vkt_elasticity"])
        target = self.VKT_BASE * math.exp(-elas * cp / self.PRICE_REF)
        vkt_prev = float(state.get("vkt", self.VKT_BASE))
        vkt = vkt_prev + self.ADJUST * (target - vkt_prev)  # gradual mode shift / fleet turnover (inertia)
        pm25 = self.PM_BACKGROUND + self.PM_PER_VKT * vkt
        prov = Provenance.make(
            model=self.name, version=self.version, paradigm=self.paradigm, solver="closed-form-elasticity",
            seed=self._seed, dials=dials, inputs=inputs,
        )
        return StepResult(
            state={"vkt": vkt, "pm25": pm25},
            outputs={"vkt": vkt, "pm25": pm25},
            provenance=prov,
            diagnostics={"vkt": vkt, "pm25": pm25},
        )

    def observe(self, state: Mapping[str, float], keys: tuple[str, ...]) -> dict[str, float]:
        return {k: float(state.get(k, 0.0)) for k in keys}
