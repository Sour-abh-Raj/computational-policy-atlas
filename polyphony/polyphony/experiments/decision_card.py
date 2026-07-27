"""Decision card — the north star made concrete: help a human choose, honestly (Iter 28).

Everything Polyphony builds exists to support one act: **a human choosing a policy with their eyes open.**
A decision card assembles, for a policy question (here: what carbon price?), the three things a single
confident number hides:

1. **Values are a dial, not a default.** The recommended policy under a utilitarian, a prioritarian, and a
   Rawlsian+tail-averse social welfare function — and whether they *agree* (they need not).
2. **Paradigms disagree.** On the key outcome (GDP), the equilibrium (CGE) and disequilibrium (E3ME)
   voices give *opposite-signed* responses to carbon pricing; the card reports the disagreement index D
   and both answers rather than silently averaging them.
3. **Validation is disclosed.** Which cross-domain couplings the ensemble leans on, and their **real-data
   verdict** — so the human knows the recommendation rests largely on couplings that *failed* real-data
   validation (six of seven were cut). A recommendation is decision-support under deep uncertainty, **not
   a forecast**.

This is deliberately anti-oracular: the card's job is to make the *contested* structure of the choice
legible, not to collapse it into one number.
"""

from __future__ import annotations

from dataclasses import dataclass

from ..core.combiner import Disagreement, combine
from ..core.interface import Model
from ..core.orchestrator import Orchestrator
from ..models import DisequilibriumEconomy, EquilibriumEconomy, ReducedFormClimate, ReducedFormEnergy
from .welfare_frontier import frontier_and_recommendations

# The ensemble's real-data verdict ledger (leaderboard Rounds 1–22): what survived, what was cut and why.
KEPT_COUPLINGS: tuple[str, ...] = (
    "Macro⇄Health (assimilation + no-lag) — survives full red-team round",
    "Energy⇄Inflation (pass-through) — REAL keep: beats every baseline + naive across walk-forward folds",
)
CUT_COUPLINGS: tuple[tuple[str, str], ...] = (
    ("Energy⇄climate⇄economy", "level artifact; genuinely cyclic"),
    ("Real climate→GDP", "fails placebo (CO₂ and temperature)"),
    ("Land⇄Climate⇄Food", "fails placebo + wrong sign on real yield"),
    ("Urban⇄Transport⇄Energy⇄Health", "right sign but no skill above trend (confounded)"),
    ("Water⇄Energy⇄Food (energy→food)", "corr +0.90 but no out-of-sample skill"),
    ("Macro⇄Finance (spread→growth)", "right sign, beats placebo, but regime-dependent skill"),
    ("Trade⇄Emissions (carbon leakage)", "right sign but confounded-away (panel FE: 92% attenuation)"),
)


def _gdp_disagreement(carbon_price: float, n: int = 30) -> Disagreement:
    """Equilibrium (CGE) vs disequilibrium (E3ME) GDP response to a carbon price — reported, not averaged."""
    voices: list[Model] = [
        ReducedFormEnergy(),
        ReducedFormClimate(),
        EquilibriumEconomy(),
        DisequilibriumEconomy(),
    ]
    routing = {
        "energy_cost": "energy",
        "emissions": "energy",
        "temperature": "dice",
        "damage_frac": "dice",
        "demand": "cge",
        "gdp": "cge",
    }
    r = Orchestrator(voices, routing).run(steps=n, dials={"carbon_price": carbon_price, "tcre": 0.001}, seed=1)
    return combine("gdp", r.answers_for("gdp"))


@dataclass(frozen=True)
class DecisionCard:
    question: str
    candidates: tuple[float, ...]
    pareto_front: tuple[str, ...]
    recommendation_by_value: dict[str, str]
    gdp_disagreement_D: float
    gdp_paradigm_answers: dict[str, float]
    kept_couplings: tuple[str, ...]
    cut_couplings: tuple[tuple[str, str], ...]

    @property
    def values_agree(self) -> bool:
        return len(set(self.recommendation_by_value.values())) == 1

    @property
    def paradigms_disagree_on_gdp(self) -> bool:
        vals = list(self.gdp_paradigm_answers.values())
        return max(vals) - min(vals) > 1e-9

    def honest_summary(self) -> str:
        rec = (
            "the same policy under all three value settings"
            if self.values_agree
            else "a **different** policy depending on your values"
        )
        return (
            f"Recommendation: {rec} — see the per-value table. On GDP, the equilibrium and "
            f"disequilibrium paradigms {'disagree' if self.paradigms_disagree_on_gdp else 'agree'} "
            f"(D={self.gdp_disagreement_D:.2f}); both answers are shown, not averaged. The ensemble leans "
            f"on cross-domain couplings of which **{len(self.cut_couplings)} of "
            f"{len(self.cut_couplings) + len(self.kept_couplings)} failed real-data validation** — so this "
            f"is decision-support under deep uncertainty, NOT a forecast. Choose with your eyes open."
        )


def build_decision_card(carbon_prices: tuple[float, ...] = (0.0, 50.0, 100.0, 200.0, 400.0)) -> DecisionCard:
    fr = frontier_and_recommendations(list(carbon_prices))
    ref = carbon_prices[len(carbon_prices) // 2]  # a representative (median) policy for the disagreement read
    dis = _gdp_disagreement(ref)
    return DecisionCard(
        question=f"What carbon price? Candidates: {', '.join(f'{c:g}' for c in carbon_prices)} $/t",
        candidates=carbon_prices,
        pareto_front=tuple(fr["pareto_front"]),
        recommendation_by_value=fr["recommendations"],
        gdp_disagreement_D=dis.index_D,
        gdp_paradigm_answers={a.voice: a.value for a in dis.answers},
        kept_couplings=KEPT_COUPLINGS,
        cut_couplings=CUT_COUPLINGS,
    )
