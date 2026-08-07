"""CLI: send a natural-language task to robot_agent.

Examples:
  ros2 run robot_agent send_task "让机器人向前移动"
  ros2 run robot_agent send_task "让机器人向前移动" --service
"""

from __future__ import annotations

import argparse

import rclpy
from rclpy.node import Node
from robot_interfaces.srv import TaskExecute
from std_msgs.msg import String


def main() -> int:
    parser = argparse.ArgumentParser(description="Send a natural-language task to robot_agent")
    parser.add_argument("task", help="task text, e.g. 让机器人向前移动")
    parser.add_argument(
        "--service", action="store_true", help="use the /task_execute service instead of topic"
    )
    parser.add_argument("--timeout", type=float, default=10.0, help="service call timeout (s)")
    args = parser.parse_args()

    rclpy.init()
    node = Node("send_task")
    try:
        if args.service:
            client = node.create_client(TaskExecute, "/task_execute")
            if not client.wait_for_service(timeout_sec=5.0):
                print("ERROR: /task_execute service not available")
                return 1
            request = TaskExecute.Request()
            request.task = args.task
            future = client.call_async(request)
            rclpy.spin_until_future_complete(node, future, timeout_sec=args.timeout)
            if not future.done() or future.result() is None:
                print("ERROR: task execution timed out or failed")
                return 1
            result = future.result()
            print(f"success    : {result.success}")
            print(f"response   : {result.response}")
            print(f"action_json: {result.action_json}")
            return 0 if result.success else 2

        publisher = node.create_publisher(String, "/task_input", 10)
        msg = String()
        msg.data = args.task
        for _ in range(5):  # a few publishes so a late-joining subscriber still receives it
            publisher.publish(msg)
            rclpy.spin_once(node, timeout_sec=0.2)
        print(f"published task to /task_input: {args.task}")
        return 0
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    raise SystemExit(main())
