"""Polyphony core — the paradigm-agnostic ensemble machinery.

Exports the common model interface, the disagreement combiner, the coupling orchestrator,
and provenance/dials support. See docs/polyphony/01-blueprint.md.
"""

from .combiner import Disagreement, VoiceAnswer, attribute_to_dial, combine
from .dials import Dial, DialsSpec
from .interface import Dials, Inputs, Model, State, StepResult, conforms
from .orchestrator import Orchestrator, RunResult
from .provenance import Provenance, stable_hash

__all__ = [
    "Model",
    "State",
    "Inputs",
    "Dials",
    "StepResult",
    "conforms",
    "Dial",
    "DialsSpec",
    "Provenance",
    "stable_hash",
    "VoiceAnswer",
    "Disagreement",
    "combine",
    "attribute_to_dial",
    "Orchestrator",
    "RunResult",
]
