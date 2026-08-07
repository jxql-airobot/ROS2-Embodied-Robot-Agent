# Agent 设计思想（继承自本科项目）

未来项目的 Agent 层继承本科 AI-Robot-Demo 的设计思想，但**执行层重新设计**，
不复制 ABB 工业机器人代码。

## 继承的设计思想

| 组件 | 思想 | 未来实现方式 |
| --- | --- | --- |
| Agent 核心 | 用户任务 → 可解释 Plan → 工具调用 → 结果反馈 | 复用同一流程 |
| Planner | LLM 生成结构化任务计划（任务分析/目标/步骤/状态） | LLM/VLM 统一接口 |
| Memory | 长期记忆 + 语义检索（RAG） | 保持，扩展多模态记忆 |
| Reflection | 执行结果反思，判断成功/失败/重规划 | 保持 |
| Recovery | 错误分级与自动恢复 | 面向 ROS2 执行错误重设计 |
| Tool 调用 | 工具注册表 + 统一 run(args) 接口 | 保持，工具换成 ROS2 后端 |
| 日志系统 | 实验可复现、执行可观测 | 保持 |
| 实验方法 | 成功率 / 轮次 / 消融对比 | 保持，面向具身任务扩展 |

## 重新设计的部分

执行层不再调用 ABB RobotStudio / RWS / RAPID，改为统一的
`Ros2RobotTool`（move / navigate / stop / get_pose / get_sensor /
execute_action），Agent 只负责"理解与规划"，ROS2 负责"执行"。

> 参考：本科 Agent 代码位于仓库根目录 `agent/`（冻结分支
> `bachelor-thesis-stable`），未来实现按本文思想重写，不直接复制。
