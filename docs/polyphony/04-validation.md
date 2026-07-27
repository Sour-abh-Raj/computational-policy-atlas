# Phase 4 — Validation: what we can and cannot claim

Validation and honesty are the *product* (ADR-0001). This page states plainly what the Round 1
tournament establishes, what it does **not**, and how each open honesty-debt is tracked.

## What Round 1 establishes ✅

**The synergy-testing method works.** On data where the truth is known by construction, Polyphony:

- **detects synergy when the coupling is real** — coupled ensemble beats economy-only, Δ = **+2.22**,
  coupling **kept**; and
- **rejects synergy when it is spurious** — on the decoupled negative control, economy-only wins,
  Δ = **−1.73**, coupling **cut**.

This is the core contribution demonstrated end-to-end: a **falsifiable** coupling test that can say
"no synergy here" and act on it — exactly what the model-intercomparison and LLM-ABM literatures do
*not* operationalize ([related-work](related-work.md)).

It also exercises the full pipeline honestly: paradigm **routing**, **run-both** economics voices, a
**disagreement** report (the two closures disagree on GDP sign under policy), **provenance** on every
step, **time-blocked** splits (no leakage), and an **append-only leaderboard**.

## What Round 1 does NOT establish ❌ (stated plainly)

1. **No real-world predictive skill.** Both MASE values are **> 1** (worse than a naive random walk):
   the slice models are **uncalibrated reduced-form toys**, commensurable with the synthetic target
   only in shape, not level. We claim the **sign of synergy**, not forecast accuracy.
