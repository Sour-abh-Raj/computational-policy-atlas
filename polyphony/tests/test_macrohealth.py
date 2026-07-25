from polyphony.data.loaders import synthetic_pandemic_series
from polyphony.experiments.macrohealth import backtest, run_two_regime_tournament


def test_macrohealth_synergy_kept_in_pandemic_and_cut_without():
    res = run_two_regime_tournament(n=40, seed=0)
    pandemic = res["pandemic_regime"]
    control = res["no_pandemic_regime"]
    # DGP has the epidemic shock → health coupling beats economy-only → keep
    assert pandemic.synergy.positive
    assert pandemic.synergy.delta > 0.0
    assert pandemic.coupled_error < pandemic.econ_only_error
    # negative control (GDP independent of the epidemic) → coupling wrongly imposes a wave → cut
    assert not control.synergy.positive
    assert control.synergy.delta <= 0.0


def test_macrohealth_champion_beats_naive_on_matched_pandemic():
    pandemic = backtest(synthetic_pandemic_series(n=40, seed=0, r0=2.5))
    # unlike the energy champion, the health-coupled predictor beats naive here (MASE < 1)
    assert pandemic.coupled_error < 1.0
