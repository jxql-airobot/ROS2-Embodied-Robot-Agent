import os
from glob import glob

from setuptools import find_packages, setup

package_name = "robot_agent"

setup(
    name=package_name,
    version="0.1.0",
    packages=find_packages(exclude=["test", "test.*"]),
    data_files=[
        ("share/ament_index/resource_index/packages", ["resource/" + package_name]),
        ("share/" + package_name, ["package.xml"]),
        (os.path.join("share", package_name, "config"), glob("config/*.yaml")),
    ],
    install_requires=["setuptools"],
    zip_safe=True,
    maintainer="jxql-airobot",
    maintainer_email="jxql-airobot@users.noreply.github.com",
    description="robot_agent: NL task -> LLM -> structured action -> Ros2RobotTool.",
    license="MIT",
    tests_require=["pytest"],
    entry_points={
        "console_scripts": [
            "robot_agent_node = robot_agent.robot_agent_node:main",
            "send_task = robot_agent.send_task:main",
        ],
    },
)
