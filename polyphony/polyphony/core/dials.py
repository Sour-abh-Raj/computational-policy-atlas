"""Dials — contested assumptions as inspectable, validated parameters.

Every contested modeling assumption from the atlas comparative matrices (optimization↔
simulation, equilibrium↔disequilibrium, foresight, …) — plus Polyphony's own *values*
dial (welfare/equity) — is a ``Dial``. A model declares its ``DialsSpec``; the
orchestrator validates and threads dial settings through every step, and provenance
records exactly which values were used.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class Dial:
    """One contested assumption. Categorical (``choices``) or numeric (``low``/``high``)."""

    name: str
    default: Any
    choices: tuple[Any, ...] | None = None
    low: float | None = None
    high: float | None = None
    description: str = ""
    provenance: str = ""  # atlas comparative-matrix link or citation

    def validate(self, value: Any) -> None:
        if self.choices is not None and value not in self.choices:
            raise ValueError(f"dial {self.name!r}={value!r} not in {self.choices}")
        if self.low is not None and value < self.low:
            raise ValueError(f"dial {self.name!r}={value!r} < low {self.low}")
        if self.high is not None and value > self.high:
            raise ValueError(f"dial {self.name!r}={value!r} > high {self.high}")


@dataclass(frozen=True)
class DialsSpec:
    dials: tuple[Dial, ...]

    def defaults(self) -> dict[str, Any]:
        return {d.name: d.default for d in self.dials}

    def validate(self, values: dict[str, Any]) -> dict[str, Any]:
        """Merge ``values`` onto defaults, validating each; reject unknown dials."""
        by_name = {d.name: d for d in self.dials}
        merged = self.defaults()
        for k, v in values.items():
            if k not in by_name:
                raise KeyError(f"unknown dial {k!r} (known: {sorted(by_name)})")
            by_name[k].validate(v)
            merged[k] = v
        return merged
