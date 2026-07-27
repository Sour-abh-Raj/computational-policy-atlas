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
- **Iter 17 — 🌡️ Powered real test with OBSERVED temperature: the climate→GDP cut is robust (not a CO₂-proxy artifact) + per-domain convergence status.**
  - **Fetched real temperature** (Hadley Centre global anomaly, via OWID) into `fetch_real.py`; merged
    with GDP+CO₂ (**58 years, 1960–2017**; CSV re-committed) and exposed as `temp` in `load_real_gdp_co2`.
  - **Re-ran the real climate→GDP tournament with a `driver` option** (`experiments/real_tournament.py`):
    driven by **observed temperature** the coupling scores MASE **1.07** vs placebo **0.87** ⇒ still
    **CUT** (fails the placebo, loses to naive) — same verdict as the cum-CO₂ proxy (1.18 vs 0.87). **The
    real-data cut is robust to the honest, direct driver**: a meaningless time trend predicts held-out
    GDP better than either climate driver. Not a claim climate doesn't affect the economy — a statement
    about *this reduced-form channel on this aggregate series*.
  - **Convergence status (per domain)** added to the leaderboard: Macro⇄Health **KEEP** (converged, real
    test underpowered — no more events to fetch); Energy **CUT**; Land⇄Climate⇄Food **KEEP-not-skillful**
    with an **open, improvable gap** (a real food-price + temperature test); Real climate→GDP **CUT**
    (robust). **Not DONE** — the land real-data gap keeps the loop going.
  - **Atlas feedback:** reuses Data Pipeline + Validation engines — no new atlas node; graph unchanged
    (**166 nodes / 452 edges, 0-dangling**).
  - **Tests:** parametrized the real-placebo test over both drivers (cum_co2, temp) + temp-carried-through
    assertion -> **70 pass.** Gates green: `pytest` (70) - `ruff` - `mypy` (40 files) - graph 0-dangling -
    `mkdocs --strict`. Leaderboard Round 12 + convergence status + 04-validation updated.
  - **Next (Iter 18):** close the one open gap — fetch **real food-price (e.g. FAO Food Price Index) +
    temperature** and run a placebo-controlled real Land⇄Climate⇄Food tournament; report keep/cut. If the
    fetch is blocked, log + work around. When no domain has an improvable gap, STOP with a convergence
    summary (per the DONE criterion).
