# IWM — Autonomous Loop Prompt

Paste this into the loop. It is written to run inside **this repo**
(`model-policy`, the Atlas of Computational Policy Simulation) and to reuse the
atlas's existing conventions as the simulator's scaffolding.

---

```
# PROJECT: Integrated World Model for Policy Simulation (IWM)
# NORTH STAR: Build the most accurate, honest, welfare- and altruism-generating
# policy simulator we can — a tool that helps humans choose better policies for a
# better world, and that is transparent about its own uncertainty and limits.
#
# MODE: Autonomous loop. Run until a fully validated, tournament-converged,
# synergy-positive world model is achieved. Do NOT stop for my approval between
# phases. Self-review at each gate and proceed on your own judgment. Only halt on a
# hard external blocker (missing credentials, data with no substitute) — and even
# then, log it, open a GitHub issue, work around it, and keep going on everything
# else. Append an "Iter NN" entry to PROGRESS.md after every iteration, exactly like
# the existing atlas log.

## 0. Load the ground truth first (do NOT skip, do NOT invent)
You are working inside the completed **Atlas of Computational Policy Simulation**.
Read it before you plan. It IS your design foundation:
- `README.md`, `PROGRESS.md` (the full iteration history + Definition of Done),
  `mkdocs.yml` (site structure), `docs/foundations/` (taxonomy, dossier template,
  the **Three-Track method**: Scholar / Engineer / Architect).
- `docs/model-families/**` — ~50 model dossiers across Climate/IAM, Energy,
  Economics, Transport, Health, Frameworks, Agriculture, Water, Urban.
- `docs/paradigms/algorithms/**` — 14 method pages (LP, MILP, DP, optimal-control,
  RL, multi-objective, Bayesian-decision, digital-twins, …).
- `docs/patterns/**` — **16 architecture "Engine" patterns**
  (integration, market, energy-dispatch, land, climate, behavior, spatial,
  optimization, calibration, validation, sensitivity, scenario, policy,
  technology-adoption, data-pipeline, visualization). THESE ARE YOUR COMPONENT
  BLUEPRINTS — the IWM is built by instantiating these engines as real, coupled
  code.
- `docs/comparative/**` — the contested-axis matrices (ABM↔CGE, equilibrium↔
  disequilibrium, optimization↔simulation, top-down↔bottom-up, …). THESE ARE YOUR
  DIALS — every contested assumption they name must become a switchable parameter.
- `docs/graph/graph.json` — the typed knowledge graph (164 nodes, 444 edges).
  Schema: nodes `{id,type,label,maturity,page}`; edges `{s,r,t}` (source, relation,
  target); `node_types` and `edge_types` enumerated in `meta`. Keep it valid and
  0-dangling as you grow it.

Design thesis of the atlas, which the IWM MUST inherit:
  1. Make every contested modeling assumption a switchable DIAL.
  2. ROUTE each question to the paradigm where it is valid.
  3. Where paradigms OVERLAP, run BOTH and REPORT THE DISAGREEMENT.
  4. Expose contested VALUES rather than hard-coding them (Pareto frontiers,
     value-of-information) — the welfare/altruism objective is a first-class,
     inspectable dial, never a buried constant.

## 1. What we're building
An **Integrated World Model (IWM)**: an ensemble that composes and EXTENDS the
atlas's models into one coupled, executable system for policy testing and
simulation — engineered as the Digital-Twin backbone the atlas already describes
(`docs/paradigms/algorithms/digital-twins.md`): model ⇄ data-assimilation ⇄
control. It must be **validated against real historical data** (backtesting) so we
can PROVE it works, not just runs, and it must report distributional / welfare /
equity outcomes so policies can be judged for altruistic value, not GDP alone.

Where it lives: a new top-level package in this repo (e.g. `iwm/`) so the atlas
knowledge base stays intact and the simulator grows beside it. Keep the MkDocs site
as the living documentation surface — add an `iwm/` docs section and keep
`mkdocs build --strict` green (the deploy workflow fails on any broken link).

## 2. The world-model bet: synergy, not summation
We are not stapling models side by side — we are integrating them into a single
world model that behaves as an actual REPLICA of the real system. The bet is that
coupling produces **emergent synergy**: cross-domain feedbacks the standalone models
cannot capture (energy⇄climate⇄economy⇄health⇄land⇄water⇄urban loops), so the
integrated whole predicts reality better than the best combination of isolated
parts. Therefore:
- Actively HUNT for synergy: instrument every cross-domain coupling and measure
  whether the coupled system beats the sum of its parts on real data.
- Treat "integration adds no synergy" as a falsifiable hypothesis. If a coupling
  doesn't earn its keep against reality, cut it; if it does, prove why and record
  the interaction effect.
- Optimize fidelity of the WHOLE, not just per-module accuracy.

## 3. Scope is a floor, not a ceiling — research and engineer freely
The existing domains, factors, paradigms, and engines are your STARTING point, not
a limit. You have a free hand to:
- Do original **feature engineering and feature discovery** — derive, transform,
  and construct new variables, couplings, and latent factors wherever the model
  needs them to match reality.
- **Extend, add, or replace** models, domains, paradigms, engines, and couplings —
  including ones not in the atlas — when evidence supports it.
- Fold in new methods (data assimilation, ensembling, causal inference, ML/hybrid,
  agent-based, surrogate/emulator, etc.) where they improve validity.
Every extension MUST be **grounded in literature**: cite primary sources, justify
against alternatives in an ADR (`docs/decisions/`), and feed it back into the atlas
— a new dossier/method/engine page at the appropriate maturity tier
(Bronze→Silver→Gold) and new nodes/edges in `graph.json`. The knowledge base grows
WITH the model. No unsupported inventions: every added factor or coupling needs a
cited reason AND a test.

## 4. Adversarial regime — competition selects everything (no fixed thresholds)
Selection is adversarial and tournament-based at every level. Nothing is accepted
for clearing a number; things survive by BEATING rivals against real data. I do NOT
want a hard-quoted threshold — choose the BEST OF COMPETITION.
- **Feature competition:** generate many candidate features/transformations; race
  them; keep only those that win on out-of-sample, holdout, and distribution-shift
  backtests. Penalize overfitting, leakage, redundancy, and complexity.
- **Coupling / synergy competition:** pit coupled configurations against decoupled
  baselines and against each other; a coupling advances only if it demonstrably
  adds predictive synergy the alternatives don't.
- **Model & method competition:** run rival models/paradigms head-to-head on the
  same question; route to winners; where winners disagree, keep both and report the
  disagreement (design thesis #3).
- **Red-team the champion:** stand up an adversary (subagent) whose sole job is to
  BREAK the current best model — adversarial scenarios, stress and shifted data,
  edge regimes, perturbations, counterfactuals, and Lucas-critique / regime-change
  attacks on policy responses. Whatever it breaks re-enters selection. The champion
  must survive SUSTAINED attack, not a one-off test.
- **Stop condition (relative, self-adjusting):** a stable champion that no
  challenger feature, coupling, method, or red-team attack can beat within a full
  tournament round — i.e., the competition has CONVERGED — AND the champion shows
  net positive synergy over isolated baselines on real data. When both hold across
  all covered domains, the loop is DONE.

## 5. Labs (subagents) — orchestrate these yourself; they mirror the Three Tracks
- **Research Lab (Scholar)** — surveys atlas + literature, discovers/engineers
  features, justifies couplings, selects methods, designs the tournament +
  validation + synergy-measurement protocol, writes ADRs and new atlas pages.
- **Engineering Lab (Engineer)** — architecture, wireframes, the common model
  interface, engine implementations, orchestration, CI, tournament/leaderboard
  machinery.
- **Testing Lab (Architect/V&V)** — builds the validation + tournament harness,
  sources real datasets, backtests, measures synergy (coupled vs sum-of-parts),
  reports fit, calibration, welfare/equity outcomes, and disagreement.
- **Red Team** — the dedicated adversary (Section 4).

## 6. Operating rules — GitHub is the single source of truth
- Every iteration ends with commits, updated docs, and PRs. Write for the
  collaborators who will join: clear READMEs, ADRs (`docs/decisions/`), issue/PR
  templates, a CONTRIBUTING guide, and reproducible env (extend `requirements.txt`
  / add lockfiles).
- Read existing dossiers/graph/patterns first and cite them; cite external
  literature when you go beyond them. Follow the atlas citation discipline (cite
  PRIMARY sources; never commit tokens/secrets — GitHub Pages deploy is
  credential-gated, `gh auth login` by the owner only).
- Design → self-review → build. Small increments, each with automated acceptance
  checks and tournament results that YOU run and log.
- Maintain, in `iwm/docs/` (surfaced in mkdocs):
  `PROGRESS.md` (append Iter NN — reuse the existing log), `docs/decisions/` (ADRs),
  and `leaderboard.md` (every competition: contenders, metrics, why the winner won).
- Keep `mkdocs build --strict` green and `graph.json` valid/0-dangling on every
  commit — same Definition-of-Done discipline the atlas already meets.

## 7. Phases (self-gated — win your own tournaments, then continue)

### Phase 0 — Scout & Inventory
Read the entire knowledge base. Produce `iwm/docs/00-inventory.md`: every model's
I/O and state, assumptions-as-dials (from the comparative matrices), native
paradigms, the 16 engines as candidate components, couplings the graph already
implies, candidate synergy loops, gaps, and candidate NEW factors/domains worth
researching. Open GitHub issues for gaps.

### Phase 1 — Blueprint & Wireframes
`iwm/docs/01-blueprint.md` + committed diagrams (Mermaid/SVG, mkdocs-rendered):
system architecture and module boundaries expressed AS the atlas engines; a common
model interface (state, step, params/dials, provenance) so any model composes; the
model⇄data-assimilation⇄control Digital-Twin backbone; the ensemble/coupling +
paradigm-routing + run-both-report-disagreement strategy; Bayesian uncertainty
propagation; the welfare/equity objective as an explicit multi-objective dial; the
tournament + adversarial + synergy-measurement protocol; feature-engineering plan;
repo/package layout; tech-stack ADR; full phase plan with automated acceptance
tests.

### Phase 2 — Engineering Lab: scaffold
Build `iwm/`: common interface, orchestrator/ensemble harness, dials/config,
provenance logging, tournament/leaderboard machinery, red-team hooks, CI (lint +
test + `mkdocs build --strict`), and adapters for a vertical slice of 2–3
representative models from different families (e.g. DICE ⇄ an energy model ⇄ a CGE),
reusing the relevant engines. Typed, tests green.

### Phase 3 — Research Lab: justify, engineer, compete
Generate and race candidate features and couplings for the slice; document why
survivors win, data needed, failure modes, methods chosen — with citations to
dossiers + external literature. `iwm/docs/03-research.md` + ADRs + leaderboard +
new/updated atlas pages and graph nodes/edges.

### Phase 4 — Testing Lab + Red Team: validate & attack
Build the validation/tournament harness. Source real historical datasets, backtest
the coupled slice, MEASURE SYNERGY (coupled vs sum-of-parts), report fit,
calibration, welfare/equity outcomes, and disagreement, then run the red team.
Reproducible eval script + metrics dashboard + `iwm/docs/04-validation.md`. Advance
the champion that wins the round; iterate features/couplings/methods until a stable
winner emerges.

### Phase 5+ — Scale to full validation
Loop interface → research → feature-engineering → tournament → red-team,
family-by-family, extending and adding domains/engines as evidence warrants, until
the FULL integrated world model is validated against real data across all covered
domains AND demonstrates net positive synergy over isolated baselines AND its
champion survives a full tournament round of sustained red-team attack with no
challenger beating it. Keep the website's interactive graph view and `graph.json`
in sync throughout. That convergence is the DONE state.

## 8. Kickoff
Set up the GitHub collaboration scaffolding (branch strategy, issue/PR templates,
CONTRIBUTING, `docs/decisions/` ADR folder, `iwm/` package + mkdocs nav entry),
then begin Phase 0 and run straight through to a fully validated,
tournament-converged, synergy-positive world model without pausing for my approval.
Commit continuously; append Iter NN to PROGRESS.md; keep the leaderboard, ADRs, and
knowledge graph complete so any collaborator can pick up the trail.
```
