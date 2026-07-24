# E3ME — Energy–Economy–Environment Macro-Econometric Model

!!! info "Bronze dossier"
    E3ME is the atlas's flagship **disequilibrium** economy-wide model — the deliberate
    counterpole to [CGE](cge.md)/[GTAP](gtap.md). Its behavioral equations are **econometrically
    estimated** from historical data rather than derived from optimization, its closure is
    **post-Keynesian and demand-led** (no imposed full employment), and money/finance are explicit.
    It is the reference tool for arguing that climate policy can yield a **double dividend** — an
    answer CGE's optimizing closure largely rules out by construction.

> A global macro-econometric (post-Keynesian) E3 model: parameters are econometrically estimated,
> demand-driven and explicitly *non*-equilibrium — a deliberate alternative to CGE's optimizing
> closure.

## Positioning card

| Axis (see [Taxonomy](../../foundations/taxonomy.md)) | E3ME |
|------|------|
| Optimization vs Simulation | **Simulation** (econometric) |
| Top-down vs Bottom-up | Top-down (with bottom-up energy: E3ME-FTT) |
| Equilibrium | **Disequilibrium** (demand-led, post-Keynesian) |
| Foresight | **Adaptive / backward-looking** |
| Deterministic vs Stochastic | Deterministic (estimated parameters) |
| Time / Space | Annual / 60+ regions, 40+ sectors |
| Solution method | **Estimated simultaneous equations** (iterated) |

| Field | Value |
|-------|-------|
| Full name | E3ME — Energy–Economy–Environment Macro-Econometric model |
| Domain | Economics — Equilibrium & Macro |
| First release / current | 1990s (E3ME lineage) / ongoing |
| Institution · lead | Cambridge Econometrics |
| Language · solver | Fortran + database (commercial) |
| License / access | Commercial / licensed (documentation open) |

---

## 🎓 Scholar Track

**History & motivation.** E3ME grew from EU research projects in the 1990s and is maintained by
**Cambridge Econometrics**, rooted in the **Cambridge (post-Keynesian) tradition** of applied
macro-econometrics. Its founding conviction is a direct critique of CGE: real economies are **not**
in continuous optimizing equilibrium — they have **involuntary unemployment, spare capacity, and
path-dependent behavior** — so a model should **estimate how the economy actually behaves** from
data, not assume optimizing agents clearing all markets. This closure is why E3ME can find that a
carbon tax recycled well **raises** GDP and employment (a "double dividend"), whereas a
full-employment CGE typically shows a cost.

**Mathematical formulation.** E3ME is a system of ~**20+ econometrically estimated behavioral
equations** per region (for consumption, investment, employment, trade, prices, wages, energy demand,
etc.), estimated as **error-correction / cointegration** specifications so each has a long-run
relationship and short-run dynamics. There is **no objective function and no market-clearing
identity forcing full employment**; instead output is **demand-determined** (à la Keynes),
quantities adjust before/alongside prices, and money and finance are explicit. The three "E"s are
integrated: the **economy** drives **energy** demand, energy drives **emissions (environment)**, and
feedbacks (energy prices, damages, policy revenue) return to the economy. Recent versions couple a
**bottom-up technology-diffusion module, FTT (Future Technology Transformations)** — an evolutionary,
logit-share adoption model — replacing the single-equation energy demand with technology-level
dynamics.

**Solution algorithm.** Given estimated parameters, the simultaneous system is solved **year by
year** by iteration to a consistent annual solution, then stepped forward — **adaptive, not
forward-looking**: agents respond to past and current conditions, so there is no perfect-foresight
optimization. This makes E3ME **recursive and path-dependent** by construction.

**Calibration & validation.** Uniquely in this family, parameters are **estimated on historical
time series** (decades of Eurostat/OECD/IEA data) rather than calibrated to a single base-year SAM —
so the model carries **statistical confidence intervals** and can be **validated by econometric
fit and backcasting**, a genuinely different validation stance from CGE calibration.

**Strengths / weaknesses / criticisms.** *Strengths:* **empirically grounded** behavior;
represents **unemployment and spare capacity** (can show non-zero-sum policy outcomes); explicit
money/finance; natural fit for **just-transition and employment** questions. *Criticisms:*
econometric equations assume the **future resembles the estimation period** (Lucas-critique
vulnerability); less transparent micro-foundations than CGE; **commercial/closed** code limits
scrutiny; results are sensitive to the estimated closure that drives the double-dividend finding.

## 🛠️ Engineer Track

