# How to Read (and Write) a Dossier

Every model dossier follows the **same canonical structure**, so that any two models
are directly comparable and no dimension is silently omitted. This page is both the
reader's map and the contributor's checklist. Copy it verbatim to start a new dossier.

## Front matter — the Positioning Card

Every dossier opens with a one-line summary and a **taxonomy positioning card**
(see [Taxonomy](../foundations/taxonomy.md)) placing the model on the standard axes,
plus a facts table:

| Field | Example |
|-------|---------|
| Full name | Dynamic Integrated Climate–Economy model |
| Domain | Climate — Integrated Assessment |
| First release / current | 1992 / DICE-2023 |
| Institution · lead | Yale University · William Nordhaus |
| Language · solver | GAMS/CONOPT; Python ports (Pyomo/IPOPT) |
| License | Model equations public; code variously MIT/academic |

## 🎓 Scholar Track

1. **History & motivation** — research group, institution, timeline, the scientific
   question it was built to answer.
2. **Mathematical formulation**
     - State variables
     - Decision (control) variables
     - Objective function(s)
     - Constraints
     - Temporal resolution
     - Spatial resolution
3. **Solution & algorithms** — optimization/solution method.
4. **Calibration** — data sources, parameter estimation.
5. **Validation** — how it is tested against reality (or why it can't be).
6. **Scenario generation** — how policy experiments are constructed.
7. **Strengths / Weaknesses / Known criticisms** — with citations to the critics.

## 🛠️ Engineer Track

8. **Software architecture** — module decomposition, the engines it contains.
9. **Data structures & pipeline** — inputs, formats, I/O.
10. **Computational complexity** — problem size, solve time, scaling behavior.
11. **Programming language · open-source status · extensibility.**
12. **How to run it** — minimal reproducible example / entry points.

## 🏛️ Architect Track

13. **Reusable design patterns** — which [Architecture Patterns](../patterns/index.md)
    it exemplifies.
14. **Trade-offs & alternatives** — what it gave up, and when the alternative wins.
15. **Adoption** — industrial, government, UN/IPCC.
16. **Ecosystem** — competing alternatives, successor models, known forks.
17. **Research gaps & future directions.**
18. **Lesson for the integrated simulator** — the one-paragraph takeaway answering:
    *"If we were designing the world's most capable policy simulator today, what
    should we learn from this model?"*

## Major publications & bibliography

A dedicated references block; primary sources also roll up into the global
[Bibliography](../bibliography.md).

---

!!! tip "Minimum bar"
    A dossier is not "done" until every one of the 18 sections is filled or explicitly
    marked *N/A with reason*. A `TODO` is acceptable and honest; a silent omission is not.

!!! warning "Sourcing"
    Prefer peer-reviewed papers, official documentation, and IPCC/OECD/World
    Bank/UN/national-lab reports. Where the atlas synthesizes or infers, say so
    explicitly rather than dressing an inference as a cited fact.
