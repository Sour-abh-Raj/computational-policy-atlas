# AIM — Asia-Pacific Integrated Model

!!! info "Bronze dossier"
    AIM is a **model family**, not a single model: a **recursive-dynamic CGE core**
    (**AIM/CGE**) coupled to **bottom-up end-use technology detail** (**AIM/Enduse**) and a
    downscaling/backend layer (**AIM/Hub**). Built at **NIES (Japan)** with an explicit
    **Asia-Pacific** focus, it is the region's marker IAM in the SSP framework and a bridge
    between the top-down CGE tradition ([CGE](../economics/cge.md)) and the bottom-up
    technology tradition ([TIMES](../energy/times.md)).

> A model family (AIM/CGE, AIM/Enduse, AIM/Hub) coupling a recursive-dynamic CGE core with
> bottom-up end-use technology detail, developed for Asian and global mitigation and SSP
> analysis.

## Positioning card

| Axis (see [Taxonomy](../../foundations/taxonomy.md)) | AIM |
|------|------|
| Optimization vs Simulation | **Hybrid** — CGE market-clearing + bottom-up enduse optimization |
| Top-down vs Bottom-up | **Hybrid** |
| Equilibrium | General equilibrium (recursive) |
| Foresight | **Recursive-dynamic** (myopic) |
| Deterministic vs Stochastic | Deterministic (+ scenarios) |
| Time / Space | 1- to 5-yr / multi-region (global 17+; detailed Asia) |
| Solution method | MCP/NLP (CGE) + LP (Enduse), soft-linked |

| Field | Value |
|-------|-------|
| Full name | AIM — Asia-Pacific Integrated Model |
| Domain | Climate — Integrated Assessment |
| First release / current | 1990s / ongoing (AIM/CGE, /Enduse, /Hub) |
| Institution · lead | National Institute for Environmental Studies (NIES), Japan; Kyoto University (with IGES) |
| Language · solver | GAMS (CGE, PATH/CONOPT); AIM/Enduse (LP); various |
| License / access | Restricted / research access (some tools & data released) |

---

## 🎓 Scholar Track

**History & motivation.** AIM was launched at **NIES (Tsukuba, Japan)** in the early 1990s
(Matsuoka, Kainuma, Masui and colleagues) with a distinctive mandate: to represent **Asia** —
fast-growing, technology-heterogeneous, and central to future emissions — in a way the
Western-built IAMs did not. Rather than one monolithic model it grew into a **toolbox**: a
**computable general equilibrium** core for the whole economy, a **bottom-up end-use** model for
technology-rich sectors, and downscaling tools to move between global and national/city scales.

**Mathematical formulation.** **AIM/CGE** is a **recursive-dynamic** multi-region, multi-sector
CGE: households maximize utility, firms minimize cost under **nested-CES** technologies, and a set
of prices clears all goods and factor markets each period — formulated as a **mixed
complementarity problem (MCP)** (or NLP) exactly in the [CGE](../economics/cge.md) tradition, with
capital accumulating between periods and **no intertemporal optimization** (myopic recursion — see
[Recursive vs Perfect Foresight](../../comparative/recursive-vs-perfect-foresight.md)). Land, energy
and emissions are tracked with detail sufficient for mitigation analysis. **AIM/Enduse** is a
**bottom-up cost-minimization** (typically an **LP**) over an explicit menu of end-use technologies
in industry, buildings and transport — the same least-cost logic as an
[energy-system model](../energy/times.md) — producing marginal abatement cost curves and technology
diffusion paths. The two are **soft-linked**: Enduse informs the CGE's sectoral technology and
abatement possibilities, while the CGE supplies activity levels and prices to Enduse.

**Solution algorithm.** Per period, solve the **CGE MCP/NLP** to clear markets; solve **AIM/Enduse
LP(s)** for least-cost technology portfolios; exchange information between them; **step forward**
(update capital, population, productivity) and repeat recursively to 2100. No global objective is
optimized across time.

**Calibration & validation.** Calibrated to a base-year **Social Accounting Matrix** (GTAP-based
for the global CGE), national energy balances (IEA), and bottom-up technology databases; validated
via IAM inter-comparisons (EMF, AMPERE, the Asian Modeling Exercise, LIMITS) and the **SSP
database** (NIES leads the **SSP3** marker narrative).

**Strengths / weaknesses / criticisms.** *Strengths:* genuine **hybrid** coverage — economy-wide
CGE consistency plus real technology detail; strong **Asian/national** resolution; a flexible
family that scales from global to city studies. *Criticisms:* recursive myopia (no anticipation);
soft-linking two paradigms risks internal inconsistency at the seam; parts of the code and data are
**restricted**, limiting external replication.

## 🛠️ Engineer Track

