# OpenABM-Covid19

!!! info "Bronze dossier"
    OpenABM-Covid19 is the **individual-based** epidemic model built at Oxford to answer one urgent
    question the 2020 pandemic posed: **can digital contact tracing suppress COVID-19?** It shares
    [Covasim](covasim.md)'s agent-based paradigm but is organized around **structured interaction
    networks** (household, workplace, school, random) and an explicit **contact-tracing / app**
    module, and it directly underpinned the mathematics behind exposure-notification apps.

> An open agent-based COVID-19 model built to evaluate digital contact tracing and non-pharmaceutical
> interventions on realistic demographic and interaction networks.

## Positioning card

| Axis (see [Taxonomy](../../foundations/taxonomy.md)) | OpenABM-Covid19 |
|------|------|
| Optimization vs Simulation | **Simulation** (agent-based) |
| Top-down vs Bottom-up | **Bottom-up** (individuals) |
| Equilibrium | N/A |
| Foresight | N/A / adaptive |
| Deterministic vs Stochastic | **Stochastic** |
| Time / Space | Daily / population + interaction networks |
| Solution method | **Monte-Carlo agent simulation on networks** |

| Field | Value |
|-------|-------|
| Full name | OpenABM-Covid19 |
| Domain | Health / Epidemiology |
| First release / current | 2020 / ongoing |
| Institution · lead | University of Oxford (Christophe Fraser group, Big Data Institute) |
| Language · solver | C (Python/`swig` interface) |
| License / access | Open (GPLv3 / MIT components) |

---

## 🎓 Scholar Track

**History & motivation.** OpenABM-Covid19 was built rapidly in early **2020** by **Christophe Fraser's
group at Oxford's Big Data Institute**, alongside their influential analysis showing SARS-CoV-2's
**pre-symptomatic transmission** made classic manual contact tracing too slow — motivating **digital
(app-based) instantaneous tracing**. The model was created to **quantify** whether such tracing, plus
NPIs, could keep $R$ below 1, and became a scientific foundation for exposure-notification apps.

**Mathematical formulation.** OpenABM is a **stochastic individual-based model** over a synthetic
population with realistic **age structure and household composition**. Each individual is embedded in
**multiple interaction networks**: a **household** network, **occupation/workplace and school**
networks, and a **random** (community) network — daily contacts are drawn from these layered networks.
Disease progresses through a detailed compartmental **natural-history** model per agent (susceptible →
exposed → pre-symptomatic/asymptomatic/symptomatic → recovered/hospitalized/ICU/death), with
**age-dependent** severity and **individual-level** timing drawn from clinical distributions.
Transmission along a contact depends on infectiousness (time-since-infection profile), network-type
weighting, and interventions. The distinctive module is **testing + contact tracing**: symptomatic
testing, **manual and digital tracing** (with adjustable app-uptake, tracing delay, and quarantine
adherence), and NPIs (lockdown, distancing, school closure) all act as **interventions** that modify
the contact networks and quarantine states. It is simulated by **Monte-Carlo** daily steps; ensembles
give distributions over epidemic trajectories.

**Solution algorithm.** Discrete daily loop: regenerate/adjust the day's contacts on each network,
draw transmission events, advance each infected agent's clinical state, apply testing/tracing/NPI
logic, and record. Written in **C** for speed with a **Python** interface for scenario scripting;
large populations (millions) are feasible.

**Calibration & validation.** Parameterized from clinical data (incubation, generation time, severity
by age) and demographic/household data; calibrated to observed case/death curves; validated against
epidemic data and cross-compared with other models during the pandemic response.

**Strengths / weaknesses / criticisms.** *Strengths:* **explicit network structure** and a
**first-class contact-tracing/app** module — purpose-built for the tracing question; fast C core;
open. *Criticisms:* like all individual ABMs it is **data- and parameter-hungry** and computationally
heavier than metapopulation ([GLEAM](gleam.md)) or ODE models; network specifications are
idealizations; single-region focus (not global spread).

## 🛠️ Engineer Track

**Architecture & engines.** A **[Behavior Engine](../../patterns/behavior-engine.md)** over **layered
interaction networks** (a network-flavored **[Spatial Engine](../../patterns/spatial-engine.md)**),
with a **[Policy Engine](../../patterns/policy-engine.md)** of intervention objects (testing, tracing,
app, NPIs) and a **[Calibration Engine](../../patterns/calibration-engine.md)**. Structurally it is a
close sibling of [Covasim](covasim.md); the emphasis differs — OpenABM foregrounds **networks +
tracing**, Covasim foregrounds **flexible intervention scripting and contact layers**. C core +
Python (`swig`) API.

