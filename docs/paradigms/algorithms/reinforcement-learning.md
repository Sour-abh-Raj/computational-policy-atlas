# Reinforcement Learning (RL) for Policy

!!! info "Silver method dossier"
    Reinforcement learning is **approximate [dynamic programming](dp.md) you can afford** — a way to learn
    a decision policy by **trial-and-error interaction with a (usually simulated) environment**, without
    solving the Bellman equation exactly or even knowing the model. It attacks the very state-space sizes
    that defeat exact DP and optimal control, which is why it is the emerging route to **adaptive,
    high-dimensional sequential policy** — and why the atlas's simulators ([SUMO](../../model-families/transport/sumo.md),
    energy models, IAMs) increasingly serve as **RL environments**.

> Learning a decision policy by trial-and-error interaction with a (usually simulated) environment to
> maximize expected cumulative reward — a data-driven route to sequential policy without an explicit
> model.

## Positioning card

| Axis (see [Taxonomy](../../foundations/taxonomy.md)) | Reinforcement Learning (RL) for Policy |
|------|------|
| Optimization vs Simulation | **Optimization via a learned policy** (learns *in* simulation) |
| Top-down vs Bottom-up | Data-driven |
| Equilibrium | N/A (multi-agent RL → learned equilibria) |
| Foresight | **Adaptive** (learned, closed-loop) |
| Deterministic vs Stochastic | **Stochastic** (MDP) |
| Time / Space | Step-based / state space (often high-dimensional) |
| Solution method | **Value / policy-gradient** (Q-learning, PPO, actor-critic) |

| Field | Value |
|-------|-------|
| Full name | Reinforcement Learning for Policy |
| Domain | Methods & Algorithms |
| First release / current | 1980s (TD learning) / deep RL 2013+ |
| Institution · lead | Sutton & Barto; deep RL (DeepMind, 2013+) |
| Language · solver | Python (Gymnasium, Stable-Baselines3, RLlib, CleanRL) |
| License / access | Open |

---

## 🎓 Scholar Track

