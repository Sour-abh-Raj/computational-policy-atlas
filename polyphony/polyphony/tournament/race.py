"""Race — rank contenders by out-of-sample skill minus overfit/complexity penalties.

Contenders are features, couplings, models, or combiners. Higher ``score`` (e.g. negative
held-out error) is better; ``penalty`` docks overfitting/leakage/redundancy/complexity so a
marginally-better-but-bloated candidate can lose. The winner is the top adjusted score.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Sequence


@dataclass(frozen=True)
class Contender:
    name: str
    score: float  # higher is better (e.g. -error, or skill)
    penalty: float = 0.0  # overfit / leakage / redundancy / complexity
    meta: dict[str, Any] = field(default_factory=dict)

    @property
    def adjusted(self) -> float:
        return self.score - self.penalty


@dataclass(frozen=True)
class RaceResult:
    ranked: tuple[Contender, ...]

    @property
    def winner(self) -> Contender:
        return self.ranked[0]

    def margin(self) -> float:
        """Winner's adjusted-score lead over the runner-up (0 if only one contender)."""
        if len(self.ranked) < 2:
            return 0.0
        return self.ranked[0].adjusted - self.ranked[1].adjusted


def race(contenders: Sequence[Contender]) -> RaceResult:
    if not contenders:
        raise ValueError("race needs at least one contender")
    ranked = tuple(sorted(contenders, key=lambda c: c.adjusted, reverse=True))
    return RaceResult(ranked=ranked)
