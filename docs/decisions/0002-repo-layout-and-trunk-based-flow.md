# ADR-0002: Repo layout, docs surface, and the autonomous-loop trunk-based flow

- **Status:** Accepted
- **Date:** 2026-07-24
- **Deciders:** Polyphony build loop (Engineering Lab)
- **Phase:** 0

## Context

Polyphony must grow **beside** the completed atlas without disturbing it, keep MkDocs as
the living-docs surface with `mkdocs build --strict` **green on every commit**, and support
both an **autonomous build loop** and **human collaborators**. Two layout questions arise:

1. **Where does Polyphony's documentation live?** The brief refers to `polyphony/docs/`,
   but MkDocs builds only from the configured `docs_dir` (`docs/`). Docs physically outside
   `docs/` are not picked up by a plain `mkdocs build`, which would break strict mode or
   require an extra plugin.
2. **What is the git flow** for a solo autonomous loop that also wants a collaborator-ready
   PR process, given that pushing to `main` auto-deploys Pages?

## Decision

**Layout.** Split code from docs:

- **Code** → top-level Python package `polyphony/` (`polyphony/polyphony/…`, `pyproject.toml`,
  `tests/`). This is the "new top-level package" the brief asks for.
- **Docs** → `docs/polyphony/**` (inventory, blueprint, research, validation, leaderboard,
  PROGRESS, related-work), surfaced in the MkDocs nav. Living in `docs/` keeps strict-build
  green with **no extra plugin**. References to "`polyphony/docs/`" in the brief are honored
  as "the Polyphony docs section," now at `docs/polyphony/`.
- **ADRs** → `docs/decisions/**` (also MkDocs-visible).

**Flow.** Trunk-based on `main`, gated:

- The **autonomous loop** commits directly to `main` behind a **green gate**
  (`mkdocs build --strict` + `graph.json` 0-dangling + `pytest`/`ruff`/`mypy` once code
  exists), mirroring the atlas loop that produced 33 clean iterations. This keeps Pages
  continuously deployed and avoids self-review ceremony that adds no value with no second
  reviewer.
- **Human collaborators** use short-lived `feat|fix|docs/<slug>` branches + PRs with the
  repo templates and required checks (see [CONTRIBUTING](https://github.com/Sour-abh-Raj/computational-policy-atlas/blob/main/CONTRIBUTING.md)).

## Consequences

- Strict build stays green; no monorepo/multi-docs plugin needed.
- One obvious home for each artifact type (see the CONTRIBUTING table).
- The autonomous loop keeps momentum and a continuously live site.
- Trade-off: loop commits are **not** peer-reviewed pre-merge. Mitigated by the automated
  green gate, the append-only `PROGRESS.md`/`leaderboard.md` audit trail, and ADRs. If/when a
  second maintainer joins, flip the loop to the PR path (this ADR is the revisit trigger).

## Alternatives considered

- **`polyphony/docs/` + mkdocs-monorepo/multirepo plugin** — rejected for now: extra
  dependency and config surface for no reader-visible benefit; revisit if the package needs
  fully self-contained docs.
- **PR-per-iteration self-merge via `gh`** — rejected: ceremony without review value in a
  solo loop; retained as the documented path for humans.
- **A separate repository for Polyphony** — rejected: the brief wants the ensemble and the
  atlas to grow together and share the knowledge graph.

## Links

- [CONTRIBUTING.md](https://github.com/Sour-abh-Raj/computational-policy-atlas/blob/main/CONTRIBUTING.md) · [ADR-0001](0001-positioning-paradigm-plural-not-world-model.md)
- `.github/workflows/deploy.yml` (Pages deploy on push to `main`)
