# 🏆 Gemini Benchmark & Dual-Channel PK Suite (v3.0)

本项目是一个专门用于对 **Google Cloud Vertex AI (企业级 Service Account 授权)** 与 **Google AI Studio (Gemini API Key 授权)** 两个主流分发通道进行高并发、流式多维度竞技压测与基准评估的现代化开发工具箱。

支持通过 **CLI 脚本** 与 **MCP Server (Model Context Protocol)** 两种形态供工程师或 AI Agent 直接调度。

---

## 🌟 核心特性与架构升级 (v3.0)

1. **🚀 业内前沿多维度流式基准指标 (Industry Benchmark Standards)**：
   - **TTFT (Time to First Token)**：流式捕获首字生成延迟，真实反映端到端交互灵敏度。
   - **Output TPS (Throughput)**：纯输出解码速率（Tokens / Second）。
   - **Latency Jitter (StdDev)**：延迟标准差，量化网络与并发抖动，衡量服务稳定性（SLA）。
   - **Format Compliance**：结构化输出（JSON Schema）合规率与有效性校验。
   - **Cost Efficiency**：基于 2026 最新官方定价表，折算每 1 美元实际可产出 Token 数量（Tokens / $1）。
   - **Error Taxonomy**：细分归类 `429_RATE_LIMIT`、`500_SERVER_INTERNAL`、`400_LOCATION_UNSUPPORTED` 等错误。

2. **🧩 声明式模型系列与注册中心 (`core/registry.py`)**：
   按模型家族（Family）解耦管理，新增模型即插即用：
   - 🧠 **Pro 系列**（深度推理）：`gemini-3.1-pro-preview`、`gemini-3-pro-preview`
   - ⚡ **Flash 系列**（通用主力）：`gemini-3.8-flash` (2026 最新)、`gemini-3.7-flash`、`gemini-3.6-flash`、`gemini-3.5-flash`、`gemini-3-flash-preview`
   - 🪶 **Flash Lite 系列**（极速轻量）：`gemini-3.5-flash-lite`、`gemini-3.1-flash-lite`
   - 🍌 **NB 系列**（Nano-Banana / 图像生成）：`gemini-3-pro-image-preview` (`nano-banana-pro`)、`gemini-3.1-flash-image`、`gemini-3.1-flash-lite-image`
   - 🌐 **Omni 系列**（全能多模态）：`gemini-omni-flash-preview`

3. **🤖 原生 MCP Server 支持 (`mcp_server/`)**：
   基于 `FastMCP` 标准构建，无缝接入 **Antigravity CLI (`agy`)**、Claude Desktop、Cursor 等支持 MCP 的 AI Agent。

---

## 🛠️ MCP Server 工具集与使用指南

MCP Server 位于 `mcp_server/server.py`，对外暴露 4 个标准 MCP 工具：

| MCP Tool | 功能描述 | 核心入参 |
| :--- | :--- | :--- |
| **`list_available_models`** | 查询模型注册表中所有可用模型、系列分类与定价 | `family`: `"all"`, `"pro"`, `"flash"`, `"flash_lite"`, `"nano_banana"`, `"omni"` |
| **`benchmark_vertex_ai`** | 在 GCP Vertex AI 上进行多维度流式基准压测 | `project_id`, `location`, `families`, `models`, `trials`, `delay`, `prompt` |
| **`benchmark_channel_pk`** | 跨 Vertex AI 与 Gemini API 对同一模型进行双通道同频对决 | `model_id`, `project_id`, `trials`, `delay`, `prompt` |
| **`benchmark_gemini_api`** | 在 Gemini API (AI Studio) 上进行模型基准评测 | `families`, `models`, `trials`, `delay`, `api_key` |

### 🔧 在 Antigravity CLI (`agy`) 中配置 MCP

在全局配置文件 `~/.gemini/config/mcp_config.json` 的 `mcpServers` 下追加：

```json
{
  "mcpServers": {
    "gemini-benchmark-tool": {
      "command": "python3",
      "args": [
        "-m",
        "mcp_server.server"
      ],
      "cwd": "/path/to/gemini_pk_tool",
      "env": {
        "PYTHONPATH": "/path/to/gemini_pk_tool",
        "GOOGLE_APPLICATION_CREDENTIALS": "/path/to/your-service-account-key.json"
      }
    }
  }
}
```

