"""Polyphony engines — the `＊new` capabilities the atlas implies but does not yet ship.

Currently: the **welfare/equity engine** (the inspectable values dial — issue #4) and a
**calibration** helper. Data-assimilation, surrogate, and ensemble/meta engines follow.
"""

from .calibration import calibrate_scale_offset, calibrated_track
from .welfare import (
    PolicyOutcome,
    WelfareDials,
    atkinson_index,
    ede,
    gini,
    objective_vector,
    pareto_frontier,
    rank_policies,
    social_welfare_score,
    value_of_information,
)

__all__ = [
    "WelfareDials",
    "PolicyOutcome",
    "ede",
    "gini",
    "atkinson_index",
    "objective_vector",
    "pareto_frontier",
    "social_welfare_score",
    "rank_policies",
    "value_of_information",
    "calibrate_scale_offset",
    "calibrated_track",
]
