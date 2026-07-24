# GEM-E3 — General Equilibrium Model for Energy–Economy–Environment

!!! info "Bronze dossier"
    GEM-E3 is the **EU's workhorse energy-economy CGE** — a recursive-dynamic multi-region
    [CGE](cge.md) with enough **energy-technology and emissions detail** to serve as an official
    impact-assessment tool for European climate and energy packages. It sits between the pure
    top-down [GTAP](gtap.md) and the bottom-up energy models, hybridizing a general-equilibrium
    core with explicit power-generation technologies.

> A detailed Energy-Economy-Environment recursive-dynamic CGE linking macroeconomy, energy
> technologies and emissions, used extensively for EU policy assessment.

## Positioning card

| Axis (see [Taxonomy](../../foundations/taxonomy.md)) | GEM-E3 |
|------|------|
| Optimization vs Simulation | Equilibrium root-finding (no objective) |
| Top-down vs Bottom-up | **Top-down** (+ bottom-up power-generation tech) |
| Equilibrium | **General equilibrium** |
| Foresight | **Recursive-dynamic** (myopic) |
| Deterministic vs Stochastic | Deterministic |
| Time / Space | Annual / multi-region (EU + world) |
| Solution method | **MCP / NLP** (GAMS) |

| Field | Value |
|-------|-------|
| Full name | GEM-E3 — General Equilibrium Model for Energy–Economy–Environment |
| Domain | Economics — Equilibrium & Macro |
| First release / current | 1990s / ongoing (GEM-E3-FIT, GEM-E3-JRC) |
| Institution · lead | E3MLab / NTUA Athens; EU JRC variant |
| Language · solver | GAMS (PATH/CONOPT) |
| License / access | Restricted / EU research |

---

## 🎓 Scholar Track

**History & motivation.** GEM-E3 was developed from the 1990s by a European consortium led by
**E3MLab (NTUA Athens)** with EU funding, specifically to give the **European Commission** a
consistent, economy-wide tool for assessing energy and climate policy where **macroeconomic
feedbacks, sectoral structure, and energy technology** all matter at once. It is the CGE counterpart
to the same lab's bottom-up **PRIMES** energy model, and both underpin EU "Fit-for-55"–type impact
assessments.

**Mathematical formulation.** GEM-E3 is a **recursive-dynamic, multi-region, multi-sector CGE**:
households maximize utility (nested demand systems), firms minimize cost with **nested-CES**
production combining capital, labor, energy and materials (the "KLEM" structure), and prices clear
all product and factor markets each period. It is formulated as a **mixed complementarity problem
(MCP)** in the [CGE](cge.md) tradition, closed by savings-investment and government budget balances,
with **bilateral trade** via Armington. Its distinguishing detail is a **bottom-up power-generation
module**: electricity is produced by an explicit portfolio of technologies (coal, gas, nuclear,
renewables, CCS) so that the general-equilibrium economy sees a technology-resolved power sector —
a **hybrid** top-down/bottom-up design. Emissions of CO₂ and other GHGs/air pollutants are tracked,
and policy instruments (carbon taxes, ETS permit markets, standards, revenue recycling) are
first-class. **Foresight is recursive** — capital accumulates between periods but agents do not
optimize intertemporally.

**Solution algorithm.** Each period is solved as a **square MCP/NLP** in **GAMS** (PATH/CONOPT);
periods are chained recursively (this year's outcome updates next year's capital and technology
stocks). Optional semi-endogenous learning updates technology costs.

**Calibration & validation.** Calibrated to a base-year **Social Accounting Matrix** (GTAP-derived
for the global version, Eurostat/EU accounts for the European version), energy balances, and
technology-cost data; validated through EU impact-assessment use and model-comparison exercises.

**Strengths / weaknesses / criticisms.** *Strengths:* economy-wide **macro + sectoral + energy-
technology** consistency in one equilibrium; strong **EU policy** pedigree; explicit air-pollution
co-benefits. *Criticisms:* recursive myopia (no anticipation of future policy); CGE closure assumes
optimizing full-employment clearing (the [E3ME](e3me.md) critique); **restricted access** limits
external replication.

## 🛠️ Engineer Track

