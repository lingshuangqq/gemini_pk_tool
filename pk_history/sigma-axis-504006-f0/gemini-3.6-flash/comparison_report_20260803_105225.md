# 🏁 Channel PK Duel Report (Strategy Module)
**Session Timestamp**: `20260803_105225`
**Target Project**: `sigma-axis-504006-f0`
**Target Model Tested**: `gemini-3.6-flash`
**Traffic Stress Profile (压测用例)**: `standard`

## 📊 Summary Performance Comparison
| Metrics 比较维度 | 🟢 GCP Vertex AI (SA JSON) | 🔵 Gemini API (API Key) | 🏆 Winner 优胜者 |
| :--- | :--- | :--- | :--- |
| **总测试样本 (Total Trials)** | 5 次 | 5 次 | 双方等量 |
| **成功调用次数 (Success)** | 5 次 | 5 次 | 双方持平 |
| **测试成功率 (Success Rate)** | **100.0%** | **100.0%** | 双方持平 |
| **平均端到端延迟 (Avg Latency)** | **3.129 秒** | **2.712 秒** | 🔵 Gemini API (更低延迟) |
| **最小/最大延迟 (Min/Max)** | 2.59s / 3.63s | 2.31s / 3.32s | - |
| **总预估消耗费用 (Total Cost)** | **$0.00002** | **$0.00002** | 🟢 GCP Vertex AI (更低价格) |

## 📝 Trial-by-Trial Raw Results
### GCP Vertex AI (sa_vertex_ai)
| Trial # | Status | Latency | Cost | Error details (if any) |
| :---: | :---: | :--- | :--- | :--- |
| 1 | 🟢 OK | 3.628s | $0.00000 | - |
| 2 | 🟢 OK | 3.136s | $0.00000 | - |
| 3 | 🟢 OK | 3.488s | $0.00000 | - |
| 4 | 🟢 OK | 2.594s | $0.00000 | - |
| 5 | 🟢 OK | 2.800s | $0.00000 | - |

### Gemini API (gemini_api)
| Trial # | Status | Latency | Cost | Error details (if any) |
| :---: | :---: | :--- | :--- | :--- |
| 1 | 🔵 OK | 3.321s | $0.00000 | - |
| 2 | 🔵 OK | 2.560s | $0.00000 | - |
| 3 | 🔵 OK | 2.669s | $0.00000 | - |
| 4 | 🔵 OK | 2.312s | $0.00000 | - |
| 5 | 🔵 OK | 2.700s | $0.00000 | - |
