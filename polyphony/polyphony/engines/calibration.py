"""Calibration — fit a reduced-form voice's level/scale to a target to remove systematic bias.

The atlas [Calibration Engine](../patterns/calibration-engine.md) as a first, honest step: an affine
fit ``target ≈ a·track + b`` estimated on the **training block only** (no leakage). It reduces level
bias, but — stated plainly — it does **not** manufacture skill: a structurally poor track calibrated
to the right level can still lose to a naive forecast. Real structure/data (issue #9) remains the
binding gate.
"""

from __future__ import annotations

import numpy as np
from numpy.typing import ArrayLike


def calibrate_scale_offset(track: ArrayLike, target: ArrayLike) -> tuple[float, float]:
    """Least-squares affine fit: return (a, b) minimizing ||target − (a·track + b)||²."""
    x = np.asarray(track, float)
    y = np.asarray(target, float)
    if x.shape != y.shape or x.size < 2:
        raise ValueError("track and target must be same shape with >= 2 points")
    a_mat = np.vstack([x, np.ones_like(x)]).T
    (a, b), *_ = np.linalg.lstsq(a_mat, y, rcond=None)
    return float(a), float(b)


def calibrated_track(track: ArrayLike, a: float, b: float) -> np.ndarray:
    return a * np.asarray(track, float) + b
