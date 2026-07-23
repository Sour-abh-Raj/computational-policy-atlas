# MESSAGEix

!!! info "Bronze dossier"
    MESSAGEix is IIASA's **open-source energy-system optimization framework**, the engine of
    the **MESSAGEix-GLOBIOM** integrated assessment model. It sits at the intersection of the
    [energy models](../energy/times.md) (bottom-up least-cost LP) and the process IAMs — a
    perfect-foresight optimizer linked to a macro module and to the Gold
    [GLOBIOM](../agriculture/globiom.md) land model.

> IIASA's open-source energy-system optimization framework, linked to the MACRO
> general-equilibrium module and the ixmp data platform; least-cost technology pathways under
> perfect foresight.

## Positioning card

| Axis (see [Taxonomy](../../foundations/taxonomy.md)) | MESSAGEix |
|------|------|
| Optimization vs Simulation | **Optimization** (least-cost) |
| Top-down vs Bottom-up | **Bottom-up** (+ MACRO top-down link) |
| Equilibrium | Partial (energy) + GE via MACRO |
| Foresight | **Perfect foresight** (intertemporal) |
| Deterministic vs Stochastic | Deterministic (stochastic variants) |
| Time / Space | Flexible steps / multi-region |
| Solution method | LP / MILP |

| Field | Value |
|-------|-------|
| Full name | MESSAGEix (Model for Energy Supply Strategy Alternatives and their General Environmental impact) |
| Domain | Climate — Integrated Assessment / Energy |
| First release / current | 2018 (MESSAGEix; MESSAGE since 1980s) |
| Institution · lead | IIASA (Energy, Climate & Environment program) |
| Language · solver | Python + GAMS on the **ixmp** platform |
| License / access | Open source (Apache 2.0) |

---

## 🎓 Scholar Track

**History & motivation.** MESSAGE originated at **IIASA** in the **1980s** as one of the
first bottom-up energy-systems optimization models; **MESSAGEix** (2018) is its modern,
**open-source** re-implementation on the **ixmp** (integrated modeling platform) data
backbone. Built to design **least-cost, long-horizon energy transitions** consistent with
climate targets, it is the energy core of **MESSAGEix-GLOBIOM**, a flagship IAM in the
**IPCC** and **SSP** processes (IIASA hosted the SSP2 marker).

**Mathematical formulation.** At heart a **linear program** minimizing discounted total
system cost over a multi-region **Reference Energy System** (technologies converting
commodities from resources to demands) subject to energy-balance, capacity, resource, and
policy (emissions) constraints — the same core as [TIMES](../energy/times.md)/[OSeMOSYS](../energy/osemosys.md)
but **perfect-foresight intertemporal** by default. The optional **MACRO** module adds a
top-down macroeconomic feedback (a general-equilibrium consumption/GDP response to energy
prices), iterating with the bottom-up core toward consistency — a **hybrid**
top-down/bottom-up design (see [Top-Down vs Bottom-Up](../../comparative/top-down-vs-bottom-up.md)).

**Solution algorithm.** LP (optionally MILP for lumpy/integer decisions) solved in GAMS;
MACRO coupling iterates energy prices ↔ macro demands to convergence.

**Calibration & validation.** Calibrated to base-year energy balances (IEA), technology cost
databases, and demand projections; validated via IAM/energy model-comparison exercises (IAMC,
EMF) and historical back-testing of the energy system.

**Strengths / weaknesses / criticisms.** *Strengths:* fully open, modular, **ixmp**
data/scenario management, tight land coupling (GLOBIOM), MACRO feedback. *Criticisms:*
perfect foresight overstates anticipatory investment (see
[Recursive vs Perfect Foresight](../../comparative/recursive-vs-perfect-foresight.md));
large LPs are data- and compute-heavy; MACRO is a stylized single-sector feedback.

## 🛠️ Engineer Track

