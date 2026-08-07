#!/usr/bin/env bash
# Probe rclpy / robot_interfaces import / publish in isolation with hard timeouts.
source /opt/ros/humble/setup.bash
cd /mnt/f/AI-Projects/ROS2-Embodied-Robot-Agent/ros2
source install/setup.bash
set +e

echo ">> probe 1: import robot_interfaces"
timeout -k 3 15 python3 -c "from robot_interfaces.msg import RobotCommand; print('import_ok')"
echo "exit1=$?"

echo ">> probe 2: rclpy.init + node"
timeout -k 3 15 python3 -c "import rclpy; rclpy.init(); from rclpy.node import Node; n=Node('p'); print('node_ok'); n.destroy_node(); rclpy.shutdown()"
echo "exit2=$?"

echo ">> probe 3: publish RobotCommand once"
timeout -k 3 15 python3 /mnt/f/AI-Projects/ROS2-Embodied-Robot-Agent/scripts/pub_robot_command.py --linear-x 0.1 --duration 0.1
echo "exit3=$?"
