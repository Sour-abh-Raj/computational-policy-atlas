# WITCH — World Induced Technical Change Hybrid

!!! info "Bronze dossier"
    WITCH is the IAM that takes **strategic interaction** seriously. Where [DICE](dice.md) and
    [REMIND](remind.md) solve for a cooperative or single-planner optimum, WITCH models regions
    as **players in a dynamic Nash game** — each maximizing its own welfare while free-riding on
    others' mitigation — and folds in **endogenous (induced) technical change** so that R&D and
    learning are *decision variables*, not exogenous trends. It is the atlas's canonical
    **game-theoretic** IAM.

> A game-theoretic growth IAM: regions are strategic players solving a dynamic Nash game, with
> endogenous (induced) technical change in the energy sector — built to study cooperation and
> free-riding.

## Positioning card

| Axis (see [Taxonomy](../../foundations/taxonomy.md)) | WITCH |
|------|------|
| Optimization vs Simulation | **Optimization** (dynamic game) |
| Top-down vs Bottom-up | **Hybrid** (Ramsey growth + energy tech detail) |
| Equilibrium | General equilibrium (**Nash** non-cooperative / cooperative) |
| Foresight | **Perfect foresight** |
| Deterministic vs Stochastic | Deterministic (stochastic variants exist) |
| Time / Space | 5-yr / ~13–17 regions |
| Solution method | NLP + game-theoretic iteration (to a Nash equilibrium) |

| Field | Value |
|-------|-------|
| Full name | WITCH — World Induced Technical Change Hybrid |
| Domain | Climate — Integrated Assessment |
| First release / current | 2006 / WITCH 5+ |
| Institution · lead | RFF-CMCC European Institute on Economics and the Environment (EIEE); FEEM lineage (Bosetti, Tavoni) |
| Language · solver | GAMS (NLP; CONOPT/IPOPT) |
| License / access | Open (research) |

---

## 🎓 Scholar Track

**History & motivation.** WITCH was developed at **FEEM** (later **CMCC / EIEE**) from ~2006 by
Bosetti, Carraro, Tavoni and colleagues to answer a question the single-planner IAMs structurally
cannot: **what happens when regions act strategically?** Climate mitigation is a global public
good, so the "optimal" cooperative path is not what self-interested regions will actually choose.
WITCH's two signature commitments are therefore (1) **non-cooperative game theory** between
regions and (2) **endogenous technical change** — making innovation respond to policy rather than
drift exogenously.

**Mathematical formulation.** Each region *n* maximizes its **intertemporal welfare**
(discounted utility of per-capita consumption), a **Ramsey growth** core just like [DICE](dice.md),
but with a **hybrid energy sector**: a nested-CES production function combines capital, labor and
an **energy composite** that is itself built from detailed technologies (coal, gas, oil, nuclear,
renewables, CCS, backstops). Crucially, several **state variables are endogenous stocks of
knowledge and experience**: dedicated **R&D investment** raises energy efficiency and lowers the
cost of advanced technologies, and **learning-by-doing** curves reduce costs with cumulative
installed capacity. Regions are coupled through **global externalities** — the atmospheric GHG
stock, exhaustible-fuel markets, and **international knowledge/experience spillovers**.

The solution concept is an **open-loop Nash equilibrium**: each region solves its own
perfect-foresight optimization *taking the others' emission and investment paths as given*, and the
paths are iterated to a **fixed point** where no region wants to deviate. A **cooperative
(social-planner)** solution — maximizing the weighted sum of regional welfare, the Negishi-style
first best — is computed as the contrasting benchmark, so the **cost of non-cooperation** (the gap
between Nash and cooperative outcomes) is a direct model output.

**Solution algorithm.** A large **nonlinear program per region** (GAMS), wrapped in a
**game-theoretic iteration**: solve all regions, update the external variables each region sees
(GHG stock, fuel prices, spillovers), re-solve, repeat until the Nash fixed point converges. The
cooperative case is a single joint NLP.

**Calibration & validation.** Calibrated to base-year GDP, energy balances, technology costs and
observed learning rates; validated through IAM inter-comparisons (EMF, AMPERE, ADVANCE, the SSP
database) and against the coalition/free-riding literature.

**Strengths / weaknesses / criticisms.** *Strengths:* the leading IAM for **strategic behavior,
coalition formation and free-riding**, and a pioneer of **endogenous technical change**; can price
the *cost of non-cooperation*. *Criticisms:* the open-loop Nash concept and representative regional
agents are strong idealizations of real geopolitics; perfect foresight over R&D returns is
optimistic; the coupled game is computationally heavy and sensitive to spillover assumptions.

