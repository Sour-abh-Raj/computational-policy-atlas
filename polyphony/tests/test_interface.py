from polyphony.core.interface import conforms
from polyphony.models import DisequilibriumEconomy, EquilibriumEconomy, ReducedFormEnergy


def test_slice_models_conform_to_common_interface():
    for factory in (ReducedFormEnergy, EquilibriumEconomy, DisequilibriumEconomy):
        model = factory()
        assert conforms(model)
        # required metadata for coupling/routing/provenance
        assert model.name and model.paradigm and model.version
        assert isinstance(model.provides, tuple) and isinstance(model.requires, tuple)
        assert isinstance(model.engines, tuple)


def test_dials_spec_defaults_are_valid():
    for factory in (ReducedFormEnergy, EquilibriumEconomy, DisequilibriumEconomy):
        spec = factory().dials_spec()
        # defaults must pass their own validation
        assert spec.validate(spec.defaults()) == spec.defaults()
