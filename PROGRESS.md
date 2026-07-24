# Program Tracker — The Atlas of Computational Policy Simulation

Program-director view of scope, status, and the definition of done. Updated every
work iteration. (Site-facing status also lives at `docs/status.md`.)

## Definition of Done

The loop completes when **all** of the following hold:

- [ ] **D1 — Content depth.** Every model page promoted from *stub* to at least
      **Bronze** (all 18 dossier sections filled, concise but real). Flagships reach
      **Gold** (DICE-level rigor).
- [x] **D2 — Synergy artifacts. ✅ COMPLETE.** All 10 comparison matrices written as real
      chapters **(✅ 10/10)**; all architecture patterns detailed **(✅ 16/16)**; the
      knowledge graph built as data (`graph.json`, 93 nodes / 142 edges) + rendered views
      **(✅ done)**.
- [ ] **D3 — Build health.** `mkdocs build --strict` stays green (0 warnings) at every commit.
- [ ] **D4 — Deploy pipeline.** GitHub Actions workflow in place; site builds
      deploy-ready. ✅ (pipeline ready — see below)
- [x] **D5 — Published.** ✅ **LIVE** at
      <https://sour-abh-raj.github.io/computational-policy-atlas/> — repo
      `Sour-abh-Raj/computational-policy-atlas` (public). Owner authenticated gh once
      (`gh auth login --with-token`); the deploy workflow now auto-redeploys on push
      to `main`. **Owner reminder: rotate the token whenever you choose.**

## Maturity ladder (per page)

| Level | Bar |
|-------|-----|
| Stub | Positioning card + facts + TODO sections |
| **Bronze** | All 18 sections filled, concise, ≥3 primary citations |
| **Silver** | Equations/architecture diagrams, criticisms with citations |
| **Gold** | DICE-level: full math, Mermaid architecture, ecosystem, simulator lesson |

## Status board

| Family | Pages | Stub | Bronze+ | Gold |
|--------|------:|-----:|--------:|-----:|
| Climate IAM | 9 | 0 | 7 (FUND, PAGE, MESSAGEix, REMIND, IMAGE, WITCH, AIM) | 2 (DICE, GCAM) ✅ **family complete** |
| Energy | 5 | 0 | 3 (PyPSA, Calliope, EnergyPLAN) | 2 (OSeMOSYS, TIMES) ✅ **family complete** |
| Economics | 7 | 2 | 3 (Input-Output, GTAP, E3ME) | 2 (CGE, DSGE) |
| Transport | 4 | 3 | 0 | 1 (MATSim) |
| Urban | 3 | 3 | 0 | 0 |
| Agriculture | 4 | 3 | 0 | 1 (GLOBIOM) |
| Water | 3 | 3 | 0 | 0 |
| Health | 3 | 2 | 0 | 1 (Covasim) |
| Frameworks | 7 | 6 | 0 | 1 (Vensim/SD) |
| Methods/Algorithms | 8 | 6 | 2 (LP, MILP) | 0 |
| **Synergy** | matrices **10/10** ✅ · patterns **16/16** ✅ · graph **1/1** ✅ — **D2 DONE** | | | |

## Iteration log

- **Iter 0** — Scaffold + DICE (Gold) + 52 stubs; strict build green (64 pages).
- **Iter 1** — Deploy pipeline (GitHub Actions), program tracker, OSeMOSYS → Gold
  (the bottom-up LP contrast to DICE).
- **Publish** — Repo created (public) and **site went live on GitHub Pages**:
  <https://sour-abh-raj.github.io/computational-policy-atlas/>. D5 cleared.
- **Iter 2** — TIMES → Gold (completes DICE↔OSeMOSYS↔TIMES optimization triangle);
  first synergy chapter **Optimization vs Simulation** (full comparative essay + matrix).
  Matrices 1/10. Pushed → auto-redeploys live.
- **Iter 3** — CGE → Gold (economics/equilibrium spine, Market Engine pattern); second
  matrix **Top-Down vs Bottom-Up** (energy-economy gap, hybrid synthesis). Matrices 2/10.
- **Iter 4** — DSGE → Gold (completes equilibrium trio; Lucas critique, NK 3-equation
  model, HANK); third matrix **Equilibrium vs Disequilibrium** (the coordination
  assumption; CGE/DSGE vs E3ME/ABM). Matrices 3/10.
- **Iter 5** — Pivot to the **simulation hemisphere**: Covasim → Gold (first Gold ABM;
  structure-of-arrays agents, contact-layer transmission, intervention objects, ensemble
  outputs); fourth matrix **ABM vs CGE** (emergence vs equilibrium — now with a Gold ABM
  and Gold CGE as referents). Matrices 4/10.
