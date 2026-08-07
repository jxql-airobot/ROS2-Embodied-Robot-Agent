# 新对话交接说明（ROS2 Multimodal Embodied Robot Agent）

> 用途：从上一个会话切换到新对话时的上下文交接。
> 只保留未来研究方向的规划与已完成成果；工业机器人执行模块已排除。

## 一、当前状态（接手点）

- 项目已拆分为两条路线：
  - 本科毕业设计：冻结于 `bachelor-thesis-stable` 分支（AI-Robot-Demo 仓库），
    用于论文 / 软著 / 答辩，不再演进。
  - 未来研究：本仓库（ROS2 Multimodal Embodied Robot Agent），独立演进。
- 本仓库：`F:\AI-Projects\ROS2-Embodied-Robot-Agent`
  - GitHub 远程：`github.com/jxql-airobot/ROS2-Embodied-Robot-Agent`（公开，main）
  - 已完成的里程碑（以 `git log` 为准）：
    1. P0：远程仓库创建并推送
    2. P1：ROS2 闭环 Demo（NL 任务 → LLM → 动作 → cmd_vel → 差速小车），
       含 6 个 ROS2 包 + 17 个单元测试 + 端到端无头验证（前进 ~0.9m）
    3. Web：Streamlit 控制台（web/，HTTP + 任务链路已验证）
    4. Vision：视觉模块（BaseVision + YOLO + VisionTool + ROS2 视觉节点）进行中

## 二、接下来的任务规划（按优先级）

### P2 视觉感知

1. YOLO 独立运行 + 摄像头输入（Gazebo 相机 / USB 相机）→ 检测结果
2. `VisionTool` 接入 Agent（`get_scene` / `find_object`）
3. YOLO 结果进入 LLM 上下文 → LLM 根据视觉结果规划动作

### P3 导航

4. Navigation2 + slam_toolbox：建图 → 定位 → 导航 → 避障
5. `Ros2RobotTool.navigate()` 落地

### P4 多模态与语音

6. 语音输入：ASR → 文本任务 → Agent
7. 多模态模型统一接口（chat / detect / 未来 audio）
8. 简单具身任务端到端：找物 → 导航 → 反馈

### P5 具身操作与研究点

9. MoveIt2 机械臂操作 + 视觉引导抓取
10. 长时任务记忆 / 失败恢复研究（面向 ROS2 执行错误重设计）
11. 论文选题：具身智能体任务规划与执行闭环

## 三、已完成成果（可继承的设计与代码）

### 核心框架（设计思想可复用，代码在本科冻结分支）

- LLM Agent 核心：用户任务 → 可解释 Plan → 工具调用 → 结果反馈
- Planner：LLM 生成结构化任务计划（任务分析 / 目标 / 步骤 / 状态）
- Memory：SQLite 长期记忆 + RAG 语义检索（向量 top-k + 关键词兜底）
- Reflection：执行结果反思（成功 / 失败 / 重规划）
- Recovery：错误分级与自动恢复
- Tool 抽象：工具注册表 + 统一 run(args) 接口
- 日志与实验方法：可复现实验、成功率 / 轮次 / 消融对比

### 本仓库已落地（可继续演进）

- ROS2 执行层：`Ros2RobotTool`（move / rotate / stop / get_pose / execute_action；
  navigate / get_sensor 预留），`robot_control` 把动作映射到 `/cmd_vel`
- 统一 LLM 接口：`BaseLLM`（mock 默认离线可用；deepseek / openai 可切换）
- 视觉统一接口：`BaseVision`（detect → Scene），YOLO 实现（vision/）
- Streamlit 网页控制台（web/）
- WSL 开发脚本：构建 / 单测 / 端到端验证 / 诊断（scripts/）

### 实验方法沉淀（本科项目）

- 基线对比（LLM Direct / ReAct / 本文闭环）
- 消融实验（无安全约束 / 无闭环反思 / 无动作契约）
- 恢复能力对比（单轮 / 有反思无恢复 / 闭环）
- RAG 分类别知识增强评估

## 四、排除项（本路线不包含）

- 工业机器人执行层代码与实验（保留在本科冻结分支，不参与未来开发）
- 本科论文 / 软著 / 答辩材料（冻结于本科分支，本仓库不涉及）

## 五、关键路径参考

- 路线规划：`docs/roadmap/embodied_ai_plan.md`
- 项目总览：`README.md`
- ROS2 工作区：`ros2/README.md`、`web/README.md`、`vision/README.md`
- 本科代码参考（只读）：`F:\AI-Projects\AI-Robot-Demo`（bachelor-thesis-stable 分支）
