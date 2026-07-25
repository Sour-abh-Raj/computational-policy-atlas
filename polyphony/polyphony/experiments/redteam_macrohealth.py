"""Red Team for the Macro⇄Health champion — attack the health⇄economy coupling.

Reuses the :class:`~polyphony.tournament.redteam.AttackResult` contract: an r0 distribution shift, a
**variant Lucas-critique** (r0 jumps mid-series while the champion assumes the old r0), extreme dials,
and the decisive **naive-baseline** test. A break is a finding, recorded — never hidden.
"""

from __future__ import annotations

import numpy as np

from ..data.loaders import synthetic_pandemic_series
from ..data.splits import time_blocked_split
from ..eval.metrics import mase
from ..tournament.redteam import AttackResult, RedTeamReport
from ..tournament.synergy import measure_synergy
from .macrohealth import gdp_track


def _synergy(y: np.ndarray, r0_predict: float, test: slice) -> tuple[float, float, float]:
    coupled = gdp_track(r0_predict, len(y), coupled=True)
    econ = gdp_track(r0_predict, len(y), coupled=False)
    err_c = mase(y[test], coupled[test])
    err_e = mase(y[test], econ[test])
    return err_c, err_e, measure_synergy(err_c, {"economy_only": err_e}).delta


def attack_r0_shift(r0_train: float = 2.5, r0_test: float = 4.0, n: int = 40, seed: int = 0) -> AttackResult:
    y = synthetic_pandemic_series(n=n, seed=seed, r0=r0_test).column("gdp")
    err_c, err_e, delta = _synergy(y, r0_train, time_blocked_split(n).test)
    return AttackResult(
        "r0_shift", broke=delta <= 0.0,
        evidence={"r0_train": r0_train, "r0_test": r0_test, "coupled_mase": err_c, "econ_mase": err_e, "synergy_delta": delta},
        description="World r0 differs from the champion's assumed r0.",
    )


def _regime_change_pandemic(n: int, r0_a: float, r0_b: float, seed: int = 0) -> np.ndarray:
    rng = np.random.default_rng(seed)
    s, i, r, g = 0.999, 0.001, 0.0, 0.2
    pen = np.empty(n)
    for t in range(n):
        r0 = r0_a if t < n // 2 else r0_b
        ni = r0 * g * s * i
        s = max(s - ni, 0.0)
        i = max(i + ni - g * i, 0.0)
        r = r + g * i
        pen[t] = min(2.0 * i, 0.6)
    return 100.0 * (1.0 - pen) + rng.normal(0, 0.6, n)


def attack_variant_lucas(r0_a: float = 2.5, r0_b: float = 5.0, n: int = 40, seed: int = 0) -> AttackResult:
    y = _regime_change_pandemic(n, r0_a, r0_b, seed)
    err_c, err_e, delta = _synergy(y, r0_a, slice(n // 2, n))
    return AttackResult(
        "variant_lucas", broke=delta <= 0.0,
        evidence={"r0_a": r0_a, "r0_b": r0_b, "coupled_mase": err_c, "econ_mase": err_e, "synergy_delta": delta},
        description="A variant changes r0 mid-series; the champion assumes the old r0.",
    )


def attack_edge_dials() -> AttackResult:
    bad = [r0 for r0 in (0.0, 10.0) if not np.all(np.isfinite(gdp_track(r0, 20, coupled=True)))]
    return AttackResult("edge_dials", broke=len(bad) > 0, evidence={"nonfinite_at": bad}, description="Extreme r0 dials.")


def attack_naive_baseline(n: int = 40, r0: float = 2.5, seed: int = 0) -> AttackResult:
    y = synthetic_pandemic_series(n=n, seed=seed, r0=r0).column("gdp")
    test = time_blocked_split(n).test
    m = mase(y[test], gdp_track(r0, n, coupled=True)[test])
    return AttackResult("naive_baseline", broke=m > 1.0, evidence={"coupled_mase": m}, description="Must beat a naive forecast (MASE<1).")


def run_red_team(n: int = 40, seed: int = 0) -> RedTeamReport:
    return RedTeamReport(
        attacks=(
            attack_r0_shift(n=n, seed=seed),
            attack_variant_lucas(n=n, seed=seed),
            attack_edge_dials(),
            attack_naive_baseline(n=n, seed=seed),
        )
    )
