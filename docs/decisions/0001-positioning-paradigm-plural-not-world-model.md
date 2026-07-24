# ADR-0001: Positioning — a paradigm-plural ensemble, **not** a world model

- **Status:** Accepted
- **Date:** 2026-07-24
- **Deciders:** Polyphony build loop (Research Lab)
- **Phase:** 0

## Context

Integrated policy models and "world models" already exist, and the space is crowded with
strong incumbents (see [related-work](../polyphony/related-work.md)):

- **Earth digital twins** (Destination Earth / DestinE) — high-resolution geophysical
  replicas, increasingly hybrid physics–AI, but **thin on the human/economic/policy side**
  and built in a **single modeling tradition**.
- **Integrated Assessment Models** (DICE, GCAM, IMAGE, REMIND, MESSAGEix — all in our
  atlas) — genuinely integrated economy⇄climate⇄energy, but each **hard-codes one set of
  contested assumptions** and they compare only via **manual intercomparison** (EMF, IPCC).
- **AI/agent "world models"** — (a) ML latent simulators for RL (Dreamer, JEPA, Genie);
  (b) LLM-driven ABMs of economies/societies (EconAgent, PolicySim). The field's own
  admitted central weakness is **validation**.

Two failure modes threaten a project like this: (1) **reinventing** an incumbent, and
(2) **overclaiming** — describing the artifact as "the world model," an oracle, or a
faithful replica of reality. Both would be dishonest and would obscure the actual
contribution.

## Decision

Polyphony is positioned, in **all** docs, code, papers, and READMEs, as a **paradigm-plural,
adversarially-validated policy-simulation ensemble** — a **decision-support instrument that
reports disagreement**. The contribution is a **method and a discipline of honesty**, not a
claim to replicate the world. Concretely, Polyphony commits to:

1. **Plurality** — keep rival traditions as distinct voices; never fuse them into one.
2. **Disagreement as signal** — where paradigms overlap, run **both** and **report the
   spread**; consensus and dissent are both first-class outputs.
3. **Adversarial validation** — select features/couplings/models by **beating rivals on
   real data** and by **surviving red-team attack**, directly attacking the validation gap
   the LLM-ABM literature concedes.
4. **Falsifiable synergy** — couple only where the **coupled ensemble out-predicts the sum
   of isolated parts** on real data; "no synergy here" is an acceptable finding.
5. **Exposed values** — welfare/equity is an **inspectable multi-objective dial**, never a
   buried constant.

**Banned language:** "world model," "digital twin of the world/economy/society" (as a
claim of fidelity), "oracle," "faithful/accurate replica," "predicts the future." We may
*use* the digital-twin **engineering backbone** (model ⇄ assimilation ⇄ control) without
claiming to be a twin *of the world*.

## Consequences

- Every artifact must pass an **honesty check** (PR template enforces it).
- Validation and disagreement-reporting are **not optional polish** — they are the product.
- We are differentiated from all three incumbent classes and can state precisely why.
- Risk: the honest framing is less flashy than "world model." Accepted deliberately — the
  credibility of a decision-support tool depends on it.

## Alternatives considered

- **Frame as an IAM++** — rejected: collapses plurality into one tradition, the exact gap
  we exist to fill.
- **Frame as a learned world model** — rejected: we make no latent-simulator claim and would
  inherit the unresolved validation critique without addressing it.
- **Stay silent on positioning** — rejected: ambiguity invites overclaiming; §0 of the brief
  requires explicit differentiation.

## Links

- [related-work.md](../polyphony/related-work.md) · [00-inventory.md](../polyphony/00-inventory.md)
- Atlas: [Digital Twins](../paradigms/algorithms/digital-twins.md) ·
  [Validation Engine](../patterns/validation-engine.md)
