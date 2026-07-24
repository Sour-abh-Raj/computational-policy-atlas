<!-- Polyphony / Atlas pull request -->

## What & why
<!-- One-paragraph summary. Link the issue(s) and ADR(s) this implements. -->

Closes #

## Type
- [ ] Atlas content (dossier / method / engine / matrix)
- [ ] Polyphony code (interface / engine / orchestrator / tournament)
- [ ] Validation / dataset / tournament result
- [ ] Docs / ADR only

## Evidence (competition, not thresholds)
<!-- If this adds a feature, coupling, or model: what did it BEAT, on what real data,
     out-of-sample? Link the leaderboard row. If it's a coupling, report synergy vs
     sum-of-parts. "No synergy found" is a valid, acceptable result — say so. -->
- Leaderboard row:
- Backtest / holdout result:
- Synergy vs decoupled baseline:
- Red-team attempts survived:

## Honesty & positioning
- [ ] Nothing here describes Polyphony as a "world model", oracle, or faithful replica.
- [ ] New factors/couplings/models cite **primary sources** and ship with a **test**.
- [ ] Contested values (welfare/equity/discounting) remain **inspectable dials**, not
      hard-coded constants.

## Checklist
- [ ] `python -m mkdocs build --strict` is green
- [ ] `docs/graph/graph.json` is valid and **0-dangling**
- [ ] `pytest` / `ruff` / `mypy` green (if code touched)
- [ ] ADR added/updated in `docs/decisions/` for any non-trivial decision
- [ ] `docs/polyphony/PROGRESS.md` updated with an `Iter NN` entry (if a loop iteration)