2. **The Round-1 target was synthetic.** Real historical data (issue #9) has since **landed** — World
   Bank GDP + OWID CO₂, 65 years — and the first real-data tournament (Round 10 below) returns an honest
   **cut** (the climate→GDP coupling fails a placebo control). The synthetic rounds validate the
   *method*; the real round supplies the first real-world verdict.
3. **A coupled DGP makes positive synergy "expected."** That is *why* the **negative control** is
   essential and reported alongside: it shows the method is not merely confirming its own generator —
   it **cuts** the coupling when the generator lacks it.
4. **Welfare/equity is not yet an engine.** The values dial (issue #4) is specified in the
   [blueprint §5](01-blueprint.md) but not yet computing Pareto frontiers/VoI; Round 1 reports GDP and
   emissions only, not distributional incidence.

## Calibration & disagreement (current state)

- **Calibration metrics** (CRPS/PIT) exist in `polyphony/eval` and are unit-tested, but the ensemble
  does not yet emit full predictive **distributions** per step, so they are not yet part of the
  scored tournament — next once parametric uncertainty is propagated.
- **Disagreement** is live: under a carbon price the equilibrium (CGE) and disequilibrium (E3ME)
  voices disagree on GDP with **opposite sign**, attributed to the **closure dial** — reported, never
  averaged away.

## Reproducing

```bash
pip install -e "polyphony[dev]"
cd polyphony && python -m pytest -q               # includes the two-regime tournament test
python -m polyphony.experiments.run_leaderboard   # regenerates docs/polyphony/leaderboard.json
```

## Red Team (Round 2) — the champion does **not** survive

The Round-1 champion was attacked with five stress tests (`polyphony/tournament/redteam.py`). It
survived distribution shift, a Lucas-critique policy-regime change, extreme dials, and noise-seed
instability — but was **broken by the naive-baseline attack**: its held-out **MASE ≈ 8 > 1**, i.e. it
is **worse than a naive random-walk forecast**. The apparent "synergy" is only relative to an
artificially weak economy-only baseline, not evidence of absolute skill.

This is the honest headline of the phase: **the synergy *method* is validated; the *champion* is
not.** The break is a hard gate — no skill claim, and no trusted champion, until calibration against
**real data** (issue #9) closes the gap. Exactly the kind of self-inflicted failure Polyphony is
built to surface rather than paper over.

## Scored tournament (CRPS/PIT) & calibration — Round 3

The tournament now scores the **parametric ensemble distribution** (`experiments/scored.py`), not just
a point track:

- **CRPS synergy holds on the proper score:** coupled ensemble **CRPS ≈ 7.9 < 10.2** economy-only ⇒ the
  coupling helps on a *probabilistic* metric, not only on point MASE.
- **PIT reveals mis-calibration:** mean PIT ≈ 0 — the ensemble sits **below** the target (biased low, and
  too narrow). Reported, not hidden; the distribution is not yet trustworthy even where the mean helps.
- **Calibration partly lifts the skill gate:** an affine level fit on the **train block only** drops the
  coupled mean's held-out **MASE from ≈ 8.0 to ≈ 0.61 — now below 1, i.e. it beats naive** on the
  synthetic target. Honest caveats: (a) **synthetic** data (real is #9); (b) calibration fixes *level*,
  not the mis-calibrated *distribution* (PIT); (c) a genuine skill claim still needs real data. So the
  Red-Team naive break is **partly addressed** (point skill after calibration) but **not closed**.

## Welfare frontier — values change the recommendation (the altruism payoff)

`experiments/welfare_frontier.py` maps coupled-ensemble outcomes across candidate carbon prices into
welfare `PolicyOutcome`s (a stylized 3-group consumption distribution net of a quadratic **abatement
cost**, plus emissions and welfare-equivalent climate risk), and ranks them under different value dials:

| Value stance | Recommended carbon price |
|--------------|--------------------------|
| Utilitarian | **50** |
| Prioritarian (η=1) | **50** |
| Rawlsian + tail-averse | **100** |

The recommendation **changes with the values**: a Rawlsian who is tail-averse to climate risk accepts a
higher near-term abatement cost for a safer world, where a utilitarian does not. This is the point of the
[Welfare/Equity engine](../patterns/welfare-equity-engine.md) — the choice of values is **surfaced**, not
hidden in a single welfare number. (Numbers are illustrative — reduced-form outcomes + a stylized
incidence/abatement assumption — but the *mechanism* is the deliverable.)

## Assimilation closes the r0-shift break — Round 6 (the digital-twin backbone)

The one outstanding red-team break was the Macro⇄Health `r0_shift`: the champion *assumed* a
reproduction number and lost badly when the world's r0 differed. The
[Data-Assimilation engine](../patterns/data-assimilation-engine.md) (`engines/assimilation.py`) fixes
it by **estimating r0 from the early observed dip on the train block** (grid least-squares over the
SIR) before forecasting — the model ⇄ **assimilation** ⇄ control limb of the digital twin. Re-running
the *same* attack **with** assimilation: r0 is recovered as **4.0** (exact), coupled **MASE 30.3 →
1.03**, synergy **Δ −26.2 → +3.09**, and `run_red_team(assimilate=True).survived` is **True**.

Honest caveats, stated: the data is still **synthetic** (real is #9); assimilation fixes the
**parameter**, not the coupling **structure**; and the grid estimator is a stand-in for a proper
Kalman/particle filter. But the claim is narrow and verified: *when the epidemic driver is read off the
data rather than assumed, the Macro⇄Health coupling survives the full red-team round it previously
failed.* The break was surfaced, not hidden — and closed by earning a new atlas engine (#18) that
itself carries a validation test (recovers a known r0 to within 0.5).

## A fair calibration cuts the energy synergy — Round 7 (a published "no synergy")

The energy champion's naive break (Round 2) had been *partly* addressed by calibrating the coupled
track (Round 3, MASE 8→0.61). Round 7 finishes the accounting honestly by calibrating **both sides**.
Two findings, reported together:

1. **Calibration closes the naive break.** `run_red_team(calibrate=True).survived == True` — the
   train-block-calibrated champion beats naive (MASE 0.60 < 1) and clears every other energy attack.
2. **But a *fair* calibration erases the energy synergy.** When the economy-only baseline gets its own
   train-block affine fit (`experiments.calibrated_synergy`), the coupled advantage collapses to
   **Δ ≈ −0.01** (mean +0.001 across 8 seeds, sign unstable) ⇒ **cut**. The Round-1 +2.22 was a **level
   artifact**, not structural skill.

This is a **falsifiable "no synergy" result**, published rather than buried — and it is the *point* of
the method. It **contrasts** with Macro⇄Health, whose coupling survives calibration **and** assimilation
with a real Δ>0: Polyphony's tournament separates a **real** coupling from a **spurious/level** one. No
energy skill claim survives; genuine energy synergy needs real data + richer structure (issue #9).

## The Land⇄Climate⇄Food coupling is real — Round 8 (the discrimination the method exists for)

Round 7 cut the energy synergy as a level artifact. Round 8 subjects the land coupling to the **same**
fair-calibration attack (`experiments/redteam_landfood.py`) and gets the **opposite** result:

- **level_artifact attack — SURVIVED.** After the land-only baseline gets its own train-block affine fit,
  the coupling *still* wins big: calibrated coupled MASE **2.87** vs land-only **18.1**, **Δ +15.2**
  (mean +15.5 across 8 seeds). The warming→food-price shape is genuinely informative; no calibration of a
  climate-blind baseline can fake it. **KEEP.**
- **policy_shift attack — SURVIVED.** When the world mitigates (cp=100) but the champion assumed none, the
  calibrated coupling still beats land-only (Δ +4.1).
- **naive_baseline (calibrated) — BROKE.** The calibrated champion's MASE **2.87 > 1**: still worse than
  naive. So the coupling is **real but not yet skillful** — no absolute skill claim.

This is the point of the whole apparatus: the tournament now **discriminates** three couplings by *why*
they do or don't earn their keep — energy **cut** (level artifact), land **kept but not skillful**,
Macro⇄Health **kept and skillful** (with assimilation). Honesty means reporting all three verdicts, not
just the flattering one.

## Why the land champion loses to naive — a precise attribution (Round 9)

The land coupling is real (Δ +15 survives a fair calibration) but the champion loses to naive. Iter 14
narrows *why* by elimination, and refuses the dishonest shortcut:

- **Not a parameter error.** `engines.assimilation.estimate_yield_sensitivity` recovers the true yield
  sensitivity (**0.1**) from the early food-price rise, across seeds — the driver was already right.
- **Not (only) the coupling lag.** The energy→climate→land chain is *acyclic*, so it can be resolved
  **contemporaneously** in topological order within the step ([ADR-0005](../decisions/0005-contemporaneous-resolution-of-acyclic-couplings.md),
  `Orchestrator.run(resolve="contemporaneous")`). This removes the spurious one-step-per-hop delay — the
  first-step price now moves with warming — yet the calibrated champion's **MASE stays ≈ 2.87**.
- **It is a structural voice/DGP mismatch.** With parameter and lag removed, the residual is the
  reduced-form energy/climate voices' **tail dynamics** diverging from the target — closable with **real
  data / richer voices (issue #9)**, not by tuning the toy voices to their own synthetic generator (that
  would be **dishonest skill-inflation**, and we refuse it).

This is the honesty machinery working as intended: rather than a single "it doesn't beat naive," we now
have an **attributed** diagnosis, and a general method improvement (contemporaneous resolution) banked
regardless. Contrast Macro⇄Health, where the driver *was* mis-estimated and assimilation closed the gap.

## Real data landed — and the first real-data verdict is an honest CUT (Round 10, issue #9)

The largest honesty debt is now **closed**: `polyphony/data/fetch_real.py` fetches **real** World Bank
world GDP + **OWID** global CO₂ (65 years), and `experiments/real_tournament.py` runs the first
tournament on non-synthetic data. The result is a model of the honesty the project is *for*:

- The CO₂ coupling **appears** to help (held-out MASE 3.20 → 1.49, Δ +1.70 over an economy-only trend).
- But it **fails a placebo control**: the same damage form driven by a meaningless **t^1.5** trend does
  as well or better (MASE 1.34). So the "synergy" is **spurious** — cumulative CO₂ is proxying the
  post-2008 growth slowdown, not carrying climate signal ⇒ **CUT**.
- Neither predictor **beats naive** (coupled MASE 1.49 > 1).

So on real aggregate data, this reduced-form climate→GDP coupling shows **no genuine predictive
synergy**. That is not a claim that climate doesn't affect the economy — only that a single global
CO₂→GDP damage regression adds no short-horizon skill over trend, and any claim it does must clear a
placebo. The placebo control is now a **standing requirement** for real-data couplings.

## Fourth coupling: the air-quality co-benefit passes the *synthetic* bar, not yet the real one (Round 14)

Honoring "scope is a floor", the ensemble extends into **Urban⇄Transport⇄Energy⇄Health** — the health
co-benefit of transport decarbonization (carbon price → less traffic → less PM2.5 → fewer premature
deaths). This is the most *intuitively compelling* coupling in the whole ensemble, which is exactly why
it gets no free pass. On a matched synthetic DGP the coupled ensemble survives the **same three-way
discrimination** every other domain faced: fair-calibrated Δ **+13.5** (so it is not the energy-style
level artifact that a calibrated baseline erases), correctly **cut** (Δ 0.00) on a flat negative control,
and the exposure **sign is as assumed** (corr(PM2.5, burden) +0.997 — more pollution, more mortality,
per the concentration–response literature). Two new voices (`transport`, `airhealth`) coupled
contemporaneously (acyclic chain; ADR-0005); atlas fed back with a **BenMAP-CE** dossier and graph nodes.

**The honest caveat, stated as plainly as the result:** this is a *synthetic* keep — machinery, not skill
— identical in status to Land⇄Climate⇄Food at Round 8, which a real-data placebo later **falsified**
(wrong sign, Round 13). So the co-benefit is **not** banked. It opens a **new honesty debt**: a real
PM2.5 + mortality series must beat both a no-exposure baseline and a placebo before any keep is believed.
The convergence status is therefore **reopened** until that real test resolves (keep or cut, both
publishable).

## The real air-quality co-benefit is CUT — right sign, no signal above trend (Round 15)

Iter 20 closes the gap Iter 19 opened. The co-benefits voice (more PM2.5 → higher mortality) is tested on
**real** World Bank world PM2.5 exposure vs an **independent** all-cause crude death rate (34 yrs,
1990–2023). The result is a CUT that is *scientifically the most interesting* of the four:

- **The outcome had to be chosen honestly.** The obvious outcome — GBD "mortality attributed to ambient
  PM2.5" — is **derived from** PM2.5 via a concentration-response function, so using it would be
  **circular**. We use all-cause mortality instead, which *can* fail the mechanism.
- **The sign is right.** corr(PM2.5, death rate) = **+0.35** — more pollution, more mortality, as the
  mechanism assumes (unlike land, where real yield rose *with* warming).
- **But there is no skill above a trend.** Fit on the train block, PM2.5's hazard coefficient **clamps to
  zero**: coupled MASE 1.781 = trend MASE 1.781, and a generic-time-trend **placebo does marginally
  better (1.768)**. The positive correlation is a **shared downward trend**, not PM2.5 carrying
  independent information about mortality deviations.

The lesson is precise and worth stating: a coupling can be **true micro-epidemiology** (cohort CRFs
genuinely identify PM2.5 mortality) and still earn **no predictive skill in an aggregate time series**,
because ecological confounding and a dominant demographic trend swamp it. Honesty means reporting that
the co-benefit is *real science* **and** *not a skillful aggregate predictor* — and refusing to bank the
intuitively-appealing coupling on a synthetic keep. Four couplings cut, each for a *different, named*
reason (level artifact; genuinely cyclic; wrong sign; confounded-away) — that catalogue of failure modes
is the instrument's real output.

## The real energy→food nexus leg is CUT — strong correlation, no forecast skill (Round 17)

Iter 22 closes the gap Iter 21 opened. A clean global water-scarcity driver isn't available annually, so
we test the nexus's data-rich **energy → food-price** leg (the pumping/fertilizer pass-through the
`nexusfood` voice carries) on real IMF food and energy price indices (34 yrs). The result is the fourth
*distinct* failure mode:

- **The sign and correlation are strong.** corr(energy, food) = **+0.90** contemporaneously — energy and
  food prices clearly co-move, and in the assumed direction.
- **But there is no out-of-sample skill.** A train-fit energy pass-through does **worse than a plain
  trend** (MASE 3.84 vs 3.27), worse than a placebo (3.74), and far worse than **naive** (all ≫ 1). Food
  prices are a volatile near-random-walk; a reduced-form pass-through fit on 1992–2015 does **not**
  extrapolate to the **2022 energy shock** (energy roughly doubled; food, buffered by inventories and
  substitution, rose far less).

The lesson, stated plainly: **a strong contemporaneous correlation is not a usable leading predictor.**
This is different from the co-benefit's "confounded-away" (there the correlation *vanished* on detrending;
here it stays strong but doesn't forecast). Honesty means reporting the +0.90 correlation **and** the CUT
in the same breath — the co-movement is real, the forecast skill is not. Five couplings cut, five *named*
failure modes (level artifact, cyclic, wrong sign, confounded-away, real-signal-no-skill); one kept.

## Walk-forward CV hardens (and corrects) the real-data verdicts (Round 18)

Each single-split verdict rests on one arbitrary train/test cut — and the nexus placebo comparison flipped
between two reasonable choices. Iter 23 re-runs every real coupling over an **expanding-window
walk-forward** and reports, across folds, how often it beats its baseline, a placebo, and naive. The
result is both a confirmation and a correction:

- **All four cuts hold** across folds — none is a single-split artifact.
- **But the *reason* is corrected.** climate→GDP and energy→food actually **beat the placebo in most
  folds**, so the earlier "fails placebo" attributions were partly split-dependent. What is invariant is
  that **none beats a naive random-walk in a majority of folds** (14%, 14%, 50%, 25%). On smooth aggregate
  series, a random walk is the honest baseline, and these reduced-form couplings do not clear it.

This is the validation discipline working on *itself*: a more robust method (walk-forward) revised a
conclusion reached by a weaker one (single split), and the revision is documented rather than hidden. The
standing lesson — *beat rivals AND a placebo AND naive on real data, or be cut* — is unchanged; walk-forward
just makes the "naive" clause the load-bearing one.

## Probabilistic scoring: inaccurate *and* overconfident (Round 19)

Point scores (MASE) miss whether a model's uncertainty is honest. Iter 24 turns each real coupling's point
forecast into a predictive distribution (point ± resampled train residuals) and scores CRPS + PIT against a
probabilistic naive. Two separate verdicts result:

- **Accuracy:** every coupling loses to naive on CRPS too (consistent with the point cuts).
- **Calibration:** every coupling is **grossly overconfident** — the PIT piles entirely at the tails (0%
  of values in the central half), so the predictive interval almost never contains the realised value.
  Out-of-sample error is dominated by **trend-extrapolation bias** the in-sample residual spread never
  saw, so train-calibrated bands are far too narrow out of sample.

This is the north star made quantitative: *foregrounding uncertainty* means reporting not just that a
forecast is wrong, but that its **confidence is unearned**. The honest remedy — predictive distributions
carrying parameter and structural uncertainty rather than only in-sample residuals — is now future work
motivated by a measured miscalibration, not a vibe.

## Honest uncertainty: calibration achievable, but blind to regime breaks (Round 20)

Round 19 found the couplings overconfident; Round 20 builds an honest predictive distribution — OOS bias
correction (walk-forward on train) + √h horizon-fanning bands — and asks whether it earns calibration.

- **Where the future resembles the past** (climate→GDP, warming→yield), it does: central PIT coverage
  rises from **0% to 47% / 100%**. A *calibrated* predictive distribution is achievable even for a
  coupling with **no point skill** — honest confidence, neither absent nor false.
- **Where the test block holds a regime break** (PM2.5→mortality's aging upturn; energy→food's 2022
  shock), it does **not**: historical residuals cannot insure against a structural break the backtest
  never saw. Calibration stays broken — and saying so plainly is the honest outcome.

The lesson for the instrument: honest uncertainty from history is a real, achievable virtue, but it is
**still blind to structural breaks**. Any claim of calibrated bands must carry that caveat — which is
precisely the kind of over-promise a single-confident-number simulator makes and this project refuses.

## Real Macro⇄Finance: the closest call, a narrow CUT (regime-dependent skill) (Round 22)

Iter 27 closes the gap on the coupling *most likely* to survive — the financial-conditions→output channel
(Gilchrist-Zakrajšek 2012). Tested as a real-time **nowcast**: the Baa−10Y credit spread vs annual real-GDP
growth (39 yrs), decided by walk-forward.

- **Strongest real signal yet:** corr(spread, growth) = **−0.61**, the right sign, robust across folds; the
  spread **beats a placebo in 80%** of folds and **naive in 60%** — genuine, non-spurious information.
- **But cut:** it beats a mean-growth **climatology in only 40%** of folds. The per-fold detail shows why —
  it **caught the 2008 and COVID collapses** but *hurt* in calm years and **overshot the 2022** spread
  spike that brought no recession. Its skill is **regime-dependent** (real near crises, noise otherwise),
  which an annual reduced-form linear coupling cannot turn into an unconditional edge.

The lesson is the project's thesis in one result: a channel with genuine, well-documented, right-signed
information is still **cut** because it does not robustly beat the honest baseline. **The bar does not bend
for a good story** — the sixth distinct named failure mode (regime-dependent skill), and the fifth real-data
cut under a placebo.

## Panel fixed effects confirm the modal cut with far more power (Round 25 / Iter 33)

The most common way a real-data coupling was cut is **confounded-away** — a strong correlation between two
trending series that vanishes once a trend is removed. On a single time series the placebo control catches
it; a **cross-country panel** catches it far more powerfully. Iter 33 assembles a **114-country × 32-year**
panel for carbon leakage and applies **two-way fixed effects** (removing every country's level *and* every
year's common shock — the shared global trend):

- **pooled** corr(openness, consumption/production ratio) = **+0.30** (the naive leakage story),
- **two-way-FE within** corr = **+0.025** — essentially zero,
- **attenuation = 92%**: almost the entire correlation was the shared trend, not a within-country mechanism.

This confirms the Iter-30 UK cut across 114 countries: trade openness has **no within-country effect** on
the emissions ratio once common year effects are removed. The fixed-effects estimator is itself validated
on synthetic panels (a pure confound demeans to ≈0; a real within-effect survives), so the method — not
just the datum — is trustworthy. Panel FE is now a reusable tool for separating **mechanism from shared
trend**, the sharpest instrument yet against the confounded-away trap.

**A contrasting case shows FE's own limits (Iter 34).** Applied to the co-benefit (PM2.5 → all-cause
mortality across **243 countries**), panel FE **cannot recover** the effect: the within-country correlation
is weak and even **wrong-signed** (−0.14). This is not because PM2.5 is harmless — it is because
**all-cause mortality is itself dominated by a confounded within-country trajectory** (the development and
aging transition), which fixed effects on the *driver* cannot remove. The honest lesson: panel FE isolates
a mechanism only when the **outcome** is not itself a confounded trend — a limit worth stating as plainly as
the leakage success, and a re-confirmation of Iter 20's point that aggregate all-cause mortality is the
wrong instrument for a real but small air-pollution effect (the properly-attributable outcome, GBD, is
circular).

## Honesty-debt register (tracked to close)

| Debt | Status | Tracked by |
|------|--------|-----------|
| Real historical datasets | ✅ **LANDED** — World Bank GDP + OWID CO₂ (65 yrs) fetched & merged; first real tournament run | issue #9 |
| Real-data climate→GDP synergy | ✅ **CUT** — beats trend (Δ+1.70) but **fails a placebo control** (t^1.5 does better); no genuine signal, loses to naive | issue #9 |
| Real-data cut robustness | ✅ **holds with OBSERVED temperature** (Hadley), not just the CO₂ proxy — coupled 1.07 vs placebo 0.87 ⇒ still cut; not a proxy artifact | issue #9 |
| Real Land⇄Climate⇄Food test | ✅ **CUT on real data** — real cereal yield vs Hadley temp: fails placebo (2.21 vs 2.20) **and wrong sign** (corr +0.90; Green-Revolution tech dominates). Synthetic-kept coupling falsified by real data | issue #6/#9 |
| Fourth synergy loop (breadth, #7) | ✅ **KEEP on synthetic** — Urban⇄Transport⇄Energy⇄Health co-benefit survives fair calibration (Δ +13.5) + correct sign; negative control cut. New voices `transport`+`airhealth`, BenMAP-CE dossier | issue #7 |
| Real Urban⇄Transport⇄Energy⇄Health test | ✅ **CUT on real data** — real PM2.5 vs independent all-cause death rate (34 yrs): **right sign** (+0.35) but PM2.5 adds no skill above trend (hazard k→0), fails placebo (1.781 vs 1.768). Ecological confounding, not a wrong mechanism; GBD outcome excluded as circular | issue #7-real |
| Convergence | ✅ **DONE (again)** — the Iter-19 scope extension is resolved: the fourth coupling is cut on real data (confounding). Every kept coupling survives its round; all four cuts have recorded, falsifiable reasons; no open improvable gap | — |
| Fifth synergy loop (breadth, #10) | ✅ **KEEP on synthetic** — Water⇄Energy⇄Food nexus survives fair calibration (Δ +99) + correct sign; negative control cut. New voices `water`+`nexusfood`, CLEWs dossier | issue #10 |
| Real Water⇄Energy⇄Food test | ✅ **CUT on real data** — energy→food leg (IMF indices, 34 yrs): corr +0.90 (right sign) but **no out-of-sample skill** (loses to trend/placebo/naive; 2022 energy shock doesn't pass through). Water-leg driver data-limited | issue #10-real |
| Convergence (after #10) | ✅ **DONE (again)** — nexus resolved on real data (fourth distinct failure mode). Every kept coupling survives its round; five cuts, five named failure modes; no open improvable gap | — |
| Split-robustness of real verdicts | ✅ **hardened by walk-forward CV** — all four real cuts hold across expanding-window folds; the robust common reason is **no skill vs naive** (single-split placebo attributions were partly split artifacts). `experiments/walkforward.py` | Round 18 |
| Uncertainty honesty of real forecasts | ✅ **measured (CRPS/PIT)** — real couplings are not only inaccurate but **grossly overconfident** (PIT at the tails, 0% central coverage): train-residual bands are far too narrow out-of-sample. Honest remedy (parameter/structural uncertainty) now motivated. `experiments/real_probabilistic.py` | Round 19 |
| Honest predictive bands | ✅ **calibration achievable, with a caveat** — OOS bias-correction + √h horizon-fanning bands lift central coverage 0%→47%/100% where the future resembles the past (climate→GDP, warming→yield), but **cannot** cover regime breaks (PM2.5 aging upturn; 2022 energy shock). Honest uncertainty from history is still blind to structural breaks. `experiments/honest_uncertainty.py` | Round 20 |
| Sixth synergy loop (breadth, #11) | ✅ **KEEP on synthetic** — Macro⇄Finance financial-accelerator survives fair calibration (Δ +2.74), correct sign (corr −0.999), and **beats naive**; decoupled control cut. New voice `finance`, EIRIN dossier + `d-finance` domain | issue #11 |
| Real Macro⇄Finance test | ✅ **CUT on real data (narrowest call)** — spread→growth nowcast (39 yrs): right sign (−0.61), beats placebo 80% + naive 60% of walk-forward folds, but not a mean-growth climatology (40%). **Regime-dependent skill** — real near crises, noise otherwise. The bar didn't bend for the best-motivated coupling. `experiments/real_finance_tournament.py` | issue #11-real |
| Convergence (after #11) | ✅ **DONE (again)** — Macro⇄Finance resolved on real data (sixth distinct failure mode). Every kept coupling survives its round; six cuts, six named failure modes; no open improvable gap | — |
| Seventh synergy loop (breadth, #12) | ✅ **KEEP on synthetic** — Trade⇄Emissions carbon leakage survives fair calibration (Δ +17.3) + correct sign; no-leakage control cut. New voice `trade`, MRIO dossier + `d-trade` domain | issue #12 |
| Real Trade⇄Emissions test | ⏳ **OPEN** — synthetic keep is machinery; needs a real production-vs-consumption CO₂ placebo test. Unusually clean target: OWID publishes the gap (`trade_co2`) directly | issue #12-real |
| Real Trade⇄Emissions test | ✅ **CUT on real data** — UK (textbook leakage): gap real (corr +0.81, right sign) but openness-leakage **confounded-away** — loses to a production-blind baseline in 0% of walk-forward folds. Openness↔gap is a shared trend, not independent info. `experiments/real_trade_tournament.py` | issue #12-real |
| Convergence (after #12) | ✅ **DONE (again)** — Trade⇄Emissions resolved on real data. Every kept coupling survives its round; **seven** cuts (six on real data), spanning the failure-mode catalogue; no open improvable gap | — |
| Panel fixed-effects validation | ✅ **confounded-away confirmed with power** — 114-country × 32-year carbon-leakage panel: pooled corr +0.30 → two-way-FE within corr +0.025 (**92% attenuation**). FE estimator validated on synthetic panels. Reusable tool vs the modal failure. `experiments/panel_validation.py` | Iter 33 |
| Panel FE — the method's own limit | ✅ **stated honestly** — on PM2.5 → all-cause mortality (243 countries) panel FE **cannot** recover the effect (within corr −0.14, wrong-signed): the *outcome* is dominated by a confounded within-country trajectory (development/aging). FE isolates a mechanism only when the outcome is clean | Iter 34 |
| Eighth coupling (#13) — a real KEEP | ✅ **Energy⇄Inflation kept on real data** — energy-price growth vs US CPI (32 yrs): corr +0.65, beats mean baseline/placebo/persistence/naive across walk-forward folds with the right sign. Method validated synthetically (kept when present, cut when absent). The bar rewards a skillful coupling as surely as it cuts hollow ones. FRB/US dossier. `experiments/inflation_tournament.py` | issue #13 |
| Ninth coupling (#14) — reverse causation | ✅ **Interest-Rate⇄Housing CUT** — a new failure mode: contemporaneous corr is **+0.38** (wrong sign; the Fed hikes into booms), and the correctly-signed lagged rate loses to housing **momentum** (persistence, 0% of folds). Policy endogeneity + momentum, cut for a principled reason. `experiments/real_housing_tournament.py` | issue #14 |
| Red-team of the Energy⇄Inflation keep | ✅ **survives** — dropping the most extreme energy year (2022), the pass-through still beats baseline + naive in every walk-forward fold (not a single-episode artifact); stable in the recent half; early half weaker (disclosed small-sample caveat). `experiments/redteam_inflation.py` | Iter 43 |
| Model calibration (real levels) | affine calibration now beats naive **on synthetic** (MASE 0.61); real-level calibration still pending | (opens when #9 lands) |
| Welfare/equity engine (values dial) | ✅ **built + integrated** — frontier over policies; recommendation changes with values | issue #4 |
| Predictive distributions → CRPS/PIT in tournament | ✅ **scored + calibrated** — `calibrate_ensemble` de-bias+widen ⇒ CRPS 7.9→0.44, **PIT 0.0→0.39** (near-uniform, synthetic) | blueprint §6 |
| Second synergy loop (breadth) | ✅ **Macro⇄Health (#8)**: keep in pandemic (coupled MASE 0.95 beats naive), cut on control | blueprint §7 |
| Third synergy loop (breadth) | ✅ **Land⇄Climate⇄Food (#6)**: keep under warming (+23.9), cut on flat control | blueprint §7 |
| Land⇄Climate⇄Food red team | ✅ **coupling REAL** — survives fair calibration (Δ +15.2) & policy shift; but champion **loses to naive** (MASE 2.87) ⇒ keep, no skill claim yet | issue #9 |
| Land naive-loss attribution | ✅ **diagnosed** — not parameter (assimilation recovers ys=0.1), not lag (contemporaneous resolution, ADR-0005); residual is voice/DGP structure ⇒ needs real data | issue #9 |
| Macro⇄Health red team | ✅ **r0_shift CLOSED by assimilation** — `estimate_r0` recovers r0=4.0 from the early dip; coupled MASE 30.3→**1.03**, Δ −26.2→**+3.09**; champion survives the full round (synthetic) | issue #1 |
| Contemporaneous resolution (acyclic slices) | ✅ **helps Macro⇄Health** (no-lag ⇒ MASE 0.95→**0.10**, Δ +8.92) and is **correctly refused for the cyclic energy slice** (guard raises) | ADR-0005 |
| Red-team attack on the champion | ✅ done — broken by naive; **resolved honestly**: calibration lets it beat naive but a *fair* baseline calibration cuts the energy synergy to Δ≈0 (level artifact) | blueprint §7 |
| Energy synergy after fair calibration | ✅ **cut** — coupled ties calibrated economy-only (Δ≈−0.01, 8 seeds); published "no synergy" (contrast Macro⇄Health keep) | issue #9 |

## Next

Because the champion loses to naive, the priority is **skill, not more couplings**: (1) land a real
dataset (#9) or a calibrated synthetic; (2) **calibrate** the reduced-form voices to real levels; (3)
re-run the tournament scoring **CRPS/PIT** (now available) alongside MASE; (4) only then re-arm the
Red Team. A coupling that cannot beat naive earns no place, however positive its synergy Δ.