**Architecture & engines.** A **[Market Engine](../../patterns/market-engine.md)** (KLEM nested-CES
+ Armington + MCP closure) hybridized with an **[Energy Dispatch](../../patterns/energy-dispatch-engine.md) /
[Technology-Adoption Engine](../../patterns/technology-adoption-engine.md)** in the power sector, and
a **[Data Pipeline](../../patterns/data-pipeline.md)** building the SAM and technology database. A
**[Policy Engine](../../patterns/policy-engine.md)** exposes taxes, permits, standards and recycling
rules. Implemented in **GAMS**.

**Data & complexity.** Multi-region × multi-sector recursive CGE with an embedded technology module;
tractable per-period MCP solves chained over decades. Aggregation flexibility (region/sector) trades
detail for speed.

**Openness / extensibility.** **Restricted** (E3MLab / JRC), though the **GEM-E3-JRC** version has
public documentation and controlled release. Extensible via variants (GEM-E3-FIT for
technology/finance detail, GEM-E3-Power) and coupling to PRIMES.

## 🏛️ Architect Track

**Reusable patterns.** The transferable idea is the **hybrid CGE**: keep a full general-equilibrium
economy but **embed a bottom-up technology module** in the sector where technology detail is
decision-relevant (power), so macro and technology are mutually consistent — a softer-linked cousin
of [REMIND](../climate-iam/remind.md)'s hard-linked hybrid. Also reusable: **rich policy-instrument
representation** with revenue recycling, and **air-pollution co-benefit** accounting.

**Trade-offs & alternatives.** GEM-E3 and [ENVISAGE](envisage.md) are near-siblings — recursive-
dynamic energy-economy CGEs in GAMS — differing mainly in **institutional home and emphasis**
(GEM-E3: EU policy, power-tech + air pollution; ENVISAGE: World Bank, global development & climate).
Against [GTAP](gtap.md) it adds **dynamics, energy technology and emissions**; against
[E3ME](e3me.md) it is the **optimizing-equilibrium** alternative to demand-led econometrics; against
bottom-up energy models it embeds only a stylized technology module inside a full economy.

**Adoption.** A core **European Commission** impact-assessment model (climate/energy packages,
carbon pricing, ETS); used across EU-funded projects; the CGE partner to PRIMES.

**Ecosystem.** E3MLab/NTUA (GEM-E3, PRIMES), EU JRC (GEM-E3-JRC); peers ENVISAGE, GTAP-E, MIRAGE,
AIM/CGE.

**Research gaps.** Foresight; opening access; deeper technology detail without losing tractability;
reconciling equilibrium closure with observed labour-market slack.

!!! quote "Lesson for the integrated simulator"
    GEM-E3 shows the **embedded-technology hybrid CGE** in its practical, policy-serving form: a full
    general-equilibrium economy with a **bottom-up technology module dropped into the one sector
    (power) where technology choice drives the answer**, plus a rich menu of policy instruments and
    revenue-recycling rules. For the integrated simulator the lesson is **selective resolution** —
    resolve technology in detail *only where it changes the policy conclusion*, and keep the rest of
    the economy at CGE aggregation for consistency and speed — and the value of a **first-class
    policy-instrument layer** (taxes, permit markets, standards, recycling) shared across engines.
    Its EU-impact-assessment role also reinforces that credible policy tools pair a **top-down
    economy** with a **bottom-up technology** view of the sector under scrutiny.

## Major publications

- Capros, P., et al. (2013). "GEM-E3 Model Documentation." JRC Technical Reports, European
  Commission.
- E3MLab (2017). *GEM-E3 Manual: General Equilibrium Model for Economy–Energy–Environment.* NTUA.
- Fragkos, P., et al. (2017). "Energy system impacts and policy implications of the EU INDC"
  (GEM-E3 / PRIMES application). *Energy Policy* 112.

## See also
- Sibling: [ENVISAGE](envisage.md) · Builds on: [CGE](cge.md) · [GTAP](gtap.md) · Contrast: [E3ME](e3me.md) · Hybrid cousin: [REMIND](../climate-iam/remind.md)
- Patterns: [Market Engine](../../patterns/market-engine.md) · [Technology-Adoption Engine](../../patterns/technology-adoption-engine.md) · [Policy Engine](../../patterns/policy-engine.md)
- Positioning: [Taxonomy](../../foundations/taxonomy.md) · Quality bar: [DICE dossier](../../model-families/climate-iam/dice.md)
