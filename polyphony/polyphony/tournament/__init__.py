"""Tournament — adversarial selection. Nothing wins by a threshold; only by beating rivals.

``synergy`` measures coupled − best-sum-of-parts; ``race`` ranks contenders by out-of-sample
skill minus overfit/complexity penalties; ``leaderboard`` records every contest with provenance
(docs/polyphony/01-blueprint.md §7, ADR-0004).
"""

from .leaderboard import Leaderboard, LeaderboardRow
from .race import Contender, RaceResult, race
from .synergy import SynergyResult, measure_synergy

__all__ = [
    "measure_synergy",
    "SynergyResult",
    "race",
    "Contender",
    "RaceResult",
    "Leaderboard",
    "LeaderboardRow",
]
