# 🏆 GCP Vertex AI vs Gemini API (Google AI Studio) 双通道同频竞技平台 (v2.0)

本项目是一个专门用于对 **GCP Vertex AI (Service Account 授权)** 与 **Google AI Studio (Gemini API Key 授权)** 两个主流大模型分发通道进行高并发、同频同负载、多维度竞技压测的通用开发测试平台。

---

## 🎯 1. 当前文件夹下代码的主要任务 (Core Objectives & Major Tasks)

本目录（`gcp_vs_geminiapi_pk_tool`）下代码的核心任务是在**排除网络及提示词差异**的绝对控制变量前提下，通过双向客户端在毫秒级的极小时间差内，针对完全相同的输入执行压测。其主要任务包括：

1.  **📊 多维度性能基准压测 (E2E Benchmark)**：
    测量同一款模型在两个不同云端分发渠道的**端到端请求延迟 (End-to-End Latency)**。
2.  **真实阻断与频控极限校验 (429 & Quota Check)**：
    在高并发状态下，评估两个通道对于不同调用频次（RPM/TPM）的弹抗能力，暴露并统计 `429 (Resource Exhausted)` 频控报错的真实边界。
3.  **💰 实际计费精细比对 (Cost Disparity Analysis)**：
    分别采用 Vertex AI（标准 Token 段计费）和 AI Studio（Character段/单图固定计费）的 **2026 最新官方定价表**，折算每一次请求的实际消耗金额，帮助业务做出最具性价比的架构选型。
4.  **💾 自动化审计与历史数据落盘 (Unified Run Archiver)**：
    将所有的压测细节、请求/返回 Snippet、报错堆栈以及量化对比表格，按照“项目 -> 模型”的层级结构一站式打包归档，确保历史压测结果可回溯、可追溯。

---

## 🚦 2. 模型定制化“流量压测测试用例”矩阵 (Traffic Stress Profiles)

不同的模型由于其底层计算复杂度及各渠道默认配额（Quota）的巨大差异，强制采用统一的压力配置是不科学的。

因此，本项目**为每个模型独立内置了定制化的流量压测测试用例（Traffic Stress Case）**。这些用例经过精密折算，既能最大化榨干配额上限，又能避免触发毁灭性的 100% 账号阻断：

| 模型标识 (Model ID) | 压测用例名 (Stress Case) | 试运行次数 (Trials) | 发送冷却间隔 (Delay) | 🎯 核心压测目的 |
| :--- | :--- | :---: | :---: | :--- |
| **`gemini-3.1-flash-lite`** | 🟢 标准巡检 (Standard) | 5 次 | 1.5s | 常规的通道连通性及状态巡检。 |
| (极速文本大配额) | 🟡 中载压力 (Concurrency Stress) | 20 次 | 0.4s | 模拟高吞吐量下，极速大模型的并发承受力。 |
| | 🔴 极限高频 (Heavy Burst) | 40 次 | 0.1s | 极速爆破测试，考验双通道的高密突发吞吐能力。 |
| **`gemini-3.5-flash`** | 🟢 标准巡检 (Standard) | 5 次 | 1.5s | 针对最新 3.5 代标准型 Flash 通道连通比对。 |
| (最新旗舰级 Flash) | 🟡 高频并发 (Concurrency Stress) | 25 次 | 0.3s | 密集压力测试，考验 3.5 通道多路分发负载力。 |
| | 🔴 极限冲击 (Heavy Burst) | 50 次 | 0.1s | 极短延迟下突破厂商速率红线，评估限流阈值。 |
| **`gemini-omni-flash-preview`**| 🟢 标准巡检 (Standard) | 5 次 | 1.5s | 最新 Omni 模态标准文本交互性能巡检。 |
| (最新多模态 Omni 通道) | 🟡 并发性能 (Concurrency Stress) | 20 次 | 0.4s | 模拟全模态分发中，多通道吞吐及延迟损耗。 |
| | 🔴 极限吞吐 (Heavy Burst) | 40 次 | 0.1s | 超强密集请求冲击，探测新模态频控边界。 |
| **`gemini-3.1-pro-preview`**| 🟢 标准巡检 (Standard) | 5 次 | 2.0s | 高阶推理模型的常规连通与延迟对比。 |
| (长文本高推理配额) | 🟡 中载推理 (Reasoning Stress) | 10 次 | 1.0s | 模拟高难度长推理状态下的中高并发持续运行。 |
| | 🔴 极限吞吐 (Extreme Depth) | 15 次 | 0.6s | 逼近大模型 TPM/RPM 保护墙的深度压测。 |
| **`gemini-3.1-flash-lite-image`**| 🟢 标准画质 (Standard) | 3 次 | 3.0s | 常规 1K 图像生成速度及初始画质评测。 |
| (轻量级多模态图像) | 🟡 高频图像 (Image Concurrency Stress) | 8 次 | 1.5s | 触发高频多模态图像分发，测试其频控吞吐瓶颈。 |
| **`gemini-3.1-flash-image`** | 🟢 标准画质 (Standard) | 3 次 | 4.0s | 标准 2K 图像生成的时延及多模态协同巡检。 |
| (标准级多模态图像) | 🟡 图像压力 (Flash Image Stress Blast) | 6 次 | 2.0s | 中度高强度的 2K 图像配额极限拉压。 |
| **`gemini-3-pro-image`** | 🟢 标准画质 (Standard) | 2 次 | 5.0s | 4K 超高清旗舰图像生成的时间/带宽延迟拉拽。 |
| (旗舰级超清多模态图像) | 🟡 图像压力 (Pro Image Stress Blast) | 5 次 | 3.0s | 极速大尺寸图像频发，对双渠道最核心配额壁垒进行压力试探。 |

