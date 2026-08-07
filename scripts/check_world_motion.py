#!/usr/bin/env python3
"""Ground-truth motion check using /gazebo/model_states.

Publishes a move command to /robot_command, then reports the world pose
of simple_diffbot before / after (bypasses the agent, pure physics test).
"""

from __future__ import annotations

import math

import rclpy
from gazebo_msgs.msg import ModelStates
from rclpy.duration import Duration
from rclpy.node import Node
from robot_interfaces.msg import RobotCommand


def yaw_of(q) -> float:
    return math.atan2(2.0 * (q.w * q.z + q.x * q.y), 1.0 - 2.0 * (q.y * q.y + q.z * q.z))


def main() -> int:
    rclpy.init()
    node = Node("world_motion_check")
    poses: dict = {}

    def on_states(msg: ModelStates) -> None:
        for name, pose in zip(msg.name, msg.pose):
            if name == "simple_diffbot":
                poses[name] = (pose.position.x, pose.position.y, yaw_of(pose.orientation))

    node.create_subscription(ModelStates, "/gazebo/model_states", on_states, 10)

    def wait_for_pose(seconds: float) -> bool:
        deadline = node.get_clock().now() + Duration(seconds=seconds)
        while node.get_clock().now() < deadline:
            rclpy.spin_once(node, timeout_sec=0.1)
            if "simple_diffbot" in poses:
                return True
        return False

    if not wait_for_pose(90.0):
        print("FAIL: no model_states for simple_diffbot")
        node.destroy_node()
        rclpy.shutdown()
        return 1

    before = poses["simple_diffbot"]
    print(f"before: x={before[0]:.4f} y={before[1]:.4f} yaw={before[2]:.4f}")

    publisher = node.create_publisher(RobotCommand, "/robot_command", 10)
    cmd = RobotCommand()
    cmd.action = "move"
    cmd.linear_x = 0.3
    cmd.duration = 2.0
    publisher.publish(cmd)
    print("published move vx=0.3 duration=2.0 to /robot_command")

    deadline = node.get_clock().now() + Duration(seconds=3.5)
    while node.get_clock().now() < deadline:
        rclpy.spin_once(node, timeout_sec=0.1)
        publisher.publish(cmd)  # keep refreshing so late subscribers still get it

    after = poses["simple_diffbot"]
    print(f"after : x={after[0]:.4f} y={after[1]:.4f} yaw={after[2]:.4f}")
    dx = after[0] - before[0]
    dy = after[1] - before[1]
    dist = math.hypot(dx, dy)
    print(f"delta : dx={dx:.4f} dy={dy:.4f} dist={dist:.4f}")

    # A forward move should go mostly along +X of the odom/world frame
    moved = dist >= 0.05
    forward = abs(dx) >= 0.8 * dist if dist > 1e-6 else False
    print("RESULT:", "PASS" if moved and forward else "SUSPECT")
    node.destroy_node()
    rclpy.shutdown()
    return 0 if moved and forward else 2


if __name__ == "__main__":
    raise SystemExit(main())
