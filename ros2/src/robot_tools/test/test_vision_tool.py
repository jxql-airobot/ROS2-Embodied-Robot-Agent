"""Unit tests for Ros2VisionTool query logic (no running node needed)."""

import unittest

from robot_tools.ros2_vision_tool import Ros2VisionTool


SCENE = {
    "image_width": 640,
    "image_height": 480,
    "source": "yolo",
    "objects": [
        {"name": "cup", "confidence": 0.92, "bbox": [300, 220, 340, 260], "center": [320, 240]},
        {"name": "person", "confidence": 0.8, "bbox": [100, 50, 200, 400], "center": [150, 225]},
    ],
}


class TestVisionToolQuery(unittest.TestCase):
    def test_find_object_matches_case_insensitive(self):
        result = Ros2VisionTool._find(SCENE, "CUP")
        self.assertTrue(result["found"])
        self.assertEqual(len(result["objects"]), 1)
        obj = result["objects"][0]
        self.assertEqual(obj["name"], "cup")
        self.assertAlmostEqual(obj["confidence"], 0.92)
        self.assertEqual(obj["position"], {"x": 320, "y": 240})

    def test_get_objects_returns_all(self):
        result = Ros2VisionTool._find(SCENE, "")
        self.assertTrue(result["found"])
        self.assertEqual(len(result["objects"]), 2)

    def test_min_confidence_filters(self):
        result = Ros2VisionTool._find(SCENE, "", 0.9)
        self.assertEqual([o["name"] for o in result["objects"]], ["cup"])

    def test_no_match_returns_empty(self):
        result = Ros2VisionTool._find(SCENE, "bottle")
        self.assertFalse(result["found"])
        self.assertEqual(result["objects"], [])

    def test_empty_scene(self):
        result = Ros2VisionTool._find(None, "cup")
        self.assertFalse(result["found"])
        self.assertEqual(result["objects"], [])

    def test_result_json_shape_is_stable(self):
        obj = Ros2VisionTool._find(SCENE, "cup")["objects"][0]
        self.assertEqual(set(obj.keys()), {"name", "confidence", "position"})
        self.assertEqual(set(obj["position"].keys()), {"x", "y"})


if __name__ == "__main__":
    unittest.main()
