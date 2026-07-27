"""Disagreement study — when do modeling traditions disagree, and how much? (Iter 32)

Polyphony's distinctive move is to **report** the disagreement between paradigms, never average it away
(ADR-0004). This study asks the natural follow-up: *when* does the disagreement matter? It sweeps the
carbon-price dial and, at each level, measures the equilibrium (CGE) vs disequilibrium (E3ME) split on GDP
— the classic contested question of whether pricing carbon lowers or raises output.

The finding is sharper than "they disagree": the split is **small when no policy is acting** and
**activates** — jumping several-fold — as soon as a carbon price bites, then **saturates** once the energy
transition completes (the fossil share is fully priced out). The decision-relevant reading: the *choice of
economic paradigm matters most precisely where a real policy is contemplated*, so that is exactly where an
honest instrument should flag caution rather than report one confident number.
"""

from __future__ import annotations

from dataclasses import dataclass

from .decision_card import _gdp_disagreement


@dataclass(frozen=True)
class DisagreementPoint:
    carbon_price: float
    index_D: float
    spread: float
    cge_gdp: float
    e3me_gdp: float


@dataclass(frozen=True)
class DisagreementStudy:
    points: tuple[DisagreementPoint, ...]

    @property
    def d_at_zero(self) -> float:
        return self.points[0].index_D

    @property
    def d_peak(self) -> float:
        return max(p.index_D for p in self.points)

    @property
    def activation_ratio(self) -> float:
        """How many times larger the peak disagreement is than the no-policy baseline disagreement."""
        return self.d_peak / max(self.d_at_zero, 1e-6)

    def activates_with_policy(self) -> bool:
        """True if pricing carbon sharply raises the paradigm disagreement (not merely present at baseline)."""
        return self.activation_ratio > 3.0

    def paradigms_split_by_sign(self) -> bool:
        """At the peak-disagreement policy, do the paradigms straddle the base (CGE < 100 < E3ME)?"""
        peak = max(self.points, key=lambda p: p.index_D)
        return peak.cge_gdp < 100.0 < peak.e3me_gdp


def run_disagreement_study(
    carbon_prices: tuple[float, ...] = (0.0, 25.0, 50.0, 100.0, 200.0, 400.0),
) -> DisagreementStudy:
    points = []
    for cp in carbon_prices:
        dis = _gdp_disagreement(cp)
        ans = {a.voice: a.value for a in dis.answers}
        points.append(
            DisagreementPoint(
                carbon_price=cp,
                index_D=dis.index_D,
                spread=dis.spread,
                cge_gdp=float(ans.get("cge", 0.0)),
                e3me_gdp=float(ans.get("e3me", 0.0)),
            )
        )
    return DisagreementStudy(points=tuple(points))
