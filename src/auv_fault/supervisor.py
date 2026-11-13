"""Composition of fault handling with the shared safety filter."""

from __future__ import annotations

from auv_core.contracts import ControlProposal, SafeCommand, SafetyContext
from auv_core.interfaces import SafetyFilter

from .interfaces import DegradationPolicy, FaultDetector, FaultSignal


class SafetySupervisor:
    """Compose fault detection, degradation, and the shared safety filter."""

    def __init__(
        self,
        detector: FaultDetector,
        degradation: DegradationPolicy,
        safety_filter: SafetyFilter,
    ) -> None:
        self._detector = detector
        self._degradation = degradation
        self._safety_filter = safety_filter

    def supervise(self, proposal: ControlProposal, context: SafetyContext) -> SafeCommand:
        if not isinstance(proposal, ControlProposal):
            raise TypeError("proposal must be a ControlProposal")
        if not isinstance(context, SafetyContext):
            raise TypeError("context must be a SafetyContext")

        signal = self._detector.detect(context)
        if signal is not None:
            if not isinstance(signal, FaultSignal):
                raise TypeError("detector must return FaultSignal or None")
            proposal = self._degradation.degrade(proposal, signal)
        return self._safety_filter.filter(proposal, context)


__all__ = ["SafetySupervisor"]
