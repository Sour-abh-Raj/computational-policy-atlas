# Input–Output (Leontief) Models

!!! info "Bronze dossier"
    Input–Output analysis is the **structural ancestor** of every economy-wide policy model in
    this atlas. Before [CGE](cge.md) added prices and substitution, Leontief showed that an
    economy's inter-industry flows form a **linear operator** whose inverse propagates any final-
    demand shock through the whole production web. It is the simplest possible
    **[Market Engine](../../patterns/market-engine.md)** — fixed coefficients, no optimization —
    and the SAM it generalizes is the calibration substrate of CGE.

> The oldest structural policy tool: a linear map of how each sector's output feeds every other,
> letting a demand change ripple through the whole economy via the Leontief inverse.

## Positioning card

| Axis (see [Taxonomy](../../foundations/taxonomy.md)) | Input–Output (Leontief) |
|------|------|
| Optimization vs Simulation | **Simulation** (linear propagation) |
| Top-down vs Bottom-up | Structural (sectoral) |
| Equilibrium | **Fixed-coefficient** (no substitution) |
| Foresight | Static (dynamic extensions) |
| Deterministic vs Stochastic | Deterministic |
| Time / Space | Static or annual / regional MRIO |
| Solution method | **Linear algebra** (Leontief inverse) |

| Field | Value |
|-------|-------|
| Full name | Input–Output (Leontief) Models |
| Domain | Economics — Equilibrium & Macro |
| First release / current | 1940s / ongoing (SUTs, MRIO) |
| Institution · lead | Wassily Leontief (Harvard; Nobel 1973) |
| Language · solver | Any (linear algebra); R, Python, GEMPACK |
| License / access | Data/method open (national SUTs; WIOD/EXIOBASE/Eora MRIO) |

---

## 🎓 Scholar Track

**History & motivation.** **Wassily Leontief** built the first input–output tables of the US
economy in the 1930s–40s (Nobel 1973), turning the abstract idea of general interdependence into a
**measured, computable** object: a matrix of who-buys-what-from-whom. The motivation was intensely
practical — wartime planning, structural analysis, and later environmental and energy accounting —
and its legacy is foundational: the **Social Accounting Matrix (SAM)** that calibrates every
[CGE](cge.md) is a price-augmented descendant of Leontief's table.

**Mathematical formulation.** Let $\mathbf{x}$ be the vector of sectoral gross outputs,
$\mathbf{f}$ final demand, and $\mathbf{A}$ the **technical-coefficient matrix** where
$a_{ij}$ = input from sector $i$ needed per unit of sector $j$'s output. The accounting identity
"output = intermediate use + final demand" is

$$\mathbf{x} = \mathbf{A}\mathbf{x} + \mathbf{f} \;\;\Longrightarrow\;\;
\mathbf{x} = (\mathbf{I}-\mathbf{A})^{-1}\mathbf{f},$$

