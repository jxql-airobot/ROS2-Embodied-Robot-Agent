"""Launch robot_control + robot_agent without simulation (headless test mode)."""

import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description() -> LaunchDescription:
    pkg_agent = get_package_share_directory("robot_agent")
    default_llm_config = os.path.join(pkg_agent, "config", "llm.yaml")

    robot_control = Node(
        package="robot_control",
        executable="robot_control_node",
        output="screen",
    )
    robot_agent = Node(
        package="robot_agent",
        executable="robot_agent_node",
        output="screen",
        parameters=[
            {
                "llm_config": LaunchConfiguration("llm_config"),
                "llm_provider": LaunchConfiguration("llm_provider"),
            }
        ],
    )

    return LaunchDescription(
        [
            DeclareLaunchArgument("llm_config", default_value=default_llm_config),
            DeclareLaunchArgument("llm_provider", default_value=""),
            robot_control,
            robot_agent,
        ]
    )
