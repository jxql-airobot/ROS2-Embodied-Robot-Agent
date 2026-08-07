#!/usr/bin/env bash
# Ground-truth probe: launch sim, print gz model pose before/after a move command.
source /opt/ros/humble/setup.bash
cd "$(dirname "$0")/.."
cd ros2
source install/setup.bash
set -uo pipefail

LOG_DIR="${TMPDIR:-/tmp}/robot_pose_probe"
mkdir -p "$LOG_DIR"

"$(dirname "$0")/wsl_cleanup.sh"
ros2 launch robot_bringup demo.launch.py gui:=false rviz:=false verbose:=true \
  > "$LOG_DIR/launch.log" 2>&1 &
LAUNCH_PID=$!

cleanup() {
  kill -INT "$LAUNCH_PID" 2>/dev/null || true
  sleep 1
  pkill -9 -f "simple_world" 2>/dev/null || true
}
trap cleanup EXIT

echo ">> waiting for /odom ..."
python3 "$(dirname "$0")/wait_topic.py" /odom nav_msgs/msg/Odometry --timeout 90 \
  || { echo "FAIL: no /odom"; tail -40 "$LOG_DIR/launch.log"; exit 1; }

echo ">> before:"
BEFORE=$(bash "$(dirname "$0")/gz_pose.sh")
echo "$BEFORE"

echo ">> sending move vx=0.3 duration=2 via /robot_command"
python3 "$(dirname "$0")/pub_robot_command.py" --linear-x 0.3 --duration 2.0
sleep 4

echo ">> after:"
AFTER=$(bash "$(dirname "$0")/gz_pose.sh")
echo "$AFTER"

echo ">> delta (x y z):"
python3 -c "
import sys
b = [float(v) for v in '$BEFORE'.split()]
a = [float(v) for v in '$AFTER'.split()]
print(f'dx={a[0]-b[0]:.4f} dy={a[1]-b[1]:.4f} dz={a[2]-b[2]:.4f}')
"
