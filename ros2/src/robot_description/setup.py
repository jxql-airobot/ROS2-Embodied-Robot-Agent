import os
from glob import glob

from setuptools import setup

package_name = "robot_description"

setup(
    name=package_name,
    version="0.1.0",
    packages=[package_name],
    data_files=[
        ("share/ament_index/resource_index/packages", ["resource/" + package_name]),
        ("share/" + package_name, ["package.xml"]),
        (os.path.join("share", package_name, "urdf"), glob("urdf/*")),
    ],
    install_requires=["setuptools"],
    zip_safe=True,
    maintainer="jxql-airobot",
    maintainer_email="jxql-airobot@users.noreply.github.com",
    description="URDF description of the simple_diffbot Gazebo robot.",
    license="MIT",
    entry_points={},
)
