#!/usr/bin/env python3
"""Print the latest /odom pose (x y yaw) once."""

from __future__ import annotations

import math

import rclpy
from nav_msgs.msg import Odometry
from rclpy.node import Node


def main() -> int:
    rclpy.init()
    node = Node("odom_pose_once")
    result: dict = {}

    def on_odom(msg: Odometry) -> None:
        q = msg.pose.pose.orientation
        yaw = math.atan2(2.0 * (q.w * q.z + q.x * q.y), 1.0 - 2.0 * (q.y * q.y + q.z * q.z))
        result["x"] = msg.pose.pose.position.x
        result["y"] = msg.pose.pose.position.y
        result["yaw"] = yaw

    node.create_subscription(Odometry, "/odom", on_odom, 10)
    deadline = node.get_clock().now() + rclpy.duration.Duration(seconds=10.0)
    while node.get_clock().now() < deadline and "x" not in result:
        rclpy.spin_once(node, timeout_sec=0.1)
    node.destroy_node()
    rclpy.shutdown()

    if "x" not in result:
        print("FAIL: no /odom sample")
        return 1
    print(f"x={result['x']:.4f} y={result['y']:.4f} yaw={result['yaw']:.4f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
