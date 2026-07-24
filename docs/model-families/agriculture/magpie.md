# MAgPIE — Model of Agricultural Production and its Impact on the Environment

!!! info "Bronze dossier"
    MAgPIE is PIK's **land-use optimization** model — the recursive-dynamic, spatially-explicit
    **cost-minimization** counterpart to IIASA's partial-equilibrium [GLOBIOM](globiom.md). It decides
    **where on a clustered grid** food, feed, material, and bioenergy demand is met at least cost, under
    biophysical yield, water, and land constraints — and it is the **land module of [REMIND](../climate-iam/remind.md)**,
    closing the loop between climate-economy pathways and land-use change.

> A recursive-dynamic land-use *cost-minimization* optimization on a spatial grid, coupled to REMIND,
> resolving where food/feed/bioenergy demand is met under biophysical and water constraints.

## Positioning card

| Axis (see [Taxonomy](../../foundations/taxonomy.md)) | MAgPIE |
|------|------|
| Optimization vs Simulation | **Optimization** (cost minimization) |
| Top-down vs Bottom-up | **Bottom-up** (spatial clusters) |
| Equilibrium | Partial equilibrium (recursive) |
| Foresight | **Recursive-dynamic** (myopic) |
| Deterministic vs Stochastic | Deterministic |
| Time / Space | 5–10-yr / **clustered grid cells** |
| Solution method | **NLP / LP** (GAMS) |

| Field | Value |
|-------|-------|
| Full name | MAgPIE — Model of Agricultural Production and its Impact on the Environment |
| Domain | Agriculture & Land |
| First release / current | 2000s / ongoing (MAgPIE 4.x) |
| Institution · lead | Potsdam Institute for Climate Impact Research (PIK) |
| Language · solver | GAMS + R (`madrat`/`mrland`) |
| License / access | Open source (AGPL) |

---

## 🎓 Scholar Track

**History & motivation.** MAgPIE was developed at **PIK** (Lotze-Campen, Popp and colleagues) from the
mid-2000s to represent **global land use as an economic optimization** consistent with PIK's
climate-economy modeling. Its purpose is to answer *where* and *how* the world's growing demand for
**food, feed, fiber, material, and bioenergy** is met — and at what cost to **forests, water, and
carbon** — in a way that could be **coupled to [REMIND](../climate-iam/remind.md)** so that mitigation
pathways see their land-use and land-based-mitigation (afforestation, bioenergy) consequences.

**Mathematical formulation.** MAgPIE minimizes **global agricultural production cost** subject to
meeting exogenous **regional demand** each period. Decision variables: **land-use allocation** (cropland,
pasture, forest, other) and production **activities** across **spatial clusters** (grid cells grouped
for tractability), plus technological-change investment, trade, and water use. Constraints encode
**biophysical yields** (from the **LPJmL** dynamic global vegetation model), **land availability**,
**water** availability, carbon stocks, and food/material demand balances. Formally,

$$\min_{x}\; \sum_{c}\big(\text{factor} + \text{land-conversion} + \text{tech} + \text{trade}\big)\;
\text{cost}_c \quad \text{s.t. demand, land, water, yield constraints},$$

solved **recursively** (each period optimizes given the previous land state; **myopic**, no perfect
foresight — the [Recursive vs Perfect Foresight](../../comparative/recursive-vs-perfect-foresight.md)
axis). **Endogenous technological change** (yield-increasing investment) and **land conversion** costs
give path dependence. Land-use-change **emissions** feed the climate side.

**Solution algorithm.** A **nonlinear program** (GAMS) per period over the cluster set, chained
recursively to 2100; the **madrat/mrland** R toolchain harmonizes inputs and **LPJmL** supplies gridded
biophysical parameters. Spatial **clustering** keeps the grid-scale problem solvable.

**Calibration & validation.** Calibrated to FAO production/land statistics, LPJmL biophysics, and
historical land patterns; validated via land-use inter-comparison (AgMIP, the SSP land database) and
coupling checks with REMIND. Contributes **SSP** land-use pathways.

**Strengths / weaknesses / criticisms.** *Strengths:* **spatially explicit least-cost land use** with
real biophysics; **open source**; tight **REMIND coupling** and land-based-mitigation detail.
*Criticisms:* cost-minimization with a single planner is an idealization (no diverse land-holder
behavior); recursive myopia; heavy data/biophysical dependencies; clustering trades spatial detail for
tractability.

## 🛠️ Engineer Track

