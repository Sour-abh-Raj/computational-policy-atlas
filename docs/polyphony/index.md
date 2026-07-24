# Polyphony

**A paradigm-plural, adversarially-validated policy simulation ensemble** — built on the
[Atlas of Computational Policy Simulation](../index.md).

!!! abstract "What Polyphony is (and is not)"
    Polyphony couples the modeling traditions catalogued in the atlas into one executable
    system for policy testing, and **reports their disagreement as first-class signal**
    rather than averaging it into a single confident number. It is a **decision-support
    instrument**, not a "world model," an oracle, or a faithful replica of reality. See
    **[related work](related-work.md)** for how it differs from Destination Earth, the IAM
    family, and ML/LLM "world models," and **[ADR-0001](../decisions/0001-positioning-paradigm-plural-not-world-model.md)**
    for the positioning decision.

## The north star

Help humans choose better, more **altruistic** policies by simulating their consequences
as **accurately AND as honestly** as we can — foregrounding uncertainty, disagreement
between modeling traditions, and welfare/equity effects rather than hiding them behind one
number.

## The method (the actual contribution)

1. **Paradigm-plural** — rival traditions are kept as **distinct voices**.
2. **Disagreement is signal** — overlapping paradigms are run **both** and their **spread
   reported**.
3. **Adversarial selection** — features, couplings, and models survive by **beating rivals
   on real data** and **surviving red-team attack**, not by clearing a fixed threshold.
4. **Falsifiable synergy** — a coupling is kept only if the **coupled ensemble out-predicts
   the sum of isolated parts**; "no synergy" is an acceptable, publishable finding.
5. **Exposed values** — welfare/equity is an **inspectable multi-objective dial**.

## Design thesis (inherited from the atlas)

> Make every contested assumption a **dial** · **route** each question to the paradigm where
> it is valid · where paradigms **overlap, run both and report the disagreement** · **expose
> contested values** rather than hard-coding them.

## Documents

| Page | What it is |
|------|-----------|
| [00 — Inventory](00-inventory.md) | The atlas as raw material: models, dials, engines, couplings, gaps |
| [Related work](related-work.md) | Positioning vs DestinE, IAMs, ML/LLM world models |
| [Leaderboard](leaderboard.md) | Every tournament: contenders, metrics, why the winner won |
| [PROGRESS](PROGRESS.md) | The iteration log (append-only, `Iter NN`) |
| [Decisions (ADRs)](../decisions/index.md) | The audit trail of design choices |

## Phase map

- **Phase 0 — Scout, Inventory & Position** *(in progress)* — read the atlas; produce the
  inventory and related-work; open gap issues.
- **Phase 1 — Blueprint & Wireframes** — architecture as atlas engines; common model
  interface; coupling/routing/disagreement strategy; tournament protocol.
- **Phase 2 — Scaffold** — the `polyphony/` package: interface, orchestrator, tournament,
  a 2–3 model vertical slice.
- **Phase 3 — Research & compete** — race candidate features and couplings.
- **Phase 4 — Validate & attack** — backtest on real data, measure synergy, red-team.
- **Phase 5+ — Scale** — family by family, to a validated, tournament-converged,
  synergy-positive ensemble.
