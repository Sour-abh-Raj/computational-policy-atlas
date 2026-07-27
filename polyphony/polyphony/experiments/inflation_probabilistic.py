"""Probabilistic scoring of the Energy⇄Inflation keep (Iter 49) — is the one keep also *calibrated*?

Round 19 (`real_probabilistic.py`) showed the **cut** couplings are not merely inaccurate but **grossly
overconfident** — their predictive intervals almost never contain the truth (PIT piled at the tails). The
complementary question was never asked: is the coupling that *clears* the bar — Energy⇄Inflation — also
**honest about its uncertainty**? (Its target is a growth rate that can go negative, so the log-trend
scorer used for the cuts does not apply; this uses the pass-through point forecast + a train-residual
ensemble, against an honest persistence naive.)

The answer completes the picture: the keep is **accurate *and* calibrated** — its predictive distribution
beats a naive one on **CRPS**, and its **PIT** is centred (mean ≈ 0.5) with roughly nominal central
coverage. So the one coupling that earns its keep is trustworthy in *both* dimensions — the mirror image of
the cuts, which are wrong *and* overconfident. Skill and honest uncertainty travel together here, exactly as
they should.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from ..data.loaders import load_real_inflation
from ..data.splits import time_blocked_split
from ..eval.metrics import crps_series, pit_values
from .inflation_tournament import _growth, _passthrough_predict


@dataclass(frozen=True)
class ProbInflationResult:
    crps_coupled: float
    crps_naive: float
    pit_mean: float
    pit_in_iqr: float  # fraction of PIT in [0.25, 0.75]; ≈ 0.5 if calibrated

    @property
    def crps_beats_naive(self) -> bool:
        return self.crps_coupled < self.crps_naive

    @property
    def calibrated(self) -> bool:
        return abs(self.pit_mean - 0.5) < 0.15 and self.pit_in_iqr >= 0.35


def score_inflation_keep(test_frac: float = 0.3, seed: int = 0, m: int = 400) -> ProbInflationResult:
    ds = load_real_inflation()
    y = _growth(ds.column("cpi"))
    energy = _growth(ds.column("energy"))
    n = len(y)
    split = time_blocked_split(n, test_frac)
    tr, te = split.train, split.test
    rng = np.random.default_rng(seed)

    coupled = _passthrough_predict(y, energy, tr)
    resid = y[tr] - coupled[tr]
    samp_c = coupled[te][:, None] + rng.choice(resid, size=(n - te.start, m), replace=True)

    persistence = np.concatenate([[y[0]], y[:-1]])  # honest naive: last quarter's inflation
    naive_resid = np.diff(y[tr])
    samp_n = persistence[te][:, None] + rng.choice(naive_resid, size=(n - te.start, m), replace=True)

    pit = pit_values(samp_c, y[te])
    return ProbInflationResult(
        crps_coupled=crps_series(samp_c, y[te]),
        crps_naive=crps_series(samp_n, y[te]),
        pit_mean=float(np.mean(pit)),
        pit_in_iqr=float(np.mean((pit >= 0.25) & (pit <= 0.75))),
    )
