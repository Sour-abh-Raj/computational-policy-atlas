"""Combiner — the heart of Polyphony: report the *disagreement*, never a silent average.

When several voices answer the same quantity, the default combiner keeps **all** answers
and reports their skill-weighted spread as a normalized **disagreement index** ``D`` plus
an **attribution** of D to the dial that drives the split (ADR-0004,
docs/polyphony/01-blueprint.md §4). Averaging combiners (BMA, weighted mean) exist only as
tournament *challengers* elsewhere — they are not the default here.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import sqrt
from typing import Mapping, Sequence


@dataclass(frozen=True)
class VoiceAnswer:
    voice: str
    value: float
    weight: float = 1.0  # out-of-sample skill weight (equal by default)
    paradigm: str = ""


@dataclass(frozen=True)
class Disagreement:
    quantity: str
    answers: tuple[VoiceAnswer, ...]
    weighted_mean: float
    weighted_sd: float
    index_D: float  # sd_w / (|mean_w| + eps) — normalized disagreement
    spread: float  # max - min

    @property
    def consensus(self) -> bool:
        """Convenience label; the tolerance is a *reporting* dial, never a selection gate."""
        return self.spread == 0.0

    def as_dict(self) -> dict:
        return {
            "quantity": self.quantity,
            "answers": [vars(a) for a in self.answers],
            "weighted_mean": self.weighted_mean,
            "weighted_sd": self.weighted_sd,
            "index_D": self.index_D,
            "spread": self.spread,
        }


def _normalize_weights(weights: Sequence[float]) -> list[float]:
    if any(w < 0 for w in weights):
        raise ValueError("weights must be non-negative")
    total = sum(weights)
    if total <= 0:
        return [1.0 / len(weights)] * len(weights)
    return [w / total for w in weights]


def _weighted_mean(values: Sequence[float], w: Sequence[float]) -> float:
    return sum(v * wi for v, wi in zip(values, w))


def _weighted_sd(values: Sequence[float], w: Sequence[float], mean: float) -> float:
    var = sum(wi * (v - mean) ** 2 for v, wi in zip(values, w))
    return sqrt(max(var, 0.0))


def combine(quantity: str, answers: Sequence[VoiceAnswer], eps: float = 1e-9) -> Disagreement:
    """Combine voice answers into a :class:`Disagreement` (does **not** collapse them)."""
    if not answers:
        raise ValueError("combine() needs at least one answer")
    values = [a.value for a in answers]
    w = _normalize_weights([a.weight for a in answers])
    mean = _weighted_mean(values, w)
    sd = _weighted_sd(values, w, mean)
    index_d = sd / (abs(mean) + eps)
    return Disagreement(
        quantity=quantity,
        answers=tuple(answers),
        weighted_mean=mean,
        weighted_sd=sd,
        index_D=index_d,
        spread=max(values) - min(values),
    )


def attribute_to_dial(
    quantity: str,
    answers: Sequence[VoiceAnswer],
    dial_value_by_voice: Mapping[str, object],
) -> dict:
    """How much of the disagreement does one (categorical) dial explain?

    Groups answers by the dial setting each voice used, computes the weight-averaged
    *within-group* disagreement, and reports the explained fraction
    ``1 - within/overall``. A high explained fraction means "the split is driven by this
    dial" — the actionable finding, not a failure.
    """
    overall = combine(quantity, answers).index_D
    groups: dict[object, list[VoiceAnswer]] = {}
    for a in answers:
        groups.setdefault(dial_value_by_voice.get(a.voice), []).append(a)

    total_w = sum(a.weight for a in answers) or float(len(answers))
    within = 0.0
    for items in groups.values():
        gd = 0.0 if len(items) == 1 else combine(quantity, items).index_D
        gw = sum(i.weight for i in items) or float(len(items))
        within += (gw / total_w) * gd

    explained = 0.0 if overall == 0 else max(0.0, 1.0 - within / overall)
    return {
        "quantity": quantity,
        "overall_D": overall,
        "within_group_D": within,
        "explained_fraction": explained,
        "groups": {str(k): [a.voice for a in v] for k, v in groups.items()},
    }
