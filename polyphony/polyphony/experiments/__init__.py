"""Runnable experiments — reproducible tournaments wiring the harness to the slice."""

from .slice_tournament import BacktestResult, backtest_gdp, run_two_regime_tournament
from .uncertainty import ensemble_crps, ensemble_gdp_tracks

__all__ = [
    "BacktestResult",
    "backtest_gdp",
    "run_two_regime_tournament",
    "ensemble_gdp_tracks",
    "ensemble_crps",
]
