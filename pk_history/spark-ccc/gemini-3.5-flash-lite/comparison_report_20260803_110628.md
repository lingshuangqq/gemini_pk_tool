# 🏁 Channel PK Duel Report (Strategy Module)
**Session Timestamp**: `20260803_110628`
**Target Project**: `spark-ccc`
**Target Model Tested**: `gemini-3.5-flash-lite`
**Traffic Stress Profile (压测用例)**: `standard`

## 📊 Summary Performance Comparison
| Metrics 比较维度 | 🟢 GCP Vertex AI (SA JSON) | 🔵 Gemini API (API Key) | 🏆 Winner 优胜者 |
| :--- | :--- | :--- | :--- |
| **总测试样本 (Total Trials)** | 5 次 | 5 次 | 双方等量 |
| **成功调用次数 (Success)** | 5 次 | 5 次 | 双方持平 |
| **测试成功率 (Success Rate)** | **100.0%** | **100.0%** | 双方持平 |
| **平均端到端延迟 (Avg Latency)** | **1.215 秒** | **0.982 秒** | 🔵 Gemini API (更低延迟) |
| **最小/最大延迟 (Min/Max)** | 0.93s / 1.83s | 0.78s / 1.33s | - |
| **总预估消耗费用 (Total Cost)** | **$0.00005** | **$0.00005** | 🟢 GCP Vertex AI (更低价格) |

## 📝 Trial-by-Trial Raw Results
### GCP Vertex AI (sa_vertex_ai)
| Trial # | Status | Latency | Cost | Error details (if any) |
| :---: | :---: | :--- | :--- | :--- |
| 1 | 🟢 OK | 1.831s | $0.00001 | - |
| 2 | 🟢 OK | 1.088s | $0.00001 | - |
| 3 | 🟢 OK | 1.149s | $0.00001 | - |
| 4 | 🟢 OK | 0.933s | $0.00001 | - |
| 5 | 🟢 OK | 1.076s | $0.00001 | - |

### Gemini API (gemini_api)
| Trial # | Status | Latency | Cost | Error details (if any) |
| :---: | :---: | :--- | :--- | :--- |
| 1 | 🔵 OK | 1.328s | $0.00001 | - |
| 2 | 🔵 OK | 0.784s | $0.00001 | - |
| 3 | 🔵 OK | 0.981s | $0.00001 | - |
| 4 | 🔵 OK | 0.932s | $0.00001 | - |
| 5 | 🔵 OK | 0.885s | $0.00001 | - |
