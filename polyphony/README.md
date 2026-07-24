# Polyphony

**A paradigm-plural, adversarially-validated policy simulation ensemble.**

> Polyphony is a decision-support instrument that couples the modeling traditions
> catalogued in the [Atlas of Computational Policy Simulation](../README.md) into one
> executable system — and **reports their disagreement as first-class signal** rather
> than averaging it into a single confident number. It is **not** a world model, an
> oracle, or a faithful replica of reality. See
> [related-work](../docs/polyphony/related-work.md) for how it differs from Destination
> Earth, the IAM family, and ML/LLM "world models."

## What it is (the contribution is a *method*, not a claim of fidelity)

1. **Paradigm-plural** — rival traditions (optimization, equilibrium, agent-based,
   system-dynamics, econometric, …) are kept as **distinct voices**, not fused into one.
2. **Disagreement is signal** — where paradigms overlap we run **both** and **report the
   spread**; consensus and dissent are both outputs.
3. **Adversarial selection** — features, couplings, and models survive by **beating rivals
   against real data** in a tournament, not by clearing a fixed threshold; a **Red Team**
   tries to break the champion.
4. **Synergy is a falsifiable bet** — cross-domain couplings must **out-predict the
   sum of isolated parts** on real data or they are cut. "Integration adds no synergy
   here" is an acceptable, publishable finding.
5. **Values are exposed, not buried** — welfare/equity is an **inspectable
   multi-objective dial** (Pareto frontiers, value-of-information), never a hidden constant.

## Layout

- `polyphony/` — the Python package (common model interface, orchestrator, tournament,
  engines-as-code). *Scaffolded in Phase 2.*
- `../docs/polyphony/` — living documentation surfaced in MkDocs: inventory, blueprint,
  research, validation, **leaderboard**, **PROGRESS** (iteration log), related-work.
- `../docs/decisions/` — Architecture Decision Records (ADRs).

## Status

Phase 0 (Scout, Inventory & Position). See
[`docs/polyphony/PROGRESS.md`](../docs/polyphony/PROGRESS.md) for the iteration log and
[`docs/polyphony/00-inventory.md`](../docs/polyphony/00-inventory.md) for the atlas
inventory that grounds the design.

## Design thesis (inherited from the atlas)

Make every contested assumption a **dial** · **route** each question to the paradigm where
it is valid · where paradigms **overlap, run both and report the disagreement** · **expose
contested values** rather than hard-coding them.
