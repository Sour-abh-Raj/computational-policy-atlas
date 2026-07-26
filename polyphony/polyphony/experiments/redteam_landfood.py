"""Red Team for the Land⇄Climate⇄Food coupling — is its Δ+23.9 real, or a level artifact?

Iter 12 showed the *energy* synergy collapsed to a **cut** once the baseline was fairly calibrated.
This module applies the same adversarial test to the land coupling, plus a policy distribution shift
and the decisive naive baseline. The result differs from energy — the coupling **survives** the
level-artifact attack — which is exactly the discrimination the tournament exists to make. A break is a
finding, recorded (blueprint §7). Reuses the :class:`~polyphony.tournament.redteam.AttackResult` contract.
"""

from __future__ import annotations

import numpy as np

from ..data.loaders import synthetic_food_series
from ..data.splits import time_blocked_split
from ..engines.calibration import calibrate_scale_offset, calibrated_track
from ..eval.metrics import mase
from ..tournament.redteam import AttackResult, RedTeamReport
from .landfood import calibrated_synergy, foodprice_track


def _calibrated_delta(y: np.ndarray, cp_predict: float, train: slice, test: slice) -> tuple[float, float]:
    """Fair calibration of BOTH sides on the train block; returns (coupled_cal_mase, calibrated Δ)."""
    coupled = foodprice_track(cp_predict, len(y), coupled=True)
    land = foodprice_track(cp_predict, len(y), coupled=False)
    ac, bc = calibrate_scale_offset(coupled[train], y[train])
    al, bl = calibrate_scale_offset(land[train], y[train])
    mc = mase(y[test], calibrated_track(coupled, ac, bc)[test])
    ml = mase(y[test], calibrated_track(land, al, bl)[test])
    return mc, ml - mc


def attack_level_artifact(n: int = 40, seed: int = 0) -> AttackResult:
    """The energy-killer: after a FAIR calibration of the land-only baseline, does the coupling still help?"""
    result = calibrated_synergy(synthetic_food_series(n=n, seed=seed, carbon_price=0.0))
    return AttackResult(
        "level_artifact",
        broke=result.delta <= 0.05,
        evidence={"coupled_cal_mase": result.coupled_cal_mase, "land_cal_mase": result.land_cal_mase, "cal_delta": result.delta},
        description="Fair calibration of the baseline must not erase the coupling's advantage (energy failed this).",
    )


def attack_policy_shift(cp_train: float = 0.0, cp_test: float = 100.0, n: int = 40, seed: int = 0) -> AttackResult:
    """The world mitigates (cp_test) but the champion assumed none (cp_train); does the coupling survive after calibration?"""
    y = synthetic_food_series(n=n, seed=seed, carbon_price=cp_test).column("food_price")
    split = time_blocked_split(n)
    _, delta = _calibrated_delta(y, cp_train, split.train, split.test)
    return AttackResult(
        "policy_shift",
        broke=delta <= 0.0,
        evidence={"cp_train": cp_train, "cp_test": cp_test, "cal_delta": delta},
        description="Unassumed mitigation policy shifts warming; calibrated coupling must still beat land-only.",
    )


def attack_edge_dials() -> AttackResult:
    bad = [
        (cp, tc)
        for cp in (0.0, 1000.0)
        for tc in (0.0, 0.01)
        if not np.all(np.isfinite(foodprice_track(cp, 20, coupled=True, tcre=tc)))
    ]
    return AttackResult("edge_dials", broke=len(bad) > 0, evidence={"nonfinite_at": bad}, description="Extreme carbon_price/tcre dials.")


def attack_naive_baseline(n: int = 40, seed: int = 0, calibrate: bool = True) -> AttackResult:
    """Decisive skill test: must the (calibrated) champion beat a naive random-walk forecast (MASE<1)?"""
    y = synthetic_food_series(n=n, seed=seed, carbon_price=0.0).column("food_price")
    split = time_blocked_split(n)
    coupled = foodprice_track(0.0, n, coupled=True)
    if calibrate:
        a, b = calibrate_scale_offset(coupled[split.train], y[split.train])
        coupled = calibrated_track(coupled, a, b)
    m = mase(y[split.test], coupled[split.test])
    return AttackResult(
        "naive_baseline" + ("_calibrated" if calibrate else ""),
        broke=m > 1.0,
        evidence={"coupled_mase": m, "beats_naive": m <= 1.0, "calibrated": calibrate},
        description="Champion must beat a naive random-walk forecast (MASE<1).",
    )


def run_red_team(n: int = 40, seed: int = 0) -> RedTeamReport:
    """Red-team the Land⇄Climate⇄Food coupling. The coupling is KEPT (survives the level-artifact and
    policy-shift attacks after calibration) but the champion still LOSES to naive — an honest split."""
    return RedTeamReport(
        attacks=(
            attack_level_artifact(n=n, seed=seed),
            attack_policy_shift(n=n, seed=seed),
            attack_edge_dials(),
            attack_naive_baseline(n=n, seed=seed, calibrate=True),
        )
    )
