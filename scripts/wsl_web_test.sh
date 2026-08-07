#!/usr/bin/env bash
# Smoke-test the web GUI: launch demo, start streamlit, check HTTP + task path.
source /opt/ros/humble/setup.bash
cd "$(dirname "$0")/.."
cd ros2
source install/setup.bash
set -uo pipefail

REPO="$(dirname "$0")/.."

"$(dirname "$0")/wsl_cleanup.sh"
ros2 launch robot_bringup demo.launch.py gui:=false rviz:=false \
  > /tmp/web_demo.log 2>&1 &
LAUNCH_PID=$!

cleanup() {
  kill -INT "$LAUNCH_PID" 2>/dev/null || true
  pkill -9 -f "streamlit run web/app.py" 2>/dev/null || true
  sleep 1
  pkill -9 -f "simple_world" 2>/dev/null || true
}
trap cleanup EXIT

echo ">> waiting for /odom ..."
python3 "$(dirname "$0")/wait_topic.py" /odom nav_msgs/msg/Odometry --timeout 90 \
  || { echo "FAIL: no /odom"; tail -30 /tmp/web_demo.log; exit 1; }

echo ">> starting streamlit on :8502 ..."
cd "$REPO"
python3 -m streamlit run web/app.py --server.headless true --server.port 8502 \
  > /tmp/web_gui.log 2>&1 &
WEB_PID=$!
sleep 8

echo ">> HTTP check:"
curl -s -o /dev/null -w "HTTP %{http_code}\n" http://localhost:8502

echo ">> task path check (send_task via Ros2Client):"
python3 -c "
import sys
sys.path.insert(0, 'web')
from ros2_client import Ros2Client
client = Ros2Client()
result = client.send_task('让机器人向前移动')
print(result)
client.close()
"

kill "$WEB_PID" 2>/dev/null || true
echo "WEB TEST DONE"
