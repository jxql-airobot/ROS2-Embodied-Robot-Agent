"""Structured action plan produced by the LLM / agent."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any, Dict

#: Actions the agent may generate (execution layer supports the first three).
ALLOWED_ACTIONS = ("move", "stop", "rotate", "navigate")


@dataclass
class ActionPlan:
    """Validated, normalized action plan."""

    action: str
    linear_x: float = 0.0
    linear_y: float = 0.0
    angular_z: float = 0.0
    duration: float = 0.0
    goal: str = ""
    params: Dict[str, Any] = field(default_factory=dict)
    response: str = ""  # natural-language feedback for the user

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    def to_command_dict(self) -> Dict[str, Any]:
        """Dict that maps 1:1 onto robot_interfaces/RobotCommand fields."""
        return {k: v for k, v in asdict(self).items() if k != "response"}

    @classmethod
    def from_dict(cls, data: Dict[str, Any], response: str = "") -> "ActionPlan":
        action = str(data.get("action", "")).strip().lower()
        if action not in ALLOWED_ACTIONS:
            raise ValueError(f"unsupported action: {action!r}")
        return cls(
            action=action,
            linear_x=float(data.get("linear_x", 0.0) or 0.0),
            linear_y=float(data.get("linear_y", 0.0) or 0.0),
            angular_z=float(data.get("angular_z", 0.0) or 0.0),
            duration=float(data.get("duration", 0.0) or 0.0),
            goal=str(data.get("goal", "") or ""),
            params=dict(data.get("params") or {}),
            response=response,
        )
