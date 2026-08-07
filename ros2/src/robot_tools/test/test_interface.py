"""Tests for the RobotTool interface contract."""

import unittest

from robot_tools.base_robot_tool import BaseRobotTool


class _FakeTool(BaseRobotTool):
    """Minimal concrete implementation to validate the abstract contract."""

    def __init__(self):
        self.calls = []

    def move(self, linear_x=0.0, linear_y=0.0, angular_z=0.0, duration=0.0):
        self.calls.append(("move", linear_x, linear_y, angular_z, duration))
        return True

    def stop(self):
        self.calls.append(("stop",))
        return True

    def rotate(self, angular_z, duration=0.0):
        self.calls.append(("rotate", angular_z, duration))
        return True

    def navigate(self, goal, **kwargs):
        self.calls.append(("navigate", goal))
        return True

    def get_pose(self):
        return {"x": 0.0, "y": 0.0, "yaw": 0.0, "stamp": 0.0}

    def get_sensor(self, name):
        return {"name": name, "available": False}

    def execute_action(self, action):
        self.calls.append(("execute_action", action))
        return True


class TestRobotToolContract(unittest.TestCase):
    def test_abstract_class_cannot_instantiate(self):
        with self.assertRaises(TypeError):
            BaseRobotTool()  # type: ignore[abstract]

    def test_fake_tool_implements_all_methods(self):
        tool = _FakeTool()
        self.assertTrue(tool.move(linear_x=0.3, duration=2.0))
        self.assertTrue(tool.stop())
        self.assertTrue(tool.rotate(0.5))
        self.assertTrue(tool.navigate("kitchen"))
        self.assertIsNotNone(tool.get_pose())
        self.assertFalse(tool.get_sensor("camera")["available"])
        self.assertTrue(tool.execute_action({"action": "stop"}))


if __name__ == "__main__":
    unittest.main()
