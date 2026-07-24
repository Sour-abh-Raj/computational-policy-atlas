# NetLogo

!!! info "Bronze dossier"
    NetLogo is the **most widely used ABM environment in the world** — and the reason a whole
    generation learned agent-based thinking. Its genius is **accessibility**: a deliberately simple
    **turtles-and-patches** language, an instant visual world, and a vast **Models Library**, all
    designed so a domain expert (or a student) can express an emergent-systems idea in minutes. It is
    the **lingua franca of ABM pedagogy** and a serious research prototyping tool.

> The most widely used ABM environment for teaching and research, with an accessible language and
> rich model library — the lingua franca of agent-based modeling pedagogy.

## Positioning card

| Axis (see [Taxonomy](../../foundations/taxonomy.md)) | NetLogo |
|------|------|
| Optimization vs Simulation | **Simulation** (ABM environment) |
| Top-down vs Bottom-up | **Bottom-up** |
| Equilibrium | N/A (model-defined) |
| Foresight | Model-defined |
| Deterministic vs Stochastic | Model-defined (usually stochastic) |
| Time / Space | **Tick-based / patch grid + turtles** |
| Solution method | **Agent (turtle/patch/link) step scheduler** |

| Field | Value |
|-------|-------|
| Full name | NetLogo |
| Domain | Frameworks & Environments |
| First release / current | 1999 / ongoing (NetLogo 6.x) |
| Institution · lead | Uri Wilensky — Center for Connected Learning (CCL), Northwestern |
| Language · solver | NetLogo language (JVM/Scala) |
| License / access | Free (GPL); source open |

---

## 🎓 Scholar Track

