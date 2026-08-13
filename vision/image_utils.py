"""Pure image conversion helpers shared by the ROS2 vision node and tests.

Kept free of ROS imports so the conversion can be unit-tested without a ROS
environment. A ROS ``sensor_msgs/Image`` payload is raw bytes laid out as
(rows, cols, channels); the channel order is described by ``encoding``.
"""

from __future__ import annotations

import cv2
import numpy as np


def ros_image_to_bgr(data: bytes, height: int, width: int, encoding: str = "bgr8"):
    """Convert a ROS image payload to an OpenCV BGR numpy array.

    YOLO (and OpenCV in general) treats a 3-channel numpy array as BGR, while
    Gazebo cameras usually publish ``rgb8``. This helper converts RGB -> BGR
    when needed and expands monochrome frames to 3 channels so colour-sensitive
    detections are not corrupted.
    """
    frame = np.frombuffer(data, dtype=np.uint8).reshape(height, width, -1)
    enc = (encoding or "bgr8").lower()

    if frame.shape[2] >= 3:
        frame = frame[:, :, :3]
        if enc.startswith("rgb"):
            return cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        return frame  # bgr8 / bgra8: BGR channel order already

    # monochrome (mono8 etc.) -> 3-channel BGR
    return cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR)
