# 🏁 Channel PK Duel Report (Strategy Module)
**Session Timestamp**: `20260803_110628`
**Target Project**: `spark-ccc`
**Target Model Tested**: `gemini-3.1-pro-preview`
**Traffic Stress Profile (压测用例)**: `standard`

## 📊 Summary Performance Comparison
| Metrics 比较维度 | 🟢 GCP Vertex AI (SA JSON) | 🔵 Gemini API (API Key) | 🏆 Winner 优胜者 |
| :--- | :--- | :--- | :--- |
| **总测试样本 (Total Trials)** | 5 次 | 5 次 | 双方等量 |
| **成功调用次数 (Success)** | 4 次 | 5 次 | Gemini API |
| **测试成功率 (Success Rate)** | **80.0%** | **100.0%** | 双方持平 |
| **平均端到端延迟 (Avg Latency)** | **13.745 秒** | **4.663 秒** | 🔵 Gemini API (更低延迟) |
| **最小/最大延迟 (Min/Max)** | 6.01s / 21.22s | 4.18s / 5.18s | - |
| **总预估消耗费用 (Total Cost)** | **$0.00087** | **$0.00104** | 🟢 GCP Vertex AI (更低价格) |

## 📝 Trial-by-Trial Raw Results
### GCP Vertex AI (sa_vertex_ai)
| Trial # | Status | Latency | Cost | Error details (if any) |
| :---: | :---: | :--- | :--- | :--- |
| 1 | 🟢 OK | 21.219s | $0.00020 | - |
| 2 | 🟢 OK | 12.986s | $0.00020 | - |
| 3 | 🟢 OK | 6.007s | $0.00031 | - |
| 4 | 🟢 OK | 14.768s | $0.00015 | - |
| 5 | 🔴 FAIL | 0.000s | $0.00000 | 429 RESOURCE_EXHAUSTED. {'error': {'code': 429, 'message': 'Resource exhausted. Please try again later. Please refer to https://cloud.google.com/vertex-ai/generative-ai/docs/error-code-429 for more details.', 'status': 'RESOURCE_EXHAUSTED'}} |

### Gemini API (gemini_api)
| Trial # | Status | Latency | Cost | Error details (if any) |
| :---: | :---: | :--- | :--- | :--- |
| 1 | 🔵 OK | 4.679s | $0.00020 | - |
| 2 | 🔵 OK | 5.176s | $0.00021 | - |
| 3 | 🔵 OK | 4.178s | $0.00021 | - |
| 4 | 🔵 OK | 4.464s | $0.00020 | - |
| 5 | 🔵 OK | 4.815s | $0.00022 | - |
