# REMIND — Regional Model of Investment and Development

!!! info "Bronze dossier"
    REMIND is PIK's flagship IAM — essentially **[DICE](dice.md)'s Ramsey-growth philosophy
    scaled up**: intertemporal welfare maximization across 12 regions, but with a *detailed
    energy system* fused in and **Nash/Negishi trade coupling** between regions, linked to
    **MAgPIE** for land. It is the perfect-foresight, macro-first counterpart to the
    energy-first [MESSAGEix](messageix.md).

> A multi-region Ramsey-growth optimization IAM (DICE's philosophy, scaled up): intertemporal
> welfare maximization with a detailed energy system and Nash trade coupling, linked to
> MAgPIE for land.

## Positioning card

| Axis (see [Taxonomy](../../foundations/taxonomy.md)) | REMIND |
|------|------|
| Optimization vs Simulation | **Optimization** (intertemporal welfare) |
| Top-down vs Bottom-up | **Hybrid** (top-down growth + bottom-up energy) |
| Equilibrium | General equilibrium (Negishi/Nash) |
| Foresight | **Perfect foresight** |
| Deterministic vs Stochastic | Deterministic |
| Time / Space | 5-year / 12 regions |
| Solution method | NLP + iterative trade coupling |

| Field | Value |
|-------|-------|
| Full name | REMIND — Regional Model of Investment and Development |
| Domain | Climate — Integrated Assessment |
| First release / current | 2010s / REMIND 3.x |
| Institution · lead | Potsdam Institute for Climate Impact Research (PIK) |
| Language · solver | GAMS (CONOPT); R data pipeline |
| License / access | Open source (AGPL / LGPL) |

---

## 🎓 Scholar Track

**History & motivation.** REMIND was built at the **Potsdam Institute for Climate Impact
Research (PIK)** from the late 2000s to combine a **macroeconomic growth model** with a
**detailed bottom-up energy system** — bridging the top-down/bottom-up divide within one
optimization. It is a core **IPCC**/**SSP** model (PIK led SSP5) and a prominent voice on
deep-decarbonization pathways.

**Mathematical formulation.** REMIND maximizes **intertemporal social welfare** — the
discounted sum of regional utility of per-capita consumption — à la **Ramsey growth**
(exactly [DICE](dice.md)'s objective, but multi-region and with rich energy detail). A
**macroeconomic core** (CES production nesting capital, labor, and energy) is **hard-linked**
to a **bottom-up energy-system module** (many technologies, like an
[energy model](../energy/times.md)), so investment in macro capital and in specific energy
technologies is chosen *jointly and optimally* under **perfect foresight**. Regions are
coupled through **trade** (in goods, energy, and emissions permits), and the multi-region
equilibrium is found by an **iterative Negishi/Nash** procedure that reconciles regional
optimizations into a global equilibrium.

**Solution algorithm.** A large **nonlinear program** (GAMS/CONOPT) per region, wrapped in an
**iterative trade-coupling** loop until inter-regional markets clear.

**Calibration & validation.** Calibrated to base-year GDP, energy balances, and technology
costs; validated through IAM inter-comparison (IAMC, EMF, ADVANCE) and coupling checks with
MAgPIE and the climate module.

**Strengths / weaknesses / criticisms.** *Strengths:* consistent **macro + energy
optimization**, welfare-based (can discuss optimal policy), open, strong land coupling.
*Criticisms:* perfect foresight and a single representative regional agent are idealizations;
large NLPs are heavy and occasionally hard to solve; hard-linking macro and energy demands
strong internal consistency.

## 🛠️ Engineer Track

**Architecture & engines.** An **[Optimization Engine](../../patterns/optimization-engine.md)**
(intertemporal welfare) fusing a **[Market Engine](../../patterns/market-engine.md)**-style
macro core with an **[Energy Dispatch Engine](../../patterns/energy-dispatch-engine.md)**
(technology detail), coupled via trade and to the **[Land Engine](../../patterns/land-engine.md)**
(**MAgPIE**). Built on GAMS with an **R-based [Data Pipeline](../../patterns/data-pipeline.md)**
(`madrat`/`mrremind`).

**Data & complexity.** 12 regions × 5-year steps × detailed energy tech, solved as coupled
NLPs — computationally demanding; the R data toolchain (madrat) automates input harmonization.

**Openness / extensibility.** Open source (AGPL) on GitHub with the PIK modeling ecosystem;
modular (energy, macro, climate modules) and coupled to MAgPIE via a common framework.

## 🏛️ Architect Track

**Reusable patterns.** **Hard-linked macro + energy optimization** (a single objective over
both), **iterative multi-region trade coupling** (Negishi/Nash), and **cross-model coupling**
to land (MAgPIE) via a shared data pipeline.

**Trade-offs & alternatives.** Against [MESSAGEix](messageix.md): both are open,
perfect-foresight optimizing IAMs coupled to a land model, but REMIND leads with an
**intertemporal macro (Ramsey) core** and soft/hard energy link, while MESSAGEix leads with a
**detailed energy LP** plus a MACRO feedback. Against [GCAM](gcam.md): REMIND **optimizes
welfare** with perfect foresight; GCAM **simulates** market clearing with recursive myopia —
the [Optimization vs Simulation](../../comparative/optimization-vs-simulation.md) and
[Recursive vs Perfect Foresight](../../comparative/recursive-vs-perfect-foresight.md) contrasts.
Against [DICE](dice.md): REMIND is DICE's welfare-optimization idea with real technological and
regional detail.

**Adoption.** IPCC/SSP marker model (SSP5); ADVANCE, ENGAGE, and EU decarbonization studies;
a leading European IAM.

**Ecosystem.** REMIND-MAgPIE (land), coupled climate module (MAGICC/emulator), madrat/mrremind
data tools; peers MESSAGEix-GLOBIOM, GCAM, WITCH, IMAGE.

**Research gaps.** Foresight realism; heterogeneity beyond a representative regional agent;
solve robustness for large coupled NLPs.

!!! quote "Lesson for the integrated simulator"
    REMIND demonstrates the **hard-linked hybrid**: put a top-down macro growth model and a
    bottom-up energy system under *one* welfare objective so capital and technology investment
    are chosen jointly and optimally — the tightest form of the top-down/bottom-up integration
    the atlas keeps circling. Its multi-region **Negishi/Nash trade coupling** is a reusable
    recipe for stitching many regional optimizations into a global equilibrium. The caution it
    carries is the price of that tightness: perfect foresight and a representative agent buy
    consistency and a clean welfare metric at the cost of realism — reinforcing that the
    integrated simulator should treat **foresight and agent-heterogeneity as dials**, and be
    able to relax REMIND's idealizations where the transition's messiness is the point.

## Major publications

- Luderer, G., et al. (2015). "The REMIND model: description and evaluation." (PIK; and
  Baumstark et al. 2021, *Geoscientific Model Development* 14).
- Bauer, N., et al. (2012). "REMIND: The equations." PIK technical documentation.
- Baumstark, L., et al. (2021). "REMIND2.1." *Geoscientific Model Development* 14(10).

## See also
- Contrast: [MESSAGEix](messageix.md) · [GCAM](gcam.md) · [DICE](dice.md) · [Optimization vs Simulation](../../comparative/optimization-vs-simulation.md)
- Coupled: [Land Engine](../../patterns/land-engine.md) (MAgPIE) · Patterns: [Optimization Engine](../../patterns/optimization-engine.md) · [Energy Dispatch Engine](../../patterns/energy-dispatch-engine.md)
- Positioning: [Taxonomy](../../foundations/taxonomy.md) · Quality bar: [DICE dossier](dice.md)
