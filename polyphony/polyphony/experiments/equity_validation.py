"""The first *equity* (distributional) outcome to face the bar (Iter 57) — income → inequality (Kuznets).

Every validated finding before this one concerns a **mean** outcome — life expectancy, fertility, inflation,
GDP. Yet the north star is about *altruistic* policy and *welfare/equity* effects, i.e. **who gets what**, not
just the average. That half of the mission had been *exposed as a dial* (see ``welfare_frontier``) but never
**validated on real distributional data**. This module closes that gap by putting the classic optimistic
development claim — *growth reduces inequality* — through the identical instrument that separated the panel
survivors from the confounded couplings: two-way (country + year) fixed effects plus an out-of-sample
within-country test.

The honest result is a **cut**, and an instructive one:

- **Pooled (cross-country):** income and the Gini index correlate *negatively* — richer countries are more
  equal. Taken at face value this looks like the optimistic story confirmed.
- **Within (two-way FE):** the correlation **collapses to ≈0** (even turns slightly positive) — ~80% of the
  pooled association is a between-country level artifact. As a given country grows, its inequality does **not**
  reliably fall.
- **Out-of-sample:** the within-country prediction has ≈0 correlation with held-out Gini — no forecasting skill.

So the belief "grow the economy and inequality takes care of itself" is an inference from comparing *different
countries*, not from what happens *within* one over time — consistent with the modern inequality literature
(Deininger–Squire 1998 on the fragility of the within-country Kuznets curve; Piketty 2014 and Milanovic 2016 on
within-country inequality often *rising* through growth episodes). For a decision-maker this is decision-support
hygiene on the equity dimension: **growth is not a reliable within-country lever on inequality**, so a distinct
distributional instrument (transfers, tax design) is needed — the growth dial alone will not deliver it.

It also **sharpens the two-domain epistemology**: the panel domain is not uniformly signal-rich. Genuine *mean*
mechanisms (Preston, demographic transition) survive fixed effects, but the *distributional* outcome is
confounded-away just like the aggregate couplings — the survivability of a panel coupling depends on the
**outcome**, not merely on being cross-sectional.
"""

from __future__ import annotations

from dataclasses import dataclass

from .panel_validation import oos_within_prediction, run_inequality_panel
from ..data.loaders import load_real_inequality_panel


@dataclass(frozen=True)
class EquityFinding:
    question: str
    optimistic_claim: str
    pooled_corr: float
    within_corr: float
    oos_within_corr: float
    verdict: str
    lesson: str

    @property
    def is_cut(self) -> bool:
        """A cut: the within-country distributional effect neither survives FE nor forecasts."""
        return abs(self.within_corr) < 0.1 and abs(self.oos_within_corr) < 0.1

    @property
    def pooled_is_optimistic(self) -> bool:
        """The pooled (cross-country) correlation has the hopeful sign (income up → inequality down)."""
        return self.pooled_corr < 0


def run_inequality_equity_test() -> EquityFinding:
    """Run the income→inequality (Kuznets) coupling through the panel-survivor instrument and report the
    honest equity verdict. The first *distributional* outcome to face the real-data / FE / out-of-sample bar."""
    fe = run_inequality_panel()
    iso, year, log_gdppc, gini = load_real_inequality_panel()
    oos = oos_within_prediction(iso, year, log_gdppc, gini)
    return EquityFinding(
        question="Does income growth reduce inequality *within* a country?",
        optimistic_claim="growth reduces inequality (income↑ → Gini↓)",
        pooled_corr=fe.pooled_corr,
        within_corr=fe.within_corr,
        oos_within_corr=oos,
        verdict=fe.verdict(),
        lesson=(
            "The optimistic 'growth fixes inequality' story is a between-country level artifact: rich "
            "countries are more equal, but a country growing does not reliably become more equal. Growth is "
            "not a within-country lever on distribution — a separate instrument (transfers, tax) is needed."
        ),
    )


def equity_dimension_summary() -> str:
    """One honest line on the state of the welfare/equity dimension — its first validated result is a cut."""
    f = run_inequality_equity_test()
    return (
        f"Equity dimension — first distributional outcome tested (income→inequality): "
        f"pooled {f.pooled_corr:+.2f} (optimistic), within {f.within_corr:+.2f}, OOS {f.oos_within_corr:+.2f} "
        f"⇒ {f.verdict}. Growth is not a within-country lever on inequality."
    )
