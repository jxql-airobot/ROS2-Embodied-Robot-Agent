# 具身智能研究规划（Embodied AI Plan）

> 面向未来硕士研究方向：ROS2 Multimodal Embodied Robot Agent System。
> 本文档只做路线规划，不约束具体实现细节；实现按里程碑逐步推进。

## 1. 项目目标

构建一个"能听、能看、能理解、能规划、能行动"的机器人智能体：

```
用户（语音 / 文本 / 图像）
        │
        ▼
Multimodal Robot Agent（LLM/VLM + Planner + Memory + Reflection + Recovery）
        │
        ▼
              ROS2
        │
   Camera / LiDAR / Robot（视觉 / SLAM / 导航 / 操作）
```

## 2. ROS2 路线

### 2.1 阶段一：基础通信与导航（规划）

- 搭建 ROS2 节点框架（Humble 或更新 LTS）
- 机器人执行层统一接口：

```python
class Ros2RobotTool:
    def move(self, *args, **kwargs): ...      # 运动指令
    def navigate(self, *args, **kwargs): ...  # 导航到目标点
    def stop(self, *args, **kwargs): ...      # 急停/停止
    def get_pose(self, *args, **kwargs): ...  # 当前位姿
    def get_sensor(self, *args, **kwargs): ...# 传感器数据（相机/里程计/激光）
    def execute_action(self, *args, **kwargs): ...  # 高层动作执行
```

- Topic / Service / Action 分层：状态上报用 Topic，指令下发用 Service，
  长时任务（导航/操作）用 Action。

### 2.2 阶段二：SLAM 与导航

- Navigation2（map 构建 → 定位 → 全局/局部规划）
- LiDAR + 里程计融合
- 动态避障与行为树/状态机管理

### 2.3 阶段三：操作（Manipulation）

- MoveIt2 + 机械臂控制
- 视觉引导抓取（相机 → 目标定位 → 执行）

## 3. 视觉路线

### 3.1 第一阶段：YOLO（复用现有能力，走统一接口）

```
Camera → YOLO 检测 → 目标信息 → Agent 理解 → ROS2 执行
```

统一接口 `BaseVision.detect(image)`，输出结构化目标
（类别 / 置信度 / 边界框 / 中心点），Agent 不关心检测器细节。

### 3.2 未来：多模态视觉

- GPT Vision / Gemini Vision / Qwen-VL 等视觉语言模型
- 开放词汇检测与场景理解
- 通过统一接口替换，不改 Agent 核心逻辑

## 4. 语音路线

```
语音输入 → ASR → 文本任务 → Agent 规划 → 机器人执行
```

- 第一阶段：ASR 文本转写（中英），接入 Agent 任务入口
- 未来：语音交互（TTS 反馈、多轮对话）
- 独立 `speech/` 模块，与 Agent 通过文本解耦

## 5. 多模态模型路线

### 5.1 统一接口

设计 `MultimodalModelInterface`，同一接口承载：

- 语言理解与规划（chat / complete）
- 视觉理解（detect / describe）
- 未来：语音理解（audio）

### 5.2 供应商策略

- 不绑定单一模型：GPT 系列、Gemini、Claude、Qwen、DeepSeek 可替换
- 通过配置选择 provider（沿用 config/model.yaml 思路）
- 默认保留 DeepSeek 作为低成本文本后端，视觉单独走视觉后端

## 6. 硕士研究规划（建议节奏）

### 第一学期：基础平台

- ROS2 环境与差速/轮式平台接入
- 导航 + SLAM 跑通
- Agent 核心（Planner / Memory / Reflection / Recovery）在 ROS2 上重构

### 第二学期：多模态感知

- 视觉统一接口落地（YOLO → 多模态视觉）
- 语音输入闭环
- 简单任务（找物、导航、抓取）端到端打通

### 第三学期：具身操作与研究点

- MoveIt2 操作 + 视觉引导抓取
- 长时任务记忆 / 失败恢复研究
- 论文选题：具身智能体任务规划与执行闭环

## 7. 与本科项目的边界

- 本科项目（AI-Robot-Demo）冻结在 `bachelor-thesis-stable` 分支，
  仅用于毕业论文、软著与答辩，不再演进
- 本路线不修改本科实验数据、不删除本科代码
- ABB 相关模块只归档在 `research/legacy/`，不进入未来实现
