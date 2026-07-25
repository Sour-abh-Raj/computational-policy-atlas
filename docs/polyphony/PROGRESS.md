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
- **Iter 03 — 🎉 Phase 2 scaffold (core + vertical slice), all green.** The blueprint became
  running code — see **[`02-scaffold.md`](02-scaffold.md)**.
  - **`polyphony/polyphony/core/`**: `interface.py` (common `Model` `Protocol` state·step·dials·
    provenance, `conforms()`), `dials.py` (`Dial`/`DialsSpec`, validated inspectable assumptions),
    `provenance.py` (per-step reproducible record + stable input hash), **`combiner.py`** (the
    `Disagreement` with the normalized **index D**, skill-weighted mean/sd, and `attribute_to_dial()`
    explained-fraction — answers never averaged away, per ADR-0004), `orchestrator.py` (recursive
    lagged coupling bus with **routing** for dynamics + **run-both** recording; validates names/routing).
  - **`polyphony/polyphony/models/`** — first vertical slice (reduced-form toys, fidelity limits
    stated, **no** fidelity claim): `energy_lp.py` (logit least-cost tech choice + carbon-price dial),
    `econ_cge.py` (equilibrium: cost↑→GDP↓), `econ_e3me.py` (disequilibrium: cost↑→GDP↑).
  - **Golden coupled test** (`tests/test_slice.py`): carbon price loops energy⇄economy; the two econ
    voices are **run both** and **disagree with opposite sign**; the test asserts disagreement **D grows
    with policy**, is **attributed to the closure dial** (>0.9), emissions **fall** with the price, and
    provenance is recorded every step. 15 tests pass.
  - **Gates green:** `pytest` (15) · `ruff` · `mypy` (11 files) · `tools/validate_graph.py` (164 nodes
    / 444 edges, 0-dangling) · `mkdocs build --strict`. Added **`.github/workflows/ci.yml`** running all
    of them on push/PR. Fixed one design bug: dials are a **shared global panel**, so the orchestrator
    now filters to each voice's declared dials before validating.
