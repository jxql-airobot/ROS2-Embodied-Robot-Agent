"""Abstract executor interface + result type."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Dict

from robot_agent.planner.task_schema import Task


@dataclass
class TaskResult:
    """Outcome of executing a single Task."""

    task_id: int
    success: bool
    message: str = ""
    data: Dict[str, Any] = field(default_factory=dict)


class BaseExecutor(ABC):
    """Contract for a low-level executor that dispatches one Task to a tool."""

    @abstractmethod
    def execute(self, task: Task, context: Dict[str, Any]) -> TaskResult:
        """Execute ``task`` using tools, returning a TaskResult."""
