"""Failure-mode catalogue — how policy-simulation couplings fail on real data (Iter 31).

Seven cross-domain couplings were each *kept on synthetic data* and then tested on real data under a
strict bar (beat a rival, a placebo, and naive; have the assumed sign; hold up under walk-forward). One
survived; six were cut — and the value of the exercise is that **each cut names a distinct, reusable
failure mode.** This module is the canonical, tested taxonomy: the modes, the coupling that exemplifies
each, the real diagnostic that reveals it, and the lesson. It is the ensemble's honest product — a field
guide to the ways a plausible cross-sector story fails to earn its keep.

The catalogue is *data*, cross-checked by tests against the recorded ledger; the per-coupling diagnostics
are asserted live in each domain's own real-data test (see ``tests/test_real_*_tournament.py``).
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class FailureMode:
    key: str
    name: str
    definition: str
    diagnostic: str  # how the real-data machinery detects it
    lesson: str


@dataclass(frozen=True)
class CouplingVerdict:
    coupling: str
    mode: str  # a FailureMode.key, or "kept"
    headline: str  # the decisive real (or synthetic-round) number


CATALOGUE: tuple[FailureMode, ...] = (
    FailureMode(
        key="level-artifact",
        name="Level artifact",
        definition="The coupling only supplies a level/scale that a fairly-calibrated baseline reproduces.",
        diagnostic="Give the baseline its own train-block affine fit; the synergy Δ collapses to ≈0.",
        lesson="A big raw synergy can be pure level-matching. Calibrate both sides fairly before believing it.",
    ),
    FailureMode(
        key="genuinely-cyclic",
        name="Genuinely cyclic",
        definition="The coupling truly feeds back, so a no-lag (contemporaneous) solve is not admissible.",
        diagnostic="The routing graph has a cycle; the topological solver refuses and lagging is required.",
        lesson="Don't remove a coupling lag that encodes a real feedback just to buy apparent skill.",
    ),
    FailureMode(
        key="wrong-sign",
        name="Wrong sign",
        definition="The real-data correlation has the opposite sign to the mechanism's assumption.",
        diagnostic="corr(driver, target) contradicts the assumed direction (e.g. warming ↔ higher yield).",
        lesson="A mechanism true in a lab/cohort can have the wrong sign in aggregate data (confounders dominate).",
    ),
    FailureMode(
        key="confounded-away",
        name="Confounded-away (shared trend)",
        definition="Right sign and strong raw correlation, but the signal vanishes once a trend is removed.",
        diagnostic="Fails a placebo / the fitted partial coefficient → 0 / loses to a trend-scaled baseline.",
        lesson="A strong correlation between two trending series is usually the trend, not the mechanism.",
    ),
    FailureMode(
        key="real-signal-no-skill",
        name="Real signal, no out-of-sample skill",
        definition="Genuine, right-signed, placebo-beating information that still yields no forecast skill.",
        diagnostic="Beats a placebo but loses to a naive random walk (MASE ≥ 1) out of sample.",
        lesson="Contemporaneous association is not a usable forecast; a volatile target can be near-unforecastable.",
    ),
    FailureMode(
        key="regime-dependent-skill",
        name="Regime-dependent skill",
        definition="Real skill in some regimes (e.g. crises) that does not beat an unconditional baseline.",
        diagnostic="Beats placebo + naive in a majority of walk-forward folds, but not a climatology baseline.",
        lesson="Skill concentrated in rare regimes won't beat a mean/climatology on average — say so honestly.",
    ),
    FailureMode(
        key="reverse-causation",
        name="Reverse causation / policy endogeneity",
        definition="The policy responds to the outcome, so the contemporaneous correlation has the wrong sign.",
        diagnostic="Contemporaneous corr is opposite to the mechanism; even the correctly-signed lag loses to momentum.",
        lesson="When the lever reacts to the target (the Fed hikes into booms), use lags — and beware momentum baselines.",
    ),
)

_MODE_KEYS = frozenset(m.key for m in CATALOGUE) | {"kept"}

LEDGER: tuple[CouplingVerdict, ...] = (
    CouplingVerdict("Macro⇄Health", "kept", "survives full red-team round; assimilation + no-lag ⇒ MASE 0.10"),
    CouplingVerdict("Energy⇄Inflation", "kept", "REAL keep: corr +0.65, beats every baseline + naive across walk-forward folds"),
    CouplingVerdict("Energy⇄climate⇄economy", "level-artifact", "fair-cal Δ ≈ −0.01 (also genuinely cyclic)"),
    CouplingVerdict("Real climate→GDP", "confounded-away", "fails placebo under both CO₂ and temperature"),
    CouplingVerdict("Land⇄Climate⇄Food", "wrong-sign", "corr(temp, real yield) = +0.90 (Green Revolution)"),
    CouplingVerdict("Urban⇄Transport⇄Energy⇄Health", "confounded-away", "PM2.5 corr +0.35 but hazard k → 0; ties placebo"),
    CouplingVerdict("Water⇄Energy⇄Food (energy→food)", "real-signal-no-skill", "corr +0.90 but MASE ≫ 1 (loses to naive)"),
    CouplingVerdict("Macro⇄Finance (spread→growth)", "regime-dependent-skill", "corr −0.61, beats placebo 80% but not climatology"),
    CouplingVerdict("Trade⇄Emissions (carbon leakage)", "confounded-away", "openness↔gap corr +0.81 but loses to production-blind"),
    CouplingVerdict("Interest-Rate⇄Housing", "reverse-causation", "contemp corr +0.38 (Fed hikes into booms); lagged rate loses to momentum"),
)


def mode(key: str) -> FailureMode:
    """Look up a failure mode by key."""
    for m in CATALOGUE:
        if m.key == key:
            return m
    raise KeyError(key)


def kept() -> tuple[CouplingVerdict, ...]:
    return tuple(c for c in LEDGER if c.mode == "kept")


def cut() -> tuple[CouplingVerdict, ...]:
    return tuple(c for c in LEDGER if c.mode != "kept")


def modes_exemplified() -> frozenset[str]:
    """The set of failure-mode keys that at least one cut coupling exemplifies."""
    return frozenset(c.mode for c in cut())
