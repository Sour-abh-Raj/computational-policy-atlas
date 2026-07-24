# Model Families

The dossiers. Each follows the canonical
[dossier structure](../foundations/dossier-template.md) and opens with a taxonomy
positioning card. This index is also the **production roadmap** — depth-first: one
flagship per family reaches publishable quality, then breadth fills in against the
proven pattern.

Legend: ✅ complete · 🟡 in progress · ⬜ planned

## Climate — Integrated Assessment Models (IAMs)

| Model | Institution | Status |
|-------|-------------|--------|
| [**DICE**](climate-iam/dice.md) — Dynamic Integrated Climate–Economy | Yale (Nordhaus) | ✅ Gold (flagship) |
| [**GCAM**](climate-iam/gcam.md) — Global Change Analysis Model | PNNL / JGCRI | ✅ Gold |
| [**FUND**](climate-iam/fund.md) — sector-disaggregated damages | Tol & Anthoff | ✅ Bronze |
| [**PAGE**](climate-iam/page.md) — uncertainty-first (Stern Review) | Hope (Cambridge) | ✅ Bronze |
| [**MESSAGEix**](climate-iam/messageix.md) — energy-system optimization IAM | IIASA | ✅ Bronze |
| [**REMIND**](climate-iam/remind.md) — Ramsey-growth macro+energy IAM | PIK Potsdam | ✅ Bronze |
| [**IMAGE**](climate-iam/image.md) — process-based, biophysical SSP model | PBL Netherlands | ✅ Bronze |
| [**WITCH**](climate-iam/witch.md) — game-theoretic, induced tech change | RFF-CMCC / EIEE | ✅ Bronze |
| [**AIM**](climate-iam/aim.md) — CGE + bottom-up enduse family | NIES Japan | ✅ Bronze |

## Energy Systems

| Model | Institution | Status |
|-------|-------------|--------|
| [**OSeMOSYS**](energy/osemosys.md) — Open Source energy MOdelling SYStem | KTH / open community | ✅ Gold |
| [**TIMES**](energy/times.md) — The Integrated MARKAL-EFOM System | IEA-ETSAP | ✅ Gold |
| [**PyPSA**](energy/pypsa.md) — network-physics power-system optimization | TU Berlin / open | ✅ Bronze |
| [**Calliope**](energy/calliope.md) — declarative (YAML) energy optimization | ETH / open | ✅ Bronze |
| [**EnergyPLAN**](energy/energyplan.md) — rule-based national-system simulation | Aalborg University | ✅ Bronze |

## Economics — Equilibrium & Macro

| Model | Type | Status |
|-------|------|--------|
| [**CGE**](economics/cge.md) (static & dynamic) | Computable General Equilibrium | ✅ Gold |
| [**DSGE**](economics/dsge.md) | Dynamic Stochastic General Equilibrium | ✅ Gold |
| [**Input–Output / Leontief**](economics/input-output.md) — the structural ancestor | Leontief | ✅ Bronze |
| [**GTAP**](economics/gtap.md) — global multi-region trade CGE | Purdue consortium | ✅ Bronze |
| [**E3ME**](economics/e3me.md) — macro-econometric, disequilibrium | Cambridge Econometrics | ✅ Bronze |
| [**GEM-E3**](economics/gem-e3.md) — EU energy-economy hybrid CGE | E3MLab / NTUA · EU JRC | ✅ Bronze |
| [**ENVISAGE**](economics/envisage.md) — World Bank global CGE + climate | World Bank | ✅ Bronze |

## Transportation

| Model | Institution | Status |
|-------|-------------|--------|
| [**MATSim**](transport/matsim.md) — Multi-Agent Transport Simulation | ETH Zürich / TU Berlin | ✅ Gold |
| [**SUMO**](transport/sumo.md) — microscopic vehicle-level traffic sim | DLR | ✅ Bronze |
| [**TRANSIMS**](transport/transims.md) — CA-based regional ABM (the ancestor) | LANL | ✅ Bronze |
| [**ActivitySim**](transport/activitysim.md) — activity-based demand (nested logit) | consortium | ✅ Bronze |

## Urban

| Model | Institution | Status |
|-------|-------------|--------|
| [**UrbanSim**](urban/urbansim.md) — land-use/transport microsimulation | Waddell / UC Berkeley | ✅ Bronze |
| SILO — LUTI microsimulation | TU Munich / partners | ⬜ |
| CityScope — tangible interactive urban modeling | MIT Media Lab | ⬜ |

## Agriculture & Land

| Model | Institution | Status |
|-------|-------------|--------|
| [**GLOBIOM**](agriculture/globiom.md) — Global Biosphere Management Model | IIASA | ✅ Gold |
| [**MAgPIE**](agriculture/magpie.md) — land-use cost-minimization (REMIND's land module) | PIK Potsdam | ✅ Bronze |
| [**DSSAT**](agriculture/dssat.md) — process-based crop-growth simulator | DSSAT Foundation / U. Florida | ✅ Bronze |
| [**EPIC**](agriculture/epic.md) — field crop + erosion/nutrient model | USDA / Texas A&M | ✅ Bronze |

## Water

| Model | Institution | Status |
|-------|-------------|--------|
| [**SWAT**](water/swat.md) — watershed hydrology & water quality | USDA-ARS / Texas A&M | ✅ Bronze |
| [**MODFLOW**](water/modflow.md) — 3-D groundwater-flow PDE (finite-difference) | USGS | ✅ Bronze |
| [**WEAP**](water/weap.md) — water allocation & planning (LP + scenarios) | SEI | ✅ Bronze |

## Health / Epidemiology

| Model | Institution | Status |
|-------|-------------|--------|
| [**Covasim**](health/covasim.md) — COVID-19 Agent-based Simulator | IDM / Gates Foundation | ✅ Gold |
| [**GLEAM**](health/gleam.md) — metapopulation + mobility epidemic model | Northeastern (MOBS) | ✅ Bronze |
| [**OpenABM-Covid19**](health/openabm.md) — agent-based, contact-tracing focus | Oxford | ✅ Bronze |

## Cross-cutting method families (documented under [Paradigms](../paradigms/index.md))

Agent-Based ([**Mesa** ✅ Bronze](frameworks/mesa.md), [**Repast** ✅ Bronze](frameworks/repast.md),
[**NetLogo** ✅ Bronze](frameworks/netlogo.md), [**GAMA** ✅ Bronze](frameworks/gama.md)) ·
System Dynamics ([**Vensim** ✅ Gold](frameworks/vensim.md),
[**Stella** ✅ Bronze](frameworks/stella.md), [**AnyLogic** ✅ Bronze](frameworks/anylogic.md) — multi-method) ·
Optimization (LP, MILP, DP, optimal control, multi-objective) · ML-based policy (RL,
Bayesian decision models, digital twins).

---

!!! note "Why DICE is the flagship"
    DICE is small enough to state in full (≈30 equations), old enough to have a
    thoroughly documented literature of criticism, and influential enough (Nobel
    2018; underpins official Social Cost of Carbon estimates) that the lessons
    transfer widely. It sets the quality bar for every dossier that follows.
