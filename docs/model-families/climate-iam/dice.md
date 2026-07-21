# DICE — Dynamic Integrated Climate–Economy Model

> The smallest complete integrated assessment model, and the most influential.
> One representative agent optimizes global welfare while a compact carbon-cycle and
> climate module returns the temperature that damages its output. If you understand
> DICE, you understand the skeleton of every IAM that followed.

## Positioning card

| Axis (see [Taxonomy](../../foundations/taxonomy.md)) | DICE |
|------|------|
| Optimization vs Simulation | **Optimization** — intertemporal welfare maximization |
| Top-down vs Bottom-up | **Top-down** — aggregate Cobb–Douglas, no explicit technologies |
| Equilibrium | **Equilibrium** — Ramsey optimal growth |
| Foresight | **Perfect foresight** over the full horizon |
| Deterministic vs Stochastic | **Deterministic** (stochastic variant: **DSICE**) |
| Time / Space | **Discrete, 5-year steps** (older: 10-yr) / **global single region** |
| Solution method | **NLP** — GAMS/CONOPT; Python ports Pyomo/IPOPT; Julia Mimi |

| Field | Value |
|-------|-------|
| Full name | Dynamic Integrated model of Climate and the Economy |
| Domain | Climate — Integrated Assessment |
| First release / current | 1992 / **DICE-2023** (latest major revision) |
| Regional sibling | **RICE** (Regional Integrated Climate–Economy) |
| Institution · lead | Yale University · **William D. Nordhaus** (Nobel Prize in Economics, 2018) |
| Horizon | Typically to 2100–2500, 5-year steps |
| License | Model equations fully public; GAMS source published; multiple open-source ports |

---

## 🎓 Scholar Track

### History & motivation

DICE was developed by **William Nordhaus at Yale** through the late 1980s and
introduced in its recognizable form in 1992–1994 (*Managing the Global Commons*,
1994). The motivating question was radical for its time: **treat climate change as an
economic problem of optimal capital allocation over time.** Rather than asking
"how much warming is dangerous?", DICE asks "what emissions-control path *maximizes
the discounted welfare of humanity*, given that abatement is costly today but
avoids damages later?"

It fuses two previously separate traditions:

- the **Ramsey (1928) optimal growth model** of the macroeconomy, and
- a **reduced-form geophysical model** of the carbon cycle and global temperature.

The coupling produces an endogenous **Social Cost of Carbon (SCC)** — the marginal
welfare damage of one additional tonne of CO₂ — which became DICE's most consequential
export to policy. Nordhaus shared the 2018 Nobel Memorial Prize "for integrating
climate change into long-run macroeconomic analysis." Major versions: DICE-1994,
-1999 (RICE), -2007, -2013R, -2016R(2), and **DICE-2016R2 / 2023**.

### Mathematical formulation

DICE is a **finite-horizon nonlinear optimal-growth problem**. Below is the standard
DICE-2016R form (notation lightly modernized). Time $t$ is indexed in 5-year steps.

#### Objective — discounted utilitarian welfare

$$
\max_{\{\mu_t,\, s_t\}} \; W = \sum_{t=1}^{T} R_t \, L_t \, U(c_t),
\qquad U(c_t) = \frac{c_t^{\,1-\alpha} - 1}{1-\alpha}, \qquad R_t = \frac{1}{(1+\rho)^{5t}}
$$

- $c_t$ — per-capita consumption; $L_t$ — population (labor);
- $\alpha$ — elasticity of marginal utility of consumption (risk/inequality aversion);
- $\rho$ — **pure rate of social time preference** (the contested discount parameter);
- $R_t$ — utility discount factor.

#### Economy (Ramsey growth)

Gross output via Cobb–Douglas in capital and labor with exogenous total-factor
productivity $A_t$:

$$
Y^{\text{gross}}_t = A_t \, K_t^{\gamma} \, L_t^{\,1-\gamma}
$$

Output is reduced by **climate damages** $\Omega_t$ and **abatement costs** $\Lambda_t$:

