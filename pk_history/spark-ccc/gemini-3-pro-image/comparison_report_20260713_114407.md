# 🏁 Channel PK Duel Report (Strategy Module)
**Session Timestamp**: `20260713_114407`
**Target Project**: `spark-ccc`
**Target Model Tested**: `gemini-3-pro-image`
**Traffic Stress Profile (压测用例)**: `standard`

## 📊 Summary Performance Comparison
| Metrics 比较维度 | 🟢 GCP Vertex AI (SA JSON) | 🔵 Gemini API (API Key) | 🏆 Winner 优胜者 |
| :--- | :--- | :--- | :--- |
| **总测试样本 (Total Trials)** | 2 次 | 2 次 | 双方等量 |
| **成功调用次数 (Success)** | 2 次 | 2 次 | 双方持平 |
| **测试成功率 (Success Rate)** | **100.0%** | **100.0%** | 双方持平 |
| **平均端到端延迟 (Avg Latency)** | **108.752 秒** | **46.480 秒** | 🔵 Gemini API (更低延迟) |
| **最小/最大延迟 (Min/Max)** | 98.11s / 119.40s | 43.59s / 49.37s | - |
| **总预估消耗费用 (Total Cost)** | **$0.19360** | **$0.48000** | 🟢 GCP Vertex AI (更低价格) |

## 📝 Trial-by-Trial Raw Results
### GCP Vertex AI (sa_vertex_ai)
| Trial # | Status | Latency | Cost | Error details (if any) |
| :---: | :---: | :--- | :--- | :--- |
| 1 | 🟢 OK | 119.395s | $0.09680 | - |
| 2 | 🟢 OK | 98.109s | $0.09680 | - |

### Gemini API (gemini_api)
| Trial # | Status | Latency | Cost | Error details (if any) |
| :---: | :---: | :--- | :--- | :--- |
| 1 | 🔵 OK | 43.590s | $0.24000 | - |
| 2 | 🔵 OK | 49.370s | $0.24000 | - |
