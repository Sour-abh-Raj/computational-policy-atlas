# TRANSIMS — Transportation Analysis and Simulation System

!!! info "Bronze dossier"
    TRANSIMS is the **historically pivotal** transport model — the Los Alamos project that first
    put a **synthetic population of individual travelers** on a **cellular-automata traffic
    network** at regional scale, and in doing so invented much of the machinery
    [MATSim](matsim.md) and [ActivitySim](activitysim.md) later refined. It is the **agent-based
    microsimulation** origin story of modern travel modeling.

> A pioneering regional agent-based travel-demand microsimulation built on cellular-automata
> traffic, generating synthetic populations and second-by-second regional travel.

## Positioning card

| Axis (see [Taxonomy](../../foundations/taxonomy.md)) | TRANSIMS |
|------|------|
| Optimization vs Simulation | **Simulation** (agent-based micro) |
| Top-down vs Bottom-up | **Bottom-up** (individuals) |
| Equilibrium | N/A (iterated relaxation) |
| Foresight | Myopic (route/activity) |
| Deterministic vs Stochastic | **Stochastic** |
| Time / Space | Second-scale / regional network |
| Solution method | **Cellular-automata traffic + microsimulation** |

| Field | Value |
|-------|-------|
| Full name | TRANSIMS — Transportation Analysis and Simulation System |
| Domain | Transportation |
| First release / current | 1990s–2000s (open-sourced 2000s) |
| Institution · lead | Los Alamos National Laboratory (LANL) |
| Language · solver | C++ (open sourced) |
| License / access | Open (Apache / NASA-style) |

---

## 🎓 Scholar Track

**History & motivation.** TRANSIMS was built at **Los Alamos National Laboratory** in the 1990s
(funded by US DOT/FHWA), applying the lab's **complex-systems and cellular-automata** expertise to a
problem the incumbent "four-step" travel-demand models handled crudely: the fact that traffic is the
**emergent product of millions of individual trips**. Its radical proposal was to **replace aggregate
zonal flows with a simulated synthetic population** — every household and traveler represented
explicitly — and to run their trips through a **fast cellular-automata traffic microsimulation**. This
was the conceptual birth of **activity-based, agent-based regional travel modeling**.

**Mathematical formulation.** TRANSIMS is a **pipeline of microsimulation modules**: (1) a
**population synthesizer** generates a synthetic population matching census marginals (iterative
proportional fitting / IPF); (2) an **activity generator** assigns each synthetic person a daily
activity pattern (where/when/what); (3) a **router** finds paths on the multimodal network; (4) a
**traffic microsimulator** executes all trips using the **Nagel–Schreckenberg cellular-automaton**:
the road is discretized into cells (~7.5 m), and each vehicle's speed $v \in \{0,\dots,v_{\max}\}$
updates each second by the rules **accelerate → brake to avoid collision → randomize (dawdle with
probability $p$) → move**. This astonishingly simple rule set reproduces realistic flow–density
relationships and spontaneous jams. The system is **iterated**: travelers **re-plan routes/times**
in response to the congestion they experienced, relaxing toward a **stochastic user equilibrium** —
exactly the **feedback loop** MATSim later generalized to full day-plan co-evolution.

**Solution algorithm.** Run the module pipeline, execute the CA traffic sim for the day, feed back
realized travel times, let a fraction of travelers re-plan, and **repeat until relaxation**. The CA
kernel is integer-arithmetic and extremely fast, which is what made **regional-scale** microsimulation
feasible on 1990s hardware.

**Calibration & validation.** Population synthesis calibrated to census; network and counts to
regional data; validated in large US case studies (notably **Portland, Oregon**) against observed
volumes and travel times.

**Strengths / weaknesses / criticisms.** *Strengths:* **pioneering** integrated
synthetic-population + activity + CA-traffic pipeline; fast integer CA kernel; fully **disaggregate**.
*Criticisms:* CA traffic is coarser than continuous car-following ([SUMO](sumo.md)); the toolchain was
**complex and hard to deploy**, which limited uptake and ultimately saw it **superseded** by MATSim
(behavioral scoring) and ActivitySim (statistical choice models); development has largely wound down.

