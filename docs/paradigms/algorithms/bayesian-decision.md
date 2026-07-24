# Bayesian Decision Models

!!! info "Silver method dossier"
    Bayesian decision theory is the **principled framework for acting under quantified uncertainty**:
    hold a **probabilistic belief** over unknowns, **update** it with evidence via Bayes' rule, and
    **choose the action that maximizes expected utility** over that belief. It is the formal backbone of
    the atlas's uncertainty-first models — [PAGE](../../model-families/climate-iam/page.md)'s Monte-Carlo
    SCC, [DSGE](../../model-families/economics/dsge.md)'s Bayesian estimation — and the rigorous answer to
    the question climate policy keeps posing: *what should we do when the most important quantities (climate
    sensitivity, damages) are deeply uncertain?*

> Choosing actions to maximize expected utility under a probabilistic posterior over unknowns — the
> principled framework for decision-making under quantified (and updated) uncertainty.

## Positioning card

| Axis (see [Taxonomy](../../foundations/taxonomy.md)) | Bayesian Decision Models |
|------|------|
| Optimization vs Simulation | **Optimization** (expected utility) |
| Top-down vs Bottom-up | N/A (method) |
| Equilibrium | N/A |
| Foresight | **Bayesian updating** (learning) |
| Deterministic vs Stochastic | **Stochastic** (posterior over unknowns) |
| Time / Space | N/A (static or sequential) |
| Solution method | **Bayesian inference + decision-theoretic maximization** |

| Field | Value |
|-------|-------|
| Full name | Bayesian Decision Models / Decision Analysis |
| Domain | Methods & Algorithms |
| First release / current | 1950s–60s / mature |
| Institution · lead | Savage (foundations); Raiffa & Schlaifer (decision analysis) |
| Language · solver | PyMC, Stan, ArviZ; influence diagrams; POMDP solvers |
| License / access | Open |

---

## 🎓 Scholar Track

**History & motivation.** Bayesian decision theory was axiomatized by **Leonard Savage** (*The
Foundations of Statistics*, 1954) — who showed that a rational agent satisfying coherence axioms **acts as
if** maximizing expected utility under a **subjective probability** — and made operational for practice by
**Raiffa & Schlaifer**'s **decision analysis** (1961). Its motivation is exactly the situation policy
faces: decisions must be made **now**, under **irreducible uncertainty**, with the prospect of **learning**
later. It provides the one framework that treats *belief*, *evidence*, and *action* coherently.

**Mathematical formulation.** Let $\theta$ be unknown states (e.g. climate sensitivity, damage exponent),
with **prior** $p(\theta)$. Observing data $D$ yields the **posterior** by **Bayes' rule**:

$$p(\theta\mid D) = \frac{p(D\mid\theta)\,p(\theta)}{p(D)}.$$

For an action $a$ with utility $u(a,\theta)$, the Bayes-optimal choice **maximizes posterior expected
utility**:

$$a^\* = \arg\max_a\; \mathbb{E}_{\theta\sim p(\theta\mid D)}\big[\,u(a,\theta)\,\big]
= \arg\max_a \int u(a,\theta)\,p(\theta\mid D)\,d\theta.$$

