"""The panel instrument's **second boundary**: direction-blindness under simultaneity (Iter 61).

The panel survivors — income → life expectancy, → fertility, → absolute poverty — all share a feature that
made their within-FE correlation *interpretable*: income is the clear **driver**, the outcome does not push
back on income within the horizons that matter. Education ⇄ income breaks that assumption. Human capital
raises income (Mincer returns) **and** richer countries school more (income funds education) — the pair is
**bidirectionally causal**. So it is the perfect stress test of what a surviving two-way-FE within-correlation
does and does *not* license.

On real World Bank data (secondary-school gross enrolment vs log GDP per capita, 236 countries, 1970–2025):

- The within-FE correlation **survives** — +0.22, and it forecasts held-out years (OOS ≈ +0.38). By the bar
  that admitted the other panel survivors, this "passes".
- **But the lead-lag is symmetric.** Schooling(t) → income(t+1) correlates +0.37; income(t) → schooling(t+1)
  correlates +0.38 — if anything income leads schooling *slightly more*. Neither direction dominates.

**The boundary:** a surviving within-correlation is **necessary but not sufficient** for a *directional*
(let alone causal) claim. For income→poverty the direction is defensible from outside the data (income is the
policy lever, poverty the mechanical consequence); for education⇄income it is **not** — calling this "returns
to schooling" would overclaim, because the reverse channel is at least as strong here. So education⇄income is
**deliberately not promoted to a reliable finding**; it is documented as the instrument's second limit.

This complements the first boundary (PM2.5 → all-cause mortality, Iter 34): there, FE fails because the
*outcome* is dominated by a confounded within-country trend. Here, FE *succeeds* at detecting covariation but
is **direction-blind** when causation runs both ways. Two distinct ways a panel within-correlation can fail to
mean what a hasty reader wants it to mean — both stated, neither hidden.
"""

from __future__ import annotations

from dataclasses import dataclass

from .panel_validation import (
    oos_within_prediction,
    run_education_panel,
    within_leadlag,
)
from ..data.loaders import load_real_education_panel


@dataclass(frozen=True)
class DirectionalityResult:
    within_corr: float
    oos_within_corr: float
    lead_school_to_income: float  # schooling(t) → income(t+1), within-country, FE-removed
    lead_income_to_school: float  # income(t) → schooling(t+1), within-country, FE-removed

    @property
    def within_survives(self) -> bool:
        """The contemporaneous within-FE correlation is non-trivial (would 'pass' the survivor bar)."""
        return abs(self.within_corr) > 0.1 and abs(self.oos_within_corr) > 0.1

    @property
    def directionally_ambiguous(self) -> bool:
        """Neither lead-lag direction dominates — the survival cannot be assigned a direction. True when the
        two lead-lag correlations are close (within 0.1) and the reverse channel is not weaker than assumed."""
        return abs(self.lead_school_to_income - self.lead_income_to_school) < 0.1

    @property
    def is_reliable_finding(self) -> bool:
        """A surviving *and* directionally-resolved coupling would be usable. Education⇄income survives but is
        directionally ambiguous, so it is **not** a reliable finding — necessary-but-not-sufficient made concrete."""
        return self.within_survives and not self.directionally_ambiguous

    def verdict(self) -> str:
        if not self.within_survives:
            return "no within covariation"
        if self.directionally_ambiguous:
            return "survives but DIRECTIONALLY AMBIGUOUS (not a reliable finding — the instrument's 2nd limit)"
        return "survives with a resolved direction"


def run_education_directionality() -> DirectionalityResult:
    """Run the education⇄income directional stress test: contemporaneous within-FE correlation, out-of-sample
    within-prediction, and the two within-country lead-lag correlations. Demonstrates that a surviving
    within-correlation does not by itself establish a direction when causation is bidirectional."""
    fe = run_education_panel()
    iso, year, log_gdppc, sec = load_real_education_panel()
    return DirectionalityResult(
        within_corr=fe.within_corr,
        oos_within_corr=oos_within_prediction(iso, year, log_gdppc, sec),
        lead_school_to_income=within_leadlag(sec, log_gdppc, iso, year, k=1),
        lead_income_to_school=within_leadlag(log_gdppc, sec, iso, year, k=1),
    )


def boundary_summary() -> str:
    """One honest line on the instrument's second limit — a surviving correlation is not a directional claim."""
    r = run_education_directionality()
    return (
        f"Education⇄income: within {r.within_corr:+.2f} survives and forecasts (OOS {r.oos_within_corr:+.2f}), "
        f"but lead-lag is symmetric — schooling→income {r.lead_school_to_income:+.2f} vs income→schooling "
        f"{r.lead_income_to_school:+.2f}. A surviving within-correlation is necessary but NOT sufficient for a "
        f"directional claim; not promoted to a reliable finding."
    )
