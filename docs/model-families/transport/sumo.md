# SUMO — Simulation of Urban MObility

!!! info "Bronze dossier"
    SUMO is the **microscopic** end of the transport family: it resolves **individual vehicles in
    continuous space at sub-second time**, using car-following and lane-change physics. Where
    [MATSim](matsim.md) simulates a whole region's *day plans* to a behavioral equilibrium, SUMO
    zooms all the way in to **how vehicles actually move, queue, and interact** — the standard open
    testbed for traffic signal control and connected/automated-vehicle (CAV) research.

> An open microscopic traffic simulator resolving individual vehicles in continuous space and
> sub-second time; the standard testbed for traffic control and connected/automated-vehicle
> research.

## Positioning card

| Axis (see [Taxonomy](../../foundations/taxonomy.md)) | SUMO |
|------|------|
| Optimization vs Simulation | **Simulation** (microscopic) |
| Top-down vs Bottom-up | **Bottom-up** (vehicles) |
| Equilibrium | N/A (can iterate to DUE) |
| Foresight | Myopic (car-following) |
| Deterministic vs Stochastic | Deterministic + stochastic demand |
| Time / Space | **Sub-second / continuous road network** |
| Solution method | **Car-following / lane-change models** |

| Field | Value |
|-------|-------|
| Full name | SUMO — Simulation of Urban MObility |
| Domain | Transportation |
| First release / current | 2001 / ongoing |
| Institution · lead | German Aerospace Center (DLR) |
| Language · solver | C++ (Python **TraCI** API) |
| License / access | Open (EPL 2.0) |

---

## 🎓 Scholar Track

**History & motivation.** SUMO was started in **2001 at the German Aerospace Center (DLR)** to
provide an **open, portable microscopic traffic simulator** — at a time when the field was dominated
by expensive proprietary tools (VISSIM, Aimsun). Its purpose is operational and engineering: study
**traffic signals, ramp metering, emissions, and increasingly connected/automated vehicles**, where
the object of interest is the **second-by-second motion and interaction of individual vehicles**, not
long-run travel-demand equilibrium.

**Mathematical formulation.** SUMO is a **time-stepped microscopic simulation**. Each vehicle is an
agent whose longitudinal motion follows a **car-following model** — by default a space-continuous
**Krauss** model: a vehicle computes a **safe velocity** that guarantees it can stop before colliding
with the leader given reaction time $\tau$ and deceleration $b$,

$$v_{\text{safe}}(t) = v_\ell(t) + \frac{g(t) - v_\ell(t)\,\tau}{\frac{\bar v}{b} + \tau},$$

where $g$ is the gap and $v_\ell$ the leader's speed; the vehicle then takes
$v = \min(v_{\text{safe}}, v+a\,\Delta t, v_{\max})$ minus a stochastic "driver imperfection" term.
**Lateral motion** uses a lane-change model (strategic/cooperative/tactical/regret incentives).
Alternative models (IDM, Wiedemann) are selectable. The network is a **continuous graph of lanes,
junctions, and connections** with traffic-light logic; demand is a set of vehicles with **routes**.
There is no objective function — behavior *emerges* from the local rules — though SUMO can be
iterated (via **duaIterate**) to a **dynamic user equilibrium** on route choice.

**Solution algorithm.** Advance simulation time in small steps (default 1 s, sub-second available):
each step update every vehicle's speed/position from the car-following + lane-change rules, resolve
junctions and signals, and log detector/emission output. Scales by **parallelization** and
mesoscopic fallback (queue-based) for large networks.

**Calibration & validation.** Calibrated to observed flows, speeds, and headways from loop detectors
and floating-car data; car-following parameters tuned to trajectory datasets; validated against
measured link travel times and queue lengths. Emissions via embedded models (HBEFA, PHEMlight).

**Strengths / weaknesses / criticisms.** *Strengths:* **high physical fidelity**, open, huge feature
set (signals, public transit, CAVs, emissions), scriptable in real time via **TraCI**. *Criticisms:*
microscopic detail is **expensive** at regional scale; not a travel-demand model on its own (needs
external demand); many parameters to calibrate; myopic — no behavioral day-planning like MATSim.

## 🛠️ Engineer Track

