"""Red Team — try to BREAK the champion. No champion is trusted until it survives attack.

Attacks the Round-1 claim ("the energy⇄climate⇄economy coupling adds synergy — coupled beats
economy-only") under stress: distribution shift, extreme dials, a **Lucas-critique** policy-regime
change between train and test, and noise-seed instability. Each returns a structured
:class:`AttackResult`; a break is a **finding**, recorded and fed back into selection — never hidden
(blueprint §7). Predictor import is lazy to avoid an import cycle with ``experiments``.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from ..data.loaders import synthetic_policy_series
from ..data.splits import time_blocked_split
from ..eval.metrics import mase
from .synergy import measure_synergy


@dataclass(frozen=True)
class AttackResult:
    name: str
    broke: bool
    evidence: dict
    description: str


@dataclass(frozen=True)
class RedTeamReport:
    attacks: tuple[AttackResult, ...]

    @property
    def survived(self) -> bool:
        return not any(a.broke for a in self.attacks)

    def breaks(self) -> tuple[AttackResult, ...]:
        return tuple(a for a in self.attacks if a.broke)


def _synergy_on(y: np.ndarray, cp_predict: float, test: slice) -> tuple[float, float, float]:
    from ..experiments.slice_tournament import gdp_track  # lazy (avoids import cycle)

    coupled = gdp_track(cp_predict, len(y), coupled=True)
    econ = gdp_track(cp_predict, len(y), coupled=False)
    err_c = mase(y[test], coupled[test])
    err_e = mase(y[test], econ[test])
    return err_c, err_e, measure_synergy(err_c, {"economy_only": err_e}).delta


def attack_distribution_shift(cp_train: float = 50.0, cp_test: float = 150.0, n: int = 40, seed: int = 0) -> AttackResult:
    """The world runs at a carbon price the champion did not assume."""
    y = synthetic_policy_series(n=n, seed=seed, carbon_price=cp_test).column("gdp")
    err_c, err_e, delta = _synergy_on(y, cp_train, time_blocked_split(n).test)
    return AttackResult(
        "distribution_shift",
        broke=delta <= 0.0,
        evidence={"cp_train": cp_train, "cp_test": cp_test, "coupled_mase": err_c, "econ_mase": err_e, "synergy_delta": delta},
        description="Champion assumes cp_train but the DGP ran at cp_test.",
    )


def _regime_change_series(n: int, cp_a: float, cp_b: float, seed: int = 0) -> np.ndarray:
    rng = np.random.default_rng(seed)
    t = np.arange(n)
    cp = np.where(t < n // 2, cp_a, cp_b).astype(float)
    emissions = 80.0 * np.exp(-0.02 * cp) * (1.0 - 0.01 * t) + rng.normal(0, 1.5, n)
    cum = np.cumsum(np.clip(emissions, 0, None))
    damage = 0.005 * (0.001 * cum) ** 2
    return 100.0 * (1.0 - 0.002 * cp) * (1.0 - damage) + rng.normal(0, 0.6, n)


def attack_lucas_regime_change(cp_a: float = 50.0, cp_b: float = 250.0, n: int = 40, seed: int = 0) -> AttackResult:
    """Lucas critique: policy regime changes mid-series; champion still assumes the old policy."""
    y = _regime_change_series(n, cp_a, cp_b, seed)
    post_change = slice(n // 2, n)
    err_c, err_e, delta = _synergy_on(y, cp_a, post_change)
    return AttackResult(
        "lucas_regime_change",
        broke=delta <= 0.0,
        evidence={"cp_a": cp_a, "cp_b": cp_b, "coupled_mase": err_c, "econ_mase": err_e, "synergy_delta": delta},
        description="Carbon-price regime changes between train and test; champion assumes cp_a.",
    )


def attack_edge_dials() -> AttackResult:
    """Extreme carbon_price / tcre dials must not produce non-finite predictions."""
    from ..experiments.slice_tournament import gdp_track  # lazy

    bad: list[tuple[float, float]] = []
    for cp in (0.0, 1000.0):
        for tc in (0.0, 0.01):
            track = gdp_track(cp, 20, coupled=True, tcre=tc)
            if not np.all(np.isfinite(track)):
                bad.append((cp, tc))
    return AttackResult(
        "edge_dials",
        broke=len(bad) > 0,
        evidence={"nonfinite_at": bad},
        description="Extreme carbon_price/tcre dials; predictions must stay finite.",
    )


def attack_noise_stability(n: int = 40, cp: float = 50.0, seeds: int = 8) -> AttackResult:
    """Synergy sign must be robust across noise realizations (fragile if it flips a majority)."""
    flips = 0
    for s in range(seeds):
        y = synthetic_policy_series(n=n, seed=s, carbon_price=cp).column("gdp")
        _, _, delta = _synergy_on(y, cp, time_blocked_split(n).test)
        if delta <= 0.0:
            flips += 1
    frac = flips / seeds
    return AttackResult(
        "noise_stability",
        broke=frac > 0.5,
        evidence={"flip_fraction": frac, "seeds": seeds},
        description="Fraction of noise seeds where the coupling's advantage vanishes.",
    )


def attack_naive_baseline(n: int = 40, cp: float = 50.0, seed: int = 0) -> AttackResult:
    """The decisive skill test: must the champion beat a NAIVE random-walk forecast?

    MASE is defined against a one-step naive forecast, so MASE > 1 means the champion is *worse
    than naive*. A model that loses to naive has **no skill claim**, however favourable its synergy
    against a weaker structural baseline. This attack exists to stop Polyphony from mistaking
    "less-bad than an artificially weak baseline" for skill.
    """
    from ..experiments.slice_tournament import gdp_track  # lazy

    y = synthetic_policy_series(n=n, seed=seed, carbon_price=cp).column("gdp")
    test = time_blocked_split(n).test
    coupled_mase = mase(y[test], gdp_track(cp, n, coupled=True)[test])
    return AttackResult(
        "naive_baseline",
        broke=coupled_mase > 1.0,
        evidence={"coupled_mase": coupled_mase, "beats_naive": coupled_mase <= 1.0},
        description="Champion must beat a naive random-walk forecast (MASE<1), not just a weak baseline.",
    )


def run_red_team(n: int = 40, seed: int = 0) -> RedTeamReport:
    return RedTeamReport(
        attacks=(
            attack_distribution_shift(n=n, seed=seed),
            attack_lucas_regime_change(n=n, seed=seed),
            attack_edge_dials(),
            attack_noise_stability(n=n),
            attack_naive_baseline(n=n, seed=seed),
        )
    )
