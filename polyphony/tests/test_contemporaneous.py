import pytest

from polyphony.core.orchestrator import Orchestrator
from polyphony.data.loaders import synthetic_food_series
from polyphony.data.splits import time_blocked_split
from polyphony.engines.assimilation import estimate_yield_sensitivity
from polyphony.engines.calibration import calibrate_scale_offset, calibrated_track
from polyphony.eval.metrics import mase
from polyphony.experiments.landfood import foodprice_track


def test_contemporaneous_removes_the_coupling_lag():
    # Lagged mode holds the land price at base for the first step(s) (temperature not yet propagated);
    # contemporaneous resolves energy->climate->land within the step, so it moves immediately.
    lagged = foodprice_track(0.0, 40, coupled=True, resolve="lagged")
    contemp = foodprice_track(0.0, 40, coupled=True, resolve="contemporaneous")
    assert lagged[0] == pytest.approx(100.0)  # lag: no warming has propagated yet
    assert contemp[0] > 100.0  # no lag: warming already raises the first-step price


class _PingPong:
    """Minimal conforming voice that reads ``reads`` and drives ``writes`` — used to build a cycle."""

    def __init__(self, name: str, reads: str, writes: str) -> None:
        self.name = name
        self.version = "test"
        self.paradigm = "test"
        self.engines: tuple[str, ...] = ()
        self.provides: tuple[str, ...] = (writes,)
        self.requires: tuple[str, ...] = (reads,)
        self._writes = writes

    def dials_spec(self):  # type: ignore[no-untyped-def]
        from polyphony.core.dials import DialsSpec

        return DialsSpec(())

    def init_state(self, dials, seed):  # type: ignore[no-untyped-def]
        return {self._writes: 0.0}

    def step(self, state, inputs, dt, dials):  # type: ignore[no-untyped-def]
        from polyphony.core.interface import StepResult
        from polyphony.core.provenance import Provenance

        val = float(next(iter(inputs.values()), 0.0)) + 1.0
        prov = Provenance.make(model=self.name, version=self.version, paradigm=self.paradigm,
                               solver="test", seed=0, dials=dials, inputs=inputs)
        return StepResult(state={self._writes: val}, outputs={self._writes: val}, provenance=prov, diagnostics={})

    def observe(self, state, keys):  # type: ignore[no-untyped-def]
        return {k: float(state.get(k, 0.0)) for k in keys}


def test_contemporaneous_rejects_a_cyclic_routing():
    # a drives x from y; b drives y from x -> a genuine cycle that MUST be lagged, not resolved in order.
    a = _PingPong("a", reads="y", writes="x")
    b = _PingPong("b", reads="x", writes="y")
    orch = Orchestrator([a, b], {"x": "a", "y": "b"})
    orch.run(steps=2, dials={}, resolve="lagged")  # lagged is fine
    with pytest.raises(ValueError, match="cycle"):
        orch.run(steps=2, dials={}, resolve="contemporaneous")


def test_land_naive_gap_is_not_a_parameter_error():
    # Assimilation recovers the TRUE yield sensitivity (0.1) from the early food-price rise…
    y = synthetic_food_series(n=40, seed=0, carbon_price=0.0).column("food_price")
    split = time_blocked_split(40)
    assert abs(estimate_yield_sensitivity(y, split.train) - 0.1) < 0.02
    # …yet the calibrated champion still loses to naive even with the lag removed — the residual is a
    # structural voice/DGP mismatch, not a parameter or lag error (needs real data, issue #9).
    contemp = foodprice_track(0.0, 40, coupled=True, resolve="contemporaneous")
    a, b = calibrate_scale_offset(contemp[split.train], y[split.train])
    assert mase(y[split.test], calibrated_track(contemp, a, b)[split.test]) > 1.0
