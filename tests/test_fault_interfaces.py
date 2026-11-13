from __future__ import annotations

import math

import pytest

from auv_fault.interfaces import (
    DegradationPolicy,
    FaultDetector,
    FaultInjector,
    FaultSignal,
)
from conftest import make_context, make_proposal


def test_fault_signal_accepts_valid_fields() -> None:
    signal = FaultSignal(kind="rudder_jam", severity=0.75, stamp_s=1.25)

    assert signal.kind == "rudder_jam"
    assert signal.severity == pytest.approx(0.75)
    assert signal.stamp_s == pytest.approx(1.25)


@pytest.mark.parametrize("kind", ["", "   "])
def test_fault_signal_rejects_empty_kind(kind: str) -> None:
    with pytest.raises(ValueError, match="kind"):
        FaultSignal(kind=kind, severity=0.5, stamp_s=1.0)


@pytest.mark.parametrize("severity", [-0.01, 1.01, math.nan, math.inf])
def test_fault_signal_rejects_invalid_severity(severity: float) -> None:
    with pytest.raises(ValueError, match="severity"):
        FaultSignal(kind="rudder_jam", severity=severity, stamp_s=1.0)


@pytest.mark.parametrize("stamp_s", [-0.01, math.nan, math.inf])
def test_fault_signal_rejects_invalid_stamp(stamp_s: float) -> None:
    with pytest.raises(ValueError, match="stamp_s"):
        FaultSignal(kind="rudder_jam", severity=0.5, stamp_s=stamp_s)


def test_contracts_are_structural_protocols() -> None:
    class Detector:
        def detect(self, context):
            del context
            return None

    class Injector:
        def inject(self, capability, signal):
            del signal
            return capability

    class Policy:
        def degrade(self, proposal, signal):
            del signal
            return proposal

    assert isinstance(Detector(), FaultDetector)
    assert isinstance(Injector(), FaultInjector)
    assert isinstance(Policy(), DegradationPolicy)


def test_injector_can_return_new_capability_without_mutating_input() -> None:
    context = make_context()
    before = context.capability
    signal = FaultSignal(kind="rudder_jam", severity=0.8, stamp_s=1.0)

    class Injector:
        def inject(self, capability, signal):
            del signal
            return type(capability)(
                available_actuators=("propeller",),
                effectiveness={"propeller": capability.effectiveness["propeller"]},
            )

    after = Injector().inject(before, signal)

    assert after is not before
    assert before.available_actuators == ("propeller", "rudder")
    assert after.available_actuators == ("propeller",)


def test_degradation_policy_receives_original_proposal_and_signal() -> None:
    proposal = make_proposal()
    signal = FaultSignal(kind="rudder_jam", severity=0.8, stamp_s=1.0)

    class Policy:
        def degrade(self, candidate, fault):
            assert candidate is proposal
            assert fault is signal
            return candidate

    assert Policy().degrade(proposal, signal) is proposal
