# 新对话交接说明（ROS2 Multimodal Embodied Robot Agent）

> 用途：从上一个会话切换到新对话时的上下文交接。
> 只保留未来研究方向的规划与已完成成果，ABB 相关全部排除
> （已归档 legacy/，不参与未来开发）。

## 一、当前状态（接手点）

- 项目已拆分为两条路线：
  - 本科毕业设计：冻结于 `bachelor-thesis-stable` 分支（AI-Robot-Demo 仓库），
    用于论文 / 软著 / 答辩，不再演进。
  - 未来研究：本仓库（ROS2 Multimodal Embodied Robot Agent），独立演进。
- 本仓库本地已初始化：`F:\AI-Projects\ROS2-Embodied-Robot-Agent`
  - 初始提交：`ba86948`
  - 内容：项目骨架（README / roadmap / ros2 / vision / speech / models / legacy）
  - LICENSE：MIT
- GitHub 远程仓库：**尚未创建**（进行中）
  - gh CLI 已安装（`C:\Program Files\GitHub CLI\gh.exe`），未登录
  - SSH 密钥已认证账号 `jxql-airobot`（可推送，但不能建仓）
  - 待办：`gh auth login`（浏览器授权）或提供 PAT → 创建
    `github.com/jxql-airobot/ROS2-Embodied-Robot-Agent` → 推送本地提交

## 二、接下来的任务规划（按优先级）

### P0 仓库落地
1. GitHub 认证（`gh auth login`，账号 jxql-airobot）
2. `gh repo create jxql-airobot/ROS2-Embodied-Robot-Agent --public --source . --push`
3. 确认 README / LICENSE / .gitignore 正常显示

### P1 基础平台（第一学期）
4. ROS2 环境搭建（Humble 或更新 LTS），确认本地运行
5. 执行层统一接口落地：`Ros2RobotTool`
   （move / navigate / stop / get_pose / get_sensor / execute_action）
6. ROS2 节点框架：Topic（状态上报）+ Service（指令下发）+ Action（长时任务）
7. Navigation2 导航闭环（建图 → 定位 → 规划 → 避障）

### P2 多模态感知（第二学期）
8. 视觉统一接口落地：`BaseVision.detect(image)`，第一阶段 YOLO
9. 语音输入闭环：ASR → 文本任务 → Agent 规划 → 执行
10. 多模态模型统一接口：`MultimodalModelInterface`
    （chat / detect / 未来 audio；不绑定 GPT / Gemini / Claude / Qwen / DeepSeek）
11. 简单具身任务端到端：找物 → 导航 → 抓取

### P3 具身操作与研究点（第三学期）
12. MoveIt2 机械臂操作 + 视觉引导抓取
13. 长时任务记忆 / 失败恢复研究（面向 ROS2 执行错误重设计）
14. 论文选题：具身智能体任务规划与执行闭环

## 三、已完成成果（非 ABB，可继承的设计与代码）

### 核心框架（设计思想可复用，代码在本科冻结分支）
- LLM Agent 核心：用户任务 → 可解释 Plan → 工具调用 → 结果反馈
- Planner：LLM 生成结构化任务计划（任务分析 / 目标 / 步骤 / 状态）
- Memory：SQLite 长期记忆 + RAG 语义检索（向量 top-k + 关键词兜底）
- Reflection：执行结果反思（成功 / 失败 / 重规划）
- Recovery：错误分级与自动恢复
- Tool 抽象：工具注册表 + 统一 run(args) 接口
- 日志与实验方法：可复现实验、成功率 / 轮次 / 消融对比

### 视觉与模型接口（V7/V8 已验证，未来项目直接沿用）
- YOLO 视觉感知（yolo26n）+ 颜色零件兜底检测，统一 VisionState 输出
- 统一视觉接口 `BaseVision`（detect / get_visual_state），后端可替换
- 统一大模型接口 `BaseLLM`（chat / json_mode），DeepSeek 默认实现
- 配置化模型选择（config/model.yaml：llm.provider / vision.provider）

### 实验方法沉淀
- 基线对比（LLM Direct / ReAct / 本文闭环）
- 消融实验（无安全约束 / 无闭环反思 / 无动作契约）
- 恢复能力对比（单轮 / 有反思无恢复 / 闭环）
- RAG 分类别知识增强评估

## 四、排除项（本路线不包含）

- ABB RobotStudio / IRC5 / RWS / RAPID 相关代码与实验（已归档
  `legacy/robotstudio/`、`legacy/abb_tools/`，标记"不参与未来开发"）
- 本科论文 / 软著 / 答辩材料（冻结于本科分支，本仓库不涉及）
- ROS2 功能实现（当前仅规划，尚未写代码）

## 五、关键路径参考

- 路线规划：`docs/roadmap/embodied_ai_plan.md`
- 项目总览：`README.md`
- 各模块规划：`ros2/`、`vision/`、`speech/`、`models/` 下 README
- 本科代码参考（只读）：`F:\AI-Projects\AI-Robot-Demo`（bachelor-thesis-stable 分支）