## 🛠️ Engineer Track

**Architecture & engines.** The archetypal transport **[Data Pipeline](../../patterns/data-pipeline.md)**
(synthesize → generate activities → route → simulate → feed back), with a
**[Behavior Engine](../../patterns/behavior-engine.md)** (agents with activities/routes) on a
**[Spatial Engine](../../patterns/spatial-engine.md)** (CA network) closed by a re-planning
**feedback loop** — the pattern MATSim turned into its co-evolutionary algorithm. Written in C++,
later **open-sourced**.

**Data & complexity.** The **Nagel–Schreckenberg CA** makes per-vehicle updates integer and
cache-friendly, so regional populations (millions of trips) were tractable early; the heavy cost is
the multi-module data plumbing.

**Openness / extensibility.** Open-sourced (via USDOT/FHWA and a Google-Code era release); influential
as a **reference design** more than a living codebase today. Its ideas live on in MATSim/ActivitySim.

## 🏛️ Architect Track

**Reusable patterns.** TRANSIMS contributed foundational patterns the whole field now assumes:
**synthetic-population generation** as stage one of demand modeling, the **activity→route→network-sim
→feedback** pipeline, and the **cellular-automaton** as a minimal traffic kernel. Its **iterated
re-planning relaxation** is the direct ancestor of MATSim's co-evolutionary user equilibrium.

**Trade-offs & alternatives.** TRANSIMS is the ancestor `succeeded` by [MATSim](matsim.md) (which
replaced CA + module-pipeline with a cleaner **utility-scored day-plan co-evolution**) and
conceptually by [ActivitySim](activitysim.md) (which formalized the activity generator as **estimated
discrete-choice** submodels). Against [SUMO](sumo.md) it trades microscopic car-following fidelity for
**regional coverage** via the CA kernel. It is the origin point of the **agent-based** answer to the
aggregate four-step model.

**Adoption.** Historically significant (Portland and other US MPO studies); its **legacy is
methodological** — nearly every modern activity-/agent-based regional model descends from it.

**Ecosystem.** LANL / USDOT-FHWA lineage; descendants MATSim, ActivitySim, POLARIS, mobiTopp; the
Nagel–Schreckenberg CA literature.

**Research gaps.** (Largely historical) — superseded; its open questions (deployment complexity,
CA vs continuous fidelity) were answered by successors.

!!! quote "Lesson for the integrated simulator"
    TRANSIMS is the atlas's reminder that **the disaggregate, synthetic-population approach was a
    hard-won invention**, and that its **pipeline** — synthesize a population, give agents activities,
    route them, simulate, and **feed realized experience back into re-planning** — is the reusable
    skeleton of behavioral simulation, whatever kernel sits underneath. For the integrated simulator
    the lessons are: (1) a **synthetic population** is foundational infrastructure many domains
    (transport, health, energy demand) can share; (2) the **iterate-to-relaxation feedback loop** is a
    general way to reach equilibrium *by simulation* rather than assumption; and (3) the reason
    TRANSIMS was overtaken — **deployment complexity** — is itself a design warning: architectural
    clarity and usability decide whether a powerful model actually gets adopted.

## Major publications

- Nagel, K., Schreckenberg, M. (1992). "A cellular automaton model for freeway traffic." *Journal de
  Physique I* 2(12).
- Smith, L., Beckman, R., et al. (1995). "TRANSIMS: Transportation Analysis and Simulation System."
  Los Alamos National Laboratory LA-UR-95-1641.
- Nagel, K., et al. (1999). "TRANSIMS traffic flow characteristics." LANL technical reports.

## See also
- Succeeded by: [MATSim](matsim.md) · [ActivitySim](activitysim.md) · Contrast: [SUMO](sumo.md)
- Patterns: [Data Pipeline](../../patterns/data-pipeline.md) · [Behavior Engine](../../patterns/behavior-engine.md) · [Spatial Engine](../../patterns/spatial-engine.md)
- Positioning: [Taxonomy](../../foundations/taxonomy.md) · Quality bar: [DICE dossier](../../model-families/climate-iam/dice.md)