**Data & complexity.** Millions of agents × layered networks × daily Monte-Carlo steps; C
implementation keeps national-scale runs tractable. Memory/compute scale with population × contacts.

**Openness / extensibility.** **Open source** (GitHub, GPL/MIT), with a Python API for scenario
sweeps; extensible interventions and network definitions; adopted and forked for other settings.

## 🏛️ Architect Track

**Reusable patterns.** Transferable ideas: **layered contact networks** as the substrate for
transmission (household/work/school/random as separable, independently-toggleable layers), and
**interventions as composable objects** — especially a **contact-tracing/app** abstraction with dials
for uptake, delay, and adherence. Both are exactly the **Policy Engine** philosophy applied to
epidemics.

**Trade-offs & alternatives.** OpenABM and [Covasim](covasim.md) are the two flagship **individual-
based** COVID models — same paradigm, complementary emphases (networks/tracing vs intervention
flexibility); either is the **micro** counterpoint to metapopulation [GLEAM](gleam.md) (global,
mesoscale) and to aggregate ODE/[system-dynamics](../frameworks/vensim.md) epidemic models. The choice
is the [Continuous vs Discrete](../../comparative/continuous-vs-discrete.md) / granularity trade-off:
individual realism for intervention design vs speed/coverage. Peers: Covasim, CovidSim (Imperial),
OpenABM forks.

**Adoption.** Directly informed **digital contact-tracing / exposure-notification** policy and app
design (the Fraser group's work underpinned NHS/Google-Apple-style analyses); used across pandemic
research and by public-health teams.

**Ecosystem.** Oxford Big Data Institute; OpenABM-Covid19 on GitHub; the Fraser-group instantaneous-
tracing literature; peers Covasim (IDM), CovidSim; general ABM toolkits like [Mesa](../frameworks/mesa.md).

**Research gaps.** Reducing parameter/data burden; behavior-response endogeneity (adherence as a
function of policy); coupling to mobility ([GLEAM](gleam.md)) and to economic impact; automated
calibration.

!!! quote "Lesson for the integrated simulator"
    OpenABM sharpens two atlas themes. First, **structure lives in the network**: representing contact
    as **separable, toggleable layers** (household, work, school, community) makes both transmission
    and interventions natural — you close schools by editing one layer — a pattern the integrated
    simulator should adopt wherever interaction structure matters. Second, it is a vivid case of
    **interventions as first-class, parameterized objects**: a *contact-tracing app* with dials for
    uptake, delay, and adherence is exactly the composable **Policy Engine** the atlas argues for, and
    the reason the model could answer a precise, urgent policy question fast. Together with
    [Covasim](covasim.md) and [GLEAM](gleam.md), OpenABM shows the simulator should host **multiple
    epidemic resolutions** (individual-network, metapopulation, aggregate) and route each question to
    the level where it is well-posed — running more than one and comparing when they overlap.

## Major publications

- Hinch, R., Probert, W., Fraser, C., et al. (2021). "OpenABM-Covid19—An agent-based model for
  non-pharmaceutical interventions against COVID-19 including contact tracing." *PLOS Computational
  Biology* 17(7).
- Ferretti, L., Fraser, C., et al. (2020). "Quantifying SARS-CoV-2 transmission suggests epidemic
  control with digital contact tracing." *Science* 368(6491).
- Wymant, C., Fraser, C., et al. (2021). "The epidemiological impact of the NHS COVID-19 app."
  *Nature* 594.

## See also
- Contrast: [Covasim](covasim.md) · [GLEAM](gleam.md) · [Continuous vs Discrete](../../comparative/continuous-vs-discrete.md) · Toolkit: [Mesa](../frameworks/mesa.md)
- Patterns: [Behavior Engine](../../patterns/behavior-engine.md) · [Policy Engine](../../patterns/policy-engine.md) · [Spatial Engine](../../patterns/spatial-engine.md) · [Calibration Engine](../../patterns/calibration-engine.md)
- Positioning: [Taxonomy](../../foundations/taxonomy.md) · Quality bar: [DICE dossier](../../model-families/climate-iam/dice.md)
