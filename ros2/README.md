# ROS2 Workspace — Embodied Robot Agent Execution Layer

ROS2 Humble 工作区：`自然语言任务 -> LLM Agent -> 结构化动作 -> cmd_vel -> 差速小车` 的最小闭环，以及面向后续视觉 / 导航 / 多模态扩展的执行层。

## 架构

```text
用户任务 (文本 / 未来语音)
        |
        v
robot_agent  (LLM: mock / deepseek / openai 可替换)
        |  BaseLLM.generate_action(task) -> ActionPlan
        v
Ros2RobotTool (BaseRobotTool 接口，agent 不感知底层机器人)
        |  RobotCommand (/robot_command)
        v
robot_control (move / stop / rotate -> Twist)
        |  /cmd_vel
        v
Gazebo simple_diffbot (diff_drive 插件 -> /odom)
```

设计原则：

- **机器人后端抽象**：Agent 只面向 `BaseRobotTool`（move / rotate / stop / navigate / get_pose / get_sensor / execute_action），不直接调 ROS2；未来换实体车 / 机械臂不改 Agent。
- **LLM 可替换**：`robot_agent/config/llm.yaml` 选 provider（mock 默认离线可用；deepseek / openai 走 OpenAI 兼容接口）。
- **话题/服务分层**：指令走 Topic（`/robot_command`），同步任务走 Service（`/task_execute`），未来长任务（导航/操作）走 Action。
- **预留接口**：`get_sensor()`、`navigate()`、`camera_link` / `lidar_link` 已为 YOLO 视觉、Nav2、语音预留。

## 包

| 包 | 作用 |
| --- | --- |
| `robot_interfaces` | RobotCommand / RobotStatus 消息 + ExecuteCommand / TaskExecute 服务 |
| `robot_control` | 执行层：move / stop / rotate -> /cmd_vel，带时长与状态反馈 |
| `robot_tools` | BaseRobotTool 抽象接口 + Ros2RobotTool（ROS2 实现） |
| `robot_agent` | 自然语言 -> LLM -> ActionPlan -> RobotTool；send_task CLI |
| `robot_description` | simple_diffbot 差速小车 URDF（xacro） |
| `robot_bringup` | launch / Gazebo 世界 / RViz 配置 |

## 环境

WSL2 + Ubuntu 22.04 + ROS2 Humble + Gazebo 11（已验证）。

```bash
# 首次构建（在 WSL 中，仓库根目录）
bash scripts/wsl_build.sh
```

## 运行 Demo（Gazebo 图形界面）

```bash
# 终端 1：启动仿真 + 控制 + Agent（默认带 Gazebo 和 RViz）
bash scripts/run_demo.sh

# 终端 2：发送自然语言任务
ros2 run robot_agent send_task "让机器人向前移动"
# 或同步等待结果
ros2 run robot_agent send_task "让机器人向前移动" --service
```

支持指令（mock LLM，中英均可）：向前/后退/左转/右转/停止，如"后退半米"、"左转90度"。

## 测试

```bash
# 单元测试（robot_control / robot_tools / robot_agent）
bash scripts/run_tests.sh

# 端到端无头测试：启动 -> 发任务 -> 校验 /odom 位移
bash scripts/wsl_demo_test.sh
```

## LLM 配置

`ros2/src/robot_agent/config/llm.yaml`：

```yaml
provider: mock          # mock | deepseek | openai
model: deepseek-chat
base_url: https://api.deepseek.com/v1
api_key_env: DEEPSEEK_API_KEY
```

切换真实模型：设置环境变量后 `ros2 launch robot_bringup demo.launch.py llm_provider:=deepseek`。

## 下一步

- 视觉感知层：YOLO -> `vision/`（BaseVision 接口，独立于 Agent）
- Nav2 + slam_toolbox：`navigate()` 落地
- 语音输入：`speech/` -> `/task_input`
