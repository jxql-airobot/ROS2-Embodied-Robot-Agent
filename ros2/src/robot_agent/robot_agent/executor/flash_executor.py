"""FlashExecutor: dispatch one Task to VisionTool / RobotTool / NavTool."""

from __future__ import annotations

from typing import Any, Dict, Optional

from robot_agent.executor.base_executor import BaseExecutor, TaskResult
from robot_agent.llm import BaseLLM, LLMError
from robot_agent.planner.task_schema import Task


class FlashExecutor(BaseExecutor):
    """Executes a single task, calling tools directly (fast, low-level)."""

    def __init__(
        self,
        robot_tool: Any = None,
        vision_tool: Any = None,
        llm: Optional[BaseLLM] = None,
    ) -> None:
        self._robot = robot_tool
        self._vision = vision_tool
        self._llm = llm

    def execute(self, task: Task, context: Dict[str, Any]) -> TaskResult:
        try:
            if task.tool == "vision":
                return self._run_vision(task)
            if task.tool == "robot":
                return self._run_robot(task, context)
            if task.tool == "nav":
                return TaskResult(task.id, False, "nav tool not implemented yet")
            return TaskResult(task.id, False, f"unknown tool: {task.tool}")
        except Exception as exc:  # keep the loop alive on unexpected errors
            return TaskResult(task.id, False, f"executor error: {exc}")

    def _run_vision(self, task: Task) -> TaskResult:
        if self._vision is None:
            return TaskResult(task.id, False, "vision tool unavailable")
        if task.action in ("find_object", "find"):
            data = self._vision.find_object(task.target)
            if isinstance(data, dict) and not data.get("found", True):
                return TaskResult(task.id, False, f"no target found: {task.target}", data=data)
            return TaskResult(task.id, True, "vision ok", data={"vision": data})
        elif task.action in ("observe", "scene", "get_objects"):
            data = self._vision.get_objects()
        else:
            data = self._vision.get_scene()
        return TaskResult(task.id, True, "vision ok", data={"vision": data})

    def _run_robot(self, task: Task, context: Dict[str, Any]) -> TaskResult:
        if self._robot is None:
            return TaskResult(task.id, False, "robot tool unavailable")
        if task.action == "infer":
            if self._llm is None:
                return TaskResult(task.id, False, "no LLM for infer action")
            plan = self._llm.generate_action(task.target)
            if plan.action == "vision" or plan.action == "approach":
                return TaskResult(task.id, False, "infer resolved to non-motion action")
            self._robot.execute_action(plan.to_command_dict())
            return TaskResult(task.id, True, plan.response or plan.action, data={"action": plan.to_command_dict()})

        if task.action in ("move", "rotate", "stop"):
            if task.action == "stop":
                self._robot.stop()
                return TaskResult(task.id, True, "stopped")
            if task.action == "rotate":
                self._robot.rotate(
                    float(task.params.get("angular_z", 0.5)),
                    float(task.params.get("duration", 1.0)),
                )
                return TaskResult(task.id, True, "rotated")
            # move: use vision context when available, else explicit params
            if self._llm is not None and context.get("vision") is not None:
                motion = self._llm.plan_motion(context.get("goal", task.target), context["vision"])
                if motion.action == "stop":
                    return TaskResult(task.id, False, "cannot plan motion from vision")
                self._robot.execute_action(motion.to_command_dict())
                return TaskResult(task.id, True, motion.response or "moved", data={"action": motion.to_command_dict()})
            self._robot.move(
                float(task.params.get("linear_x", 0.3)),
                float(task.params.get("linear_y", 0.0)),
                float(task.params.get("angular_z", 0.0)),
                float(task.params.get("duration", 1.0)),
            )
            return TaskResult(task.id, True, "moved")

        return TaskResult(task.id, False, f"unknown robot action: {task.action}")
