# Comparative Analyses

Head-to-head matrices along the axes defined in the
[Taxonomy](../foundations/taxonomy.md). Each planned matrix compares two paradigms on
assumptions, appropriate regime, failure modes, data needs, and computational cost.

## Planned matrices

- Optimization vs Simulation
- ABM vs CGE
- IAM vs Energy-System models
- System Dynamics vs Agent-Based
- Recursive-Dynamic vs Perfect Foresight
- LP vs MILP
- Top-Down vs Bottom-Up
- Equilibrium vs Disequilibrium
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
