# How couplings fail on real data — a field guide

Polyphony tested **seven** cross-domain couplings. Each was *kept on synthetic data* (the machinery works)
and then faced a strict real-data bar: **beat a rival, a placebo, and naive; have the assumed sign; hold
up under walk-forward.** **One survived. Six were cut** — and the cuts are the product. Each names a
distinct, reusable way a plausible cross-sector story fails to earn its keep. This page is the honest
synthesis, generated from the tested catalogue in `experiments/failure_modes.py`.

> **Why a catalogue of failures is the point.** A tool that only ever reports successes is an oracle. An
> honest instrument reports *how* things fail, so the next modeller recognises the trap. Six of seven
> couplings here are cut — and naming the mechanism of each cut is worth more than a seventh confident
> number would have been.

## The ledger

| Coupling | Verdict | Failure mode | Decisive real number |
|---|---|---|---|
| **Macro⇄Health** | ✅ **kept** | — | survives full red-team round; assimilation + no-lag ⇒ MASE 0.10 |
| **Energy⇄Inflation** | ✅ **kept (real)** | — | corr +0.65; beats every baseline + naive across walk-forward folds |
| Energy⇄climate⇄economy | ❌ cut | Level artifact | fair-cal Δ ≈ −0.01 (also genuinely cyclic) |
| Real climate→GDP | ❌ cut | Confounded-away | fails placebo under both CO₂ and temperature |
| Land⇄Climate⇄Food | ❌ cut | Wrong sign | corr(temp, real yield) = **+0.90** (Green Revolution) |
| Urban⇄Transport⇄Energy⇄Health | ❌ cut | Confounded-away | PM2.5 corr +0.35 but hazard **k → 0**; ties placebo |
| Water⇄Energy⇄Food (energy→food) | ❌ cut | Real signal, no skill | corr **+0.90** but MASE ≫ 1 (loses to naive) |
| Macro⇄Finance (spread→growth) | ❌ cut | Regime-dependent skill | corr −0.61, beats placebo 80% but not climatology |
| Trade⇄Emissions (carbon leakage) | ❌ cut | Confounded-away | openness↔gap corr **+0.81** but loses to production-blind |
| Interest-Rate⇄Housing | ❌ cut | Reverse causation | contemp corr **+0.38** (Fed hikes into booms); lagged rate loses to momentum |

## The failure modes

### 1. Level artifact
A coupling can look enormously helpful just because it supplies a **level** the sum-of-parts baseline
lacks. *Diagnostic:* give the baseline its **own** train-block affine fit — the synergy Δ collapses to ≈0.
*Lesson:* a big raw synergy can be pure level-matching; calibrate both sides fairly before believing it.
(Energy⇄climate⇄economy, [Round 7](leaderboard.md).)

### 2. Genuinely cyclic
Some couplings are a **real feedback**, so a no-lag (contemporaneous) solve is inadmissible. *Diagnostic:*
the routing graph has a cycle; the topological solver refuses and lagging is required (ADR-0005).
*Lesson:* don't remove a coupling lag that encodes a real feedback just to buy apparent skill.

### 3. Wrong sign
A mechanism true at the micro level can have the **opposite sign** in aggregate data. *Diagnostic:*
corr(driver, target) contradicts the assumption. The land voice assumed warming lowers yield; real yield
rose **with** warming (corr +0.90) because the Green Revolution dominated. *Lesson:* lab/cohort truth is
not aggregate truth — confounders can flip the sign. (Land⇄Climate⇄Food, [Round 13](leaderboard.md).)

### 4. Confounded-away (shared trend) — *the modal failure*
Right sign, strong raw correlation — but the signal **vanishes once a trend is removed**. *Diagnostic:*
fails a placebo, or the fitted partial coefficient → 0, or it loses to a trend-scaled baseline. Three
couplings land here (climate→GDP, the PM2.5 co-benefit, and UK carbon leakage). *Lesson:* a strong
correlation between two trending series is usually **the trend, not the mechanism** — which is exactly why
the placebo control is non-negotiable. (Rounds [10](leaderboard.md), [15](leaderboard.md), [24](leaderboard.md).)
**Confirmed with power by a panel:** across a **114-country × 32-year** carbon-leakage panel, the pooled
openness↔gap correlation (+0.30) collapses to **+0.025 under two-way fixed effects** (92% attenuation) —
once every country's level and every year's common shock are removed, the mechanism is gone. Panel fixed
effects are the sharpest instrument against this trap ([validation](04-validation.md), `experiments/panel_validation.py`).

