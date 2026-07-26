# ADR-0005: Resolve acyclic couplings contemporaneously; lag only to break cycles

- **Status:** Accepted
- **Date:** 2026-07-26
- **Deciders:** Polyphony build loop (Research Lab)
- **Phase:** 7

## Context

The [Orchestrator](../polyphony/02-scaffold.md) couples voices with a **recursive (lagged,
Gauss–Seidel)** bus: each step, every voice reads the shared bus, advances, and writes its outputs,
which become inputs **next** step. Lagging is *necessary* when the coupling has a **cycle** (A needs B
and B needs A) — you must break the loop with a one-step delay.

But many Polyphony couplings are **acyclic** feed-forward chains: energy → climate → land
(emissions → temperature → food price). Lagging *every* hop there inserts a **spurious delay** — the
land voice reads a temperature that is one (here two) steps stale. Iter 13 kept the Land⇄Climate⇄Food
coupling as **real** (Δ +15 survives a fair calibration) yet found the champion **loses to naive**
(MASE 2.87). Iter 14 diagnosed why: with the driver assimilated to its true value
(`estimate_yield_sensitivity` recovers ys = 0.1) the early track was still delayed by the bus lag — a
**method artifact**, not a modeling error.

## Decision

Add an **opt-in** `resolve="contemporaneous"` mode to `Orchestrator.run`. It topologically sorts the
voices by the routing DAG (producer before consumer) and resolves them **in order within each step**,
so a downstream voice reads upstream outputs **produced this same step** — no delay. If the routing
contains a **cycle**, contemporaneous resolution **raises**, and the caller must use the default
`resolve="lagged"`. Lagged remains the **default**, so no existing result changes unless explicitly
opted in.

## Consequences

- The land champion's **coupling lag is removed** (the first-step price now moves with warming instead
  of sitting at base). This is a correct, general improvement wherever a coupling is acyclic.
- **Honest limit, reported:** removing the lag does **not** by itself make the land champion beat naive
  (calibrated MASE stays ≈ 2.87). With the parameter already right (assimilation) and the lag now gone,
  the **residual is a structural mismatch** between the reduced-form energy/climate voices' tail
  dynamics and the target — resolvable only with **real data / richer voices** (issue #9), **not** by
  tuning the toy voices to their own synthetic generator (which would be dishonest skill-inflation).
  See [leaderboard Round 9](../polyphony/leaderboard.md) and [validation](../polyphony/04-validation.md).
- Cyclic couplings (genuine two-way feedback) are unaffected and still lagged — the mode guards this by
  refusing to run.
- Falsification/revisit trigger: if a within-step **fixed-point iteration** (not just topological order)
  is later shown to improve skill on cyclic couplings without instability, revisit with a new ADR.

## Alternatives considered

- **Make contemporaneous the default** — rejected: it changes every existing tournament result silently
  and is undefined for cyclic couplings; opt-in keeps prior results reproducible.
- **Hand-roll a no-lag forward map per experiment** — rejected: duplicates the coupling logic outside
  the orchestrator and drifts from the voices; a first-class solver mode is auditable and reusable.
- **Tune the reduced-form voices to the synthetic DGP** to beat naive — rejected as **dishonest**:
  fitting a model to its own synthetic generator manufactures skill that would not survive real data.

## Links

- [ADR-0001](0001-positioning-paradigm-plural-not-world-model.md) ·
  [01-blueprint.md §3 coupling](../polyphony/01-blueprint.md) · [leaderboard](../polyphony/leaderboard.md)
- Atlas: [Integration Engine](../patterns/integration-engine.md) ·
  [Data-Assimilation Engine](../patterns/data-assimilation-engine.md)
