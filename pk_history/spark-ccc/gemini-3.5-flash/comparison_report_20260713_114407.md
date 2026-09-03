# 🏁 Channel PK Duel Report (Strategy Module)
**Session Timestamp**: `20260713_114407`
**Target Project**: `spark-ccc`
**Target Model Tested**: `gemini-3.5-flash`
**Traffic Stress Profile (压测用例)**: `standard`

## 📊 Summary Performance Comparison
| Metrics 比较维度 | 🟢 GCP Vertex AI (SA JSON) | 🔵 Gemini API (API Key) | 🏆 Winner 优胜者 |
| :--- | :--- | :--- | :--- |
| **总测试样本 (Total Trials)** | 5 次 | 5 次 | 双方等量 |
| **成功调用次数 (Success)** | 5 次 | 5 次 | 双方持平 |
| **测试成功率 (Success Rate)** | **100.0%** | **100.0%** | 双方持平 |
| **平均端到端延迟 (Avg Latency)** | **3.173 秒** | **2.008 秒** | 🔵 Gemini API (更低延迟) |
| **最小/最大延迟 (Min/Max)** | 1.64s / 7.18s | 1.81s / 2.36s | - |
| **总预估消耗费用 (Total Cost)** | **$0.00011** | **$0.00002** | 🔵 Gemini API (更低价格) |

## 📝 Trial-by-Trial Raw Results
### GCP Vertex AI (sa_vertex_ai)
| Trial # | Status | Latency | Cost | Error details (if any) |
| :---: | :---: | :--- | :--- | :--- |
| 1 | 🟢 OK | 2.069s | $0.00002 | - |
| 2 | 🟢 OK | 7.179s | $0.00002 | - |
| 3 | 🟢 OK | 2.942s | $0.00003 | - |
| 4 | 🟢 OK | 1.635s | $0.00002 | - |
| 5 | 🟢 OK | 2.039s | $0.00002 | - |

### Gemini API (gemini_api)
| Trial # | Status | Latency | Cost | Error details (if any) |
| :---: | :---: | :--- | :--- | :--- |
| 1 | 🔵 OK | 1.954s | $0.00000 | - |
| 2 | 🔵 OK | 1.809s | $0.00000 | - |
| 3 | 🔵 OK | 1.892s | $0.00000 | - |
| 4 | 🔵 OK | 2.363s | $0.00000 | - |
| 5 | 🔵 OK | 2.022s | $0.00000 | - |