### 5. Real signal, no out-of-sample skill
Genuine, right-signed, **placebo-beating** information that still yields **no forecast skill**.
*Diagnostic:* beats a placebo but loses to a naive random walk (MASE ≥ 1). The real energy→food price
correlation is +0.90, yet a train-fit pass-through doesn't extrapolate to the 2022 shock. *Lesson:*
contemporaneous association is not a usable forecast; a volatile target can be near-unforecastable.
(Water⇄Energy⇄Food, [Round 17](leaderboard.md).)

### 6. Regime-dependent skill
Real skill in some **regimes** (e.g. crises) that doesn't beat an **unconditional** baseline. *Diagnostic:*
beats placebo + naive in most walk-forward folds, but not a climatology. The credit spread caught the 2008
and COVID growth collapses but hurt in calm years and overshot the 2022 spread spike. *Lesson:* skill
concentrated in rare regimes won't beat a mean on average — say so, don't claim an unconditional edge.
(Macro⇄Finance, [Round 22](leaderboard.md).)

### 7. Reverse causation / policy endogeneity
The lever **reacts to the target**, so the *contemporaneous* correlation has the **wrong sign**.
*Diagnostic:* contemporaneous corr opposite to the mechanism; even the correctly-signed lag loses to
momentum. Higher interest rates should slow house prices, but rates and house-price growth co-move
**positively** because the Fed hikes *into* booms; the correctly-signed lagged rate then can't beat housing
**momentum** (persistence). *Lesson:* when the policy responds to the outcome, the naive correlation is
backwards — use lags, and beware momentum baselines. (Interest-Rate⇄Housing, [Round 27](leaderboard.md).)

## What survived, and why it matters that the bar rewards it

**Two** couplings earn their keep — **but not with equal evidence**, and honesty means saying so.
**Macro⇄Health** — a health shock genuinely drags output, the data-assimilation engine recovers the
reproduction number, and the contemporaneous solve sharpens it to MASE 0.10, surviving the full red-team
round — **on synthetic data**; its *real* test is **underpowered** (≈1 pandemic event, no way to validate
out-of-sample). **Energy⇄Inflation** — energy-price growth beats every baseline, persistence, and naive
across walk-forward folds **on real data** (corr +0.65) and survives a real red-team (drop the 2022 spike,
it holds): the **only keep validated on real data** (`real_data_keeps()`). So "two keeps" is really *one
real-data keep and one synthetic-plus-underpowered-real keep* — the ledger records the difference rather
than flattening it, because a synthetic keep is a hypothesis, not a result. Those two successes, standing
against **eight** named failures, are the honest yield of
paradigm-plural, adversarially-validated simulation. The point is not that the instrument is destructive:
the same strict bar that cut six plausible couplings **rewarded** the two that were genuinely skillful — a
*discriminating* instrument. A single-confident-number simulator would have reported nine "insights";
Polyphony reports two results and eight cautionary tales — and the cautionary tales are the more valuable
half, because they are the ones you would otherwise have believed.

## The central generalization (what all of this adds up to)

After ten couplings plus two celebrated extra probes, a single empirical regularity has emerged and held
every time:

> **Reduced-form couplings on annual aggregate targets almost never beat a climatology baseline.**

The two probes are the sharpest test of it (`experiments/additional_probes.py`): **Okun's law**
(Δunemployment↔growth, corr **−0.81** — one of the strongest correlations in macro) is *cut*, because
unemployment is **coincident** with growth, not a forecast of it; and the **yield curve** (the classic
*leading* recession indicator) is *cut* too, because its ~1-year lead is washed out at annual resolution.
Neither a famously strong *coincident* relationship nor a famously reliable *leading* one clears the bar.

