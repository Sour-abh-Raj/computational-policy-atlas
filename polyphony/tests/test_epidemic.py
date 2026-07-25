from polyphony.core.interface import conforms
from polyphony.models import ReducedFormEpidemic


def test_epidemic_conforms_and_produces_an_outbreak_wave():
    m = ReducedFormEpidemic()
    assert conforms(m)
    st = m.init_state({"r0": 2.5, "npi_strength": 0.0}, 0)
    penalties = []
    for _ in range(40):
        res = m.step(st, {}, 1.0, {"r0": 2.5, "npi_strength": 0.0})
        st = res.state
        penalties.append(res.outputs["output_penalty"])
    assert max(penalties) > penalties[0]  # the epidemic wave rises above baseline
    assert max(penalties) <= 0.6  # capped


def test_npi_reduces_the_peak():
    m = ReducedFormEpidemic()

    def peak(npi: float) -> float:
        st = m.init_state({"r0": 2.5, "npi_strength": npi}, 0)
        pk = 0.0
        for _ in range(40):
            res = m.step(st, {}, 1.0, {"r0": 2.5, "npi_strength": npi})
            st = res.state
            pk = max(pk, res.diagnostics["infected_frac"])
        return pk

    assert peak(0.6) < peak(0.0)  # interventions flatten the curve
