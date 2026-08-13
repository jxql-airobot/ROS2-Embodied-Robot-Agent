"""Abstract high-level planner interface."""

from __future__ import annotations

from abc import ABC, abstractmethod

from robot_agent.executor.base_executor import TaskResult
from robot_agent.planner.task_schema import Plan, Task


class BasePlanner(ABC):
    """Decompose a high-level goal into a Plan; re-plan on failure."""

    @abstractmethod
    def plan(self, goal: str) -> Plan:
        """Decompose ``goal`` into an ordered list of Tasks."""

    @abstractmethod
    def replan(self, goal: str, task: Task, result: TaskResult) -> Plan:
        """Produce recovery tasks after ``task`` fails with ``result``."""