---

## 🔑 凭据与秘钥配置指南 (Credentials & API Key Configuration)

本项目严格遵循“安全零硬编码”设计，支持通过**环境变量**、**命令行入参**或 **MCP 动态传参**三种方式灵活指定目标 GCP 项目与 Gemini API 凭证：

> 💡 **运行提示**：在不同环境或企业生产项目中运行时，无需修改任何代码，直接通过以下推荐方式指定对应的 GCP Project ID 与鉴权凭据即可。

### 1. GCP Vertex AI 通道 (Service Account 授权)

*   **方式 A：通过环境变量指定（推荐，全局通用）**
    ```bash
    export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your-service-account-key.json"
    ```
*   **方式 B：通过 CLI 命令行参数指定（适合快速切换不同业务项目）**
    ```bash
    python3 run_all_pk.py \
      --project "<YOUR_PROJECT_ID>" \
      --sa-key "/path/to/your-service-account-key.json"
    ```
*   **方式 C：通过 MCP 工具入参动态指定（供 AI Agent 调度）**
    在调用 `benchmark_vertex_ai` 或 `benchmark_channel_pk` 时，直接传递 `project_id` 和 `sa_key`：
    ```json
    {
      "project_id": "<YOUR_PROJECT_ID>",
      "sa_key": "/path/to/your-service-account-key.json",
      "models": ["gemini-3.8-flash"],
      "trials": 3
    }
    ```

### 2. Gemini API 通道 (Google AI Studio Key 授权)

*   **方式 A：通过环境变量指定（推荐）**
    ```bash
    export GEMINI_API_KEY="<YOUR_GEMINI_API_KEY>"
    ```
*   **方式 B：通过 CLI 命令行参数指定**
    ```bash
    python3 run_all_pk.py \
      --project "<YOUR_PROJECT_ID>" \
      --sa-key "/path/to/your-service-account-key.json" \
      --api-key "<YOUR_GEMINI_API_KEY>"
    ```
*   **方式 C：通过 MCP 工具入参动态指定（供 AI Agent 调度）**
    在调用 `benchmark_channel_pk` 或 `benchmark_gemini_api` 时，直接传递 `api_key`：
    ```json
    {
      "model_id": "gemini-3.8-flash",
      "project_id": "<YOUR_PROJECT_ID>",
      "sa_key": "/path/to/your-service-account-key.json",
      "api_key": "<YOUR_GEMINI_API_KEY>",
      "trials": 3
    }
    ```

---

## 💻 命令行执行与脚本测试

### 1. 运行 MCP Server 本地集成验证
```bash
python3 test_mcp_direct.py
```

### 2. 跨模型横向基准对比脚本
```bash
python3 compare_models_benchmark.py
```

### 3. 全自动化双通道 PK 压测与报告落盘
```bash
python3 run_all_pk.py \
  --project "<YOUR_PROJECT_ID>" \
  --sa-key "/path/to/your-service-account-key.json"
```

### 4. 快捷交互式压测启动
```bash
./run_pk_test.sh
```

---

## 📂 历史测试报告与审计落盘 (`pk_history/`)

所有压测细节与指标均按结构化规范落盘归档：

```
pk_history/
└── <GCP_Project_ID>/
    └── <Model_ID>/
        ├── comparison_report_<timestamp>.md       # 📄 Markdown 评测报告
        └── raw_metrics_<timestamp>.json           # 📄 原始数值指标 (JSON)
```

---

## 🔌 如何新增一个模型（零侵入扩展）

当 Google 推出新模型时（例如 `gemini-3.9-flash`），无需修改任何核心执行逻辑，仅需在 `core/registry.py` 中追加注册声明：

```python
ModelRegistry.register(ModelSpec(
    model_id="gemini-3.9-flash",
    display_name="Gemini 3.9 Flash",
    family=ModelFamily.FLASH,
    description="2026 全新主力模型",
    input_price_per_1m=0.075,
    output_price_per_1m=0.30,
    modalities=["text", "json", "streaming"],
    aliases=["3.9-flash"]
))
```

注册完成后，无论是 CLI 脚本还是 MCP Server 都会即时生效并提供支持！
