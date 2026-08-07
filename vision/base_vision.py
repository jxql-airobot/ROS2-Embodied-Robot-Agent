"""Unified vision interface (roadmap: YOLO -> GPT Vision / Gemini / Qwen-VL)."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

from vision.vision_schema import Scene


class BaseVision(ABC):
    """Contract between the robot's perception and the agent.

    Implementations:
      - YOLODetector  : real-time object detection (this repo)
      - future        : VLM (GPT-4o / Gemini / Qwen-VL) describing scenes

    The agent never cares which backend is used.
    """

    backend_name: str = "base"

    @abstractmethod
    def detect(self, image: Any) -> Scene:
        """Detect objects in `image` (numpy BGR / path / PIL) and return a Scene."""
