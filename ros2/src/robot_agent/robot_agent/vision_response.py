"""Format Ros2VisionTool results into natural-language feedback."""

from __future__ import annotations

from typing import Any, Dict


def format_vision_result(result: Dict[str, Any], goal: str = "") -> str:
    """Turn a ``{found, objects:[...]}`` dict into a human-readable answer."""
    objects = result.get("objects", [])
    if not objects:
        return f"未找到 {goal}。" if goal else "当前场景未检测到任何物体。"

    lines = [f"找到 {goal}：" if goal else "检测到以下物体："]
    for obj in objects:
        name = obj.get("name", "")
        confidence = float(obj.get("confidence", 0.0))
        position = obj.get("position") or {}
        x, y = position.get("x"), position.get("y")
        location = ""
        if x is not None and y is not None:
            location = f"，位置 ({x:.0f}, {y:.0f})"
        lines.append(f"- {name}（置信度 {confidence:.2f}）{location}")
    return "\n".join(lines)
