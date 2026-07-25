#!/usr/bin/env python3
"""Validate the atlas knowledge graph: 0-dangling edges, unique node ids, no dup edges.

Exit non-zero on any problem so it can gate CI and every commit (per CONTRIBUTING /
ADR-0002). Usage: ``python tools/validate_graph.py``.
"""

from __future__ import annotations

import collections
import json
import pathlib
import sys

GRAPH = pathlib.Path(__file__).resolve().parent.parent / "docs" / "graph" / "graph.json"


def main() -> int:
    g = json.loads(GRAPH.read_text(encoding="utf-8"))
    nodes = g.get("nodes", [])
    edges = g.get("edges", [])

    ids = [n["id"] for n in nodes]
    dup_nodes = [k for k, v in collections.Counter(ids).items() if v > 1]
    idset = set(ids)
    dangling = [e for e in edges if e["s"] not in idset or e["t"] not in idset]
    dup_edges = [
        k for k, v in collections.Counter((e["s"], e["r"], e["t"]) for e in edges).items() if v > 1
    ]

    ok = not dup_nodes and not dangling and not dup_edges
    print(f"graph: {len(nodes)} nodes, {len(edges)} edges")
    if dup_nodes:
        print(f"  ERROR duplicate node ids: {dup_nodes}")
    if dangling:
        print(f"  ERROR {len(dangling)} dangling edges: {dangling[:5]}{' …' if len(dangling) > 5 else ''}")
    if dup_edges:
        print(f"  ERROR {len(dup_edges)} duplicate edges: {dup_edges[:5]}")
    print("OK" if ok else "FAILED")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
