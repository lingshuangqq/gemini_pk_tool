# 🏁 Channel PK Duel Report (Strategy Module)
**Session Timestamp**: `20260803_105225`
**Target Project**: `sigma-axis-504006-f0`
**Target Model Tested**: `gemini-3.5-flash-lite`
**Traffic Stress Profile (压测用例)**: `standard`

## 📊 Summary Performance Comparison
| Metrics 比较维度 | 🟢 GCP Vertex AI (SA JSON) | 🔵 Gemini API (API Key) | 🏆 Winner 优胜者 |
| :--- | :--- | :--- | :--- |
| **总测试样本 (Total Trials)** | 5 次 | 5 次 | 双方等量 |
| **成功调用次数 (Success)** | 5 次 | 5 次 | 双方持平 |
| **测试成功率 (Success Rate)** | **100.0%** | **100.0%** | 双方持平 |
| **平均端到端延迟 (Avg Latency)** | **1.148 秒** | **1.163 秒** | 🟢 GCP Vertex AI (更低延迟) |
| **最小/最大延迟 (Min/Max)** | 0.92s / 1.43s | 0.85s / 2.09s | - |
| **总预估消耗费用 (Total Cost)** | **$0.00005** | **$0.00005** | 🟢 GCP Vertex AI (更低价格) |

## 📝 Trial-by-Trial Raw Results
### GCP Vertex AI (sa_vertex_ai)
| Trial # | Status | Latency | Cost | Error details (if any) |
| :---: | :---: | :--- | :--- | :--- |
| 1 | 🟢 OK | 1.434s | $0.00001 | - |
| 2 | 🟢 OK | 1.160s | $0.00001 | - |
| 3 | 🟢 OK | 1.162s | $0.00001 | - |
| 4 | 🟢 OK | 1.062s | $0.00001 | - |
| 5 | 🟢 OK | 0.922s | $0.00001 | - |

### Gemini API (gemini_api)
| Trial # | Status | Latency | Cost | Error details (if any) |
| :---: | :---: | :--- | :--- | :--- |
| 1 | 🔵 OK | 2.088s | $0.00001 | - |
| 2 | 🔵 OK | 0.854s | $0.00001 | - |
| 3 | 🔵 OK | 0.957s | $0.00001 | - |
| 4 | 🔵 OK | 1.062s | $0.00001 | - |
| 5 | 🔵 OK | 0.852s | $0.00001 | - |
