"""Directional attribution and the **low power of the lead-lag test** (Iters 61–62 — a self-correction).

Iter 61 asked whether education⇄income should join the reliable findings. It **survives** the panel bar
(within-FE +0.22, OOS +0.38) but its within-country lead-lag is symmetric (schooling→income +0.37 vs
income→schooling +0.38), and Iter 61 read that symmetry as the *distinguishing* evidence that the pair is
bidirectional and therefore not directionally interpretable.

**Iter 62 tested that claim against the reliable findings themselves — and corrected it.** Running the same
within-country lead-lag on the three income→X survivors shows they are *also* near-symmetric:

| Pair | income→outcome (t→t+1) | outcome→income (t→t+1) |
|---|---:|---:|
| income → life expectancy | +0.217 | +0.233 |
| income → fertility | −0.191 | −0.202 |
| income → absolute poverty | −0.483 | −0.493 |
| education ⇄ income | +0.367 | +0.383 |

In **every** case the reverse lead-lag is marginally *stronger* than the forward. The lead-lag test does **not**
single out education — it is near-symmetric for all four. The reason is statistical, not causal: these series
(income, life expectancy, fertility, poverty, enrolment) are **highly persistent**, so each variable at *t* is
almost itself at *t+1*, and lag-1 cross-correlations are near-symmetric **regardless of the true causal
direction**. The lead-lag test is simply **low-powered** for smooth macro series.

**The corrected lesson (the honest one):** a data-driven lead-lag *cannot* certify the direction of a surviving
within-correlation for persistent series. Direction has to come from **outside the data** — from
*manipulability*: which variable is an actionable policy lever, and is it the *only* one?

- income → {life expectancy, fertility, poverty}: income is a manipulable lever and the reverse is **not** a
  policy channel (you cannot legislate longevity, fertility, or a poverty rate directly), so treating income as
  the actionable driver is defensible — **as a manipulability argument, explicitly not a data-proven direction.**
- education ⇄ income: **both** are independently manipulable levers (invest in schooling; grow income), so
  neither is "the" driver — which is why it stays out of the reliable findings.

This refines, rather than repeals, Iter 61's core point: a surviving within-correlation is **necessary but not
sufficient** for a directional claim. What Iter 62 corrects is *how* the sufficiency is established — by an
external manipulability argument, not by a (here uninformative) lead-lag asymmetry. Catching and fixing that
overreach is the same discipline the whole project runs on.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from .panel_validation import (
    oos_within_prediction,
    run_education_panel,
    within_leadlag,
)
from ..data.loaders import (
    load_real_demographic_panel,
    load_real_education_panel,
    load_real_poverty_panel,
    load_real_preston_panel,
)


@dataclass(frozen=True)
class DirectionalityResult:
    within_corr: float
    oos_within_corr: float
    lead_forward: float  # driver(t) → outcome(t+1), within-country, FE-removed
    lead_reverse: float  # outcome(t) → driver(t+1), within-country, FE-removed

    @property
    def within_survives(self) -> bool:
        """The contemporaneous within-FE correlation is non-trivial and forecasts (would 'pass' the bar)."""
        return abs(self.within_corr) > 0.1 and abs(self.oos_within_corr) > 0.1

    @property
    def leadlag_symmetric(self) -> bool:
        """The two lead-lag correlations are close — near-symmetric. NOTE (Iter 62): this is true for *all*
        the persistent panel pairs (survivors included), so it does **not** by itself distinguish a
        bidirectional pair from a one-way one — the lead-lag test is low-powered for smooth series."""
        return abs(abs(self.lead_forward) - abs(self.lead_reverse)) < 0.1


def _pair(iso: np.ndarray, year: np.ndarray, driver: np.ndarray, outcome: np.ndarray) -> DirectionalityResult:
    from .panel_validation import two_way_within

    return DirectionalityResult(
        within_corr=two_way_within(outcome, driver, iso, year),
        oos_within_corr=oos_within_prediction(iso, year, driver, outcome),
        lead_forward=within_leadlag(driver, outcome, iso, year, k=1),
        lead_reverse=within_leadlag(outcome, driver, iso, year, k=1),
    )


def run_education_directionality() -> DirectionalityResult:
    """Education⇄income directional stress test (the motivating case): within-FE correlation, out-of-sample
    within-prediction, and the two within-country lead-lag correlations."""
    fe = run_education_panel()
    iso, year, log_gdppc, sec = load_real_education_panel()
    return DirectionalityResult(
        within_corr=fe.within_corr,
        oos_within_corr=oos_within_prediction(iso, year, log_gdppc, sec),
        lead_forward=within_leadlag(sec, log_gdppc, iso, year, k=1),
        lead_reverse=within_leadlag(log_gdppc, sec, iso, year, k=1),
    )


def survivor_directionality() -> dict[str, DirectionalityResult]:
    """The three income→X reliable-finding survivors, run through the *same* lead-lag test as education — the
    control that reveals the test's low power (all near-symmetric)."""
    out: dict[str, DirectionalityResult] = {}
    for name, load in (
        ("income → life expectancy", load_real_preston_panel),
        ("income → fertility", load_real_demographic_panel),
        ("income → absolute poverty", load_real_poverty_panel),
    ):
        iso, year, inc, outcome = load()
        out[name] = _pair(iso, year, inc, outcome)
    return out


def leadlag_test_is_low_power() -> bool:
    """True iff the lead-lag is near-symmetric for **all** the survivors *and* education — i.e. the test does
    not discriminate direction for these persistent series (the empirical basis for the Iter-62 correction)."""
    results = list(survivor_directionality().values()) + [run_education_directionality()]
    return all(r.leadlag_symmetric for r in results)


def directional_attribution_summary() -> str:
    """One honest line: the lead-lag test is low-power for smooth series, so direction rests on manipulability."""
    return (
        "Lead-lag is near-symmetric for ALL persistent panel pairs (survivors AND education), so it cannot "
        "certify direction — the test is low-powered for smooth series. Directional attribution therefore rests "
        "on an EXTERNAL manipulability argument (income is the actionable lever; the reverse is not a policy "
        "channel), NOT on a data lead-lag. Education stays out because BOTH its directions are manipulable."
    )
