import pytest

from polyphony.core.dials import Dial, DialsSpec


def test_defaults_and_merge():
    spec = DialsSpec(
        (
            Dial("carbon_price", 0.0, low=0.0, high=100.0),
            Dial("closure", "equilibrium", choices=("equilibrium", "disequilibrium")),
        )
    )
    assert spec.defaults() == {"carbon_price": 0.0, "closure": "equilibrium"}
    merged = spec.validate({"carbon_price": 50.0})
    assert merged == {"carbon_price": 50.0, "closure": "equilibrium"}


def test_reject_unknown_dial():
    spec = DialsSpec((Dial("carbon_price", 0.0, low=0.0, high=100.0),))
    with pytest.raises(KeyError):
        spec.validate({"nope": 1})


def test_reject_out_of_range():
    spec = DialsSpec((Dial("carbon_price", 0.0, low=0.0, high=100.0),))
    with pytest.raises(ValueError):
        spec.validate({"carbon_price": 200.0})


def test_reject_bad_category():
    spec = DialsSpec((Dial("closure", "equilibrium", choices=("equilibrium",)),))
    with pytest.raises(ValueError):
        spec.validate({"closure": "disequilibrium"})
