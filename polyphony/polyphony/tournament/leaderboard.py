"""Leaderboard — the append-only record of every contest (contenders, metric, winner, why)."""

from __future__ import annotations

import datetime
import json
import pathlib
from dataclasses import asdict, dataclass, field


def _now() -> str:
    return datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds")


@dataclass
class LeaderboardRow:
    question: str
    champion: str
    beat: list[str]
    metric: str
    value: float
    synergy_delta: float | None = None
    data: str = ""
    why: str = ""
    ts: str = field(default_factory=_now)


class Leaderboard:
    """JSON-backed store of :class:`LeaderboardRow`s, renderable to a Markdown table."""

    def __init__(self, path: str | pathlib.Path):
        self.path = pathlib.Path(path)

    def rows(self) -> list[LeaderboardRow]:
        if not self.path.exists():
            return []
        raw = json.loads(self.path.read_text(encoding="utf-8"))
        return [LeaderboardRow(**r) for r in raw]

    def add(self, row: LeaderboardRow) -> None:
        rows = self.rows()
        rows.append(row)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text(
            json.dumps([asdict(r) for r in rows], indent=2), encoding="utf-8"
        )

    def to_markdown(self) -> str:
        header = (
            "| Question | Champion | Beat | Metric | Value | Synergy Δ | Data | Why |\n"
            "|---|---|---|---|---:|---:|---|---|\n"
        )
        lines = []
        for r in self.rows():
            syn = "" if r.synergy_delta is None else f"{r.synergy_delta:+.4g}"
            lines.append(
                f"| {r.question} | {r.champion} | {', '.join(r.beat)} | {r.metric} "
                f"| {r.value:.4g} | {syn} | {r.data} | {r.why} |"
            )
        return header + "\n".join(lines) + ("\n" if lines else "")
