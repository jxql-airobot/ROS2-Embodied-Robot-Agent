"""YOLO object detector (ultralytics, open source). First-generation robot eye."""

from __future__ import annotations

from typing import Any, Optional

from vision.base_vision import BaseVision
from vision.vision_schema import Detection, Scene


class YOLODetector(BaseVision):
    """Real-time object detector backed by ultralytics YOLO.

    Args:
        model_path: local weights or a name like "yolov8n.pt" (auto-downloaded).
        conf: minimum confidence threshold.
    """

    backend_name = "yolo"

    def __init__(self, model_path: str = "yolov8n.pt", conf: float = 0.35) -> None:
        try:
            from ultralytics import YOLO
        except ImportError as exc:  # pragma: no cover
            raise RuntimeError(
                "ultralytics not installed; run: pip3 install ultralytics"
            ) from exc
        self._model = YOLO(model_path)
        self._conf = conf

    def detect(self, image: Any) -> Scene:
        results = self._model.predict(image, conf=self._conf, verbose=False)
        result = results[0]
        names = result.names
        height, width = (result.orig_shape[0], result.orig_shape[1])

        scene = Scene(image_width=width, image_height=height, source=self.backend_name)
        if result.boxes is None:
            return scene

        boxes = result.boxes.xyxy.tolist()
        confs = result.boxes.conf.tolist()
        classes = result.boxes.cls.tolist()
        for box, conf, cls in zip(boxes, confs, classes):
            x1, y1, x2, y2 = box
            scene.objects.append(
                Detection(
                    name=str(names[int(cls)]),
                    confidence=round(float(conf), 4),
                    bbox=[round(v, 1) for v in (x1, y1, x2, y2)],
                    center=[round((x1 + x2) / 2.0, 1), round((y1 + y2) / 2.0, 1)],
                )
            )
        return scene
