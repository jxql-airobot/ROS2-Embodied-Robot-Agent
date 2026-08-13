"""Integration-style test: the agent routes a vision action to the vision tool."""

import unittest

import rclpy

from robot_agent.llm import MockLLM
from robot_agent.robot_agent_node import RobotAgentNode


class _FakeVisionTool:
    def __init__(self):
        self.last_query = None

    def find_object(self, name):
        self.last_query = ("find", name)
        return {
            "found": True,
            "objects": [
                {"name": name, "confidence": 0.93, "position": {"x": 320.0, "y": 240.0}}
            ],
        }

    def get_objects(self):
        self.last_query = ("scene", "")
        return {"found": True, "objects": []}


class _FakeRobotTool:
    def execute_action(self, action):
        return True


class TestAgentVisionRouting(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        rclpy.init()

    @classmethod
    def tearDownClass(cls):
        rclpy.shutdown()

    def setUp(self):
        self.vision = _FakeVisionTool()
        self.agent = RobotAgentNode(
            llm=MockLLM(), tool=_FakeRobotTool(), vision_tool=self.vision
        )

    def tearDown(self):
        self.agent.destroy_node()

    def test_find_object_routes_to_vision_tool(self):
        ok, response, action_json = self.agent.handle_task("帮我找杯子")
        self.assertTrue(ok)
        self.assertEqual(self.vision.last_query, ("find", "cup"))
        self.assertIn("cup", response)
        self.assertIn("cup", action_json)

    def test_scene_query_routes_to_vision_tool(self):
        ok, response, action_json = self.agent.handle_task("场景中有什么物体？")
        self.assertTrue(ok)
        self.assertEqual(self.vision.last_query, ("scene", ""))
        self.assertIn("未检测到", response)


if __name__ == "__main__":
    unittest.main()
