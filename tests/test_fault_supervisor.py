from __future__ import annotations

import numpy as np
from auv_core.contracts import ControlProposal, SafeCommand, SafetyContext

from auv_fault.interfaces import FaultSignal
from auv_fault.supervisor import SafetySupervisor
from conftest import make_context, make_proposal


class RecordingDetector:
    def __init__(self, signal: FaultSignal | None, order: list[str]) -> None:
        self.signal = signal
        self.order = order
        self.contexts: list[SafetyContext] = []

    def detect(self, context):
        self.order.append("detect")
        self.contexts.append(context)
        return self.signal


class RecordingPolicy:
    def __init__(self, order: list[str], degraded: ControlProposal) -> None:
        self.order = order
        self.degraded = degraded
        self.calls: list[tuple[ControlProposal, FaultSignal]] = []

    def degrade(self, proposal, signal):
        self.order.append("degrade")
        self.calls.append((proposal, signal))
        return self.degraded


class RecordingFilter:
    def __init__(self, order: list[str], allowed: bool = True) -> None:
        self.order = order
        self.allowed = allowed
        self.calls: list[tuple[ControlProposal, SafetyContext]] = []

    def filter(self, proposal, context):
        self.order.append("filter")
        self.calls.append((proposal, context))
        reason = None if self.allowed else "blocked by test filter"
        return SafeCommand(command=proposal, allowed=self.allowed, reason=reason)


def test_no_fault_skips_degradation_and_filters_original_proposal() -> None:
    order: list[str] = []
    detector = RecordingDetector(None, order)
    policy = RecordingPolicy(order, make_proposal(2.0))
    safety_filter = RecordingFilter(order)
    proposal = make_proposal()
    context = make_context()

    result = SafetySupervisor(detector, policy, safety_filter).supervise(proposal, context)

    assert order == ["detect", "filter"]
    assert policy.calls == []
    assert safety_filter.calls == [(proposal, context)]
    assert result.command is proposal
    assert result.allowed is True


def test_fault_runs_detection_degradation_then_filter() -> None:
    order: list[str] = []
    signal = FaultSignal(kind="rudder_jam", severity=0.8, stamp_s=1.0)
    original = make_proposal()
    degraded = ControlProposal(
        stamp_s=1.0,
        linear_accel_body_mps2=np.array([0.1, 0.2, 0.3], dtype=np.float64),
        angular_velocity_body_rps=np.array([0.0, 0.0, 0.2], dtype=np.float64),
        valid_until_s=1.1,
    )
    detector = RecordingDetector(signal, order)
    policy = RecordingPolicy(order, degraded)
    safety_filter = RecordingFilter(order)
    context = make_context()

    result = SafetySupervisor(detector, policy, safety_filter).supervise(original, context)

    assert order == ["detect", "degrade", "filter"]
    assert detector.contexts == [context]
    assert policy.calls == [(original, signal)]
    assert safety_filter.calls == [(degraded, context)]
    assert result.command is degraded
    assert result.allowed is True


def test_supervisor_returns_filter_decision_without_rewriting_it() -> None:
    order: list[str] = []
    detector = RecordingDetector(None, order)
    policy = RecordingPolicy(order, make_proposal(2.0))
    safety_filter = RecordingFilter(order, allowed=False)

    result = SafetySupervisor(detector, policy, safety_filter).supervise(
        make_proposal(), make_context()
    )

    assert result.allowed is False
