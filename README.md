# ROS2 Multimodal Embodied Robot Agent System

> 状态：**规划中（独立仓库初始化）**。本项目是未来研究方向的项目骨架，
> 与本科毕业设计（AI-Robot-Demo 工业机器人 Agent 系统）解耦，独立演进。

## 定位

面向**具身智能（Embodied Intelligence）**的多模态机器人智能体系统：

```
能听 → 能看 → 能理解 → 能规划 → 能行动
```

技术栈：ROS2 + Vision + Speech + Multimodal AI + Embodied Intelligence。

## 与本科项目（AI-Robot-Demo）的关系

- **继承设计思想**：Agent 架构、Planner、Memory、Reflection、Recovery、
  Tool 调用、日志系统、实验方法（详见 [agent/](agent/README.md)）。
- **不复制工业机器人代码**：ABB RobotStudio / IRC5 / RWS / RAPID 相关模块
  归档在 [legacy/](legacy/README.md)，标记为历史模块，不参与未来开发。
- **机器人执行层重新设计**：以 ROS2 为执行底座（Navigation2 / SLAM / 相机 /
  LiDAR），不再依赖 ABB 专用接口。

## 路线总览

| 模块 | 第一阶段 | 未来 |
| --- | --- | --- |
| 执行 | ROS2（规划中） | Navigation2 + SLAM + 机械臂 |
| 视觉 | YOLO（统一接口） | GPT Vision / Gemini Vision / Qwen-VL |
| 语音 | 规划中 | ASR → 文本任务 |
| 模型 | 多模态模型接口（不绑定单一供应商） | GPT / Gemini / Claude / Qwen / DeepSeek |

详细规划见 [docs/roadmap/embodied_ai_plan.md](docs/roadmap/embodied_ai_plan.md)。

## 目录结构（当前为规划骨架，逐步填充实现）

```
research/
├── agent/        # Agent 设计思想（继承自本科项目，执行层重设计）
├── ros2/         # ROS2 节点 / Topic / Service / Action / 导航 / SLAM（规划）
├── vision/       # 视觉统一接口（YOLO 起步，未来多模态）
├── speech/       # 语音输入 → ASR → 任务（规划）
├── models/       # 多模态模型统一接口（不绑定单一模型）
├── legacy/       # 历史工业机器人适配模块（ABB，不参与未来开发）
└── docs/         # 规划文档（roadmap 等）
```
