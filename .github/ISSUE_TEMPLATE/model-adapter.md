---
name: Model adapter
about: Wrap an atlas model behind the common Polyphony interface so it can compose
title: "[adapter] <model> (<family>)"
labels: ["adapter", "engineering", "phase-2"]
---

## Model
<!-- Which atlas dossier. Link docs/model-families/**/<model>.md and its graph node. -->

## Interface mapping (state · step · dials · provenance)
- **State** vector it exposes:
- **`step(state, inputs, dt)`** semantics (time base, recursion vs foresight):
- **Dials** (contested assumptions from the comparative matrices it should expose):
- **Inputs it needs / outputs it emits** (for coupling):
- **Provenance** (paradigm, engine(s) it instantiates, native solver):

## Native paradigm & engines
<!-- Which of the 16 engine patterns this model instantiates; its native paradigm. -->

## Reference / surrogate
<!-- Is there an open reference implementation to wrap, or do we build a faithful
     reduced-form / surrogate? Cite it. Note fidelity limits honestly. -->

## Definition of done
- [ ] Implements the common `Model` interface; typed; unit-tested
- [ ] Round-trips a known scenario within documented tolerance of the reference
- [ ] Dials wired to config; provenance logged
- [ ] Registered in the ensemble registry; leaderboard/eval can call it
