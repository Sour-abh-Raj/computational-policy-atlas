# Repast — Recursive Porous Agent Simulation Toolkit

!!! info "Bronze dossier"
    Repast is the **high-performance, scale-out** member of the ABM framework family. Where
    [Mesa](mesa.md) optimizes for Pythonic accessibility and [NetLogo](netlogo.md) for pedagogy,
    Repast targets **large-scale** social and complex-systems simulation — and uniquely offers
    **Repast HPC**, an MPI-based engine for distributing millions of agents across a
    supercomputer. It is the framework you reach for when the model outgrows one machine.

> A mature, high-performance ABM platform family (Repast Simphony for desktop, Repast HPC for
> supercomputers) for large-scale social and complex-systems simulation.

## Positioning card

| Axis (see [Taxonomy](../../foundations/taxonomy.md)) | Repast |
|------|------|
| Optimization vs Simulation | **Simulation** (ABM toolkit) |
| Top-down vs Bottom-up | **Bottom-up** |
| Equilibrium | N/A (model-defined) |
| Foresight | Model-defined |
| Deterministic vs Stochastic | Model-defined |
| Time / Space | Model-defined / grid, GIS, network, continuous |
| Solution method | **Discrete-event scheduler; MPI for HPC** |

| Field | Value |
|-------|-------|
| Full name | Repast — Recursive Porous Agent Simulation Toolkit |
| Domain | Frameworks & Environments |
| First release / current | 2000s / ongoing (Simphony, HPC, Repast4Py) |
| Institution · lead | Argonne National Laboratory / ROAD consortium |
| Language · solver | Java (Simphony), C++ (Repast HPC), Python (Repast4Py) |
| License / access | Open (BSD) |

---

## 🎓 Scholar Track

**History & motivation.** Repast originated in the early 2000s (University of Chicago social-science
computing, then stewarded by **Argonne National Laboratory** and the **ROAD** consortium) as a
research-grade successor to the pioneering **Swarm** toolkit. Its motivating concern is **scale and
rigor**: production social-simulation research needs a **fast, reproducible, well-engineered**
platform, and — increasingly — the ability to run **beyond a single computer**. That last need
produced **Repast HPC**, a distinctive contribution no other mainstream ABM framework matched for
years.

**Mathematical formulation.** Like any framework, Repast fixes **no domain mathematics**; it
formalizes the ABM execution model. A model is a population of **agents** with `step`-style behaviors,
embedded in one or more **projections** (spatial contexts): grids, continuous space, **GIS**, and
**networks**. A **discrete-event scheduler** orders behaviors in simulated time (agents can schedule
future events, not just tick uniformly — a more general model than fixed-step activation). The
distinguishing formal content is **parallel/distributed execution**: in **Repast HPC**, the agent
population and space are **partitioned across MPI processes**, with **ghost/buffer agents** replicated
at partition boundaries and **synchronization** each step so cross-boundary interactions stay
consistent — the classic **parallel discrete-event / domain-decomposition** problem. The "solution" is
the scheduled advance of the distributed agent population.

**Solution algorithm.** Advance the **event schedule**; in HPC mode each rank steps its local agents,
exchanges boundary (ghost) state with neighbor ranks via MPI, and synchronizes — enabling
**strong/weak scaling** to millions–billions of agents. **Repast Simphony** (Java) provides the
desktop/interactive experience; **Repast4Py** brings the HPC model to Python.

**Calibration & validation.** Framework-level: Repast ships **batch-run and parameter-sweep**
infrastructure and integrates with model-exploration/optimization tools (e.g. via the EMEWS
framework for large-scale workflow-driven calibration on clusters); model-specific validation is the
user's.

**Strengths / weaknesses / criticisms.** *Strengths:* **maturity and performance**; the premier
**HPC** ABM path; multiple projections (incl. GIS); strong reproducibility and batch tooling.
*Criticisms:* **steeper learning curve** than NetLogo/Mesa; Java/C++ verbosity; the power of HPC comes
with distributed-systems complexity (partitioning, load balance) most models never need.

## 🛠️ Engineer Track

