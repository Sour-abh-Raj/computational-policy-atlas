"""Failure-mode catalogue tests (Iter 31) — the taxonomy is consistent AND tied to live results.

The catalogue is the honest product of the seven-domain sweep. These tests keep it truthful: every ledger
entry maps to a defined mode, the kept/cut counts match the record, and — where the real data is present —
the live tournament diagnostics actually match each coupling's classified failure mode (so the taxonomy is
validated against reproducible computation, not just prose).
"""

from __future__ import annotations

import pytest

from polyphony.data.loaders import (
    has_real_finance,
    has_real_food,
    has_real_nexus,
    has_real_trade,
)
from polyphony.experiments.failure_modes import (
    CATALOGUE,
    LEDGER,
    _MODE_KEYS,
    cut,
    kept,
    mode,
    modes_exemplified,
)


def test_catalogue_and_ledger_are_internally_consistent():
    assert len(CATALOGUE) == 6
    assert len({m.key for m in CATALOGUE}) == 6  # unique keys
    for c in LEDGER:
        assert c.mode in _MODE_KEYS, f"{c.coupling}: unknown mode {c.mode!r}"
    assert len(kept()) == 1  # Macro⇄Health
    assert len(cut()) == 7  # the rest
    # Every mode a cut coupling claims is a real, defined mode; at least five distinct modes are exemplified.
    assert modes_exemplified() <= {m.key for m in CATALOGUE}
    assert len(modes_exemplified()) >= 5


def test_every_mode_has_a_lesson_and_diagnostic():
    for m in CATALOGUE:
        assert m.definition and m.diagnostic and m.lesson


def test_confounded_away_is_the_most_common_mode():
    # Two real couplings (co-benefit, trade) plus climate→GDP land in "confounded-away" — the modal way a
    # plausible, right-signed coupling fails: a shared trend masquerading as a mechanism.
    confounded = [c for c in cut() if c.mode == "confounded-away"]
    assert len(confounded) >= 2


@pytest.mark.skipif(not has_real_food(), reason="real food dataset not fetched")
def test_land_live_diagnostic_matches_wrong_sign():
    from polyphony.experiments.real_land_tournament import run_real_land_tournament

    r = run_real_land_tournament()
    assert r.temp_yield_corr > 0.5 and not r.sign_as_assumed  # the defining diagnostic of "wrong-sign"
    assert mode("wrong-sign").key == "wrong-sign"


@pytest.mark.skipif(not has_real_nexus(), reason="real nexus dataset not fetched")
def test_nexus_live_diagnostic_matches_real_signal_no_skill():
    from polyphony.experiments.real_nexus_tournament import run_real_nexus_tournament

    r = run_real_nexus_tournament()
    assert r.energy_food_corr > 0.5 and not r.coupled_beats_naive  # strong signal, no skill


@pytest.mark.skipif(not (has_real_finance() and has_real_trade()), reason="real datasets not fetched")
def test_finance_and_trade_live_diagnostics_match_their_modes():
    from polyphony.experiments.real_finance_tournament import run_real_finance_tournament
    from polyphony.experiments.real_trade_tournament import run_real_trade_tournament

    fin = run_real_finance_tournament()
    assert fin.wf_beats_placebo > 0.5 and fin.robust_verdict() == "cut"  # regime-dependent skill
    tr = run_real_trade_tournament()
    assert tr.openness_ratio_corr > 0.5 and tr.robust_verdict() == "cut"  # confounded-away