where $(\mathbf{I}-\mathbf{A})^{-1}$ is the **Leontief inverse** — its column $j$ gives the *total*
(direct + indirect) output of every sector required to deliver one unit of final demand for $j$.
The key modeling assumptions are **fixed coefficients** (no input substitution) and **constant
returns / no price response** — which make it linear and exactly solvable, but also its central
limitation. Extensions: **environmentally-extended IO** (append emission/energy intensity vectors
to get carbon/water footprints), **multi-regional IO (MRIO)** for trade-embodied flows,
**supply-and-use tables**, and **dynamic IO** (Leontief's own investment-driven extension).

**Solution algorithm.** A single **linear solve** (matrix inversion or, for large MRIO,
iterative/sparse methods) — no iteration, no optimization. This exactness and speed is precisely
why IO remains ubiquitous for footprint and multiplier analysis.

**Calibration & validation.** Coefficients come directly from **national statistical accounts**
(supply-use tables); global versions from **WIOD, EXIOBASE, Eora, GTAP-MRIO**. "Validation" is
mostly accounting consistency (row/column balance) rather than behavioral fit.

**Strengths / weaknesses / criticisms.** *Strengths:* **transparent, exact, data-grounded**;
unmatched for **multipliers** and **embodied/footprint** accounting; the shared substrate for CGE.
*Criticisms:* **fixed coefficients** mean no substitution, no prices, no supply constraints — it
answers "what flows are implied by this demand?" not "how would the economy re-optimize?"; strictly
it assumes infinitely elastic supply.

## 🛠️ Engineer Track

**Architecture & engines.** The minimal **[Market Engine](../../patterns/market-engine.md)**: a
linear operator instead of a price-clearing solve. In practice it is mostly a
**[Data Pipeline](../../patterns/data-pipeline.md)** — building and balancing supply-use/MRIO
tables (RAS balancing, concordances) dominates the work; the "model" itself is one matrix inverse.
Environmentally-extended IO bolts a **satellite-account** layer (emissions per unit output) onto
the same algebra.

**Data & complexity.** A national table is tiny (tens–hundreds of sectors); global MRIO (EXIOBASE:
~200 sectors × 44+ regions) is large and sparse, handled with sparse linear algebra. Trivial
runtime relative to any optimizing model.

**Openness / extensibility.** Method fully open; implementable in a few lines of NumPy/R. Databases
range from open (Eora, EXIOBASE tiers) to licensed (WIOD updates, GTAP-MRIO). The **`pymrio`**
library is a common open toolchain.

## 🏛️ Architect Track

**Reusable patterns.** Two transferable ideas: the **Leontief inverse** as a reusable *impact-
propagation operator* (any linear network — supply chains, ecosystems — can be analyzed this way),
and the **SAM/supply-use table as the shared calibration substrate** that higher models (CGE) build
on. Also the **satellite-account** pattern: attach intensity vectors to an economic core to get
footprints.

**Trade-offs & alternatives.** IO is the **linear, price-free** floor of the economics family:
[CGE](cge.md) adds prices, substitution (CES), and market clearing on top of the same SAM;
[E3ME](e3me.md) adds econometric behavior and disequilibrium; [DSGE](dsge.md) adds optimizing
forward-looking agents. Choosing IO means choosing **transparency and exact accounting** over
behavioral realism — the far "no-substitution" end of the
[Equilibrium vs Disequilibrium](../../comparative/equilibrium-vs-disequilibrium.md) and
[Optimization vs Simulation](../../comparative/optimization-vs-simulation.md) discussions.

**Adoption.** Ubiquitous: national statistical offices, the **carbon-footprint / embodied-emissions**
literature (consumption-based accounting), life-cycle assessment, supply-chain and disaster-impact
studies, and as the data backbone of CGE/IAM calibration.

**Ecosystem.** WIOD, EXIOBASE, Eora, GTAP-MRIO databases; `pymrio`; environmentally-extended IO
(EEIO); predecessors/relatives: SAM multiplier models, structural decomposition analysis.

**Research gaps.** Endogenizing coefficients (the CGE answer); reconciling MRIO databases (they
disagree); timeliness (tables lag years); uncertainty quantification on multipliers.

!!! quote "Lesson for the integrated simulator"
    Input–Output is the atlas's reminder that **the data substrate is a model in its own right**.
    Before any behavior is added, a balanced table of inter-sector flows already answers a huge
    class of policy questions — multipliers, embodied emissions, supply-chain exposure — exactly and
    transparently, via one linear operator. For the integrated simulator the lesson is twofold:
    (1) build on a **shared, balanced accounting core** (SAM/supply-use/MRIO) that every richer
    engine — CGE, IAM, footprint analysis — can draw from, so paradigms stay mutually consistent;
    and (2) keep the **cheap linear layer available** as a fast, auditable first pass, escalating to
    price-endogenous CGE or econometric E3ME only when substitution and behavior actually matter.
    It is the base of the tower the rest of the economics family is built on.

## Major publications

- Leontief, W. (1936). "Quantitative Input and Output Relations in the Economic System of the United
  States." *Review of Economics and Statistics* 18(3).
- Leontief, W. (1970). "Environmental Repercussions and the Economic Structure: An Input-Output
  Approach." *Review of Economics and Statistics* 52(3).
- Miller, R. E., Blair, P. D. (2009). *Input-Output Analysis: Foundations and Extensions.* 2nd ed.,
  Cambridge University Press.

## See also
- Builds toward: [CGE](cge.md) · Contrast: [E3ME](e3me.md) · [DSGE](dsge.md) · [Equilibrium vs Disequilibrium](../../comparative/equilibrium-vs-disequilibrium.md)
- Patterns: [Market Engine](../../patterns/market-engine.md) · [Data Pipeline](../../patterns/data-pipeline.md)
- Positioning: [Taxonomy](../../foundations/taxonomy.md) · Quality bar: [DICE dossier](../../model-families/climate-iam/dice.md)
