#!/usr/bin/env bash
# Diagnostics: reproduce the gzserver launch command and watch for crashes.
source /opt/ros/humble/setup.bash
set +e

WORLD="/mnt/f/AI-Projects/ROS2-Embodied-Robot-Agent/ros2/install/robot_bringup/share/robot_bringup/worlds/simple_world.world"

echo ">> exact launch cmd (no --verbose), 20s:"
timeout -k 5 20 gzserver "$WORLD" \
  -s libgazebo_ros_init.so -s libgazebo_ros_factory.so -s libgazebo_ros_force_system.so \
  2>&1 | tail -40
echo "exit=${PIPESTATUS[0]}"

echo ">> via ros2 launch sim.launch.py (headless, verbose), 40s:"
cd /mnt/f/AI-Projects/ROS2-Embodied-Robot-Agent/ros2
source install/setup.bash
ros2 launch robot_bringup sim.launch.py gui:=false rviz:=false verbose:=true \
  > /tmp/gz_launch_test.log 2>&1 &
LPID=$!
sleep 40
if kill -0 "$LPID" 2>/dev/null; then
  echo "launch still running after 40s (gzserver survived)"
else
  echo "launch exited early"
fi
echo "---- gzserver death check ----"
grep -n "process has died\|segmentation\|Segmentation\|abort\|core dumped" /tmp/gz_launch_test.log
echo "---- tail of launch log ----"
tail -40 /tmp/gz_launch_test.log
kill -9 "$LPID" 2>/dev/null
pkill -9 -x gzserver 2>/dev/null
echo DONE
echo "---- tail of launch log ----"
tail -60 /tmp/gz_launch_test.log
echo "exit=${PIPESTATUS[0]}"
