# Polyphony — Autonomous Loop Prompt

Paste this into the loop. It runs inside **this repo** (`model-policy`, the Atlas of
Computational Policy Simulation) and reuses the atlas's conventions as scaffolding.
The simulator it builds is named **Polyphony**: many independent modeling voices
sounding at once, where both the harmony and the dissonance are signal — explicitly
NOT a single "world model" or oracle.

---

```
# PROJECT: Polyphony — a paradigm-plural policy simulation ensemble
# (built on the Atlas of Computational Policy Simulation, this repo)
#
# NORTH STAR: Help humans choose better, more altruistic policies by simulating
# their consequences as accurately AND as honestly as we can — foregrounding
# uncertainty, disagreement between modeling traditions, and welfare/equity effects
# rather than hiding them behind a single confident number.
#
# MODE: Autonomous loop. Run until the ensemble is fully validated,
# tournament-converged, and synergy-positive. Do NOT stop for my approval between
# phases. Self-review at each gate and proceed on your own judgment. Only halt on a
# hard external blocker (missing credentials, data with no substitute) — and even
# then, log it, open a GitHub issue, work around it, and keep going on everything
# else. Append an "Iter NN" entry to PROGRESS.md after every iteration, exactly like
# the existing atlas log.

## 0. POSITIONING — what Polyphony IS and IS NOT (read, then honor throughout)
Integrated policy models and "world models" already exist; do NOT reinvent one or
overclaim to be one. Know the incumbents and stay differentiated:
- **Earth digital twins (e.g. Destination Earth / DestinE).** Geophysical replicas
  (climate, extremes, oceans) at high resolution, increasingly hybrid physics-AI.
  Thin on the human/economic/policy side; single modeling tradition, not
  paradigm-plural. We are NOT building an Earth-system twin.
- **Integrated Assessment Models (DICE, GCAM, IMAGE, REMIND, MESSAGE — already in
  our atlas).** Genuinely integrated economy⇄climate⇄energy, but each hard-codes ONE
  set of contested assumptions and they only compare via manual intercomparison. We
  are NOT building yet another single-tradition IAM.
- **AI/agent "world models."** Two senses: (a) ML latent simulators for RL agents
  (Dreamer, JEPA, Genie); (b) LLM-driven ABMs of economies/societies (EconAgent,
  PolicySim). The field's own admitted central weakness is VALIDATION. We are NOT
  claiming a learned latent world model, and we are NOT hand-waving validation.

**What Polyphony IS — the actual contribution (a METHOD, not just an artifact):**
a paradigm-plural, adversarially-validated, synergy-testing ensemble that (1) keeps
rival modeling traditions as distinct voices, (2) treats their DISAGREEMENT as
first-class signal rather than error to be averaged away, (3) selects features,
couplings, and models by adversarial competition against real data instead of fixed
thresholds, and (4) directly attacks the validation gap the LLM-ABM literature
concedes. Novelty is in the method and the honesty, NOT in claiming to replicate the
world. In all docs, papers, and READMEs: describe Polyphony as a paradigm-plural
policy simulation ensemble / a decision-support instrument that reports disagreement
— never as "the world model," an oracle, or a faithful replica of reality.

## 1. Load the ground truth first (do NOT skip, do NOT invent)
You are working inside the completed **Atlas of Computational Policy Simulation**.
Read it before you plan; it IS your design foundation:
- `README.md`, `PROGRESS.md` (full iteration history + Definition of Done),
  `mkdocs.yml`, `docs/foundations/` (taxonomy, dossier template, the **Three-Track
  method**: Scholar / Engineer / Architect).
- `docs/model-families/**` — ~50 model dossiers across Climate/IAM, Energy,
  Economics, Transport, Health, Frameworks, Agriculture, Water, Urban.
- `docs/paradigms/algorithms/**` — 14 method pages (LP, MILP, DP, optimal-control,
  RL, multi-objective, Bayesian-decision, digital-twins, …).
- `docs/patterns/**` — **16 architecture "Engine" patterns** (integration, market,
  energy-dispatch, land, climate, behavior, spatial, optimization, calibration,
  validation, sensitivity, scenario, policy, technology-adoption, data-pipeline,
  visualization). THESE ARE YOUR COMPONENT BLUEPRINTS — Polyphony is built by
  instantiating these engines as real, coupled code.
- `docs/comparative/**` — the contested-axis matrices (ABM↔CGE, equilibrium↔
  disequilibrium, optimization↔simulation, top-down↔bottom-up, …). THESE ARE YOUR
  DIALS — every contested assumption becomes a switchable parameter.
- `docs/graph/graph.json` — the typed knowledge graph (164 nodes, 444 edges).
  Nodes `{id,type,label,maturity,page}`; edges `{s,r,t}`; `node_types`/`edge_types`
  in `meta`. Keep it valid and 0-dangling as you grow it.

Design thesis of the atlas, which Polyphony MUST inherit:
  1. Make every contested modeling assumption a switchable DIAL.
  2. ROUTE each question to the paradigm where it is valid.
  3. Where paradigms OVERLAP, run BOTH and REPORT THE DISAGREEMENT (this is the
     whole point — polyphony, not unison).
  4. Expose contested VALUES rather than hard-coding them (Pareto frontiers,
     value-of-information); the welfare/altruism objective is a first-class,
     inspectable dial, never a buried constant.

## 2. What we're building
**Polyphony**: an ensemble that composes and EXTENDS the atlas's models into one
coupled, executable system for policy testing — engineered on the Digital-Twin
backbone the atlas describes (`docs/paradigms/algorithms/digital-twins.md`): model ⇄
data-assimilation ⇄ control. It must be **validated against real historical data**
(backtesting) so we can PROVE it works, and it must report distributional / welfare
/ equity outcomes so policies can be judged for altruistic value, not GDP alone.

Where it lives: a new top-level package in this repo (`polyphony/`) so the atlas
stays intact and the simulator grows beside it. Keep MkDocs as the living docs
surface — add a `polyphony/` docs section and keep `mkdocs build --strict` green.

## 3. The synergy bet (stated honestly, not as a world-model claim)
We couple models because we hypothesize **emergent synergy**: cross-domain feedbacks
(energy⇄climate⇄economy⇄health⇄land⇄water⇄urban) that standalone models miss, so the
coupled ensemble predicts reality better than the best combination of isolated parts.
This is a FALSIFIABLE hypothesis, not a promise of a faithful replica:
- Instrument every cross-domain coupling and measure whether coupled beats
  sum-of-parts on real data.
- If a coupling doesn't earn its keep, cut it; if it does, prove why and record the
  interaction effect. "Integration adds no synergy here" is an acceptable, publishable
  finding.
- Optimize fidelity of the WHOLE for the QUESTION asked; never claim general fidelity
  to the world.

## 4. Scope is a floor, not a ceiling — research and engineer freely
The existing domains, factors, paradigms, and engines are your STARTING point. You
have a free hand to do original **feature engineering and feature discovery**; to
**extend, add, or replace** models, domains, paradigms, engines, and couplings
(including ones not in the atlas); and to fold in new methods (data assimilation,
ensembling, causal inference, ML/hybrid, agent-based, surrogate/emulator, etc.) when
they improve validity. Every extension MUST be **grounded in literature**: cite
primary sources, justify against alternatives in an ADR (`docs/decisions/`), and feed
it back into the atlas as a new dossier/method/engine page at the right maturity tier
(Bronze→Silver→Gold) plus new nodes/edges in `graph.json`. The knowledge base grows
WITH the ensemble. No unsupported inventions: every added factor or coupling needs a
cited reason AND a test.

## 5. Adversarial regime — competition selects everything (NO fixed thresholds)
Selection is adversarial and tournament-based at every level. Nothing is accepted for
clearing a number; things survive by BEATING rivals against real data. Choose the
BEST OF COMPETITION.
- **Feature competition:** generate many candidate features/transformations; race
  them; keep only those that win on out-of-sample, holdout, and distribution-shift
  backtests. Penalize overfitting, leakage, redundancy, complexity.
- **Coupling / synergy competition:** pit coupled configurations against decoupled
  baselines and each other; a coupling advances only if it adds demonstrable synergy.
- **Model & method competition:** rival paradigms head-to-head on the same question;
  route to winners; where winners disagree, keep BOTH and report the disagreement.
- **Red-team the champion:** a dedicated adversary subagent whose sole job is to BREAK
  the current best — adversarial scenarios, stress/shifted data, edge regimes,
  perturbations, counterfactuals, and Lucas-critique / regime-change attacks on policy
  responses. Whatever it breaks re-enters selection. The champion must survive
  SUSTAINED attack, not a one-off test.
- **Stop condition (relative, self-adjusting):** a stable champion that no challenger
  feature, coupling, method, or red-team attack can beat within a full tournament
  round — competition CONVERGED — AND net positive synergy over isolated baselines on
  real data, across all covered domains. When both hold, the loop is DONE.

## 6. Labs (subagents) — orchestrate these yourself; they mirror the Three Tracks
- **Research Lab (Scholar)** — surveys atlas + literature (including the incumbents in
  §0), discovers/engineers features, justifies couplings, selects methods, designs the
  tournament + validation + synergy-measurement protocol, writes ADRs and atlas pages.
- **Engineering Lab (Engineer)** — architecture, wireframes, the common model
  interface, engine implementations, orchestration, CI, tournament/leaderboard.
- **Testing Lab (Architect/V&V)** — builds the validation + tournament harness, sources
  real datasets, backtests, measures synergy, reports fit, calibration, welfare/equity
  outcomes, and disagreement.
- **Red Team** — the dedicated adversary (§5).

## 7. Operating rules — GitHub is the single source of truth
- Every iteration ends with commits, updated docs, and PRs. Write for collaborators:
  READMEs, ADRs (`docs/decisions/`), issue/PR templates, CONTRIBUTING, reproducible env.
- Read existing dossiers/graph/patterns first and cite them; cite external literature
  when you go beyond them. Follow atlas citation discipline (cite PRIMARY sources; never
  commit tokens/secrets — Pages deploy is credential-gated, `gh auth login` by owner).
- Design → self-review → build. Small increments, each with automated acceptance checks
  and tournament results that YOU run and log.
- Maintain in `polyphony/docs/` (surfaced in mkdocs): `PROGRESS.md` (append Iter NN),
  `docs/decisions/` (ADRs), `leaderboard.md` (every competition: contenders, metrics,
  why the winner won), and `related-work.md` (the §0 positioning, kept current).
- Keep `mkdocs build --strict` green and `graph.json` valid/0-dangling every commit.

## 8. Phases (self-gated — win your own tournaments, then continue)

### Phase 0 — Scout, Inventory & Position
Read the entire knowledge base. Produce `polyphony/docs/00-inventory.md`: each model's
I/O and state, assumptions-as-dials (from the comparative matrices), native paradigms,
the 16 engines as candidate components, couplings the graph implies, candidate synergy
loops, gaps, and candidate NEW factors/domains. Also produce `related-work.md`: situate
Polyphony against DestinE, the IAM family, LLM-ABMs, and ML world models (§0), stating
crisply what we are and are not building and where the contribution lies. Open GitHub
issues for gaps.

### Phase 1 — Blueprint & Wireframes
`polyphony/docs/01-blueprint.md` + committed Mermaid/SVG diagrams: architecture and
module boundaries expressed AS the atlas engines; a common model interface (state,
step, params/dials, provenance) so any model composes; the model⇄assimilation⇄control
backbone; the ensemble/coupling + paradigm-routing + run-both-report-disagreement
strategy; Bayesian uncertainty propagation; welfare/equity as an explicit
multi-objective dial; the tournament + adversarial + synergy-measurement protocol;
feature-engineering plan; package layout; tech-stack ADR; phase plan with automated
acceptance tests.

### Phase 2 — Engineering Lab: scaffold
Build `polyphony/`: common interface, orchestrator/ensemble harness, dials/config,
provenance logging, tournament/leaderboard machinery, red-team hooks, CI (lint + test +
`mkdocs build --strict`), and adapters for a vertical slice of 2–3 representative models
from different families (e.g. DICE ⇄ an energy model ⇄ a CGE), reusing the engines.
Typed, tests green.

### Phase 3 — Research Lab: justify, engineer, compete
Generate and race candidate features and couplings for the slice; document why survivors
win, data needed, failure modes, methods chosen — with citations. `03-research.md` + ADRs
+ leaderboard + new/updated atlas pages and graph nodes/edges.

### Phase 4 — Testing Lab + Red Team: validate & attack
Build the validation/tournament harness. Source real historical datasets, backtest the
coupled slice, MEASURE SYNERGY (coupled vs sum-of-parts), report fit, calibration,
welfare/equity outcomes, and disagreement, then run the red team. Reproducible eval
script + metrics dashboard + `04-validation.md`. Advance the round's winner; iterate
until a stable champion emerges.

### Phase 5+ — Scale to full validation
Loop interface → research → feature-engineering → tournament → red-team,
family-by-family, extending and adding domains/engines as evidence warrants, until the
FULL ensemble is validated against real data across all covered domains AND shows net
positive synergy over isolated baselines AND its champion survives a full tournament
round of sustained red-team attack with no challenger beating it. Keep the website's
graph view and `graph.json` in sync throughout. That convergence is the DONE state.

## 9. Kickoff
Set up the GitHub collaboration scaffolding (branch strategy, issue/PR templates,
CONTRIBUTING, `docs/decisions/` ADR folder, `polyphony/` package + mkdocs nav entry),
then begin Phase 0 and run straight through to a fully validated, tournament-converged,
synergy-positive ensemble without pausing for my approval. Commit continuously; append
Iter NN to PROGRESS.md; keep the leaderboard, ADRs, related-work, and knowledge graph
complete so any collaborator can pick up the trail. Throughout: describe the system
honestly as a paradigm-plural policy simulation ensemble — never as a world model.
```
