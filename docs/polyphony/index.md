# Polyphony

**A paradigm-plural, adversarially-validated policy simulation ensemble** — built on the
[Atlas of Computational Policy Simulation](../index.md).

!!! abstract "What Polyphony is (and is not)"
    Polyphony couples the modeling traditions catalogued in the atlas into one executable
    system for policy testing, and **reports their disagreement as first-class signal**
    rather than averaging it into a single confident number. It is a **decision-support
    instrument**, not a "world model," an oracle, or a faithful replica of reality. See
    **[related work](related-work.md)** for how it differs from Destination Earth, the IAM
    family, and ML/LLM "world models," and **[ADR-0001](../decisions/0001-positioning-paradigm-plural-not-world-model.md)**
    for the positioning decision.

## The north star

Help humans choose better, more **altruistic** policies by simulating their consequences
as **accurately AND as honestly** as we can — foregrounding uncertainty, disagreement
between modeling traditions, and welfare/equity effects rather than hiding them behind one
number.

## The method (the actual contribution)

1. **Paradigm-plural** — rival traditions are kept as **distinct voices**.
2. **Disagreement is signal** — overlapping paradigms are run **both** and their **spread
   reported** (and it [*activates* with policy](decision-support.md#when-does-the-disagreement-matter-a-policy-sweep)).
3. **Adversarial selection** — features, couplings, and models survive by **beating rivals
   on real data** and **surviving red-team attack**, not by clearing a fixed threshold.
4. **Falsifiable synergy** — a coupling is kept only if the **coupled ensemble out-predicts
   the sum of isolated parts**; "no synergy" is an acceptable, publishable finding.
5. **Exposed values** — welfare/equity is an **inspectable multi-objective dial**.

## The result so far — the state of the ensemble

**Ten cross-domain couplings have been raced. Two earned their keep; eight were cut** — and every cut
names a **distinct, reusable failure mode** (seven modes in all). (See the
[failure-mode field guide](failure-modes.md) and the [leaderboard](leaderboard.md).)

| | Coupling | Verdict |
|---|---|---|
| ✅ | **Macro⇄Health** (epidemic → output; data-assimilation + no-lag) | **kept** — survives the full red-team round (MASE 0.10) |
| ✅ | **Energy⇄Inflation** (price pass-through) | **kept on real data** — beats every baseline + naive across walk-forward folds; forecasts ~1 year ahead |
| ❌ | Energy⇄climate⇄economy | cut — *level artifact* |
| ❌ | Real climate→GDP | cut — *confounded-away* (fails placebo) |
| ❌ | Land⇄Climate⇄Food | cut — *wrong sign* (real yield rose with warming) |
| ❌ | Urban⇄Transport⇄Energy⇄Health (co-benefit) | cut — *confounded-away* |
| ❌ | Water⇄Energy⇄Food (nexus) | cut — *real signal, no out-of-sample skill* |
| ❌ | Macro⇄Finance (spread→growth) | cut — *regime-dependent skill* |
| ❌ | Trade⇄Emissions (carbon leakage) | cut — *confounded-away* (panel FE, 114 countries, 92% attenuation) |
| ❌ | Interest-Rate⇄Housing | cut — *reverse causation* (the Fed hikes into booms) + momentum |

**Why so few keeps is the point.** The same strict bar that cut seven plausible couplings **rewarded**
the two that were genuinely skillful — a *discriminating* instrument, not a destructive one. And the
[meta-analysis](failure-modes.md#what-actually-separates-keeps-from-cuts-a-computed-answer) shows what
actually decides: of every plausible test, **only out-predicting the honest baseline** separates keeps from
cuts — the right sign, beating a placebo, even beating naive are each *necessary-ish but not sufficient*
(Macro⇄Finance clears all three yet is cut). A single-confident-number simulator would have reported ten
"insights"; Polyphony reports **two results and eight cautionary tales** — and the cautionary tales are the
more valuable half, because they are the ones you would otherwise have believed.

## How a coupling earns its keep (the bar)

A coupling is kept only if, on **real** data, it: has the **assumed sign**; beats a **placebo** (a
meaningless regressor); beats **naive** (a random walk); and — decisively — **out-predicts the honest
baseline** (the sum-of-parts / climatology) — all robustly under **walk-forward** cross-validation, not one
lucky split. Six validation methods enforce this: fair calibration · placebo control · walk-forward CV ·
CRPS/PIT probabilistic scoring · honest (bias-corrected, horizon-fanning) uncertainty · panel fixed effects.
See [validation & honesty](04-validation.md).

## Design thesis (inherited from the atlas)

> Make every contested assumption a **dial** · **route** each question to the paradigm where
> it is valid · where paradigms **overlap, run both and report the disagreement** · **expose
> contested values** rather than hard-coding them.

The payoff is the [worked decision card](decision-support.md): for "what carbon price?", it surfaces that
the recommendation **depends on your values**, that the **paradigms disagree** on GDP (and both answers are
shown, not averaged), and that **eight of ten couplings failed real-data validation** — decision-support
under deep uncertainty, *not* a forecast.

## Documents

| Page | What it is |
|------|-----------|
| [Failure modes](failure-modes.md) | Field guide: how couplings fail on real data (the honest product) |
| [Decision support](decision-support.md) | A worked decision card — the north star made concrete |
| [Validation & honesty](04-validation.md) | What is established, what is not, the honesty-debt register |
| [Leaderboard](leaderboard.md) | Every tournament round: contenders, metrics, why the verdict |
| [Related work](related-work.md) | Positioning vs DestinE, IAMs, ML/LLM world models |
| [Inventory](00-inventory.md) · [Blueprint](01-blueprint.md) · [Scaffold](02-scaffold.md) | The build: atlas raw material → architecture → package |
| [PROGRESS](PROGRESS.md) · [Decisions (ADRs)](../decisions/index.md) | The iteration log and the audit trail of design choices |

## Coverage & status

Ten atlas domains (climate · energy · economics · health · transport · agriculture · water · urban ·
**finance** · **trade**), a typed [knowledge graph](../graph/index.md) of 180 nodes / 480 edges (0-dangling),
and a Python package (`polyphony/`) with 130+ tests, all green under `ruff` · `mypy` · `mkdocs --strict`.

- **Phases 0–4 — done.** Inventory & positioning; blueprint; scaffold (interface, orchestrator, tournament);
  research (couplings raced); validation (real data, placebo, walk-forward, red-team).
- **Phase 5 — scale (ongoing).** Family by family and domain by domain, extending coverage while holding
  every addition to the same real-data bar — "scope is a floor," and each keep or cut is reported honestly.
