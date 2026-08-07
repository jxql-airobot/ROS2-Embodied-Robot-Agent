# legacy/ — 历史工业机器人适配模块（Legacy Module）

> 这些模块来自本科项目（AI-Robot-Demo）的 ABB 工业机器人适配层，
> **仅归档，不参与未来 ROS2 具身智能项目开发**。

## 归档范围（本科冻结分支保留原件）

| 模块 | 原件位置 | 说明 |
| --- | --- | --- |
| RobotStudio 适配 | `robotstudio/` | ABB RobotStudio 6.08 客户端 / Mock / 配置 |
| RobotStudio 后端 | `agent/tools/robotstudio_tool.py` | Agent 的 ABB 执行后端 |
| RWS 恢复 | `agent/recovery/rws_manager.py` | 控制器级自动恢复（IRC5） |
| ABB 实验脚本 | `experiments/robotstudio_benchmark.py` 等 | 真实/仿真验证 |
| ABB 文档 | `docs/robotstudio_*.md` | 设计 / 环境 / 实验记录 |

## 标记

```
历史工业机器人适配模块
Legacy Module
不参与未来开发
```

## 迁移策略

1. 本科冻结分支 `bachelor-thesis-stable` 保留全部原件，不删除
2. 未来项目只参考其**设计思想**，不复制 ABB 专用代码
3. 如需对照历史实现，从本科冻结分支 checkout 对应文件