**Architecture & engines.** An **[Optimization Engine](../../patterns/optimization-engine.md)** +
**[Land Engine](../../patterns/land-engine.md)** (finite land as a contested least-cost account — the
same pattern as [GLOBIOM](globiom.md)) over a clustered **[Spatial Engine](../../patterns/spatial-engine.md)**,
coupled to a **[Climate Engine](../../patterns/climate-engine.md)** (LUC emissions) and driven by a
strong R **[Data Pipeline](../../patterns/data-pipeline.md)** (`madrat`/`mrland`, LPJmL inputs). GAMS
solver core; R harmonization shell — the same toolchain family as REMIND.

**Data & complexity.** Gridded biophysics clustered into tractable units × recursive periods; the
**LPJmL coupling** and data harmonization dominate the pipeline. NLP solves per period are the compute
core.

**Openness / extensibility.** **Open source (AGPL)** on GitHub within the PIK ecosystem; modular
(land, water, bioenergy, forestry modules); coupled to REMIND (climate-economy) and LPJmL (biophysics).

## 🏛️ Architect Track

**Reusable patterns.** The transferable ideas: **least-cost land allocation on a clustered grid**
(spatial optimization with biophysical constraints), **cross-model coupling via a shared data pipeline**
(MAgPIE↔REMIND↔LPJmL through `madrat`), and **endogenous land conversion + technological change** giving
path dependence.

**Trade-offs & alternatives.** MAgPIE and [GLOBIOM](globiom.md) are the **two great global land-use
models** — both spatial, both partial-equilibrium land economics, both coupled to a climate-energy IAM
(MAgPIE↔REMIND at PIK; GLOBIOM↔MESSAGEix at IIASA). The design difference: MAgPIE is a **pure
cost-minimization** (planner) with LPJmL biophysics; GLOBIOM is a **spatial partial-equilibrium
surplus-maximization** (market). Comparing them is a clean study in how modeling choices shape land-use
projections. Against process-based [IMAGE](../climate-iam/image.md) land, both are optimization rather
than simulation.

**Adoption.** IPCC/SSP land-use pathways; PIK land-and-bioenergy studies; AgMIP land inter-comparisons;
a leading open global land model.

**Ecosystem.** PIK (MAgPIE, REMIND, LPJmL, madrat/mrland); peers GLOBIOM/G4M (IIASA), IMAGE-land (PBL),
GCAM-land; AgMIP community.

**Research gaps.** Behavioral heterogeneity beyond least-cost; foresight; finer spatial detail vs
tractability; deeper water/biodiversity constraints.

!!! quote "Lesson for the integrated simulator"
    MAgPIE reinforces two atlas themes from the land angle. First, **finite land is a shared, contested
    account** best handled by an explicit **spatial optimization** with real biophysical constraints —
    and pairing it with [GLOBIOM](globiom.md) shows the *same* land question answered by
    cost-minimization vs market surplus-maximization, so the integrated simulator should be able to run
    **both land-allocation logics and compare**. Second, MAgPIE is a masterclass in **cross-model
    coupling through a shared data pipeline**: the `madrat` toolchain lets MAgPIE, REMIND, and LPJmL
    exchange harmonized inputs so climate-economy, land, and biophysics stay mutually consistent — the
    concrete mechanism behind the atlas's call for a **common data substrate** that lets domain engines
    couple without drifting apart.

## Major publications

- Lotze-Campen, H., et al. (2008). "Global food demand, productivity growth, and the scarcity of land
  and water resources: a spatially explicit mathematical programming approach." *Agricultural Economics*
  39(3).
- Popp, A., et al. (2017). "Land-use futures in the shared socio-economic pathways (MAgPIE)." *Global
  Environmental Change* 42.
- Dietrich, J. P., et al. (2019). "MAgPIE 4 – a modular open-source framework for modeling global
  land systems." *Geoscientific Model Development* 12(4).

## See also
- Sibling/contrast: [GLOBIOM](globiom.md) · Coupled to: [REMIND](../climate-iam/remind.md) · Contrast: [IMAGE](../climate-iam/image.md) · [Recursive vs Perfect Foresight](../../comparative/recursive-vs-perfect-foresight.md)
- Patterns: [Land Engine](../../patterns/land-engine.md) · [Optimization Engine](../../patterns/optimization-engine.md) · [Spatial Engine](../../patterns/spatial-engine.md) · [Data Pipeline](../../patterns/data-pipeline.md)
- Positioning: [Taxonomy](../../foundations/taxonomy.md) · Quality bar: [DICE dossier](../../model-families/climate-iam/dice.md)