$$
Q_t = \Omega_t \,(1 - \Lambda_t)\, Y^{\text{gross}}_t,
\qquad
\Omega_t = \frac{1}{1 + a_2 T_{AT,t}^{\,2}} \;\approx\; 1 - a_2 T_{AT,t}^{2}
$$

$$
\Lambda_t = \theta_{1,t}\, \mu_t^{\,\theta_2}
$$

- $\Omega_t$ — the **damage function**, mapping atmospheric temperature $T_{AT}$ to a
  fraction of output lost (quadratic in temperature);
- $\Lambda_t$ — abatement cost as a fraction of output, convex in the **emissions
  control rate** $\mu_t \in [0,1]$; $\theta_{1,t}$ is the backstop-technology cost, $\theta_2 \approx 2.6$.

Capital accumulation and the budget identity:

$$
K_{t+1} = (1-\delta)^5 K_t + 5\, I_t, \qquad
I_t = s_t Q_t, \qquad
C_t = Q_t - I_t, \qquad c_t = C_t / L_t
$$

#### Emissions and the carbon cycle

Industrial emissions fall with the control rate; $\sigma_t$ is the carbon intensity of output:

$$
E^{\text{ind}}_t = \sigma_t (1-\mu_t)\, Y^{\text{gross}}_t, \qquad
E_t = E^{\text{ind}}_t + E^{\text{land}}_t
$$

Carbon accumulates in a **three-reservoir linear box model** — atmosphere (AT),
upper ocean/biosphere (UP), deep ocean (LO):

$$
\mathbf{M}_{t+1} = \Phi\, \mathbf{M}_t + \begin{bmatrix} 5\,E_t \\ 0 \\ 0 \end{bmatrix},
\qquad
\mathbf{M} = \begin{bmatrix} M_{AT} \\ M_{UP} \\ M_{LO} \end{bmatrix}
$$

where $\Phi$ is a $3\times3$ mass-conserving transfer matrix.

#### Radiative forcing and temperature

Forcing is logarithmic in the atmospheric CO₂ stock, plus exogenous non-CO₂ forcing $F^{EX}$:

$$
F_t = \eta \, \log_2\!\left(\frac{M_{AT,t}}{M_{AT,1750}}\right) + F^{EX}_t
$$

Temperature evolves as a **two-box energy-balance model** (atmosphere/upper ocean $T_{AT}$, deep ocean $T_{LO}$):

$$
T_{AT,t+1} = T_{AT,t} + \xi_1\!\left[ F_{t+1} - \lambda\, T_{AT,t} - \xi_2 (T_{AT,t}-T_{LO,t}) \right]
$$
$$
T_{LO,t+1} = T_{LO,t} + \xi_3 (T_{AT,t} - T_{LO,t})
$$

$\lambda = \eta/\text{ECS}$ links the feedback parameter to **equilibrium climate
sensitivity** — the single geophysical number that most drives DICE's policy output.

#### The variable ledger

| Kind | Symbols |
|------|---------|
| **State variables** | $K_t$ (capital), $\mathbf{M}_t$ (carbon stocks), $T_{AT,t}, T_{LO,t}$ (temperatures) |
| **Decision (control) variables** | $\mu_t$ (emissions control rate), $s_t$ (savings rate) → $I_t$ |
| **Objective** | $W$ = discounted sum of population-weighted utility |
| **Key exogenous drivers** | $A_t, L_t, \sigma_t, \theta_{1,t}, F^{EX}_t, E^{\text{land}}_t$ |
| **Contested parameters** | $\rho$ (discount), $\alpha$, $a_2$ (damage), ECS |

### Solution & algorithms

DICE is a smooth **nonlinear program (NLP)**: ~30 equality/inequality constraints,
a few hundred variables once unrolled over the ~60 time steps. The reference
implementation is **GAMS with the CONOPT** gradient-based NLP solver. It solves in
**seconds** on a laptop. Python ports use **Pyomo + IPOPT**; the Julia **Mimi**
framework offers a modular reimplementation (MimiDICE) built for coupling and
uncertainty analysis.

### Calibration

- **Economy**: $A_t, L_t, \sigma_t$ calibrated to historical GDP, population, and
  emissions and extrapolated with assumed decarbonization and productivity growth.
