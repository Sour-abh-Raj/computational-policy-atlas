# MODFLOW

!!! info "Bronze dossier"
    MODFLOW is the **physics** pole of the water domain — the USGS finite-difference solver of the 3-D
    groundwater-flow **partial differential equation**. Where [SWAT](swat.md) simulates surface
    hydrology with empirical response units and [WEAP](weap.md) allocates water by rules, MODFLOW
    computes **hydraulic head in an aquifer** from conservation of mass and Darcy's law on a numerical
    grid. It is the global standard for **aquifer management, water-rights, and groundwater-contaminant**
    analysis, and the atlas's cleanest example of a **PDE simulation engine**.

> The USGS finite-difference groundwater-flow simulator: a modular numerical solver of the 3-D
> groundwater PDE, the global standard for aquifer and water-rights analysis.

## Positioning card

| Axis (see [Taxonomy](../../foundations/taxonomy.md)) | MODFLOW |
|------|------|
| Optimization vs Simulation | **Simulation** (numerical PDE solve) |
| Top-down vs Bottom-up | **Bottom-up** (grid cells) |
| Equilibrium | N/A (steady-state or transient) |
| Foresight | N/A / transient |
| Deterministic vs Stochastic | Deterministic (stochastic via ensembles/PEST) |
| Time / Space | **Days–years / 3-D grid** |
| Solution method | **Finite-difference solve of the groundwater-flow PDE** |

| Field | Value |
|-------|-------|
| Full name | MODFLOW (Modular Three-Dimensional Finite-Difference Ground-Water Flow Model) |
| Domain | Water |
| First release / current | 1984 / MODFLOW 6 |
| Institution · lead | U.S. Geological Survey (USGS) |
| Language · solver | Fortran (**FloPy** Python interface) |
| License / access | **Public domain** |

---

## 🎓 Scholar Track

**History & motivation.** MODFLOW was released by the **USGS** in **1984** (McDonald & Harbaugh) and
became the world's most-used groundwater model precisely because of a design choice in its name:
**modular**. Rather than a monolithic program, it is a **core solver plus interchangeable packages**
(rivers, wells, recharge, drains, evapotranspiration), so users assemble exactly the processes their
aquifer needs. Its motivation is quantitative **groundwater management** — sustainable yield, well-field
design, saltwater intrusion, contaminant transport, and the science behind **water-rights** and
depletion disputes.

**Mathematical formulation.** MODFLOW solves the **3-D transient groundwater-flow equation**, obtained
by combining **Darcy's law** with **conservation of mass**:

$$\frac{\partial}{\partial x}\!\left(K_x \frac{\partial h}{\partial x}\right)
+\frac{\partial}{\partial y}\!\left(K_y \frac{\partial h}{\partial y}\right)
+\frac{\partial}{\partial z}\!\left(K_z \frac{\partial h}{\partial z}\right)
+ W = S_s \frac{\partial h}{\partial t},$$

where $h$ is **hydraulic head** (the state variable), $K$ the hydraulic conductivity tensor, $S_s$
specific storage, and $W$ volumetric source/sink terms (wells, recharge). The domain is discretized
into a **structured (or, in MODFLOW 6, unstructured) grid** of cells; the PDE is approximated by
**finite differences**, giving a large **sparse linear system** $\mathbf{A}\mathbf{h}=\mathbf{b}$ each
time step (steady-state drops the storage term). Boundary conditions and stresses enter through
packages. There is **no objective function** — MODFLOW *simulates* the head field that the physics
dictates; optimization (e.g. pumping to minimize drawdown) is layered on externally.

**Solution algorithm.** Assemble the finite-difference matrix and solve the sparse linear system with
iterative solvers (PCG, GMRES, or the Newton formulation for unconfined/drying cells in MODFLOW 6);
step through **stress periods** for transient runs. **FloPy** (Python) builds inputs, runs the model,
and post-processes — the modern scripting front end.

**Calibration & validation.** Calibrated to observed **head and flux** measurements, typically with
**PEST/PEST++** (inverse modeling, parameter estimation, and uncertainty) — a rigorous, physics-anchored
validation culture. Coupled transport (**MT3D**, MODFLOW 6 GWT) extends to contaminants.

**Strengths / weaknesses / criticisms.** *Strengths:* **rigorous physics**, public-domain, modular,
enormous validation record, the legal/regulatory standard for groundwater. *Criticisms:* **data-hungry**
(conductivity, storage fields are hard to know); **structured-grid** limitations (eased by MODFLOW 6
unstructured grids); computationally heavy for large 3-D transient models; groundwater–surface-water
coupling historically required linking to [SWAT](swat.md)/others (now improving).

## 🛠️ Engineer Track

