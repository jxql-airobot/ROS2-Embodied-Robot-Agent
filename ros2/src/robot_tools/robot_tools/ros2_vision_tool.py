"""Ros2VisionTool: agent-facing vision query backed by /vision/detections.

The agent reads perception results over ROS2 (a std_msgs/String carrying the
Scene JSON emitted by ros2_vision_node). This tool never imports YOLO or the
camera driver directly, keeping perception decoupled from planning.
"""

from __future__ import annotations

import json
from typing import Any, Dict, Optional

from rclpy.node import Node
from std_msgs.msg import String


class Ros2VisionTool(Node):
    def __init__(
        self,
        node_name: str = "ros2_vision_tool",
        detections_topic: str = "/vision/detections",
    ) -> None:
        Node.__init__(self, node_name)
        self._detections_topic = detections_topic
        self._latest: Optional[Dict[str, Any]] = None
        self._sub = self.create_subscription(String, detections_topic, self._on_scene, 10)
        self.get_logger().info(f"Ros2VisionTool ready: detections->{detections_topic}")

    def _on_scene(self, msg: String) -> None:
        try:
            self._latest = json.loads(msg.data)
        except (json.JSONDecodeError, TypeError):
            self.get_logger().warn("ignoring malformed /vision/detections message")

    def get_scene(self) -> Optional[Dict[str, Any]]:
        """Return the latest raw Scene dict (or None before the first message)."""
        return self._latest

    def get_objects(self, min_confidence: float = 0.0) -> Dict[str, Any]:
        """Return every object in the latest scene above ``min_confidence``."""
        return self._find(self._latest, "", min_confidence)

    def find_object(self, object_name: str, min_confidence: float = 0.0) -> Dict[str, Any]:
        """Return objects whose name contains ``object_name`` (case-insensitive)."""
        return self._find(self._latest, object_name, min_confidence)

    @staticmethod
    def _find(
        scene: Optional[Dict[str, Any]], object_name: str, min_confidence: float = 0.0
    ) -> Dict[str, Any]:
        """Pure query helper so the matching logic is unit-testable without a node."""
        key = (object_name or "").strip().lower()
        matches = []
        for obj in (scene or {}).get("objects", []):
            name = str(obj.get("name", ""))
            confidence = float(obj.get("confidence", 0.0))
            if confidence < min_confidence:
                continue
            if key and key not in name.lower():
                continue
            center = obj.get("center") or [None, None]
            matches.append(
                {
                    "name": name,
                    "confidence": round(confidence, 4),
                    "position": {"x": center[0], "y": center[1]},
                }
            )
        return {"found": bool(matches), "objects": matches}
