# ROS2 模块（规划）

> 状态：**规划中，尚未实现**。本目录将承载未来项目的 ROS2 执行底座。

## 职责

- ROS2 节点（生命周期管理、参数、日志）
- Topic（状态上报：位姿 / 传感器 / 任务状态）
- Service（指令下发：移动 / 停止 / 查询）
- Action（长时任务：导航 / 操作，带进度与取消）
- Navigation2（地图 / 定位 / 全局与局部规划 / 避障）
- SLAM（建图与定位）
- 机器人控制（差速 / 机械臂 / 传感器融合）

## 执行层统一接口（规划）

```python
class Ros2RobotTool:
    def move(self, *args, **kwargs): ...
    def navigate(self, *args, **kwargs): ...
    def stop(self, *args, **kwargs): ...
    def get_pose(self, *args, **kwargs): ...
    def get_sensor(self, *args, **kwargs): ...
    def execute_action(self, *args, **kwargs): ...
```

## 里程碑

1. ROS2 基础节点 + 执行层接口骨架
2. Navigation2 导航闭环
3. SLAM 建图与定位
4. MoveIt2 操作

> 本科项目中 ROS2 相关历史实现（ros2_ws 等）仅作参考，不直接并入本项目。
