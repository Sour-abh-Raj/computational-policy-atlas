"""Parametric uncertainty — sample dials → an ensemble of tracks → probabilistic scoring.

Turns the point predictor into a **distribution** by sampling the uncertain dials (carbon price,
climate sensitivity ``tcre``) and running the coupled ensemble per draw. This lets **CRPS/PIT**
calibration enter the scored tournament (blueprint §6), not just point MASE — carrying uncertainty
end to end rather than collapsing to one number.
"""

from __future__ import annotations

import numpy as np
from numpy.typing import ArrayLike

from ..eval.metrics import crps_series
from .slice_tournament import gdp_track


def ensemble_gdp_tracks(
    cp: float = 50.0,
    steps: int = 40,
    members: int = 64,
    cp_sd: float = 10.0,
    tcre_mean: float = 0.001,
    tcre_sd: float = 0.0003,
    seed: int = 0,
    coupled: bool = True,
) -> np.ndarray:
    """(steps, members) ensemble of GDP tracks from sampled dials (coupled or economy-only)."""
    rng = np.random.default_rng(seed)
    cols = []
    for _ in range(members):
        c = float(max(0.0, rng.normal(cp, cp_sd)))
        tc = float(np.clip(rng.normal(tcre_mean, tcre_sd), 0.0, 0.01))
        cols.append(gdp_track(c, steps, coupled=coupled, tcre=tc))
    return np.stack(cols, axis=1)


def ensemble_crps(target: ArrayLike, cp: float = 50.0, **kwargs) -> float:
    """Mean CRPS of the sampled coupled ensemble against a target GDP series."""
    y = np.asarray(target, float)
    samples = ensemble_gdp_tracks(cp=cp, steps=len(y), **kwargs)
    return crps_series(samples, y)
