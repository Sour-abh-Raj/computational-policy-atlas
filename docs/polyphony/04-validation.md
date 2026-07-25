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
2. **The target is synthetic.** Real historical data is **issue #9**; an automated fetch (World Bank
   GDP / OWID CO₂ / HadCRUT) is **currently blocked** (network egress unavailable to the loop — logged,
   worked around with the labelled synthetic series, and the loop continued, per the run contract).
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

## Honesty-debt register (tracked to close)

| Debt | Status | Tracked by |
|------|--------|-----------|
| Real historical datasets | network-blocked; synthetic fallback | issue #9 |
| Model calibration (real levels) | affine calibration now beats naive **on synthetic** (MASE 0.61); real-level calibration still pending | (opens when #9 lands) |
| Welfare/equity engine (values dial) | ✅ **built + integrated** — frontier over policies; recommendation changes with values | issue #4 |
| Predictive distributions → CRPS/PIT in tournament | ✅ **scored + calibrated** — `calibrate_ensemble` de-bias+widen ⇒ CRPS 7.9→0.44, **PIT 0.0→0.39** (near-uniform, synthetic) | blueprint §6 |
| Second synergy loop (breadth) | ✅ **Macro⇄Health (#8)**: keep in pandemic (coupled MASE 0.95 beats naive), cut on control | blueprint §7 |
| Red-team attack on the champion | ✅ done — broken by naive; **partly addressed** by calibration (synthetic only) | blueprint §7 |

## Next

Because the champion loses to naive, the priority is **skill, not more couplings**: (1) land a real
dataset (#9) or a calibrated synthetic; (2) **calibrate** the reduced-form voices to real levels; (3)
re-run the tournament scoring **CRPS/PIT** (now available) alongside MASE; (4) only then re-arm the
Red Team. A coupling that cannot beat naive earns no place, however positive its synergy Δ.
