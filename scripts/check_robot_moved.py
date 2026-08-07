#!/usr/bin/env python3
"""Subscribe /odom for a few seconds and report whether the robot moved.

Exit code 0 = moved at least --threshold meters (demo closed-loop check).
"""

from __future__ import annotations

import argparse
import math

import rclpy
from nav_msgs.msg import Odometry
from rclpy.duration import Duration
from rclpy.node import Node


def main() -> int:
    parser = argparse.ArgumentParser(description="Verify robot displacement via /odom")
    parser.add_argument("--duration", type=float, default=2.0)
    parser.add_argument("--threshold", type=float, default=0.05)
    args = parser.parse_args()

    rclpy.init()
    node = Node("odom_checker")
    samples: list[tuple[float, float]] = []

    def on_odom(msg: Odometry) -> None:
        samples.append((msg.pose.pose.position.x, msg.pose.pose.position.y))

    node.create_subscription(Odometry, "/odom", on_odom, 10)
    end_time = node.get_clock().now() + Duration(seconds=args.duration)
    while node.get_clock().now() < end_time:
        rclpy.spin_once(node, timeout_sec=0.1)

    node.destroy_node()
    rclpy.shutdown()

    if len(samples) < 2:
        print("FAIL: no /odom samples received")
        return 1

    x0, y0 = samples[0]
    x1, y1 = samples[-1]
    displacement = math.hypot(x1 - x0, y1 - y0)
    print(
        f"odom samples={len(samples)} "
        f"displacement={displacement:.3f} m (threshold={args.threshold})"
    )
    return 0 if displacement >= args.threshold else 1


if __name__ == "__main__":
    raise SystemExit(main())
