"""Unit tests for ActionPlan validation/normalization."""

import unittest

from robot_agent.action_plan import ActionPlan


class TestActionPlan(unittest.TestCase):
    def test_from_dict_valid(self):
        plan = ActionPlan.from_dict({"action": "move", "linear_x": 0.3, "duration": 2.0})
        self.assertEqual(plan.action, "move")
        self.assertAlmostEqual(plan.linear_x, 0.3)
        self.assertEqual(plan.duration, 2.0)

    def test_from_dict_rejects_unknown_action(self):
        with self.assertRaises(ValueError):
            ActionPlan.from_dict({"action": "fly"})

    def test_to_command_dict_excludes_response(self):
        plan = ActionPlan("move", linear_x=0.3, duration=2.0, response="ok")
        command = plan.to_command_dict()
        self.assertNotIn("response", command)
        self.assertEqual(command["action"], "move")
        self.assertAlmostEqual(command["linear_x"], 0.3)

    def test_action_lowercased(self):
        plan = ActionPlan.from_dict({"action": "STOP"})
        self.assertEqual(plan.action, "stop")

    def test_vision_action_is_allowed(self):
        plan = ActionPlan.from_dict({"action": "vision", "goal": "cup"})
        self.assertEqual(plan.action, "vision")
        self.assertEqual(plan.goal, "cup")

    def test_approach_action_is_allowed(self):
        plan = ActionPlan.from_dict({"action": "approach", "goal": "cup"})
        self.assertEqual(plan.action, "approach")
        self.assertEqual(plan.goal, "cup")


if __name__ == "__main__":
    unittest.main()
