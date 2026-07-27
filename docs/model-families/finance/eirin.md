# EIRIN — a stock-flow-consistent macro-finance model

!!! info "Bronze dossier"
    EIRIN is a **stock-flow-consistent (SFC)** behavioural macro-finance model — the counterpart, on the
    *finance* side, to the real-economy IAMs elsewhere in the atlas. It represents households, firms,
    banks, a central bank and a government as interlocking **balance sheets** whose every flow is
    accounted (no money leaks), and studies how **financial shocks and climate transition risk** propagate
    through credit, asset prices, and output. It is a leading tool in the **climate-financial-risk**
    literature (stranded assets, transition-risk stress tests).

> A stock-flow-consistent, behavioural model of the macro-financial system used to trace how financial
> and climate-transition shocks propagate through balance sheets to credit, asset prices, and output.

## Positioning card

| Axis (see [Taxonomy](../../foundations/taxonomy.md)) | EIRIN |
|------|------|
| Optimization vs Simulation | **Simulation** (dynamic accounting + behaviour) |
| Top-down vs Bottom-up | **Meso** (sectoral balance sheets) |
| Equilibrium | **Disequilibrium** (out-of-equilibrium dynamics) |
| Foresight | **Adaptive / boundedly rational** |
| Deterministic vs Stochastic | Scenario-driven, shock experiments |
| Time / Space | Annual / economy-wide |
| Solution method | **Stock-flow-consistent accounting + behavioural rules** |

| Field | Value |
|-------|-------|
| Full name | EIRIN — a stock-flow-consistent behavioural macro-finance model |
| Domain | Finance / Systemic Risk |
| First release / current | ~2015 / ongoing |
| Institution · lead | RFF-CMCC / EIEE (Irene Monasterolo and collaborators) |
| Language · solver | Python / R; SFC solver |
| License / access | Research tool |

---

## 🎓 Scholar Track

**History & motivation.** EIRIN grew from the **stock-flow-consistent** tradition (Godley-Lavoie) fused
with the **financial-instability** view (Minsky) and the **financial-accelerator** channel
(Bernanke-Gertler-Gilchrist 1999): financial conditions are not a passive veil on the real economy but an
*amplifier* — leverage, collateral values, and credit spreads feed back into investment and output. Its
distinctive application is **climate transition risk**: a carbon-price or stranded-asset shock hits firm
balance sheets, propagates through banks, and shows up as macro instability — a question real-economy IAMs
miss.

**Mathematical formulation.** A closed system of **balance-sheet identities** (every asset is someone's
liability; every flow has a source and a use) plus **behavioural rules** for consumption, investment,
lending, and portfolio choice. Dynamics are **out-of-equilibrium**: agents adapt with bounded rationality
and the system need not clear each period. Financial stress is endogenous — a shock is amplified by
deleveraging and spread widening, the mechanism the atlas's reduced-form finance voice caricatures.

**Calibration & validation.** Calibrated to national accounts and flow-of-funds data; validated by
**scenario plausibility** and reproduction of stylised crisis dynamics, not out-of-sample forecast skill —
the same limitation, and the same reason for Polyphony's real-data + placebo discipline, as the other
integrated tools.

**Strengths / weaknesses / criticisms.** *Strengths:* accounting consistency (no phantom money),
endogenous financial instability, a natural home for climate-transition risk. *Criticisms:* behavioural
rules are calibrated not micro-founded; meso aggregation hides network structure; scenario contrasts, not
validated predictions.

## 🛠️ Engineer Track

**Architecture & engines.** A **[Behavior Engine](../../patterns/behavior-engine.md)** (sectoral decision
rules) over a stock-flow-consistent **[Integration Engine](../../patterns/integration-engine.md)** (the
balance-sheet accounting stepped through time), driven by a **[Scenario Engine](../../patterns/scenario-engine.md)**
(shock/policy experiments). Its signature is **accounting-closed macro-finance dynamics**.

**Data & complexity.** Modest: a system of sectoral balances and behavioural equations; the effort is
consistent balance-sheet data and rule calibration.

**Openness / extensibility.** A research codebase; extensible with sectors, asset classes, and
climate-damage/transition channels.

## 🏛️ Architect Track

**Reusable patterns.** The transferable idea is **stock-flow consistency as a discipline**: if every flow
is accounted, a model *cannot* quietly create or destroy value — a structural honesty guarantee. For the
Macro⇄Finance coupling, EIRIN is the reference for treating finance as an **amplifier with its own
dynamics**, which the atlas's reduced financial-accelerator voice mimics (a credit shock building to a
delayed output trough).

**Trade-offs & alternatives.** SFC macro-finance (EIRIN) vs DSGE with a financial accelerator ([DSGE](../economics/dsge.md))
vs financial-network/systemic-risk models: SFC buys accounting consistency and out-of-equilibrium
dynamics at the cost of micro-foundations; DSGE the reverse. Complementary lenses on the same
finance→output channel.

**Adoption.** Climate-financial-risk research; transition-risk stress-test design; central-bank and
supervisor-adjacent scenario work (NGFS-style).

**Ecosystem.** RFF-CMCC / EIEE; the SFC and climate-finance research communities; links to climate IAMs on
the transition-risk side.

**Research gaps.** Network/contagion structure; empirical validation of behavioural rules; coupling to
real-economy IAMs end to end — a nexus the atlas's Macro⇄Finance loop gestures at.

!!! quote "Lesson for the integrated simulator"
    EIRIN teaches **stock-flow consistency** as a built-in honesty constraint — a model that must balance
    every account cannot hide leakage — and it teaches that **finance is an amplifier with its own
    dynamics**, not a passive veil. Polyphony keeps both ideas in its reduced Macro⇄Finance voice, and
    subjects the resulting coupling to the same real-data + placebo gate as every other: a plausible
    amplifier must still out-predict a rival and a placebo, or be cut.

## Major publications

- Monasterolo, I., & Raberto, M. (2018). "The EIRIN flow-of-funds behavioural model of green fiscal
  policies and green sovereign bonds." *Ecological Economics* 144.
- Bernanke, B., Gertler, M., & Gilchrist, S. (1999). "The financial accelerator in a quantitative
  business cycle framework." *Handbook of Macroeconomics*.
- Gilchrist, S., & Zakrajšek, E. (2012). "Credit spreads and business cycle fluctuations." *American
  Economic Review* 102(4).

## See also
- Contrast: [DSGE](../economics/dsge.md) · [E3ME](../economics/e3me.md)
- Patterns: [Behavior Engine](../../patterns/behavior-engine.md) · [Integration Engine](../../patterns/integration-engine.md) · [Scenario Engine](../../patterns/scenario-engine.md)
- Positioning: [Taxonomy](../../foundations/taxonomy.md) · Quality bar: [DICE dossier](../../model-families/climate-iam/dice.md)
