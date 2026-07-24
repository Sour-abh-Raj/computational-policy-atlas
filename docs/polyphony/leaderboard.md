# Leaderboard — every competition, recorded

Polyphony selects by **adversarial competition against real data**, never by clearing a fixed
threshold. This page is the running record of **every tournament**: the contenders, the metric,
the out-of-sample / holdout / distribution-shift result, and **why the winner won**. A feature,
coupling, model, or method is only "in" if it appears here as a **winner over named rivals** — and
it can be **dethroned** by a later challenger or a red-team break.

!!! info "Reading a row"
    Each contest records: **question** (what is being predicted/decided), **contenders**,
    **data & split** (dataset, train/test window, shift test), **metric(s)**, **winner**,
    **margin**, **why**, **red-team status**, and a link to the eval script + ADR.

## Standing champions

| Question / slice | Champion | Beat | On (data, split) | Synergy vs sum-of-parts | Red-team | Ref |
|------------------|----------|------|------------------|-------------------------|----------|-----|
| _none yet — Phase 0_ | — | — | — | — | — | — |

## Contest log

### Round 0 — (Phase 0)
No tournaments have run yet. Phase 0 is inventory & positioning. The **first contests**
(Phase 3–4) will race:

1. **Feature competition** — candidate features/transformations for the DICE⇄energy⇄CGE slice,
   scored on out-of-sample backtests with overfitting/leakage/redundancy penalties.
2. **Coupling/synergy competition** — coupled configurations vs decoupled baselines vs rival
   couplings; a coupling advances only if it adds **demonstrable synergy** on real data.
3. **Model/method competition** — rival paradigm voices head-to-head on the same question; route
   to winners; where winners disagree, **keep both and report the disagreement**.
4. **Ensembling competition** — Bayesian model averaging **vs** deliberate disagreement-preservation.

Each will be logged here with full provenance so any collaborator can reproduce and challenge it.

## Convergence criterion (the DONE state)

A **stable champion** that no challenger feature, coupling, method, or red-team attack can beat
within a full tournament round — competition **converged** — **and** net positive synergy over
isolated baselines on real data, across all covered domains. Until then, the loop continues.
