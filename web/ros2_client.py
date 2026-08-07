"""ROS2 client for the Streamlit web GUI.

Design (borrowed from the bachelor project's gui/ros2_client.py):
  - one background node + spin thread keeps /robot_status and /odom snapshots;
  - each task call uses its own short-lived node + synchronous service call,
    so GUI interactions never block the background snapshot loop.
"""

from __future__ import annotations

import atexit
import math
import threading
import time
from typing import Any, Dict, Optional

import rclpy
from nav_msgs.msg import Odometry
from rclpy.node import Node
from robot_interfaces.msg import RobotStatus
from robot_interfaces.srv import TaskExecute


class Ros2Client:
    def __init__(self) -> None:
        if not rclpy.ok():
            rclpy.init(args=[])
        self._lock = threading.Lock()
        self._status: Optional[Dict[str, Any]] = None
        self._odom: Optional[Dict[str, float]] = None

        self._bg_node = Node("robot_web_gui")
        self._bg_node.create_subscription(RobotStatus, "/robot_status", self._on_status, 10)
        self._bg_node.create_subscription(Odometry, "/odom", self._on_odom, 10)

        self._stop = False
        self._spin_thread = threading.Thread(target=self._spin, name="gui-rclpy-spin", daemon=True)
        self._spin_thread.start()
        atexit.register(self.close)

    # ------------------------------------------------------------------ #

    def _spin(self) -> None:
        while not self._stop and rclpy.ok():
            rclpy.spin_once(self._bg_node, timeout_sec=0.05)

    def _on_status(self, msg: RobotStatus) -> None:
        with self._lock:
            self._status = {
                "action": msg.action,
                "state": msg.state,
                "remaining": float(msg.remaining),
                "message": msg.message,
                "time": time.strftime("%H:%M:%S"),
            }

    def _on_odom(self, msg: Odometry) -> None:
        q = msg.pose.pose.orientation
        yaw = math.atan2(2.0 * (q.w * q.z + q.x * q.y), 1.0 - 2.0 * (q.y * q.y + q.z * q.z))
        with self._lock:
            self._odom = {
                "x": msg.pose.pose.position.x,
                "y": msg.pose.pose.position.y,
                "yaw": yaw,
            }

    # ------------------------------------------------------------------ #

    def get_status(self) -> Optional[Dict[str, Any]]:
        with self._lock:
            return self._status

    def get_odom(self) -> Optional[Dict[str, float]]:
        with self._lock:
            return self._odom

    def send_task(self, task: str, timeout: float = 15.0) -> Dict[str, Any]:
        """Synchronously execute a natural-language task via /task_execute."""
        node = Node("robot_web_task")
        try:
            client = node.create_client(TaskExecute, "/task_execute")
            if not client.wait_for_service(timeout_sec=5.0):
                return {
                    "success": False,
                    "response": "未找到 /task_execute 服务，请先启动 robot_agent",
                    "action_json": "",
                }
            request = TaskExecute.Request()
            request.task = task
            future = client.call_async(request)
            rclpy.spin_until_future_complete(node, future, timeout_sec=timeout)
            if future.done() and future.result() is not None:
                result = future.result()
                return {
                    "success": bool(result.success),
                    "response": result.response,
                    "action_json": result.action_json,
                }
            return {"success": False, "response": "任务执行超时", "action_json": ""}
        finally:
            node.destroy_node()

    def close(self) -> None:
        self._stop = True
        if self._spin_thread.is_alive():
            self._spin_thread.join(timeout=2.0)
        try:
            self._bg_node.destroy_node()
        except Exception:
            pass
        if rclpy.ok():
            rclpy.shutdown()
