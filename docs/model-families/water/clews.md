# CLEWs — Climate, Land, Energy and Water strategies

!!! info "Bronze dossier"
    CLEWs is the canonical **integrated nexus** framework — the tool built specifically to model the
    **Climate–Land–Energy–Water** system *jointly* rather than one resource at a time. Where
    [WEAP](weap.md) centres water allocation and [OSeMOSYS](../energy/osemosys.md) centres the energy
    system, CLEWs **couples** an energy-system optimization, a land/agriculture balance, and a water
    balance under shared climate inputs, so that a drought, a biofuel mandate, or a cooling-water limit
    propagates across all three. It is the applied embodiment of the **nexus** thesis (Hoff 2011).

> An open, integrated modelling framework that links Climate, Land, Energy and Water systems to reveal
> the cross-sector trade-offs and synergies a single-sector model would miss.

## Positioning card

| Axis (see [Taxonomy](../../foundations/taxonomy.md)) | CLEWs |
|------|------|
| Optimization vs Simulation | **Optimization** (energy core) + accounting balances (land, water) |
| Top-down vs Bottom-up | **Bottom-up** (technology/resource explicit) |
| Equilibrium | Partial (least-cost energy) |
| Foresight | **Perfect-foresight** (energy LP) |
| Deterministic vs Stochastic | **Deterministic** (scenario-based) |
| Time / Space | Multi-year / national or regional |
| Solution method | **Linear programming** (OSeMOSYS engine) + coupled balances |

| Field | Value |
|-------|-------|
| Full name | CLEWs — Climate, Land, Energy and Water strategies |
| Domain | Water / cross-sector nexus |
| First release / current | ~2011 / ongoing (UN DESA, KTH, IAEA teaching tool) |
| Institution · lead | KTH (Mark Howells) with UN DESA / IAEA |
| Language · solver | GNU MathProg / Python (OSeMOSYS-based) / open LP solvers |
| License / access | Open source |

---

## 🎓 Scholar Track

**History & motivation.** CLEWs grew out of the **[OSeMOSYS](../energy/osemosys.md)** open energy-modelling
community at **KTH** (Mark Howells and colleagues) around the 2011 **Bonn Nexus Conference**, whose
premise — later formalized by Hoff (2011) — was that water, energy, and food security are so
interdependent that optimizing one in isolation can *worsen* another (biofuels that save carbon but
consume water; irrigation that lifts yields but strands energy). CLEWs was designed as an **open,
teachable** framework (adopted by UN DESA and the IAEA for capacity building) to make those trade-offs
explicit for national planning.

**Mathematical formulation.** At its core is the OSeMOSYS **linear program**: minimize discounted system
cost subject to demand-balance, capacity, and resource constraints. CLEWs **extends the constraint set
across sectors** — water availability limits thermoelectric cooling and irrigation; land availability
limits bioenergy and food crops; climate scenarios shift hydrology, yields, and demand. The coupling is
through **shared resource-balance constraints and exogenous climate drivers**, so a change in one sector
shows up as a shadow price in the others.

**Calibration & validation.** Scenario-driven rather than fit: populated with national energy balances,
land-use and water-availability data, and climate projections; validated by **scenario plausibility and
stakeholder review** rather than out-of-sample forecast skill — a limitation it shares with most
integrated-assessment tooling and one Polyphony's real-data + placebo discipline is meant to counter.

**Strengths / weaknesses / criticisms.** *Strengths:* explicit cross-sector trade-offs; open and
teachable; leverages a mature energy LP. *Criticisms:* the water and land balances are coarser than
dedicated models ([MODFLOW](modflow.md), [GLOBIOM](../agriculture/globiom.md)); perfect-foresight LP
inherits the usual optimization critiques; nexus results are **scenario contrasts**, not validated
predictions.

## 🛠️ Engineer Track

**Architecture & engines.** A least-cost **[Optimization Engine](../../patterns/optimization-engine.md)**
(the OSeMOSYS LP) wrapped in an **[Integration Engine](../../patterns/integration-engine.md)** that
couples land and water balances to it, driven by a **[Scenario Engine](../../patterns/scenario-engine.md)**
(climate/policy cases). Its signature is **cross-sector constraint coupling** — the cleanest atlas
example of a *nexus* architecture.

**Data & complexity.** A modest LP per scenario; the cost is data assembly across four sectors and
maintaining consistent units/boundaries between them.

**Openness / extensibility.** Fully open (OSeMOSYS lineage); extensible with finer sector models and new
constraints. Widely used as a **teaching** platform, which keeps the barrier to entry low.

## 🏛️ Architect Track

**Reusable patterns.** The transferable idea is **shared-constraint coupling**: represent each sector's
scarce resource as a constraint the others must respect, and the nexus trade-offs emerge as **shadow
prices** — no bespoke feedback code, just a shared feasibility region. This is exactly the
Water⇄Energy⇄Food coupling Polyphony's fifth loop probes, and CLEWs is the reference for doing it as an
integrated optimization.

**Trade-offs & alternatives.** CLEWs trades **per-sector fidelity** for **cross-sector coverage** — the
opposite choice from deep single-domain models ([MODFLOW](modflow.md) for groundwater, [OSeMOSYS](../energy/osemosys.md)
for energy). The two are complementary: deep models for a sector's mechanism, CLEWs for the trade-offs
*between* sectors. Peers: WEF-nexus tools generally, the Global CLEWs, integrated assessment models.

**Adoption.** UN DESA and IAEA capacity-building; national nexus assessments (e.g. Mauritius, Bolivia);
a staple of open energy-planning curricula.

**Ecosystem.** KTH / OSeMOSYS community; UN DESA; IAEA; links to WEAP (water) and land/agriculture data.

**Research gaps.** Finer hydrology and land representation; uncertainty quantification; and — the gap
Polyphony targets — **validating** nexus couplings against real data rather than presenting scenario
contrasts as if they were predictions.

!!! quote "Lesson for the integrated simulator"
    CLEWs teaches that a **nexus is a set of shared constraints**, not a pile of bolted-together models:
    the honest way to couple water, energy, and food is to let each sector's scarce resource constrain
    the others and read off the trade-offs as shadow prices. But it also teaches the atlas's central
    caution — an integrated model that is only ever run as **scenario contrasts** has never been told it
    could be *wrong*. Polyphony keeps CLEWs' coupling idea and adds the missing gate: the nexus synergy
    must beat a sum-of-parts baseline **and a placebo on real data**, or it is cut.

## Major publications

- Howells, M., et al. (2013). "Integrated analysis of climate change, land-use, energy and water
  strategies." *Nature Climate Change* 3.
- Hoff, H. (2011). "Understanding the Nexus." Background paper, Bonn2011 Nexus Conference (SEI).
- Welsch, M., et al. (2014). "Adding value with CLEWS — Modelling the energy system and its
  interdependencies for Mauritius." *Applied Energy* 113.

## See also
- Contrast: [WEAP](weap.md) · [MODFLOW](modflow.md) · [OSeMOSYS](../energy/osemosys.md)
- Patterns: [Optimization Engine](../../patterns/optimization-engine.md) · [Integration Engine](../../patterns/integration-engine.md) · [Scenario Engine](../../patterns/scenario-engine.md)
- Positioning: [Taxonomy](../../foundations/taxonomy.md) · Quality bar: [DICE dossier](../../model-families/climate-iam/dice.md)
