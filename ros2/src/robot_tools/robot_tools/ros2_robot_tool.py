"""Ros2RobotTool: ROS2 implementation of BaseRobotTool.

Publishes RobotCommand to the execution layer (/robot_command) and
reads /odom + /robot_status for pose/status feedback.
"""

from __future__ import annotations

import math
from typing import Any, Dict, Optional

from nav_msgs.msg import Odometry
from rclpy.node import Node
from robot_interfaces.msg import RobotCommand, RobotStatus

from robot_tools.base_robot_tool import BaseRobotTool


class Ros2RobotTool(Node, BaseRobotTool):
    def __init__(
        self,
        node_name: str = "ros2_robot_tool",
        command_topic: str = "/robot_command",
        status_topic: str = "/robot_status",
        odom_topic: str = "/odom",
    ) -> None:
        Node.__init__(self, node_name)
        self._command_topic = command_topic
        self._cmd_pub = self.create_publisher(RobotCommand, command_topic, 10)
        self._odom_sub = self.create_subscription(Odometry, odom_topic, self._on_odom, 10)
        self._status_sub = self.create_subscription(
            RobotStatus, status_topic, self._on_status, 10
        )
        self._latest_pose: Optional[Dict[str, float]] = None
        self._latest_status: Optional[RobotStatus] = None
        self.get_logger().info(
            f"Ros2RobotTool ready: cmd->{command_topic}, odom->{odom_topic}, status->{status_topic}"
        )

    # ------------------------------------------------------------------ #

    def _on_odom(self, msg: Odometry) -> None:
        p = msg.pose.pose.position
        q = msg.pose.pose.orientation
        yaw = math.atan2(
            2.0 * (q.w * q.z + q.x * q.y), 1.0 - 2.0 * (q.y * q.y + q.z * q.z)
        )
        self._latest_pose = {
            "x": p.x,
            "y": p.y,
            "yaw": yaw,
            "stamp": msg.header.stamp.sec + msg.header.stamp.nanosec * 1e-9,
        }

    def _on_status(self, msg: RobotStatus) -> None:
        self._latest_status = msg

    def _publish(self, action: str, **fields: Any) -> bool:
        msg = RobotCommand()
        msg.action = action
        msg.linear_x = float(fields.get("linear_x", 0.0))
        msg.linear_y = float(fields.get("linear_y", 0.0))
        msg.angular_z = float(fields.get("angular_z", 0.0))
        msg.duration = float(fields.get("duration", 0.0))
        msg.goal = str(fields.get("goal", ""))
        msg.source = str(fields.get("source", ""))
        self._cmd_pub.publish(msg)
        return True

    # ------------------------------------------------------------------ #

    def move(
        self,
        linear_x: float = 0.0,
        linear_y: float = 0.0,
        angular_z: float = 0.0,
        duration: float = 0.0,
    ) -> bool:
        return self._publish(
            "move", linear_x=linear_x, linear_y=linear_y, angular_z=angular_z, duration=duration
        )

    def stop(self) -> bool:
        return self._publish("stop")

    def rotate(self, angular_z: float, duration: float = 0.0) -> bool:
        return self._publish("rotate", angular_z=angular_z, duration=duration)

    def navigate(self, goal: str, **kwargs: Any) -> bool:
        return self._publish("navigate", goal=goal, **kwargs)

    def get_pose(self) -> Optional[Dict[str, float]]:
        return self._latest_pose

    def get_sensor(self, name: str) -> Dict[str, Any]:
        # Reserved interface: real sensor topics (camera /scan) land in the
        # vision & navigation milestones. Return honest availability info.
        return {
            "name": name,
            "available": False,
            "note": "sensor integration planned for vision (P2) / navigation (P1) milestones",
        }

    def execute_action(self, action: Dict[str, Any]) -> bool:
        if hasattr(action, "to_command_dict"):
            action = action.to_command_dict()
        return self._publish(
            action.get("action", ""),
            linear_x=action.get("linear_x", 0.0),
            linear_y=action.get("linear_y", 0.0),
            angular_z=action.get("angular_z", 0.0),
            duration=action.get("duration", 0.0),
            goal=action.get("goal", ""),
            source=action.get("source", ""),
        )

    def latest_status(self) -> Optional[RobotStatus]:
        return self._latest_status
