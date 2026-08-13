"""Unit tests for ROS image -> BGR conversion (no ROS / model needed)."""

import unittest

from vision.image_utils import ros_image_to_bgr


class TestRosImageToBgr(unittest.TestCase):
    def test_rgb8_is_converted_to_bgr(self):
        # 1x1 pure red pixel: RGB (255, 0, 0) -> BGR (0, 0, 255)
        frame = ros_image_to_bgr(bytes([255, 0, 0]), 1, 1, "rgb8")
        self.assertEqual(frame.shape, (1, 1, 3))
        self.assertEqual(list(frame[0, 0]), [0, 0, 255])

    def test_bgr8_passthrough(self):
        frame = ros_image_to_bgr(bytes([1, 2, 3]), 1, 1, "bgr8")
        self.assertEqual(list(frame[0, 0]), [1, 2, 3])

    def test_rgba8_drops_alpha_and_converts(self):
        # RGBA (255, 0, 0, 128) -> BGR (0, 0, 255)
        frame = ros_image_to_bgr(bytes([255, 0, 0, 128]), 1, 1, "rgba8")
        self.assertEqual(frame.shape, (1, 1, 3))
        self.assertEqual(list(frame[0, 0]), [0, 0, 255])

    def test_mono8_expands_to_three_channels(self):
        frame = ros_image_to_bgr(bytes([128]), 1, 1, "mono8")
        self.assertEqual(frame.shape, (1, 1, 3))
        self.assertEqual(list(frame[0, 0]), [128, 128, 128])


if __name__ == "__main__":
    unittest.main()