**History & motivation.** NetLogo was created by **Uri Wilensky in 1999** at Northwestern's **Center
for Connected Learning**, descending from the **Logo / StarLogo** educational-computing tradition (the
"turtle" of Logo). Its explicit mission is **learnability**: to let people *think with* agent-based
models without first becoming software engineers. That design choice — optimize for the human, accept
performance limits — made it the **default teaching platform** and, because ideas prototype so fast,
a heavily used **research** tool too (the [Wilensky & Rand textbook](#) is a field standard).

**Mathematical formulation.** NetLogo fixes **no domain math**; it provides an unusually clear
**ontology** for ABM. The world is a **grid of `patches`** (stationary agents with state and
behavior), a set of mobile **`turtles`** (agents that move over the continuous-within-grid space),
and **`links`** (network edges connecting turtles) — plus the **`observer`** (global control). Time
advances in **`ticks`**; behavior is written as procedures over **agentsets** (e.g. `ask turtles [ …
]`), with an implicit, usually **randomized activation** order. This tiny, consistent vocabulary —
turtles/patches/links/observer — is expressive enough for a stunning range of models (segregation,
epidemics, flocking, markets, ecology) while staying teachable in an afternoon. Everything is
**stochastic-capable** (built-in RNG with reproducible seeds) and instantly **visual** (the world view
renders agents live).

**Solution algorithm.** The canonical loop is a `go` procedure called each **tick**: `ask` the
relevant agentsets to run their behaviors (in randomized order), update patches, advance the tick, and
refresh the view. **BehaviorSpace** automates **parameter sweeps / experiments** across runs and seeds.

**Calibration & validation.** BehaviorSpace supports systematic experiments; external tools
(**RNetLogo**, **pyNetLogo**, **NL4Py**, and the **NetLogo controlling API**) drive NetLogo from
R/Python for calibration, sensitivity, and optimization — a common workflow pairing NetLogo's modeling
ease with the scientific-computing stack for analysis.

**Strengths / weaknesses / criticisms.** *Strengths:* **unmatched accessibility**, instant
visualization, huge **Models Library**, superb for teaching and rapid prototyping, reproducible RNG.
*Criticisms:* the JVM interpreter and single-machine design **cap performance/scale** (big or complex
models migrate to [Repast](repast.md)/[Mesa](mesa.md)); the domain-specific language is less flexible
than a general programming language for advanced software engineering.

## 🛠️ Engineer Track

**Architecture & engines.** A **[Behavior Engine](../../patterns/behavior-engine.md)** (turtles/patches)
over a built-in **[Spatial Engine](../../patterns/spatial-engine.md)** (patch grid + continuous
movement + link networks), a tick-based **[Integration Engine](../../patterns/integration-engine.md)**,
a first-class **[Visualization Engine](../../patterns/visualization-engine.md)** (the live world view,
the model's signature), and **BehaviorSpace** as a **[Sensitivity Engine](../../patterns/sensitivity-engine.md)**.
Runs on the **JVM** (implemented largely in Scala/Java).

**Data & complexity.** Optimized for **clarity over raw speed**; comfortable for tens of thousands of
agents interactively, with BehaviorSpace for batch runs. Very large models are out of scope by design.

**Openness / extensibility.** **Free and open (GPL)**; extensible via an **extensions API** (GIS, nw
networks, R, Python, ARM/robotics, LevelSpace for model-of-models) and controllable headless from
R/Python. Web variant **NetLogo Web** runs models in a browser.

## 🏛️ Architect Track

**Reusable patterns.** NetLogo's enduring contribution is its **ontology**: **turtles / patches /
links / observer** is a minimal, teachable decomposition of "agents + environment + network + global
control" that maps cleanly onto the atlas's engines. Also reusable: **live visualization as a
first-class, always-on feature** (you *see* emergence as it happens) and **BehaviorSpace** experiments
as a built-in norm, not an afterthought.

**Trade-offs & alternatives.** Among frameworks, NetLogo = **accessibility/pedagogy**, [Mesa](mesa.md)
= **Python ecosystem**, [Repast](repast.md) = **HPC/scale**, [GAMA](gama.md) = **GIS**. The recurring
move in practice is **prototype in NetLogo, scale in Repast/Mesa** once the concept is proven — NetLogo
lowers the *idea-to-model* time, the others lower the *model-to-scale* time. All are the
simulation-paradigm environments contrasted with the SD environment [Vensim](vensim.md).

**Adoption.** The **most-taught** ABM platform globally (universities, high schools, MOOCs); enormous
**Models Library**; widely used for research prototypes across social science, ecology, economics
(the CCL and the ABM textbook anchor a huge community).

**Ecosystem.** Northwestern CCL (NetLogo, NetLogo Web, HubNet for participatory sims, LevelSpace);
StarLogo lineage; controlling APIs (pyNetLogo, RNetLogo, NL4Py); peers Mesa, Repast, GAMA, AnyLogic.

**Research gaps.** Performance/scale (partially addressed by NL4Py + clusters); bridging DSL
simplicity with software-engineering rigor; standardized model description.

!!! quote "Lesson for the integrated simulator"
    NetLogo proves that **accessibility is a first-order design goal, not a nicety**. By giving ABM a
    tiny, consistent **ontology (turtles/patches/links/observer)** and an **always-on live
    visualization**, it collapsed the distance between *having an idea* and *running a model* — which
    is why it became the field's teaching language and a prolific source of research prototypes. For
    the integrated simulator the lessons are: expose a **small, coherent conceptual vocabulary** that
    domain experts can wield without deep programming; make **visualization of emergence a default**,
    not an add-on; build in **experiment/parameter-sweep tooling** (BehaviorSpace) as standard; and
    embrace a **prototype-then-scale** pathway — a low-friction front end that can hand a proven model
    off to a high-performance backend ([Repast](repast.md)). The right tool depends on the phase of
    work, so the simulator should support the whole arc.

## Major publications

- Wilensky, U. (1999). *NetLogo.* Center for Connected Learning, Northwestern University.
- Wilensky, U., Rand, W. (2015). *An Introduction to Agent-Based Modeling.* MIT Press.
- Tisue, S., Wilensky, U. (2004). "NetLogo: A simple environment for modeling complexity."
  *International Conference on Complex Systems*.

## See also
- Peers: [Mesa](mesa.md) · [Repast](repast.md) · [GAMA](gama.md) · Analogy: [Vensim](vensim.md) (SD environment)
- Patterns: [Behavior Engine](../../patterns/behavior-engine.md) · [Spatial Engine](../../patterns/spatial-engine.md) · [Visualization Engine](../../patterns/visualization-engine.md) · [Sensitivity Engine](../../patterns/sensitivity-engine.md)
- Positioning: [Taxonomy](../../foundations/taxonomy.md) · Quality bar: [DICE dossier](../../model-families/climate-iam/dice.md)
