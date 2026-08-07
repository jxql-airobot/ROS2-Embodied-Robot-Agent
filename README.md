# ROS2 Multimodal Embodied Robot Agent System

> 状态：**P0/P1 已落地**（ROS2 闭环 Demo 跑通：自然语言 → LLM → 结构化动作 → cmd_vel → 差速小车）。
> 面向具身智能的多模态机器人智能体系统，独立演进。

## 定位

面向**具身智能（Embodied Intelligence）**的多模态机器人智能体系统：

```text
能听 → 能看 → 能理解 → 能规划 → 能行动
```

技术栈：ROS2 + Vision + Speech + Multimodal AI + Embodied Intelligence。

## 与本科项目（AI-Robot-Demo）的关系

- **继承设计思想**：Agent 架构、Planner、Memory、Reflection、Recovery、
  Tool 调用、日志系统、实验方法（详见 [agent/](agent/README.md)）。
- **不复制旧项目代码**：本科项目冻结于 `bachelor-thesis-stable` 分支，
  本仓库仅继承设计思想。
- **执行层重新设计**：以 ROS2 为执行底座（Navigation2 / SLAM / 相机 / LiDAR）。

## 路线总览

| 模块 | 当前 | 未来 |
| --- | --- | --- |
| 执行 | ROS2 闭环（move / stop / rotate → cmd_vel，已跑通） | Navigation2 + SLAM + 机械臂 |
| 视觉 | YOLO（BaseVision 统一接口，进行中） | GPT Vision / Gemini / Qwen-VL |
| 语音 | 规划中 | ASR → 文本任务 |
| 模型 | 多模态模型接口（不绑定单一供应商） | GPT / Gemini / Claude / Qwen / DeepSeek |
| 网页 | Streamlit 控制台（web/） | 视觉面板实时显示 |

## 目录结构

```text
├── agent/        # Agent 设计思想（继承自本科项目，执行层重设计）
├── ros2/         # ROS2 工作区（interfaces / control / tools / agent / description / bringup）
├── vision/       # 视觉统一接口（BaseVision + YOLO，未来多模态）
├── speech/       # 语音输入 → ASR → 任务（规划）
├── web/          # Streamlit 网页控制台
├── models/       # 多模态模型统一接口（规划）
├── scripts/      # WSL 构建 / 测试 / 演示脚本
└── docs/         # 规划文档（roadmap、交接说明等）
```

## 快速开始（WSL）

```bash
# 构建工作区
bash scripts/wsl_build.sh

# 单元测试
bash scripts/run_tests.sh

# 启动仿真 Demo（Gazebo + RViz + robot_control + robot_agent）
bash scripts/run_demo.sh

# 另开终端，发送自然语言任务
ros2 run robot_agent send_task "让机器人向前移动"

# 网页控制台（再开一个终端）
source ros2/install/setup.bash
python3 -m streamlit run web/app.py --server.port 8502
```

详见 [ros2/README.md](ros2/README.md)、[vision/README.md](vision/README.md)、
[web/README.md](web/README.md)、[docs/roadmap/embodied_ai_plan.md](docs/roadmap/embodied_ai_plan.md)。
