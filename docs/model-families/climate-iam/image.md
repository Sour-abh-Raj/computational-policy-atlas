# IMAGE — Integrated Model to Assess the Global Environment

!!! info "Bronze dossier"
    IMAGE is the **process-based, biophysically-detailed** pole of the IAM family — the
    opposite design choice from [DICE](dice.md). Where DICE compresses the Earth system into
    ~30 equations and *optimizes* a welfare objective, IMAGE **simulates** a richly
    resolved world — 26 regions plus a geographic grid for land, carbon, nutrients and
    biodiversity — stepping *recursively* year by year with no global objective at all. It is
    the workhorse behind the **SSP** scenario framework and IPCC land-use narratives.

> A large process-based simulation IAM emphasizing biophysical detail — land, biodiversity,
> nutrient and carbon cycles — driving the SSP scenario framework rather than optimizing a
> welfare objective.

## Positioning card

| Axis (see [Taxonomy](../../foundations/taxonomy.md)) | IMAGE |
|------|------|
| Optimization vs Simulation | **Simulation** (process-based) |
| Top-down vs Bottom-up | **Hybrid**, biophysically detailed |
| Equilibrium | Partial |
| Foresight | **Recursive** (myopic) |
| Deterministic vs Stochastic | Deterministic (+ scenarios) |
| Time / Space | Annual / 26 regions + 5′ or 0.5° grid |
| Solution method | Recursive simulation + embedded optimizers (TIMER, MAGNET) |

| Field | Value |
|-------|-------|
| Full name | IMAGE — Integrated Model to Assess the Global Environment |
| Domain | Climate — Integrated Assessment |
| First release / current | 1990 / IMAGE 3.x |
| Institution · lead | PBL Netherlands Environmental Assessment Agency (with Utrecht University) |
| Language · solver | Mixed (Fortran/C + the M framework); TIMER (energy) & MAGNET (CGE) modules |
| License / access | Restricted / research access (documentation open) |

---

## 🎓 Scholar Track

**History & motivation.** IMAGE was built at **RIVM/PBL (Netherlands)** from 1990 onward
(IMAGE 1.0 supported early IPCC assessments) with a founding conviction opposite to the
cost-benefit IAMs: that the value of an integrated model is in **representing the biophysical
Earth system in geographic detail** — land cover, crops, carbon, nitrogen, water, biodiversity
— not in collapsing it into a single optimized welfare number. It became a **marker model for
the SSP framework** (PBL led SSP1, the "sustainability" narrative) and a central supplier of
land-use and emissions pathways to the IPCC.

**Mathematical formulation.** IMAGE is a **system of coupled process modules**, not a single
optimization. There is **no global objective function**; instead each subsystem evolves by its
own dynamics and they are integrated **recursively** (myopic, period-by-period — see
[Recursive vs Perfect Foresight](../../comparative/recursive-vs-perfect-foresight.md)). Core
components: the **energy system** (**TIMER**, a bottom-up simulation of demand and technology
substitution driven by relative costs and learning curves), the **agro-economic system**
(**MAGNET**, a global CGE for supply/demand/trade of agricultural commodities), a **land-use
allocation** model that downscales regional demand onto a geographic grid, and Earth-system
components: a **carbon cycle**, **nutrient (N/P) cycles**, a **terrestrial vegetation / LPJmL**
coupling, and a **climate emulator** (MAGICC-style) closing the loop from emissions to
temperature back to impacts. Formally the state is a huge vector of grid- and region-level
stocks (land classes, carbon pools, capital, populations); the "decision" content lives inside
the embedded optimizers (TIMER's cost-minimizing technology mix, MAGNET's market clearing)
rather than in a top-level planner.

**Solution algorithm.** **Recursive dynamic simulation**: given the state at year *t*, each
module computes flows for *t→t+1* (energy demand & mix, agricultural markets, land allocation,
emissions), the climate emulator updates the physical state, and the loop advances. Embedded
modules solve their own sub-problems (TIMER cost-minimization; MAGNET a complementarity/CGE
solve) but the **system as a whole is not optimized** — it is *stepped*.

**Calibration & validation.** Calibrated to historical land cover (HYDE database), FAO
agricultural statistics, IEA energy balances, and observed carbon/nutrient fluxes; validated by
backcasting land-use change and by participation in inter-comparisons (ISIMIP, the SSP database,
EMF, IPCC AR5/AR6).

**Strengths / weaknesses / criticisms.** *Strengths:* unmatched **biophysical and spatial
detail** (gridded land, biodiversity, nutrients); a natural home for **SSP storyline →
quantified pathway** translation; strong on land-use change emissions and impacts. *Criticisms:*
because it does not optimize, it cannot directly answer "what is the *optimal* policy?" the way
DICE or REMIND can; recursive myopia means no anticipation of future scarcity/policy; the sheer
number of coupled modules makes the system heavy, partly closed, and hard to fully audit.

## 🛠️ Engineer Track

