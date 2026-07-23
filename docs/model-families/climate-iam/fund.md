# FUND — Climate Framework for Uncertainty, Negotiation and Distribution

!!! info "Bronze dossier"
    FUND completes the **cost-benefit IAM trio** with [DICE](dice.md) and [PAGE](page.md).
    Its distinguishing feature is **unusually disaggregated, sector-by-sector damage
    functions** across 16 regions — making it the reference for *what climate damage is
    actually made of*, and a frequent outlier (sometimes showing net *benefits* from mild
    warming) in social-cost-of-carbon comparisons.

> A cost-benefit IAM with unusually disaggregated, sector-by-sector damage functions across
> 16 regions; run as a simulation to recover marginal (social cost of carbon) damages.

## Positioning card

| Axis (see [Taxonomy](../../foundations/taxonomy.md)) | FUND |
|------|------|
| Optimization vs Simulation | **Simulation** (marginal-damage evaluation) |
| Top-down vs Bottom-up | Top-down (aggregate economy) |
| Equilibrium | Partial equilibrium |
| Foresight | Recursive / myopic |
| Deterministic vs Stochastic | Deterministic core + **Monte-Carlo uncertainty** |
| Time / Space | Annual / 16 regions |
| Solution method | Recursive simulation |

| Field | Value |
|-------|-------|
| Full name | FUND — Climate Framework for Uncertainty, Negotiation and Distribution |
| Domain | Climate — Integrated Assessment (cost-benefit) |
| First release / current | 1990s / FUND 3.x–4.x |
| Institution · lead | Richard Tol & David Anthoff (orig. Vrije Universiteit; now open academic) |
| Language · solver | C# (earlier Fortran/Pascal); **MimiFUND** (Julia) |
| License / access | Open (academic; MIT via the Mimi framework) |

---

## 🎓 Scholar Track

**History & motivation.** FUND was begun by **Richard Tol** in the early 1990s (initially to
study international climate negotiation and burden-sharing — hence "Negotiation and
Distribution"), later co-developed with **David Anthoff**. Its ambition was **damage
detail**: rather than DICE's single aggregate damage function, FUND estimates impacts
**sector by sector** (agriculture, sea-level rise, energy demand for heating/cooling, water
resources, human health/vector-borne disease, ecosystems, storms) and **region by region**.

**Mathematical formulation.** FUND is a **recursive simulation**, not an optimization. An
exogenous (or policy) emissions path drives a simple carbon-cycle and temperature model;
temperature and income then feed **sectoral damage functions** $D_{s,r}(T, Y)$ for sector
$s$ and region $r$. Damages are typically nonlinear in temperature and scaled by
regional income/vulnerability; some sectors show **negative damages (benefits)** at low
warming (e.g. reduced heating demand, CO₂ fertilization). The **social cost of carbon** is
recovered by a **marginal experiment**: run a baseline, add one pulse tonne of CO₂, re-run,
and discount the difference in global damages.

**Solution algorithm.** Step annually: emissions → concentrations → temperature → sectoral
damages → aggregate; no equilibrium solve, no optimization. SCC = discounted marginal damage
of a pulse.

**Calibration & validation.** Sectoral damage functions are **calibrated to the impacts
literature** (dose-response studies per sector); the climate module is tuned to reproduce
assessed warming. Validated by comparison with other IAMs' SCC ranges and impact
meta-analyses; participates in SCC model-comparison exercises (e.g. the US IWG).

**Strengths / weaknesses / criticisms.** *Strengths:* transparent, decomposable damages you
can audit sector by sector; native Monte-Carlo uncertainty; distributional (regional)
detail. *Criticisms:* the low-warming *benefit* result and specific damage calibrations are
contested; sensitive to discounting like all cost-benefit IAMs; damage functions
extrapolate beyond the data range at high temperatures.

## 🛠️ Engineer Track

**Architecture & engines.** A **[Climate Engine](../../patterns/climate-engine.md)** (simple
carbon/temperature) feeding a bank of sectoral **damage modules**, wrapped in a
**[Scenario Engine](../../patterns/scenario-engine.md)** and a
**[Sensitivity Engine](../../patterns/sensitivity-engine.md)** (Monte-Carlo over uncertain
parameters). The modern implementation, **MimiFUND**, is built on the **Mimi** Julia
framework — a component architecture shared with the modern
[DICE](dice.md)/Mimi ecosystem, making modules composable and swappable.

**Data & complexity.** Lightweight: 16 regions × ~8 sectors × annual steps runs in seconds,
which is what makes large **Monte-Carlo SCC ensembles** (tens of thousands of runs) routine.

**Openness / extensibility.** Fully open via Mimi (Julia); components (climate, each damage
sector) are independently replaceable — a model-as-components design.

## 🏛️ Architect Track

**Reusable patterns.** [Climate Engine](../../patterns/climate-engine.md) +
[Sensitivity Engine](../../patterns/sensitivity-engine.md) +
[Scenario Engine](../../patterns/scenario-engine.md); the standout is **decomposed,
sector-modular damages** — the single most transferable idea.

**Trade-offs & alternatives.** Against [DICE](dice.md): FUND trades DICE's optimizable
compactness for **damage disaggregation and distributional detail** (but is run as a
simulation, so it yields no *optimal* path itself). Against [PAGE](page.md): both emphasize
uncertainty, but PAGE foregrounds probabilistic/catastrophic risk while FUND foregrounds
sectoral structure. See [Deterministic vs Stochastic](../../comparative/deterministic-vs-stochastic.md).

**Adoption.** A core input to the **US Interagency Working Group** SCC estimates (alongside
DICE and PAGE); widely used in academic damage and distributional analysis.

**Ecosystem.** Siblings DICE, PAGE; implemented in **Mimi** alongside MimiDICE, MimiGIVE.
Successor concepts feed the modern **GIVE**/RFF-SP SCC framework.

**Research gaps.** Damage-function uncertainty at high warming; missing/underweighted
catastrophic and non-market damages; keeping sectoral calibrations current with impacts
science.

!!! quote "Lesson for the integrated simulator"
    FUND's contribution is **damage as a decomposable, auditable structure** rather than a
    single black-box coefficient: an integrated simulator should represent climate (and other)
    damages **sector by sector and region by region**, so a headline harm number can be opened
    up to show *what* it is made of and *who* bears it — and so the most contested pieces (the
    low-warming benefits, the high-warming tail) can be inspected and stress-tested
    individually rather than hidden inside an aggregate. Its Mimi **model-as-components**
    design is itself the lesson: damage sectors as swappable modules on a shared climate core.

## Major publications

- Tol, R. S. J. (1997). "On the optimal control of carbon dioxide emissions: an application
  of FUND." *Environmental Modeling & Assessment* 2.
- Anthoff, D., & Tol, R. S. J. (2014). "The income elasticity of the impact of climate
  change." In *Is the Environment a Luxury?* (and FUND documentation).
- Anthoff, D., & Tol, R. S. J. (2013). "The uncertainty about the social cost of carbon."
  *Environmental and Resource Economics* 56.

## See also
- Trio: [DICE](dice.md) · [PAGE](page.md) · Contrast: [GCAM](gcam.md)
- Patterns: [Climate Engine](../../patterns/climate-engine.md) · [Sensitivity Engine](../../patterns/sensitivity-engine.md)
- Positioning: [Taxonomy](../../foundations/taxonomy.md) · Quality bar: [DICE dossier](dice.md)
