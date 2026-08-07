"""Abstract execution-layer interface used by the agent (roadmap: Ros2RobotTool).

Concrete implementations:
  - Ros2RobotTool  : ROS2 topics/services (this repo)
  - future         : hardware adapter, MoveIt2 arm tool, mock tool for experiments
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional


class BaseRobotTool(ABC):
    """Contract between the agent and the robot execution layer."""

    @abstractmethod
    def move(
        self,
        linear_x: float = 0.0,
        linear_y: float = 0.0,
        angular_z: float = 0.0,
        duration: float = 0.0,
    ) -> bool:
        """Move with the given velocity for `duration` seconds (0 = until stopped)."""

    @abstractmethod
    def stop(self) -> bool:
        """Stop the robot immediately."""

    @abstractmethod
    def rotate(self, angular_z: float, duration: float = 0.0) -> bool:
        """Rotate with angular velocity `angular_z` rad/s for `duration` seconds."""

    @abstractmethod
    def navigate(self, goal: str, **kwargs: Any) -> bool:
        """Navigate to `goal` (requires Navigation2; reserved for the next milestone)."""

    @abstractmethod
    def get_pose(self) -> Optional[Dict[str, float]]:
        """Return latest pose dict {x, y, yaw, stamp} or None if unknown."""

    @abstractmethod
    def get_sensor(self, name: str) -> Dict[str, Any]:
        """Return latest sensor data for `name` (e.g. camera / laser)."""

    @abstractmethod
    def execute_action(self, action: Dict[str, Any]) -> bool:
        """Dispatch a structured action dict (action/linear_x/...) to the robot."""
