"""Synergy — the falsifiable coupling bet: does coupled out-predict the sum of parts?

Synergy Δ = (best isolated-part error) − (coupled error), on **held-out** data. Δ > 0 means the
coupling earns its keep; Δ ≤ 0 means cut it (a publishable "no synergy" result). This is the
headline metric that decides whether a cross-domain coupling stays (blueprint §7).
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping


@dataclass(frozen=True)
class SynergyResult:
    coupled_error: float
    best_part: str
    best_part_error: float
    delta: float  # best_part_error - coupled_error ; > 0 ⇒ coupled better ⇒ synergy
    positive: bool

    def verdict(self) -> str:
        return "keep (synergy)" if self.positive else "cut (no synergy)"


def measure_synergy(coupled_error: float, part_errors: Mapping[str, float]) -> SynergyResult:
    """Compare a coupled configuration's error to the *best* isolated part's error.

    ``part_errors`` maps a baseline name (e.g. a standalone voice, or an additive
    sum-of-parts predictor) to its held-out error. Lower error is better.
    """
    if not part_errors:
        raise ValueError("need at least one baseline part error")
    best_part = min(part_errors, key=lambda k: part_errors[k])
    best_err = part_errors[best_part]
    delta = best_err - coupled_error
    return SynergyResult(
        coupled_error=coupled_error,
        best_part=best_part,
        best_part_error=best_err,
        delta=delta,
        positive=delta > 0.0,
    )