**Architecture & engines.** A **[Market Engine](../../patterns/market-engine.md)** (AIM/CGE, the
MCP/CGE core) soft-linked to an **[Energy Dispatch](../../patterns/energy-dispatch-engine.md) /
[Technology-Adoption Engine](../../patterns/technology-adoption-engine.md)** (AIM/Enduse LP), with a
**[Data Pipeline](../../patterns/data-pipeline.md)** / downscaling layer (**AIM/Hub**) moving
quantities between global, national and sub-national scales. The family is the
[top-down ↔ bottom-up](../../comparative/top-down-vs-bottom-up.md) bridge made concrete.

**Data & complexity.** Global CGE on **GTAP** sectors/regions (17+), with much finer detail for
Asian economies; AIM/Enduse carries thousands of technology entries per country. Each period is a
CGE solve plus LP solves; recursion to 2100 keeps it tractable relative to perfect-foresight NLP
IAMs.

**Openness / extensibility.** Core code is **research-access**, but NIES/IGES have released
**AIM/Enduse** teaching versions, emission datasets, and downscaling tools; the family is explicitly
**modular** — country teams across Asia build national AIM models that plug into the framework.

## 🏛️ Architect Track

**Reusable patterns.** The signature is **soft-linked hybridization**: keep a **top-down CGE** for
economy-wide consistency and a **bottom-up LP** for technology realism, and pass information between
them rather than forcing one formalism. Also reusable: **multi-scale downscaling** (global →
national → city) as an explicit architectural layer, and a **family-of-models** strategy where a
shared framework hosts many national instances.

**Trade-offs & alternatives.** AIM sits with the **recursive, process/CGE** IAMs
[GCAM](gcam.md) and [IMAGE](image.md) (myopic, simulate market clearing) rather than the
perfect-foresight optimizers [REMIND](remind.md)/[MESSAGEix](messageix.md)/[WITCH](witch.md). Its
distinctive choice versus GCAM (nested-logit partial equilibrium) is a **full CGE** economy-wide
core; versus IMAGE (biophysical process modules) it is **economy-first**. The soft-link design is
the pragmatic middle of the [top-down vs bottom-up](../../comparative/top-down-vs-bottom-up.md)
debate.

**Adoption.** The **Asia-Pacific** marker IAM; **SSP3** narrative lead (NIES); heavily used for
Japanese and Asian national mitigation strategy, NDC analysis, and IPCC assessments.

**Ecosystem.** NIES / Kyoto University / IGES; AIM/CGE, AIM/Enduse, AIM/Hub, plus national AIM
models across Asia; peers GCAM, IMAGE, REMIND, MESSAGEix, WITCH.

**Research gaps.** Tightening the CGE–Enduse link toward hard-linking; adding foresight where
lock-in matters; opening more of the code base; sub-national heterogeneity.

!!! quote "Lesson for the integrated simulator"
    AIM demonstrates the **soft-linked hybrid** and the **family-of-models** strategy at once. Its
    two cores — an economy-wide CGE and a technology-rich bottom-up LP — answer questions neither
    could alone, and it passes information across the seam instead of collapsing them into one
    formalism ([REMIND](remind.md) shows the *hard-linked* alternative; AIM shows the *soft-linked*
    one, and the integrated simulator will want **both coupling strengths available as a choice**).
    Just as important is AIM's **multi-scale** design: an explicit downscaling layer that lets the
    same framework speak at global, national and city resolution, and lets local teams build
    plug-in national models. For a would-be world simulator, that is the template for **coupling
    and for federation** — many domain models, many scales, one interoperable substrate — which is
    the atlas's central architectural bet.

## Major publications

- Fujimori, S., Masui, T., Matsuoka, Y. (2012, 2017). "AIM/CGE model" — NIES technical reports and
  *AIM/CGE V2.0* documentation.
- Kainuma, M., Matsuoka, Y., Morita, T. (eds.) (2003). *Climate Policy Assessment: Asia-Pacific
  Integrated Modeling.* Springer.
- Fujimori, S., et al. (2017). "SSP3: AIM implementation of Shared Socioeconomic Pathways."
  *Global Environmental Change* 42.

## See also
- Contrast: [GCAM](gcam.md) · [IMAGE](image.md) · [CGE](../economics/cge.md) · [TIMES](../energy/times.md) · [Top-Down vs Bottom-Up](../../comparative/top-down-vs-bottom-up.md)
- Patterns: [Market Engine](../../patterns/market-engine.md) · [Technology-Adoption Engine](../../patterns/technology-adoption-engine.md) · [Data Pipeline](../../patterns/data-pipeline.md)
- Positioning: [Taxonomy](../../foundations/taxonomy.md) · Quality bar: [DICE dossier](dice.md)
