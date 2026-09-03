# 🏁 Channel PK Duel Report (Strategy Module)
**Session Timestamp**: `20260713_114407`
**Target Project**: `spark-ccc`
**Target Model Tested**: `gemini-3.1-flash-lite`
**Traffic Stress Profile (压测用例)**: `standard`

## 📊 Summary Performance Comparison
| Metrics 比较维度 | 🟢 GCP Vertex AI (SA JSON) | 🔵 Gemini API (API Key) | 🏆 Winner 优胜者 |
| :--- | :--- | :--- | :--- |
| **总测试样本 (Total Trials)** | 5 次 | 5 次 | 双方等量 |
| **成功调用次数 (Success)** | 5 次 | 5 次 | 双方持平 |
| **测试成功率 (Success Rate)** | **100.0%** | **100.0%** | 双方持平 |
| **平均端到端延迟 (Avg Latency)** | **1.178 秒** | **0.833 秒** | 🔵 Gemini API (更低延迟) |
| **最小/最大延迟 (Min/Max)** | 0.99s / 1.67s | 0.78s / 0.86s | - |
| **总预估消耗费用 (Total Cost)** | **$0.00040** | **$0.00009** | 🔵 Gemini API (更低价格) |

## 📝 Trial-by-Trial Raw Results
### GCP Vertex AI (sa_vertex_ai)
| Trial # | Status | Latency | Cost | Error details (if any) |
| :---: | :---: | :--- | :--- | :--- |
| 1 | 🟢 OK | 1.667s | $0.00008 | - |
| 2 | 🟢 OK | 1.161s | $0.00008 | - |
| 3 | 🟢 OK | 1.030s | $0.00008 | - |
| 4 | 🟢 OK | 1.040s | $0.00009 | - |
| 5 | 🟢 OK | 0.990s | $0.00008 | - |

### Gemini API (gemini_api)
| Trial # | Status | Latency | Cost | Error details (if any) |
| :---: | :---: | :--- | :--- | :--- |
| 1 | 🔵 OK | 0.857s | $0.00002 | - |
| 2 | 🔵 OK | 0.839s | $0.00002 | - |
| 3 | 🔵 OK | 0.858s | $0.00002 | - |
| 4 | 🔵 OK | 0.785s | $0.00002 | - |
| 5 | 🔵 OK | 0.827s | $0.00002 | - |
