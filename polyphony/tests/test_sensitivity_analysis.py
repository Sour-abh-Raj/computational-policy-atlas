"""Sensitivity-analysis tests (Iter 41) — which uncertainty is load-bearing?

The recommendation grid over (value setting × economic paradigm) shows, for the carbon-price question, that
varying **values** produces two distinct policies while varying the **paradigm** produces one — so the
load-bearing uncertainty is *ethical*, not *paradigmatic*. The card can then direct a decision-maker's
attention to the axis that actually moves the choice.
"""

from __future__ import annotations

from polyphony.experiments.sensitivity_analysis import run_sensitivity_analysis


def test_grid_covers_values_by_paradigms():
    s = run_sensitivity_analysis()
    assert len(s.grid) == 6  # 3 value settings × 2 paradigms
    assert all(name.startswith("cp=") for name in s.grid.values())


def test_values_are_load_bearing_paradigm_is_not():
    s = run_sensitivity_analysis()
    assert s.value_sensitivity == 2  # values move the choice between two policies
    assert s.paradigm_sensitivity == 1  # the paradigm does not move it at all
    assert s.dominant_uncertainty == "values (ethical)"