Two powerful extensions matter for policy: the **value of information (VoI)** — the expected utility gain
from resolving uncertainty *before* acting, which quantifies what better science/data is *worth*; and
**sequential** decision-making under partial observability (**POMDPs**), which fuses Bayesian belief-
updating with [dynamic programming](dp.md) — the agent maintains a **belief state** and plans over it,
formally uniting [DP](dp.md)/[RL](reinforcement-learning.md) with Bayesian inference. In climate economics,
this is the machinery behind **"act–then–learn" vs "learn–then–act"** and the economics of **catastrophic
tail risk** (Weitzman's dismal theorem is a statement about $p(\theta\mid D)$ having fat tails).

**Solution algorithm.** Inference: conjugate updates where possible, else **MCMC** (Stan, PyMC) or
variational methods to sample the posterior; then **integrate utility over the posterior** (often by Monte
Carlo) and maximize over actions. Sequential problems use **influence diagrams** or POMDP solvers.

**Strengths / weaknesses.** *Strengths:* a **coherent, normative** account of uncertainty and learning;
naturally quantifies the **value of information** and updates as evidence arrives; makes priors and value
judgments **explicit**. *Weaknesses:* results depend on the **prior** (contested for deep uncertainty);
posteriors can be **fat-tailed and fragile** (tail risk dominates yet is hard to estimate); full
sequential (POMDP) solutions are computationally hard; assumes uncertainty is **quantifiable** as
probability — challenged by **deep/Knightian uncertainty**.

## 🛠️ Engineer Track

**Where it lives in the atlas.** Bayesian decision theory is the formal core of the
**[Sensitivity Engine](../../patterns/sensitivity-engine.md)** in its *uncertainty-quantification* mode and
of the **[Calibration Engine](../../patterns/calibration-engine.md)** (Bayesian estimation).
[PAGE](../../model-families/climate-iam/page.md) *is* a Monte-Carlo integration over a prior for the SCC;
[DSGE](../../model-families/economics/dsge.md) is **Bayesian-estimated** (priors + likelihood → posterior
parameter distributions); [Covasim](../../model-families/health/covasim.md) and others calibrate in the same
spirit. It underlies **robust decision-making** debates across the IAMs.

**Implementation.** Probabilistic programming (**Stan, PyMC, NumPyro**) for the posterior; **ArviZ** for
diagnostics; Monte-Carlo expectation of utility; **influence diagrams**/POMDP libraries for sequential
problems. Complexity is dominated by posterior sampling (MCMC mixing) × the utility-integration Monte Carlo.

**Data structures.** Prior/posterior distributions (samples or parametric); a utility function $u(a,\theta)$;
for sequential problems, a **belief state** and observation model.

## 🏛️ Architect Track

**Reusable patterns.** The transferable ideas: **belief → update → act** as the decision loop, **expected
utility over a posterior** as the objective (not a point estimate), the **value of information** as a
first-class output (what is more research/monitoring *worth*?), and the **belief-state** abstraction that
lets sequential decisions ([DP](dp.md)/[RL](reinforcement-learning.md)) proceed under partial observability.

**Trade-offs & alternatives.** Bayesian decision theory quantifies uncertainty as **probability** and
optimizes the **mean** of utility — powerful when priors are credible, but contested under **deep
uncertainty**, where alternatives step in: **robust decision-making (RDM)**, **info-gap**, **min-max
regret**, and **scenario** approaches that seek decisions performing *well across* many futures rather than
*optimally in expectation*. This is the [Deterministic vs Stochastic](../../comparative/deterministic-vs-stochastic.md)
axis at the decision level, and it connects to [multi-objective](multiobjective.md) framing (robustness as
an objective). The atlas's stance — *document every viewpoint* — applies squarely: Bayesian expected-utility
and deep-uncertainty robustness are complementary lenses, not rivals.

**Adoption.** Decision analysis (medicine, engineering, business), **DSGE** macro estimation, **climate
economics** (uncertainty in the SCC, learning models, VoI for climate observation), epidemiological
inference, and risk regulation.

**Research gaps.** Priors and **fat tails** for climate catastrophe; scalable **sequential** Bayesian
decision (POMDP) for policy; reconciling Bayesian expected utility with **deep-uncertainty/robust** methods;
communicating probabilistic results to decision-makers.

!!! quote "Lesson for the integrated simulator"
    Bayesian decision theory gives the integrated simulator its **grammar for uncertainty and learning**:
    represent the unknown quantities as a **posterior**, optimize **expected utility over it** (not over a
    single "best guess"), and report the **value of information** so users see what resolving a given
    uncertainty is worth. This is the rigorous version of the atlas's insistence that models **carry
    distributions, not point estimates** ([PAGE](../../model-families/climate-iam/page.md)'s lesson), and it
    supplies the **belief-state** machinery to make sequential "act-then-learn" policy well-posed (uniting
    it with [DP](dp.md)/[RL](reinforcement-learning.md)). But the simulator must also heed the **limit**:
    when uncertainty is **deep** — priors themselves are contested, tails are fat and unknowable — expected-
    utility optimality can mislead, so the simulator should offer **robust/deep-uncertainty** decision modes
    alongside the Bayesian one and, true to the atlas method, **run both and show where they disagree**.
    Uncertainty is not noise to average away; it is a **first-class object** the whole simulator should carry
    end to end.

## Major publications

- Savage, L. J. (1954). *The Foundations of Statistics.* Wiley.
- Raiffa, H., Schlaifer, R. (1961). *Applied Statistical Decision Theory.* Harvard.
- Berger, J. O. (1985). *Statistical Decision Theory and Bayesian Analysis* (2nd ed.). Springer. ·
  Weitzman, M. (2009). "On modeling and interpreting the economics of catastrophic climate change." *REStat*
  91(1).

## See also
- Uncertainty-first models: [PAGE](../../model-families/climate-iam/page.md) · [DSGE](../../model-families/economics/dsge.md) (Bayesian estimation) · [Covasim](../../model-families/health/covasim.md)
- Sequential/kin: [Dynamic Programming](dp.md) · [Reinforcement Learning](reinforcement-learning.md) (belief-state POMDPs) · framing: [Multi-Objective](multiobjective.md)
- Axes: [Deterministic vs Stochastic](../../comparative/deterministic-vs-stochastic.md)
- Patterns: [Sensitivity Engine](../../patterns/sensitivity-engine.md) · [Calibration Engine](../../patterns/calibration-engine.md) · Positioning: [Taxonomy](../../foundations/taxonomy.md)
