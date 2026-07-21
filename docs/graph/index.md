# Knowledge Graph

A semantic graph linking every entity in the atlas — **paradigms, algorithms, models,
institutions, researchers, domains, mathematics, and software** — with edges for
*successor-of*, *depends-on*, *shares-assumption-with*, and *alternative-to*.

The graph is the payoff of the whole atlas: it makes the *relationships* between
modeling traditions queryable, which is exactly what an integrated simulator's designer
needs.

## Schema

```mermaid
graph LR
    Paradigm -->|realized_by| Model
    Model -->|developed_at| Institution
    Model -->|led_by| Researcher
    Model -->|solves_with| Algorithm
    Model -->|belongs_to| Domain
    Model -->|implemented_in| Software
    Model -->|successor_of| Model2[Model]
    Model -->|alternative_to| Model2
    Model -->|shares_assumption| Model2
    Algorithm -->|grounded_in| Mathematics
```

## Seed graph (from the DICE dossier)

```mermaid
graph TD
    OPT[Paradigm: Optimization]
    RAMSEY[Math: Ramsey optimal growth]
    NLP[Algorithm: NLP / CONOPT]
    DICE[Model: DICE]
    RICE[Model: RICE]
    DSICE[Model: DSICE]
    GIVE[Model: GIVE]
    FUND[Model: FUND]
    PAGE[Model: PAGE]
    YALE[Institution: Yale]
    NORD[Researcher: W. Nordhaus]
    CLIM[Domain: Climate IAM]
    GAMS[Software: GAMS / Pyomo / Mimi]

    OPT --> DICE
    RAMSEY --> DICE
    NLP --> DICE
    DICE -->|developed_at| YALE
    DICE -->|led_by| NORD
    DICE -->|belongs_to| CLIM
    DICE -->|implemented_in| GAMS
    DICE -->|regional_sibling| RICE
    DICE -->|stochastic_successor| DSICE
    DICE -->|modern_successor| GIVE
    DICE -->|alternative_to| FUND
    DICE -->|alternative_to| PAGE
```

## Planned representation

- **Source of truth**: a `graph.json` (nodes + typed edges) generated from dossier
  front-matter, so the graph stays consistent with the prose.
- **Rendering**: Mermaid for embedded views here; an interactive HTML view for the
  full graph.
- **Queries** the graph should answer: *"what depends on LP?"*, *"what are the
  perfect-foresight IAMs?"*, *"which models share the equilibrium assumption?"*,
  *"what succeeded MARKAL?"*

!!! tip "Tie-in"
    This dovetails with the local **`/graphify`** workflow (input → knowledge graph →
    clustered communities). Each completed dossier contributes its entities and edges
    to the growing atlas graph.