The **one** exception — **Energy⇄Inflation** — is the exception that proves the rule: it keeps not because
it forecasts an unforecastable series, but because energy is a **large, mechanical, contemporaneous
component of the CPI**. So the honest one-line summary of the whole exercise: *aggregate outcomes are hard
to beat a climatology on; the couplings that look like they should help usually don't; and the rare one
that does, does so for a boringly mechanical reason.* Reporting that plainly is worth more than a shelf of
plausible-but-hollow "insights."

**The generalization has a boundary — and it is about *aggregate forecasting*, not "nothing works".** The
instrument is not a nihilism machine. Move from forecasting an aggregate time series to a **cross-country
panel** with a genuine within-unit mechanism, and couplings *do* survive. The panel domain has its own
honest taxonomy — **two survivors and two cut**, mirroring the aggregate story (`run_all_panels`):

| Panel coupling (252 countries) | pooled | two-way-FE within | verdict |
|---|---:|---:|---|
| **Income → life expectancy** (Preston) | +0.79 | **+0.13** | survives |
| **Income → fertility** (demographic transition) | −0.71 | **−0.11** | survives |
| Trade openness → leakage gap | +0.30 | +0.02 | cut (confounded-away) |
| PM2.5 → all-cause mortality | −0.00 | −0.14 | cut (outcome confounded) |

The *same* fixed-effects tool passes the two real within-country mechanisms and cuts the two confounded
ones. So the failure of aggregate couplings is a statement about **the difficulty of beating climatology on
aggregate time series**, not about the instrument's ability to find real structure when it is there — and
the panel taxonomy is the mirror image of the aggregate one: *real mechanisms survive; confounds don't.*

## What actually separates keeps from cuts (a computed answer)

Given two keeps and seven cuts, *which property* decides? Scoring every coupling on four plausible
discriminators (`experiments/meta_analysis.py`) gives a sharp, slightly surprising answer:

| Discriminator | Perfectly separates keep/cut? | False positives (cut couplings that have it) |
|---|---|---|
| right sign of the real correlation | ❌ | **7 of 8 cuts** — sign alone tells you almost nothing |
| beats a placebo | ❌ | Macro⇄Finance |
| beats naive (random walk) | ❌ | Macro⇄Finance |
| **beats the honest baseline** (sum-of-parts / climatology) | ✅ | — |

**Only beating the honest baseline perfectly separates the real couplings from the hollow ones.** The
decisive teaching case is **Macro⇄Finance**: it has the right sign, beats a placebo, *and* beats naive in a
majority of folds — yet is cut, because its (regime-dependent) skill does not beat the mean-growth
baseline. So a strong correlation, the right sign, beating a placebo, even beating naive are each
**necessary-ish but not sufficient**. The one criterion that decides is **out-predicting the honest
baseline** — the whole project's discipline compressed into a single computed fact.

!!! warning "Honest caveat on the separator"
    One of the two "beats-baseline" keeps — **Macro⇄Health** — clears the baseline on **synthetic** data
    (its real test is underpowered), so the boolean perfect-separator claim rests on *real* evidence for
    Energy⇄Inflation and the seven real cuts, plus *synthetic* evidence for Macro⇄Health. We flag the mixed
    footing rather than hide it.

    **And we checked it holds on real evidence alone.** A **numeric** version
    (`experiments/real_margins.py`) computes, for the four couplings decided by walk-forward *on real data*,
    the fraction of folds beating the honest baseline: **Energy⇄Inflation (keep) 100%**, Macro⇄Finance 40%,
    Trade⇄Emissions 0%, Interest-Rate⇄Housing 0%. The keep clears the 50% line; every cut falls below it —
    so the separator is clean **without** the synthetic Macro⇄Health evidence.

*Reproduce:* `python -c "from polyphony.experiments.failure_modes import LEDGER; [print(c.mode, c.coupling)
for c in LEDGER]"` and `from polyphony.experiments.meta_analysis import perfect_separators; print(perfect_separators())`.
Each live diagnostic is asserted in `tests/test_failure_modes.py`, `tests/test_meta_analysis.py`, and the
per-domain `tests/test_real_*_tournament.py`. See also the [leaderboard](leaderboard.md) and
[validation & honesty](04-validation.md).
