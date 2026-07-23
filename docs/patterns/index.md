# Architecture Patterns

Across wildly different models, the *same software engines* recur. This section
catalogs them as reusable patterns — the raw material for a future integrated
simulator. Each pattern names its intent, the models that exemplify it, its interface,
and its trade-offs.

## The engine catalog

```mermaid
graph TD
    DP[Data Pipeline] --> SE[Scenario Engine]
    SE --> OE[Optimization Engine]
    SE --> BE[Behavior Engine]
    OE --> ME[Market Engine]
    BE --> ME
    ME --> CE[Climate Engine]
    ME --> EN[Energy Dispatch Engine]
    ME --> LE[Land Engine]
    CE --> SP[Spatial Engine]
    OE --> SN[Sensitivity Engine]
    SN --> CAL[Calibration Engine]
    CAL --> VAL[Validation Engine]
    VAL --> VIZ[Visualization Engine]
    OE --> POL[Policy Engine]
```

Legend: ✅ detailed page · ⬜ cataloged, page pending

| Pattern | Intent | Exemplars | |
|---------|--------|-----------|--|
| **[Scenario Engine](scenario-engine.md)** | Parameterize & manage policy experiments | every IAM; SSP/RCP frameworks | ✅ |
| **[Optimization Engine](optimization-engine.md)** | Maximize objective under module-supplied constraints | DICE, TIMES, OSeMOSYS, PyPSA | ✅ |
| **[Market Engine](market-engine.md)** | Clear supply & demand at a price | CGE, GTAP, DSGE | ✅ |
| **[Behavior Engine](behavior-engine.md)** | Heterogeneous agents + decision heuristics | Covasim, MATSim, ABMs | ✅ |
| **[Integration Engine](integration-engine.md)** | Stock-flow / ODE accumulation & feedback | Vensim/SD, DICE climate boxes | ✅ |
| **[Sensitivity Engine](sensitivity-engine.md)** | Response to parameter perturbation | Morris, Sobol, Monte-Carlo | ✅ |
| **[Calibration Engine](calibration-engine.md)** | Fit parameters to data | SAM, Bayesian, ABC, emulators | ✅ |
| **[Climate Engine](climate-engine.md)** | Emissions → concentration → temperature | DICE carbon/temp boxes, FAIR, MAGICC | ✅ |
| **[Energy Dispatch Engine](energy-dispatch-engine.md)** | Least-cost dispatch under network constraints | OSeMOSYS, TIMES, PyPSA | ✅ |
| **Technology Adoption Engine** | Diffusion / vintage turnover | GCAM, energy models | ⬜ |
| **Land Engine** | Land-use allocation & competition | GLOBIOM, MAgPIE | ⬜ |
| **Spatial Engine** | Gridded / networked space | SWAT, MODFLOW, SUMO | ⬜ |
| **Validation Engine** | Test against reality / benchmarks | backcasting, module emulation | ⬜ |
| **Policy Engine** | Encode instruments (taxes, standards, caps) | carbon-price modules | ⬜ |
| **Visualization Engine** | Communicate results | dashboards, scenario explorers | ⬜ |
| **Data Pipeline** | Ingest, clean, harmonize inputs | ETL front-ends | ⬜ |

## The recurring meta-pattern

The [DICE dossier](../model-families/climate-iam/dice.md) already shows the most
important one: an **Optimization Engine wrapping coupled domain modules**, with
policy quantities recovered from **shadow prices**, and the **most uncertain
assumption (the damage function) isolated as a swappable component**. Cataloging when
this pattern applies — versus a Behavior/Market-Engine simulation — is a central task
of the atlas.

!!! note "Status"
    Patterns are extracted *from* dossiers as they are written. **9 of 15** now have
    detailed pages — the core computational engines (Scenario, Optimization, Market,
    Behavior, Integration), the two cross-cutting UQ engines (Sensitivity, Calibration),
    and two domain engines with Gold referents (Climate, Energy Dispatch). The remaining
    engines (Technology-Adoption, Land, Spatial, Validation, Policy, Visualization,
    Data-Pipeline) are cataloged and will be detailed as their model families reach Gold.
