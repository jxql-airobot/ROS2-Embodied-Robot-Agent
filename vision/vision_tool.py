"""VisionTool: agent-facing vision capability (get_scene / find_object)."""

from __future__ import annotations

from typing import Any, List, Optional

from vision.base_vision import BaseVision
from vision.vision_schema import Detection, Scene


class VisionTool:
    """Wraps a BaseVision backend for the agent (similar role to RobotTool)."""

    def __init__(self, vision: BaseVision) -> None:
        self._vision = vision

    @property
    def backend_name(self) -> str:
        return self._vision.backend_name

    def get_scene(self, image: Any = None) -> Scene:
        """Describe the current scene."""
        return self._vision.detect(image)

    def find_object(self, name: str, image: Any = None) -> List[Detection]:
        """Find objects matching `name` in the latest scene."""
        return self._vision.detect(image).find(name)
