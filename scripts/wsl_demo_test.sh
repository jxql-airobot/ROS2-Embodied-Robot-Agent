#!/usr/bin/env bash
# End-to-end demo test (headless):
#   launch Gazebo sim + robot_control + robot_agent
#   send task "让机器人向前移动"
#   verify the robot actually moved via /odom
source /opt/ros/humble/setup.bash
cd "$(dirname "$0")/.."
cd ros2
source install/setup.bash
set -uo pipefail

LOG_DIR="${TMPDIR:-/tmp}/robot_demo_test"
mkdir -p "$LOG_DIR"

echo ">> cleaning leftovers from previous runs ..."
"$(dirname "$0")/wsl_cleanup.sh"

echo ">> launching demo (headless: gui:=false rviz:=false)"
ros2 launch robot_bringup demo.launch.py gui:=false rviz:=false \
  > "$LOG_DIR/launch.log" 2>&1 &
LAUNCH_PID=$!

cleanup() {
  kill -INT "$LAUNCH_PID" 2>/dev/null || true
  sleep 2
  pkill -9 -f "simple_world" 2>/dev/null || true
}
trap cleanup EXIT

echo ">> waiting for /odom ..."
python3 "$(dirname "$0")/wait_topic.py" /odom nav_msgs/msg/Odometry --timeout 90 \
  || { echo "FAIL: /odom never appeared"; tail -60 "$LOG_DIR/launch.log"; exit 1; }
echo ">> /odom is up"

echo ">> baseline pose:"
BASELINE=$(python3 "$(dirname "$0")/odom_pose.py")
echo "$BASELINE"

echo ">> sending task: 让机器人向前移动"
ros2 run robot_agent send_task "让机器人向前移动" > "$LOG_DIR/task.log" 2>&1 || true
cat "$LOG_DIR/task.log"

echo ">> waiting 6s for motion ..."
sleep 6

echo ">> final pose:"
FINAL=$(python3 "$(dirname "$0")/odom_pose.py")
echo "$FINAL"

echo ">> verifying displacement (baseline vs final)"
python3 -c "
import re, math, sys

def parse(line):
    m = re.search(r'x=([-\d.]+) y=([-\d.]+) yaw=([-\d.]+)', line)
    return (float(m.group(1)), float(m.group(2))) if m else None

b = parse('''$BASELINE''')
f = parse('''$FINAL''')
if b is None or f is None:
    print('FAIL: could not parse odom poses')
    sys.exit(1)
dist = math.hypot(f[0] - b[0], f[1] - b[1])
print(f'displacement={dist:.3f} m (threshold=0.05)')
sys.exit(0 if dist >= 0.05 else 2)
"
RESULT=$?

if [ "$RESULT" -eq 0 ]; then
  echo "PASS: robot moved - closed loop (NL task -> LLM -> action -> cmd_vel -> motion) OK"
else
  echo "FAIL: robot did not move"
  tail -40 "$LOG_DIR/launch.log"
  exit 1
fi
