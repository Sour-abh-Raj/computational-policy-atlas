"""Data layer — real historical series + time-blocked splits for honest backtesting.

Prefers real CSVs dropped in ``polyphony/data/datasets/`` (documented schema); falls back to a
**clearly-labeled synthetic** series so the harness is testable offline. Sourcing real datasets
(World Bank GDP, Our World in Data CO₂, IEA energy balances) is tracked as a GitHub issue.
"""

from .loaders import (
    Dataset,
    load,
    synthetic_decoupled_series,
    synthetic_pandemic_series,
    synthetic_policy_series,
)
from .splits import Split, time_blocked_split, walk_forward

__all__ = [
    "Dataset",
    "load",
    "synthetic_policy_series",
    "synthetic_decoupled_series",
    "synthetic_pandemic_series",
    "Split",
    "time_blocked_split",
    "walk_forward",
]