- **Iter 04 — Climate loop closed + validation/tournament harness stood up (all green).**
  - **Climate voice** `models/climate_dice.py` (`ReducedFormClimate`, toy): emissions → carbon
    stock → **TCRE**-linear temperature → Nordhaus quadratic `damage_frac`; `tcre` dial. Wired
    `damage_frac` into **both** economy voices (GDP ×(1−damage)), closing
    energy⇄economy⇄**climate** (backward-compatible: absent climate ⇒ damage 0, the 3-voice slice
    test is unchanged).
  - **Data layer** `polyphony/data/`: `splits.py` (`time_blocked_split`, expanding-window
    `walk_forward` — no shuffling a time series), `loaders.py` (real CSV if present in
    `datasets/`, else a **clearly-labeled synthetic** fallback), `datasets/README.md` (schema +
    real-source list). Real data tracked as **issue #9** (logged blocker + workaround).
  - **Eval metrics** `polyphony/eval/metrics.py`: `mae`, `rmse`, `mase` (Hyndman–Koehler),
    `crps_ensemble`/`crps_series` (Gneiting–Raftery; reduces to abs-error for a point ensemble,
    rewards sharp-correct spread), `pit_values` (calibration).
  - **Tournament** `polyphony/tournament/`: `synergy.py` (**Δ = best-part-error − coupled-error**;
    >0 ⇒ keep, ≤0 ⇒ cut, "no synergy" publishable), `race.py` (rank by skill − overfit/complexity
    penalty; penalties can dethrone a bloated candidate), `leaderboard.py` (append-only JSON store +
    Markdown render).
  - **Tests:** +13 (climate loop warms & damages, carbon price reduces warming, disagreement
    survives climate coupling; metrics; synergy keep/cut; race ranking & dethrone; leaderboard
    round-trip) → **28 pass**. Gates green: `pytest` · `ruff` · `mypy` (21 files) · graph 0-dangling
    · `mkdocs --strict`.
  - **Honest status:** the harness is real but runs on a **synthetic** target so far — this proves
    the *machinery* (backtest → metric → synergy Δ → leaderboard), **not** real-world skill; that
    awaits real data (#9) and is the Phase 4 deliverable.
- **Iter 05 — 🎉 First synergy tournament: the method works (validated on a two-regime control).**
  - **Coupled predictor vs economy-only baseline** (`polyphony/experiments/slice_tournament.py`):
    predicts a GDP track two ways — the 4-voice coupled ensemble vs the same economics voices with
    the energy/climate **feedback switched off** — scores held-out **MASE** on time-blocked splits,
    and computes **synergy Δ = economy-only − coupled**.
  - **Two-regime method validation** (the honest core): on a synthetic DGP that **has** the coupling,
    coupled wins → **Δ = +2.22 → keep**; on a **decoupled negative control** (GDP ⟂ emissions),
    economy-only wins → **Δ = −1.73 → cut**. The method **detects synergy when real and cuts it when
    spurious** — Polyphony's falsifiable-coupling thesis demonstrated end-to-end. Test
    `tests/test_first_tournament.py` asserts both signs. **29 tests pass.**
  - **Leaderboard is live:** `docs/polyphony/leaderboard.json` (machine-readable, regenerated by
    `python -m polyphony.experiments.run_leaderboard`) + Round 1 table rendered into
    [`leaderboard.md`](leaderboard.md). Wrote **[`03-research.md`](03-research.md)** (the coupling,
    grounded in DICE/CGE/E3ME lit; race protocol; result) and **[`04-validation.md`](04-validation.md)**
    (a blunt what-we-can/can't-claim + an honesty-debt register).
  - **Honesty (recorded, not hidden):** MASE>1 (uncalibrated toys) ⇒ we claim the **sign of synergy**,
    not forecast skill; target is **synthetic**; **real-data fetch is network-blocked** (confirmed via
    urllib timeout) — logged, worked around with the labelled synthetic series, loop continued, per
    contract (issue **#9**). Added negative synthetic control generator + `synthetic_decoupled_series`.
  - **Gates green:** `pytest` (29) · `ruff` · `mypy` (24 files) · graph 0-dangling · `mkdocs --strict`.
    Nav gained 03/04; fixed a mypy Protocol-variance issue by widening model tuple annotations.
- **Iter 06 — 🔴 Red Team breaks the champion (the honest headline) + parametric uncertainty wired.**
  - **`polyphony/tournament/redteam.py`** — five attacks on the Round-1 champion returning structured
    `AttackResult(broke, evidence)`: `distribution_shift`, `lucas_regime_change` (policy shift between
    train/test), `edge_dials` (extreme carbon_price/tcre stay finite), `noise_stability` (sign robust
    across seeds), and the decisive **`naive_baseline`** (must beat a naive random-walk, i.e. MASE<1).
  - **Result — champion does NOT survive.** It survives the first four, but is **broken by
    naive_baseline**: coupled **MASE ≈ 8 > 1** ⇒ worse than naive. The "synergy" was only relative to
    an artificially weak economy-only baseline; there is **no absolute-skill claim**. The Red Team
    caught the ensemble mistaking "less-bad than a weak baseline" for skill — exactly its job. Break
    recorded on the [leaderboard](leaderboard.md) (Round 2) and in [04-validation](04-validation.md);
    it is now a **hard gate**: calibration + real data (#9) required before any champion is trusted.
  - **Parametric uncertainty** `polyphony/experiments/uncertainty.py`: `ensemble_gdp_tracks` samples
    the uncertain dials (carbon price, tcre) → an ensemble of coupled tracks; `ensemble_crps` scores
    it — verified a **calibrated-input ensemble beats a biased one** on CRPS. This puts **CRPS/PIT**
    on the runway to enter the *scored* tournament (not just point MASE).
  - **Tests:** +6 (red-team runs all 5 attacks; edge dials finite; naive-baseline breaks; champion
    doesn't survive; ensemble shape/spread; CRPS centered<biased) → **35 pass.** Gates green:
    `pytest` (35) · `ruff` · `mypy` (26 files) · graph 0-dangling · `mkdocs --strict`.
  - **Next (Iter 07):** priority is **skill, not more couplings**. Land a real/calibrated dataset
    (#9), **calibrate** the reduced-form voices to real levels, re-run the tournament scoring
    **CRPS/PIT** alongside MASE, and only then re-arm the Red Team. Also begin the **welfare/equity
    engine** (#4) so policies are scored on the inspectable values dial (Pareto frontier + VoI).
