# Phase 3 — Research: candidate couplings, raced

The Research Lab's job is to **justify couplings and race them against baselines on real data**.
This page records the first coupling put to the test and the protocol; it grows as more couplings
and features are raced (each survivor cited, each result on the [leaderboard](leaderboard.md)).

## The first coupling under test: energy ⇄ climate ⇄ economy

**Hypothesis (issue [#5](https://github.com/Sour-abh-Raj/computational-policy-atlas/issues/5)).**
A carbon price changes the energy mix → changes emissions → changes temperature and climate damages
→ changes GDP → changes energy demand. A model that carries this **feedback loop** should predict a
GDP path better than the best model that ignores it — *when the feedback is actually operating*.

**Why it's grounded (literature).** This is the integrated-assessment thesis (Nordhaus's
[DICE](../model-families/climate-iam/dice.md); Weyant 2017 on IAMs) combined with the contested
economic closure ([CGE](../model-families/economics/cge.md) equilibrium vs
[E3ME](../model-families/economics/e3me.md) demand-led — Pollitt & Mercure 2018). Polyphony's twist:
keep **both** economic closures as voices and **report their disagreement**, and make the coupling
itself a **falsifiable** claim rather than an assumption.

## Contenders

| Contender | What it is | Feedback active? |
|-----------|-----------|:---:|
| **coupled ensemble** | energy + climate + CGE + E3ME under one clock (the [orchestrator](02-scaffold.md)) | ✅ |
| **economy-only (sum-of-parts)** | CGE + E3ME with energy cost at base and zero climate damage | ❌ |

Prediction for each = the **disagreement combiner's** skill-weighted mean of the two economics
voices' GDP (the point summary of a distribution we also keep in full).

## Race protocol (no fixed thresholds)

1. **Backtest** each contender on a **held-out, time-blocked** 30% tail (never shuffle a time
   series — `polyphony/data/splits.py`).
2. Score with **MASE** (scale-free; `polyphony/eval/metrics.py`); probabilistic CRPS/PIT come online
   once the ensemble emits full predictive distributions.
3. **Synergy Δ = economy-only error − coupled error** (`polyphony/tournament/synergy.py`). Δ>0 keeps
   the coupling; Δ≤0 **cuts** it (a publishable null).
4. **Two regimes** to validate the *method*, not just fit one dataset: a coupled data-generating
   process **and** a decoupled **negative control**.

## Result (Round 1)

| Regime | coupled MASE | economy-only MASE | Synergy Δ | Verdict |
|--------|---:|---:|---:|---|
| coupled DGP | 8.016 | 10.232 | **+2.216** | **keep** |
| decoupled (control) | 2.326 | 0.599 | **−1.727** | **cut** |

The method **keeps the coupling exactly when the coupling is real and cuts it when it is not** — the
behaviour a trustworthy synergy test must have. Full caveats in [04-validation](04-validation.md).

## Honest limitations & next couplings

- Predictors are **uncalibrated reduced-form toys** (MASE>1); this races the *coupling structure*,
  not a tuned forecast. Calibration + real data (issue #9) are prerequisites for skill claims.
- **Next to race:** feature candidates (lagged emissions, cumulative-emissions vs flow, regime
  indicators); the other synergy loops (land⇄climate⇄water #6, urban⇄transport⇄energy⇄health #7,
  macro⇄health #8); and **combiner** contenders (disagreement-preservation vs BMA, per ADR-0004).
- Every survivor earns an ADR and a leaderboard row; every null is recorded, not hidden.
