# CityScope

!!! info "Bronze dossier"
    CityScope is the atlas's **participatory, tangible** modeling platform — the one entry whose primary
    innovation is the **human-model interface**, not the internal mathematics. MIT's City Science group
    built it so that stakeholders gathered around a **physical tabletop of illuminated LEGO-like blocks**
    can *rearrange the city with their hands* and watch **agent-based and data-driven indicators** update
    in real time. It embodies the atlas's [Visualization Engine](../../patterns/visualization-engine.md)
    argument taken to its physical, collaborative extreme.

> A tangible, interactive urban-simulation and decision-support platform combining physical tabletop
> interfaces with agent-based and data-driven models for participatory planning.

## Positioning card

| Axis (see [Taxonomy](../../foundations/taxonomy.md)) | CityScope |
|------|------|
| Optimization vs Simulation | **Simulation** (agent-based + data-driven indicators) |
| Top-down vs Bottom-up | **Bottom-up** |
| Equilibrium | N/A |
| Foresight | Myopic / **interactive** |
| Deterministic vs Stochastic | Mixed |
| Time / Space | **Interactive (real-time)** / neighborhood grid |
| Solution method | ABM + indicator models behind a **tangible UI** |

| Field | Value |
|-------|-------|
| Full name | CityScope |
| Domain | Urban |
| First release / current | 2010s / ongoing |
| Institution · lead | MIT Media Lab — City Science group (Kent Larson, Ariel Noyman) |
| Language · solver | JavaScript / Python + tangible (LEGO + projection/scanner) UI |
| License / access | Open (varies by module) |

---

## 🎓 Scholar Track

**History & motivation.** CityScope was developed by the **MIT Media Lab's City Science group** (Kent
Larson and collaborators, incl. Ariel Noyman) in the 2010s to attack a **process** failure in urban
planning, not a modeling gap: expert models are opaque to the stakeholders whose neighborhoods they
describe, so planning decisions lack shared understanding and buy-in. CityScope's proposition is
**tangible, collaborative modeling** — turn the model into a **physical, manipulable table** that
non-experts can reason with together, collapsing the distance between *changing an assumption* and
*seeing its consequences* to the act of moving a block.

**Mathematical formulation.** CityScope is a **platform** rather than a single model; its internal
mathematics is an assembly of **agent-based and data-driven indicator models**, but its defining formal
content is the **tangible-interface loop**. A tabletop of **tagged physical blocks** (each encoding a
land use, building type, or intervention) on a grid is **scanned** (computer vision / RFID) into a
**digital state**; that state drives **real-time models** — pedestrian/mobility **ABM**, accessibility
and **proximity ("15-minute city") metrics**, daylight/energy, density, and diversity **indicators** —
whose outputs are **projected back onto the table** and screens. The loop is
**physical change → sensing → model recompute → projection**, closed in seconds, so a group **iterates
interactively**. Models are chosen for **responsiveness** (fast enough for live interaction) over
exhaustive fidelity — a deliberate accuracy-for-interactivity trade.

**Solution algorithm.** A **real-time interaction loop**: continuously scan the tabletop, update the
digital scenario, recompute lightweight ABM/indicator models, and re-project results — running as long
as the workshop does. Heavier analyses (full MATSim-style runs) can be attached asynchronously.

**Calibration & validation.** Indicator and ABM modules are calibrated to city data (mobility surveys,
GIS, census); "validation" also includes a **human-factors** dimension — does the tool improve
stakeholder understanding and decision quality? — evaluated in workshops and deployments.

**Strengths / weaknesses / criticisms.** *Strengths:* **participation, communication, and rapid
what-if** exploration; makes modeling **legible and collaborative**; strong for engagement and education.
*Criticisms:* models are **simplified for speed** (not a substitute for detailed LUTI like
[UrbanSim](urbansim.md)/[SILO](silo.md)); neighborhood-scale; results depend on which indicators are
shown (framing effects); hardware/setup overhead.

## 🛠️ Engineer Track

**Architecture & engines.** A tangible-input layer (CV/RFID **scanner**) → a **digital scenario state** →
lightweight **[Behavior Engine](../../patterns/behavior-engine.md)** (pedestrian/mobility ABM) and
**indicator** modules → a **[Visualization Engine](../../patterns/visualization-engine.md)** (projection
mapping + dashboards). It is essentially a **[Scenario Engine](../../patterns/scenario-engine.md)** with a
**physical controller** and a real-time render loop — the Visualization/Interaction pattern made literal.
Modular web (JS) + Python analytics; hardware = table, blocks, projector, camera.