- **Carbon cycle / climate**: $\Phi$, $\eta$, ECS, and the $\xi$ coefficients tuned so
  the reduced-form modules **emulate full Earth-system models** (e.g., MAGICC) and CMIP
  ensembles over standard forcing scenarios.
- **Damage function** $a_2$: calibrated to a small set of sectoral damage estimates
  (agriculture, sea-level, health) — the **weakest empirical link**, see criticisms.
- **Preferences**: $\rho$ and $\alpha$ chosen to match observed real interest
  rates/returns (Nordhaus's "descriptive" calibration), a deeply contested choice.

### Validation

IAMs like DICE **cannot be validated by out-of-sample prediction** in the usual
sense — the horizon is centuries and the counterfactuals are unobservable. Validation
is instead:

1. **Module emulation** — checking the carbon/climate boxes reproduce complex Earth-system
   models over known scenarios.
2. **Backcasting** the economic/emissions modules against history.
3. **Structural / sensitivity analysis** — confirming outputs respond sensibly to
   parameter changes.

This *validation gap* is itself a central lesson (see Architect Track).

### Scenario generation

Policy experiments are constructed by constraining or fixing the controls:

- **Optimal** — let the model choose $\mu_t$ (the welfare-maximizing path → endogenous SCC).
- **Baseline / no-policy** — fix $\mu_t = 0$.
- **Temperature-limited** — add a constraint $T_{AT,t} \le 2^\circ\text{C}$ (or 1.5 °C).
- **Carbon-price paths** — impose an exogenous price and read the induced $\mu_t$.
- **Uncertainty** — Monte-Carlo over ECS, $\rho$, $a_2$ (the basis of probabilistic SCC).

### Strengths / Weaknesses / Known criticisms

=== "Strengths"
    - **Transparency**: small enough to write on a few pages and fully audit.
    - **Integration**: end-to-end economy→emissions→climate→damages→welfare in one solve.
    - **Endogenous SCC**: a single, policy-usable number falls out of the optimization.
    - **Speed & extensibility**: seconds to solve; trivial to embed in Monte-Carlo or couple.
    - **Pedagogical canon**: the reference against which all IAMs are taught.

=== "Weaknesses / Criticisms"
    - **The damage function.** Quadratic $a_2 T^2$ is calibrated to sparse data and
      almost certainly **understates tail and catastrophic risk**; Pindyck (2013,
      *"Climate Change Policy: What Do the Models Tell Us?"*) argues the damage and
      climate-sensitivity assumptions are "close to arbitrary." No tipping points.
    - **Discounting.** The SCC is extraordinarily sensitive to $\rho$. The
      **Stern (2007) vs Nordhaus** debate — near-zero prescriptive discounting vs
      market-calibrated descriptive discounting — can move the SCC by an order of magnitude.
    - **Aggregation.** One global representative agent hides distribution, equity, and
      regional heterogeneity (partly addressed by RICE).
    - **Deep uncertainty / fat tails.** Weitzman's "Dismal Theorem" argues expected-utility
      IAMs with fat-tailed sensitivity can be dominated by unbounded low-probability losses.
    - **Coarse resolution.** 5-year steps and a single region cannot represent
      short-run variability, extremes, or spatial damages.

### Major publications

- Nordhaus, W. (1992). *An Optimal Transition Path for Controlling Greenhouse Gases.* Science.
- Nordhaus, W. (1994). *Managing the Global Commons: The Economics of Climate Change.* MIT Press.
- Nordhaus, W. & Boyer, J. (2000). *Warming the World: Economic Models of Global Warming* (RICE). MIT Press.
- Nordhaus, W. (2017). *Revisiting the Social Cost of Carbon.* PNAS 114(7).
- Nordhaus, W. (2018). Nobel Prize Lecture: *Climate Change: The Ultimate Challenge for Economics.*
- Pindyck, R. (2013). *Climate Change Policy: What Do the Models Tell Us?* J. Econ. Literature. (critique)
- Stern, N. (2007). *The Economics of Climate Change: The Stern Review.* (discounting debate)

---

## 🛠️ Engineer Track

### Software architecture

Despite its influence, reference DICE is a **single GAMS file**: parameter blocks,
variable declarations, an equation block, and a solve statement. Conceptually it
decomposes into engines that recur across all IAMs (see
[Architecture Patterns](../../patterns/index.md)):

```mermaid
graph LR
    SC[Scenario config<br/>exogenous paths A,L,σ] --> EC[Economy Engine<br/>Ramsey growth]
    EC -->|"emissions E"| CC[Carbon-cycle Engine<br/>3-box M]
    CC -->|"stock M_AT"| CL[Climate Engine<br/>forcing + 2-box T]
    CL -->|"temperature T_AT"| DM[Damage Engine<br/>Ω(T)]
    DM -->|"net output Q"| EC
    EC --> OBJ[Welfare objective W]
    OPT([Optimization Engine<br/>NLP solver]) -.controls μ,s.-> EC
    OPT -.maximizes.-> OBJ
```

The **Optimization Engine wraps everything**: the four physical/economic engines
define constraints; the solver chooses $\mu_t, s_t$ to maximize $W$. This
"optimizer-on-top-of-coupled-modules" is the defining IAM software pattern.

### Data structures & pipeline

- **Inputs**: scalar parameters + a handful of exogenous **time series**
  ($A_t, L_t, \sigma_t, \theta_{1,t}, F^{EX}_t, E^{\text{land}}_t$), typically hard-coded
  or read from a spreadsheet.
- **Internal**: everything is indexed over the single set `t` (time). No spatial grid,
  no agent list — a defining simplicity.
- **Outputs**: time paths of $T_{AT}, M_{AT}, \mu_t$, consumption, and the SCC
  (recovered as the ratio of shadow prices $\partial W/\partial E_t \big/ \partial W/\partial C_t$).

### Computational complexity

Trivial by modern standards: a few hundred variables, dense small Jacobian, converges
in **seconds**. The cost multiplies only for **uncertainty quantification** — thousands
to millions of Monte-Carlo solves over ECS/damage/discount draws — which is embarrassingly
parallel. Stochastic-dynamic variants (**DSICE**, Cai–Judd) are far heavier: solving the
Bellman recursion in a multi-dimensional continuous state space needs sparse-grid /
approximate dynamic programming.

### Language · open-source · extensibility

| Implementation | Stack | Notes |
|----------------|-------|-------|
| Reference | **GAMS + CONOPT** | Nordhaus's published source |
| Python | **Pyomo + IPOPT**, `PyDICE`, `DICE` ports | most common for research reuse |
| Julia | **Mimi** framework (`MimiDICE`, `MimiRICE`) | modular, built for coupling + UQ |
| R / Excel | teaching ports | pedagogy |

Extensibility is DICE's quiet superpower: because it is tiny and equation-explicit,
researchers routinely swap the **damage function** (e.g., Howard–Sterner, Burke et al.),
the **carbon cycle** (FAIR, MAGICC emulators), or add **regions** (→ RICE), **sectors**,
or **stochasticity** (→ DSICE) without rewriting the whole model.

### How to run it (minimal Pyomo sketch)

```python
# Illustrative skeleton — not a drop-in DICE; shows the optimizer-on-modules pattern.
from pyomo.environ import (ConcreteModel, Var, Objective, Constraint,
                           NonNegativeReals, maximize, SolverFactory, value)

m = ConcreteModel()
T = range(60)                      # 60 five-year steps
m.mu = Var(T, bounds=(0, 1.2))     # emissions control rate (control)
m.s  = Var(T, bounds=(0.1, 0.9))   # savings rate (control)
# ... declare K, M_AT, M_UP, M_LO, T_AT, T_LO as Vars over T ...

# Constraints encode: Cobb-Douglas output, damages Omega, abatement Lambda,
# capital accumulation, 3-box carbon cycle, forcing, 2-box temperature.
# m.capital = Constraint(T, rule=lambda m,t: ...)   # K[t+1] = (1-delta)^5 K[t] + 5 I[t]

m.W = Objective(expr=sum(R[t]*L[t]*util(c[t]) for t in T), sense=maximize)
SolverFactory("ipopt").solve(m)
scc = ...   # = shadow price on emissions / shadow price on consumption, scaled
```

---

## 🏛️ Architect Track

### Reusable design patterns

DICE is the cleanest textbook example of several patterns catalogued in
[Architecture Patterns](../../patterns/index.md):

- **Optimization Engine over coupled modules** — a solver maximizes a global objective
  subject to constraints supplied by domain modules. Carry this as the top-level
  contract of any policy-optimization subsystem.
- **Reduced-form emulator** — replace an expensive Earth-system model with a handful of
  linear boxes calibrated to it. The general lesson: *an integrated simulator should
  expose "emulator" and "full-fidelity" implementations behind one interface.*
- **Damage/Objective as a swappable component** — the most contested equation is
  isolated, so it can be replaced without touching the solver. **Make your most
  uncertain assumptions the most modular.**
- **Shadow-price extraction** — policy-relevant quantities (SCC) recovered from the
  optimizer's duals rather than computed separately.

### Trade-offs & alternatives

| DICE chose | It gave up | The alternative wins when… |
|-----------|------------|----------------------------|
| Aggregate top-down | Technological & regional detail | you need explicit technology choice → **TIMES/MESSAGEix**, or regions → **RICE/REMIND** |
| Perfect foresight | Realistic myopia/learning | agents can't foresee prices → **recursive-dynamic (GCAM)** or **RL** |
| Deterministic | Risk & fat tails | tail risk dominates → **DSICE / robust decision-making** |
| Quadratic damages | Tipping points, non-convexity | catastrophe matters → **damage functions with thresholds** |
| Tiny & auditable | Fidelity | you need sectoral/spatial realism → bottom-up energy or process models |

### Adoption

- **Government / policy**: DICE (with **FUND** and **PAGE**) underpinned the U.S.
  Interagency Working Group's **Social Cost of Carbon** estimates used in federal
  rulemaking. Its successors (e.g., the **GIVE** model) inform the EPA's updated SCC.
- **IPCC**: DICE-family results feature in Working Group III assessments of mitigation
  costs and carbon pricing.
- **Academia**: the default teaching and benchmarking IAM worldwide.

### Ecosystem

- **Regional sibling**: **RICE** (multi-region DICE).
- **Competing cost-benefit IAMs**: **FUND** (Tol) and **PAGE** (Hope) — the other two
  "IWG" models, with richer damage disaggregation (FUND) and explicit uncertainty (PAGE).
- **Process/technology-rich IAMs** (a different philosophy): **GCAM, MESSAGEix, IMAGE,
  REMIND, WITCH, AIM** — bottom-up, multi-region, scenario-driven rather than a single
  welfare optimum.
- **Successors / forks**: **DICE-2023**, **DSICE** (stochastic), **MimiDICE** (Julia),
  **GIVE** (modular, updated damages/climate, EPA 2022).

### Research gaps & future directions

- Empirically grounded, **non-convex damage functions** with tipping points.
- Principled treatment of **deep uncertainty** (beyond Monte-Carlo over a few parameters).
- **Distributional** welfare (equity weights, within-region inequality).
- **Endogenous technical change** and induced innovation.
- Coupling DICE-style optimization with **high-resolution physical and energy models**
  without losing tractability — precisely the integrated-simulator problem.

### Lesson for the integrated simulator

!!! quote "If we were designing the world's most capable policy simulator today…"
    DICE teaches that **auditability is a feature, not a limitation**. Its influence
    comes not from fidelity but from being small enough that every assumption is
    visible and every contested equation — the damage function, the discount rate — is
    a *named, swappable component*. A next-generation simulator should keep that
    discipline at every scale: **couple modules through explicit interfaces, expose
    emulator/full-fidelity variants behind one contract, recover policy quantities
    from shadow prices, and make the most uncertain assumptions the most modular** —
    so that when philosophies disagree (Stern vs Nordhaus on discounting), the system
    can host *both* rather than hard-coding one.

## See also

- Paradigm: [Optimization vs Simulation](../../comparative/index.md)
- Foundations: [Taxonomy](../../foundations/taxonomy.md) · [Three-Track Method](../../foundations/three-track-method.md)
- Roadmap of related IAMs: [Model Families](../index.md)
