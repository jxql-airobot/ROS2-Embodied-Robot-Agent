"""Unit tests for natural-language vision result formatting."""

import unittest

from robot_agent.vision_response import format_vision_result


class TestFormatVisionResult(unittest.TestCase):
    def test_scene_lists_objects(self):
        result = {
            "found": True,
            "objects": [
                {"name": "cup", "confidence": 0.92, "position": {"x": 320.0, "y": 240.0}},
            ],
        }
        text = format_vision_result(result, "")
        self.assertIn("检测到以下物体", text)
        self.assertIn("cup", text)
        self.assertIn("0.92", text)

    def test_find_specific_object(self):
        result = {
            "found": True,
            "objects": [
                {"name": "cup", "confidence": 0.92, "position": {"x": 320.0, "y": 240.0}},
            ],
        }
        text = format_vision_result(result, "cup")
        self.assertIn("找到 cup", text)

    def test_find_missing_object(self):
        text = format_vision_result({"found": False, "objects": []}, "cup")
        self.assertIn("未找到 cup", text)

    def test_empty_scene(self):
        text = format_vision_result({"found": False, "objects": []}, "")
        self.assertIn("未检测到", text)


if __name__ == "__main__":
    unittest.main()
