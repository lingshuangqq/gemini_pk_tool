# 🏁 Channel PK Duel Report (Strategy Module)
**Session Timestamp**: `20260803_105225`
**Target Project**: `sigma-axis-504006-f0`
**Target Model Tested**: `gemini-3-pro-image`
**Traffic Stress Profile (压测用例)**: `standard`

## 📊 Summary Performance Comparison
| Metrics 比较维度 | 🟢 GCP Vertex AI (SA JSON) | 🔵 Gemini API (API Key) | 🏆 Winner 优胜者 |
| :--- | :--- | :--- | :--- |
| **总测试样本 (Total Trials)** | 2 次 | 2 次 | 双方等量 |
| **成功调用次数 (Success)** | 1 次 | 2 次 | Gemini API |
| **测试成功率 (Success Rate)** | **50.0%** | **100.0%** | 双方持平 |
| **平均端到端延迟 (Avg Latency)** | **54.464 秒** | **45.393 秒** | 🔵 Gemini API (更低延迟) |
| **最小/最大延迟 (Min/Max)** | 54.46s / 54.46s | 42.79s / 48.00s | - |
| **总预估消耗费用 (Total Cost)** | **$0.09680** | **$0.48000** | 🟢 GCP Vertex AI (更低价格) |

## 📝 Trial-by-Trial Raw Results
### GCP Vertex AI (sa_vertex_ai)
| Trial # | Status | Latency | Cost | Error details (if any) |
| :---: | :---: | :--- | :--- | :--- |
| 1 | 🟢 OK | 54.464s | $0.09680 | - |
| 2 | 🔴 FAIL | 0.000s | $0.00000 | 429 RESOURCE_EXHAUSTED. {'error': {'code': 429, 'message': 'Resource has been exhausted (e.g. check quota).', 'status': 'RESOURCE_EXHAUSTED'}} |

### Gemini API (gemini_api)
| Trial # | Status | Latency | Cost | Error details (if any) |
| :---: | :---: | :--- | :--- | :--- |
| 1 | 🔵 OK | 47.998s | $0.24000 | - |
| 2 | 🔵 OK | 42.789s | $0.24000 | - |
