# 🏁 Channel PK Duel Report (Strategy Module)
**Session Timestamp**: `20260803_111409`
**Target Project**: `spark-ccc`
**Target Model Tested**: `gemini-3.1-flash-image`
**Traffic Stress Profile (压测用例)**: `标准画质巡检 (Flash Image Standard)`

## 📊 Summary Performance Comparison
| Metrics 比较维度 | 🟢 GCP Vertex AI (SA JSON) | 🔵 Gemini API (API Key) | 🏆 Winner 优胜者 |
| :--- | :--- | :--- | :--- |
| **总测试样本 (Total Trials)** | 3 次 | 3 次 | 双方等量 |
| **成功调用次数 (Success)** | 3 次 | 3 次 | 双方持平 |
| **测试成功率 (Success Rate)** | **100.0%** | **100.0%** | 双方持平 |
| **平均端到端延迟 (Avg Latency)** | **29.065 秒** | **23.346 秒** | 🔵 Gemini API (更低延迟) |
| **最小/最大延迟 (Min/Max)** | 27.15s / 30.46s | 19.15s / 27.81s | - |
| **总预估消耗费用 (Total Cost)** | **$0.29040** | **$0.45300** | 🟢 GCP Vertex AI (更低价格) |

## 📝 Trial-by-Trial Raw Results
### GCP Vertex AI (sa_vertex_ai)
| Trial # | Status | Latency | Cost | Error details (if any) |
| :---: | :---: | :--- | :--- | :--- |
| 1 | 🟢 OK | 29.583s | $0.09680 | - |
| 2 | 🟢 OK | 27.150s | $0.09680 | - |
| 3 | 🟢 OK | 30.462s | $0.09680 | - |

### Gemini API (gemini_api)
| Trial # | Status | Latency | Cost | Error details (if any) |
| :---: | :---: | :--- | :--- | :--- |
| 1 | 🔵 OK | 19.149s | $0.15100 | - |
| 2 | 🔵 OK | 23.081s | $0.15100 | - |
| 3 | 🔵 OK | 27.808s | $0.15100 | - |
