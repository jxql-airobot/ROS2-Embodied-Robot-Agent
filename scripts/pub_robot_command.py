#!/usr/bin/env python3
"""Publish a RobotCommand (e.g. move) to /robot_command a few times."""

from __future__ import annotations

import argparse

import rclpy
from rclpy.node import Node
from robot_interfaces.msg import RobotCommand


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--action", default="move")
    parser.add_argument("--linear-x", type=float, default=0.0)
    parser.add_argument("--angular-z", type=float, default=0.0)
    parser.add_argument("--duration", type=float, default=0.0)
    args = parser.parse_args()

    rclpy.init()
    node = Node("pub_robot_command")
    publisher = node.create_publisher(RobotCommand, "/robot_command", 10)
    cmd = RobotCommand()
    cmd.action = args.action
    cmd.linear_x = args.linear_x
    cmd.angular_z = args.angular_z
    cmd.duration = args.duration

    for _ in range(10):
        publisher.publish(cmd)
        rclpy.spin_once(node, timeout_sec=0.1)
    node.destroy_node()
    rclpy.shutdown()
    print(f"published {args.action} vx={args.linear_x} wz={args.angular_z} dur={args.duration}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
