from polyphony.core.interface import conforms
from polyphony.experiments.landfood import run_two_regime_tournament
from polyphony.models import ReducedFormLand


def test_land_voice_price_rises_with_warming():
    m = ReducedFormLand()
    assert conforms(m)
    cold = m.step(m.init_state({"yield_sensitivity": 0.1}, 0), {"temperature": 0.0}, 1.0, {"yield_sensitivity": 0.1})
    hot = m.step(m.init_state({"yield_sensitivity": 0.1}, 0), {"temperature": 3.0}, 1.0, {"yield_sensitivity": 0.1})
    assert hot.outputs["food_price"] > cold.outputs["food_price"]


def test_landfood_synergy_kept_under_warming_and_cut_when_flat():
    res = run_two_regime_tournament(n=40, seed=0)
    warming = res["warming_regime"]
    flat = res["flat_regime"]
    assert warming.synergy.positive
    assert warming.synergy.delta > 0.0
    assert warming.coupled_error < warming.land_only_error
    assert not flat.synergy.positive
    assert flat.synergy.delta <= 0.0
