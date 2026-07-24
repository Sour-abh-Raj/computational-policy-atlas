# ADR-0003: Tech stack for the Polyphony package

- **Status:** Accepted
- **Date:** 2026-07-24
- **Deciders:** Polyphony build loop (Engineering Lab)
- **Phase:** 1

## Context

Phase 2 scaffolds real code: a common model interface, an orchestrator, a combiner, a tournament,
and adapters for a DICE⇄energy⇄CGE slice. We need a stack that is (a) **reproducible and open**
(ADR-0001/0002), (b) low-friction for scientific-Python collaborators, (c) able to host both
equation-based and agent-based voices, and (d) honest about dependencies (kept minimal early).

## Decision

- **Language:** Python ≥ 3.11 (matches the atlas's scientific-Python framing — Mesa, PyPSA,
  ActivitySim, UrbanSim all Python; lowest barrier).
- **Core numerics:** `numpy`, `pandas`, `scipy`. **Typing:** standard `typing.Protocol` for the
  model interface (structural typing → adapters need not inherit).
- **Config/dials:** plain dataclasses + YAML (declarative, à la [Calliope](../model-families/energy/calliope.md)'s
  model-as-data); dials validated against a `DialsSpec`.
- **Uncertainty/assimilation:** start with hand-rolled Kalman/EnKF + Monte-Carlo on numpy (few deps,
  fully inspectable); allow `filterpy`/`pymc` behind extras only if a tournament shows they earn it.
- **Surrogates:** `scikit-learn` (GP/tree) behind an extra; heavier neural emulators only if they win.
- **Optimization/solvers:** keep solver deps **out of core**; adapters that need LP/NLP declare their
  own extra (e.g. `pulp`/`highspy` for a toy energy LP, `scipy.optimize` for reduced-form DICE). No
  commercial solver is required to run the slice.
- **Testing/quality:** `pytest`, `ruff`, `mypy`; CI runs these + `mkdocs build --strict` + the graph
  0-dangling check.
- **Docs:** MkDocs Material (already the atlas surface); diagrams as Mermaid in-repo (no external
  render service).

## Consequences

- `pip install -e "polyphony[dev]"` stays fast; heavy/commercial deps are opt-in extras, never in the
  core install — keeps the vertical slice reproducible on a laptop and in CI.
- Structural typing lets us wrap reference implementations without invasive inheritance.
- Risk: hand-rolled assimilation/surrogates are less battle-tested than libraries — accepted for
  transparency and few-deps; they must **win their tournament** against library alternatives to stay,
  which is the mechanism ADR-0001 mandates anyway.

## Alternatives considered

- **Julia (SciML)** — excellent for coupled ODE/optimization, but raises the contributor barrier and
  diverges from the atlas's Python ecosystem; revisit only if performance becomes the binding constraint.
- **Mesa/AnyLogic as the host runtime** — Mesa is ABM-only; AnyLogic is closed/commercial (rejected by
  ADR-0001's openness commitment). We instead take AnyLogic's *multi-method* lesson and build an open
  composition layer.
- **Heavy deps up front (pymc/pytorch in core)** — rejected: violates the minimal-repro principle;
  admitted later only by winning a tournament.

## Links

- [01-blueprint.md](../polyphony/01-blueprint.md) · [ADR-0002](0002-repo-layout-and-trunk-based-flow.md)
- Atlas: [Calliope](../model-families/energy/calliope.md) (model-as-data) ·
  [Digital Twins](../paradigms/algorithms/digital-twins.md)
