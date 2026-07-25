"""Runnable experiments — reproducible tournaments wiring the harness to the slice."""

from .slice_tournament import BacktestResult, backtest_gdp, run_two_regime_tournament

__all__ = ["BacktestResult", "backtest_gdp", "run_two_regime_tournament"]
