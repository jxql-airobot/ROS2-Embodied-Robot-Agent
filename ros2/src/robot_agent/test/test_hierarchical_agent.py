"""Integration tests for the HierarchicalAgent (Pro -> Manager -> Flash)."""

import unittest

from robot_agent.hierarchical_agent import build_hierarchical_agent


class _FakeRobotTool:
    def __init__(self):
        self.actions = []

    def execute_action(self, action):
        self.actions.append(action)
        return True

    def move(self, linear_x=0.0, linear_y=0.0, angular_z=0.0, duration=0.0):
        self.actions.append(
            {"action": "move", "linear_x": linear_x, "linear_y": linear_y, "angular_z": angular_z, "duration": duration}
        )
        return True

    def rotate(self, angular_z, duration=0.0):
        self.actions.append({"action": "rotate", "angular_z": angular_z, "duration": duration})
        return True

    def stop(self):
        self.actions.append({"action": "stop"})
        return True


class _FakeVisionTool:
    def __init__(self, found=True, direction="center"):
        self.found = found
        self.direction = direction
        self.last_query = None

    def find_object(self, name):
        self.last_query = ("find", name)
        if not self.found:
            return {"found": False, "objects": []}
        return {
            "found": True,
            "objects": [
                {"name": name, "confidence": 0.9, "center_x": 320.0, "center_y": 240.0, "direction": self.direction}
            ],
        }

    def get_objects(self):
        self.last_query = ("scene", "")
        return {"found": self.found, "objects": []}

    def get_scene(self):
        return {"found": self.found, "objects": []}


class TestHierarchicalAgent(unittest.TestCase):
    def test_complex_find_then_move(self):
        vision = _FakeVisionTool(found=True, direction="center")
        robot = _FakeRobotTool()
        agent = build_hierarchical_agent({"provider": "mock"}, robot_tool=robot, vision_tool=vision)
        results = agent.run("找到杯子然后移动过去")
        self.assertTrue(results)
        self.assertEqual(vision.last_query, ("find", "cup"))
        self.assertTrue(any(a.get("action") == "move" for a in robot.actions))
        self.assertTrue(all(r.success for r in results))

    def test_simple_stop_goes_straight_to_flash(self):
        robot = _FakeRobotTool()
        agent = build_hierarchical_agent({"provider": "mock"}, robot_tool=robot, vision_tool=None)
        results = agent.run("停止机器人")
        self.assertEqual(len(results), 1)
        self.assertTrue(results[0].success)
        self.assertEqual(robot.actions[0].get("action"), "stop")

    def test_failure_recovery_replans_search(self):
        vision = _FakeVisionTool(found=False)
        robot = _FakeRobotTool()
        agent = build_hierarchical_agent({"provider": "mock"}, robot_tool=robot, vision_tool=vision)
        results = agent.run("找到杯子然后移动过去")
        self.assertTrue(any(not r.success for r in results))
        self.assertTrue(any(a.get("action") == "rotate" for a in robot.actions))


if __name__ == "__main__":
    unittest.main()
