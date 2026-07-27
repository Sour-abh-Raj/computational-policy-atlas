# Decision support — a worked example (the north star)

Everything in Polyphony exists to support one act: **a human choosing a policy with their eyes open.**
This page is the payoff — a worked **decision card** for a concrete question, assembled by
`experiments/decision_card.py`. Its job is deliberately *anti-oracular*: not to collapse the choice into
one confident number, but to make the **contested structure** of the choice legible.

> **Positioning (ADR-0001).** This is a paradigm-plural decision-support instrument that reports
> disagreement — never a world model, oracle, or faithful replica, and it does not "predict the future".
> The numbers below are illustrative reduced-form outputs; the *structure* is the contribution.

## The question

**What carbon price?** Candidates: 0, 50, 100, 200, 400 $/t. All five are on the Pareto frontier (each
buys lower climate risk at a rising consumption cost — a genuine efficiency ↔ safety trade-off), so none
dominates: the choice is genuinely a matter of **values and beliefs**, not arithmetic.

## 1. The recommendation depends on your values

Values are an **inspectable dial**, never hard-coded. Under three social welfare functions the
recommended policy is **not the same**:

| Value setting | Recommended carbon price |
|---|---|
| Utilitarian (sum of utilities) | **50 $/t** |
| Prioritarian (weight the worse-off) | **50 $/t** |
| Rawlsian + tail-risk averse (maximin + fear of climate tails) | **100 $/t** |

A welfare number that hid its weights would quietly pick one of these and call it "optimal". Polyphony
shows the fork instead: **caring more about the worst-off and about catastrophic tails moves the answer
up.** That is a value judgement for the human to own, not for the model to smuggle.

## 2. The paradigms disagree — and both answers are shown

On the key outcome, **GDP under a 100 $/t carbon price**, the two economic traditions give
**opposite-signed** answers:

| Voice | Paradigm | GDP (base = 100) |
|---|---|---|
| CGE | equilibrium (full-employment closure) | **88.0** — pricing *lowers* output |
| E3ME | disequilibrium (idle resources, green multiplier) | **108.0** — pricing *raises* output |

Disagreement index **D ≈ 0.10**. Polyphony **reports both and the D**, never a silent average — because
which paradigm is right is itself contested (it depends on whether the economy has slack), and averaging
would manufacture a false consensus. The honest read: *whether a carbon price helps or hurts GDP depends
on a modelling assumption you should choose consciously.*

### When does the disagreement matter? (a policy sweep)

Sweeping the carbon price shows the disagreement is not constant — it **activates with policy**
(`experiments/disagreement_study.py`):

| Carbon price | Disagreement index D | CGE GDP | E3ME GDP |
|---:|---:|---:|---:|
| 0 | 0.02 | 99.9 | 95.5 |
| 25 | **0.13** | 84.6 | 109.9 |
| 100 | 0.10 | 88.0 | 108.0 |
| 400 | 0.10 | 88.0 | 108.0 |

At **zero** policy the paradigms nearly agree (D ≈ 0.02); the moment a carbon price bites the split jumps
**~6×** (D ≈ 0.13), then plateaus once the energy transition completes. The decision-relevant lesson: **the
choice of economic paradigm matters most exactly where a real policy is contemplated** — so that is where
the instrument raises a flag, not where it hides one. Disagreement is a *signal about where your beliefs
are load-bearing*, not noise to be smoothed.

## 3. The validation status is disclosed

The recommendation leans on cross-domain couplings. Their **real-data verdict** (leaderboard Rounds 1–22)
is disclosed, not hidden:

| Coupling | Real-data verdict |
|---|---|
| **Macro⇄Health** (assimilation + no-lag) | ✅ **kept** — survives the full red-team round |
| Energy⇄climate⇄economy | ❌ cut — level artifact; genuinely cyclic |
| Real climate→GDP | ❌ cut — fails placebo (CO₂ *and* temperature) |
| Land⇄Climate⇄Food | ❌ cut — fails placebo + wrong sign on real yield |
| Urban⇄Transport⇄Energy⇄Health | ❌ cut — right sign but no skill above trend (confounded) |
| Water⇄Energy⇄Food (energy→food) | ❌ cut — corr +0.90 but no out-of-sample skill |
| Macro⇄Finance (spread→growth) | ❌ cut — right sign, beats placebo, but regime-dependent skill |

**Six of seven couplings failed real-data validation.** The card states this plainly, because a
decision-support tool that let you forget it would be lying by omission.

## The bottom line

> Recommendation: **a different policy depending on your values** — utilitarian/prioritarian favour
> 50 $/t, a Rawlsian + tail-averse view favours 100 $/t. On GDP the equilibrium and disequilibrium
> paradigms **disagree** (D ≈ 0.10); both answers are shown, not averaged. The ensemble leans on
> cross-domain couplings of which **six of seven failed real-data validation** — so this is
> **decision-support under deep uncertainty, NOT a forecast. Choose with your eyes open.**

That paragraph is the whole thesis of Polyphony in miniature: surface the **values**, surface the
**disagreement**, surface the **validation status** — and refuse to pretend a contested choice is a solved
one. Contrast this with a single "optimal carbon price = \$X" headline, and the difference between an
**oracle** and an **honest instrument** is exactly the three things this card refuses to hide.

*Reproduce:* `python -c "from polyphony.experiments.decision_card import build_decision_card as b;
print(b().honest_summary())"` (see also [validation & honesty](04-validation.md) and the
[leaderboard](leaderboard.md)).