---

## 💻 3. 运行方式与启动命令 (Execution Methods & Startup Commands)

本工具箱提供两种运行方式，分别满足**极简交互**与**企业自动化 CI/CD 评测**的不同需要：

### 🚀 方式一：快捷交互式启动 (推荐，带参数自动缓存与压测用例自由选择)
专为本地开发/测试人员设计。在您选定大模型后，**系统会自动呈上针对该模型专属定制的“流量压测用例”菜单**，免去您手动记忆 and 输入 Trials / Delay 值的繁琐：

*   **启动命令**：
    ```bash
    ./run_pk_test.sh
    ```
*   **运行步骤演示**：
    1.  **GCP 密钥选择**：脚本在终端中列出候选 JSON 密钥，键入序号（如 `1`）或直接按回车确认。
    2.  **API Key 确认**：直接回车复用上次缓存的 Gemini API Key。
    3.  **选择评测模型**：例如输入 `5` 选择最新 `gemini-3.5-flash`。
    4.  **🎯 压测用例匹配**：系统会动态调出该模型的专属用例菜单，供您一键施压：
        ```
        📊 Choose Traffic Stress Case (压测用例) for gemini-3.5-flash:
          1) 标准巡检 (Standard)          - 5 trials, 1.5s delay
          2) 高频并发 (Concurrency Stress) - 25 trials, 0.3s delay
          3) 极限冲击 (Heavy Burst)        - 50 trials, 0.1s delay
        Select stress case [1-3, default: 1]: 2
        ```

---

### ⚙️ 方式二：中枢控制器启动 (Orchestrator Mode)
专为脚本化、定时触发或 CI/CD 测试管道设计。通过直接调用中枢调度器，传入 `--profile` 标识即可自动拉起测试用例参数。

*   **基本启动命令 (使用预设流量用例)**：
    ```bash
    python3 pk_controller.py \
      --sa-key "../gcp_quota_warmup_tool/openclaw-slam-001/openclaw-slam-001-73ab12289173.json" \
      --project "openclaw-slam-001" \
      --api-key "your-gemini-api-key" \
      --model "gemini-3.5-flash" \
      --profile "concurrency_stress"
    ```
*   **手工超越压测参数 (Manual Override)**：
    如果您想要超越任何内置用例参数，可以使用 `--trials` 和 `--delay` 参数进行强制覆盖：
    ```bash
    python3 pk_controller.py \
      --sa-key "../gcp_quota_warmup_tool/openclaw-slam-001/openclaw-slam-001-73ab12289173.json" \
      --project "openclaw-slam-001" \
      --api-key "your-gemini-api-key" \
      --model "gemini-3.5-flash" \
      --trials 100 \
      --delay 0.05
    ```

---

## 🎨 4. 插件式架构设计与目录树

项目采用了高内聚、低耦合的设计，所有模型压测策略独立成卡：

