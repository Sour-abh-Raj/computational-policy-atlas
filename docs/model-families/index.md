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
| [**DICE**](climate-iam/dice.md) — Dynamic Integrated Climate–Economy | Yale (Nordhaus) | ✅ flagship |
| FUND | Tol / others | ⬜ |
| PAGE | Hope (Cambridge) | ⬜ |
| GCAM — Global Change Analysis Model | PNNL / JGCRI | ⬜ |
| MESSAGEix | IIASA | ⬜ |
| IMAGE | PBL Netherlands | ⬜ |
| REMIND | PIK Potsdam | ⬜ |
| WITCH | RFF-CMCC / EIEE | ⬜ |
| AIM | NIES Japan | ⬜ |

## Energy Systems

| Model | Institution | Status |
|-------|-------------|--------|
| [**OSeMOSYS**](energy/osemosys.md) — Open Source energy MOdelling SYStem | KTH / open community | ✅ Gold |
| [**TIMES**](energy/times.md) — The Integrated MARKAL-EFOM System | IEA-ETSAP | ✅ Gold |
| PyPSA | TU Berlin / open | ⬜ |
| Calliope | ETH / open | ⬜ |
| EnergyPLAN | Aalborg University | ⬜ |

## Economics — Equilibrium & Macro

| Model | Type | Status |
|-------|------|--------|
| [**CGE**](economics/cge.md) (static & dynamic) | Computable General Equilibrium | ✅ Gold |
| [**DSGE**](economics/dsge.md) | Dynamic Stochastic General Equilibrium | ✅ Gold |
| Input–Output / Leontief | Structural | ⬜ |
| GTAP | Global trade CGE (Purdue) | ⬜ |
| GEM-E3 / ENVISAGE | Energy-economy CGE | ⬜ |
| E3ME | Macroeconometric (Cambridge Econometrics) | ⬜ |

## Transportation

| Model | Institution | Status |
|-------|-------------|--------|
| [**MATSim**](transport/matsim.md) — Multi-Agent Transport Simulation | ETH Zürich / TU Berlin | ✅ Gold |
| SUMO | DLR | ⬜ |
| TRANSIMS | LANL | ⬜ |
| ActivitySim | consortium | ⬜ |

## Urban

UrbanSim · CityScope · SILO — ⬜

## Agriculture & Land

| Model | Institution | Status |
|-------|-------------|--------|
| [**GLOBIOM**](agriculture/globiom.md) — Global Biosphere Management Model | IIASA | ✅ Gold |
| MAgPIE | PIK Potsdam | ⬜ |
| DSSAT | crop-model consortium | ⬜ |
| EPIC | Texas A&M / IIASA | ⬜ |

## Water

WEAP · SWAT · MODFLOW — ⬜

## Health / Epidemiology

| Model | Institution | Status |
|-------|-------------|--------|
| [**Covasim**](health/covasim.md) — COVID-19 Agent-based Simulator | IDM / Gates Foundation | ✅ Gold |
| GLEAM | Northeastern / ISI | ⬜ |
| OpenABM-Covid19 | Oxford | ⬜ |

## Cross-cutting method families (documented under [Paradigms](../paradigms/index.md))

Agent-Based (Mesa, Repast, NetLogo, GAMA) · System Dynamics
([**Vensim** ✅ Gold](frameworks/vensim.md), Stella, AnyLogic) · Optimization (LP, MILP,
DP, optimal control, multi-objective) · ML-based policy (RL, Bayesian decision models,
digital twins).

---

!!! note "Why DICE is the flagship"
    DICE is small enough to state in full (≈30 equations), old enough to have a
    thoroughly documented literature of criticism, and influential enough (Nobel
    2018; underpins official Social Cost of Carbon estimates) that the lessons
    transfer widely. It sets the quality bar for every dossier that follows.
