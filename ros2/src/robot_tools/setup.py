from setuptools import setup

package_name = "robot_tools"

setup(
    name=package_name,
    version="0.1.0",
    packages=[package_name],
    data_files=[
        ("share/ament_index/resource_index/packages", ["resource/" + package_name]),
        ("share/" + package_name, ["package.xml"]),
    ],
    install_requires=["setuptools"],
    zip_safe=True,
    maintainer="jxql-airobot",
    maintainer_email="jxql-airobot@users.noreply.github.com",
    description="RobotTool interface: BaseRobotTool + Ros2RobotTool (ROS2 topics).",
    license="MIT",
    tests_require=["pytest"],
    entry_points={},
)
