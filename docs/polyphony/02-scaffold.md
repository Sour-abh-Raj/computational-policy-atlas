# Phase 2 — Scaffold (core + vertical slice)

The blueprint is now **running code**. This iteration builds `polyphony/`'s core ensemble
machinery and a first coupled vertical slice, all typed and tested green.

!!! success "Phase 2 acceptance gate — met"
    `pytest` (15 tests) · `ruff` · `mypy` · `tools/validate_graph.py` (0-dangling) ·
    `mkdocs build --strict` — all green. A coupled scenario runs end-to-end with provenance,
    routing, run-both, and disagreement reporting.

## What was built (`polyphony/polyphony/`)

**`core/`** — the paradigm-agnostic machinery:

- **`interface.py`** — the common `Model` `Protocol` (`state · step · dials · provenance`),
  structurally typed so adapters need not inherit; `conforms()` checks conformance.
- **`dials.py`** — `Dial`/`DialsSpec`: contested assumptions as **validated, inspectable**
  parameters (categorical or numeric), each carrying an atlas/citation provenance string.
- **`provenance.py`** — `Provenance`: model version, paradigm, solver, seed, dials, and a
  stable hash of inputs — recorded on **every** step so any number is reproducible.
- **`combiner.py`** — the heart: `combine()` returns a **`Disagreement`** (all answers kept,
  skill-weighted mean/sd, the normalized **disagreement index `D`**, spread) and
  `attribute_to_dial()` reports **what fraction of the disagreement a dial explains** — never a
  silent average (ADR-0004).
- **`orchestrator.py`** — couples voices under one clock via a **recursive (lagged, Gauss–Seidel)**
  bus; **routes** each quantity's coupled dynamics to a designated voice while **recording all
  voices'** outputs for the combiner. Validates unique names and routing.

**`models/`** — the first vertical slice (reduced-form, honestly-labeled toys; **not** the full
models, no fidelity claim):

- **`energy_lp.py`** — logit-smoothed least-cost technology choice; a carbon-price dial raises the
  fossil cost; provides `energy_cost`, `emissions`.
- **`econ_cge.py`** — equilibrium closure: costlier energy **lowers** GDP.
- **`econ_e3me.py`** — disequilibrium/demand-led closure: the same shock can **raise** GDP.

## The golden coupled scenario (`tests/test_slice.py`)

A carbon price flows `carbon_price → energy → energy_cost → economy → demand → energy …` around a
recursive loop. The two economics voices are **run both**; their GDP answers **disagree with
opposite sign** (CGE cost vs E3ME dividend), and the test asserts:

- the **disagreement `D` grows with the carbon price** (policy sharpens the split);
- the split is **attributed to the closure dial** (`explained_fraction > 0.9`);
- a higher carbon price **cuts emissions** (the energy voice responds);
- **provenance** is recorded for every voice every step.

This is Polyphony's thesis in miniature: *route the dynamics, run rival voices, and report the
disagreement with its driver* — not one confident number.

## CI (`.github/workflows/ci.yml`)

On every push/PR to `main`: graph 0-dangling gate → `ruff` → `mypy` → `pytest` → `mkdocs --strict`.

## Honest limits (recorded, not hidden)

The slice models are **reduced-form scaffolding**, not validated against data yet — this phase
proves the **machinery**, not predictive skill. Real backtesting, synergy measurement, and the
Red Team arrive in Phase 4; a faithful reduced-form **DICE (climate)** voice joins the slice next
iteration so the loop closes energy⇄economy⇄**climate**.

## Next (Iter 04 → toward Phase 3/4)

- Add a reduced-form **DICE** voice (capital + carbon stock + temperature) to close the
  energy⇄economy⇄climate loop; wire emissions → climate → damages → economy.
- Stand up the **data layer** (`data/loaders.py`, time-blocked `splits.py`) and **eval metrics**
  (`eval/metrics.py`: MAE/MASE, CRPS, calibration/PIT) so Phase 4 backtesting has a harness.
- Begin the **tournament** skeleton (`tournament/race.py`, `synergy.py`, `leaderboard.py`) with the
  first coupled-vs-sum-of-parts synergy measurement stub.
