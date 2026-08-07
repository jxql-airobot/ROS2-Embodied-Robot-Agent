# legacy/abb_tools/ — ABB 工具与恢复模块（历史归档）

```
历史工业机器人适配模块
Legacy Module
不参与未来开发
```

归档内容（原件保留在本科冻结分支 `bachelor-thesis-stable`）：

- `agent/recovery/rws_manager.py`：基于 RWS 的控制器级自动恢复
  （错误分级、mastership、set-entrypoint、resetpp、start）
- `agent/tools/robotstudio_tool.py`：RobotStudio 执行后端（含
  RAPID socket 协议：MOVEL / MOVEJ / GETPOSE / ERRINFO）
- `docs/robotstudio_*.md`：ABB 环境与实验文档

未来 ROS2 项目的恢复机制面向 ROS2 执行错误重设计。
