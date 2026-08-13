"""Pick the next pending task by priority."""

from __future__ import annotations

from typing import Callable, List, Optional

from robot_agent.planner.task_schema import Task
from robot_agent.task_manager.priority import compute_priority
from robot_agent.task_manager.task_state import TaskStatus


class Scheduler:
    def __init__(self, priority_fn: Callable[[Task], float] = compute_priority) -> None:
        self._priority_fn = priority_fn

    def next_task(self, tasks: List[Task]) -> Optional[Task]:
        pending = [t for t in tasks if t.status == TaskStatus.PENDING.value]
        if not pending:
            return None
        return max(pending, key=self._priority_fn)
