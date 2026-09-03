# 🏁 Channel PK Duel Report (Strategy Module)
**Session Timestamp**: `20260803_105225`
**Target Project**: `sigma-axis-504006-f0`
**Target Model Tested**: `gemini-3.1-pro-preview`
**Traffic Stress Profile (压测用例)**: `standard`

## 📊 Summary Performance Comparison
| Metrics 比较维度 | 🟢 GCP Vertex AI (SA JSON) | 🔵 Gemini API (API Key) | 🏆 Winner 优胜者 |
| :--- | :--- | :--- | :--- |
| **总测试样本 (Total Trials)** | 5 次 | 5 次 | 双方等量 |
| **成功调用次数 (Success)** | 5 次 | 5 次 | 双方持平 |
| **测试成功率 (Success Rate)** | **100.0%** | **100.0%** | 双方持平 |
| **平均端到端延迟 (Avg Latency)** | **4.062 秒** | **4.858 秒** | 🟢 GCP Vertex AI (更低延迟) |
| **最小/最大延迟 (Min/Max)** | 3.73s / 4.57s | 4.12s / 5.68s | - |
| **总预估消耗费用 (Total Cost)** | **$0.00096** | **$0.00094** | 🔵 Gemini API (更低价格) |

## 📝 Trial-by-Trial Raw Results
### GCP Vertex AI (sa_vertex_ai)
| Trial # | Status | Latency | Cost | Error details (if any) |
| :---: | :---: | :--- | :--- | :--- |
| 1 | 🟢 OK | 4.204s | $0.00019 | - |
| 2 | 🟢 OK | 4.569s | $0.00017 | - |
| 3 | 🟢 OK | 3.956s | $0.00020 | - |
| 4 | 🟢 OK | 3.733s | $0.00020 | - |
| 5 | 🟢 OK | 3.850s | $0.00020 | - |

### Gemini API (gemini_api)
| Trial # | Status | Latency | Cost | Error details (if any) |
| :---: | :---: | :--- | :--- | :--- |
| 1 | 🔵 OK | 4.122s | $0.00020 | - |
| 2 | 🔵 OK | 4.863s | $0.00013 | - |
| 3 | 🔵 OK | 4.564s | $0.00021 | - |
| 4 | 🔵 OK | 5.678s | $0.00020 | - |
| 5 | 🔵 OK | 5.065s | $0.00021 | - |
