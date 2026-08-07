#!/usr/bin/env bash
# Kill leftover ROS2 demo / Gazebo processes from THIS project only.
# Only touches gzserver instances running our simple_world, never the user's
# own gazebo / ai_robot processes.
set +e
pkill -9 -f "simple_world"
pkill -9 -f "robot_control_node"
pkill -9 -f "robot_agent_node"
pkill -9 -f "robot_state_publisher"
pkill -9 -f "spawn_entity"
pkill -9 -f "ros2 launch"
pkill -9 -f "check_world_motion"
pkill -9 -f "odom_checker"
pkill -9 -f "odom_pose_once"
sleep 1
if ss -ltn 2>/dev/null | grep -q ":11345 "; then
  echo "WARN: port 11345 still busy (not ours?)"
else
  echo "cleaned"
fi
