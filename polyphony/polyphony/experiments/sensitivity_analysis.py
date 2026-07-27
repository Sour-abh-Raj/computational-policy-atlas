"""Sensitivity analysis — which uncertainty is load-bearing? (Iter 41)

A policy recommendation rests on two very different kinds of uncertainty: **ethical** (which social welfare
function — utilitarian, prioritarian, Rawlsian) and **positive/paradigmatic** (which economic worldview —
equilibrium vs disequilibrium). A decision-maker's scarce attention should go to whichever one actually
*moves the choice*. This builds the full **recommendation grid** over (value setting × paradigm) and reports
how many distinct policies each axis produces — so the card can say not just "the models disagree" but
"**for this question, your *values* decide and the economic paradigm does not**" (or vice-versa).

For the carbon-price question the answer is clear and useful: the recommendation spans two policies across
value settings but is invariant to the paradigm — the **load-bearing uncertainty is ethical, not
paradigmatic**. That is a different, sharper honesty than a bare disagreement index.
"""

from __future__ import annotations

from dataclasses import dataclass

from .welfare_frontier import frontier_and_recommendations

_VALUE_SETTINGS = ("utilitarian", "prioritarian", "rawlsian_tail_averse")
_PARADIGMS = ("equilibrium", "disequilibrium")


@dataclass(frozen=True)
class SensitivityResult:
    grid: dict[tuple[str, str], str]  # (value_setting, paradigm) -> recommended policy name

    @property
    def value_sensitivity(self) -> int:
        """Most distinct recommendations produced by varying **values** (holding a paradigm fixed)."""
        return max(
            len({self.grid[(v, p)] for v in _VALUE_SETTINGS}) for p in _PARADIGMS
        )

    @property
    def paradigm_sensitivity(self) -> int:
        """Most distinct recommendations produced by varying the **paradigm** (holding values fixed)."""
        return max(
            len({self.grid[(v, p)] for p in _PARADIGMS}) for v in _VALUE_SETTINGS
        )

    @property
    def dominant_uncertainty(self) -> str:
        if self.value_sensitivity > self.paradigm_sensitivity:
            return "values (ethical)"
        if self.paradigm_sensitivity > self.value_sensitivity:
            return "paradigm (positive)"
        return "both equally" if self.value_sensitivity > 1 else "neither (robust choice)"


def run_sensitivity_analysis(carbon_prices: tuple[float, ...] = (0.0, 50.0, 100.0, 200.0, 400.0)) -> SensitivityResult:
    prices = list(carbon_prices)
    grid: dict[tuple[str, str], str] = {}
    for p in _PARADIGMS:
        recs = frontier_and_recommendations(prices, paradigm=p)["recommendations"]
        for v in _VALUE_SETTINGS:
            grid[(v, p)] = recs[v]
    return SensitivityResult(grid=grid)
