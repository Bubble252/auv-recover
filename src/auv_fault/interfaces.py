"""Stable fault detection, injection, and degradation contracts."""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Protocol, runtime_checkable

from auv_core.contracts import CapabilitySet, ControlProposal, SafetyContext


@dataclass(frozen=True)
class FaultSignal:
    """A detected fault condition.

    ``None`` from :meth:`FaultDetector.detect` means that no fault is present.
    A finite severity in ``[0, 1]`` communicates confidence or impact without
    requiring callers to interpret a magic zero-severity signal.
    """

    kind: str
    severity: float
    stamp_s: float

    def __post_init__(self) -> None:
        if not isinstance(self.kind, str):
            raise TypeError("kind must be a string")
        if not self.kind.strip():
            raise ValueError("kind must not be empty")
        if not isinstance(self.severity, (int, float)) or not math.isfinite(self.severity):
            raise ValueError("severity must be finite")
        if not 0.0 <= self.severity <= 1.0:
            raise ValueError("severity must be in [0, 1]")
        if not isinstance(self.stamp_s, (int, float)) or not math.isfinite(self.stamp_s):
            raise ValueError("stamp_s must be finite")
        if self.stamp_s < 0.0:
            raise ValueError("stamp_s must be non-negative")
        object.__setattr__(self, "severity", float(self.severity))
        object.__setattr__(self, "stamp_s", float(self.stamp_s))


@runtime_checkable
class FaultDetector(Protocol):
    """Detect a fault from the current safety context."""

    def detect(self, context: SafetyContext) -> FaultSignal | None: ...


@runtime_checkable
class FaultInjector(Protocol):
    """Apply a detected fault to an explicit capability set."""

    def inject(self, capability: CapabilitySet, signal: FaultSignal) -> CapabilitySet: ...


@runtime_checkable
class DegradationPolicy(Protocol):
    """Select a degraded control proposal for a detected fault."""

    def degrade(self, proposal: ControlProposal, signal: FaultSignal) -> ControlProposal: ...


__all__ = ["DegradationPolicy", "FaultDetector", "FaultInjector", "FaultSignal"]
