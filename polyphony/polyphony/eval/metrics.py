"""Point and probabilistic skill metrics + calibration (numpy only)."""

from __future__ import annotations

import numpy as np
from numpy.typing import ArrayLike


def mae(y_true: ArrayLike, y_pred: ArrayLike) -> float:
    y, yh = np.asarray(y_true, float), np.asarray(y_pred, float)
    return float(np.mean(np.abs(y - yh)))


def rmse(y_true: ArrayLike, y_pred: ArrayLike) -> float:
    y, yh = np.asarray(y_true, float), np.asarray(y_pred, float)
    return float(np.sqrt(np.mean((y - yh) ** 2)))


def mase(y_true: ArrayLike, y_pred: ArrayLike) -> float:
    """Mean Absolute Scaled Error (Hyndman & Koehler 2006): MAE / naive one-step MAE.

    Scale-free; <1 means the prediction beats a random-walk naive forecast.
    """
    y, yh = np.asarray(y_true, float), np.asarray(y_pred, float)
    if y.size < 2:
        raise ValueError("MASE needs at least 2 points")
    naive = float(np.mean(np.abs(np.diff(y))))
    naive = naive if naive > 0 else 1e-9
    return float(np.mean(np.abs(y - yh)) / naive)


def crps_ensemble(samples: ArrayLike, obs: float) -> float:
    """Empirical CRPS of a finite ensemble against a scalar observation.

    CRPS = E|X - y| - ½ E|X - X'| (Gneiting & Raftery 2007). Reduces to |mean - y| =
    absolute error for a degenerate (point) ensemble, and rewards sharp, well-placed spread.
    """
    s = np.asarray(samples, float)
    y = float(obs)
    term1 = np.mean(np.abs(s - y))
    term2 = np.mean(np.abs(s[:, None] - s[None, :]))
    return float(term1 - 0.5 * term2)


def crps_series(samples: ArrayLike, y_true: ArrayLike) -> float:
    """Mean CRPS over time. ``samples`` is (T, M); ``y_true`` is (T,)."""
    s = np.asarray(samples, float)
    y = np.asarray(y_true, float)
    if s.ndim != 2 or s.shape[0] != y.shape[0]:
        raise ValueError("samples must be (T, M) aligned with y_true (T,)")
    return float(np.mean([crps_ensemble(s[t], y[t]) for t in range(y.shape[0])]))


def pit_values(samples: ArrayLike, y_true: ArrayLike) -> np.ndarray:
    """Probability Integral Transform per step: F_ensemble(obs). Uniform ⇒ calibrated."""
    s = np.asarray(samples, float)
    y = np.asarray(y_true, float)
    return np.array([np.mean(s[t] <= y[t]) for t in range(y.shape[0])], dtype=float)
