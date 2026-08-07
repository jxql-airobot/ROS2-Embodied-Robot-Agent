#!/usr/bin/env bash
set +e
echo "== OS =="
. /etc/os-release && echo "$PRETTY_NAME"
echo "== ROS2 =="
if [ -d /opt/ros ]; then ls /opt/ros; else echo "no /opt/ros"; fi
command -v ros2 && ros2 --version
echo "== Python =="
python3 --version
command -v pip3 && pip3 --version
echo "== Docker =="
command -v docker && docker --version
echo "== GUI =="
echo "DISPLAY=$DISPLAY"
echo "WAYLAND_DISPLAY=$WAYLAND_DISPLAY"
ls /mnt/wslg 2>/dev/null | head -5
echo "== Gazebo =="
command -v gazebo && gazebo --version 2>/dev/null | head -2
command -v gz && gz --version 2>/dev/null | head -2
echo "== Memory/Disk =="
free -h | head -2
df -h / | tail -1
echo DONE
