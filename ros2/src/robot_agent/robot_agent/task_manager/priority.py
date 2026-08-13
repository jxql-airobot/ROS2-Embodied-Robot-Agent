"""Priority scoring for tasks."""

from __future__ import annotations

from typing import List

from robot_agent.planner.task_schema import Task

#: Weighted priority model.
WEIGHTS = {
    "importance": 0.4,
    "urgency": 0.3,
    "dependency": 0.2,
    "complexity": 0.1,
}


def compute_priority(task: Task) -> float:
    """priority = importance*0.4 + urgency*0.3 + dependency*0.2 + complexity*0.1"""
    return (
        task.importance * WEIGHTS["importance"]
        + task.urgency * WEIGHTS["urgency"]
        + task.dependency * WEIGHTS["dependency"]
        + task.complexity * WEIGHTS["complexity"]
    )


def rank_tasks(tasks: List[Task]) -> List[Task]:
    """Return tasks sorted by priority, highest first."""
    return sorted(tasks, key=compute_priority, reverse=True)
