# Comparative Analyses

Head-to-head matrices along the axes defined in the
[Taxonomy](../foundations/taxonomy.md). Each matrix compares two paradigms on
assumptions, appropriate regime, failure modes, data needs, and computational cost.

!!! success "All 10 matrices complete"
    The comparative layer is finished — **10 of 10** full chapters, each with a positioning
    frame, a comparison table, a "why it changes the answer" diagram, when-each-applies,
    failure modes, a synthesis frontier, and a **lesson for the integrated simulator**.

## The ten matrices

| # | Matrix | The question it settles |
|--:|--------|--------------------------|
| 1 | ✅ **[Optimization vs Simulation](optimization-vs-simulation.md)** | Compute the *best*, or watch what *happens*? |
| 2 | ✅ **[Top-Down vs Bottom-Up](top-down-vs-bottom-up.md)** | Aggregate economy, or explicit technologies? |
| 3 | ✅ **[Equilibrium vs Disequilibrium](equilibrium-vs-disequilibrium.md)** | Do markets clear? |
| 4 | ✅ **[ABM vs CGE](abm-vs-cge.md)** | Emergence from agents, or imposed consistency? |
| 5 | ✅ **[System Dynamics vs Agent-Based](system-dynamics-vs-abm.md)** | Aggregate feedback, or individual interaction? |
| 6 | ✅ **[IAM vs Energy-System Models](iam-vs-energy.md)** | *How much* to abate, or *how* to deliver it? |
| 7 | ✅ **[LP vs MILP](lp-vs-milp.md)** | The price of an integer |
| 8 | ✅ **[Recursive-Dynamic vs Perfect Foresight](recursive-vs-perfect-foresight.md)** | How much does the model know about its future? |
| 9 | ✅ **[Deterministic vs Stochastic](deterministic-vs-stochastic.md)** | One trajectory, or a distribution? |
| 10 | ✅ **[Continuous vs Discrete](continuous-vs-discrete.md)** | Smooth flows, or countable events? |

!!! note "How to read these"
    These are decision aids, not verdicts. Where paradigms genuinely disagree the atlas
    **documents both** — the point is to know *which regime* each is right for, so an
    integrated simulator can route subsystems to the appropriate tool. Several matrices show
    the *same* policy can flip sign or change cost depending on the axis choice — that
    conditionality is the headline finding, not a flaw.

## The recurring lesson

Read together, the ten matrices converge on one design principle for a next-generation
simulator: **make each contested modeling assumption an explicit, switchable dial**, route
every question to the paradigm where it is valid, and — where two paradigms overlap — run
both and **report the disagreement** as a measure of model uncertainty rather than hiding it
behind a single number.
