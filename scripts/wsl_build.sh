#!/usr/bin/env bash
# Build the ROS2 workspace in WSL (run from repo root or anywhere).
source /opt/ros/humble/setup.bash
set -euo pipefail

cd "$(dirname "$0")/../ros2"
colcon build "$@"
