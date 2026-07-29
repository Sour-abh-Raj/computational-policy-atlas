"""The welfare/**equity** dimension, held to the same bar (Iters 57–58) — the honest, nuanced answer.

Every validated finding before this concerned a **mean** outcome — life expectancy, fertility, inflation,
GDP. Yet the north star is about *altruistic* policy and *welfare/equity* effects, i.e. **who gets what**, not
just the average. That half of the mission had been *exposed as a dial* (see ``welfare_frontier``) but never
**validated on real distributional data**. This module closes that gap by putting the two classic optimistic
claims about growth and welfare through the identical instrument that separated the panel survivors from the
confounded couplings — two-way (country + year) fixed effects plus an out-of-sample within-country test.

The result is a sharp **relative-vs-absolute split**, not a slogan:

- **Income → *relative* inequality (Kuznets):** a **cut**. Pooled cross-country correlation is optimistic
  (−0.35, richer countries more equal), but ~80% is a between-country level artifact — within a country the
  effect collapses to ≈0 and forecasts nothing. Growth is **not** a within-country lever on the *distribution*
  (Deininger–Squire 1998; Piketty 2014; Milanovic 2016 — inequality often *rises* through growth).
- **Income → *shared prosperity* (bottom-40% income share):** also a **cut**, and the point of testing it — a
  *second, independent* relative measure (the World Bank's official shared-prosperity population). Pooled
  +0.32 (optimistic), within −0.06, ~80% attenuation, no out-of-sample skill. The relative/absolute split is
  therefore **not an artifact of the Gini metric**: measured either way, the *relative* distribution is
  confounded-away within countries.
- **Income → *absolute* poverty (the $2.15/day headcount):** a **survivor**, and the strongest of any panel.
  Pooled −0.72, two-way-FE within **−0.48** (only ~34% attenuation), out-of-sample within-prediction **+0.58**.
  Growth **is** a strong, validated within-country lever on *absolute* poverty (Dollar–Kraay 2002).

**The honest welfare message for a decision-maker:** growth reliably lifts people out of *absolute* poverty but
does **not** compress the *relative* distribution (by either of two measures). Both facts matter for altruistic
policy, and conflating them (the common "a rising tide lifts all boats" elision of poverty with inequality) is
exactly the error this instrument catches. Absolute-poverty reduction can lean on the growth dial; relative
equity needs its own instrument (transfers, tax design).

It also **sharpens the two-domain epistemology**: the panel domain is not uniformly signal-rich. Survivability
depends on the **outcome** — a genuine *within-unit mechanism* (poverty tracks income almost mechanically)
survives; a *confounded distributional* outcome (inequality, shared-prosperity share) does not, exactly like
the aggregate couplings.
"""

from __future__ import annotations

from dataclasses import dataclass

from .panel_validation import (
    oos_within_prediction,
    run_inequality_panel,
    run_poverty_panel,
    run_shared_prosperity_panel,
)
from ..data.loaders import (
    load_real_inequality_panel,
    load_real_poverty_panel,
    load_real_shared_prosperity_panel,
)


@dataclass(frozen=True)
class EquityFinding:
    question: str
    optimistic_claim: str
    assumed_sign: int  # +1 or −1 (the sign the optimistic claim predicts for the within effect)
    pooled_corr: float
    within_corr: float
    oos_within_corr: float
    verdict: str
    lesson: str

    @property
    def is_cut(self) -> bool:
        """A cut: the within-country effect neither survives FE nor forecasts."""
        return abs(self.within_corr) < 0.1 and abs(self.oos_within_corr) < 0.1

    @property
    def is_survivor(self) -> bool:
        """A survivor: the within effect has the assumed sign, is non-trivial, and forecasts out of sample."""
        within_right = (self.within_corr > 0) == (self.assumed_sign > 0) and abs(self.within_corr) > 0.1
        return within_right and abs(self.oos_within_corr) > 0.1

    @property
    def pooled_is_optimistic(self) -> bool:
        """The pooled (cross-country) correlation has the hopeful sign the optimistic claim predicts."""
        return (self.pooled_corr > 0) == (self.assumed_sign > 0)


