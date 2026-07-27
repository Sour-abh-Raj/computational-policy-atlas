"""Higher-power confirmation of the Energy⇄Inflation keep at quarterly frequency (Iter 48).

The keep was established on **annual** data (32 years ⇒ only ~4 walk-forward folds). A fair worry is that a
4-fold walk-forward is low-powered. This re-runs the *same* pass-through test at **quarterly** frequency
(~136 quarters ⇒ ~8 folds), using annualized quarter-on-quarter growth. If the keep holds with roughly
double the folds and a stronger contemporaneous correlation, it is not an artifact of low-power annual data
— it is the project's most solidly established real-data result.
"""

from __future__ import annotations

import numpy as np

from ..data.loaders import load_real_inflation_q
from .inflation_tournament import InflationResult, _score


def _annualized_growth(x: np.ndarray) -> np.ndarray:
    return np.diff(np.log(x)) * 400.0  # quarter-on-quarter, annualized (%)


def run_quarterly_confirmation(horizon: int = 8) -> InflationResult:
    ds = load_real_inflation_q()
    inflation = _annualized_growth(ds.column("cpi"))
    energy_growth = _annualized_growth(ds.column("energy"))
    return _score(inflation, energy_growth, horizon)
