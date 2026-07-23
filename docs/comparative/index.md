# Comparative Analyses

Head-to-head matrices along the axes defined in the
[Taxonomy](../foundations/taxonomy.md). Each planned matrix compares two paradigms on
assumptions, appropriate regime, failure modes, data needs, and computational cost.

## Matrices

- ✅ **[Optimization vs Simulation](optimization-vs-simulation.md)** — the deepest divide (full chapter)
- ✅ **[Top-Down vs Bottom-Up](top-down-vs-bottom-up.md)** — the energy-economy gap (full chapter)
- ✅ **[Equilibrium vs Disequilibrium](equilibrium-vs-disequilibrium.md)** — how coordination happens (full chapter)
- ✅ **[ABM vs CGE](abm-vs-cge.md)** — emergence vs equilibrium, the two ways to build an economy (full chapter)
- ✅ **[System Dynamics vs Agent-Based](system-dynamics-vs-abm.md)** — aggregate feedback vs individual interaction (full chapter)
- ✅ **[IAM vs Energy-System Models](iam-vs-energy.md)** — the same climate problem at two scales (full chapter)
- ✅ **[LP vs MILP](lp-vs-milp.md)** — the price of an integer (full chapter)
- Recursive-Dynamic vs Perfect Foresight
- Deterministic vs Stochastic
- Continuous vs Discrete

## Sample matrix — Optimization vs Simulation

A first, illustrative matrix (the full set follows the same schema):

| Dimension | **Optimization** | **Simulation** |
|-----------|------------------|----------------|
| Question answered | Normative — *what is best?* | Positive — *what will happen?* |
| Core object | Objective + constraints | Rules / behaviors / transitions |
| System-level goal | Yes — extremized | None — outcomes emergent |
| Foresight | Often perfect | Typically none / adaptive |
| Typical math | LP/MILP/NLP, optimal control | ODEs, stochastic stepping, agent rules |
| Multiplicity of outcomes | One optimum (per scenario) | Distribution of outcomes |
| Behavioral realism | Low (rational optimizer) | Potentially high (heuristics, heterogeneity) |
| Interpretability | High (duals, shadow prices) | Lower (emergent, path-dependent) |
| Exemplars | DICE, TIMES, OSeMOSYS, PyPSA | Mesa/NetLogo ABMs, Vensim SD, MATSim |
| Fails when… | agents aren't optimizing / can't foresee | you need a normative optimum / calibration is thin |

!!! note
    These are decision aids, not verdicts. Where paradigms genuinely disagree the atlas
    **documents both** — the point is to know *which regime* each is right for, so an
    integrated simulator can route subsystems to the appropriate tool.