**Data & complexity.** Deliberately **lightweight** models for real-time response; complexity budget is
spent on **latency** (sense→compute→project must feel instant), not on maximal simulation depth.

**Openness / extensibility.** **Open** (many modules on MIT City Science GitHub); a modular ecosystem of
indicator/ABM plugins; deployed as workshops and installations worldwide; **Brain**/CityScope module
framework for adding analyses.

## 🏛️ Architect Track

**Reusable patterns.** CityScope's contribution is architectural in the **human dimension**: a
**real-time sense→model→project interaction loop** with a **tangible controller**, and a **portfolio of
fast indicators** designed for *legibility and responsiveness*. It is the strongest expression in the
atlas of **participatory modeling** — models as shared decision instruments, not just analyst tools.

**Trade-offs & alternatives.** Within urban, CityScope trades the **analytical depth** of
[UrbanSim](urbansim.md)/[SILO](silo.md) for **interactivity, legibility, and participation** — different
tools for different phases (engage/ideate vs forecast). It is the physical-tabletop cousin of live
interactive climate tools like **En-ROADS** (see [Visualization Engine](../../patterns/visualization-engine.md))
and of [Stella](../frameworks/stella.md)'s "flight-simulator" interfaces. Peers: UrbanSim/SILO (analytic
LUTI), Envision Tomorrow, participatory-GIS tools.

**Adoption.** Used in **planning workshops, universities, and city engagements** worldwide (MIT City
Science network and partner labs) for participatory scenario design — transit, zoning, 15-minute-city,
and resilience conversations.

**Ecosystem.** MIT Media Lab City Science; CityScope module framework (mobility, proximity, density,
daylight indicators); partner City Science Labs globally; couples to detailed models asynchronously.

**Research gaps.** Rigor vs responsiveness balance; validating participatory outcomes; coupling live
tangible tools to detailed back-end models; avoiding indicator-framing bias.

!!! quote "Lesson for the integrated simulator"
    CityScope insists that **who can use the model, and how, is part of the model's design** — a theme the
    atlas raises with [Stella](../frameworks/stella.md), NetLogo, and the
    [Visualization Engine](../../patterns/visualization-engine.md), pushed here to its physical, collective
    extreme. Its **real-time sense → recompute → project interaction loop** shows that **legibility and
    responsiveness** are first-class requirements, sometimes worth trading fidelity for, because a model
    that stakeholders can *manipulate together* changes decisions in ways an opaque batch model cannot. For
    the integrated simulator this argues for **interactive, low-latency front ends** and **participatory
    modes** layered over the heavy engines — and for a **tiered fidelity** design where fast indicator
    models drive live interaction while detailed models run asynchronously. The deepest lesson: a
    world-class policy simulator is not only an analytical instrument but a **shared decision-making
    environment**, and its interface is where analysis becomes policy.

## Major publications

- Alonso, L., Noyman, A., Larson, K., et al. (2018). "CityScope: A Data-Driven Interactive Simulation
  Tool for Urban Design." *Unifying Themes in Complex Systems IX (ICCS 2018)*, Springer.
- Noyman, A., et al. (2017). "Finding Places: HCI Platform for Public Participation in Refugees'
  Accommodation Process." *Procedia Computer Science* 112.
- Grignard, A., Alonso, L., Noyman, A., Larson, K., et al. (2018). "The CityScope platform for real-time
  participatory urban design." (City Science / CUPUM).

## See also
- Urban peers: [UrbanSim](urbansim.md) · [SILO](silo.md) · Interaction kin: [Stella](../frameworks/stella.md) · [Visualization Engine](../../patterns/visualization-engine.md)
- Patterns: [Visualization Engine](../../patterns/visualization-engine.md) · [Scenario Engine](../../patterns/scenario-engine.md) · [Behavior Engine](../../patterns/behavior-engine.md)
- Positioning: [Taxonomy](../../foundations/taxonomy.md) · Quality bar: [DICE dossier](../../model-families/climate-iam/dice.md)
