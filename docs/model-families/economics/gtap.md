# GTAP — Global Trade Analysis Project

!!! info "Bronze dossier"
    GTAP is the **global standardization** of the [CGE](cge.md) idea: one harmonized, community-
    maintained **world Social Accounting Matrix** plus a **standard multi-region CGE**, so that
    trade and global-policy questions are answered on a *shared, comparable* data foundation. It is
    the de-facto reference for quantifying **trade agreements, tariffs, and border measures**, and
    its database feeds much of the IAM/energy-economy world too.

> A global, multi-region CGE built on a harmonized world Social Accounting Matrix; the de-facto
> standard for quantifying trade-agreement and global-policy impacts.

## Positioning card

| Axis (see [Taxonomy](../../foundations/taxonomy.md)) | GTAP |
|------|------|
| Optimization vs Simulation | Equilibrium **root-finding** (no objective) |
| Top-down vs Bottom-up | **Top-down** |
| Equilibrium | **General equilibrium** (multi-region) |
| Foresight | Comparative-static (recursive-dynamic variants) |
| Deterministic vs Stochastic | Deterministic (+ systematic sensitivity) |
| Time / Space | Comparative-static / 100+ regions & sectors |
| Solution method | **Johansen/Euler linearization** (GEMPACK) |

| Field | Value |
|-------|-------|
| Full name | GTAP — Global Trade Analysis Project |
| Domain | Economics — Equilibrium & Macro |
| First release / current | 1990s / GTAP 11 database |
| Institution · lead | Purdue University (GTAP consortium; Thomas Hertel) |
| Language · solver | GEMPACK (RunGTAP); GAMS ports |
| License / access | Database licensed; software commercial/academic |

---

## 🎓 Scholar Track

**History & motivation.** GTAP was founded at **Purdue University** by **Thomas Hertel** in the
early 1990s to solve a coordination problem: everyone building global trade CGEs was assembling
incompatible datasets, so results could not be compared. GTAP's answer was a **public good** — a
**harmonized global database** (bilateral trade, protection, energy, input–output tables for 100+
regions and 65+ sectors), a **standard model**, and a **community** that maintains and documents
both. It became the lingua franca of quantitative trade policy (WTO rounds, RTAs, Brexit, carbon
border adjustments).

**Mathematical formulation.** The **standard GTAP model** is a comparative-static, multi-region
CGE: in each region, a **regional household** allocates income across private consumption
(constant-difference-of-elasticities demand), government, and saving; firms combine primary factors
and intermediates under **nested-CES** technology; and goods are differentiated by origin via the
**Armington assumption** (imports from different countries are imperfect substitutes) — the device
that lets the model carry **bilateral trade** and hence tariff analysis. Global equilibrium requires
that all goods and factor markets clear, that bilateral trade is consistent, and that two **global
institutions** balance: a global bank equating savings and investment, and a global transport sector
for trade margins. The model is written and solved in **percentage-change (linearized) form** —
GTAP's distinctive methodological choice.

**Solution algorithm.** GTAP is solved in **GEMPACK** using **Johansen/Euler** methods: the
nonlinear equilibrium is represented as a system of **linearized (percentage-change) equations** and
solved by multi-step Euler integration with **Richardson extrapolation** to control linearization
error. (GAMS/MPSGE ports solve the levels form as an [MCP](cge.md) instead.) **Systematic
Sensitivity Analysis (SSA)** — sampling key elasticities — gives result distributions.

**Calibration & validation.** Calibrated by construction to the **GTAP database** (a balanced global
SAM assembled from national IO tables, UN COMTRADE trade, and protection data, released in versioned
"data bases" up to GTAP 11); elasticities from econometric estimates. Validation is via replication
of historical episodes and model-comparison exercises (EMF, the Energy Modeling Forum trade studies).

**Strengths / weaknesses / criticisms.** *Strengths:* the **global standard** — comparable,
documented, community-maintained; unrivalled **bilateral trade and protection** detail; huge trained
user base. *Criticisms:* comparative-static core (the standard model has no time/foresight); the
**Armington** structure mechanically ties trade responses to fixed elasticities; like all CGE it
assumes full employment and optimizing clearing — the [E3ME](e3me.md) critique; linearization error
must be managed.

## 🛠️ Engineer Track

