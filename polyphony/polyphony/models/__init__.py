"""Vertical-slice voices for Polyphony (Phase 2 scaffold).

These are **reduced-form, honestly-labeled toy** implementations behind the common
:class:`~polyphony.core.interface.Model` interface — enough to exercise coupling, routing,
run-both, disagreement, dials, and provenance end-to-end. They are **not** the full
reference models and make no fidelity claim; faithful reduced-form DICE/energy/CGE
adapters (with stated fidelity limits) and, later, wrapped reference implementations
replace them in subsequent iterations.
"""

from .econ_cge import EquilibriumEconomy
from .econ_e3me import DisequilibriumEconomy
from .energy_lp import ReducedFormEnergy

__all__ = ["ReducedFormEnergy", "EquilibriumEconomy", "DisequilibriumEconomy"]
