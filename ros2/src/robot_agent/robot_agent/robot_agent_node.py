"""robot_agent node: NL task -> LLM -> structured action -> Ros2RobotTool.

Inputs:
  - topic   /task_input   (std_msgs/String)
  - service /task_execute (robot_interfaces/TaskExecute)
Outputs:
  - topic   /robot_command (RobotCommand, via Ros2RobotTool)
"""

from __future__ import annotations

import json
from typing import Optional

import rclpy
from rclpy.executors import MultiThreadedExecutor
from rclpy.node import Node
from robot_interfaces.srv import TaskExecute
from std_msgs.msg import String

from robot_agent.llm import BaseLLM, LLMError, load_llm
from robot_tools.ros2_robot_tool import Ros2RobotTool


class RobotAgentNode(Node):
    def __init__(
        self,
        llm: Optional[BaseLLM] = None,
        tool: Optional[Ros2RobotTool] = None,
    ) -> None:
        super().__init__("robot_agent")

        self.declare_parameter("task_input_topic", "/task_input")
        self.declare_parameter("task_service", "/task_execute")
        self.declare_parameter("llm_config", "")
        self.declare_parameter("llm_provider", "")  # optional override of config
        self.declare_parameter("tool_command_topic", "/robot_command")
        self.declare_parameter("tool_status_topic", "/robot_status")
        self.declare_parameter("tool_odom_topic", "/odom")

        task_input_topic = self.get_parameter("task_input_topic").value
        task_service = self.get_parameter("task_service").value

        self._llm = llm if llm is not None else self._make_llm()
        self._tool = tool if tool is not None else Ros2RobotTool(
            command_topic=self.get_parameter("tool_command_topic").value,
            status_topic=self.get_parameter("tool_status_topic").value,
            odom_topic=self.get_parameter("tool_odom_topic").value,
        )

        self._task_sub = self.create_subscription(
            String, task_input_topic, self._on_task_input, 10
        )
        self._task_srv = self.create_service(
            TaskExecute, task_service, self._on_task_service
        )

        self.get_logger().info(
            f"robot_agent ready: topic={task_input_topic}, service={task_service}, "
            f"llm={type(self._llm).__name__}"
        )

    # ------------------------------------------------------------------ #

    @property
    def tool(self) -> Ros2RobotTool:
        return self._tool

    def _make_llm(self) -> BaseLLM:
        config_path = str(self.get_parameter("llm_config").value)
        config = {}
        if config_path:
            try:
                import yaml
            except ImportError as exc:  # pragma: no cover
                raise LLMError("PyYAML not installed; cannot read LLM config") from exc
            with open(config_path, "r", encoding="utf-8") as f:
                config = yaml.safe_load(f) or {}
        provider_override = str(self.get_parameter("llm_provider").value)
        if provider_override:
            config["provider"] = provider_override
        return load_llm(config)

    def handle_task(self, task: str) -> tuple[bool, str, str]:
        """Run one NL task. Returns (success, response, action_json)."""
        try:
            plan = self._llm.generate_action(task)
            action_json = json.dumps(plan.to_command_dict(), ensure_ascii=False)
            ok = self._tool.execute_action(plan.to_command_dict())
            if ok:
                self.get_logger().info(f"task='{task}' -> {action_json}")
                response = plan.response or f"已执行动作：{plan.action}"
                return True, response, action_json
            return False, "执行层受理失败", action_json
        except LLMError as exc:
            self.get_logger().warn(f"LLM error for task '{task}': {exc}")
            return False, str(exc), ""
        except Exception as exc:  # keep the node alive on unexpected errors
            self.get_logger().error(f"unexpected error for task '{task}': {exc}")
            return False, f"内部错误：{exc}", ""

    def _on_task_input(self, msg: String) -> None:
        success, response, _ = self.handle_task(msg.data)
        self.get_logger().info(f"[task done] success={success} response={response}")

    def _on_task_service(self, request, response) -> TaskExecute.Response:
        response.success, response.response, response.action_json = self.handle_task(request.task)
        return response


def main(args=None) -> None:
    rclpy.init(args=args)
    agent = RobotAgentNode()
    executor = MultiThreadedExecutor()
    executor.add_node(agent)
    executor.add_node(agent.tool)
    try:
        executor.spin()
    except KeyboardInterrupt:
        pass
    finally:
        executor.shutdown()
        agent.tool.destroy_node()
        agent.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == "__main__":
    main()
