# ENVISAGE — Environmental Impact and Sustainability Applied General Equilibrium

!!! info "Bronze dossier"
    ENVISAGE is the **World Bank's** global recursive-dynamic energy-economy [CGE](cge.md) — a
    close sibling of [GEM-E3](gem-e3.md), built on the [GTAP](gtap.md) database, but oriented toward
    **development, trade, and distributional** questions alongside climate. Its distinguishing
    feature is an **integrated emissions-and-climate module**, making it a compact CGE-based IAM in
    its own right.

> The World Bank's global recursive-dynamic CGE for climate and trade analysis, with an integrated
> emissions-and-climate module.

## Positioning card

| Axis (see [Taxonomy](../../foundations/taxonomy.md)) | ENVISAGE |
|------|------|
| Optimization vs Simulation | Equilibrium root-finding (no objective) |
| Top-down vs Bottom-up | **Top-down** |
| Equilibrium | **General equilibrium** |
| Foresight | **Recursive-dynamic** (myopic) |
| Deterministic vs Stochastic | Deterministic |
| Time / Space | Annual / multi-region (global, GTAP-based) |
| Solution method | **MCP / NLP** (GAMS) |

| Field | Value |
|-------|-------|
| Full name | ENVISAGE — Environmental Impact and Sustainability Applied General Equilibrium |
| Domain | Economics — Equilibrium & Macro |
| First release / current | 2000s / ongoing (v10+) |
| Institution · lead | World Bank (Dominique van der Mensbrugghe) |
| Language · solver | GAMS |
| License / access | Open documentation (model code shared in courses) |

---

## 🎓 Scholar Track

