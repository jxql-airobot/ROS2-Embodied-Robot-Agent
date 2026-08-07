#!/usr/bin/env python3
"""Robot Agent Web GUI (Streamlit) for the ROS2 Embodied Robot Agent.

Run (WSL, after sourcing ROS2 + the workspace):
  python3 -m streamlit run web/app.py --server.port 8502
"""

from __future__ import annotations

import json
import os
import sys
import time

WEB_DIR = os.path.dirname(os.path.abspath(__file__))
if WEB_DIR not in sys.path:
    sys.path.insert(0, WEB_DIR)

import streamlit as st  # noqa: E402

from ros2_client import Ros2Client  # noqa: E402

st.set_page_config(page_title="ROS2 Embodied Robot Agent", page_icon="🤖", layout="wide")

if "client" not in st.session_state:
    st.session_state.client = Ros2Client()
if "history" not in st.session_state:
    st.session_state.history = []

client: Ros2Client = st.session_state.client

# --------------------------------------------------------------------------- #

with st.sidebar:
    st.title("ROS2 Embodied Robot Agent")
    st.caption("自然语言 → LLM → 结构化动作 → ROS2 机器人")
    st.divider()

    st.subheader("任务输入")
    task = st.text_input("任务", placeholder="例如：让机器人向前移动 / 左转90度 / 停止")
    if st.button("执行任务", type="primary", use_container_width=True) and task.strip():
        result = client.send_task(task.strip())
        st.session_state.history.append(
            {"task": task.strip(), "result": result, "time": time.strftime("%H:%M:%S")}
        )
        st.session_state.last = result

    st.divider()
    st.caption("连接话题：/task_execute · /robot_status · /odom")

# --------------------------------------------------------------------------- #

col_status, col_odom, col_last = st.columns(3)

with col_status:
    st.subheader("机器人状态")
    status = client.get_status()
    if status:
        st.metric("当前动作", status["action"])
        st.metric("状态", status["state"])
        st.caption(f"{status['message']}（{status['time']}）")
    else:
        st.info("等待 /robot_status …")

with col_odom:
    st.subheader("里程计")
    odom = client.get_odom()
    if odom:
        st.metric("x", f"{odom['x']:.2f} m")
        st.metric("y", f"{odom['y']:.2f} m")
        st.metric("yaw", f"{odom['yaw']:.2f} rad")
    else:
        st.info("等待 /odom …")

with col_last:
    st.subheader("最近一次任务")
    last = st.session_state.get("last")
    if last:
        if last["success"]:
            st.success(last["response"])
        else:
            st.error(last["response"])
        if last.get("action_json"):
            try:
                st.json(json.loads(last["action_json"]))
            except json.JSONDecodeError:
                st.code(last["action_json"])
    else:
        st.info("尚未执行任务")

st.divider()

st.subheader("任务历史")
if st.session_state.history:
    for item in reversed(st.session_state.history[-20:]):
        ok = bool(item["result"].get("success"))
        icon = "✅" if ok else "❌"
        st.markdown(
            f"{icon} **{item['time']}** {item['task']} — {item['result'].get('response', '')}"
        )
else:
    st.caption("暂无任务记录")

st.divider()

st.subheader("视觉感知（下一阶段）")
st.caption("YOLO 视觉模块接入后，这里将实时显示目标检测结果（类别 / 置信度 / 位置）。")
