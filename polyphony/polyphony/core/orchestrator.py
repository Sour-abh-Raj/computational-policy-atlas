"""Orchestrator — couple voices under one clock; route dynamics, record disagreement.

The orchestrator holds a set of :class:`~polyphony.core.interface.Model` voices wired by
state hand-offs (``provides`` → ``requires``). Cross-domain feedback loops are expected,
so the default coupling is **recursive (lagged, Gauss–Seidel)**: each step every voice reads
the shared *bus*, advances, and writes its outputs; the bus value for a quantity is updated by
its **routed** voice (paradigm routing), while **all** voices' outputs are recorded for the
:mod:`~polyphony.core.combiner` to report disagreement (blueprint §4).

Lagging every hop is only *required* to break **cycles**. For an **acyclic** (feed-forward)
routing DAG — e.g. energy → climate → land — the correct solve resolves voices in **topological
order within the step**, so downstream voices read fresh upstream outputs with no one-step delay
(``resolve="contemporaneous"``). This removes a spurious lag that otherwise costs real forecast
skill (ADR-0005). Lag remains the default and the only option when the routing has a cycle.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Literal, Mapping, Sequence

from .combiner import VoiceAnswer
from .interface import Model
from .provenance import Provenance


@dataclass
class RunResult:
    history: list[dict[str, float]]  # per-step bus snapshot (the coupled trajectory)
    voice_outputs: list[dict[str, list[VoiceAnswer]]]  # per-step {quantity: [answers]}
    provenance: list[list[Provenance]]  # per-step, per-voice provenance

    def answers_for(self, quantity: str, step: int = -1) -> list[VoiceAnswer]:
        return self.voice_outputs[step].get(quantity, [])


@dataclass
class Orchestrator:
    voices: Sequence[Model]
    routing: Mapping[str, str]  # quantity -> voice.name that drives the bus for it
    skill_weight: Mapping[str, float] = field(default_factory=dict)  # voice.name -> weight

    def __post_init__(self) -> None:
        names = [v.name for v in self.voices]
        if len(set(names)) != len(names):
            raise ValueError(f"voice names must be unique: {names}")
        for q, vname in self.routing.items():
            if vname not in names:
                raise ValueError(f"routing[{q!r}] -> unknown voice {vname!r}")
            provider = next(v for v in self.voices if v.name == vname)
            if q not in provider.provides:
                raise ValueError(f"routed voice {vname!r} does not provide {q!r}")

    def _topological_order(self) -> list[Model]:
        """Order voices so every routed producer runs before its consumers. Raise if cyclic.

        Edge producer → consumer whenever a consumer ``requires`` a quantity the producer is
        **routed** to drive. A cycle means the coupling genuinely feeds back and must be lagged.
        """
        deps: dict[str, set[str]] = {v.name: set() for v in self.voices}  # name -> producers it waits on
        for q, producer in self.routing.items():
            for v in self.voices:
                if q in v.requires and v.name != producer:
                    deps[v.name].add(producer)
        order: list[Model] = []
        placed: set[str] = set()
        while len(placed) < len(self.voices):
            ready = [v for v in self.voices if v.name not in placed and deps[v.name] <= placed]
            if not ready:
                raise ValueError("routing has a cycle; use resolve='lagged' (the default)")
            for v in ready:  # stable: preserve declaration order among independents
                order.append(v)
                placed.add(v.name)
        return order

    def run(
        self,
        steps: int,
        dials: Mapping[str, Any],
        seed: int = 0,
        dt: float = 1.0,
        resolve: Literal["lagged", "contemporaneous"] = "lagged",
    ) -> RunResult:
        # Validate dials per voice; init states; seed the bus from initial observations.
        merged: dict[str, dict[str, Any]] = {}
        states: dict[str, dict[str, float]] = {}
        bus: dict[str, float] = {}
        for v in self.voices:
            spec = v.dials_spec()
            # `dials` is a shared global panel; each voice consumes only what it declares.
            known = {d.name for d in spec.dials}
            merged[v.name] = spec.validate({k: val for k, val in dials.items() if k in known})
            states[v.name] = v.init_state(merged[v.name], seed)
            for k, val in v.observe(states[v.name], v.provides).items():
                bus.setdefault(k, val)

        # Contemporaneous mode resolves an acyclic DAG in dependency order (raises if cyclic);
        # lagged mode (default) keeps declaration order and applies routed updates after the step.
        order = self._topological_order() if resolve == "contemporaneous" else list(self.voices)

        history: list[dict[str, float]] = []
        voice_outputs: list[dict[str, list[VoiceAnswer]]] = []
        provenance: list[list[Provenance]] = []

        for _ in range(steps):
            step_answers: dict[str, list[VoiceAnswer]] = {}
            step_prov: list[Provenance] = []
            routed_updates: dict[str, float] = {}
            for v in order:
                # Contemporaneous: read routed outputs already produced upstream this step.
                source = {**bus, **routed_updates} if resolve == "contemporaneous" else bus
                inputs = {k: source.get(k, 0.0) for k in v.requires}
                res = v.step(states[v.name], inputs, dt, merged[v.name])
                states[v.name] = res.state
                step_prov.append(res.provenance)
                w = self.skill_weight.get(v.name, 1.0)
                for q, val in res.outputs.items():
                    step_answers.setdefault(q, []).append(
                        VoiceAnswer(voice=v.name, value=val, weight=w, paradigm=v.paradigm)
                    )
                    if self.routing.get(q) == v.name:
                        routed_updates[q] = val
            bus.update(routed_updates)
            history.append(dict(bus))
            voice_outputs.append(step_answers)
            provenance.append(step_prov)

        return RunResult(history=history, voice_outputs=voice_outputs, provenance=provenance)
