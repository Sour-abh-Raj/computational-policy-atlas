# Program Tracker — The Atlas of Computational Policy Simulation

Program-director view of scope, status, and the definition of done. Updated every
work iteration. (Site-facing status also lives at `docs/status.md`.)

## Definition of Done

The loop completes when **all** of the following hold:

- [ ] **D1 — Content depth.** Every model page promoted from *stub* to at least
      **Bronze** (all 18 dossier sections filled, concise but real). Flagships reach
      **Gold** (DICE-level rigor).
- [ ] **D2 — Synergy artifacts.** All 10 comparison matrices written as real chapters;
      the 15 architecture patterns detailed; the knowledge graph built as data
      (`graph.json`) + rendered views.
- [ ] **D3 — Build health.** `mkdocs build --strict` stays green (0 warnings) at every commit.
- [ ] **D4 — Deploy pipeline.** GitHub Actions workflow in place; site builds
      deploy-ready. ✅ (pipeline ready — see below)
- [x] **D5 — Published.** ✅ **LIVE** at
      <https://sour-abh-raj.github.io/computational-policy-atlas/> — repo
      `Sour-abh-Raj/computational-policy-atlas` (public). Owner authenticated gh once
      (`gh auth login --with-token`); the deploy workflow now auto-redeploys on push
      to `main`. **Owner reminder: rotate the token whenever you choose.**

## Maturity ladder (per page)

| Level | Bar |
|-------|-----|
| Stub | Positioning card + facts + TODO sections |
| **Bronze** | All 18 sections filled, concise, ≥3 primary citations |
| **Silver** | Equations/architecture diagrams, criticisms with citations |
| **Gold** | DICE-level: full math, Mermaid architecture, ecosystem, simulator lesson |

## Status board

| Family | Pages | Stub | Bronze+ | Gold |
|--------|------:|-----:|--------:|-----:|
| Climate IAM | 9 | 8 | 0 | 1 (DICE) |
| Energy | 5 | 3 | 0 | 2 (OSeMOSYS, TIMES) |
| Economics | 7 | 6 | 0 | 1 (CGE) |
| Transport | 4 | 4 | 0 | 0 |
| Urban | 3 | 3 | 0 | 0 |
| Agriculture | 4 | 4 | 0 | 0 |
| Water | 3 | 3 | 0 | 0 |
| Health | 3 | 3 | 0 | 0 |
| Frameworks | 7 | 7 | 0 | 0 |
| Methods/Algorithms | 8 | 8 | 0 | 0 |
| **Synergy** | matrices 2/10 · patterns 0/15 · graph 0/1 | | | |

## Iteration log

- **Iter 0** — Scaffold + DICE (Gold) + 52 stubs; strict build green (64 pages).
- **Iter 1** — Deploy pipeline (GitHub Actions), program tracker, OSeMOSYS → Gold
  (the bottom-up LP contrast to DICE).
- **Publish** — Repo created (public) and **site went live on GitHub Pages**:
  <https://sour-abh-raj.github.io/computational-policy-atlas/>. D5 cleared.
- **Iter 2** — TIMES → Gold (completes DICE↔OSeMOSYS↔TIMES optimization triangle);
  first synergy chapter **Optimization vs Simulation** (full comparative essay + matrix).
  Matrices 1/10. Pushed → auto-redeploys live.
- **Iter 3** — CGE → Gold (economics/equilibrium spine, Market Engine pattern); second
  matrix **Top-Down vs Bottom-Up** (energy-economy gap, hybrid synthesis). Matrices 2/10.

## Working order (program-director priority)

1. **Contrast pair**: OSeMOSYS + TIMES (bottom-up energy) vs DICE → unlocks the
   *IAM vs Energy* and *Optimization vs Simulation* matrices with real referents.
2. Equilibrium spine: CGE + DSGE + Input–Output → *ABM vs CGE*, *Equilibrium vs
   Disequilibrium* matrices.
3. Simulation spine: one ABM (MATSim/Covasim) + system dynamics → *ABM vs SD*.
4. Fill remaining stubs to Bronze, family by family.
5. Synergy layer: complete all matrices, detail all patterns, build the knowledge graph.
6. Signal D5 (publish) to the owner.
