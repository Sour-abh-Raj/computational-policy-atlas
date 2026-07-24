# Polyphony — iteration log

Append-only. One `Iter NN` entry per loop iteration, mirroring the atlas log. Tracks the
walk from Phase 0 (inventory) to a validated, tournament-converged, synergy-positive ensemble.

## Definition of Done (the convergence criterion)

The loop completes when **both** hold, across all covered domains:

- **Competition converged** — a stable champion (feature set + couplings + routed models) that
  **no** challenger feature, coupling, method, or **red-team** attack can beat within a full
  tournament round on real data.
- **Synergy-positive** — the coupled ensemble **out-predicts the sum of isolated parts** on real
  historical data (net positive synergy), or every retained coupling is individually
  synergy-justified and non-synergistic ones are cut.

Plus the standing invariants (every commit): `mkdocs build --strict` green · `graph.json` valid &
0-dangling · Polyphony package typed with tests green · positioning honesty preserved (no
"world model" claims).

## Phase gates

- **P0** Scout, Inventory & Position · **P1** Blueprint & Wireframes · **P2** Scaffold (vertical
  slice) · **P3** Research & compete · **P4** Validate & attack · **P5+** Scale to full validation.

## Log

- **Iter 01 — Kickoff + Phase 0 underway.** Established the GitHub collaboration scaffolding and
  the Phase-0 deliverables:
  - **Scaffolding:** `polyphony/` top-level package (README, `pyproject.toml`, `polyphony/__init__.py`);
    root `CONTRIBUTING.md`; `.github/` PR template + 3 issue templates (synergy-hypothesis,
    model-adapter, gap-or-extension); `docs/decisions/` ADR folder (index + template).
  - **ADR-0001** — Positioning: a paradigm-plural ensemble, **not** a world model (bans
    overclaiming language; commits to plurality, disagreement-as-signal, adversarial validation,
    falsifiable synergy, exposed values).
  - **ADR-0002** — Repo layout (code at `polyphony/`, docs at `docs/polyphony/`, ADRs at
    `docs/decisions/`) + autonomous-loop trunk-based flow behind a green gate; keeps
    `mkdocs build --strict` green with no extra plugin.
  - **Phase 0 docs:** `docs/polyphony/index.md`; **`00-inventory.md`** (atlas reduced to
    models/state/paradigm, 11 dials from the comparative matrices incl. the new **values dial**,
    the 16 engines as component blueprints, graph-implied couplings, 4 candidate synergy loops,
    and gaps/new-factor candidates — incl. proposed new engines: data-assimilation, surrogate,
    ensemble/meta, welfare-equity); **`related-work.md`** (positioning vs DestinE, IAMs, ML/LLM
    world models; the 4-part gap Polyphony fills); **`leaderboard.md`** + this **`PROGRESS.md`**.
  - **mkdocs nav:** added *Polyphony* and *Decisions* sections; strict build green.
  - **GitHub gap issues opened (#1–#8):** 4 new-engine gaps — **#1** data-assimilation, **#2**
    surrogate/emulator, **#3** ensemble/meta (BMA vs disagreement), **#4** welfare/equity engine;
    4 synergy hypotheses — **#5** Energy⇄Economy⇄Climate (the first vertical slice), **#6**
    Land⇄Climate⇄Water⇄Food, **#7** Urban⇄Transport⇄Energy⇄Health, **#8** Macro⇄Health. Labels
    created (synergy/gap/engine/research/phase-\*/needs-evidence). **Phase 0 deliverables complete.**
- **Iter 02 — 🎉 Phase 1 COMPLETE (Blueprint & Wireframes).** Wrote
  **[`01-blueprint.md`](01-blueprint.md)** — the full engineering design expressed **as the atlas's
  16 engines**, with committed Mermaid diagrams: (1) architecture across data/model/core/decision/
  selection planes (naming the 4 `＊new` engines — assimilation, surrogate, welfare/equity, ensemble/
  meta — from issues #1–#4); (2) the **common `Model` interface** (state·step·dials·provenance) as a
  paradigm-agnostic Python `Protocol`, with foresight handled as a *property* not a baked-in
  assumption, and mandatory provenance; (3) the **model⇄assimilation⇄control** backbone; (4)
  **routing + run-both + report-disagreement** with a defined **disagreement index D** and dial-
  attribution; (5) the **welfare/equity multi-objective dial** (SWF/inequality-aversion/discount/
  tail-risk as inspectable dials → Pareto frontier + VoI); (6) Bayesian + structural uncertainty
  propagation; (7) the **tournament + synergy-Δ + Red-Team** protocol with metrics (CRPS/MASE,
  calibration/PIT, synergy = coupled − best sum-of-parts) and the convergence/DONE criterion; (8)
  feature-engineering plan; (9) package layout; (10) phase plan with **automated acceptance gates**.
  Plus **ADR-0003** (tech stack: Python ≥3.11, numpy/pandas/scipy core, Protocol typing, YAML dials,
  hand-rolled assimilation/surrogate first with library challengers behind extras, no commercial
  solver in core) and **ADR-0004** (disagreement-preservation is the **default combiner**; BMA and
  skill-weighted averaging are **tournament challengers**, routed per question). Nav + decisions index
  updated; strict build green.
  - **Next (Iter 03 → Phase 2):** turn the blueprint into code — scaffold
    `polyphony/polyphony/core/` (`interface.py` common `Model` Protocol, `orchestrator.py`,
    `combiner.py` with the disagreement index D, `provenance.py`, `dials.py`) with `pytest`/`ruff`/
    `mypy` green, plus `tools/validate_graph.py` as the 0-dangling gate. Then begin adapters for the
    **DICE ⇄ energy (reduced-form LP) ⇄ CGE** vertical slice (reduced-form, faithful, fidelity limits
    stated) and a golden end-to-end coupled-scenario integration test.
