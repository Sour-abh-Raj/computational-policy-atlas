"""Provenance — every number Polyphony produces is traceable.

A ``Provenance`` record pins the exact model version, paradigm, solver, RNG seed, the
dials in force, and a stable hash of the inputs consumed. This is what makes any
ensemble answer reproducible and any *disagreement* attributable to a concrete cause
(see docs/polyphony/01-blueprint.md §2).
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass
from typing import Any, Mapping


def stable_hash(obj: Any) -> str:
    """Deterministic short hash of any JSON-encodable object (sorted keys)."""
    payload = json.dumps(obj, sort_keys=True, default=str, separators=(",", ":"))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()[:16]


@dataclass(frozen=True)
class Provenance:
    model: str
    version: str
    paradigm: str
    solver: str
    seed: int
    dials: Mapping[str, Any]
    inputs_hash: str

    def to_dict(self) -> dict[str, Any]:
        d = asdict(self)
        d["dials"] = dict(self.dials)
        return d

    @classmethod
    def make(
        cls,
        *,
        model: str,
        version: str,
        paradigm: str,
        solver: str,
        seed: int,
        dials: Mapping[str, Any],
        inputs: Mapping[str, Any],
    ) -> "Provenance":
        return cls(
            model=model,
            version=version,
            paradigm=paradigm,
            solver=solver,
            seed=seed,
            dials=dict(dials),
            inputs_hash=stable_hash(dict(inputs)),
        )
