"""Reduced-form air-quality health voice — the health side of Urban⇄Transport⇄Energy⇄Health (#7).

A minimal reduction of an air-pollution health-impact model
([BenMAP-CE](../model-families/health/benmap.md), WHO AirQ+): a **concentration–response function** turns
ambient fine particulate ``pm25`` into a relative-risk multiplier and thence an excess-mortality
``health_burden`` (index). The log-linear CRF ``RR = exp(β·(pm25 − pm25_ref))`` is the standard
epidemiological form (Dockery et al. 1993, Harvard Six Cities; Burnett et al. 2018 GEMM). Consumes
``pm25`` (from the transport voice), emits ``health_burden`` — closing **transport ⇄ health**. Toy
scaffold (NOT the full model); it tests whether coupling the transport-driven exposure into health
predicts the mortality burden better than a policy-blind (constant-exposure) baseline.

The mechanism's **sign is not free**: more PM2.5 → more mortality is one of the most robust
dose–response relationships in environmental epidemiology, so a coupled predictor whose exposure moves
the right way should track a real co-benefit — but that is a hypothesis to test on real data, not assume.
"""

from __future__ import annotations

import math
from typing import Any, Mapping

from ..core.dials import Dial, DialsSpec
from ..core.interface import StepResult
from ..core.provenance import Provenance


class ReducedFormAirHealth:
    name: str = "airhealth"
    version: str = "0.1-reduced"
    paradigm: str = "system-dynamics"  # exposure→response accounting (reduced)
    engines: tuple[str, ...] = ("integration", "welfare-equity")
    provides: tuple[str, ...] = ("health_burden",)
    requires: tuple[str, ...] = ("pm25",)

    PM_REF = 5.0  # µg/m³ WHO 2021 annual guideline (counterfactual exposure)
    BASE_BURDEN = 100.0  # index scale for the excess-mortality burden

    def __init__(self) -> None:
        self._seed = 0

    def dials_spec(self) -> DialsSpec:
        return DialsSpec(
            (
                Dial(
                    "crf_beta",
                    0.02,
                    low=0.0,
                    high=0.2,
                    description="log-linear concentration-response slope (per µg/m³ PM2.5)",
                    provenance="model-families/health/benmap.md",
                ),
            )
        )

    def init_state(self, dials: Mapping[str, Any], seed: int) -> dict[str, float]:
        self._seed = seed
        return {"health_burden": 0.0, "pm25": self.PM_REF}

    def step(
        self,
        state: Mapping[str, float],
        inputs: Mapping[str, float],
        dt: float,
        dials: Mapping[str, Any],
    ) -> StepResult:
        pm25 = float(inputs.get("pm25", self.PM_REF))
        beta = float(dials["crf_beta"])
        rr = math.exp(beta * max(pm25 - self.PM_REF, 0.0))  # relative risk vs the guideline
        health_burden = self.BASE_BURDEN * (rr - 1.0)  # excess mortality attributable to PM2.5
        prov = Provenance.make(
            model=self.name, version=self.version, paradigm=self.paradigm, solver="closed-form-crf",
            seed=self._seed, dials=dials, inputs=inputs,
        )
        return StepResult(
            state={"health_burden": health_burden, "pm25": pm25},
            outputs={"health_burden": health_burden},
            provenance=prov,
            diagnostics={"relative_risk": rr, "pm25": pm25},
        )

    def observe(self, state: Mapping[str, float], keys: tuple[str, ...]) -> dict[str, float]:
        return {k: float(state.get(k, 0.0)) for k in keys}
