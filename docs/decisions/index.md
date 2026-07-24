# Architecture Decision Records (ADRs)

Non-trivial decisions in Polyphony — a coupling, a method, a dataset, a tech-stack pick,
a positioning claim — are recorded here as short, dated, immutable **Architecture
Decision Records**. New decisions that supersede an old one link back to it; we never
silently rewrite history.

Format: [Michael Nygard's ADR style](https://github.com/joelparkerhenderson/architecture-decision-record)
— see the [template](adr-template.md).

## Log

| # | Title | Status |
|---|-------|--------|
| [0001](0001-positioning-paradigm-plural-not-world-model.md) | Positioning: a paradigm-plural ensemble, **not** a world model | Accepted |
| [0002](0002-repo-layout-and-trunk-based-flow.md) | Repo layout, docs surface, and the autonomous-loop trunk-based flow | Accepted |
| [0003](0003-tech-stack.md) | Tech stack for the Polyphony package | Accepted |
| [0004](0004-disagreement-preservation-vs-bma.md) | Disagreement-preservation as default combiner; BMA as a challenger | Accepted |

!!! note "Why ADRs matter here"
    Polyphony selects by **adversarial competition**, extends the atlas freely, and makes
    strong honesty commitments. ADRs are how a collaborator (or a future iteration of the
    loop) can reconstruct *why* a coupling, model, or method was chosen or cut — the audit
    trail behind the leaderboard.
