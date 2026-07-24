# ADR-0004: Disagreement-preservation as the default combiner; BMA as a challenger

- **Status:** Accepted
- **Date:** 2026-07-24
- **Deciders:** Polyphony build loop (Research Lab)
- **Phase:** 1

## Context

When several paradigm voices answer the same quantity, Polyphony must decide how to **combine** them.
The obvious default from the forecasting literature is **Bayesian Model Averaging (BMA)** — weight
each model by posterior probability and report the mixture, collapsing disagreement into a single
predictive distribution. But Polyphony's entire premise (ADR-0001) is that **disagreement between
modeling traditions is signal**, not noise to average away: when a CGE says a carbon tax costs GDP
and E3ME says it pays, the *fact of the disagreement and its driver* is often more decision-relevant
than any blended number.

## Decision

The **default combiner preserves disagreement**: for each quantity it reports the **full set** of
voice answers, their skill-weighted spread, a **disagreement index** $D$, and an **attribution** of
$D$ to the dial(s) driving the split (see [blueprint §4](../polyphony/01-blueprint.md#4-coupling-routing-and-run-both-report-disagreement)).
Consensus is reported where voices agree; dissent is reported where they don't.

**BMA is not banned — it is a challenger.** We implement BMA (and simple skill-weighted averaging) as
**alternative combiners** and put them in the **tournament** against disagreement-preservation on real
data, per question. Where a *single predictive distribution* is what the decision needs and a combiner
demonstrably improves out-of-sample skill/calibration without hiding a decision-relevant split, it may
win **for that question**. The choice of combiner is thus itself **routed and evidence-based**, never
assumed.

## Consequences

- The product's headline output is a **distribution-with-disagreement**, matching the honesty
  commitment and the north star.
- We must build $D$, its attribution, and disagreement-fidelity metrics — and a UI/report that shows
  spread first ([Visualization engine](../patterns/visualization-engine.md), disagreement-first).
- Risk: decision-makers sometimes *want* one number. Mitigated by offering combiners **as an explicit,
  logged choice** with their skill/calibration shown — and by always surfacing what was averaged over.
- Falsification/revisit trigger: if, across many questions, a combiner robustly beats
  disagreement-preservation on decision-relevant metrics *without* masking splits, promote it to
  default for those question classes (new ADR).

## Alternatives considered

- **BMA as default** — rejected as default: collapses the signal we exist to surface; retained as a
  tournament entrant.
- **Pick-one-best-model per question** — rejected: throws away the plurality; but "route to the valid
  voice(s)" already narrows the set before combining.
- **Naive mean/median ensemble** — included only as a baseline for the tournament.

## Links

- [ADR-0001](0001-positioning-paradigm-plural-not-world-model.md) ·
  [01-blueprint.md §4, §7](../polyphony/01-blueprint.md) · [leaderboard](../polyphony/leaderboard.md)
- Atlas: [Bayesian Decision](../paradigms/algorithms/bayesian-decision.md) ·
  [Sensitivity Engine](../patterns/sensitivity-engine.md)
