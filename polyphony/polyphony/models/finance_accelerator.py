"""Reduced-form finance voice — the financial side of the Macro⇄Finance loop (issue #11).

A minimal reduction of a **financial-accelerator / leverage-cycle** model (Bernanke-Gertler-Gilchrist
1999; Minsky's financial-instability hypothesis; the Gilchrist-Zakrajšek 2012 excess-bond-premium
channel): a credit shock builds through the leverage cycle to a **delayed peak** of financial stress and
then unwinds slowly (deleveraging), a smooth boom-bust wave. Emitted as an ``output_penalty`` (the drag
on output from a credit crunch) that the economy voices subtract from GDP, closing **finance ⇄ macro**.
Toy scaffold (NOT the full model); it tests whether coupling a financial shock into the economy earns its
keep. Structurally mirrors the epidemic voice (a shock ⇒ a wave of drag), with a *financial* accelerator.
"""

from __future__ import annotations

import math
from typing import Any, Mapping

from ..core.dials import Dial, DialsSpec
from ..core.interface import StepResult
from ..core.provenance import Provenance


class ReducedFormFinance:
    name: str = "finance"
    version: str = "0.1-reduced"
    paradigm: str = "system-dynamics"  # leverage-cycle accelerator (reduced)
    engines: tuple[str, ...] = ("behavior", "integration")
    provides: tuple[str, ...] = ("output_penalty", "credit_spread")
    requires: tuple[str, ...] = ()

    DECAY = 0.95  # per-step persistence a; stress ∝ t·aᵗ peaks at t ≈ 1/(-ln a) ≈ 20 (delayed crisis)
    MAX_PEN = 0.5  # cap on the output drag
    # Amplitude normaliser so the stress peak equals the credit_shock dial: max of t·aᵗ is (1/λ)·e⁻¹.
    _XPEAK = (1.0 / (-math.log(DECAY))) * math.exp(-1.0)

    def __init__(self) -> None:
        self._seed = 0

    def dials_spec(self) -> DialsSpec:
        return DialsSpec(
            (
                Dial(
                    "credit_shock",
                    0.0,
                    low=0.0,
                    high=1.0,
                    description="financial-stress impulse; the leverage cycle builds it to a delayed peak",
                    provenance="patterns/policy-engine.md",
                ),
            )
        )

    def init_state(self, dials: Mapping[str, Any], seed: int) -> dict[str, float]:
        self._seed = seed
        # Two-state critically-damped response: p_t = aᵗ, x_t = t·aᵗ (a smooth delayed hump).
        return {"p": 1.0, "x": 0.0, "credit_spread": 0.0, "output_penalty": 0.0}

    def step(
        self,
        state: Mapping[str, float],
        inputs: Mapping[str, float],
        dt: float,
        dials: Mapping[str, Any],
    ) -> StepResult:
        shock = float(dials["credit_shock"])
        p = float(state.get("p", 1.0))
        x = float(state.get("x", 0.0))
        stress = shock * x / self._XPEAK  # normalised so the peak equals `shock`
        output_penalty = min(max(stress, 0.0), self.MAX_PEN)
        x_new = self.DECAY * x + self.DECAY * p  # x_{t+1} = a·x_t + a·p_t  ⇒  x_t = t·aᵗ
        p_new = self.DECAY * p  # p_{t+1} = a·p_t   ⇒  p_t = aᵗ
        prov = Provenance.make(
            model=self.name, version=self.version, paradigm=self.paradigm, solver="closed-form-accelerator",
            seed=self._seed, dials=dials, inputs=inputs,
        )
        return StepResult(
            state={"p": p_new, "x": x_new, "credit_spread": stress, "output_penalty": output_penalty},
            outputs={"output_penalty": output_penalty, "credit_spread": stress},
            provenance=prov,
            diagnostics={"credit_spread": stress},
        )

    def observe(self, state: Mapping[str, float], keys: tuple[str, ...]) -> dict[str, float]:
        return {k: float(state.get(k, 0.0)) for k in keys}
