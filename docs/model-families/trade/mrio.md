# MRIO — Multi-Regional Input-Output models (EXIOBASE, Eora, WIOD)

!!! info "Bronze dossier"
    MRIO databases are the standard tool for **consumption-based accounting** — tracing the emissions,
    land, water, and labour **embodied in trade** so a product's full footprint is attributed to its final
    consumer, not the country that produced it. They are how **carbon leakage** and the
    production-vs-consumption emissions gap are measured (EXIOBASE, [Eora](https://worldmrio.com), WIOD).
    Where a trade CGE like [GTAP](../economics/gtap.md) *optimizes* reallocation, an MRIO is an
    **accounting** engine: a giant Leontief inter-industry table linking every sector in every region.

> A global inter-region, inter-sector input-output table that traces resources embodied in trade,
> enabling consumption-based (footprint) accounting and carbon-leakage analysis.

## Positioning card

| Axis (see [Taxonomy](../../foundations/taxonomy.md)) | MRIO |
|------|------|
| Optimization vs Simulation | **Simulation** (linear accounting) |
| Top-down vs Bottom-up | **Top-down** (sectoral, economy-wide) |
| Equilibrium | Fixed-coefficient (Leontief), no price response |
| Foresight | N/A (static, historical) |
| Deterministic vs Stochastic | **Deterministic** |
| Time / Space | Annual / multi-region × multi-sector |
| Solution method | **Leontief inverse** (linear algebra on the IO table) |

| Field | Value |
|-------|-------|
| Full name | Multi-Regional Input-Output models / databases (EXIOBASE, Eora, WIOD) |
| Domain | Trade / Carbon Leakage |
| First release / current | 2010s / ongoing |
| Institution · lead | Eora (U. Sydney, Manfred Lenzen); EXIOBASE (EU consortium); WIOD (Groningen) |
| Language · solver | MATLAB / Python / R (sparse linear algebra) |
| License / access | Research / open (varies by database) |

---

## 🎓 Scholar Track

**History & motivation.** Built on Leontief's input-output economics, MRIO databases extend a single
country's IO table to a **global, multi-region** system so that the resources used *anywhere* in a supply
chain can be attributed to *final demand* — the basis of **consumption-based** (footprint) accounting.
Their signature policy use is **carbon leakage**: when a country prices carbon and its production
emissions fall, an MRIO reveals whether its **consumption** emissions fell too, or merely moved offshore
(the pollution-haven / [Copeland-Taylor](https://en.wikipedia.org/wiki/Pollution_haven_hypothesis) story).

**Mathematical formulation.** From the inter-industry requirements matrix $A$ and final demand $y$, total
output is $x = (I - A)^{-1} y$ — the **Leontief inverse** propagates demand through all supply-chain tiers.
Multiplying by a per-sector emission-intensity vector yields the emissions **embodied** in each unit of
final demand; summing over a region's imports gives its embodied-carbon (leakage) balance. It is exact
accounting under **fixed technical coefficients** — no prices, no substitution.

**Calibration & validation.** Assembled from national accounts, supply-use tables, bilateral trade, and
environmental satellite accounts; validated by **balance and reconciliation** (rows/columns must sum
consistently) rather than out-of-sample forecasting — an accounting identity, not a predictive model.

**Strengths / weaknesses / criticisms.** *Strengths:* the definitive footprint/leakage measure;
full supply-chain coverage; transparent linear structure. *Criticisms:* fixed coefficients (no price
response or substitution — the gap a CGE fills); heavy data assembly and sector aggregation; lags of a
few years; uncertainty in the satellite accounts.

## 🛠️ Engineer Track

**Architecture & engines.** A **[Market Engine](../../patterns/market-engine.md)** in the
inter-industry sense (Leontief demand propagation) sitting on a heavy
**[Data Pipeline](../../patterns/data-pipeline.md)** (reconciling trade, supply-use, and satellite
accounts into one balanced global table). Its signature is **embodied-flow accounting** — the cleanest
atlas example of tracing a quantity *through* the trade network.

**Data & complexity.** A large sparse linear system (thousands of region×sector cells); cheap to solve,
expensive to build and keep current.

**Openness / extensibility.** Eora and EXIOBASE are widely available to researchers; extensible to any
satellite account (water, land, materials, labour) — the same inverse, a new intensity vector.

## 🏛️ Architect Track

**Reusable patterns.** The transferable idea is **embodied-flow accounting via the Leontief inverse**:
attribute an impact to *final demand* by propagating it back through the whole supply chain. This is
exactly the Trade⇄Emissions coupling Polyphony's seventh loop tests — production vs consumption emissions,
with the gap = carbon leakage — and MRIO is the reference for measuring it.

**Trade-offs & alternatives.** MRIO (fixed-coefficient accounting) vs trade CGE ([GTAP](../economics/gtap.md),
price-responsive optimization): the MRIO tells you *where the embodied carbon is now*; the CGE tells you
*how it would move* under a policy. Complementary — accounting vs behavioural response.

**Adoption.** The backbone of consumption-based national emission inventories, carbon-leakage studies, and
border-carbon-adjustment analysis; used by statistical agencies and the IPCC.

**Ecosystem.** Eora (U. Sydney), EXIOBASE (EU), WIOD (Groningen); satellite-account communities; links to
trade CGEs on the behavioural side and to climate IAMs on the policy side.

**Research gaps.** Timeliness (reducing the multi-year lag); uncertainty quantification; hybridising the
fixed-coefficient accounting with price-responsive reallocation.

!!! quote "Lesson for the integrated simulator"
    MRIO teaches **consumption-based honesty**: a policy that cuts *production* emissions has not helped
    the climate if it merely exported them, and only tracing **embodied flows through trade** reveals the
    difference. Polyphony keeps this as its Trade⇄Emissions coupling — and holds even this well-motivated
    leakage channel to the same real-data + placebo bar (the gap it must explain is OWID's ``trade_co2``),
    because a plausible accounting story is still a hypothesis until it out-predicts a rival on real data.

## Major publications

- Lenzen, M., et al. (2013). "Building Eora: a global multi-region input-output database at high country
  and sector resolution." *Economic Systems Research* 25(1).
- Stadler, K., et al. (2018). "EXIOBASE 3." *Journal of Industrial Ecology* 22(3).
- Peters, G., et al. (2011). "Growth in emission transfers via international trade." *PNAS* 108(21).

## See also
- Contrast: [GTAP](../economics/gtap.md) · [Input-Output](../economics/input-output.md)
- Patterns: [Market Engine](../../patterns/market-engine.md) · [Data Pipeline](../../patterns/data-pipeline.md)
- Positioning: [Taxonomy](../../foundations/taxonomy.md) · Quality bar: [DICE dossier](../../model-families/climate-iam/dice.md)