**Architecture & engines.** The archetypal **PDE [Integration Engine](../../patterns/integration-engine.md)**
over a 3-D grid **[Spatial Engine](../../patterns/spatial-engine.md)**, with a **package architecture**
(pluggable process modules) that is itself a lesson in modular design. Inverse calibration (PEST) is a
**[Calibration Engine](../../patterns/calibration-engine.md)**; **FloPy** provides the
**[Data Pipeline](../../patterns/data-pipeline.md)** and scripting. Public-domain Fortran core.

**Data & complexity.** Cost scales with grid cells × time steps; large sparse linear solves dominate.
Building the conductivity/boundary data set is the practical bottleneck. MODFLOW 6 unifies the code base
and adds unstructured grids and integrated transport/multiple models.

**Openness / extensibility.** **Public domain** (USGS) — maximally open; a vast ecosystem of packages,
GUIs (ModelMuse, Groundwater Vistas), and the **FloPy** Python stack; the reference implementation others
interoperate with.

## 🏛️ Architect Track

**Reusable patterns.** MODFLOW's headline lessons: the **modular package architecture** (a solver core
plus interchangeable process packages — assemble the model you need), **finite-difference PDE solution**
as a reusable physical-simulation engine, and **inverse calibration with uncertainty (PEST)** as a
first-class companion, not an afterthought. Its public-domain status made it an **interoperability
standard** — a governance lesson as much as a technical one.

**Trade-offs & alternatives.** MODFLOW is the **deep-physics** water engine; within the domain it
complements [SWAT](swat.md) (surface/watershed process hydrology, empirical) and [WEAP](weap.md) (water
**allocation/planning**, rule/optimization-based) — **groundwater PDE · surface process · allocation**
are three different questions needing three engines, increasingly **coupled** (SWAT-MODFLOW; MODFLOW 6
GWF-GWT). Against the economic/optimizing models elsewhere in the atlas, MODFLOW is pure **physical
simulation** — the far end of the [Optimization vs Simulation](../../comparative/optimization-vs-simulation.md)
and [Continuous vs Discrete](../../comparative/continuous-vs-discrete.md) axes (continuous fields, not
agents or equilibria).

**Adoption.** The **global standard** for groundwater — USGS and state agencies, consultancies, courts
(water-rights litigation), and research worldwide; MODFLOW results underpin aquifer-management and
depletion policy.

**Ecosystem.** USGS (MODFLOW 6, MT3D-USGS, GSFLOW for coupled surface-groundwater); FloPy, PEST/PEST++,
ModelMuse; peers FEFLOW, SWAT (surface), HydroGeoSphere.

**Research gaps.** Data scarcity for subsurface parameters; tighter surface–groundwater–ecosystem
coupling; uncertainty at scale; coupling to economic/allocation decision models.

!!! quote "Lesson for the integrated simulator"
    MODFLOW contributes the **PDE-physics engine** and a governance lesson. Technically, it shows that
    some policy questions (aquifer depletion, contamination, saltwater intrusion) require **conservation-
    law physics on a numerical grid** — a finite-difference/finite-element solver — which is a distinct
    engine from the optimization, equilibrium, and agent engines the atlas catalogs; a world-class
    simulator must be able to host **continuous-field physical simulation** alongside them, and to
    **couple** it (groundwater ↔ surface water ↔ land use ↔ economics). Its **modular package
    architecture** is a direct model for how the simulator should let users *assemble* a model from
    interchangeable process components, and its **PEST inverse-calibration-with-uncertainty** pairing
    reinforces that calibration and uncertainty belong inside the tool. Finally, MODFLOW's **public-
    domain** status is why it became an interoperability standard — a reminder that **openness is an
    architectural feature**, not just a license choice.

## Major publications

- McDonald, M. G., Harbaugh, A. W. (1988). *A Modular Three-Dimensional Finite-Difference Ground-Water
  Flow Model.* USGS Techniques of Water-Resources Investigations 6-A1.
- Langevin, C. D., et al. (2017). "Documentation for the MODFLOW 6 Groundwater Flow Model." USGS
  Techniques and Methods 6-A55.
- Bakker, M., et al. (2016). "Scripting MODFLOW model development using Python and FloPy." *Groundwater*
  54(5).

## See also
- Water-domain peers: [SWAT](swat.md) (surface hydrology) · [WEAP](weap.md) (allocation) · Contrasts: [Optimization vs Simulation](../../comparative/optimization-vs-simulation.md) · [Continuous vs Discrete](../../comparative/continuous-vs-discrete.md)
- Patterns: [Integration Engine](../../patterns/integration-engine.md) · [Spatial Engine](../../patterns/spatial-engine.md) · [Calibration Engine](../../patterns/calibration-engine.md) · [Data Pipeline](../../patterns/data-pipeline.md)
- Positioning: [Taxonomy](../../foundations/taxonomy.md) · Quality bar: [DICE dossier](../../model-families/climate-iam/dice.md)
