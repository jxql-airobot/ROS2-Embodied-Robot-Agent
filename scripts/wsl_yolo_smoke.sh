#!/usr/bin/env bash
# Smoke test: YOLO detection via our vision module (LOCAL weights + cached image,
# no network).
set +e
cd /tmp
echo ">> downloading sample image ..."
if [ ! -f /tmp/bus.jpg ]; then
  wget -q -O /tmp/bus.jpg https://ultralytics.com/images/bus.jpg || curl -sL -o /tmp/bus.jpg https://ultralytics.com/images/bus.jpg
fi
ls -la /tmp/bus.jpg

echo ">> running YOLODetector ..."
python3 - <<'EOF'
import sys
sys.path.insert(0, "/mnt/f/AI-Projects/ROS2-Embodied-Robot-Agent")
from vision.yolo_detector import YOLODetector

detector = YOLODetector(
    model_path="/mnt/f/AI-Projects/ROS2-Embodied-Robot-Agent/models/yolov8n.pt",
    conf=0.35,
)
scene = detector.detect("/tmp/bus.jpg")
print("backend:", detector.backend_name)
print("image:", scene.image_width, "x", scene.image_height)
print("objects:", len(scene.objects))
for o in scene.objects:
    print(" -", o.name, o.confidence, o.bbox, o.center)
print("json:", scene.to_json()[:200])
EOF
