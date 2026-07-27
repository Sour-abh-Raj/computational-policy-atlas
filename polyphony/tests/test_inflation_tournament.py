"""Energy⇄Inflation tests (issue #13) — the first clean real-data KEEP.

The method is validated on synthetic data (a real pass-through is kept; an independent control is cut), and
on real FRED data (energy price index + US CPI) energy-price growth beats a mean baseline, a placebo,
persistence, and naive across walk-forward folds with the assumed positive sign — a genuine keep, showing
the strict bar rewards a skillful coupling as surely as it cuts a hollow one.
"""

from __future__ import annotations

import pytest

from polyphony.data.loaders import has_real_inflation, load_real_inflation
from polyphony.experiments.inflation_tournament import run_real_inflation_tournament, run_synthetic_check


def test_synthetic_passthrough_is_kept_and_control_is_cut():
    assert run_synthetic_check(present=True).robust_verdict() == "keep"
    assert run_synthetic_check(present=False).robust_verdict() == "cut"


@pytest.mark.skipif(not has_real_inflation(), reason="real inflation dataset not fetched")
def test_real_inflation_dataset_loads_and_is_not_synthetic():
    ds = load_real_inflation()
    assert not ds.synthetic
    assert len(ds) >= 20
    assert "energy" in ds.series and "cpi" in ds.series


@pytest.mark.skipif(not has_real_inflation(), reason="real inflation dataset not fetched")
def test_real_energy_inflation_is_a_robust_keep():
    r = run_real_inflation_tournament()
    assert r.corr > 0.5 and r.sign_as_assumed  # strong, right-signed pass-through
    # Beats every baseline in a majority of walk-forward folds — a genuine, skillful coupling.
    assert r.wf_beats_baseline > 0.5
    assert r.wf_beats_placebo > 0.5
    assert r.wf_beats_persistence > 0.5
    assert r.wf_beats_naive > 0.5
    assert r.robust_verdict() == "keep"