def run_inequality_equity_test() -> EquityFinding:
    """Income → *relative* inequality (Kuznets): the distributional claim that growth compresses the
    distribution. On real data this is a **cut** — confounded-away within countries."""
    fe = run_inequality_panel()
    iso, year, log_gdppc, gini = load_real_inequality_panel()
    oos = oos_within_prediction(iso, year, log_gdppc, gini)
    return EquityFinding(
        question="Does income growth reduce *relative* inequality *within* a country?",
        optimistic_claim="growth reduces inequality (income↑ → Gini↓)",
        assumed_sign=-1,
        pooled_corr=fe.pooled_corr,
        within_corr=fe.within_corr,
        oos_within_corr=oos,
        verdict=fe.verdict(),
        lesson=(
            "The optimistic 'growth fixes inequality' story is a between-country level artifact: rich "
            "countries are more equal, but a country growing does not reliably become more equal. Relative "
            "equity is not a within-country function of growth — it needs its own instrument (transfers, tax)."
        ),
    )


def run_poverty_equity_test() -> EquityFinding:
    """Income → *absolute* poverty (the $2.15/day headcount): the claim that growth lifts people out of
    absolute poverty. On real data this is a **survivor** — the strongest within-FE effect of any panel."""
    fe = run_poverty_panel()
    iso, year, log_gdppc, poverty = load_real_poverty_panel()
    oos = oos_within_prediction(iso, year, log_gdppc, poverty)
    return EquityFinding(
        question="Does income growth reduce *absolute* poverty *within* a country?",
        optimistic_claim="growth reduces absolute poverty (income↑ → $2.15/day headcount↓)",
        assumed_sign=-1,
        pooled_corr=fe.pooled_corr,
        within_corr=fe.within_corr,
        oos_within_corr=oos,
        verdict=fe.verdict(),
        lesson=(
            "Absolute poverty falls strongly within countries as income grows, and the effect forecasts "
            "held-out years — growth IS a validated within-country lever on absolute poverty (Dollar–Kraay). "
            "The complement to the inequality cut: the tide lifts boats OUT of poverty, without levelling them."
        ),
    )


def run_shared_prosperity_equity_test() -> EquityFinding:
    """Income → *shared prosperity* (bottom-40% income share): a second *relative* distributional measure. On
    real data this is a **cut**, like inequality — confirming the relative/absolute split is not a Gini artifact."""
    fe = run_shared_prosperity_panel()
    iso, year, log_gdppc, share = load_real_shared_prosperity_panel()
    oos = oos_within_prediction(iso, year, log_gdppc, share)
    return EquityFinding(
        question="Does income growth raise the bottom-40% income *share* *within* a country?",
        optimistic_claim="growth raises the poorest 40%'s share (income↑ → bottom-40 share↑)",
        assumed_sign=+1,
        pooled_corr=fe.pooled_corr,
        within_corr=fe.within_corr,
        oos_within_corr=oos,
        verdict=fe.verdict(),
        lesson=(
            "A second, independent relative measure (the World Bank's shared-prosperity population) is also "
            "confounded-away within countries — so 'growth is not a within-country lever on relative "
            "distribution' is not an artifact of the Gini metric; it holds however relative equity is measured."
        ),
    )


def equity_dimension() -> tuple[EquityFinding, EquityFinding, EquityFinding]:
    """All three equity results: the *relative-inequality* cut, the *shared-prosperity-share* cut (a second
    relative measure), and the *absolute-poverty* survivor."""
    return run_inequality_equity_test(), run_shared_prosperity_equity_test(), run_poverty_equity_test()


def equity_dimension_summary() -> str:
    """One honest line on the welfare/equity dimension — growth cuts absolute poverty but not relative inequality."""
    ineq, share, pov = equity_dimension()
    return (
        f"Equity dimension: absolute poverty SURVIVES (within {pov.within_corr:+.2f}, OOS "
        f"{pov.oos_within_corr:+.2f}) — growth is a within-country lever on absolute poverty; but BOTH relative "
        f"measures are CUT — inequality (within {ineq.within_corr:+.2f}) and shared-prosperity share (within "
        f"{share.within_corr:+.2f}) — growth does not compress the distribution. Both matter; do not conflate them."
    )