**History & motivation.** RL grew from **animal-learning psychology** and **Sutton & Barto's** temporal-
difference learning in the **1980s**, fusing with **[dynamic programming](dp.md)** theory (RL *is*
sampled/approximate DP). The **deep RL** era (DeepMind's DQN on Atari, **2013**; AlphaGo, 2016) showed
neural function approximation could tackle enormous state spaces. Its motivation for policy modeling: many
sequential decisions are **high-dimensional and uncertain**, with no clean differentiable model — exactly
where exact DP/[optimal control](optimal-control.md) fail — but where a **simulator** can generate the
experience needed to *learn* a good policy.

**Mathematical formulation.** RL solves a **Markov Decision Process** $(S,A,P,r,\gamma)$: from state
$s_t$, an agent takes action $a_t\sim\pi_\theta(\cdot|s_t)$, receives reward $r_t$ and next state
$s_{t+1}\sim P$, seeking a policy maximizing **expected discounted return**
$J(\pi)=\mathbb{E}_\pi\big[\sum_t \gamma^t r_t\big]$. This is the **same Bellman objective** as [DP](dp.md)
— but $P$ and $r$ are **unknown or only sampleable**, so RL *learns* rather than solves. Two main families:

- **Value-based** — learn the action-value $Q(s,a)\approx \mathbb{E}[\text{return}\mid s,a]$ via the
  **temporal-difference** update $Q(s,a)\leftarrow Q(s,a)+\alpha\big(r+\gamma\max_{a'}Q(s',a')-Q(s,a)\big)$;
  with neural approximation this is **DQN**. Act greedily w.r.t. $Q$.
- **Policy-gradient / actor-critic** — parameterize the policy $\pi_\theta$ and ascend
  $\nabla_\theta J = \mathbb{E}[\nabla_\theta\log\pi_\theta(a|s)\,A(s,a)]$ (REINFORCE), stabilized by a
  learned **critic** (A2C/A3C) and trust-region/clipping (**TRPO/PPO**) — the workhorses for continuous
  control.

Key tensions: **exploration vs exploitation**, **sample efficiency**, and **stability** of function
approximation + bootstrapping + off-policy data (the "deadly triad").

**Solution algorithm.** Loop: the agent interacts with the **environment** (real or, usually, a
**simulator**), collects transitions, and updates $Q$ or $\pi_\theta$ by gradient methods; repeat for
millions of steps. **Model-based RL** additionally learns $P$ to plan; **offline RL** learns from logged
data without live interaction.

**Calibration & validation.** RL's "environment" *is* a simulator, so validation hinges on **sim-to-real**
fidelity and robustness; policies are stress-tested across seeds/scenarios. For policy applications,
**interpretability and safety** of the learned rule are central concerns (a black-box policy is hard to
defend).

**Strengths / weaknesses.** *Strengths:* handles **high-dimensional, model-free, stochastic** sequential
problems where DP/optimal control cannot; learns **closed-loop, adaptive** policies. *Weaknesses:*
**sample-hungry**, unstable to train, **black-box** (interpretability/accountability problems for public
policy), reward-specification is fraught ("reward hacking"), and sim-to-real gaps.

## 🛠️ Engineer Track

**Where it lives in the atlas.** RL is **approximate DP** applied where the state space is huge and a
**simulator supplies experience**: [SUMO](../../model-families/transport/sumo.md)'s **TraCI** makes it a
signal-control/CAV RL environment; energy dispatch, building control, and even IAM policy search are
active RL testbeds. It sits atop the **[Behavior Engine](../../patterns/behavior-engine.md)** (learning
agents) and turns a **[simulation](../../comparative/optimization-vs-simulation.md)** into an
optimization loop — the simulator is the environment, RL is the optimizer.

**Implementation.** **Gymnasium** environment API + agents from **Stable-Baselines3 / RLlib / CleanRL**
(PPO, SAC, DQN); training is GPU- and sample-intensive; parallel/vectorized environments and distributed
rollout (RLlib) are standard. Complexity is dominated by **environment steps** (millions) × network
updates.

**Data structures.** A replay buffer of transitions $(s,a,r,s')$ (off-policy), or trajectory rollouts
(on-policy); parametric $Q_\theta$/$\pi_\theta$ (neural nets); the environment's step/reset interface.

## 🏛️ Architect Track

**Reusable patterns.** RL contributes the **simulator-as-environment** pattern (wrap any forward model in
a step/reward interface and *learn* to control it — [SUMO](../../model-families/transport/sumo.md)/TraCI is
the exemplar), the **learned closed-loop policy** $\pi(s)$ (adaptive feedback vs a committed open-loop
plan), and **function approximation** to beat the [DP](dp.md) curse of dimensionality. **Multi-agent RL**
learns emergent equilibria — a bridge to [agent-based](../../comparative/abm-vs-cge.md) and game-theoretic
([WITCH](../../model-families/climate-iam/witch.md)) modeling.

**Trade-offs & alternatives.** RL vs [optimal control](optimal-control.md)/[DP](dp.md): same MDP objective,
but RL trades **guarantees and interpretability** for the ability to handle **model-free, high-dimensional,
stochastic** problems by learning from a simulator. Vs classical optimization ([LP](lp.md)/[MILP](milp.md)):
RL shines when the problem is **sequential, uncertain, and non-differentiable**, but a well-posed LP is
faster, optimal, and auditable — so for many policy problems the classical methods remain preferable. RL's
**black-box** nature is a serious drawback for **accountable public policy**, a caution the atlas stresses.

**Adoption.** Dominant in games/robotics; growing in **energy** (grid/building/battery control, dispatch),
**transport** (signal control, autonomous driving via SUMO/CARLA), operations, finance, and experimental
**climate-policy** search (e.g. RL over IAM/energy environments); LLM alignment (RLHF) popularized the term.

**Research gaps.** **Sample efficiency** and model-based RL; **safety, robustness, and interpretability**
for policy use; **sim-to-real** transfer; reward specification and value alignment; multi-agent learning of
credible equilibria.

!!! quote "Lesson for the integrated simulator"
    RL closes a loop the atlas keeps drawing: it turns the **simulator itself into the optimizer's
    environment**. Where a problem is genuinely **sequential, high-dimensional, and uncertain** — beyond
    exact [DP](dp.md) or [optimal control](optimal-control.md) — an agent can *learn* a closed-loop policy
    by interacting with the model, provided the model exposes a clean **step/reward interface** (the
    [SUMO](../../model-families/transport/sumo.md)/TraCI lesson). So the integrated simulator should be
    **RL-ready by design**: every engine drivable as an environment, with pause/observe/act hooks, so
    learning and classical optimization can both sit on top. But RL also sharpens a **governance caution**
    the atlas insists on: a learned policy is a **black box**, and public policy demands accountability — so
    the simulator should treat RL as one option on the **foresight/feedback dial** (open-loop optimal
    control and closed-loop DP/RL side by side), and pair any learned policy with the **interpretable
    shadow-price and Pareto-frontier** outputs that let humans understand and contest what the machine
    proposes.

## Major publications

- Sutton, R. S., Barto, A. G. (2018). *Reinforcement Learning: An Introduction* (2nd ed.). MIT Press.
- Mnih, V., et al. (2015). "Human-level control through deep reinforcement learning." *Nature* 518 (DQN).
- Schulman, J., et al. (2017). "Proximal Policy Optimization Algorithms." arXiv:1707.06347.

## See also
- Parent/siblings: [Dynamic Programming](dp.md) (exact) · [Optimal Control](optimal-control.md) (continuous) · composes with [Multi-Objective](multiobjective.md) (multi-objective RL)
- Environments in the atlas: [SUMO](../../model-families/transport/sumo.md) (TraCI) · energy dispatch · agent models ([Mesa](../../model-families/frameworks/mesa.md))
- Axes: [Optimization vs Simulation](../../comparative/optimization-vs-simulation.md) · [Deterministic vs Stochastic](../../comparative/deterministic-vs-stochastic.md)
- Patterns: [Behavior Engine](../../patterns/behavior-engine.md) · [Optimization Engine](../../patterns/optimization-engine.md) · Positioning: [Taxonomy](../../foundations/taxonomy.md)