```
gcp_vs_geminiapi_pk_tool/
├── README.md                      # 📖 本说明文档
├── pk_controller.py               # 🎮 【中枢控制器】：统一入口及核心调度，负责动态导入和执行对应模型策略
├── run_pk_test.sh                 # 🚀 【统一启动脚本】：支持交互式预设、SA json文件自动搜索、Project ID自动提取及密钥缓存
└── models/                        # 🔌 【策略插件包】
    ├── __init__.py                # 🔑 【策略注册表】：维护 Model ID 到测试类的映射关系
    ├── base_tester.py             # 📐 【测试基类】：封装双客户端初始化、双向并发Trial循环、动态分流日志、MD及JSON生成
    ├── gemini_3_1_flash_lite.py   # 📝 【文本 Lite 插件】
    ├── gemini_3_1_pro_preview.py  # 📝 【文本 Pro 插件】
    ├── gemini_3_1_flash_lite_image.py # 🎨 【图像 Lite 插件】
    ├── gemini_3_1_flash_image.py  # 🎨 【图像 Flash 插件】
    ├── gemini_3_pro_image.py      # 🎨 【图像 Pro 插件】
    ├── gemini_3_5_flash.py        # 📝 【最新 3.5 Flash 插件】 (新增)
    └── gemini_omni_flash_preview.py # 📝 【最新 Omni Flash 插件】 (新增)
```

---

## 📂 5. 日志与归档存储规范 (Project & Model Isolation)

为了保证压测日志的可追溯性与绝对隔离，系统抛弃了混杂日志的写入逻辑，改用 **以项目和模型为根节点** 的规范化目录：

```
pk_history/
└── <GCP_Project_ID>/                    # 第一层 (例如: openclaw-slam-001)
    └── <Model_ID>/                      # 第二层 (例如: gemini-3.5-flash)
        ├── sa_vertex_ai_run_<timestamp>.log       # 🟢 GCP Vertex AI (SA JSON) 专属底层通信日志
        ├── gemini_api_run_<timestamp>.log         # 🔵 Gemini API (API Key) 专属底层通信日志
        ├── comparison_report_<timestamp>.md       # 📄 PK 评测分析对照报告 (Markdown 格式)
        └── raw_metrics_<timestamp>.json           # 📄 结构化原始指标数据 (JSON 格式)
```

每个文件均附加 `_<timestamp>` 唯一时间戳（格式为 `YYYYMMDD_HHMMSS`），支持多次测试记录和谐共存。

---

## 🔌 6. 如何新增一个模型插件（无损扩展指南）

当 Google 推出全新大模型（例如：`gemini-3.5-pro`），您只需简单两步即可扩容对比：

### 第一步：在 `models/` 目录下创建对应策略类并指定它的测试用例
新建文件 `models/gemini_3_5_pro.py`：
```python
import asyncio
from google.genai import types
from .base_tester import BaseModelTester

class Gemini35ProTester(BaseModelTester):
    def __init__(self, project_id, location, sa_key, api_key, timestamp):
        super().__init__(
            model_id="gemini-3.5-pro", # 设定模型唯一 Key
            project_id=project_id,
            location=location,
            sa_key=sa_key,
            api_key=api_key,
            timestamp=timestamp
        )

    @classmethod
    def get_traffic_profiles(cls):
        # ⚠️ 必须在这里声明该模型专属的压测流量测试用例
        return {
            "standard": {"name": "标准巡检", "trials": 5, "delay": 2.0, "desc": "常规同频推理校验"},
            "pro_stress": {"name": "密集推理压测", "trials": 12, "delay": 0.8, "desc": "高并发下 3.5 Pro 性能评估"}
        }

    def get_default_prompt(self):
        return "请写一段100字的Gemini 3.5 Pro架构分析。"

    async def execute_gcp_call(self, prompt, index):
        loop = asyncio.get_running_loop()
        config = types.GenerateContentConfig(temperature=0.4, max_output_tokens=500)
        
        response = await loop.run_in_executor(
            None,
            lambda: self.gcp_client.models.generate_content(
                model=self.model_id, contents=prompt, config=config
            )
        )
        cost = 0.005 # 示例估算费用
        return True, cost, len(response.text), ""

    async def execute_api_call(self, prompt, index):
        loop = asyncio.get_running_loop()
        config = types.GenerateContentConfig(temperature=0.4, max_output_tokens=500)
        
        response = await loop.run_in_executor(
            None,
            lambda: self.api_client.models.generate_content(
                model=self.model_id, contents=prompt, config=config
            )
        )
        cost = 0.003 # 示例
        return True, cost, len(response.text), ""
```

### 第二步：在 `models/__init__.py` 中注册它
打开 `models/__init__.py` 并导入/注册您的新类：
```python
# 1. 导入
from .gemini_3_5_pro import Gemini35ProTester

# 2. 注册进字典
MODEL_REGISTRY = {
    # ... 现有模型
    "gemini-3.5-pro": Gemini35ProTester,
}
```

**✅ 注册完成！** 
此时，中枢控制器 `pk_controller.py --model gemini-3.5-pro --profile pro_stress` 便能立刻调用并执行此全新大模型定制用例。
