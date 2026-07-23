# Pattern — Climate Engine

!!! abstract "Pattern at a glance"
    **Intent:** translate a path of **emissions** into **atmospheric concentrations**,
    **radiative forcing**, and **temperature** — the physical core that turns an economic
    policy into a climate outcome.
    **Also known as:** carbon-cycle + energy-balance module, simple climate model (SCM),
    climate emulator.
    **Grounded in:** the carbon/temperature boxes of
    [DICE](../model-families/climate-iam/dice.md); the standalone emulators **FAIR** and
    **MAGICC**.

## Problem & forces

An economic or energy model produces **emissions**; policy relevance requires knowing the
**warming** they cause. Full Earth-System Models (ESMs) answer this with millions of CPU
hours — impossible to embed inside an optimization loop. The Climate Engine is a
**reduced-order emulator** capturing the ESM's input→output behavior cheaply. The forces:

- **Speed vs fidelity** — it must run thousands of times inside a
  [scenario](scenario-engine.md)/[optimization](optimization-engine.md) loop, so it must be
  small (a few state variables), yet track the ESMs it emulates.
- **Conservation & lags** — carbon accumulates and redistributes among reservoirs; heat
  takes decades to reach the deep ocean. These are **stocks with delays** (an
  [Integration Engine](integration-engine.md) instance).
- **Emulation target** — parameters are tuned so the simple model reproduces the assessed
  range of complex models (an inverse/[calibration](calibration-engine.md) problem).

## Structure

```mermaid
graph LR
    E[Emissions path<br/>CO2, non-CO2] --> C[Carbon cycle<br/>reservoir boxes]
    C --> CONC[Concentration / stock]
    CONC --> F[Radiative forcing<br/>F = η·ln(C/C0) + Fother]
    F --> T[Energy balance<br/>atm & ocean heat boxes]
    T --> TEMP[Temperature anomaly ΔT]
    TEMP -.feedback.-> C
```

Canonically (as in [DICE](../model-families/climate-iam/dice.md)): a **3-box carbon cycle**
(atmosphere / upper ocean+biosphere / deep ocean), a logarithmic **forcing** relation, and
a **2-box energy balance** (atmosphere-surface / deep ocean) giving the temperature
anomaly. Everything is linear/log — deliberately, so it inverts and differentiates cleanly.

## Interface

```
emissions(t) → carbon_cycle → concentration(t)
concentration → forcing:  F(t) = η·log2(C/C_preindustrial) + F_exogenous
forcing → energy_balance → ΔT_atmosphere(t), ΔT_ocean(t)
params tuned to emulate ESM ensemble (TCR, ECS, carbon-cycle response)
```

## Exemplars

| Emulator | Origin | Role |
|----------|--------|------|
| [DICE](../model-families/climate-iam/dice.md) climate module | Nordhaus | Embedded in the welfare optimization; SCC depends on it |
| **FAIR** | Millar/Smith (Leach et al.) | Open Python emulator; used in IPCC AR6 |
| **MAGICC** | Meinshausen et al. | The workhorse emulator across IAM scenario runs |
| Hector, CICERO-SCM | various | Alternative reduced-complexity models |

## Trade-offs & variants

- **Box models vs impulse-response** — explicit reservoir boxes (DICE) vs convolution of an
  impulse-response function (FAIR); mathematically close, different ergonomics.
- **Climate sensitivity as the master dial** — ECS/TCR dominate the output spread; a prime
  target for the [Sensitivity Engine](sensitivity-engine.md).
- **CO₂-only vs multi-gas** — richer emulators track CH₄, N₂O, aerosols separately.
- **Emulator fidelity** — a simple model is only as good as its calibration to the ESM
  ensemble; it can miss nonlinearities and tipping points.

!!! quote "Lesson for the integrated simulator"
    The Climate Engine is the archetype of a **reduced-order emulator**: a small, fast,
    differentiable surrogate that lets an expensive physical truth participate in an
    economic optimization loop. The design lesson generalizes far beyond climate — *any*
    subsystem too costly to simulate at full fidelity (a power grid, an ice sheet, a
    hydrological basin) should be wrapped as a calibrated emulator with an explicit,
    **swappable fidelity level** and its **key uncertain parameter exposed as a dial**
    (here, climate sensitivity). Crucially, the emulator must be honest about its envelope:
    the simulator should record what ESM ensemble it was tuned to and flag when a scenario
    pushes it outside that range, so a cheap surrogate never silently fabricates confidence.

## See also
- [Integration Engine](integration-engine.md) · [Optimization Engine](optimization-engine.md) · [Sensitivity Engine](sensitivity-engine.md)
- [DICE dossier](../model-families/climate-iam/dice.md) · [Patterns catalog](index.md)
