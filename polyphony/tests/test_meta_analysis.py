"""Meta-analysis tests (Iter 37) — the one criterion that separates keeps from cuts.

Of four plausible discriminators (right sign, beats-placebo, beats-naive, beats-baseline), only
**beats-baseline** perfectly partitions the two keeps from the seven cuts. The right sign is nearly useless
(most cuts have it); beating a placebo and beating naive each admit one false positive — Macro⇄Finance,
which clears all three yet is cut because it does not beat the honest baseline. That single computed fact is
the project's discipline in miniature.
"""

from __future__ import annotations

from polyphony.experiments.meta_analysis import (
    cut,
    false_positive_features,
    kept,
    perfect_separators,
)


def test_two_keeps_seven_cuts():
    assert len(kept()) == 2
    assert len(cut()) == 7


def test_only_beating_the_baseline_perfectly_separates():
    assert perfect_separators() == ("beats_baseline",)


def test_right_sign_is_a_poor_discriminator():
    fps = false_positive_features()
    # Most cut couplings have the assumed sign — sign alone tells you almost nothing.
    assert len(fps["right_sign"]) >= 5


def test_placebo_and_naive_each_admit_the_finance_false_positive():
    fps = false_positive_features()
    assert fps["beats_placebo"] == ("Macro⇄Finance",)
    assert fps["beats_naive"] == ("Macro⇄Finance",)


def test_finance_is_the_instructive_case():
    # Macro⇄Finance has the right sign, beats a placebo, and beats naive — yet is cut. The lesson: those
    # three are necessary-ish but not sufficient; only beating the honest baseline decides.
    fin = next(c for c in cut() if c.coupling == "Macro⇄Finance")
    assert fin.right_sign and fin.beats_placebo and fin.beats_naive
    assert not fin.beats_baseline
