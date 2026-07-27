"""Additional-probe tests (Iter 50) — the generalization holds against famous macro relationships.

Okun's law (a very strong *coincident* correlation) and the yield curve (the classic *leading* recession
indicator) are both cut on the standard test — neither beats a mean-growth climatology for annual GDP
growth. This reinforces the project's central finding: reduced-form couplings on annual aggregate growth
almost never beat climatology; Energy⇄Inflation keeps only because energy is a large mechanical component of
the CPI.
"""

from __future__ import annotations

import pytest

from polyphony.data.loaders import has_additional_probes
from polyphony.experiments.additional_probes import (
    only_mechanical_component_keeps,
    run_okun_probe,
    run_yieldcurve_probe,
)

pytestmark = pytest.mark.skipif(not has_additional_probes(), reason="probe datasets not fetched")


def test_okun_is_strongly_correlated_but_cut():
    r = run_okun_probe()
    assert r.corr < -0.5  # Okun's law is a textbook-strong contemporaneous relationship…
    assert r.beats_baseline_frac <= 0.5  # …yet it does not beat climatology (coincident, not forecasting)
    assert r.verdict == "cut"


def test_yield_curve_is_cut_at_annual_resolution():
    r = run_yieldcurve_probe()
    assert r.kind == "leading"
    assert r.beats_baseline_frac <= 0.5  # a real leading indicator, but washed out at annual growth
    assert r.verdict == "cut"


def test_generalization_holds():
    # Neither a coincident nor a leading famous indicator beats climatology for annual growth.
    assert only_mechanical_component_keeps()
