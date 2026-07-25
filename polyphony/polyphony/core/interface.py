"""The common ``Model`` interface — the paradigm-agnostic contract every voice implements.

A voice may be an optimizing IAM, an LP energy model, a CGE, or an ABM; the interface
says nothing about *how* it decides, only how it exposes **state**, **steps**, declares
its **dials**, and records **provenance** (docs/polyphony/01-blueprint.md §2). Structural
typing (``Protocol``) means adapters need not inherit — they just match the shape.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping, Protocol, runtime_checkable

from .dials import DialsSpec
from .provenance import Provenance

# For the vertical slice, state/inputs are named scalars. numpy arrays are allowed later
# without changing the interface (values become float | np.ndarray).
State = Mapping[str, float]
Inputs = Mapping[str, float]
Dials = Mapping[str, Any]


@dataclass
class StepResult:
    """What a model returns from one ``step``: new state, coupling outputs, provenance."""

    state: dict[str, float]
    outputs: dict[str, float]
    provenance: Provenance
    diagnostics: dict[str, float] = field(default_factory=dict)


@runtime_checkable
class Model(Protocol):
    """The contract. See docs/polyphony/01-blueprint.md §2 for design rules."""

    name: str
    version: str
    paradigm: str  # "optimization" | "equilibrium" | "agent-based" | ...
    engines: tuple[str, ...]  # atlas engine patterns this model instantiates
    provides: tuple[str, ...]  # state/output keys it exposes for coupling
    requires: tuple[str, ...]  # input keys it needs from other voices

    def init_state(self, dials: Dials, seed: int) -> dict[str, float]:
        ...

    def step(self, state: State, inputs: Inputs, dt: float, dials: Dials) -> StepResult:
        ...

    def dials_spec(self) -> DialsSpec:
        ...

    def observe(self, state: State, keys: tuple[str, ...]) -> dict[str, float]:
        ...


def conforms(obj: object) -> bool:
    """True if ``obj`` satisfies the :class:`Model` protocol (attrs + methods present)."""
    return isinstance(obj, Model)