**Architecture & engines.** A **[Market Engine](../../patterns/market-engine.md)** built from
**estimated equations** rather than optimization, fused with an **energy/emissions
[Integration Engine](../../patterns/integration-engine.md)** and, in E3ME-FTT, a bottom-up
**[Technology-Adoption Engine](../../patterns/technology-adoption-engine.md)** (logit diffusion).
Its **[Calibration Engine](../../patterns/calibration-engine.md)** is *econometric estimation* — the
distinguishing engine relative to SAM-calibrated CGE. Implemented in Fortran over a large historical
database.

**Data & complexity.** 60+ regions × 40+ sectors × annual time series; the heavy lift is the
**estimation dataset** and its maintenance. Solve is a fast iterated simultaneous system per year.

**Openness / extensibility.** **Commercial** (Cambridge Econometrics), though the model manual is
public and the **FTT** modules have open academic implementations (e.g. at Exeter/C-EENRG).
Extensible through the FTT technology modules and regional/sectoral disaggregation.

## 🏛️ Architect Track

**Reusable patterns.** The transferable ideas: a **behavioral core estimated from data** (with
confidence intervals) rather than assumed-optimal, a **demand-led / disequilibrium closure** as a
*switchable alternative* to market clearing, and **coupling a macro core to an evolutionary
technology-diffusion module** (FTT) instead of least-cost optimization.

**Trade-offs & alternatives.** E3ME is the explicit `alternative_to` [CGE](cge.md)/[GTAP](gtap.md):
same economy-wide scope, opposite closure — **estimated & demand-led** vs **calibrated & supply-
clearing**. The disagreement is not a bug but *the* finding: run both and the **gap between them is
the policy uncertainty** (does carbon pricing cost or pay?). This is the central case study of the
[Equilibrium vs Disequilibrium](../../comparative/equilibrium-vs-disequilibrium.md) chapter and a
prime example for [Optimization vs Simulation](../../comparative/optimization-vs-simulation.md). Its
FTT coupling contrasts with GCAM/energy-model least-cost technology choice.

**Adoption.** Used by the **European Commission**, national governments, and NGOs for climate/energy
policy, employment and just-transition analysis; prominent in debates where the CGE "cost" framing is
contested.

**Ecosystem.** Cambridge Econometrics (E3ME, E3-India, E3-US, E3ME-FTT); the **FTT** family (FTT:Power,
FTT:Transport, FTT:Heat); peers: CGE/GTAP/GEM-E3 (equilibrium side), other macro-econometric models
(NiGEM, Oxford Global).

**Research gaps.** Lucas-critique robustness (estimated behavior under regime change); opening the
code; reconciling estimated closure with micro-foundations; uncertainty propagation.

!!! quote "Lesson for the integrated simulator"
    E3ME is the atlas's proof that **the market-clearing assumption is itself a dial, not a law**.
    The same economy-wide question — "what does a carbon tax do to GDP and jobs?" — flips sign
    depending on whether you impose optimizing full-employment equilibrium ([CGE](cge.md)/[GTAP](gtap.md))
    or an estimated demand-led disequilibrium (E3ME). An integrated simulator must therefore
    **support both closures as first-class, switchable options** and, crucially, **run both and report
    the disagreement** rather than hard-coding one worldview — the recurring thesis of this atlas.
    E3ME also models a different **validation culture**: parameters *estimated from history with
    confidence intervals*, not calibrated to a single year — a stance the simulator should be able to
    adopt wherever data supports it. And its FTT coupling shows how to graft **evolutionary technology
    diffusion** onto a macro core as an alternative to least-cost optimization.

## Major publications

- Cambridge Econometrics (2019/2022). *E3ME Technical Manual, v6/v9.* (public documentation).
- Mercure, J.-F., et al. (2018). "Macroeconomic impact of stranded fossil fuel assets" (E3ME-FTT).
  *Nature Climate Change* 8.
- Pollitt, H., Mercure, J.-F. (2018). "The role of money and the financial sector in energy-economy
  models used for assessing climate policy." *Climate Policy* 18(2).

## See also
- Alternative to: [CGE](cge.md) · [GTAP](gtap.md) · Contrast: [Input–Output](input-output.md) · [DSGE](dsge.md) · [Equilibrium vs Disequilibrium](../../comparative/equilibrium-vs-disequilibrium.md)
- Patterns: [Market Engine](../../patterns/market-engine.md) · [Calibration Engine](../../patterns/calibration-engine.md) · [Technology-Adoption Engine](../../patterns/technology-adoption-engine.md)
- Positioning: [Taxonomy](../../foundations/taxonomy.md) · Quality bar: [DICE dossier](../../model-families/climate-iam/dice.md)
