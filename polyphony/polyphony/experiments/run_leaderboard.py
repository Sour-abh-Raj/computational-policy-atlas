"""Generate the leaderboard from the first tournament (reproducible).

``python -m polyphony.experiments.run_leaderboard`` writes ``docs/polyphony/leaderboard.json``
and prints the Markdown table for embedding in ``docs/polyphony/leaderboard.md``.
"""

from __future__ import annotations

import pathlib
import sys

from ..tournament.leaderboard import Leaderboard, LeaderboardRow
from . import run_two_regime_tournament

ROOT = pathlib.Path(__file__).resolve().parents[3]
OUT_JSON = ROOT / "docs" / "polyphony" / "leaderboard.json"


def build_rows() -> list[LeaderboardRow]:
    res = run_two_regime_tournament(n=40, seed=0)
    cr, dr = res["coupled_regime"], res["decoupled_regime"]
    return [
        LeaderboardRow(
            question="GDP track — synthetic COUPLED regime (DGP has energy⇄climate⇄economy feedback)",
            champion="coupled ensemble (energy+climate+CGE+E3ME)",
            beat=["economy-only (feedback off)"],
            metric="MASE, held-out (time-blocked 30%)",
            value=cr.coupled_error,
            synergy_delta=cr.synergy.delta,
            data="synthetic-policy n=40 seed=0",
            why="coupled tracks the damage-driven decline economy-only misses; Δ>0 ⇒ keep",
        ),
        LeaderboardRow(
            question="GDP track — synthetic DECOUPLED regime (negative control: GDP ⟂ emissions)",
            champion="economy-only (feedback off)",
            beat=["coupled ensemble"],
            metric="MASE, held-out (time-blocked 30%)",
            value=dr.econ_only_error,
            synergy_delta=dr.synergy.delta,
            data="synthetic-decoupled n=40 seed=0",
            why="coupled wrongly imposes damages; economy-only wins ⇒ Δ≤0 ⇒ coupling correctly CUT",
        ),
    ]


def main() -> None:
    if OUT_JSON.exists():
        OUT_JSON.unlink()
    lb = Leaderboard(OUT_JSON)
    for row in build_rows():
        lb.add(row)
    # Windows consoles default to cp1252; write UTF-8 so Δ/⇄ don't crash the print.
    sys.stdout.buffer.write(lb.to_markdown().encode("utf-8"))


if __name__ == "__main__":
    main()
