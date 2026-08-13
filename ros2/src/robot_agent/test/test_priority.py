"""Unit tests for task priority and ranking."""

import unittest

from robot_agent.planner.task_schema import Task
from robot_agent.task_manager.priority import compute_priority, rank_tasks


class TestPriority(unittest.TestCase):
    def test_formula(self):
        task = Task(
            id=1,
            tool="robot",
            action="charge",
            importance=100,
            urgency=100,
            complexity=100,
            dependency=100,
        )
        self.assertAlmostEqual(compute_priority(task), 100.0)

    def test_charging_task_ranks_highest(self):
        tasks = [
            Task(id=1, tool="robot", action="move", name="move", importance=50, urgency=50, complexity=50),
            Task(id=2, tool="robot", action="log", name="log", importance=30, urgency=30, complexity=30),
            Task(
                id=3,
                tool="robot",
                action="charge",
                name="charge",
                importance=100,
                urgency=100,
                complexity=100,
                dependency=100,
            ),
        ]
        ranked = rank_tasks(tasks)
        self.assertEqual(ranked[0].name, "charge")


if __name__ == "__main__":
    unittest.main()
