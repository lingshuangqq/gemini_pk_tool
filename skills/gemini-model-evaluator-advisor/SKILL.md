---
name: gemini-model-evaluator-advisor
description: >-
  Use this skill to benchmark, evaluate, and rank Google Gemini text, image, and video models across Vertex AI and Gemini API. It calculates dual-dimensional scores (Capability Score and Cost-Performance/Value Score), builds modular comparison tables, generates scene-specific model selection recommendations, and exports formatted reports directly to Google Docs/Drive folder 1fGd22eqVHetGLQ9tfFbYpdeY8mGoHGfK using google-office-tool.
---

# Google Gemini 全模态模型评测与性价比选型决策专家

本 Skill 专用于对 Google 官方现行可用的全系模型（文本理解/推理、图像生成、视频生成）进行自动化基准评测、多维度双向打分（纯能力评分 + 性价比评分），并输出结构化选型报告自动归档至指定的 Google Drive 文件夹。

## 🎯 核心功能与交付指标

1. **全模态分类覆盖**：
   - **文本与长上下文推理模型**：`gemini-3.1-pro-preview`, `gemini-3-pro-preview`, `gemini-3.8-flash`, `gemini-3.7-flash`, `gemini-3.6-flash`, `gemini-3.5-flash`, `gemini-3.5-flash-lite`, `gemini-3.1-flash-lite` 等。
   - **图像生成与编辑模型**：`gemini-3-pro-image-preview`, `gemini-3.1-flash-image`, `gemini-3.1-flash-lite-image`, `imagen-3.0-generate-002` 等。
   - **视频生成与动态影像模型**：`veo-3.1-generate-preview`, `veo-2.0-generate-001` 等。
2. **双维度评分体系**：
   - **纯能力评分 (Capability Score, 0~100)**：衡量模型的智力推理等级、首字响应延迟（TTFT）、吞吐量 TPS 以及请求稳定性。
   - **性价比评分 (Value / ROI Score, 0~100)**：结合模型输入/输出 Token 单价、单张图片价格或视频每秒单价，计算单位成本获取的综合能力收益。
3. **结构化分模态表格排版**：
   - 文本模型矩阵表、图像模型矩阵表、视频模型矩阵表。
4. **场景化选型建议**：
   - 提供针对企业复杂 Agent 推理、大规模 RAG 检索、高并发实时交互、低成本意图路由、多媒体内容生成的精准选型指引。
5. **云端自动归档与交付**：
   - 自动调用 `google-office-tool` 的 `create_google_doc_from_markdown`，将报告写入 Google Drive 目标文件夹：`1fGd22eqVHetGLQ9tfFbYpdeY8mGoHGfK`。
   - 报告文末附带经实测验证有效的官方文档与价格链接。

---

## 📐 评分计算算法模型

### 1. 文本/推理模型 (Text Models)
* **纯能力评分 (Capability Score, 0~100)**：
  - 推理等级基准（权重 60%）：Pro 系列基准 96~98 分；Flash 系列基准 86~90 分；Flash-Lite 系列基准 75~80 分。
  - 实测性能（权重 40%）：
    - TTFT 首字延迟（15%）：$\le 1.0\text{s}$ 为 100 分，$\le 2.0\text{s}$ 为 85 分，$> 4.0\text{s}$ 为 65 分。
    - 输出 TPS 吞吐（15%）：$\ge 60\text{ TPS}$ 为 100 分，$\ge 40\text{ TPS}$ 为 85 分，$\ge 15\text{ TPS}$ 为 70 分。
    - 成功率稳定性（10%）：$\text{成功率} \times 100$。
* **性价比评分 (Cost-Performance / Value Score, 0~100)**：
  - 综合有效单价：$\text{Cost}_{\text{eff}} = \text{Input\_Price} \times 0.2 + \text{Output\_Price} \times 0.8$（单位：$/1M Tokens，若处于促销期则按折扣价计算）。
  - 性价比评分：结合能力分平滑对数计算，归一化折算 0~100 分。

### 2. 双维度正交打标决策规则 (Orthogonal Badge Rules)
纯能力评分与性价比评分为两个完全正交的独立维度，严禁将能力高误打为经济标签：
* **⚡ 深度推理旗舰**：纯能力极高（Pro 系列或能力分 $\ge 90$），且单价处于高价值区间。专用于高难度 Agent 推理与复杂架构。
* **🥇 5折全能主力 (性价比冠军)**：通用能力优秀，同时享受官方限时 5 折（半价）优惠，综合 ROI 极高。
* **💰 经济首选 (极致低成本)**：有效单价处于超低区间（$\le \$0.20/\text{1M}$ 或 Flash-Lite 系列），专属用于超高频路由、低成本批量任务。
* **🚀 高速通用主力**：常规 Flash 模型标准定价状态。

### 2. 图像模型 (Image Models)
* **纯能力评分**：图像清晰度与指令遵循度基准（Pro 级 95 分，标准级 85 分）。
* **性价比评分**：结合单张生成单价（约 $0.02 ~ $0.04/张）折算。

### 3. 视频模型 (Video Models)
* **纯能力评分**：画面连贯度、高分辨率生成质量基准（Veo 3.1 得 96 分，Veo 2.0 得 88 分）。
* **性价比评分**：结合每秒生成费用折算。

---

## 🛠️ 执行流程与助手脚本

可以直接运行内置 Python 评估脚本完成端到端压测、评分和 Google Docs 云端写入：

```bash
python3 skills/gemini-model-evaluator-advisor/scripts/evaluate_and_report.py \
  --project spark-ccc \
  --folder-id 1fGd22eqVHetGLQ9tfFbYpdeY8mGoHGfK
```

或者由 Agent 交互逐步执行：
1. 调用 `gemini-benchmark-tool` 的 `list_available_models` 获取全量模型及定价。
2. 调用 `benchmark_vertex_ai` 进行实际基准采样。
3. 结合评分模型渲染 Markdown 报告。
4. 调用 `google-office-tool` 的 `create_google_doc_from_markdown` 写入 Google Drive 文件夹 `1fGd22eqVHetGLQ9tfFbYpdeY8mGoHGfK`。

---

## 🔗 官方参考链接库（已验证有效）

报告末尾必须包含以下官方有效参考链接：
1. **Google Cloud Vertex AI 官方定价文档**: https://cloud.google.com/vertex-ai/pricing
2. **Google AI Studio / Gemini API 官方定价文档**: https://ai.google.dev/pricing
3. **Google Cloud Agent Builder / Agent Platform 官方文档**: https://docs.cloud.google.com/agent-builder/overview
4. **Vertex AI 官方生成式模型目录与规格文档**: https://cloud.google.com/vertex-ai/generative-ai/docs/learn/models
