#!/usr/bin/env bash
# Ground-truth physics check: does the robot drive forward (+X) in the world frame?
source /opt/ros/humble/setup.bash
cd "$(dirname "$0")/.."
cd ros2
source install/setup.bash
set -uo pipefail

LOG_DIR="${TMPDIR:-/tmp}/robot_world_test"
mkdir -p "$LOG_DIR"

echo ">> cleaning leftovers from previous runs ..."
"$(dirname "$0")/wsl_cleanup.sh"

ros2 launch robot_bringup demo.launch.py gui:=false rviz:=false verbose:=true \
  > "$LOG_DIR/launch.log" 2>&1 &
LAUNCH_PID=$!

cleanup() {
  kill -INT "$LAUNCH_PID" 2>/dev/null || true
  sleep 1
  pkill -9 -x gzserver 2>/dev/null || true
}
trap cleanup EXIT

echo ">> waiting for /gazebo/model_states ..."
python3 "$(dirname "$0")/wait_topic.py" /gazebo/model_states gazebo_msgs/msg/ModelStates --timeout 90 \
  || { echo "FAIL: gazebo did not come up"; exit 1; }
python3 "$(dirname "$0")/check_world_motion.py"
exit $?