**Architecture & engines.** An **[Energy Dispatch Engine](../../patterns/energy-dispatch-engine.md)**
(least-cost RES LP) + **[Optimization Engine](../../patterns/optimization-engine.md)**, an
optional **[Market Engine](../../patterns/market-engine.md)** (MACRO GE feedback), a
**[Data Pipeline](../../patterns/data-pipeline.md)** (ixmp/database), and coupling to the
**[Land Engine](../../patterns/land-engine.md)** ([GLOBIOM](../agriculture/globiom.md)).

**Data & complexity.** Runs on **ixmp** — a database-backed scenario platform (Python API,
`message_ix`) — solving via GAMS; a global multi-region run is a large but tractable LP.

**Openness / extensibility.** Apache-2.0, pip-installable (`message_ix`), strong docs and
tutorials; the **ixmp** platform is reusable for other models. A genuinely open successor to
the historically closed MESSAGE.

## 🏛️ Architect Track

**Reusable patterns.** [Optimization](../../patterns/optimization-engine.md) +
[Energy Dispatch](../../patterns/energy-dispatch-engine.md) engines with a **data platform
(ixmp)** as first-class infrastructure; **bottom-up ↔ top-down (MACRO) soft-linking** as a
composition pattern; **cross-domain coupling** to land (GLOBIOM).

**Trade-offs & alternatives.** Against [TIMES](../energy/times.md): similar least-cost
paradigm, but MESSAGEix is fully open with a modern data platform and a MACRO GE link.
Against [GCAM](gcam.md): MESSAGEix **optimizes** with perfect foresight where GCAM
**simulates** market clearing with recursive myopia — a clean
[Optimization vs Simulation](../../comparative/optimization-vs-simulation.md) contrast within
the IAM family. Against [REMIND](remind.md): both are perfect-foresight optimizing IAMs; REMIND
leads with an intertemporal macro core, MESSAGEix with a detailed energy LP.

**Adoption.** IIASA's flagship; **MESSAGEix-GLOBIOM** is an IPCC/SSP marker model; widely used
in national and global decarbonization studies.

**Ecosystem.** MESSAGEix-GLOBIOM (land), MACRO (macro feedback), ixmp/message_ix ecosystem;
peers REMIND, GCAM, IMAGE, TIMES.

**Research gaps.** Foresight realism; richer macro feedback than single-sector MACRO;
computational scaling for high spatial/temporal detail.

!!! quote "Lesson for the integrated simulator"
    MESSAGEix models two things the integrated simulator needs: a **data-platform-first**
    design (ixmp) where scenarios and results are managed in a shared database rather than ad
    hoc files, and **explicit soft-linking** between a bottom-up energy optimizer, a top-down
    macro feedback, and a land model — each kept in its own paradigm but iterated to
    consistency. It is a working, open demonstration of the atlas's core thesis that a serious
    policy simulator is a **federation of coupled, paradigm-appropriate subsystems** over a
    shared data substrate, not a single monolithic model.

## Major publications

- Huppmann, D., et al. (2019). "The MESSAGEix Integrated Assessment Model and the ix modeling
  platform." *Environmental Modelling & Software* 112.
- Krey, V., et al. (2020). *MESSAGEix-GLOBIOM documentation*. IIASA.
- Messner, S., & Strubegger, M. (1995). *User's guide for MESSAGE III*. IIASA. (lineage)

## See also
- Contrast: [GCAM](gcam.md) · [REMIND](remind.md) · [TIMES](../energy/times.md) · [Optimization vs Simulation](../../comparative/optimization-vs-simulation.md)
- Coupled: [GLOBIOM](../agriculture/globiom.md) · Patterns: [Energy Dispatch Engine](../../patterns/energy-dispatch-engine.md) · [Data Pipeline](../../patterns/data-pipeline.md)
- Positioning: [Taxonomy](../../foundations/taxonomy.md) · Quality bar: [DICE dossier](dice.md)
