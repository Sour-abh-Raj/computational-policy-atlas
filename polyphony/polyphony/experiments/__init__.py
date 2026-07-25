"""Runnable experiments — reproducible tournaments wiring the harness to the slice."""

from .scored import ScoredResult, scored_backtest
from .slice_tournament import BacktestResult, backtest_gdp, run_two_regime_tournament
from .uncertainty import ensemble_crps, ensemble_gdp_tracks
from .welfare_frontier import frontier_and_recommendations, policy_outcomes, recommendations

__all__ = [
    "BacktestResult",
    "backtest_gdp",
    "run_two_regime_tournament",
    "ensemble_gdp_tracks",
    "ensemble_crps",
    "ScoredResult",
    "scored_backtest",
    "policy_outcomes",
    "recommendations",
    "frontier_and_recommendations",
]
