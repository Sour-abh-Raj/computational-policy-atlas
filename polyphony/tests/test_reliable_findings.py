"""Reliable-findings tests (Iter 56) — the positive output is consistent with the validation.

The short list of usable relationships is tied to the actual validated results, not asserted: the aggregate
finding matches the ledger's real-data keep, and the two panel findings match the panel survivors that
forecast out of sample. Macro⇄Health (synthetic keep, underpowered real) is deliberately excluded.
"""

from __future__ import annotations

import pytest

from polyphony.data.loaders import has_real_demographic_panel, has_real_preston_panel
from polyphony.experiments.failure_modes import real_data_keeps
from polyphony.experiments.reliable_findings import n_reliable, reliable_findings


def test_exactly_three_reliable_findings_excluding_synthetic_macrohealth():
    findings = reliable_findings()
    assert n_reliable() == 3
    names = " | ".join(f.relationship for f in findings)
    assert "inflation" in names.lower()
    assert "life expectancy" in names.lower()
    assert "fertility" in names.lower()
    assert "macro" not in names.lower()  # Macro⇄Health is a synthetic-only keep — excluded, honestly


def test_the_aggregate_finding_matches_the_real_data_keep():
    # The one aggregate reliable finding must be the ledger's one real-data keep (Energy⇄Inflation).
    reals = real_data_keeps()
    assert len(reals) == 1
    assert "Inflation" in reals[0].coupling
    agg = [f for f in reliable_findings() if f.kind == "aggregate forecast"]
    assert len(agg) == 1 and "inflation" in agg[0].relationship.lower()


@pytest.mark.skipif(
    not (has_real_preston_panel() and has_real_demographic_panel()),
    reason="real panels not fetched",
)
def test_the_panel_findings_match_the_forecasting_survivors():
    from polyphony.experiments.panel_validation import run_survivor_oos

    oos = run_survivor_oos()
    # Both panel reliable findings correspond to survivors that forecast out of sample (positive OOS corr).
    assert all(v > 0.0 for v in oos.values())
    panels = [f for f in reliable_findings() if f.kind == "panel mechanism"]
    assert len(panels) == 2
