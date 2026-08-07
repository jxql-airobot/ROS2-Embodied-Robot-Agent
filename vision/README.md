# Vision 模块（规划）

> 状态：接口设计完成（沿用 V8 统一接口思路），第一阶段用 YOLO，未来支持多模态。

## 流程

```
Camera → 视觉后端（YOLO / 未来多模态）→ 结构化目标 → Agent 理解 → ROS2 执行
```

## 统一接口

```python
class BaseVision:
    def detect(self, image): ...
    def get_visual_state(self, source="synthetic", image=None): ...
```

输出统一格式（类别 / 置信度 / 边界框 / 中心点），Agent 不绑定检测器。

## 路线

- 第一阶段：YOLO（复用本科已验证的颜色兜底 + 通用目标检测思路）
- 未来：GPT Vision / Gemini Vision / Qwen-VL 等视觉语言模型

> 实现时从本科 `agent/vision/`（V8 统一接口）抽取抽象层，
> 不复制 RobotStudio 相关代码。
