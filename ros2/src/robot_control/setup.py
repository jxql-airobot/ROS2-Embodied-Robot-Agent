from setuptools import setup

package_name = "robot_control"

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
    description="Robot execution layer: robot_control node (move/stop/rotate -> cmd_vel).",
    license="MIT",
    tests_require=["pytest"],
    entry_points={
        "console_scripts": [
            "robot_control_node = robot_control.robot_control_node:main",
        ],
    },
)
