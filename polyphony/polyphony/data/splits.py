"""Time-blocked splits — never shuffle a time series (leakage guard for backtesting)."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Split:
    train: slice
    test: slice


def time_blocked_split(n: int, test_frac: float = 0.3) -> Split:
    """A single contiguous train→test split (test is the most recent block)."""
    if not 0.0 < test_frac < 1.0:
        raise ValueError("test_frac must be in (0, 1)")
    cut = int(round(n * (1.0 - test_frac)))
    cut = min(max(cut, 1), n - 1)
    return Split(train=slice(0, cut), test=slice(cut, n))


def walk_forward(n: int, min_train: int, horizon: int = 1) -> list[Split]:
    """Expanding-window walk-forward splits (train grows, test is the next `horizon`)."""
    if min_train < 1 or horizon < 1:
        raise ValueError("min_train and horizon must be >= 1")
    out: list[Split] = []
    t = min_train
    while t + horizon <= n:
        out.append(Split(train=slice(0, t), test=slice(t, t + horizon)))
        t += horizon
    return out
