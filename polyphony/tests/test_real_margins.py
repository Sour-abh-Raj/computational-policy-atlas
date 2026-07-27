"""Real-data baseline-margin tests (Iter 46) — the separator is clean on real evidence alone.

Strengthens the Iter-37 meta-analysis (whose boolean separator leaned partly on Macro⇄Health's synthetic
evidence): on the four couplings decided by walk-forward on real data, the keep beats its honest baseline in
a majority of folds and every cut does not — no synthetic evidence required.
"""

from __future__ import annotations

import pytest

from polyphony.data.loaders import (
    has_real_finance,
    has_real_housing,
    has_real_inflation,
    has_real_trade,
)
from polyphony.experiments.real_margins import real_baseline_margins, separator_holds_on_real_data

pytestmark = pytest.mark.skipif(
    not (has_real_inflation() and has_real_finance() and has_real_trade() and has_real_housing()),
    reason="real datasets not all fetched",
)


def test_keep_clears_the_baseline_line_and_cuts_do_not():
    margins = {m.coupling: m for m in real_baseline_margins()}
    # The real keep beats its baseline in a majority of folds…
    assert margins["Energy⇄Inflation"].kept
    assert margins["Energy⇄Inflation"].beats_baseline_frac > 0.5
    # …while every real cut falls below the line.
    for name in ("Macro⇄Finance", "Trade⇄Emissions", "Interest-Rate⇄Housing"):
        assert not margins[name].kept
        assert margins[name].beats_baseline_frac <= 0.5


def test_separator_holds_on_real_data_only():
    # No synthetic Macro⇄Health needed — the baseline-beating separator is clean on real evidence alone.
    assert separator_holds_on_real_data()
