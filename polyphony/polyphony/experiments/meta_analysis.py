"""Meta-analysis — what separates the keeps from the cuts? (Iter 37)

Across eight couplings, two were kept and seven cut. The synthesis question is *which property* actually
distinguishes them — because that is the load-bearing test a modeller should trust. Each coupling is scored
on four booleans drawn from its real-data result (each asserted in its own domain test):

- **right_sign** — the real correlation has the mechanism's assumed sign;
- **beats_placebo** — beats a meaningless-regressor placebo (robustly / in most walk-forward folds);
- **beats_naive** — beats a naive random-walk forecast out of sample;
- **beats_baseline** — beats the honest *sum-of-parts / climatology* baseline out of sample.

The finding is sharp and slightly surprising: **only `beats_baseline` perfectly separates keep from cut.**
Each of the other three admits a **false positive** — a coupling that *has* the property yet was still cut.
The decisive case is **Macro⇄Finance**: right sign, beats a placebo, and beats naive in a majority of
folds — yet cut, because it does not beat the mean-growth baseline (its skill is regime-dependent). So a
strong correlation, the right sign, beating a placebo, even beating naive are each **necessary-ish but not
sufficient**; the one criterion that decides is **beating the honest baseline**. That is the whole project's
discipline in a single computed fact.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class CouplingFeatures:
    coupling: str
    kept: bool
    right_sign: bool
    beats_placebo: bool
    beats_naive: bool
    beats_baseline: bool

    def has(self, feature: str) -> bool:
        return bool(getattr(self, feature))


_FEATURE_NAMES = ("right_sign", "beats_placebo", "beats_naive", "beats_baseline")

# Curated from the real-data results (each fact is asserted in the domain's own tournament test).
FEATURES: tuple[CouplingFeatures, ...] = (
    CouplingFeatures("Macro⇄Health", True, True, True, True, True),
    CouplingFeatures("Energy⇄Inflation", True, True, True, True, True),
    CouplingFeatures("Energy⇄climate⇄economy", False, True, False, False, False),
    CouplingFeatures("Real climate→GDP", False, True, False, False, False),
    CouplingFeatures("Land⇄Climate⇄Food", False, False, False, False, False),
    CouplingFeatures("Urban⇄Transport⇄Energy⇄Health", False, True, False, False, False),
    CouplingFeatures("Water⇄Energy⇄Food", False, True, False, False, False),
    CouplingFeatures("Macro⇄Finance", False, True, True, True, False),  # the instructive false positive
    CouplingFeatures("Trade⇄Emissions", False, True, False, False, False),
    CouplingFeatures("Interest-Rate⇄Housing", False, True, False, False, False),  # right-signed lag, loses to momentum
)


def _separates(feature: str) -> bool:
    """True if ``feature`` is present in every kept coupling and absent in every cut one."""
    return all(c.has(feature) == c.kept for c in FEATURES)


def perfect_separators() -> tuple[str, ...]:
    """Feature(s) that perfectly partition keep from cut."""
    return tuple(f for f in _FEATURE_NAMES if _separates(f))


def false_positive_features() -> dict[str, tuple[str, ...]]:
    """For each non-separating feature, the *cut* couplings that nonetheless have it (the false positives)."""
    out: dict[str, tuple[str, ...]] = {}
    for f in _FEATURE_NAMES:
        if not _separates(f):
            out[f] = tuple(c.coupling for c in FEATURES if c.has(f) and not c.kept)
    return out


def kept() -> tuple[CouplingFeatures, ...]:
    return tuple(c for c in FEATURES if c.kept)


def cut() -> tuple[CouplingFeatures, ...]:
    return tuple(c for c in FEATURES if not c.kept)
