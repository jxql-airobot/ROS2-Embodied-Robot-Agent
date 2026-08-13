"""Unit tests for the offline rule-based LLM provider."""

import unittest

from robot_agent.llm import LLMError, MockLLM


class TestMockLLM(unittest.TestCase):
    def setUp(self):
        self.llm = MockLLM()

    def test_forward_chinese(self):
        plan = self.llm.generate_action("让机器人向前移动")
        self.assertEqual(plan.action, "move")
        self.assertGreater(plan.linear_x, 0)
        self.assertGreater(plan.duration, 0)

    def test_forward_english(self):
        plan = self.llm.generate_action("move forward")
        self.assertEqual(plan.action, "move")
        self.assertGreater(plan.linear_x, 0)

    def test_backward_distance(self):
        plan = self.llm.generate_action("后退半米")
        self.assertEqual(plan.action, "move")
        self.assertLess(plan.linear_x, 0)
        self.assertAlmostEqual(plan.duration, 0.5 / 0.3, places=2)

    def test_rotate_left_degrees(self):
        plan = self.llm.generate_action("左转90度")
        self.assertEqual(plan.action, "rotate")
        self.assertGreater(plan.angular_z, 0)
        self.assertAlmostEqual(plan.duration, 90 * 3.141592653589793 / 180.0 / 0.5, places=1)

    def test_rotate_right(self):
        plan = self.llm.generate_action("右转")
        self.assertEqual(plan.action, "rotate")
        self.assertLess(plan.angular_z, 0)

    def test_stop(self):
        plan = self.llm.generate_action("停止")
        self.assertEqual(plan.action, "stop")

    def test_navigate(self):
        plan = self.llm.generate_action("去厨房")
        self.assertEqual(plan.action, "navigate")
        self.assertEqual(plan.goal, "厨房")

    def test_navigate_english(self):
        plan = self.llm.generate_action("go to kitchen")
        self.assertEqual(plan.action, "navigate")
        self.assertEqual(plan.goal, "kitchen")

    def test_unknown_task_raises(self):
        with self.assertRaises(LLMError):
            self.llm.generate_action("讲个笑话")

    def test_vision_find_chinese(self):
        plan = self.llm.generate_action("帮我找杯子")
        self.assertEqual(plan.action, "approach")
        self.assertEqual(plan.goal, "cup")

    def test_vision_find_english(self):
        plan = self.llm.generate_action("find a cup")
        self.assertEqual(plan.action, "approach")
        self.assertEqual(plan.goal, "cup")

    def test_vision_scene(self):
        plan = self.llm.generate_action("场景中有什么物体？")
        self.assertEqual(plan.action, "vision")
        self.assertEqual(plan.goal, "")

    def test_plan_motion_left(self):
        vision = {"found": True, "objects": [{"direction": "left"}]}
        plan = self.llm.plan_motion("找杯子", vision)
        self.assertEqual(plan.action, "rotate")
        self.assertGreater(plan.angular_z, 0)

    def test_plan_motion_center(self):
        vision = {"found": True, "objects": [{"direction": "center"}]}
        plan = self.llm.plan_motion("找杯子", vision)
        self.assertEqual(plan.action, "move")
        self.assertGreater(plan.linear_x, 0)

    def test_plan_motion_no_target(self):
        plan = self.llm.plan_motion("找杯子", {"found": False, "objects": []})
        self.assertEqual(plan.action, "stop")


if __name__ == "__main__":
    unittest.main()