**Architecture & engines.** A **[Behavior Engine](../../patterns/behavior-engine.md)** at vehicle
granularity (local car-following/lane-change rules) over a **[Spatial Engine](../../patterns/spatial-engine.md)**
(continuous lane/junction network), stepped by an **[Integration Engine](../../patterns/integration-engine.md)**
(discrete-time update). Its signature engineering asset is **TraCI** (Traffic Control Interface) — a
socket API that lets external code (Python) **read and control the simulation live**, making SUMO a
reinforcement-learning and control **testbed** ([RL for signal control](../../paradigms/algorithms/lp.md)
sits naturally on top).

**Data & complexity.** Networks import from **OpenStreetMap** (netconvert); demand from counts,
O-D matrices, or activity models. Microscopic step cost scales with vehicle count; mesoscopic mode
trades fidelity for speed on big scenarios.

**Openness / extensibility.** **EPL-2.0 open source**, C++ core with Python tools and the TraCI/
Libsumo APIs; a large ecosystem of add-ons (Flow, SUMO-RL, emission models). Runs on all platforms.

## 🏛️ Architect Track

**Reusable patterns.** The transferable ideas: a **live control API (TraCI)** that turns a simulator
into an interactive environment for control/RL, **selectable behavioral kernels** (swap Krauss/IDM/
Wiedemann without touching the engine), and **multi-resolution** operation (micro ↔ meso) on one
network.

**Trade-offs & alternatives.** Within transport, SUMO and [MATSim](matsim.md) are complementary
resolutions: SUMO = **physical, second-scale vehicle dynamics** (great for control/CAV, costly at
scale); MATSim = **behavioral, day-scale co-evolutionary equilibrium** (great for policy/demand,
coarser physics). [TRANSIMS](transims.md) sits between (regional CA microsimulation). SUMO is the
pure **simulation/emergence** pole — the [Optimization vs Simulation](../../comparative/optimization-vs-simulation.md)
and [Continuous vs Discrete](../../comparative/continuous-vs-discrete.md) axes made concrete inside
one domain. Its proprietary peers are VISSIM/Aimsun.

**Adoption.** The **de-facto open standard** for microscopic traffic and CAV research; used by DLR,
universities, and industry for signal optimization, autonomous-driving simulation, and emissions;
foundation of the **Flow**/**SUMO-RL** control benchmarks.

**Ecosystem.** DLR SUMO suite (netconvert, duarouter, TraCI, Libsumo); Flow, SUMO-RL, CARLA co-sim;
peers VISSIM, Aimsun, Paramics; upstream data from OSM.

**Research gaps.** Regional-scale microscopic tractability; automatic calibration; standardizing
CAV/driver behavioral models; coupling to demand/land-use.

!!! quote "Lesson for the integrated simulator"
    SUMO's lesson is about **resolution and interactivity**. It shows that the *right* granularity is
    question-dependent — signal timing and automated-vehicle safety need **second-scale vehicle
    physics** that a day-plan model like MATSim cannot provide — so an integrated simulator must treat
    **spatial/temporal resolution as a dial** and support **multi-resolution coupling** (micro where
    it matters, meso/macro elsewhere) on a shared network. Even more transferable is **TraCI**: a
    **live control API** that turns a forward simulation into an *interactive environment* an external
    optimizer or RL agent can drive. Any world-class policy simulator should expose exactly this — the
    ability to pause, inspect, and steer the running model — so that control and learning methods can
    be layered on top of the physics.

## Major publications

- Lopez, P. A., et al. (2018). "Microscopic Traffic Simulation using SUMO." *IEEE ITSC 2018*.
- Krauss, S. (1998). *Microscopic Modeling of Traffic Flow: Investigation of Collision Free Vehicle
  Dynamics.* PhD thesis, DLR.
- Behrisch, M., et al. (2011). "SUMO – Simulation of Urban MObility: An Overview." *SIMUL 2011*.

## See also
- Contrast: [MATSim](matsim.md) · [TRANSIMS](transims.md) · [Continuous vs Discrete](../../comparative/continuous-vs-discrete.md) · [Optimization vs Simulation](../../comparative/optimization-vs-simulation.md)
- Patterns: [Behavior Engine](../../patterns/behavior-engine.md) · [Spatial Engine](../../patterns/spatial-engine.md) · [Integration Engine](../../patterns/integration-engine.md)
- Positioning: [Taxonomy](../../foundations/taxonomy.md) · Quality bar: [DICE dossier](../../model-families/climate-iam/dice.md)