**Architecture & engines.** A **[Behavior Engine](../../patterns/behavior-engine.md)** over pluggable
**projections** (a flexible **[Spatial Engine](../../patterns/spatial-engine.md)**: grid/GIS/network/
continuous), driven by a **discrete-event [Integration Engine](../../patterns/integration-engine.md)**
(scheduler) — and, crucially, a **distributed-execution layer** (MPI domain decomposition + ghost
agents) that no pure-Python framework matches. Batch/sweep = **[Sensitivity Engine](../../patterns/sensitivity-engine.md)**;
Simphony adds a **[Visualization Engine](../../patterns/visualization-engine.md)**.

**Data & complexity.** Scales from desktop (Simphony) to **supercomputers** (HPC/4Py); performance is
the reason to choose it. Complexity budget is dominated by partitioning and synchronization at scale.

**Openness / extensibility.** **BSD open source**, actively maintained by Argonne/ROAD; three
first-class fronts — **Simphony** (Java, GUI), **Repast HPC** (C++/MPI), **Repast4Py** (Python/MPI) —
plus **EMEWS** for cluster-scale model exploration.

## 🏛️ Architect Track

**Reusable patterns.** The transferable ideas: **discrete-event scheduling** (agents schedule future
events — more expressive than uniform ticks), **pluggable spatial projections** (one agent set, many
spaces), and above all **domain decomposition with ghost agents** for **distributed agent simulation**
— the canonical recipe for scaling ABM past one node.

**Trade-offs & alternatives.** Among frameworks: Repast = **scale/HPC and rigor**;
[Mesa](mesa.md) = **Python ecosystem/accessibility**; [NetLogo](netlogo.md) = **pedagogy/rapid
prototyping**; [GAMA](gama.md) = **GIS-first spatial modeling**. Repast (with MASON) is the
performance-oriented Java lineage; its **HPC** capability is the differentiator when agent counts or
compute demands are extreme. All four sit at the **simulation/emergence** pole; the analogous
System-Dynamics environment is [Vensim](vensim.md).

**Adoption.** Widely used in **large social-science, epidemiology, market, and infrastructure**
simulations, especially where **scale** matters; Argonne and national-lab computational-social-science
work; the go-to for **supercomputer-scale** ABM.

**Ecosystem.** Argonne/ROAD (Repast Simphony, Repast HPC, Repast4Py, EMEWS); lineage from Swarm; peers
MASON, Mesa, NetLogo, GAMA, FLAME/FLAME GPU.

**Research gaps.** Lowering the HPC-programming barrier; automatic load balancing; GPU backends;
standard model-description (ODD) and reproducibility tooling.

!!! quote "Lesson for the integrated simulator"
    Repast's distinctive lesson is **scale-out architecture**: when a model must exceed a single
    machine, the reusable recipe is **domain decomposition** — partition agents and space across
    processes, replicate **ghost agents** at boundaries, and synchronize each step — the same pattern
    parallel PDE solvers use, applied to agents. An integrated policy simulator that aspires to
    *world-scale* runs (billions of agents, coupled domains) must be **distribution-ready from the
    core**, not retrofitted. Repast also argues for **discrete-event scheduling** over rigid ticks
    (let processes and agents schedule events in continuous simulated time) and for **pluggable spatial
    projections** so the same behavior runs over a grid, a network, or GIS. Its trade-off — power at
    the cost of a steeper curve — reinforces that the simulator should offer a **tiered experience**:
    an accessible mode (à la Mesa/NetLogo) that can escalate to an HPC backend when the question
    demands it.

## Major publications

- North, M. J., et al. (2013). "Complex adaptive systems modeling with Repast Simphony." *Complex
  Adaptive Systems Modeling* 1(3).
- Collier, N., North, M. (2013). "Parallel agent-based simulation with Repast for High Performance
  Computing." *Simulation* 89(10).
- Collier, N., Ozik, J., et al. (2020). "Repast4Py: distributed agent-based modeling in Python."
  *Journal of Open Source Software*.

## See also
- Peers: [Mesa](mesa.md) · [NetLogo](netlogo.md) · [GAMA](gama.md) · Analogy: [Vensim](vensim.md) (SD environment)
- Patterns: [Behavior Engine](../../patterns/behavior-engine.md) · [Spatial Engine](../../patterns/spatial-engine.md) · [Integration Engine](../../patterns/integration-engine.md) · [Sensitivity Engine](../../patterns/sensitivity-engine.md)
- Positioning: [Taxonomy](../../foundations/taxonomy.md) · Quality bar: [DICE dossier](../../model-families/climate-iam/dice.md)
