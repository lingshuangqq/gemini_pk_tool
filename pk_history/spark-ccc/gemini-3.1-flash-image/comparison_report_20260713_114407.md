# 🏁 Channel PK Duel Report (Strategy Module)
**Session Timestamp**: `20260713_114407`
**Target Project**: `spark-ccc`
**Target Model Tested**: `gemini-3.1-flash-image`
**Traffic Stress Profile (压测用例)**: `standard`

## 📊 Summary Performance Comparison
| Metrics 比较维度 | 🟢 GCP Vertex AI (SA JSON) | 🔵 Gemini API (API Key) | 🏆 Winner 优胜者 |
| :--- | :--- | :--- | :--- |
| **总测试样本 (Total Trials)** | 3 次 | 3 次 | 双方等量 |
| **成功调用次数 (Success)** | 3 次 | 3 次 | 双方持平 |
| **测试成功率 (Success Rate)** | **100.0%** | **100.0%** | 双方持平 |
| **平均端到端延迟 (Avg Latency)** | **26.722 秒** | **20.946 秒** | 🔵 Gemini API (更低延迟) |
| **最小/最大延迟 (Min/Max)** | 25.65s / 28.28s | 20.28s / 21.31s | - |
| **总预估消耗费用 (Total Cost)** | **$0.29040** | **$0.45300** | 🟢 GCP Vertex AI (更低价格) |

## 📝 Trial-by-Trial Raw Results
### GCP Vertex AI (sa_vertex_ai)
| Trial # | Status | Latency | Cost | Error details (if any) |
| :---: | :---: | :--- | :--- | :--- |
| 1 | 🟢 OK | 26.234s | $0.09680 | - |
| 2 | 🟢 OK | 28.278s | $0.09680 | - |
| 3 | 🟢 OK | 25.655s | $0.09680 | - |

### Gemini API (gemini_api)
| Trial # | Status | Latency | Cost | Error details (if any) |
| :---: | :---: | :--- | :--- | :--- |
| 1 | 🔵 OK | 21.242s | $0.15100 | - |
| 2 | 🔵 OK | 20.280s | $0.15100 | - |
| 3 | 🔵 OK | 21.314s | $0.15100 | - |
