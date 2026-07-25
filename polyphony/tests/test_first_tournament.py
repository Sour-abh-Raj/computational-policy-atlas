"""The first tournament validates the *method*: detect synergy when real, cut when spurious."""

from polyphony.experiments import run_two_regime_tournament


def test_method_detects_synergy_when_present_and_cuts_when_absent():
    res = run_two_regime_tournament(n=40, seed=0)
    coupled_regime = res["coupled_regime"]
    decoupled_regime = res["decoupled_regime"]

    # DGP has the energy⇄climate⇄economy coupling → coupled beats economy-only → keep
    assert coupled_regime.synergy.positive
    assert coupled_regime.synergy.delta > 0.0
    assert coupled_regime.coupled_error < coupled_regime.econ_only_error
    assert "keep" in coupled_regime.synergy.verdict()

    # negative control: GDP independent of emissions → economy-only wins → cut the coupling
    assert not decoupled_regime.synergy.positive
    assert decoupled_regime.synergy.delta <= 0.0
    assert decoupled_regime.econ_only_error < decoupled_regime.coupled_error
    assert "cut" in decoupled_regime.synergy.verdict()
