# The Atlas of Computational Policy Simulation

A comprehensive, textbook-quality reconnaissance of policy simulation models across
every scientific discipline — assembled as the **design foundation** for a future
next-generation integrated policy simulator.

> **This deliverable is not software. It is a knowledge base and technical book.**
> The goal is to understand every major modeling philosophy *before* attempting to
> invent a new one.

## Why this exists

Policy questions — decarbonization pathways, energy transitions, land-use change,
epidemic response, urban growth — are answered today by dozens of incompatible
modeling traditions (IAMs, CGE, energy-system optimization, agent-based, system
dynamics, RL). Each encodes a different theory of how the world works. Before
designing an integrated simulator, we map the entire territory: **why each model
exists, what it assumes, when it works, and where it fails.**

## The Three-Track method

Every topic is documented in three parallel tracks so it serves researchers,
engineers, and system designers at once:

| Track | Audience | Content |
|-------|----------|---------|
| 🎓 **Scholar** | Researchers | Textbook explanation, mathematical foundations, citations |
| 🛠️ **Engineer** | Implementers | Software architecture, algorithms, data structures, code organization |
| 🏛️ **Architect** | Simulator designers | Distilled design lessons, reusable patterns, trade-offs |

See [`docs/foundations/three-track-method.md`](docs/foundations/three-track-method.md).

## Build locally

```bash
pip install -r requirements.txt
mkdocs serve         # live preview at http://127.0.0.1:8000
mkdocs build         # static site into ./site
```

## Status

Depth-first: the structure, templates, and one flagship dossier (**DICE**) are
complete to publishable quality. Breadth (the remaining ~80 models) is produced
against that proven pattern. See `docs/model-families/index.md` for the roadmap.

## Publishing

GitHub Pages deployment is a deliberate, credential-gated step. Authenticate with
your own `gh auth login` — **never commit tokens or secrets to this repo.**

## Citation discipline

This atlas is a synthesis and navigation layer. Always cite the **primary sources**
(listed per dossier and in `docs/bibliography.md`), not the atlas itself.
