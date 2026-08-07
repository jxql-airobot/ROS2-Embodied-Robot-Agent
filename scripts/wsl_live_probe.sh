#!/usr/bin/env bash
# Probe rclpy steps WHILE the demo launch is running, with progress prints.
source /opt/ros/humble/setup.bash
cd /mnt/f/AI-Projects/ROS2-Embodied-Robot-Agent/ros2
source install/setup.bash
set -uo pipefail

"$(dirname "$0")/wsl_cleanup.sh"
ros2 launch robot_bringup demo.launch.py gui:=false rviz:=false verbose:=true \
  > /tmp/live_probe_launch.log 2>&1 &
LAUNCH_PID=$!

cleanup() {
  kill -INT "$LAUNCH_PID" 2>/dev/null || true
  sleep 1
  pkill -9 -f "simple_world" 2>/dev/null || true
}
trap cleanup EXIT

echo ">> waiting for /odom ..."
python3 "$(dirname "$0")/wait_topic.py" /odom nav_msgs/msg/Odometry --timeout 90 \
  || { echo "FAIL: no /odom"; exit 1; }

echo ">> running step-by-step rclpy probe (hard timeout 30s):"
timeout -k 3 30 python3 -u -c "
print('start', flush=True)
from robot_interfaces.msg import RobotCommand
print('import_ok', flush=True)
import rclpy
print('rclpy_import_ok', flush=True)
rclpy.init()
print('rclpy_init_ok', flush=True)
from rclpy.node import Node
n = Node('live_probe')
print('node_ok', flush=True)
p = n.create_publisher(RobotCommand, '/robot_command', 10)
print('publisher_ok', flush=True)
cmd = RobotCommand(action='move', linear_x=0.1, duration=0.1)
p.publish(cmd)
print('publish_ok', flush=True)
n.destroy_node()
rclpy.shutdown()
print('done', flush=True)
"
echo "probe_exit=$?"
