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
- **Iter 07 — ⚖️ Welfare/Equity engine (the values dial) + calibration; fed back to the atlas.**
  - **`polyphony/engines/welfare.py`** (issue **#4** closed) — the inspectable values dial: value-neutral
    axes (efficiency, −Gini equity, −climate-risk) with a **Pareto frontier** (`pareto_frontier`), a
    value-laden **social welfare function** via the **equally-distributed-equivalent** (Atkinson: η=0
    utilitarian → η→∞ Rawlsian, η>0 prioritarian) with dials {SWF, inequality aversion, discount rate,
    tail-risk aversion}, and **value of information** (`value_of_information` = EVPI ≥ 0). Cites
    Atkinson (1970), Fleurbaey (2010), Adler (2019).
  - **`polyphony/engines/calibration.py`** — honest affine level/scale fit (train-block only, no
    leakage) to remove bias; docstring states plainly it **does not manufacture skill** (a poor
    structure calibrated to the right level can still lose to naive).
  - **Fed back to the atlas** (scope-is-a-floor): new **Welfare/Equity Engine** pattern page
    (`docs/patterns/welfare-equity-engine.md`, the **17th** engine, marked Polyphony-contributed) +
    graph node `p-welfare` with edges (grounded_in multiobjective & bayesian-decision; ENVISAGE & E3ME
    exhibit it). Graph now **165 nodes / 448 edges, 0-dangling**; graph/index stats + nav updated.
  - **Tests:** +8 (EDE endpoints; Gini/Atkinson; SWF ranking flips utilitarian→Rawlsian; Pareto drops
    dominated; tail-risk widens safety margin; EVPI ≥0 and >0 when it matters; calibration recovers an
    affine map and reduces bias) → **43 pass.** Gates green: `pytest` (43) · `ruff` · `mypy` (29 files)
    · graph 0-dangling · `mkdocs --strict`.
  - **Honesty:** welfare numbers are **illustrative** (reduced-form outcomes) — the contribution is the
    *machinery of honesty* (values as dials, trade-offs on a frontier, EVPI), not a calibrated welfare
    figure. CRPS/PIT into the *scored* tournament and calibration-on-real-data remain open (bound by #9).
- **Iter 08 — 📊 Probabilistic scoring + ⚖️ welfare frontier + calibration lifts (part of) the skill gate.**
  - **CRPS/PIT scored tournament** (`experiments/scored.py`, `uncertainty.ensemble_gdp_tracks` now
    coupled/economy-only): scores the **ensemble distribution**. **CRPS synergy holds** — coupled
    **7.9 < 10.2** economy-only (coupling helps on the *proper* score, not just MASE). **PIT ≈ 0**
    honestly flags the ensemble is **biased low / mis-calibrated**.
  - **Calibration partly addresses the naive break:** affine level fit on the **train block only** drops
    the coupled mean's held-out **MASE ≈ 8.0 → 0.61 (beats naive, <1)** on the synthetic target — a real
    held-out improvement, but **synthetic-only** and it does not fix the distribution (PIT). Red-Team
    naive break now **partly addressed, not closed**.
  - **Welfare frontier integrated** (`experiments/welfare_frontier.py`): coupled outcomes across
    candidate carbon prices → `PolicyOutcome`s (stylized 3-group consumption net of a quadratic
    **abatement cost**, + emissions + welfare-equivalent climate risk) → **Pareto frontier** + rankings.
    **The recommendation changes with the values:** utilitarian & prioritarian → **cp=50**, Rawlsian +
    tail-averse → **cp=100**. The altruism payoff: values are *surfaced*, not hidden in one number.
  - **Tests:** +4 (CRPS synergy + PIT range; calibration reduces error & beats naive on synthetic;
    frontier non-empty & values change the recommendation; tail-averse never picks the dirtiest policy)
    → **47 pass.** Gates green: `pytest` (47) · `ruff` · `mypy` (31 files) · graph 0-dangling ·
    `mkdocs --strict`. Leaderboard Round 3 + 04-validation updated.
- **Iter 09 — 🔧 Ensemble calibration fixed (PIT) + 🦠 second synergy loop Macro⇄Health.**
  - **Calibration/PIT fix** (`engines.calibrate_ensemble`): de-bias (affine, train-only) **and widen**
    the predictive ensemble by the residual std. On the energy slice: **CRPS 7.9 → 0.44** and
    **PIT mean 0.0 → 0.39** (near-uniform) — the over-confident, biased ensemble is now well-calibrated.
    `scored.py` reports raw vs calibrated CRPS/PIT; tests assert the improvement.
  - **Macro⇄Health second loop** (issue **#8**): new **`models/epidemic_sir.py`** (`ReducedFormEpidemic`
    — SIR with r0/npi dials, emitting an `output_penalty`; reduced form of Covasim, cites
    Kermack–McKendrick / Eichenbaum-Rebelo-Trabandt). Wired `output_penalty` into both economy voices
    (GDP ×(1−penalty); backward-compatible, default 0 so the energy slice is unchanged).
    **`experiments/macrohealth.py`** runs the two-regime tournament: **pandemic DGP → coupled MASE 0.95
    (beats naive!) vs econ-only 9.0 → Δ +8.06 keep**; **no-pandemic control → Δ −31.5 cut**. The method
    replicates cleanly in a new domain, and here the coupled champion *beats naive* (matched SIR
    structure) — a sharper result than the energy champion.
  - **Atlas feedback:** the epidemic voice is a reduced form of existing nodes
    ([Covasim](../model-families/health/covasim.md)) coupled to [CGE](../model-families/economics/cge.md)/
    [E3ME](../model-families/economics/e3me.md) — no *new* atlas concept, so the graph is unchanged
    (still 165 nodes / 448 edges, 0-dangling); the coupling is documented as realizing #8.
  - **Tests:** +5 (epidemic wave + NPI flattens; macro-health keep/cut; champion beats naive in
    pandemic; ensemble calibration fixes CRPS+PIT) → **52 pass.** Gates green: `pytest` (52) · `ruff` ·
    `mypy` (33 files) · graph 0-dangling · `mkdocs --strict`. Leaderboard Round 4 + 04-validation updated.
- **Iter 10 — 🔴 Macro⇄Health red team (r0 fragility found) + 🌾 third synergy loop (Land⇄Climate⇄Food).**
  - **Macro⇄Health Red Team** (`experiments/redteam_macrohealth.py`): r0 distribution-shift, a variant
    **Lucas-critique** regime change, extreme dials, and the naive baseline. **Champion BROKEN by
    `r0_shift`** — at r0 4.0 while assuming 2.5, the coupling does far worse than economy-only (coupled
    MASE 30.3 vs 4.1, Δ −26). Survives variant-Lucas, edge dials, and naive. Honest finding: **the health
    coupling helps only when r0 is well-estimated**; the fix it points to is **r0 assimilation**.
  - **Third synergy loop — Land⇄Climate⇄Food (issue #6):** new **`models/land_crop.py`**
    (`ReducedFormLand`: warming → yield loss → food price; dial `yield_sensitivity`; reduced form of
    GLOBIOM + DSSAT). **`experiments/landfood.py`** two-regime tournament: **warming → coupled MASE 6.68
    vs land-only 30.56 → Δ +23.9 keep**; **flat control → Δ −112 cut**. The synergy method now replicates
    across **three independent domains** (energy, health, land).
  - **Atlas feedback:** land voice is a reduced form of existing nodes (GLOBIOM/DSSAT) coupled to climate
    — no new atlas concept; graph unchanged (165/448, 0-dangling). Real data still network-blocked (#9).
  - **Tests:** +4 (macro-health red team finds r0 break & survives naive; land price rises with warming;
    land-food keep/cut) → **56 pass.** Gates green: `pytest` (56) · `ruff` · `mypy` (36 files) ·
    graph 0-dangling · `mkdocs --strict`. Leaderboard Round 5 + 04-validation updated.
  - **Next (Iter 11):** address the r0 break — add a small **assimilation** step (estimate r0 from the
    early observed dip via least-squares) and re-run the Macro⇄Health red team to see if the coupling now
    survives the shift; and/or add a fourth loop (Urban⇄Transport⇄Energy⇄Health #7). Keep pressing real
    data (#9). Toward multi-domain convergence + a champion that survives sustained attack.
- **Iter 11 — 🛰️ Assimilation closes the r0-shift break (the digital-twin backbone) + atlas engine #18.**
  - **Assimilation engine** (`engines/assimilation.py`): `estimate_r0` fits r0 from the **early observed
    GDP dip on the train block** (grid least-squares over the SIR forward map `sir_output_track`), then
    feeds the estimate into the coupled Macro⇄Health predictor — the model ⇄ **assimilation** ⇄ control
    limb (Kalman 1960; grounding [Bayesian estimation](../paradigms/algorithms/bayesian-decision.md) /
    [Digital Twins](../paradigms/algorithms/digital-twins.md)).
  - **Red team re-run WITH assimilation** (`redteam_macrohealth.attack_r0_shift_assimilated`,
    `run_red_team(assimilate=True)`): the *same* attack that broke the champion in Iter 10 now **survives**
    — r0 recovered = **4.0** (exact), coupled **MASE 30.3 → 1.03**, synergy **Δ −26.2 → +3.09**. Reported
    honestly on [leaderboard Round 6](leaderboard.md) and [04-validation](04-validation.md): the break is
    **CLOSED** (synthetic); assimilation fixes the *parameter*, not the coupling *structure*.
  - **Atlas feedback (issue #1):** new **[Data-Assimilation Engine](../patterns/data-assimilation-engine.md)**
    — engine **#18** (after Welfare/Equity #17). Graph node `p-assimilation` (pattern) with edges
    `grounded_in` bayesian-estimation + digital-twins, and `covasim`/`dsge` `exhibits_pattern` — **166
    nodes / 452 edges, 0-dangling.** Nav + patterns index + graph stats updated.
  - **Tests:** +2 (estimator recovers known r0 to within 0.5; assimilation repairs the r0_shift break) →
    **58 pass.** Gates green: `pytest` (58) · `ruff` · `mypy` (37 files) · graph 0-dangling ·
    `mkdocs --strict`.
  - **Next (Iter 12):** the Macro⇄Health champion now survives a full red-team round *with assimilation* —
    press toward the same for the energy champion (still loses to naive) via calibration/assimilation;
    optionally add the fourth loop (Urban⇄Transport⇄Energy⇄Health #7); keep retrying real data (#9). The
    convergence target: a champion that survives sustained attack across **all** covered domains.
- **Iter 12 — ⚖️ A fair calibration cuts the energy synergy (a published "no synergy") + energy naive break resolved honestly.**
  - **Energy naive break closed by calibration:** `tournament/redteam.run_red_team(calibrate=True)` now
    affine-calibrates the champion on the **train block** before the naive test — coupled **MASE 8.0 →
    0.60 < 1**, so the calibrated champion **survives the full energy round** (raw still breaks on naive).
  - **…but a *fair* calibration erases the energy synergy** (`experiments/slice_tournament.calibrated_synergy`):
    give the economy-only baseline its *own* train-block affine fit — its strongest form — and the
    coupled advantage collapses to **Δ ≈ −0.01** (mean +0.001 across 8 seeds, sign unstable) ⇒ **cut**.
    The Round-1 +2.22 was a **level artifact**, not structural skill. A **falsifiable "no synergy"**
    result, published rather than buried — the point of the method.
  - **The contrast is the payoff:** the energy coupling is **cut** after fair calibration, while
    **Macro⇄Health** survives calibration **and** assimilation with a real Δ>0 (Iter 11). Polyphony's
    tournament **separates a real coupling from a spurious/level one** — exactly the honesty the north
    star demands. No energy skill claim survives; genuine energy synergy needs real data + richer
    structure (issue #9).
  - **Atlas feedback:** reuses the existing [Calibration Engine](../patterns/calibration-engine.md) — no
    new atlas concept, graph unchanged (**166 nodes / 452 edges, 0-dangling**).
  - **Tests:** +2 (calibration closes the energy naive break & the champion survives; a fair calibration
    erases the energy synergy -> cut) -> **60 pass.** Gates green: `pytest` (60) - `ruff` - `mypy` (37
    files) - graph 0-dangling - `mkdocs --strict`. Leaderboard Round 7 + 04-validation updated.
  - **Next (Iter 13):** with two domains now honestly adjudicated (energy = cut after fair calibration;
    Macro-Health = keep, survives full round) and Land-Climate-Food's coupling still to be red-teamed,
    run the **Land-Climate-Food red team** (does that coupling survive calibration too, or is it also a
    level artifact?); keep retrying real data (#9). Toward convergence: a champion that survives sustained
    attack in every domain where a coupling is *kept*.
- **Iter 13 — 🌾 The Land-Climate-Food coupling is REAL (survives the energy-killer test) — a three-way discrimination.**
  - **Same fair-calibration attack that CUT energy, applied to land** (`experiments/redteam_landfood.py`,
    `experiments/landfood.calibrated_synergy`): give the climate-blind **land-only** baseline its own
    train-block affine fit, then re-score. **Opposite result** — calibrated coupled MASE **2.87** vs
    land-only **18.1**, **Δ +15.2** (mean +15.5 across 8 seeds). The warming->food-price shape is
    genuinely informative; a calibrated blind baseline cannot fake it ⇒ **KEEP** (not a level artifact).
  - **Land red team:** level_artifact **survived** (Δ+15.2), policy_shift **survived** (world mitigates at
    cp=100 unassumed; calibrated Δ+4.1), edge_dials survived, **naive_baseline (calibrated) BROKE** (MASE
    2.87>1). Honest split: **coupling real, champion not yet skillful** (no absolute skill claim).
  - **The three-way contrast is now the headline** — the tournament discriminates *why* each coupling
    earns its keep: **Energy = cut** (Δ≈−0.01, level artifact); **Land-Climate-Food = keep but not
    skillful** (Δ≈+15 robust, loses to naive); **Macro-Health = keep and skillful** (Δ≈+3.1, beats naive
    MASE 1.03 with assimilation). Reporting all three verdicts — not just the flattering one — is the point.
  - **Atlas feedback:** reuses the existing [Calibration Engine](../patterns/calibration-engine.md) — no
    new atlas concept, graph unchanged (**166 nodes / 452 edges, 0-dangling**).
  - **Tests:** +2 (land coupling survives a fair calibration unlike energy; land champion still loses to
    naive — the honest split) -> **62 pass.** Gates green: `pytest` (62) - `ruff` - `mypy` (38 files) -
    graph 0-dangling - `mkdocs --strict`. Leaderboard Round 8 + 04-validation updated.
  - **Next (Iter 14):** two kept couplings (Land, Macro-Health) — press the land champion toward **beating
    naive** via richer structure/assimilation (estimate the warming driver), and keep retrying real data
    (#9). Optionally add the fourth loop (Urban-Transport-Energy-Health #7) with a cited reason + test +
    atlas feedback. Convergence = a champion that survives sustained attack in every domain where a
    coupling is kept.
- **Iter 14 — 🔎 Why the land champion loses to naive: not parameter, not lag, but structure (+ a real method fix, ADR-0005).**
  - **Attribution by elimination** of the kept-but-not-skillful land champion (Iter 13, calibrated MASE 2.87):
    - **Not a parameter error:** generalized the assimilation engine to the land domain
      (`engines.assimilation.estimate_yield_sensitivity`) — it recovers the **true 0.1** across seeds. The
      driver was already right, so assimilation is not the missing piece here (unlike Macro-Health's r0).
    - **Not (only) the coupling lag:** the energy->climate->land chain is **acyclic**, so it can be
      resolved **contemporaneously** in topological order within the step — new opt-in
      `Orchestrator.run(resolve="contemporaneous")` (**ADR-0005**; lag stays the default, raises on a
      cycle). This removes the spurious one-step-per-hop delay (first-step price now moves with warming),
      yet calibrated **MASE stays ~2.87**.
    - **It is a structural voice/DGP mismatch:** with parameter and lag removed, the residual is the
      reduced-form energy/climate voices' **tail dynamics** vs the target — closable only with **real
      data / richer voices (issue #9)**, NOT by tuning the toy voices to their own synthetic generator
      (refused as dishonest skill-inflation).
  - **Method banked regardless:** contemporaneous resolution is a correct, general orchestrator
    improvement for acyclic couplings (topological sort; cycle-guarded), retained via ADR-0005.
  - **Atlas feedback:** reuses Assimilation + Integration engines — no new atlas node; graph unchanged
    (**166 nodes / 452 edges, 0-dangling**). New **ADR-0005** added to decisions index + nav.
  - **Tests:** +3 (contemporaneous removes the lag; rejects a cyclic routing; land naive-gap is not a
    parameter error) -> **65 pass.** Gates green: `pytest` (65) - `ruff` - `mypy` (38 files) - graph
    0-dangling - `mkdocs --strict`. Leaderboard Round 9 + 04-validation + ADR-0005 updated.
  - **Next (Iter 15):** two kept couplings remain honestly bounded by real data (#9) — keep retrying the
    fetch; if still blocked, either (a) add the fourth loop (Urban-Transport-Energy-Health #7) with a
    cited reason + test + atlas feedback, or (b) offer contemporaneous resolution to the energy/Macro
    slices (both acyclic) and re-measure. Convergence = a champion surviving sustained attack in every
    domain where a coupling is kept.
- **Iter 15 — 🌍 REAL DATA lands (issue #9 closed) and the first real-data verdict is an honest CUT via placebo control.**
  - **Egress returned** — fetched **real** World Bank world GDP (`NY.GDP.MKTP.KD`, constant 2015 US$) +
    **OWID** global CO₂, merged by year (**65 years, 1960–2024**) via new `polyphony/data/fetch_real.py`
    + loader `load_real_gdp_co2` (GDP indexed to 100; CSV committed for deterministic tests).
  - **First tournament on non-synthetic data** (`experiments/real_tournament.py`): predict real GDP from
    an economy-only log-trend vs a **coupled** trend×damage driven by **observed cumulative CO₂**.
    Coupled beats the trend (held-out MASE 3.20 → **1.49**, Δ **+1.70**) — *looks like* synergy.
  - **But it FAILS a placebo control:** the same damage form driven by a meaningless **t^1.5** trend does
    as well or better (MASE **1.34**). So cumulative CO₂ is merely proxying the post-2008 growth
    slowdown, not carrying climate signal ⇒ **CUT**. Neither predictor beats naive (1.49 > 1). The
    placebo control is now a **standing requirement** for real-data couplings.
  - **Honest headline:** on 65 years of real aggregate data, this reduced-form climate→GDP coupling shows
    **no genuine predictive synergy** — precisely the self-deception a placebo exists to catch. (Not a
    claim climate doesn't affect the economy; a single global CO₂→GDP regression just adds no
    short-horizon skill over trend, and any claim it does must clear a placebo.)
  - **Atlas feedback:** reuses existing engines (Data Pipeline + Validation) — no new atlas node; graph
    unchanged (**166 nodes / 452 edges, 0-dangling**).
  - **Tests:** +2 (real dataset loads & is non-synthetic; the real climate coupling fails the placebo →
    cut) -> **67 pass.** Gates green: `pytest` (67) - `ruff` - `mypy` (40 files) - graph 0-dangling -
    `mkdocs --strict`. Leaderboard Round 10 + 04-validation (#9 closed) updated.
  - **Next (Iter 16):** with real data in hand, (a) run the placebo-controlled real tournament for the
    OTHER kept couplings where real series exist; (b) offer contemporaneous resolution to the acyclic
    energy/Macro slices and re-measure; (c) optionally the fourth loop (#7). Convergence = a champion
    surviving sustained attack in every domain where a coupling is kept — now including a **placebo
    control on real data**.
- **Iter 16 — ⚡ Contemporaneous resolution offered to the remaining slices: sharpens Macro⇄Health 10×, correctly refused for cyclic energy; + placebo-control method cited.**
  - **Macro⇄Health (epidemic→economy is acyclic):** wired `resolve` into `experiments/macrohealth.gdp_track`.
    No-lag resolution takes the coupled champion from **MASE 0.95 → 0.10** (10× sharper), synergy Δ
    **+8.06 → +8.92** — the **sharpest champion yet**, decisively naive-beating. Economy-only unchanged.
  - **Energy⇄climate⇄economy is CYCLIC** (genuine energy⇄economy feedback): `resolve="contemporaneous"`
    **raises** — the ADR-0005 guard correctly refuses to resolve a feedback loop in one pass; it stays
    lagged. Two honest wins at once: the mode helps where legitimate, forbids itself where not.
  - **Real Macro⇄Health real-data test deferred honestly:** World Bank GDP-growth + life-expectancy
    fetch fine, but 65 annual points contain essentially **one** pandemic event (2020) — too underpowered
    to claim a verdict; recorded rather than fabricated.
  - **Method surfaced:** added the **placebo / negative-control** method to `related-work.md` with
    citations (Lipsitch–Tchetgen Tchetgen–Cohen 2010; Rosenbaum 2002; Hyndman–Koehler 2006 for MASE) —
    now a standing requirement for real-data couplings (Round 10).
  - **Atlas feedback:** reuses Integration + Data-Assimilation engines — no new atlas node; graph
    unchanged (**166 nodes / 452 edges, 0-dangling**).
  - **Tests:** +2 (contemporaneous sharpens the Macro-Health champion, MASE<0.2 and <½ lagged; energy
    slice is cyclic so contemporaneous raises) -> **69 pass.** Gates green: `pytest` (69) - `ruff` -
    `mypy` (40 files) - graph 0-dangling - `mkdocs --strict`. Leaderboard Round 11 + 04-validation +
    related-work updated.
  - **Next (Iter 17):** the Macro⇄Health champion is now decisively skillful (assimilation + no-lag,
    MASE 0.10) and survives a full round — that domain is **converged**. Remaining: keep pressing a
    placebo-controlled REAL test where power exists; optionally the fourth loop (#7). Convergence overall
    = every kept coupling has a champion surviving red-team + placebo on real data.