**History & motivation.** ENVISAGE was built at the **World Bank** by **Dominique van der
Mensbrugghe** (its lineage runs through the Bank's LINKAGE model) to give development economists a
**global CGE** that could handle **trade, growth, poverty and climate** in one consistent frame. Its
motivating questions are as much about **who bears the cost** (regions, income groups) and **trade
adjustment** as about emissions — reflecting the Bank's development mandate.

**Mathematical formulation.** ENVISAGE is a **recursive-dynamic, multi-region, multi-sector CGE**
built on the **[GTAP](gtap.md) database**: utility-maximizing households (with optional multiple
income deciles for distribution), cost-minimizing firms under **nested-CES** production, Armington
bilateral trade, and market clearing solved as a **mixed complementarity problem (MCP)** each period.
Capital accumulates recursively; productivity and population grow exogenously. Its distinctive
component is a built-in **emissions accounting and climate module**: energy use generates CO₂ (and
other GHGs), which can be **priced** (carbon taxes, ETS), and a reduced-form climate relationship can
feed **temperature and damages** back to the economy — making ENVISAGE a **CGE-based integrated
assessment model**, not merely an economic CGE. It supports detailed **carbon-policy** experiments
(pricing, border adjustment, revenue recycling) and **distributional** analysis.

**Solution algorithm.** Per-period **MCP/NLP** solves in **GAMS**, chained recursively over the
horizon; damage/climate feedbacks and policy shocks are layered on the equilibrium each year.

**Calibration & validation.** Calibrated to the **GTAP** global SAM and energy data; validated
through World Bank policy studies, SSP-based projections, and model-comparison exercises.

**Strengths / weaknesses / criticisms.** *Strengths:* **global** coverage with **trade and
distributional** detail; **integrated climate module** (compact IAM); well-documented and taught.
*Criticisms:* recursive myopia; standard CGE equilibrium assumptions (the [E3ME](e3me.md) critique);
reduced-form climate is coarser than dedicated IAMs like [DICE](../climate-iam/dice.md)/[GCAM](../climate-iam/gcam.md).

## 🛠️ Engineer Track

**Architecture & engines.** A **[Market Engine](../../patterns/market-engine.md)** (nested-CES +
Armington + MCP) on the [GTAP](gtap.md) **[Data Pipeline](../../patterns/data-pipeline.md)**, fused
with a lightweight **[Climate Engine](../../patterns/climate-engine.md)** (emissions → concentration
→ temperature → damages) and a **[Policy Engine](../../patterns/policy-engine.md)** for carbon
pricing, border adjustment, and recycling. Implemented in **GAMS**; distributed with training
materials.

**Data & complexity.** Global multi-region/sector recursive CGE; aggregation-flexible over the GTAP
database. Per-period MCP solves are efficient; distributional detail multiplies household accounts.

**Openness / extensibility.** **Openly documented**, with model code circulated in World Bank/UNU-
WIDER CGE courses — unusually accessible for this class. Extensible via household disaggregation,
the climate module, and coupling to other GTAP-based tools.

## 🏛️ Architect Track

**Reusable patterns.** The transferable idea is a **CGE with an integrated climate feedback** — a
compact way to make an economy-wide model *self-contained* for climate policy (emissions and damages
inside the same equilibrium) — plus **distributional accounts** (income deciles) as a first-class
output, and reliance on a **shared standard database** (GTAP) for comparability.

**Trade-offs & alternatives.** ENVISAGE and [GEM-E3](gem-e3.md) are near-siblings (recursive-dynamic
GAMS energy-economy CGEs); ENVISAGE emphasizes **global development, trade and distribution** and
carries a tighter **climate loop**, GEM-E3 emphasizes **EU policy and power-sector technology**.
Against [GTAP](gtap.md) it adds **dynamics and a climate module**; against dedicated IAMs
([DICE](../climate-iam/dice.md), [GCAM](../climate-iam/gcam.md)) it offers **full economy-wide and
distributional detail** but a **coarser climate** representation — a different point on the
[IAM vs Energy-System](../../comparative/iam-vs-energy.md) and top-down/bottom-up trade-offs.

**Adoption.** World Bank climate, trade, and development analysis; **carbon pricing and border-
adjustment** studies; widely used in **CGE training** (its openness makes it a teaching standard).

**Ecosystem.** World Bank LINKAGE lineage; GTAP database; peers GEM-E3, MIRAGE, GTAP-E, AIM/CGE;
teaching via UNU-WIDER / GTAP courses.

**Research gaps.** Foresight; richer climate/damages; deeper within-country distribution; endogenous
technology.

!!! quote "Lesson for the integrated simulator"
    ENVISAGE makes two points for the integrated simulator. First, a general-equilibrium economy can
    carry a **compact climate feedback inside itself** — emissions, pricing and damages in the same
    equilibrium — which is a lightweight alternative to bolting on a full IAM when the economic
    response is what matters; the simulator should let the **climate loop's fidelity be a dial**,
    from reduced-form (ENVISAGE) to process-based (GCAM/IMAGE). Second, ENVISAGE elevates
    **distributional accounts** — who wins and loses across regions and income groups — to a
    first-class output, a reminder that a world-class policy simulator must answer *distributional*
    questions, not just aggregate efficiency. Its reliance on the shared **GTAP** database again
    underlines the atlas's theme that **comparability comes from a common data substrate**.

## Major publications

- van der Mensbrugghe, D. (2019). "The Environmental Impact and Sustainability Applied General
  Equilibrium (ENVISAGE) Model, Version 10.01." Center for Global Trade Analysis, Purdue University.
- van der Mensbrugghe, D. (2008). "The Environmental Impact and Sustainability Applied General
  Equilibrium (ENVISAGE) Model." World Bank.
- World Bank (2010). *World Development Report 2010: Development and Climate Change* (ENVISAGE-based
  analysis).

## See also
- Sibling: [GEM-E3](gem-e3.md) · Builds on: [GTAP](gtap.md) · [CGE](cge.md) · Contrast: [E3ME](e3me.md) · [DICE](../climate-iam/dice.md) · [IAM vs Energy](../../comparative/iam-vs-energy.md)
- Patterns: [Market Engine](../../patterns/market-engine.md) · [Climate Engine](../../patterns/climate-engine.md) · [Policy Engine](../../patterns/policy-engine.md) · [Data Pipeline](../../patterns/data-pipeline.md)
- Positioning: [Taxonomy](../../foundations/taxonomy.md) · Quality bar: [DICE dossier](../../model-families/climate-iam/dice.md)