## 🛠️ Engineer Track

**Architecture & engines.** An **[Optimization Engine](../../patterns/optimization-engine.md)**
(intertemporal Ramsey welfare) fused with an **[Energy Dispatch Engine](../../patterns/energy-dispatch-engine.md)**
(technology-resolved energy sector) and a **[Technology-Adoption Engine](../../patterns/technology-adoption-engine.md)**
made *endogenous* — R&D and learning stocks that the optimizer invests in. Wrapping all of it is a
**game-solver loop** (the distinctive engine) that iterates regional NLPs to a Nash fixed point.
Implemented in **GAMS**.

**Data & complexity.** ~13–17 regions × 5-year steps to 2100/2150, each a sizable NLP; the
game-theoretic outer loop multiplies cost by the number of iterations to convergence. Endogenous
knowledge/experience stocks add non-convexity, making solves delicate.

**Openness / extensibility.** **Open for research** (GAMS source available from the WITCH/EIEE
team, hosted online); modular technology and damage assumptions; stochastic and risk variants have
been built on the same core.

## 🏛️ Architect Track

**Reusable patterns.** Three transferable ideas: **strategic (Nash) coupling** of otherwise-standard
regional optimizations; **endogenous technical change** as investable knowledge/experience stocks;
and reporting the **cooperative-vs-noncooperative gap** as a first-class result rather than assuming
cooperation.

**Trade-offs & alternatives.** WITCH shares [DICE](dice.md)'s Ramsey-welfare skeleton and
[REMIND](remind.md)'s hybrid macro-plus-energy structure, but is the only one that **drops the
single-planner assumption** in favor of an explicit game — see
[Optimization vs Simulation](../../comparative/optimization-vs-simulation.md) (it optimizes, but
the *equilibrium concept* is Nash, not a planner) and
[Equilibrium vs Disequilibrium](../../comparative/equilibrium-vs-disequilibrium.md). Against
process-based [GCAM](gcam.md)/[IMAGE](image.md), WITCH is far more stylized but can say something
they cannot: how much worse the outcome is *because regions don't cooperate*.

**Adoption.** IPCC-cited; central to EU projects (AMPERE, ADVANCE, ENGAGE) and the economics of
international climate agreements, burden-sharing, and coalition analysis.

**Ecosystem.** FEEM → CMCC/EIEE lineage; peers REMIND, MESSAGEix, GCAM, IMAGE, AIM; the induced-
technical-change literature (Popp, Nordhaus's own ETC critiques).

**Research gaps.** Richer (closed-loop / repeated-game) strategic concepts; heterogeneity within
regions; robustness of endogenous-innovation and spillover parameters; coupling to detailed land.

!!! quote "Lesson for the integrated simulator"
    WITCH's lesson is that **the equilibrium *concept* is itself a dial**. The same Ramsey-growth
    machinery that DICE solves as a benevolent planner, WITCH solves as a **non-cooperative Nash
    game** — and the gap between the two answers *is* the policy-relevant quantity (the cost of
    free-riding). An integrated simulator that only ever computes the cooperative optimum silently
    assumes away the central difficulty of climate policy. So the simulator should let the user
    **choose the solution concept** — single planner, cooperative Negishi weighting, or
    non-cooperative Nash — and should treat **innovation as endogenous**: R&D and learning are
    investment decisions that respond to the very policies being tested, not fixed exogenous
    trends. Both are switchable assumptions the atlas keeps arguing must not be hard-coded.

## Major publications

- Bosetti, V., Carraro, C., Galeotti, M., Massetti, E., Tavoni, M. (2006). "WITCH: A World Induced
  Technical Change Hybrid Model." *The Energy Journal* 27 (Special Issue).
- Bosetti, V., et al. (2009). "The 2008 WITCH model: New model features and baseline." FEEM Working
  Paper.
- Emmerling, J., et al. (2016). "The WITCH 2016 model — documentation and implementation of the SSP
  scenarios." FEEM/CMCC Working Paper 42.2016.

## See also
- Contrast: [DICE](dice.md) · [REMIND](remind.md) · [GCAM](gcam.md) · [Equilibrium vs Disequilibrium](../../comparative/equilibrium-vs-disequilibrium.md)
- Patterns: [Optimization Engine](../../patterns/optimization-engine.md) · [Technology-Adoption Engine](../../patterns/technology-adoption-engine.md) · [Energy Dispatch Engine](../../patterns/energy-dispatch-engine.md)
- Positioning: [Taxonomy](../../foundations/taxonomy.md) · Quality bar: [DICE dossier](dice.md)
