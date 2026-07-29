"""What the instrument can *reliably* tell a decision-maker (Iter 56) — the honest positive output.

The failure-mode field guide catalogues what Polyphony **cut**. This is its complement: of everything
tested, the short list of relationships that **survived real validation** and are therefore usable to inform
a policy choice. Four — each backed by a validated experiment, not asserted:

- **Energy prices → inflation** (aggregate forecast): the sole aggregate coupling that beats every baseline
  and naive out of sample, robust to a red team and confirmed at quarterly frequency. Central-bank-relevant.
- **Income → life expectancy** (the Preston curve, cross-country panel): a within-country mechanism that
  survives two-way fixed effects *and* forecasts held-out years. Development-policy-relevant.
- **Income → fertility** (the demographic transition, panel): likewise survives FE and forecasts.
- **Income → absolute poverty** (the $2.15/day headcount, panel): the strongest within-country survivor —
  growth is a validated lever on *absolute* poverty (but *not* on *relative* inequality, which is cut; the
  two must not be conflated). Development- and welfare-policy-relevant.

Everything else tested was **cut**, honestly, for a named reason. The point of listing the survivors
separately is decision-support hygiene: a policymaker should know not only that most plausible couplings
don't hold, but *exactly which few do* — and use only those. (Macro⇄Health is a keep on *synthetic* data
with an underpowered real test, so it is deliberately **excluded** here: not reliable enough to act on.)
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ReliableFinding:
    relationship: str
    kind: str  # "aggregate forecast" | "panel mechanism"
    evidence: str
    policy_relevance: str


RELIABLE_FINDINGS: tuple[ReliableFinding, ...] = (
    ReliableFinding(
        "Energy prices → inflation",
        "aggregate forecast",
        "beats every baseline + naive across walk-forward folds; survives a red team; confirmed quarterly; calibrated",
        "how much of inflation is energy-driven, and how far ahead energy shocks forecast it (~1 year)",
    ),
    ReliableFinding(
        "Income → life expectancy (Preston curve)",
        "panel mechanism",
        "positive within-country correlation under two-way fixed effects (+0.13, 252 countries) that forecasts held-out years",
        "income growth is a genuine lever on population health — development policy",
    ),
    ReliableFinding(
        "Income → fertility (demographic transition)",
        "panel mechanism",
        "negative within-country correlation under two-way fixed effects (−0.11, 252 countries) that forecasts held-out years",
        "income growth genuinely lowers fertility — population and development policy",
    ),
    ReliableFinding(
        "Income → absolute poverty ($2.15/day headcount)",
        "panel mechanism",
        "strong negative within-country correlation under two-way fixed effects (−0.48, 121 countries) that forecasts held-out years (OOS +0.58)",
        "growth is a validated lever on absolute poverty (but NOT on relative inequality, which is cut) — development and welfare policy",
    ),
)


def reliable_findings() -> tuple[ReliableFinding, ...]:
    """The validated, usable relationships — the honest positive output of the whole exercise."""
    return RELIABLE_FINDINGS


def n_reliable() -> int:
    return len(RELIABLE_FINDINGS)
