from __future__ import annotations

import numpy as np
from auv_core.contracts import CapabilitySet, ControlProposal, SafetyContext, State


def make_context(t_s: float = 1.0) -> SafetyContext:
    state = State(
        t_s=t_s,
        position_ned_m=np.zeros(3, dtype=np.float64),
        quat_xyzw=np.array([0.0, 0.0, 0.0, 1.0], dtype=np.float64),
        linear_velocity_body_mps=np.zeros(3, dtype=np.float64),
        angular_velocity_body_rps=np.zeros(3, dtype=np.float64),
    )
    capability = CapabilitySet(
        available_actuators=("propeller", "rudder"),
        effectiveness={"propeller": 1.0, "rudder": 1.0},
    )
    return SafetyContext(
        state=state,
        local_obstacles=(),
        capability=capability,
    )


def make_proposal(t_s: float = 1.0) -> ControlProposal:
    return ControlProposal(
        stamp_s=t_s,
        linear_accel_body_mps2=np.zeros(3, dtype=np.float64),
        angular_velocity_body_rps=np.zeros(3, dtype=np.float64),
        valid_until_s=t_s + 0.1,
    )
