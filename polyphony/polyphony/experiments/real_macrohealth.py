"""Why the real Macro⇄Health test is underpowered — demonstrated, not just asserted (Iter 47).

Macro⇄Health is kept on **synthetic** data (survives the red-team round, MASE 0.10), but its *real* test is
underpowered. This module shows *why*, structurally: to validate a coupling out of sample you must **learn
it on one occurrence and test it on another**, so you need at least **two independent pandemic episodes**.
The modern GDP era (post-war) contains essentially **one** pandemic that delivered a large output shock
through the health channel — **COVID-19 (2020–2023)** — a single contiguous block at the end of the sample.

With only **one** episode you cannot learn-on-one-and-test-on-another, so `identifiable_out_of_sample =
(episodes ≥ 2)` is False. (A multi-year episode can *straddle* one fold boundary — COVID's 2020 in a train
block, 2022 in the test block — but that is *within-episode* re-testing, not independent validation.) And a
second, independent piece of evidence makes it worse: at **annual** resolution the severity↔growth
correlation is **near zero** — 2021 had the *most* deaths *and* strong recovery growth, because the 2020
collapse came from lockdowns rather than deaths directly. So the coupling that is clean by construction on
synthetic data is **neither identifiable out of sample nor even strongly present in-sample** on real annual
data. Honest underpowering, made concrete.

Pandemic severity uses documented U.S. COVID-19 deaths (CDC, thousands); the *structural* conclusion (one
episode ⇒ not cross-validatable) does not depend on the exact figures.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from ..data.loaders import load_real_finance
from ..data.splits import walk_forward

# Documented U.S. COVID-19 deaths by year (CDC, thousands); zero in every non-pandemic year.
_COVID_DEATHS_THOUSANDS = {2020: 385.0, 2021: 475.0, 2022: 245.0, 2023: 76.0}


def _pandemic_severity(years: np.ndarray) -> np.ndarray:
    return np.array([_COVID_DEATHS_THOUSANDS.get(int(y), 0.0) for y in years], dtype=float)


def _count_episodes(severity: np.ndarray) -> int:
    """Number of contiguous nonzero runs — independent pandemic episodes."""
    episodes, in_run = 0, False
    for v in severity:
        if v > 0 and not in_run:
            episodes += 1
            in_run = True
        elif v == 0:
            in_run = False
    return episodes


@dataclass(frozen=True)
class MacroHealthPower:
    n_years: int
    n_pandemic_episodes: int
    folds_with_pandemic_in_train_and_test: int
    insample_corr: float  # corr(pandemic severity, GDP growth) — strongly negative, but one episode

    @property
    def identifiable_out_of_sample(self) -> bool:
        """Need ≥2 **independent** episodes to learn-on-one-and-test-on-another; one cannot be cross-validated
        (a single multi-year episode straddling a fold is within-episode re-testing, not validation)."""
        return self.n_pandemic_episodes >= 2

    @property
    def weak_in_sample(self) -> bool:
        """The annual severity↔growth relationship is itself near-zero (lockdown-vs-deaths timing confound)."""
        return abs(self.insample_corr) < 0.3

    @property
    def underpowered(self) -> bool:
        return not self.identifiable_out_of_sample


def demonstrate_underpower(horizon: int = 4) -> MacroHealthPower:
    ds = load_real_finance()  # reuse the committed real GDP series (annual real GDP)
    years = ds.column("year")
    gdp = ds.column("gdp")
    growth = np.diff(np.log(gdp)) * 100.0
    sev = _pandemic_severity(years[1:])  # align severity with the growth years
    n = len(growth)

    both = 0
    for sp in walk_forward(n, min_train=n // 2, horizon=horizon):
        in_train = np.any(sev[sp.train] > 0)
        in_test = np.any(sev[sp.test] > 0)
        both += int(in_train and in_test)

    corr = float(np.corrcoef(sev, growth)[0, 1]) if np.std(sev) > 0 else 0.0
    return MacroHealthPower(
        n_years=n,
        n_pandemic_episodes=_count_episodes(sev),
        folds_with_pandemic_in_train_and_test=both,
        insample_corr=corr,
    )
