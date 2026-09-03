# 🏁 Channel PK Duel Report (Strategy Module)
**Session Timestamp**: `20260803_105225`
**Target Project**: `sigma-axis-504006-f0`
**Target Model Tested**: `gemini-3.1-flash-lite`
**Traffic Stress Profile (压测用例)**: `standard`

## 📊 Summary Performance Comparison
| Metrics 比较维度 | 🟢 GCP Vertex AI (SA JSON) | 🔵 Gemini API (API Key) | 🏆 Winner 优胜者 |
| :--- | :--- | :--- | :--- |
| **总测试样本 (Total Trials)** | 5 次 | 5 次 | 双方等量 |
| **成功调用次数 (Success)** | 5 次 | 5 次 | 双方持平 |
| **测试成功率 (Success Rate)** | **100.0%** | **100.0%** | 双方持平 |
| **平均端到端延迟 (Avg Latency)** | **1.679 秒** | **1.119 秒** | 🔵 Gemini API (更低延迟) |
| **最小/最大延迟 (Min/Max)** | 1.21s / 2.46s | 0.85s / 1.41s | - |
| **总预估消耗费用 (Total Cost)** | **$0.00040** | **$0.00009** | 🔵 Gemini API (更低价格) |

## 📝 Trial-by-Trial Raw Results
### GCP Vertex AI (sa_vertex_ai)
| Trial # | Status | Latency | Cost | Error details (if any) |
| :---: | :---: | :--- | :--- | :--- |
| 1 | 🟢 OK | 2.463s | $0.00008 | - |
| 2 | 🟢 OK | 1.380s | $0.00008 | - |
| 3 | 🟢 OK | 1.699s | $0.00008 | - |
| 4 | 🟢 OK | 1.211s | $0.00008 | - |
| 5 | 🟢 OK | 1.642s | $0.00008 | - |

### Gemini API (gemini_api)
| Trial # | Status | Latency | Cost | Error details (if any) |
| :---: | :---: | :--- | :--- | :--- |
| 1 | 🔵 OK | 1.346s | $0.00002 | - |
| 2 | 🔵 OK | 0.845s | $0.00002 | - |
| 3 | 🔵 OK | 1.407s | $0.00002 | - |
| 4 | 🔵 OK | 0.918s | $0.00002 | - |
| 5 | 🔵 OK | 1.078s | $0.00002 | - |
