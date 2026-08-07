#!/usr/bin/env bash
# Build the ROS2 workspace (first time) and launch the full demo.
#
# Usage (from the repo root or anywhere):
#   scripts/run_demo.sh                    # Gazebo GUI + RViz
#   scripts/run_demo.sh gui:=false         # headless sim
#   scripts/run_demo.sh rviz:=false
#   scripts/run_demo.sh llm_provider:=deepseek
source /opt/ros/humble/setup.bash
cd "$(dirname "$0")/.."
cd ros2
source install/setup.bash 2>/dev/null || true
set -euo pipefail

if [ ! -d install/robot_bringup ]; then
  echo ">> first build ..."
  colcon build --symlink-install --cmake-args -DCMAKE_BUILD_TYPE=Release
fi
source install/setup.bash

echo ">> launching demo: ros2 launch robot_bringup demo.launch.py $*"
exec ros2 launch robot_bringup demo.launch.py "$@"
