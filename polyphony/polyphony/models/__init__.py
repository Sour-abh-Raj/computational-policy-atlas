"""Vertical-slice voices for Polyphony (Phase 2 scaffold).

These are **reduced-form, honestly-labeled toy** implementations behind the common
:class:`~polyphony.core.interface.Model` interface — enough to exercise coupling, routing,
run-both, disagreement, dials, and provenance end-to-end. They are **not** the full
reference models and make no fidelity claim; faithful reduced-form DICE/energy/CGE
adapters (with stated fidelity limits) and, later, wrapped reference implementations
replace them in subsequent iterations.
"""

from .climate_dice import ReducedFormClimate
from .econ_cge import EquilibriumEconomy
from .econ_e3me import DisequilibriumEconomy
from .energy_lp import ReducedFormEnergy
from .epidemic_sir import ReducedFormEpidemic
from .finance_accelerator import ReducedFormFinance
from .health_airquality import ReducedFormAirHealth
from .land_crop import ReducedFormLand
from .nexus_food import ReducedFormNexusFood
from .trade_leakage import ReducedFormTrade
from .transport_mode import ReducedFormTransport
from .water_balance import ReducedFormWater

__all__ = [
    "ReducedFormEnergy",
    "EquilibriumEconomy",
    "DisequilibriumEconomy",
    "ReducedFormClimate",
    "ReducedFormEpidemic",
    "ReducedFormLand",
    "ReducedFormTransport",
    "ReducedFormAirHealth",
    "ReducedFormWater",
    "ReducedFormNexusFood",
    "ReducedFormFinance",
    "ReducedFormTrade",
]
