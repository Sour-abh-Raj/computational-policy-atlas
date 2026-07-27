# FRB/US — the Federal Reserve's macroeconometric model

!!! info "Bronze dossier"
    FRB/US is the **large-scale macroeconometric model** the U.S. Federal Reserve Board uses for forecasting
    and policy analysis — the workhorse behind questions like *how much of inflation is energy-driven?* and
    *how should the funds rate respond?* Unlike a stylized DSGE, it is a **big system of estimated
    behavioural equations** (hundreds of variables) with an explicit role for **expectations** (VAR-based or
    model-consistent), sitting between reduced-form time-series models and micro-founded DSGE.

> A large estimated-equation macroeconometric model of the U.S. economy used by the Federal Reserve for
> forecasting and monetary-policy analysis, with switchable expectations.

## Positioning card

| Axis (see [Taxonomy](../../foundations/taxonomy.md)) | FRB/US |
|------|------|
| Optimization vs Simulation | **Simulation** (estimated equations) |
| Top-down vs Bottom-up | **Top-down** (aggregate sectors) |
| Equilibrium | Dynamic; long-run equilibrium with sticky adjustment |
| Foresight | **Switchable** — VAR-expectations or model-consistent |
| Deterministic vs Stochastic | Deterministic baseline + stochastic simulations |
| Time / Space | Quarterly / U.S. economy |
| Solution method | **Estimated behavioural equations + expectations** |

| Field | Value |
|-------|-------|
| Full name | FRB/US — Federal Reserve Board / U.S. model |
| Domain | Economics (macro / monetary) |
| First release / current | 1996 / ongoing (public dataset + code) |
| Institution · lead | Federal Reserve Board |
| Language · solver | Python / EViews (public package) |
| License / access | Public (model + data released) |

---

## 🎓 Scholar Track

**History & motivation.** FRB/US replaced the Fed's older MPS model in 1996, designed to combine
**empirical fit** (equations estimated on data, so it tracks the actual economy) with **explicit
expectations** and a coherent long-run equilibrium — a middle path between atheoretic VARs and stylized
DSGE. It is central to how the Fed reasons about **inflation dynamics**, including the pass-through of
**energy and import prices** to core inflation — exactly the Energy⇄Inflation coupling Polyphony finds
*survives* on real data.

**Mathematical formulation.** A large system of **estimated equations** for spending, prices, wages,
finance, and the external sector, each with error-correction toward a theory-based long-run target and
polynomial-adjustment-cost dynamics for stickiness. Expectations enter explicitly and can be run as **VAR-
based** (limited-information) or **model-consistent** (rational). Policy is closed by a rule (e.g. Taylor).

**Calibration & validation.** Equations are **estimated** (not merely calibrated) and the model is
routinely validated by out-of-sample forecast performance and stochastic-simulation coverage — the
empirical discipline that makes it a natural reference for a project that insists couplings beat baselines
on real data.

**Strengths / weaknesses / criticisms.** *Strengths:* empirical fit, switchable expectations, transparency
(public code/data), policy realism. *Criticisms:* the Lucas critique (estimated equations may shift under
new policy regimes); large and complex; aggregate, so no distributional/heterogeneity detail.

## 🛠️ Engineer Track

**Architecture & engines.** A **[Market Engine](../../patterns/market-engine.md)** of estimated
supply/demand/price blocks over a **[Calibration Engine](../../patterns/calibration-engine.md)**
(estimation + error-correction), wrapped in a **[Scenario Engine](../../patterns/scenario-engine.md)**
(policy rules, stochastic simulations, alternative-expectations runs). Its signature is **estimated-equation
macro with switchable expectations**.

**Data & complexity.** Hundreds of equations/variables, quarterly; cheap to simulate, heavy to maintain and
re-estimate.

**Openness / extensibility.** The Fed **publicly releases** the FRB/US model package and dataset — unusually
open for a central-bank tool — enabling replication and extension.

## 🏛️ Architect Track

**Reusable patterns.** The transferable idea is the **estimated-equation middle path**: keep enough theory
for a coherent long run and explicit expectations, but let the data set the dynamics, so the model actually
tracks reality. For Energy⇄Inflation, FRB/US is the reference for a pass-through that is **empirically real
and forecast-relevant** — the kind of coupling that earns its keep.

**Trade-offs & alternatives.** FRB/US (estimated equations) vs [DSGE](dsge.md) (micro-founded, tighter
theory, weaker fit) vs pure VARs (atheoretic, best short-run fit): a spectrum from theory to data. FRB/US
deliberately sits in the middle; Polyphony's disagreement-reporting stance is that *which* point on that
spectrum is right is itself contested and should be exposed, not hidden.

**Adoption.** The Federal Reserve Board's staff forecasting and policy-analysis workhorse for nearly three
decades; widely used by researchers since its public release.

**Ecosystem.** Federal Reserve Board; the public FRB/US package; the broader macroeconometric and DSGE
communities.

**Research gaps.** Robustness to regime shifts (the Lucas critique); adding heterogeneity/distribution;
integrating financial-stability and climate-transition channels.

!!! quote "Lesson for the integrated simulator"
    FRB/US teaches that a coupling can be **empirically real and forecast-relevant** when the equations are
    estimated on data and validated out of sample — which is exactly why Polyphony's Energy⇄Inflation
    pass-through *survives* the real-data bar while six more speculative couplings were cut. Estimated fit is
    not a substitute for the honesty machinery (placebo, walk-forward, naive), but a coupling that clears
    all of them, as this one does, has earned a place.

## Major publications

- Brayton, F., & Tinsley, P. (1996). "A Guide to FRB/US." *Federal Reserve Board FEDS* 1996-42.
- Brayton, F., Laubach, T., & Reifschneider, D. (2014). "The FRB/US Model: A Tool for Macroeconomic Policy
  Analysis." *FEDS Notes*.

## See also
- Contrast: [DSGE](dsge.md) · [E3ME](e3me.md) · [EIRIN](../finance/eirin.md)
- Patterns: [Market Engine](../../patterns/market-engine.md) · [Calibration Engine](../../patterns/calibration-engine.md) · [Scenario Engine](../../patterns/scenario-engine.md)
- Positioning: [Taxonomy](../../foundations/taxonomy.md) · Quality bar: [DICE dossier](../../model-families/climate-iam/dice.md)
