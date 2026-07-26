"""Assimilation engine — the digital-twin backbone: estimate uncertain parameters from data.

The Macro⇄Health champion broke under an r0 distribution shift (Iter 10) because it *assumed* a
reproduction number. Assimilation fixes that: fit r0 from the **early observed** GDP dip (least-squares
over the SIR) on the train block, then feed the estimate into the coupled predictor. This is the
minimal form of the model ⇄ **data-assimilation** ⇄ control loop the digital-twin page describes
(atlas: [Digital Twins](../paradigms/algorithms/digital-twins.md)); grounding: Kalman (1960) / parameter
estimation. Grid-based here for transparency; a Kalman/particle filter is the natural upgrade.
"""

from __future__ import annotations

import numpy as np
from numpy.typing import ArrayLike


def sir_output_track(
    r0: float, n: int, penalty_coef: float = 2.0, gamma: float = 0.2, base: float = 100.0, max_penalty: float = 0.6
) -> np.ndarray:
    """GDP track implied by a reduced-form SIR at a given r0 (matches the epidemic voice)."""
    s, i, r = 0.999, 0.001, 0.0
    out = np.empty(n)
    for t in range(n):
        new_inf = r0 * gamma * s * i
        s = max(s - new_inf, 0.0)
        i = max(i + new_inf - gamma * i, 0.0)
        r = r + gamma * i
        out[t] = base * (1.0 - min(penalty_coef * i, max_penalty))
    return out


def estimate_r0(observed: ArrayLike, train: slice, lo: float = 0.5, hi: float = 8.0, steps: int = 76) -> float:
    """Assimilate r0: the value whose SIR GDP track best fits the observed dip on the TRAIN block."""
    y = np.asarray(observed, float)
    candidates = np.linspace(lo, hi, steps)
    errors = [float(np.mean((y[train] - sir_output_track(float(c), len(y))[train]) ** 2)) for c in candidates]
    return float(candidates[int(np.argmin(errors))])
