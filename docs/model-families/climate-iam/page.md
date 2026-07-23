# PAGE — Policy Analysis of the Greenhouse Effect

!!! info "Bronze dossier"
    PAGE is the **uncertainty-first** member of the cost-benefit IAM trio (with
    [DICE](dice.md) and [FUND](fund.md)) — the model behind the **Stern Review**. Where DICE
    computes an optimal path and FUND decomposes damages by sector, PAGE makes **Monte-Carlo
    the core mode**, propagating probability distributions (including explicit **catastrophic
    risk**) through a deliberately compact climate–damage chain.

> The uncertainty-first cost-benefit IAM used in the Stern Review; Monte-Carlo is the core
> mode, propagating probability distributions through a compact climate-damage chain.

## Positioning card

| Axis (see [Taxonomy](../../foundations/taxonomy.md)) | PAGE |
|------|------|
| Optimization vs Simulation | **Simulation** (probabilistic) |
| Top-down vs Bottom-up | Top-down |
| Equilibrium | Reduced-form |
| Foresight | Recursive |
| Deterministic vs Stochastic | **Stochastic** (Monte-Carlo core) |
| Time / Space | ~decadal / 8 regions |
| Solution method | Monte-Carlo simulation |

| Field | Value |
|-------|-------|
| Full name | PAGE — Policy Analysis of the Greenhouse Effect |
| Domain | Climate — Integrated Assessment (cost-benefit) |
| First release / current | 1990s / PAGE09, PAGE-ICE |
| Institution · lead | Chris Hope, University of Cambridge |
| Language · solver | Originally Excel/@RISK; **MimiPAGE** (Julia) |
| License / access | Open (MimiPAGE) |

---

## 🎓 Scholar Track

**History & motivation.** PAGE was developed by **Chris Hope** at the University of Cambridge
from the early 1990s, explicitly to support **policy analysis under deep uncertainty** —
built for the European Commission and later famous as the workhorse of the **2006 Stern
Review on the Economics of Climate Change**. Its design philosophy: keep the deterministic
skeleton small and **put the emphasis on probability distributions** over key parameters.

**Mathematical formulation.** PAGE is a **reduced-form recursive simulation** run in
**Monte-Carlo** mode. Each of ~8 regions has a compact climate response (emissions →
concentration → temperature) and **damage functions** with a polynomial dependence on
temperature, split into **economic** and **non-economic** damages plus an explicit
**discontinuity (catastrophe) term** that triggers probabilistically above a temperature
threshold. Crucially, **most inputs are distributions, not point values** — climate
sensitivity, damage exponents, the catastrophe threshold and its magnitude — so each run
draws a sample and the **output is a distribution** of impacts and SCC. Adaptation is
represented as a lever reducing a fraction of damages.

**Solution algorithm.** Sample all uncertain parameters → run the recursive climate–damage
chain → record outcome; repeat thousands of times → build the distribution. SCC via the
marginal-pulse experiment, reported as a *distribution* with a mean and tail.

**Calibration & validation.** Parameter distributions are set from the **IPCC assessed
ranges** and impacts literature; the model is benchmarked against other IAMs and used in the
**US IWG** SCC process. Its Stern-Review parameterization (notably a low discount rate) drove
its famously high damage estimates — a transparent illustration of *how assumptions, not just
mechanism, set the answer*.

**Strengths / weaknesses / criticisms.** *Strengths:* uncertainty and **catastrophic tail
risk are first-class**, not afterthoughts; compact and legible; distributional output.
*Criticisms:* reduced-form damages are coarse (fewer sectors than [FUND](fund.md)); results
are highly sensitive to the (assumed) parameter distributions and discount rate — the Stern
debate is largely about *these choices*, not PAGE's structure.

## 🛠️ Engineer Track

**Architecture & engines.** A compact **[Climate Engine](../../patterns/climate-engine.md)**
and reduced-form **damage module** wrapped in a dominant
**[Sensitivity Engine](../../patterns/sensitivity-engine.md)** — the Monte-Carlo driver *is*
the model's main loop — plus a **[Scenario Engine](../../patterns/scenario-engine.md)**. The
modern **MimiPAGE** port puts this on the **Mimi** Julia component framework alongside
MimiDICE/MimiFUND.

**Data & complexity.** Very lightweight (8 regions, decadal, reduced-form), so thousands of
Monte-Carlo draws run quickly — by design, since uncertainty propagation is the point.

**Openness / extensibility.** Originally Excel + **@RISK**; now open as **MimiPAGE** (Julia),
with swappable components and transparent parameter distributions.

## 🏛️ Architect Track

**Reusable patterns.** The exemplar of a **[Sensitivity Engine](../../patterns/sensitivity-engine.md)-first**
design — where uncertainty quantification is the primary architecture, not a wrapper — plus
[Climate](../../patterns/climate-engine.md) and [Scenario](../../patterns/scenario-engine.md)
engines. The explicit **catastrophe/discontinuity term** is a notable pattern for
representing tail risk.

**Trade-offs & alternatives.** Against [DICE](dice.md): PAGE gives up optimization for a
**probabilistic distribution** of outcomes; against [FUND](fund.md): PAGE trades sectoral
damage detail for **tail-risk and uncertainty emphasis**. This is the cost-benefit-IAM face
of [Deterministic vs Stochastic](../../comparative/deterministic-vs-stochastic.md).

**Adoption.** The **Stern Review** (2006); the **US IWG** SCC estimates (with DICE and FUND);
extensive academic uncertainty and tail-risk analysis. **PAGE-ICE** adds updated science
including tipping points.

**Ecosystem.** Trio with DICE and FUND; MimiPAGE in the Mimi ecosystem; PAGE-ICE successor.

**Research gaps.** Better-grounded parameter distributions; richer (less reduced-form)
damages; improved representation of tipping points and their correlations.

!!! quote "Lesson for the integrated simulator"
    PAGE shows what it means to make **uncertainty the primary object rather than a
    post-hoc sensitivity check**: keep the deterministic skeleton small, express the
    genuinely uncertain inputs as **distributions**, and let the model output a
    *distribution* — with an explicit **catastrophe/discontinuity term** so the tail that
    dominates welfare is represented, not truncated. For an integrated simulator the lesson is
    that a [Sensitivity Engine](../../patterns/sensitivity-engine.md) should be able to sit at
    the *center* of a subsystem, not just around it, and that the Stern experience is a
    permanent reminder to **report how much of a headline number is science and how much is
    the assumed distribution (and discount rate)** — exactly the conditionality the atlas's
    synergy layer keeps surfacing.

## Major publications

- Hope, C. (2006). "The marginal impact of CO₂ from PAGE2002." *The Integrated Assessment
  Journal* 6(1).
- Stern, N. (2007). *The Economics of Climate Change: The Stern Review*. Cambridge University
  Press. (uses PAGE)
- Yumashev, D., et al. (2019). "Climate policy under tipping points" — PAGE-ICE. *Nature
  Communications* 10.

## See also
- Trio: [DICE](dice.md) · [FUND](fund.md) · Contrast: [GCAM](gcam.md)
- Patterns: [Sensitivity Engine](../../patterns/sensitivity-engine.md) · [Climate Engine](../../patterns/climate-engine.md)
- Related: [Deterministic vs Stochastic](../../comparative/deterministic-vs-stochastic.md) · [Taxonomy](../../foundations/taxonomy.md)
