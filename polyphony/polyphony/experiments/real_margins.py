"""Real-data baseline margins (Iter 46) — the keeps-vs-cuts separator, on real evidence alone.

The Iter-37 meta-analysis found that **only out-predicting the honest baseline** separates keeps from cuts,
but that boolean claim leaned partly on Macro⇄Health's *synthetic* baseline-beating (Iter-45 caveat). This
module strengthens it to a **numeric** separator computed on the couplings decided by walk-forward **on real
data**: the fraction of folds in which each coupling beats its own honest baseline (the mean/climatology, or
— for a momentum-dominated target — persistence). The real keep clears the 50% line; every real cut falls
below it. The separator is clean on real evidence alone.
"""

from __future__ import annotations

from dataclasses import dataclass

from .inflation_tournament import run_real_inflation_tournament
from .real_finance_tournament import run_real_finance_tournament
from .real_housing_tournament import run_real_housing_tournament
from .real_trade_tournament import run_real_trade_tournament


@dataclass(frozen=True)
class RealMargin:
    coupling: str
    kept: bool
    baseline: str
    beats_baseline_frac: float  # fraction of walk-forward folds beating the honest baseline


def real_baseline_margins() -> tuple[RealMargin, ...]:
    """The four real, walk-forward-decided couplings and how often each beats its honest baseline."""
    inf = run_real_inflation_tournament()
    fin = run_real_finance_tournament()
    tr = run_real_trade_tournament()
    ho = run_real_housing_tournament()
    return (
        RealMargin("Energy⇄Inflation", True, "mean-inflation climatology", inf.wf_beats_baseline),
        RealMargin("Macro⇄Finance", False, "mean-growth climatology", fin.wf_beats_baseline),
        RealMargin("Trade⇄Emissions", False, "production-scaled baseline", tr.wf_beats_blind),
        RealMargin("Interest-Rate⇄Housing", False, "persistence (momentum)", ho.wf_beats_persistence),
    )


def separator_holds_on_real_data(threshold: float = 0.5) -> bool:
    """True if every kept coupling beats its baseline in > ``threshold`` of folds and every cut does not —
    i.e. the baseline-beating separator is clean using **real evidence only** (no synthetic Macro⇄Health)."""
    margins = real_baseline_margins()
    return all((m.beats_baseline_frac > threshold) == m.kept for m in margins)
