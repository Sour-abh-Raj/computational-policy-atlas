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
| Energy⇄climate⇄economy | ❌ cut | Level artifact | fair-cal Δ ≈ −0.01 (also genuinely cyclic) |
| Real climate→GDP | ❌ cut | Confounded-away | fails placebo under both CO₂ and temperature |
| Land⇄Climate⇄Food | ❌ cut | Wrong sign | corr(temp, real yield) = **+0.90** (Green Revolution) |
| Urban⇄Transport⇄Energy⇄Health | ❌ cut | Confounded-away | PM2.5 corr +0.35 but hazard **k → 0**; ties placebo |
| Water⇄Energy⇄Food (energy→food) | ❌ cut | Real signal, no skill | corr **+0.90** but MASE ≫ 1 (loses to naive) |
| Macro⇄Finance (spread→growth) | ❌ cut | Regime-dependent skill | corr −0.61, beats placebo 80% but not climatology |
| Trade⇄Emissions (carbon leakage) | ❌ cut | Confounded-away | openness↔gap corr **+0.81** but loses to production-blind |

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

## What survived, and why it matters that little did

**Macro⇄Health** is the one coupling that earns its keep — a health shock genuinely drags output, the
data-assimilation engine recovers the reproduction number, and the contemporaneous solve sharpens it to
MASE 0.10, surviving the full red-team round. That **one** success, standing against **six** named
failures, is the honest yield of paradigm-plural, adversarially-validated simulation. A single-confident-
number simulator would have reported seven "insights"; Polyphony reports one result and six cautionary
tales — and the cautionary tales are the more valuable half, because they are the ones you would otherwise
have believed.

*Reproduce:* `python -c "from polyphony.experiments.failure_modes import LEDGER; [print(c.mode, c.coupling)
for c in LEDGER]"`. Each live diagnostic is asserted in `tests/test_failure_modes.py` and the per-domain
`tests/test_real_*_tournament.py`. See also the [leaderboard](leaderboard.md) and
[validation & honesty](04-validation.md).