**Architecture & engines.** IMAGE is a textbook **[Integration Engine](../../patterns/integration-engine.md)**:
a set of process modules coupled through shared state and stepped in time. It embeds an
**[Energy Dispatch Engine](../../patterns/energy-dispatch-engine.md)**-flavored simulation
(TIMER), a **[Market Engine](../../patterns/market-engine.md)** (MAGNET CGE), a
**[Land Engine](../../patterns/land-engine.md)** (gridded allocation, the closest peer to
[GLOBIOM](../agriculture/globiom.md)/MAgPIE), a **[Climate Engine](../../patterns/climate-engine.md)**
(carbon cycle + MAGICC emulator), and a **[Data Pipeline](../../patterns/data-pipeline.md)** that
downscales regional quantities to grid cells.

**Data & complexity.** Runs on a **0.5° geographic grid** for land/carbon (5′ for some layers)
plus **26 world regions** for socio-economics, annual steps to 2100. The gridded land and
biogeochemistry layers dominate the compute and storage budget; a scenario is a coupled run
across all modules rather than a single solve.

**Openness / extensibility.** Model code is **restricted (research access)** but the
**documentation is fully open** (the online "IMAGE 3.0 documentation"), and outputs populate the
public **SSP database**. Modular by construction — TIMER, MAGNET, LPJmL and the climate emulator
are separately developed and swappable.

## 🏛️ Architect Track

**Reusable patterns.** The defining pattern is **process-based recursive coupling with embedded
optimizers**: a simulated world whose *sub-problems* are optimized but whose *whole* is stepped,
not planned. Also reusable: **spatial downscaling** (region → grid) as a first-class stage, and
**storyline-to-quantification** (turning qualitative SSP narratives into consistent numeric
drivers).

**Trade-offs & alternatives.** IMAGE and [GCAM](gcam.md) are the two great **process-based /
recursive-simulation** IAMs — both reject the single welfare objective, both resolve technology
and land in detail; GCAM leans on **nested-logit market shares** and a partial-equilibrium price
search, IMAGE on **explicit biophysical process modules** and gridded land. Against the
optimizing IAMs — [DICE](dice.md) (welfare, perfect foresight), [REMIND](remind.md)/
[MESSAGEix](messageix.md) (intertemporal optimization) — IMAGE trades the ability to name an
*optimum* for far richer **impact and Earth-system realism**. This is exactly the
[Optimization vs Simulation](../../comparative/optimization-vs-simulation.md) axis.

**Adoption.** A core **IPCC** land-use and SSP model (PBL's SSP1 marker); used heavily in
**biodiversity** (GLOBIO), nutrient, and land-degradation assessments (GEO, IPBES); a European
policy mainstay.

**Ecosystem.** TIMER (energy), MAGNET (agro-economy), LPJmL (vegetation), GLOBIO (biodiversity),
MAGICC (climate); peers GCAM, REMIND-MAgPIE, MESSAGEix-GLOBIOM, AIM.

**Research gaps.** Adding anticipatory behavior without abandoning the process-based ethos;
opening the code; reconciling gridded biophysical detail with the tractability that optimizing
IAMs enjoy.

!!! quote "Lesson for the integrated simulator"
    IMAGE is the atlas's clearest proof that **you do not need a global objective function to
    build a serious integrated model**. It couples optimized *sub-problems* (a least-cost energy
    mix, a clearing agricultural market) inside a world that is otherwise **simulated forward in
    biophysical detail** — land, carbon, nutrients, biodiversity on an explicit grid. For the
    integrated simulator this validates a **mixed architecture**: let the components that have a
    well-posed optimization *be* optimized, but stitch them together with a process-based,
    recursively-stepped Earth system rather than forcing one super-objective over everything.
    IMAGE also elevates **spatial downscaling** and **storyline-to-numbers** translation to
    first-class pipeline stages — machinery the simulator will need to turn scenario narratives
    into gridded, physically consistent runs.

## Major publications

- Stehfest, E., van Vuuren, D., et al. (2014). *Integrated Assessment of Global Environmental
  Change with IMAGE 3.0.* PBL Netherlands Environmental Assessment Agency.
- van Vuuren, D. P., et al. (2017). "Energy, land-use and greenhouse gas emissions trajectories
  under a green growth paradigm (SSP1)." *Global Environmental Change* 42.
- Doelman, J. C., et al. (2018). "Exploring SSP land-use dynamics using the IMAGE model."
  *Global Environmental Change* 48.

## See also
- Contrast: [GCAM](gcam.md) · [DICE](dice.md) · [Optimization vs Simulation](../../comparative/optimization-vs-simulation.md) · [Recursive vs Perfect Foresight](../../comparative/recursive-vs-perfect-foresight.md)
- Patterns: [Integration Engine](../../patterns/integration-engine.md) · [Land Engine](../../patterns/land-engine.md) · [Climate Engine](../../patterns/climate-engine.md)
- Positioning: [Taxonomy](../../foundations/taxonomy.md) · Quality bar: [DICE dossier](dice.md)
