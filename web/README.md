# Web GUI（Streamlit）

面向 ROS2 Embodied Robot Agent 的网页控制台：输入自然语言任务，实时查看 Agent 响应、结构化动作、机器人状态与里程计。

## 运行

需要 WSL 中已构建工作区并启动 Demo：

```bash
# 终端 1：启动仿真 + robot_control + robot_agent（带 Gazebo 图形界面）
bash scripts/run_demo.sh

# 终端 2：启动网页（WSL 中）
source /opt/ros/humble/setup.bash
source ros2/install/setup.bash
python3 -m streamlit run web/app.py --server.port 8502
```

浏览器打开 `http://localhost:8502`。

## 功能

- 任务输入：发送自然语言任务，经 `/task_execute` 同步调用 robot_agent
- 最近任务：Agent 响应 + 结构化动作 JSON
- 机器人状态：/robot_status（动作 / 状态 / 剩余时间）
- 里程计：/odom（x / y / yaw）
- 任务历史：会话内最近 20 条

## 说明

- `ros2_client.py`：后台 spin 线程维护状态快照；每次任务调用使用独立短生命周期节点做同步服务调用，避免阻塞。
- 视觉面板为下一阶段（YOLO）预留占位。
