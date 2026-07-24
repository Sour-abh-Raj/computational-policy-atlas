# Contributing

This repository hosts two things that grow together:

1. **The Atlas of Computational Policy Simulation** (`docs/`) — a textbook-quality
   knowledge base of ~50 policy-simulation models, 14 method pages, 16 architecture
   "engine" patterns, comparative matrices, and a typed knowledge graph.
2. **Polyphony** (`polyphony/` code, `docs/polyphony/` docs) — a paradigm-plural,
   adversarially-validated policy-simulation **ensemble** built on the atlas.

Please read [`docs/polyphony/related-work.md`](docs/polyphony/related-work.md) before
contributing to Polyphony: it states plainly what Polyphony **is and is not** (it is a
decision-support ensemble that reports disagreement, **not** a "world model").

## Ground rules

- **Cite primary sources.** Every new model/factor/coupling needs a cited literature
  justification **and** a test. No unsupported inventions. Follow the atlas's citation
  discipline (link to the relevant dossier/pattern/graph node; cite external primaries
  when you go beyond them).
- **Decisions are ADRs.** Non-trivial choices (a coupling, a method, a dataset, a
  tech-stack pick) get an Architecture Decision Record in
  [`docs/decisions/`](docs/decisions/) using the [template](docs/decisions/adr-template.md).
- **Competition, not thresholds.** Features, couplings, and models are accepted by
  **winning a tournament against rivals on real data**, not by clearing a fixed number.
  Record every contest — contenders, metrics, why the winner won — in
  [`docs/polyphony/leaderboard.md`](docs/polyphony/leaderboard.md).
- **Keep the build green.** `python -m mkdocs build --strict` must pass and
  `docs/graph/graph.json` must stay valid and **0-dangling** on every commit. The
  Polyphony package must stay typed with tests green (`pytest`, `ruff`, `mypy`).
- **Never commit secrets.** No tokens/credentials. GitHub Pages deploy is
  credential-gated (`gh auth login` by the repo owner). `.gitignore` excludes
  `*.token` and `secrets.*`.

## Branching & review

- **`main`** is always deployable; pushing to it auto-deploys the site
  (`.github/workflows/deploy.yml`).
- **Human contributors**: branch `feat/<slug>`, `fix/<slug>`, or `docs/<slug>`; open a
  PR using the [PR template](.github/pull_request_template.md); require green checks and
  one review before merge.
- **The autonomous agent loop** (Polyphony's build loop) commits to `main` behind a
  green strict-build + graph-validation gate, appending an `Iter NN` entry to
  [`docs/polyphony/PROGRESS.md`](docs/polyphony/PROGRESS.md) each iteration. Rationale and
  scope of this exception are recorded in
  [ADR-0002](docs/decisions/0002-repo-layout-and-trunk-based-flow.md).

## Local setup

```bash
pip install -r requirements.txt          # docs toolchain (mkdocs-material)
pip install -e "polyphony[dev]"          # the Polyphony package + dev tools (Phase 2+)
python -m mkdocs build --strict          # must be clean
python tools/validate_graph.py           # graph 0-dangling check (added Phase 0/2)
```

## Where to put things

| You are adding… | Put it in… |
|-----------------|-----------|
| A new model dossier / method / engine page | `docs/model-families/**`, `docs/paradigms/**`, `docs/patterns/**` (+ `graph.json` node/edges) |
| A Polyphony design decision | `docs/decisions/NNNN-*.md` (ADR) |
| A model adapter, engine impl, orchestrator code | `polyphony/polyphony/**` (+ tests) |
| A tournament / validation result | `docs/polyphony/leaderboard.md` + `docs/polyphony/04-validation.md` |
| A synergy hypothesis or a gap | a GitHub issue (templates in `.github/ISSUE_TEMPLATE/`) |
