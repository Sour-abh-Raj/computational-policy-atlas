# Related work & positioning

*What Polyphony is, what it is not, and where its contribution lies.* Kept current as the
field moves. The governing decision is [ADR-0001](../decisions/0001-positioning-paradigm-plural-not-world-model.md).

!!! danger "Honesty commitment"
    Polyphony is a **paradigm-plural policy-simulation ensemble** — a decision-support
    instrument that **reports disagreement**. It is **not** a "world model," an oracle, or a
    faithful replica of reality, and no Polyphony artifact may describe it as one. We may use
    the digital-twin **engineering backbone** (model ⇄ assimilation ⇄ control) without claiming
    to be a twin *of the world*.

## The incumbents, and how we differ

### 1. Earth digital twins — Destination Earth (DestinE)
High-resolution **geophysical** replicas (climate, extremes, oceans), increasingly hybrid
physics–AI, aimed at operational Earth-system prediction.

- **Strength:** physical fidelity and resolution.
- **Limit for policy:** thin on the **human/economic/policy** side; a **single modeling
  tradition** (physics), not paradigm-plural; not built to surface disagreement between rival
  *socio-economic* theories.
- **Polyphony differs:** we are **not** an Earth-system twin. Our core is the
  **human/economic/policy** layer, coupled to reduced-form climate/land/water — and we keep
  **multiple socio-economic traditions** in play rather than one.

### 2. Integrated Assessment Models — DICE, GCAM, IMAGE, REMIND, MESSAGEix
Genuinely integrated **economy⇄climate⇄energy** models (all catalogued in our atlas).

- **Strength:** real cross-domain integration; decades of scrutiny.
- **Limit:** each **hard-codes one set of contested assumptions** (one closure, one foresight
  regime, one damage function); they compare only via **manual intercomparison** (EMF, IPCC)
  after the fact.
- **Polyphony differs:** we make those assumptions **switchable dials**, keep the rival IAMs as
  **simultaneous voices**, and **report their disagreement as an output** rather than picking one
  model per study. We are **not** another single-tradition IAM.

### 3. AI / agent "world models"
Two distinct senses:

- **(a) ML latent simulators for RL** — Dreamer, JEPA, Genie: learn a compressed latent dynamics
  model to plan/act. Powerful for control in games/robotics; **not** validated, interpretable
  socio-economic policy models.
- **(b) LLM-driven ABMs** — EconAgent, generative-agent societies, PolicySim: LLM agents
  simulate economic/social behavior. Promising for behavioral richness, but the field's own
  reviews concede that **validation is the central unsolved problem**, and calibration/robustness
  are weak.
- **Polyphony differs:** we make **no latent-world-model claim**, and we **do not hand-wave
  validation** — adversarial backtesting against real data and red-teaming are the *product*, not
  an afterthought. LLM/ML methods are admissible **as competitors inside the tournament** (e.g. an
  ML surrogate or an LLM-ABM voice), earning their place only by winning on real data.

## The gap Polyphony fills

None of the incumbents does all four of these at once:

1. **Keeps rival modeling traditions as distinct voices** (plurality), and
2. **treats their disagreement as first-class signal** (not error to average away), and
3. **selects features, couplings, and models by adversarial competition against real data**
   (not fixed thresholds, not a single champion tradition), and
4. **directly attacks the validation gap** the LLM-ABM literature concedes, with backtesting +
   red-teaming as the core deliverable.

The contribution is therefore a **method and a discipline of honesty**, portable across domains —
not a claim to have replicated the world.

## Adjacent method traditions we build on (atlas-grounded)

- **Multi-method simulation** — [AnyLogic](../model-families/frameworks/anylogic.md) already runs
  SD+ABM+DES under one clock; it is the closest *runtime* analogue and a template. Polyphony adds
  **equilibrium/optimization** voices, **openness/reproducibility**, and **disagreement reporting**.
- **Model intercomparison projects** (EMF, AgMIP, ISIMIP, CMIP) — the scientific practice of
  running many models on one protocol. Polyphony **operationalizes** intercomparison as a *live,
  coupled, adversarial* system rather than a periodic manual exercise.
- **Bayesian model averaging / ensembling** — a genuine rival to disagreement-preservation. We
  will pit **BMA against deliberate disagreement-reporting** in a tournament and record which
  serves decision-makers better for which questions (see [00-inventory](00-inventory.md), §6 — gaps & candidate new factors).
- **Digital twins** ([atlas page](../paradigms/algorithms/digital-twins.md)) — the model⇄data⇄control
  backbone, used as **engineering**, not as a fidelity claim.

## One-line self-description (use this everywhere)

> **Polyphony is a paradigm-plural, adversarially-validated policy-simulation ensemble that
> reports the disagreement between modeling traditions — a decision-support instrument, not a
> world model.**

## Key references (to expand with primary sources as we build)

- Bauer et al. (2021), *The digital revolution of Earth-system science* / Destination Earth concept.
- Nordhaus (2017) DICE; Weyant (2017) *Some contributions of IAMs to climate policy* (IAM survey).
- Farmer & Foley (2009), *The economy needs agent-based modelling*; Haldane & Turrell (2019) on
  ABM for policy; recent LLM-ABM surveys documenting the **validation gap** (to cite precisely).
- Ha & Schmidhuber (2018) *World Models*; LeCun (2022) JEPA — for the ML "world model" sense.
- Borshchev & Filippov (2004), multi-method simulation (AnyLogic).
- Weyant, EMF; Rosenzweig et al., AgMIP; Warszawski et al., ISIMIP — intercomparison practice.