**Architecture & engines.** A multi-region **[Market Engine](../../patterns/market-engine.md)**
(nested-CES + Armington + global closure) whose defining engineering asset is its
**[Data Pipeline](../../patterns/data-pipeline.md)**: the assembly and **balancing** of a global SAM
from dozens of national sources is the real product. A **[Sensitivity Engine](../../patterns/sensitivity-engine.md)**
(SSA over elasticities) is built in. RunGTAP wraps it in an accessible GUI.

**Data & complexity.** 100+ regions × 65+ sectors makes a large but linearizable system; GEMPACK's
percentage-change solver handles it efficiently. Users **aggregate** the database to a tractable
region/sector split (FlexAgg) before solving.

**Openness / extensibility.** The **model and documentation are open**; the **database is licensed**
(revenue funds the consortium). Highly extensible via a family of variants (below) and GAMS/MPSGE
re-implementations; the **GTAP-in-GAMS** and open-source Python efforts widen access.

## 🏛️ Architect Track

**Reusable patterns.** GTAP's biggest lesson is **institutional/architectural, not mathematical**:
a **shared, versioned, balanced global database as community infrastructure** makes results
*comparable* across teams — the coordination win the atlas keeps advocating. Technically reusable:
the **Armington nested-demand** structure for bilateral trade, **percentage-change (Johansen)
solution** as an alternative to levels/MCP, and **systematic sensitivity** as a default.

**Trade-offs & alternatives.** GTAP **globalizes** the single-economy [CGE](cge.md) (it
`succeeds` CGE as the multi-region standard) and shares its equilibrium closure; against
[E3ME](e3me.md) it is the **optimizing-equilibrium** pole versus demand-led disequilibrium; against
[DSGE](dsge.md) it trades intertemporal optimization and stochastics for **rich sectoral/regional
trade detail**. Its Armington-and-elasticities core is exactly what the
[ABM vs CGE](../../comparative/abm-vs-cge.md) and
[Equilibrium vs Disequilibrium](../../comparative/equilibrium-vs-disequilibrium.md) chapters
interrogate.

**Adoption.** The **standard** for trade-policy quantification — WTO/OECD/World Bank studies, RTA
and Brexit analyses, **carbon border adjustment (CBAM)**; GTAP-E/GTAP-Power extensions feed climate
and energy work; its database underpins many IAMs.

**Ecosystem.** GTAP-E (energy-environment), GTAP-Power, GTAP-AGR, GTAP-W (water), GDyn (recursive-
dynamic), MRIO version; GEMPACK/RunGTAP; peers: MIRAGE, ENVISAGE, GEM-E3, MRIO models.

**Research gaps.** Dynamics/foresight in the standard model; moving beyond Armington;
reconciling with MRIO databases; opening the database further.

!!! quote "Lesson for the integrated simulator"
    GTAP's deepest lesson is about **shared infrastructure as a design decision**. Its lasting
    influence comes less from any equation than from a **harmonized, versioned, community-balanced
    global database** that makes every team's results *comparable* — precisely the interoperability
    the integrated simulator needs if it is to run many paradigms on one world. So the simulator
    should treat its **global accounting substrate** (a balanced multi-region SAM/MRIO, versioned and
    documented) as core infrastructure, not a per-study afterthought, and should adopt GTAP's habits
    of **built-in systematic sensitivity** and **aggregation flexibility** (solve at the resolution
    the question needs). GTAP shows that in policy modeling, the **database can be the most valuable
    part of the model**.

## Major publications

- Hertel, T. W. (ed.) (1997). *Global Trade Analysis: Modeling and Applications.* Cambridge
  University Press.
- Corong, E., Hertel, T., et al. (2017). "The Standard GTAP Model, Version 7." *Journal of Global
  Economic Analysis* 2(1).
- Aguiar, A., Chepeliev, M., et al. (2019/2022). "The GTAP Data Base: Version 10/11." *Journal of
  Global Economic Analysis*.

## See also
- Generalizes: [CGE](cge.md) · Contrast: [E3ME](e3me.md) · [DSGE](dsge.md) · [Input–Output](input-output.md) · [Equilibrium vs Disequilibrium](../../comparative/equilibrium-vs-disequilibrium.md)
- Patterns: [Market Engine](../../patterns/market-engine.md) · [Data Pipeline](../../patterns/data-pipeline.md) · [Sensitivity Engine](../../patterns/sensitivity-engine.md)
- Positioning: [Taxonomy](../../foundations/taxonomy.md) · Quality bar: [DICE dossier](../../model-families/climate-iam/dice.md)