- **Iter 18 — 🌾 Real Land⇄Climate⇄Food test CLOSES the last gap: CUT on real data (fails placebo AND wrong sign) ⇒ CONVERGENCE DONE.**
  - **Fetched real cereal yield** (World Bank `AG.YLD.CREL.KG`, kg/ha) + reused Hadley temperature into a
    new `datasets/real_food.csv` (57 yrs, 1961–2017) via `fetch_real.fetch_food` + loader `load_real_food`.
  - **Real Land⇄Climate⇄Food tournament** (`experiments/real_land_tournament.py`) tests the land voice's
    warming→lower-yield→higher-price mechanism on real yield. **CUT on two independent grounds:**
    (a) the warming-damage term beats the trend (MASE 4.94→2.21) but **ties a t^1.5 placebo** (2.20) ⇒
    fails the placebo; (b) **corr(temp, real yield) = +0.90 — the WRONG sign**: real yields rose *with*
    warming because the **Green Revolution** (fertilizer/irrigation/genetics) dominated. A coupling
    confidently **kept on synthetic** data (Δ+15) is **falsified by real data** — the sharpest possible
    demonstration that synthetic validation is never enough.
  - **CONVERGENCE (DONE):** every kept coupling survives its full round (Macro⇄Health; real test
    unimprovable on annual data) and every other candidate is **cut with a recorded, falsifiable reason**
    — three on *real* data under a placebo control. No domain retains an open, improvable gap. Convergence
    table on the leaderboard marked DONE.
  - **Atlas feedback:** reuses Data Pipeline + Validation engines — no new atlas node; graph unchanged
    (**166 nodes / 452 edges, 0-dangling**).
  - **Tests:** +2 (real food dataset loads & is non-synthetic; real land coupling is cut — fails placebo
    + wrong sign) -> **72 pass.** Gates green: `pytest` (72) - `ruff` - `mypy` (41 files) - graph
    0-dangling - `mkdocs --strict`. Leaderboard Round 13 + convergence table + 04-validation updated.
  - **Loop STOPPED** at convergence: one coupling earned its keep and survives sustained attack
    (Macro⇄Health); three were cut — and the cuts, especially the real-data sign reversal in
    Land⇄Climate⇄Food, are the most valuable results, because they are the ones a single-confident-number
    simulator would have hidden. Restartable anytime with /loop (e.g. to add the fourth domain #7).
- **Iter 19 — 🌬️ Fourth synergy loop: Urban⇄Transport⇄Energy⇄Health, the air-quality co-benefit (#7). New mandate: make the model more robust/complete/holistic + find validation avenues.**
  - **New mandate** (loop restarted, dynamic mode): act as a scientist-engineer — extend coverage, add
    validation avenues, make the ensemble more holistic. Honoring "scope is a floor", added the fourth
    domain: the **health co-benefit of transport decarbonization** (Haines et al. 2009 Lancet; Dockery
    1993 Harvard Six Cities; Burnett 2018 GEMM) — one of the best-documented cross-domain couplings.
  - **Two new voices:** `ReducedFormTransport` (carbon price → vehicle-km via mode-shift with behavioural
    inertia → ambient PM2.5) and `ReducedFormAirHealth` (log-linear concentration–response function turns
    PM2.5 into an excess-mortality `health_burden`). Coupled **contemporaneously** — the chain
    transport→airhealth is acyclic (ADR-0005). New DGPs: `synthetic_cobenefit_series` (matched, coupling
    present) + `synthetic_flat_health_series` (negative control).
  - **`experiments/urbanhealth.py`** — three-way honesty machinery transfers cleanly: raw synergy is a
    huge **level artifact** (blind baseline has no level) in BOTH regimes, but under a **fair calibration**
    the co-benefit keeps **Δ +13.5** (coupled MASE 0.87 vs blind 14.35) while the negative control is
    **cut** (Δ 0.00); the exposure **sign is as assumed** (corr +0.997). **KEEP on synthetic, CUT on
    control.**
  - **Honest caveat:** synthetic keep = machinery, not skill — identical in status to Land⇄Climate⇄Food
    at Round 8, which real data later *falsified* (Round 13). So the co-benefit is **not banked**; it
    opens a **new real-data gap** (real PM2.5 + mortality + placebo). Convergence status **REOPENED**.
  - **Atlas feedback (new coverage):** **BenMAP-CE** dossier (`docs/model-families/health/benmap.md`, EPA
    air-pollution health-impact model — genuinely missing atlas coverage) + graph nodes `benmap` (model),
    `crf` (algorithm, Concentration–Response Function), `dockery` (researcher), `epa` (institution) with
    convention-matching edges. Nav + model-families index + graph stats updated. **170 nodes / 458 edges,
    0-dangling.**
  - **Tests:** +5 (`test_urbanhealth.py`: voices conform; policy lowers exposure over time; raw synergy is
    a level artifact; co-benefit survives fair calibration + right sign; negative control cut) -> **77
    pass.** Gates green: `pytest` (77) · `ruff` · `mypy` (44 files) · graph 0-dangling · `mkdocs --strict`.
    Leaderboard Round 14 + reopened convergence table + standing champion + 04-validation + related-work
    updated.
  - **Next (Iter 20):** close the new gap — fetch a **real PM2.5 (e.g. OWID/GBD ambient PM2.5) + mortality
    (WHO/GBD attributable or all-cause) series** and run a **placebo-controlled real co-benefits
    tournament**; report keep/cut honestly (with the sign check). If the fetch is hard-blocked, log +
    open an issue + work around (deepen an existing result or add a further domain). The loop continues
    until this domain resolves on real data.
- **Iter 20 — 🌬️ Real air-quality co-benefit is CUT: RIGHT sign, but no skill above trend (confounding). Convergence DONE again.**
  - **Fetched real data** (`fetch_real.fetch_cobenefit` + `_fetch_worldbank` with retries): World Bank
    world **PM2.5 mean exposure** (`EN.ATM.PM25.MC.M3`, µg/m³) + an **independent all-cause crude death
    rate** (`SP.DYN.CDRT.IN`, per 1000) → `datasets/real_cobenefit.csv` (34 yrs, 1990–2023). Loader
    `load_real_cobenefit`.
  - **Circularity avoided (the key design choice):** used *all-cause* mortality, NOT GBD "mortality
    attributed to ambient PM2.5" — the latter is *computed from* PM2.5 via a CRF, so testing PM2.5 → it
    would confirm the mechanism by construction. Only an independent outcome can fail.
  - **Real tournament** (`experiments/real_urbanhealth_tournament.py`, `_hazard_fit_predict` with the
    assumed direction k≥0): corr(PM2.5, death rate) = **+0.35 — the RIGHT sign** (unlike land). But the
    fitted hazard **k → 0**: coupled MASE 1.781 = trend MASE, and a **t^1.5 placebo does better (1.768)**.
    **Verdict CUT.** The positive correlation is a *shared downward trend* (both fell 1990–2023), not
    PM2.5 carrying independent mortality information.
  - **The lesson:** a coupling can be **true micro-epidemiology** (cohort CRFs) yet earn **no aggregate
    time-series skill** — ecological confounding + a dominant demographic trend swamp it. Four couplings
    now cut, each for a *different, named* reason (level artifact / genuinely cyclic / wrong sign /
    confounded-away) — that catalogue of failure modes is the instrument's real output.
  - **Atlas feedback:** reuses Data Pipeline + Validation engines (like Iter 18) — no new graph node;
    graph unchanged (**170 nodes / 458 edges, 0-dangling**). New real dataset committed.
  - **CONVERGENCE (DONE again):** the Iter-19 scope extension is resolved on real data; no domain retains
    an open, improvable gap. **+2 tests -> 79 pass.** Gates green: `pytest` (79) · `ruff` · `mypy` (45
    files) · graph 0-dangling · `mkdocs --strict`. Leaderboard Round 15 + convergence table (DONE) +
    04-validation register updated.
  - **Loop continues (dynamic mode):** convergence is restored, but the standing mandate is to keep
    making the ensemble more robust/complete/holistic. Next natural avenues (each needs a cited reason +
    test + two-regime keep/cut + real-data bar + atlas feedback): a **fifth domain** (e.g.
    Water⇄Energy⇄Food nexus, or Urban⇄Housing⇄Migration), or **deepening validation** (CRPS/PIT on the
    real-data tournaments; multi-region rather than world-aggregate to reduce the confounding that cut
    the co-benefit).
- **Iter 21 — 💧 Fifth synergy loop: the Water⇄Energy⇄Food nexus (#10). KEEP on synthetic; real gap reopens convergence.**
  - **Scope is a floor:** extended to the **Water⇄Energy⇄Food nexus** (Hoff 2011 Bonn Nexus Conference;
    Howells et al. 2013 CLEWs) — water, energy, food are interdependent so a drought propagates into food
    *and* energy prices.
  - **Two new voices:** `ReducedFormWater` (a `precipitation` dial drives inflow against demand into a
    buffer **store**; a sustained deficit draws it down so **water stress** rises and saturates — storage
    dynamics turn a constant deficit into a time-varying signal) and `ReducedFormNexusFood` (irrigation
    yield loss + a pumping-energy surcharge turn stress into food price). Coupled **contemporaneously**
    (acyclic; ADR-0005). Driver is **water**, distinct from the climate-driven land voice. DGPs:
    `synthetic_nexus_series` (drought) + `synthetic_flat_nexus_series` (negative control).
  - **`experiments/waternexus.py`:** raw synergy is a level artifact (+727), but under **fair calibration**
    the coupling keeps **Δ +99.3** (coupled MASE 0.82 vs blind 100.1) with the **right sign** (corr +0.99),
    while the negative control is **cut** (Δ 0.00). **KEEP on synthetic, CUT on control.**
  - **Honest caveat:** synthetic keep = machinery, not skill (cf. every prior domain). Opens a **new
    real-data gap** (#10-real): a real water/food-price placebo test. Convergence **REOPENED**.
  - **Atlas feedback (new coverage):** **CLEWs** dossier (`docs/model-families/water/clews.md`, the
    integrated Climate-Land-Energy-Water nexus framework — genuinely missing atlas coverage) + graph nodes
    `clews` (model), `howells` (researcher, also linked to `osemosys` which he created) with
    convention-matching edges. Nav + model-families index + graph stats updated. **172 nodes / 465 edges,
    0-dangling.**
  - **Tests:** +5 (`test_waternexus.py`) -> **84 pass.** Gates green: `pytest` (84) · `ruff` · `mypy` (48
    files) · graph 0-dangling · `mkdocs --strict`. Leaderboard Round 16 + reopened convergence table +
    standing champion + 04-validation + related-work updated.
  - **Next (Iter 22):** close the new gap — fetch a **real water/food series** (e.g. FAO/IMF food price
    index vs a drought/precipitation or renewable-freshwater index; or World Bank agricultural-water data)
    and run a **placebo-controlled real nexus tournament**; report keep/cut honestly with the sign check.
    If the fetch is hard-blocked, log + open an issue + work around.
- **Iter 22 — 💧 Real energy→food nexus leg is CUT: strong correlation (+0.90), no out-of-sample skill. Convergence DONE again.**
  - **Data limitation, worked around (per contract):** a clean global *water-scarcity* annual driver is
    not readily available, so tested the nexus's most data-rich, best-documented leg — the **energy→food
    price** transmission (fertilizer/fuel/pumping), which the `nexusfood` voice carries as its
    pumping-energy surcharge. A *partial* nexus test (energy pillar); water-leg real test noted as
    data-limited.
  - **Fetched real data** (`fetch_real.fetch_nexus` + `_fetch_fred_annual`, FRED CSV, no API key): IMF
    Global **Food** (PFOODINDEXM) and **Energy** (PNRGINDEXM) price indices, annual means →
    `datasets/real_nexus.csv` (34 yrs, 1992–2025). Loader `load_real_nexus`.
  - **Real tournament** (`experiments/real_nexus_tournament.py`, reuses `_hazard_fit_predict`):
    corr(energy, food) = **+0.90 (strong, right sign)**, but a train-fit pass-through does **worse than a
    plain trend** (MASE 3.84 vs 3.27), worse than a placebo (3.74), and far worse than **naive** (all ≫ 1).
    **Verdict CUT.** The pass-through fit on 1992–2015 does **not** extrapolate to the 2022 energy shock
    (energy ~doubled; food, buffered by inventories/substitution, rose far less).
  - **The lesson (fourth distinct failure mode):** a strong *contemporaneous* correlation is **not** a
    usable leading predictor — different from the co-benefit's "confounded-away" (correlation vanished on
    detrending; here it stays +0.90 but doesn't forecast). Five couplings now cut, five *named* failure
    modes (level artifact / cyclic / wrong sign / confounded-away / real-signal-no-skill); one kept.
  - **Atlas feedback:** reuses Data Pipeline + Validation engines (like Iter 18/20) — no new graph node;
    graph unchanged (**172 nodes / 465 edges, 0-dangling**). New real dataset committed.
  - **CONVERGENCE (DONE again):** the Iter-21 scope extension is resolved on real data; no domain retains
    an open, improvable gap. **+2 tests -> 86 pass.** Gates green: `pytest` (86) · `ruff` · `mypy` (49
    files) · graph 0-dangling · `mkdocs --strict`. Leaderboard Round 17 + convergence table (DONE) +
    04-validation register updated.
  - **Loop continues (dynamic mode):** convergence restored; the standing mandate keeps pushing for more
    coverage + validation. Next avenues: a **sixth domain** (e.g. Macro⇄Finance systemic risk, or
    Migration⇄Climate), or **deepening validation** (walk-forward CV instead of a single split; CRPS/PIT
    on real tournaments; a real water-scarcity driver for the nexus water-leg if a source can be found).
- **Iter 23 — 🔁 Walk-forward CV hardens the real-data verdicts (and corrects their reasons): the robust common cut is "no skill vs naive".**
  - **Motivation (robustness, not breadth):** the single-split real tournaments each rest on one arbitrary
    time-blocked cut, and the nexus placebo comparison *flipped* between two reasonable splits (Iter 22).
    So instead of a sixth domain, this iteration hardens the validation itself.
  - **`experiments/walkforward.py`:** re-runs every real coupling over an **expanding-window walk-forward**
    (reusing the existing `walk_forward` split helper) on a unified **sign-aware reduced form**
    (`trend·(1 + direction·k·z)`, k≥0 clamped to the assumed direction), reporting per-fold how often the
    coupling beats its **baseline**, a **placebo**, and **naive**.
  - **Result — all four real cuts hold across folds, but the reason is corrected:** climate→GDP and
    energy→food actually **beat the placebo in most folds** (so the single-split "fails placebo"
    attributions were partly split artifacts); what is invariant is that **none beats a naive random walk**
    in a majority of folds (14% / 14% / 50% / 25%). On smooth aggregate series a random walk is the honest
    baseline, and these reduced-form couplings don't clear it. A more robust method revised a weaker
    method's conclusion — documented, not hidden.
  - **Atlas feedback:** deepens the **Validation Engine** — added **Walk-forward CV** and **Placebo/naive
    baselines** rows to `docs/patterns/validation-engine.md`. Reuses the Validation engine, no new graph
    node; graph unchanged (**172 nodes / 465 edges, 0-dangling**).
  - **Convergence stays DONE:** this confirms/hardens existing verdicts (doesn't add a coupling). **+2
    tests -> 88 pass.** Gates green: `pytest` (88) · `ruff` · `mypy` (50 files) · graph 0-dangling ·
    `mkdocs --strict`. Leaderboard Round 18 + 04-validation register + validation-engine page updated.
  - **Next (Iter 24):** either a **sixth domain** OR further validation depth (CRPS/PIT probabilistic
    scoring on the real tournaments; or hunt a real water-scarcity driver to test the nexus water-leg,
    not just the energy leg).
- **Iter 24 — 🎲 Probabilistic scoring on real data: the couplings are inaccurate AND grossly overconfident (foreground uncertainty).**
  - **North-star move:** point accuracy (MASE) can't see whether a model's *bands* are honest. This
    iteration scores **uncertainty**, not just error, on the real couplings.
  - **`experiments/real_probabilistic.py`:** turns each real coupling's point forecast into a predictive
    distribution (point ± resampled train residuals) and scores **CRPS** + **PIT** (reusing the existing
    metrics, previously synthetic-only) against a probabilistic **naive** (persistence ± train
    first-difference spread).
  - **Two distinct verdicts:** (1) **accuracy** — every coupling loses to naive on CRPS too (mirrors the
    point cuts); (2) **calibration** — every coupling is **grossly overconfident**: the PIT piles entirely
    at the tails (**0% of values in the central half**), so the predictive interval almost never contains
    the realised value. Cause: out-of-sample error is dominated by **trend-extrapolation bias** the
    in-sample residual spread never saw, so train-calibrated bands are far too narrow out of sample.
  - **Why it matters:** *foregrounding uncertainty* means reporting not just that a forecast is wrong but
    that its **confidence is unearned** — exactly what a single-confident-number simulator hides. The
    honest remedy (predictive distributions carrying parameter/structural uncertainty, not only in-sample
    residuals) is now future work motivated by a measured miscalibration.
  - **Atlas feedback:** deepened the **Validation Engine** page with a **Probabilistic calibration** row.
    Reuses existing CRPS/PIT metrics + Validation/Sensitivity engines — no new graph node; graph unchanged
    (**172 nodes / 465 edges, 0-dangling**).
  - **Convergence stays DONE** (validation deepening, no new coupling). **+2 tests -> 90 pass.** Gates
    green: `pytest` (90) · `ruff` · `mypy` (51 files) · graph 0-dangling · `mkdocs --strict`. Leaderboard
    Round 19 + 04-validation register + validation-engine page updated.
  - **Next (Iter 25):** either widen the predictive distributions to earn honest calibration (parameter +
    structural uncertainty; re-score CRPS/PIT), or add a **sixth domain**, or hunt a real water-scarcity
    driver for the nexus water-leg.
- **Iter 25 — 🎯 Honest uncertainty: calibration is achievable (but blind to regime breaks). Turned the Round-19 overconfidence diagnosis into a remedy.**
  - **`experiments/honest_uncertainty.py`:** builds an honest predictive distribution using only training
    info — **OOS bias correction** (walk-forward backtest on the train block) + **horizon-fanning bands**
    (spread grown as √h with forecast lead), fixing the two diagnosed causes of Round-19 overconfidence
    (out-of-sample point bias + horizon-blind in-sample bands).
  - **Two honest halves:** (1) where the future resembles the past, the honest bands **earn calibration**
    — climate→GDP and warming→yield rise from **0% → 47% / 100%** central PIT coverage, proving a
    calibrated predictive distribution is achievable **even for a coupling with no point skill**; (2) where
    the test block holds a genuine **regime break** the backtest never saw (PM2.5→mortality's aging upturn;
    energy→food's 2022 shock), historical residuals **cannot** insure against it and calibration stays
    broken.
  - **The lesson:** honest uncertainty from history is a real, achievable virtue but **still blind to
    structural breaks** — a caveat any calibration claim must carry, and exactly the over-promise a
    single-confident-number simulator makes and this project refuses.
  - **Atlas feedback:** reuses the Validation Engine (probabilistic-calibration row already added Iter 24);
    no new graph node; graph unchanged (**172 nodes / 465 edges, 0-dangling**).
  - **Convergence stays DONE** (validation/uncertainty deepening, no new coupling). **+3 tests -> 93
    pass.** Gates green: `pytest` (93) · `ruff` · `mypy` (52 files) · graph 0-dangling · `mkdocs --strict`.
    Leaderboard Round 20 + 04-validation register updated.
  - **Next (Iter 26):** a **sixth domain** for breadth (e.g. Macro⇄Finance systemic risk, Migration⇄Climate),
    or a real water-scarcity driver for the nexus water-leg, or surface the disagreement/uncertainty
    machinery in the docs as a worked decision-support example (north star: help humans choose).
- **Iter 26 — 🏦 Sixth synergy loop: Macro⇄Finance, the financial accelerator (#11). KEEP on synthetic (beats naive); real gap reopens convergence.**
  - **Scope is a floor:** extended to **Macro⇄Finance** — the financial-accelerator / leverage-cycle
    channel (Bernanke-Gertler-Gilchrist 1999; Minsky; Gilchrist-Zakrajšek 2012).
  - **New voice `ReducedFormFinance`:** a credit shock builds through the leverage cycle to a **delayed,
    slowly-unwinding output drag** (a critically-damped `t·aᵗ` boom-bust hump), feeding the economy voices'
    existing `output_penalty` channel — structurally the Macro⇄Health template with a *financial*
    accelerator. Coupled contemporaneously (acyclic; ADR-0005). New DGP
    `synthetic_financial_crisis_series` (matched) + reuse `synthetic_decoupled_series` as the control.
  - **`experiments/macrofinance.py`:** crisis regime raw Δ +35.8; under **fair calibration** Δ **+2.74**
    with the **right sign** (corr(credit spread, GDP) = −0.999) and **beats naive** (coupled MASE 0.82 < 1);
    decoupled control **cut** (Δ 0). **KEEP on synthetic, CUT on control.** Genuinely skillful on synthetic.
  - **Honest caveat:** synthetic keep = machinery, not skill. Opens a **new real-data gap** (#11-real) — and
    unusually a real KEEP is *plausible* (financial conditions lead output; Gilchrist-Zakrajšek), making the
    real test especially worth running. Convergence **REOPENED**.
  - **Atlas feedback (new coverage):** new **Finance / Systemic Risk** domain (`d-finance`) + **EIRIN**
    dossier (`docs/model-families/finance/eirin.md`, a stock-flow-consistent behavioural macro-finance
    model — genuinely missing) + graph nodes `eirin` (model), `monasterolo` (researcher), linked to the
    existing `eiee` institution. Nav + model-families index + graph stats updated. **175 nodes / 470 edges,
    0-dangling.**
  - **Tests:** +5 (`test_macrofinance.py`) -> **98 pass.** Gates green: `pytest` (98) · `ruff` · `mypy`
    (54 files) · graph 0-dangling · `mkdocs --strict`. Leaderboard Round 21 + reopened convergence table +
    standing champion + 04-validation + related-work updated.
  - **Next (Iter 27):** close the new gap — fetch a **real credit-spread → output series** (e.g. FRED
    BAA-10Y or the excess bond premium vs GDP growth) and run a **placebo-controlled real Macro⇄Finance
    tournament** (with walk-forward + CRPS/PIT); report keep/cut honestly. A real KEEP would be the second
    surviving coupling — worth testing carefully and honestly.
- **Iter 27 — 🏦 Real Macro⇄Finance: the closest call yet — a narrow CUT (regime-dependent skill). Convergence DONE again.**
  - **Fetched real data** (`fetch_real.fetch_finance`; FRED CSV, `_fetch_fred_annual` extended with a
    per-series `min_obs` so quarterly GDP isn't dropped by the monthly full-year guard): Baa−10Y **credit
    spread** (BAA10Y) + **real GDP** (GDPC1) → `datasets/real_finance.csv` (40 yrs). Loader
    `load_real_finance`.
  - **Real tournament** (`experiments/real_finance_tournament.py`): tests the spread → real-GDP-**growth**
    nowcast (the natural target; financial conditions predict activity, not the smooth level —
    Gilchrist-Zakrajšek 2012), decided by **walk-forward** (Round 18).
  - **Honest result — the strongest real signal, still CUT:** corr(spread, growth) = **−0.61** (right sign,
    robust); the spread **beats a placebo 80%** and **naive 60%** of folds (genuine information) — but
    beats a mean-growth **climatology only 40%**. Per-fold: it **caught the 2008 & COVID collapses** but
    *hurt* in calm years and **overshot the 2022** spread spike (no recession). **Regime-dependent skill** →
    not an unconditional keep. Both single-split and walk-forward agree on cut.
  - **Honesty note:** an early one-off probe (different data vintage) had looked like a KEEP; the committed,
    reproducible, pre-specified result is a narrow CUT. **Reported faithfully — did not tune settings to
    force the keep** (that would be the p-hacking this project condemns). The bar does not bend for the
    best-motivated story.
  - **Atlas feedback:** reuses Data Pipeline + Validation engines — no new graph node; graph unchanged
    (**175 nodes / 470 edges, 0-dangling**). New real dataset committed.
  - **CONVERGENCE (DONE again):** Macro⇄Finance resolved on real data (**sixth** distinct failure mode:
    regime-dependent skill). Ledger: **one coupling kept (Macro⇄Health); six cut**, five on real data under
    a placebo, six named failure modes. **+2 tests -> 100 pass.** Gates green: `pytest` (100) · `ruff` ·
    `mypy` (55 files) · graph 0-dangling · `mkdocs --strict`. Leaderboard Round 22 + convergence (DONE) +
    04-validation register updated.
  - **Next (Iter 28):** the six-domain sweep is convergence-complete. Options: a **seventh domain**, or
    consolidate — a **worked decision-support vignette** (welfare/equity dial + disagreement + honest
    uncertainty → "help a human choose", the north star), or hunt the nexus water-leg / a lead-lag finance
    spec if honestly motivated.
- **Iter 28 — 🧭 The north star, made concrete: a worked DECISION CARD (help a human choose, honestly).**
  - **Consolidation, not more breadth:** after six converged domains + deep validation machinery, this
    iteration connects it all to the *purpose* — supporting a human choosing a policy with eyes open.
  - **`experiments/decision_card.py`:** for a concrete question (what carbon price?), assembles the three
    things a single confident number hides: (1) **values are a dial** — utilitarian/prioritarian recommend
    50 $/t but a Rawlsian + tail-averse view recommends 100 $/t (the recommendation is *not*
    value-invariant); (2) **paradigms disagree** — on GDP at 100 $/t, CGE says **88** (pricing lowers
    output) while E3ME says **108** (pricing raises it), opposite signs, D≈0.10, **both reported, never
    averaged**; (3) **validation is disclosed** — the ensemble leans on couplings of which **6 of 7 failed
    real-data validation**, stated plainly. Bottom line: *decision-support under deep uncertainty, NOT a
    forecast.*
  - **Docs (north-star payoff):** new `docs/polyphony/decision-support.md` presents the worked card
    (values fork + paradigm disagreement table + real-data verdict table + the honest bottom-line
    paragraph) — the whole Polyphony thesis in miniature, contrasted with an "optimal carbon price = \$X"
    oracle headline. Added to nav.
  - **Atlas feedback:** a synthesis of existing engines (Welfare/Equity + the disagreement combiner +
    the validation ledger) — no new graph node; graph unchanged (**175 nodes / 470 edges, 0-dangling**).
  - **Convergence stays DONE** (consolidation, no new coupling). **+4 tests -> 104 pass.** Gates green:
    `pytest` (104) · `ruff` · `mypy` (56 files) · graph 0-dangling · `mkdocs --strict`.
  - **Next (Iter 29):** a **seventh domain** for further coverage, deepen the decision card (attach the
    honest predictive bands from Iter 25 to each candidate; disagreement-vs-carbon-price curve), or a
    lead-lag / crisis-conditional finance spec if honestly motivated (not to force a keep).
- **Iter 29 — 🚢 Seventh synergy loop: Trade⇄Emissions, carbon leakage (#12). KEEP on synthetic; real gap reopens convergence.**
  - **Scope is a floor:** extended to **Trade⇄Emissions** — the carbon-leakage / pollution-haven channel
    (Copeland-Taylor; Peters et al. 2011), central to border-carbon-adjustment policy.
  - **New voice `ReducedFormTrade`:** consumes production `emissions` (from the energy voice); as trade
    openness builds (globalisation relaxes toward a target), a fraction of production reappears as embodied
    carbon in imports, so **consumption-based** emissions rise above **production-based** — the leakage gap.
    Coupled contemporaneously (acyclic energy→trade; ADR-0005). DGPs: `synthetic_leakage_series` +
    `synthetic_no_leakage_series` (control).
  - **`experiments/tradeemissions.py`:** raw Δ +3.3; under **fair calibration** Δ **+17.3** with the **right
    sign** (corr(leakage, consumption) = +0.998); no-leakage control **cut** (Δ 0). **KEEP on synthetic,
    CUT on control.**
  - **Honest caveat:** synthetic keep = machinery. Opens a **new real-data gap** (#12-real) with an
    unusually clean target — **OWID publishes the production–consumption gap directly** (`trade_co2`).
    Convergence **REOPENED**.
  - **Atlas feedback (new coverage):** new **Trade / Carbon Leakage** domain (`d-trade`) + **MRIO** dossier
    (`docs/model-families/trade/mrio.md`, multi-regional input-output / consumption-based accounting —
    genuinely missing) + graph nodes `mrio` (model), `lenzen` (researcher); also linked existing `gtap` to
    `d-trade`. Nav + index + graph stats updated. **178 nodes / 475 edges, 0-dangling.**
  - **Tests:** +5 (`test_tradeemissions.py`) -> **109 pass.** Gates green: `pytest` (109) · `ruff` · `mypy`
    (58 files) · graph 0-dangling · `mkdocs --strict`. Leaderboard Round 23 + reopened convergence table +
    standing champion + 04-validation + related-work updated.
  - **Next (Iter 30):** close the gap — fetch **OWID World production vs consumption CO₂** (`co2`,
    `consumption_co2`, `trade_co2`, 35 yrs) and run a **placebo-controlled real Trade⇄Emissions tournament**
    (walk-forward): does trade openness / the leakage mechanism explain the real embodied-carbon gap beyond
    a trend + placebo? Report keep/cut honestly.
- **Iter 30 — 🚢 Real Trade⇄Emissions: carbon leakage is real but CUT (confounded-away). Convergence DONE again.**
  - **Key data insight:** the **World** aggregate can't test leakage (global trade nets to zero ⇒
    consumption = production). Used the **United Kingdom** — the textbook case (production CO₂ ~halved since
    1990 while consumption CO₂ fell far less).
  - **Fetched real data** (`fetch_real.fetch_trade` + `_fetch_owid_country_co2`): UK OWID production +
    consumption CO₂ + World Bank UK **trade openness** (`NE.TRD.GNFS.ZS`) as an **independent** leakage
    driver (using the observed gap would be circular) → `datasets/real_trade.csv` (34 yrs). Loader
    `load_real_trade`.
  - **Real tournament** (`experiments/real_trade_tournament.py`, walk-forward): corr(openness,
    consumption/production ratio) = **+0.81** (right sign — the UK gap really grew as it opened), but the
    openness-leakage term beats a **production-blind** baseline in **0% of folds** (and placebo/naive 0%).
    **Verdict CUT — "confounded-away":** the openness↔gap correlation is a **shared trend** (both rose
    1990–2023), not independent predictive info. The *average* leakage is real and trivially captured by
    production; its *openness-driven dynamics* aren't predictable beyond a trend.
  - **The lesson:** a genuine, policy-important phenomenon (UK carbon leakage is textbook) whose
    reduced-form mechanism still **fails the strict skill bar** — the bar doesn't bend for importance.
  - **Atlas feedback:** reuses Data Pipeline + Validation engines — no new graph node; graph unchanged
    (**178 nodes / 475 edges, 0-dangling**). New real dataset committed.
  - **CONVERGENCE (DONE again):** seven candidate couplings cut (six on real data), one kept
    (Macro⇄Health); no open improvable gap. **+2 tests -> 111 pass.** Gates green: `pytest` (111) · `ruff` ·
    `mypy` (59 files) · graph 0-dangling · `mkdocs --strict`. Leaderboard Round 24 + convergence (DONE) +
    04-validation register updated.
  - **Next (Iter 31):** an eighth domain, or deepen the decision card / a cross-domain disagreement study,
    or consolidate the seven-domain findings into a short synthesis page (the failure-mode catalogue as a
    teaching artifact).
- **Iter 31 — 📚 Consolidation: a VALIDATED failure-mode catalogue (how couplings fail on real data).**
  - **The intellectual payoff:** seven couplings tested on real data, one kept, six cut — and each cut
    names a distinct, reusable failure mode. This iteration turns that into a canonical, *tested* taxonomy.
  - **`experiments/failure_modes.py`:** a `CATALOGUE` of six failure modes (Level artifact · Genuinely
    cyclic · Wrong sign · Confounded-away · Real-signal-no-skill · Regime-dependent skill), each with a
    definition, the real-data diagnostic that detects it, and the lesson; plus a `LEDGER` mapping all eight
    couplings (1 kept + 7 cut) to their mode and decisive real number.
  - **Validated, not just prose:** `tests/test_failure_modes.py` checks internal consistency (kept=1,
    cut=7, all modes defined) AND — where the real data is present — re-runs the land/nexus/finance/trade
    tournaments and asserts each **live diagnostic matches its classified mode** (e.g. land: corr>0.5 &
    wrong sign; nexus: strong corr & loses to naive; finance: beats placebo but robust-cut; trade:
    corr>0.5 & robust-cut). The taxonomy is tied to reproducible computation.
  - **Finding:** **confounded-away (shared trend) is the modal failure** — three couplings (climate→GDP,
    the PM2.5 co-benefit, UK carbon leakage) fail this way, which is exactly why the placebo control is
    non-negotiable.
  - **Docs (teaching artifact):** new `docs/polyphony/failure-modes.md` — the ledger + a field guide to
    the six modes, cross-linked to the rounds, closing on why *one* success against *six* named failures is
    the honest yield of adversarial paradigm-plural simulation. Added to nav.
  - **Atlas feedback:** a synthesis of existing results — no new graph node; graph unchanged (**178 nodes /
    475 edges, 0-dangling**).
  - **Convergence stays DONE** (consolidation, no new coupling). **+6 tests -> 117 pass.** Gates green:
    `pytest` (117) · `ruff` · `mypy` (60 files) · graph 0-dangling · `mkdocs --strict`.
  - **Next (Iter 32):** an eighth domain, deepen the decision card (attach per-candidate honest bands /
    disagreement-vs-policy curve), or a cross-domain disagreement study.
- **Iter 32 — 🔀 Disagreement study: paradigm splits ACTIVATE with policy (deepening the reporting core).**
  - **The distinctive core, exercised:** Polyphony reports disagreement rather than averaging it. This
    study asks *when* the equilibrium (CGE) vs disequilibrium (E3ME) split on GDP matters, sweeping the
    carbon-price dial.
  - **`experiments/disagreement_study.py`:** at each carbon price, measures the disagreement index D and
    both paradigm answers. **Finding:** disagreement is small at zero policy (D ≈ 0.02) and **activates
    ~6×** the moment a carbon price bites (D ≈ 0.13 at cp=25), then **saturates** as the energy transition
    completes. At the peak the paradigms **straddle the baseline** — CGE says pricing lowers GDP (84.6),
    E3ME says it raises GDP (109.9), opposite signs, both reported.
  - **Decision-relevant lesson:** the choice of economic paradigm matters **most exactly where a real
    policy is contemplated** — so that is where the instrument raises a flag, not hides one. Disagreement
    is a *signal about where your beliefs are load-bearing*, not noise to smooth.
  - **Docs:** added a "When does the disagreement matter?" section (the activation table + lesson) to
    `docs/polyphony/decision-support.md`, deepening the decision card's paradigm-disagreement point.
  - **Atlas feedback:** uses the existing disagreement combiner (ADR-0004) — no new graph node; graph
    unchanged (**178 nodes / 475 edges, 0-dangling**).
  - **Convergence stays DONE.** **+3 tests -> 120 pass.** Gates green: `pytest` (120) · `ruff` · `mypy`
    (61 files) · graph 0-dangling · `mkdocs --strict`.
  - **Next (Iter 33):** an eighth domain, attach per-candidate honest predictive bands to the decision
    card, or extend the disagreement study to more quantities/couplings.
- **Iter 33 — 🌍 Panel fixed effects: confirming the modal cut (confounded-away) with cross-country power.**
  - **Chose depth over another domain:** the modal failure is *confounded-away* (a shared trend faking a
    mechanism). A cross-country **panel** with **two-way fixed effects** is the sharpest instrument against
    it — removing every country's level *and* every year's common shock isolates the within-country
    mechanism.
  - **Fetched a real panel** (`fetch_real.fetch_leakage_panel`, one bulk World Bank call + OWID): the
    consumption/production CO₂ **ratio** + **trade openness** for **114 countries × 32 years** (3,559 obs) →
    `datasets/real_leakage_panel.csv`. Loader `load_real_leakage_panel`.
  - **`experiments/panel_validation.py`** (`two_way_within` = iterative unit+time demeaning): pooled
    corr(openness, ratio) = **+0.30** (the naive leakage story) → **two-way-FE within corr = +0.025**
    (**92% attenuation**). **Verdict: cut-confirmed (confounded-away).** Openness has essentially no
    within-country effect on the emissions ratio once the shared global trend is removed — the Iter-30 UK
    cut, confirmed across 114 countries.
  - **Method validated, not just the datum:** synthetic-panel tests prove the FE estimator recovers truth
    (a pure confound demeans to ≈0; a real within-effect survives). Panel FE is now a reusable validation
    tool.
  - **Atlas feedback:** deepened the **Validation Engine** page with a **Panel fixed effects** row; failure-
    modes field guide updated with the panel confirmation. Reuses the Validation engine — no new graph node;
    graph unchanged (**178 nodes / 475 edges, 0-dangling**).
  - **Convergence stays DONE** (validation deepening). **+3 tests -> 123 pass.** Gates green: `pytest` (123)
    · `ruff` · `mypy` (62 files) · graph 0-dangling · `mkdocs --strict`. 04-validation register + Round-25
    narrative + validation-engine page + failure-modes updated.
  - **Next (Iter 34):** an eighth domain, apply panel FE to another confounded-away coupling (e.g. PM2.5→
    mortality across countries), or per-candidate honest bands on the decision card.
- **Iter 34 — 🌐 Panel FE, a contrasting case: it cannot recover the co-benefit (and that's the lesson).**
  - **Generalized the panel-FE tool** (`experiments/panel_validation.py` → sign-aware `PanelFEResult` +
    generic `_panel_fe`) and applied it to a **second** coupling: PM2.5 → all-cause mortality across
    **243 countries × 34 years** (8,262 obs; `fetch_pm25_mortality_panel`, two bulk World Bank calls;
    loader `load_real_pm25_mortality_panel`).
  - **Deliberate contrast:** leakage FE **cleanly confirms** the cut (pooled +0.30 → within +0.025, 92%
    attenuation). PM2.5→mortality FE **cannot recover** the effect — within corr is weak and even
    **wrong-signed (−0.14)**. Not because PM2.5 is harmless, but because **all-cause mortality is itself
    dominated by a confounded within-country trajectory** (development + aging) that fixing effects on the
    *driver* can't remove.
  - **The lesson (a limit of the method, stated as plainly as its success):** panel FE isolates a mechanism
    only when the **outcome** is not itself a confounded trend — re-confirming Iter 20's point that
    aggregate all-cause mortality is the wrong instrument for a real-but-small air-pollution effect (the
    properly-attributable GBD outcome is circular).
  - **Method still trustworthy:** the synthetic-panel tests (pure confound → 0; real within-effect survives)
    plus a new **contrast test** (FE confirms leakage, cannot recover the co-benefit) pin the behaviour.
  - **Atlas feedback:** reuses the Validation engine — no new graph node; graph unchanged (**178 nodes /
    475 edges, 0-dangling**). Two panel datasets committed.
  - **Convergence stays DONE.** **+3 tests -> 126 pass.** Gates green: `pytest` (126) · `ruff` · `mypy`
    (62 files) · graph 0-dangling · `mkdocs --strict`. 04-validation panel narrative + register updated.
  - **Next (Iter 35):** an eighth domain, per-candidate honest bands on the decision card, or a
    country-fixed-effects rescue attempt with a *clean* outcome (e.g. age-standardized mortality) if a
    non-circular source exists.
- **Iter 35 — 💵 Eighth coupling Energy⇄Inflation: the FIRST clean real-data KEEP. The bar rewards, not just cuts.**
  - **Balancing the ledger honestly:** seven couplings had been cut; this iteration tests one with a genuine
    chance of surviving — the energy→inflation pass-through (energy is a large CPI component + feeds core
    costs; the 1970s/2008/2022 episodes; central-bank-relevant).
  - **A reduced-form pass-through coupling** (regression, not a dynamical voice — an honest modeling choice):
    `experiments/inflation_tournament.py` fetches real IMF energy price index + US CPI (FRED, 32 yrs;
    `fetch_inflation`, loader `load_real_inflation`) and tests energy-price **growth** → inflation by
    walk-forward.
  - **Result — KEEP (robustly):** corr **+0.65** (right sign); beats a **mean baseline 100%**, **placebo
    75%**, **persistence 100%**, and **naive 100%** of walk-forward folds. Method validated synthetically
    (matched pass-through kept; independent control cut). The instrument's **first clean real-data keep**
    (Macro⇄Health is kept but its real test was underpowered).
  - **Why it matters:** the *same strict bar* that cut six plausible couplings **rewards** this genuinely
    skillful one — a **discriminating** instrument, not a destructive one. Ledger now **two kept, seven cut**.
  - **Atlas feedback (new coverage):** **FRB/US** dossier (`docs/model-families/economics/frbus.md`, the
    Fed's macroeconometric model — the empirical energy→inflation reference, genuinely missing) + graph nodes
    `frbus` (model), `fed` (institution). Nav + index + graph stats updated. **180 nodes / 480 edges,
    0-dangling.** Ledgers in `failure_modes.py` + `decision_card.py` (and the field-guide / decision-support
    pages) updated to two keeps / seven cuts.
  - **Tests:** +3 (`test_inflation_tournament.py`) + ledger-count updates -> **129 pass.** Gates green:
    `pytest` (129) · `ruff` · `mypy` (63 files) · graph 0-dangling · `mkdocs --strict`. Leaderboard Round 26
    + convergence (DONE, 2 keeps) + 04-validation + related-work updated.
  - **Next (Iter 36):** deepen the KEEP (a lead-lag / horizon study of energy→inflation), another
    plausible-keep domain, or per-candidate honest bands on the decision card.
- **Iter 36 — ⏱️ Energy⇄Inflation lead-lag: it forecasts one year ahead, then base-effects reverse it.**
  - **Deepened the keep honestly:** the Iter-35 keep tested the *contemporaneous* pass-through (a nowcast).
    The decision-relevant question is whether energy prices carry genuine **leading** information.
  - **`experiments/inflation_leadlag.py`:** lags energy-price growth by 0–3 years and re-runs walk-forward.
    **Finding:** skill is strong at **h=0** (corr +0.65) and **survives at h=1** (a genuine one-year-ahead
    forecast, corr +0.41, beats baselines) — then **decays and the sign flips by h=2** (corr −0.20). The
    **forecast horizon is 1 year**; the reversal is the classic **base effect** (a spike raises inflation
    now and lowers it ~2 years later as the level drops out).
  - **Economic content:** a real *short-horizon* forecaster, not a long-horizon one — matching central
    banks' doctrine of "looking through" transitory energy shocks. Reporting how far ahead the skill
    reaches (and where it reverses) is more honest than a bare "it predicts inflation".
  - **Atlas feedback:** reuses the Validation engine — no new graph node; graph unchanged (**180 nodes /
    480 edges, 0-dangling**).
  - **Convergence stays DONE.** **+2 tests -> 131 pass.** Gates green: `pytest` (131) · `ruff` · `mypy`
    (64 files) · graph 0-dangling · `mkdocs --strict`. Leaderboard Round 26 lead-lag deepening added.
  - **Next (Iter 37):** another plausible-keep domain (e.g. interest rate → housing), per-candidate honest
    bands on the decision card, or a cross-coupling meta-analysis of what distinguishes the two keeps from
    the seven cuts.
- **Iter 37 — 🔬 Meta-analysis: only "beats the honest baseline" separates keeps from cuts.**
  - **The synthesis question:** with two keeps and seven cuts, *which property* actually decides? Scored
    every coupling on four plausible discriminators (`experiments/meta_analysis.py`): right sign, beats
    placebo, beats naive, beats baseline.
  - **Finding (sharp, slightly surprising):** **only `beats_baseline` perfectly separates** keep from cut.
    The right sign is nearly useless (**6 of 7 cuts have it**); beating a placebo and beating naive each
    admit exactly **one false positive — Macro⇄Finance**, which clears all three yet is cut because its
    regime-dependent skill doesn't beat the mean-growth baseline. So sign / placebo / naive are each
    necessary-ish but **not sufficient**; out-predicting the honest baseline is the one decisive test — the
    project's whole discipline compressed into a single computed fact.
  - **Validated:** `tests/test_meta_analysis.py` asserts the perfect separator, the sign's poverty as a
    discriminator, and Macro⇄Finance as the instructive false positive.
  - **Docs:** added a "What actually separates keeps from cuts" section (the discriminator table + the
    Macro⇄Finance lesson) to `docs/polyphony/failure-modes.md`.
  - **Atlas feedback:** a synthesis of existing results — no new graph node; graph unchanged (**180 nodes /
    480 edges, 0-dangling**).
  - **Convergence stays DONE.** **+5 tests -> 136 pass.** Gates green: `pytest` (136) · `ruff` · `mypy`
    (65 files) · graph 0-dangling · `mkdocs --strict`.
  - **Next (Iter 38):** another plausible-keep domain (interest rate → housing) to further probe the bar,
    per-candidate honest bands on the decision card, or extend the meta-analysis with a numeric
    effect-size margin per coupling.
- **Iter 38 — 🏠 Ninth domain Interest-Rate⇄Housing: CUT via a NEW failure mode (reverse causation + momentum).**
  - **Probed the bar with a policy-central coupling** (monetary policy → house prices) that could plausibly
    keep — and found a *seventh distinct* failure mode.
  - **Fetched real data** (`fetch_housing`; loader `load_real_housing`): 30-yr mortgage rate (FRED
    MORTGAGE30US) + Case-Shiller HPI (CSUSHPINSA), 37 yrs. `experiments/real_housing_tournament.py`.
  - **Result — CUT on two counts a bare correlation hides:** (1) **reverse causation** — the contemporaneous
    corr is **+0.38 (wrong sign)** because the Fed hikes *into* booms (the policy reacts to the outcome);
    (2) the correctly-signed **lagged** rate (−0.27) can't beat a **persistence/momentum** baseline (0% of
    folds) — house-price growth is highly autocorrelated. Failing to beat the honest baseline is decisive
    (the Iter-37 rule).
  - **New failure mode #7 — reverse causation / policy endogeneity:** *when the lever reacts to the target,
    the naive correlation is backwards; use lags, and beware momentum baselines.* Added to the catalogue.
  - **Ledgers propagated:** `failure_modes.py` (7 modes, +Interest-Rate⇄Housing → reverse-causation),
    `meta_analysis.py` (+row; right-sign false positives now 7 of 8), `decision_card.py` (+cut) — with all
    three tests + the field-guide / decision-support / leaderboard / 04-validation pages updated to **two
    keeps, eight cuts**.
  - **Atlas feedback:** reuses Data Pipeline + Validation (rate/housing sits in existing d-economics) — no
    new graph node; graph unchanged (**180 nodes / 480 edges, 0-dangling**). New real dataset committed.
  - **Convergence stays DONE.** **+2 tests -> 138 pass.** Gates green: `pytest` (138) · `ruff` · `mypy`
    (66 files) · graph 0-dangling · `mkdocs --strict`. Leaderboard Round 27 + convergence + 04-validation +
    failure-modes (new mode) updated.
  - **Next (Iter 39):** per-candidate honest bands / effect-size margins on the meta-analysis, another
    domain, or an instrumental-variable rescue attempt for the housing reverse-causation (if a clean
    instrument exists).
- **Iter 39 — 📖 Rewrote the Polyphony landing page as a current "state of the ensemble" (holistic entry point).**
  - **The landing `index.md` was a stale Phase-0 stub** — it described the *method* but none of the
    *results*. Rewrote it as the crisp synthesis a newcomer reads first.
  - **New sections:** *The result so far* (the full ten-coupling verdict table — two kept, eight cut, with
    each cut's failure mode); *Why so few keeps is the point* (the discriminating-not-destructive framing +
    the meta-analysis punchline); *How a coupling earns its keep* (the bar + the six validation methods);
    the decision-card payoff; an updated document table and *Coverage & status* (10 domains, 180-node graph,
    130+ green tests); Phases 0–4 done, Phase 5 (scale) ongoing.
  - **Fixed accumulated count drift:** reconciled the ledger counts to the tested source of truth (**two
    kept, eight cut, ten couplings**) across `index.md`, `decision-support.md` ("eight of ten"; +the housing
    row), matching `decision_card.honest_summary()` ("8 of 10") and the pinned `failure_modes`/`meta_analysis`
    tests.
  - **Atlas feedback:** docs synthesis — no code/graph change; graph unchanged (**180 nodes / 480 edges,
    0-dangling**).
  - **Convergence stays DONE.** Gates green: `pytest` (138) · `ruff` · `mypy` (66 files) · graph 0-dangling ·
    `mkdocs --strict`.
  - **Next (Iter 40):** numeric effect-size margins on the meta-analysis, per-candidate honest bands on the
    decision card, or another domain under the same bar.
- **Iter 40 — ⚖️ Decision card: is the *choice* robust to the paradigm? (here yes — a useful honesty in both directions.)**
  - **Deepened the north-star artifact:** the decision card showed the paradigms disagree on the GDP *level*;
    this adds whether they disagree on the *recommended policy*. Parameterized `welfare_frontier` by
    `paradigm` (equilibrium = CGE-only, disequilibrium = E3ME-only, both) and computed the utilitarian
    recommendation **within each worldview**.
  - **Finding:** the paradigms disagree sharply on the GDP level (CGE 88 vs E3ME 108, even opposite-signed
    carbon-price effects) but **agree on the recommended carbon price (cp=50)** — because the welfare ranking
    is driven by the abatement-cost ↔ climate-risk trade-off both share. **The *choice* is robust to the
    equilibrium-vs-disequilibrium debate even though the projected *level* is not** — honesty in both
    directions (flag the disagreement, but also say when it doesn't change the decision). The recommendation
    still flips with **values**, so here the load-bearing uncertainty is *ethical, not paradigmatic*.
  - **`decision_card`:** new `recommendation_by_paradigm` + `paradigm_recommendations_agree`; `honest_summary`
    now states whether the choice flips with the paradigm.
  - **Validated:** `test_decision_card.py` asserts the paradigms disagree on the level yet agree on the
    choice, while values still change it.
  - **Atlas feedback:** reuses the welfare + disagreement engines — no new graph node; graph unchanged
    (**180 nodes / 480 edges, 0-dangling**).
  - **Convergence stays DONE.** **+1 test -> 139 pass.** Gates green: `pytest` (139) · `ruff` · `mypy`
    (66 files) · graph 0-dangling · `mkdocs --strict`. decision-support page updated.
  - **Next (Iter 41):** numeric effect-size margins on the meta-analysis, another domain, or a
    values-vs-paradigm sensitivity sweep (which uncertainty is load-bearing for which questions).
- **Iter 41 — 🎚️ Sensitivity analysis: which uncertainty is load-bearing? (values, not paradigm, here.)**
  - **Generalized Iter 40 into a tool:** `experiments/sensitivity_analysis.py` builds the full
    recommendation grid over **value setting × economic paradigm** (3×2) and reports how many distinct
    policies each axis produces.
  - **Finding (sharp + actionable):** for the carbon-price question, varying **values** yields **two**
    distinct policies (cp=50 vs cp=100) while varying the **paradigm** yields **one** →
    `dominant_uncertainty = "values (ethical)"`. The recommendation is fully invariant to the
    equilibrium-vs-disequilibrium debate but changes with the welfare weighting. The card can now point a
    decision-maker's scarce attention at the axis that *actually moves the choice* — a sharper honesty than a
    bare disagreement index ("the models disagree" → "**your values decide this one, not the economics**").
  - **Validated:** `test_sensitivity_analysis.py` asserts value_sensitivity=2, paradigm_sensitivity=1,
    dominant = values.
  - **Docs:** added the recommendation-grid table + the load-bearing-uncertainty reading to
    `docs/polyphony/decision-support.md`.
  - **Atlas feedback:** reuses the welfare + paradigm machinery — no new graph node; graph unchanged
    (**180 nodes / 480 edges, 0-dangling**).
  - **Convergence stays DONE.** **+2 tests -> 141 pass.** Gates green: `pytest` (141) · `ruff` · `mypy`
    (67 files) · graph 0-dangling · `mkdocs --strict`.
  - **Next (Iter 42):** a question where the *paradigm* IS load-bearing (to show the analysis cuts both
    ways), numeric effect-size margins on the meta-analysis, or another domain.
- **Iter 42 — ↔️ Sensitivity analysis cuts BOTH ways: cheap green tech makes the paradigm load-bearing too.**
  - **Validated the tool discriminates** (isn't rigged to always credit "values"). Threaded two scenario
    knobs through `welfare_frontier` — `abate_k` (near-term abatement-cost intensity) and `risk_weight`
    (climate-tail valuation) — so a policy *question* can be varied, not just the answer.
  - **Finding:** in a **cheap-green-tech** scenario (`cheap_green_tech_scenario`, low `abate_k`), the
    carbon-price→GDP *sign* — on which the paradigms disagree — starts to move the recommendation, and
    **paradigm-sensitivity rises from 1 (default question) to 2**. So the analysis genuinely cuts both ways:
    *when* the economics is load-bearing, it says so. (Values still matter via the fixed income
    distribution, so this is "both matter" not "paradigm alone" — an honest limit noted in the docstring.)
  - **Validated:** `test_sensitivity_analysis.py` asserts the default question is values-dominant
    (paradigm-sensitivity 1) while cheap green tech lifts paradigm-sensitivity to 2.
  - **Docs:** added the "cuts both ways" note to `docs/polyphony/decision-support.md`.
  - **Atlas feedback:** reuses the welfare machinery (now scenario-parameterized) — no new graph node; graph
    unchanged (**180 nodes / 480 edges, 0-dangling**).
  - **Convergence stays DONE.** **+1 test -> 142 pass.** Gates green: `pytest` (142) · `ruff` · `mypy`
    (67 files) · graph 0-dangling · `mkdocs --strict`.
  - **Next (Iter 43):** numeric effect-size margins on the meta-analysis, another domain, or a
    scenario-atlas of which uncertainty is load-bearing across several stylized policy questions.
- **Iter 43 — 🛡️ Red-team of the Energy⇄Inflation keep: it survives (not a 2022-spike artifact).**
  - **Hardened the core, not the periphery:** the one clean real-data keep had never been adversarially
    attacked. `experiments/redteam_inflation.py` runs three attacks.
  - **The decisive attack — remove the most extreme energy-move year (the 2022 spike)** and re-run
    walk-forward: the pass-through **still beats the baseline and naive in every fold** →
    `survives_outlier_attack = True`. The keep is **not** a single-episode artifact — the obvious objection
    is defeated.
  - **Sub-period stability:** stable in the **recent** half (100% of folds); the **early** half is weaker
    (50%) — a *disclosed* small-sample fragility (few folds, lower 1990s energy volatility), reported not
    hidden. A keep with its fragilities named, still standing.
  - **Validated:** `test_redteam_inflation.py` asserts the keep survives the outlier attack and that the
    early half is honestly weaker than the recent half.
  - **Atlas feedback:** reuses the Validation engine — no new graph node; graph unchanged (**180 nodes /
    480 edges, 0-dangling**).
  - **Convergence stays DONE.** **+2 tests -> 144 pass.** Gates green: `pytest` (144) · `ruff` · `mypy`
    (68 files) · graph 0-dangling · `mkdocs --strict`. Leaderboard Round 26 red-team + 04-validation register
    updated.
  - **Next (Iter 44):** red-team Macro⇄Health's real-data footing / the other keep, numeric effect-size
    margins on the meta-analysis, or another domain.
- **Iter 44 — 🔢 A pinned "state of the ensemble" — the tested source of truth for the headline counts (anti-drift).**
  - **Probed Okun's law (Employment⇄Output)** as a possible 11th domain / 3rd keep: corr(Δunemployment,
    GDP growth) = **−0.81** (textbook-strong, right sign) but it **fails to beat a climatology baseline**
    out-of-sample (44% of walk-forward folds, n=76) — because unemployment is a **coincident** indicator
    (two measures of one business cycle), not a leading one. A would-be cut mapping to an *existing* mode
    (real-signal-no-skill); **not added** — the ledger-propagation cost outweighed the marginal insight
    (an honest call about diminishing returns).
  - **Instead, fixed a real robustness gap** (the count drift found in Iter 39): added
    `failure_modes.state_of_ensemble()` + `VALIDATION_METHODS` — a **single tested source of truth** computed
    from the ledger/catalogue (10 couplings · 2 kept · 8 cut · 7 failure modes · 6 validation methods), never
    hand-typed. `tests/test_failure_modes.py` pins it; the landing page now cites it with a reproduce
    pointer, so the docs cannot silently diverge from the code again.
  - **Atlas feedback:** reuses existing ledgers — no new graph node; graph unchanged (**180 nodes / 480
    edges, 0-dangling**).
  - **Convergence stays DONE.** **+1 test -> 145 pass.** Gates green: `pytest` (145) · `ruff` · `mypy`
    (68 files) · graph 0-dangling · `mkdocs --strict`. Landing page (`index.md`) reproduce pointer added.
  - **Next (Iter 45):** red-team the Macro⇄Health keep on real footing, numeric effect-size margins for the
    walk-forward-decided couplings, or another genuinely distinct domain.
- **Iter 45 — ⚖️ Not all keeps are equal: distinguish the two keeps' evidential status (a self-audit honesty fix).**
  - **The self-critical finding:** the ledger listed **two keeps as equal**, but Energy⇄Inflation is
    validated on **real data** (+ red-team) whereas Macro⇄Health is kept on **synthetic** data + red-team
    with an **underpowered real test** (≈1 pandemic event). The project's own ethos — *a synthetic keep is a
    hypothesis, not a result* — demands the ledger record that difference, not flatten it.
  - **`failure_modes`:** added an `evidence` field to `CouplingVerdict` + a `real_data_keeps()` helper →
    **two keeps, but only one (Energy⇄Inflation) real-data-validated.** Also flagged the Energy⇄climate
    cut as synthetic.
  - **Honest caveat propagated to the meta-analysis:** the "only beats-baseline separates keeps from cuts"
    claim rests on *real* evidence for Energy⇄Inflation + the seven real cuts, plus *synthetic* evidence for
    Macro⇄Health — flagged in the field guide rather than hidden.
  - **Validated:** `test_failure_modes.py` asserts only one keep is real-data-validated and that
    Macro⇄Health's evidence says "underpowered". Docs (index result table, failure-modes "what survived" +
    separator caveat) updated to distinguish the keeps.
  - **Atlas feedback:** reuses existing ledgers — no new graph node; graph unchanged (**180 nodes / 480
    edges, 0-dangling**).
  - **Convergence stays DONE.** **+1 test -> 146 pass.** Gates green: `pytest` (146) · `ruff` · `mypy`
    (68 files) · graph 0-dangling · `mkdocs --strict`.
  - **Next (Iter 46):** attempt a concrete (even if underpowered) real Macro⇄Health test around COVID-2020
    to make the "underpowered" claim demonstrated rather than asserted, or another distinct domain.
- **Iter 46 — 📏 The keeps-vs-cuts separator, on REAL evidence alone (numeric, addressing the Iter-45 caveat).**
  - **Motivation:** Iter 45 flagged that the meta-analysis's boolean "beats-baseline separates keeps from
    cuts" leaned partly on Macro⇄Health's *synthetic* baseline-beating. This strengthens it to a **numeric**
    separator using **real data only**.
  - **`experiments/real_margins.py`:** for the four couplings decided by walk-forward on real data, pulls
    the live fraction of folds each beats its honest baseline — **Energy⇄Inflation (keep) 100%**,
    Macro⇄Finance 40%, Trade⇄Emissions 0%, Interest-Rate⇄Housing 0%. The keep clears the 50% line; every cut
    falls below it → `separator_holds_on_real_data()` is True. The separator is clean **without** the
    synthetic Macro⇄Health evidence — the Iter-45 caveat is answered, not just noted.
  - **Validated:** `test_real_margins.py` asserts the keep clears the line and every cut falls below it.
    Field-guide caveat updated with the numeric real-data confirmation.
  - **Atlas feedback:** reuses the real tournaments — no new graph node; graph unchanged (**180 nodes / 480
    edges, 0-dangling**).
  - **Convergence stays DONE.** **+2 tests -> 148 pass.** Gates green: `pytest` (148) · `ruff` · `mypy`
    (69 files) · graph 0-dangling · `mkdocs --strict`.
  - **Next (Iter 47):** a concrete demonstration of the Macro⇄Health real-data underpowering (one-pandemic
    unidentifiability), or another distinct domain.
- **Iter 47 — 🦠 Macro⇄Health underpowering, DEMONSTRATED (not asserted) — completing the honesty arc.**
  - **`experiments/real_macrohealth.py`:** turns the "real test underpowered" claim into a computed fact via
    two independent structural reasons:
    1. **One pandemic episode.** The modern GDP era has exactly **one** output-shock pandemic (COVID,
       2020–2023, a single contiguous block), so you cannot learn the coupling on one occurrence and test it
       on another → `identifiable_out_of_sample = (episodes ≥ 2)` is **False**. (A multi-year episode can
       straddle one fold boundary — 2020 in train, 2022 in test — but that is *within-episode* re-testing,
       not independent validation.)
    2. **Near-zero in-sample relationship.** At **annual** resolution corr(severity, GDP growth) = **−0.02**
       — 2021 had the *most* deaths *and* strong recovery growth, because the 2020 collapse came from
       lockdowns, not deaths directly (a timing confound). So the coupling that is clean *by construction* on
       synthetic data is neither cross-validatable nor even strongly present in-sample on real annual data.
  - **Closes the Iter 45–47 honesty arc:** Iter 45 flagged the two keeps' unequal footing; Iter 46 confirmed
    the separator on real evidence alone; Iter 47 now **demonstrates** exactly why Macro⇄Health's real
    footing is thin. The synthetic keep remains honest machinery, its limits fully explicit.
  - **Validated:** `test_real_macrohealth.py` asserts one episode / not identifiable / weak in-sample.
  - **Atlas feedback:** reuses the committed real GDP series + documented CDC COVID deaths — no new graph
    node; graph unchanged (**180 nodes / 480 edges, 0-dangling**).
  - **Convergence stays DONE.** **+2 tests -> 150 pass.** Gates green: `pytest` (150) · `ruff` · `mypy`
    (70 files) · graph 0-dangling · `mkdocs --strict`. 04-validation register updated.
  - **Next (Iter 48):** a genuinely distinct new domain, or a further robustness/coverage pass if one is
    worth the propagation.
- **Iter 48 — 📈 Higher-power confirmation: the Energy⇄Inflation keep holds at QUARTERLY frequency.**
  - **Strengthened the one solid real result.** The keep rested on annual data (~4 walk-forward folds — a
    fair low-power worry). Re-ran the *same* pass-through test at **quarterly** frequency.
  - **Fetched quarterly data** (`fetch_inflation_quarterly` + `_fetch_fred_quarterly`): FRED energy price
    index + US CPI, quarterly means → `datasets/real_inflation_q.csv` (137 quarters). Loader
    `load_real_inflation_q`; `experiments/inflation_quarterly.py` reuses the annual `_score` on annualized
    QoQ growth with **8 folds**.
  - **Result — KEEP holds, with more power:** 136 quarters, **8 folds** (double the annual), a **stronger**
    contemporaneous correlation (**0.72** vs 0.65), beating baseline **88%**, placebo **75%**, persistence
    **75%**, naive **75%** of folds. The keep is **not** an artifact of low-power annual data — it is the
    project's most solidly established real-data result.
  - **Validated:** `test_inflation_quarterly.py` asserts ≥6 folds, right sign, and a robust keep across all
    baselines. Leaderboard Round 26 updated with the higher-power confirmation.
  - **Atlas feedback:** reuses the inflation machinery — no new graph node; graph unchanged (**180 nodes /
    480 edges, 0-dangling**). New quarterly dataset committed.
  - **Convergence stays DONE.** **+1 test -> 151 pass.** Gates green: `pytest` (151) · `ruff` · `mypy`
    (71 files) · graph 0-dangling · `mkdocs --strict`.
  - **Next (Iter 49):** a genuinely distinct new domain, a monthly/lead-lag deepening of the keep, or a
    consolidation pass.
- **Iter 49 — 🎯 Is the keep also *calibrated*? Yes — accurate AND honest (the mirror image of the cuts).**
  - **Completed the uncertainty picture.** Iter 24 showed the *cut* couplings are inaccurate AND grossly
    **overconfident** (PIT at the tails). The complementary question — is the coupling that *clears* the bar
    also honest about its uncertainty? — had never been asked.
  - **`experiments/inflation_probabilistic.py`:** scores the Energy⇄Inflation keep's predictive distribution
    (pass-through point + train-residual ensemble) vs an honest persistence naive, via **CRPS** + **PIT**.
    (The target is a growth rate that can go negative, so the log-trend scorer used for the level-target cuts
    doesn't apply — a small correct scorer was needed.)
  - **Result — accurate AND calibrated:** CRPS coupled **0.89** beats naive **1.21**, and the **PIT is
    centred** (mean 0.55) with ~**50%** central coverage (well-dispersed). So the one coupling that earns its
    keep is trustworthy in *both* dimensions — the exact mirror of the cuts (wrong *and* overconfident).
    Skill and honest uncertainty travel together here, as they should.
  - **Validated:** `test_inflation_probabilistic.py` asserts the keep beats naive on CRPS and is calibrated.
    04-validation register updated.
  - **Atlas feedback:** reuses the CRPS/PIT metrics + inflation machinery — no new graph node; graph
    unchanged (**180 nodes / 480 edges, 0-dangling**).
  - **Convergence stays DONE.** **+1 test -> 152 pass.** Gates green: `pytest` (152) · `ruff` · `mypy`
    (72 files) · graph 0-dangling · `mkdocs --strict`.
  - **Next (Iter 50):** a genuinely distinct new domain, or a consolidation/polish pass.
- **Iter 50 — 🧭 Milestone: the central generalization, stress-tested against two famous macro relationships.**
  - **Probed two celebrated indicators** and captured the result as tested "additional probes"
    (`experiments/additional_probes.py`, without heavy LEDGER propagation): **Okun's law** (Δunemployment↔
    growth, corr **−0.81**, *coincident*) and the **yield curve** (10Y−3M term spread → next-year growth,
    the classic *leading* recession indicator). Also probed the yield curve on *annual recession* (binary),
    which fails too — recessions are rare (14% base rate; "never-recession" is 86% accurate) and annual
    averaging destroys the monthly inversion signal.
  - **Both CUT** (beat climatology in 44% / 40% of walk-forward folds). Neither a famously strong coincident
    relationship nor a famously reliable leading one clears the bar for **annual growth**.
  - **The central generalization, now stress-tested and articulated** (capstone in the field guide):
    *reduced-form couplings on annual aggregate targets almost never beat a climatology baseline.* The sole
    keep — **Energy⇄Inflation** — is the exception that proves the rule: it works because energy is a
    **large, mechanical, contemporaneous component of the CPI**, not because it forecasts an otherwise
    unforecastable series.
  - **Validated:** `test_additional_probes.py` asserts Okun's strong-but-cut, the yield curve's cut, and
    the generalization (`only_mechanical_component_keeps()`). Field guide capstone section added.
  - **Atlas feedback:** reuses the walk-forward machinery — no new graph node; graph unchanged (**180 nodes
    / 480 edges, 0-dangling**). Two probe datasets committed.
  - **Convergence stays DONE.** **+3 tests -> 155 pass.** Gates green: `pytest` (155) · `ruff` · `mypy`
    (73 files) · graph 0-dangling · `mkdocs --strict`.
  - **Next (Iter 51):** the project is intellectually complete — the central finding is stress-tested and
    articulated. Options: a non-aggregate (panel/micro) domain where the generalization might *not* hold, or
    a consolidation/polish pass.
