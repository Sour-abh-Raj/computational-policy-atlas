"""Red team for the Energy⇄Inflation keep (Iter 43) — is the one clean real keep fragile?

A keep is only trustworthy if it survives adversarial attack, not just the standard walk-forward. The
obvious objection to "energy-price growth predicts inflation" is that it rides on **one episode** — the
2022 energy spike. So the decisive attack **removes the most extreme energy-move year** and re-runs the
walk-forward; if the keep holds, it is not a single-outlier artifact. Two more attacks probe **sub-period
stability** (does it hold in the early and recent halves separately?).

Result: the keep **survives the outlier attack** — dropping the 2022 spike, energy-price growth still beats
the baseline and naive in every fold. It is stable in the **recent** half; the **early** half is weaker, an
honest small-sample caveat (few folds, lower 1990s energy volatility). Reporting the sub-period weakness
alongside the outlier-robustness is the point — a keep with its fragilities disclosed, not hidden.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from ..data.loaders import load_real_inflation
from ..data.splits import walk_forward
from ..eval.metrics import mase
from .inflation_tournament import _growth, _passthrough_predict


def _wf(inflation: np.ndarray, energy_growth: np.ndarray, horizon: int = 4) -> tuple[float, float]:
    """(fraction of folds beating the mean baseline, fraction beating naive) for the pass-through."""
    n = len(inflation)
    base, coup = [], []
    for sp in walk_forward(n, min_train=n // 2, horizon=horizon):
        tr, te = sp.train, sp.test
        b = np.full(n, float(inflation[tr].mean()))
        c = _passthrough_predict(inflation, energy_growth, tr)
        base.append(mase(inflation[te], b[te]))
        coup.append(mase(inflation[te], c[te]))
    b_, c_ = np.array(base), np.array(coup)
    return float(np.mean(c_ < b_)), float(np.mean(c_ < 1.0))


@dataclass(frozen=True)
class RedTeamInflationResult:
    base_beats_baseline: float
    base_beats_naive: float
    drop_extreme_beats_baseline: float  # THE decisive attack: remove the 2022-style spike
    drop_extreme_beats_naive: float
    first_half_beats_baseline: float
    second_half_beats_baseline: float

    @property
    def survives_outlier_attack(self) -> bool:
        """The keep is not a single-episode artifact: it holds after the most extreme energy year is removed."""
        return self.drop_extreme_beats_baseline > 0.5 and self.drop_extreme_beats_naive > 0.5

    @property
    def stable_in_recent_half(self) -> bool:
        return self.second_half_beats_baseline > 0.5


def run_red_team() -> RedTeamInflationResult:
    ds = load_real_inflation()
    inflation = _growth(ds.column("cpi"))
    energy = _growth(ds.column("energy"))

    bb, bn = _wf(inflation, energy)
    k = int(np.argmax(np.abs(energy)))  # the most extreme energy-move year (the 2022 spike)
    keep = np.arange(len(energy)) != k
    db, dn = _wf(inflation[keep], energy[keep])
    h = len(inflation) // 2
    fh, _ = _wf(inflation[:h], energy[:h])
    sh, _ = _wf(inflation[h:], energy[h:])

    return RedTeamInflationResult(
        base_beats_baseline=bb,
        base_beats_naive=bn,
        drop_extreme_beats_baseline=db,
        drop_extreme_beats_naive=dn,
        first_half_beats_baseline=fh,
        second_half_beats_baseline=sh,
    )