- **Iter 6** — Vensim/**System Dynamics** → Gold (stock-flow-feedback paradigm; World3/
  Limits-to-Growth lineage; ODE integration; sensitivity/calibration engines); fifth
  matrix **System Dynamics vs Agent-Based** (aggregate feedback vs individual interaction;
  Vensim vs Covasim). Completes the simulation-paradigm spine. Matrices 5/10.
- **Iter 7** — Opened the **Architecture Patterns** layer: 7 detailed engine pages
  (Scenario, Optimization, Market, Behavior, Integration/stock-flow, Sensitivity,
  Calibration), each with intent/forces/structure/interface/exemplars/simulator-lesson and
  cross-linked to the Gold dossiers that exhibit them. Patterns 7/15.
- **Iter 8** — Two domain-engine pattern pages with Gold referents: **Climate Engine**
  (reduced-order emulator; DICE boxes, FAIR/MAGICC) and **Energy Dispatch Engine**
  (least-cost RES/model-generator; OSeMOSYS/TIMES/PyPSA). Patterns 9/15.
- **Iter 9** — Built the **knowledge graph** as a data artifact: `docs/graph/graph.json`
  (80 typed nodes, 106 typed edges, 0 dangling refs — validated) + rewrote `graph/index.md`
  with rendered views (paradigms→models, models→patterns, algorithms→patterns), four worked
  relational queries, and live stats. **Graph 1/1 ✅** — last empty D2 slot cleared.
- **Iter 10** — Sixth matrix **IAM vs Energy-System Models** (the same climate problem at
  two scales; cost-benefit DICE vs bottom-up TIMES/OSeMOSYS — all-Gold referents; SCC↔target
  and cost-curve↔MAC handshake; process-based IAMs as the synthesis). Matrices 6/10.
- **Iter 11** — Double-leverage: seventh matrix **LP vs MILP** (the price of an integer —
  convexity/duality lost with integrality; why OSeMOSYS/TIMES stay LP) **+** promoted the
  **LP** and **MILP** algorithm pages from stub → Silver method dossiers (same material).
  Matrices 7/10; first 2 algorithm stubs cleared (D1 breadth begins).
- **Iter 12** — Eighth matrix **Recursive-Dynamic vs Perfect Foresight** (Taxonomy Axis 4;
  clairvoyant intertemporal optimum vs myopic period-by-period stepping; lock-in & stranded
  assets; DICE/TIMES vs recursive CGE/GCAM; foresight-as-a-dial). Matrices 8/10.
- **Iter 13** — **Completed the comparative layer**: ninth matrix **Deterministic vs
  Stochastic** (Axis 5; expected path vs distribution; tails/Weitzman; DICE/CGE vs
  DSGE/Covasim) + tenth matrix **Continuous vs Discrete** (Axis 6; ODE densities vs countable
  agents/events; epidemic extinction; mean-field limit; Vensim vs Covasim). Rebuilt the
  comparative hub as a 10-row index with the "recurring lesson." **Matrices 10/10 ✅.**
- **Iter 14** — Opened the **transport domain**: **MATSim** → Gold (co-evolutionary user
  equilibrium — "equilibrium by learning, not assumption"; queue MobSim; Charypar–Nagel
  scoring; event-stream architecture) **+** wrote the **Spatial Engine** pattern it grounds
  (grid vs network geometry; MATSim/SWAT/MODFLOW referents). Patterns 10/15; graph grown to
  82 nodes / 111 edges (MATSim + Spatial Engine wired in).
- **Iter 15** — Two **cross-cutting patterns** (no new dossier; grounded across the 8 Gold
  models): **Policy Engine** (instruments as composable objects — price/quantity/standard/
  behavioral injection points) and **Validation Engine** (fit≠validity; backcasting,
  extreme-condition, cross-model battery). Patterns 12/16; graph 84 nodes / 117 edges.
  *(Note: pattern catalog is 16, not 15 — the Integration/Stock-Flow engine was added as a
  distinct core engine during Iter 7.)*
- **Iter 16** — Two **infrastructure patterns** (cross-cutting, no new dossier):
  **Visualization Engine** (comparison + uncertainty as defaults; En-ROADS live loop) and
  **Data Pipeline** (ingest→clean→**balance**→build; SAM/RES/synthetic-population; shared
  harmonized substrate for multi-domain coupling). Patterns 14/16 — only the two
  domain-gated engines (Technology-Adoption ← GCAM, Land ← GLOBIOM/MAgPIE) remain. Graph 86
  nodes / 121 edges.
- **Iter 17** — Opened the **agriculture & land domain**: **GLOBIOM** → Gold (spatial
  partial-equilibrium land-use; STJ surplus-max = market equilibrium; Simulation Units;
  biophysical–economic coupling via EPIC/G4M; LUC emissions → climate) **+** the **Land
  Engine** pattern it grounds (finite land as a shared contested account). Patterns 15/16 —
  only Technology-Adoption (← Gold GCAM) remains. Graph 90 nodes / 131 edges.
- **Iter 18 — 🎉 D2 COMPLETE.** **GCAM** → Gold (process-based IAM; partial-equilibrium
  price search; **nested-logit market share**; Hector climate; recursive-dynamic; the
  detailed-IAM synthesis of cost-benefit + bottom-up) **+** the final **Technology-Adoption
  Engine** pattern (logit share vs knife-edge least cost; vintage turnover; β dial).
  **Patterns 16/16 ✅.** With matrices 10/10 and the graph done, the entire **synergy layer
  (D2) is finished**. Graph 93 nodes / 142 edges. Loop now pivots to D1 breadth.
- **Iter 19 — D1 breadth begins.** **FUND** and **PAGE** → Bronze (all 18 sections filled),
  completing the **cost-benefit IAM trio** with DICE: FUND = sector-disaggregated damages;
  PAGE = uncertainty-first (Stern Review), Sensitivity-Engine-at-the-core + catastrophe term.
  Climate-IAM family now 2 Gold + 2 Bronze. Graph 93 nodes / 151 edges.
- **Iter 20** — **MESSAGEix** and **REMIND** → Bronze (the perfect-foresight optimizing IAMs):
  MESSAGEix = IIASA energy-system LP on ixmp + MACRO, coupled to GLOBIOM; REMIND = PIK
  Ramsey-growth macro+energy NLP with Negishi/Nash trade, coupled to MAgPIE. Climate-IAM now
  2 Gold + 4 Bronze (3 stubs left: IMAGE, WITCH, AIM). Graph 94 nodes / 163 edges.
- **Iter 21 — 🎉 Climate-IAM family COMPLETE.** **IMAGE**, **WITCH**, **AIM** → Bronze,
  clearing the last three climate-IAM stubs (family now **2 Gold + 7 Bronze, 0 stubs**).
  These fill the paradigm corners the family was missing: **IMAGE** = process-based
  biophysical simulation (no objective; the SSP land engine); **WITCH** = game-theoretic
  Nash IAM with induced technical change (the equilibrium *concept* as a dial); **AIM** =
  soft-linked CGE + bottom-up enduse family with multi-scale downscaling (Asia-Pacific
  marker). Graph 97 nodes / 190 edges (3 institutions added: PBL, EIEE, NIES). **The Climate
  IAM family — the atlas's flagship domain — is now fully at Bronze-or-better.**
- **Iter 22 — 🎉 Energy family COMPLETE.** **PyPSA**, **Calliope**, **EnergyPLAN** → Bronze
  (family now **2 Gold + 3 Bronze, 0 stubs**). The trio sharpens the in-domain paradigm split:
  **PyPSA** = network-physics LP (Kirchhoff constraints inside the optimization; space matters);
  **Calliope** = declarative YAML "model-as-data" LP (reproducibility as architecture);
  **EnergyPLAN** = rule-based hourly *simulation* (no optimizer — the in-domain
  [Optimization vs Simulation](docs/comparative/optimization-vs-simulation.md) fork, feasibility
  over optimality). Graph 99 nodes / 212 edges (institutions ETH, Aalborg added).
- **Iter 23 — Economics breadth.** **Input–Output**, **GTAP**, **E3ME** → Bronze — the three
  *structurally distinct* economy-wide models around the Gold CGE/DSGE core: **Input–Output** =
  the linear Leontief ancestor (fixed coefficients, the SAM substrate CGE calibrates on);
  **GTAP** = the global multi-region trade-CGE standard (shared versioned world SAM as community
  infrastructure); **E3ME** = the flagship *disequilibrium* macro-econometric alternative
  (estimated, demand-led — the double-dividend counter to CGE's closure, the
  [Equilibrium vs Disequilibrium](docs/comparative/equilibrium-vs-disequilibrium.md) case study).
  Economics now 2 Gold + 3 Bronze (2 stubs left: GEM-E3, ENVISAGE). Graph 101 nodes / 229 edges
  (Leontief + Harvard added).

## Working order (program-director priority)

1. **Contrast pair**: OSeMOSYS + TIMES (bottom-up energy) vs DICE → unlocks the
   *IAM vs Energy* and *Optimization vs Simulation* matrices with real referents.
2. Equilibrium spine: CGE + DSGE + Input–Output → *ABM vs CGE*, *Equilibrium vs
   Disequilibrium* matrices.
3. Simulation spine: one ABM (MATSim/Covasim) + system dynamics → *ABM vs SD*.
4. Fill remaining stubs to Bronze, family by family.
5. Synergy layer: complete all matrices, detail all patterns, build the knowledge graph.
6. Signal D5 (publish) to the owner.
