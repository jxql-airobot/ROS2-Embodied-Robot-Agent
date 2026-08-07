#!/usr/bin/env bash
# Show how the installed gazebo.launch.py builds the gzserver command line.
set -uo pipefail

FILE="/opt/ros/humble/share/gazebo_ros/launch/gazebo.launch.py"
grep -n "force_system\|ExecuteProcess\|cmd=\|gui\|gzserver\|gzclient" "$FILE" | head -40
echo "---- full ExecuteProcess block ----"
sed -n '/gzserver/,/^        ]/p' "$FILE" | head -60
