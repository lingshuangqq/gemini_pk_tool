# 🏁 Channel PK Duel Report (Strategy Module)
**Session Timestamp**: `20260803_105225`
**Target Project**: `sigma-axis-504006-f0`
**Target Model Tested**: `gemini-3.1-flash-lite-image`
**Traffic Stress Profile (压测用例)**: `standard`

## 📊 Summary Performance Comparison
| Metrics 比较维度 | 🟢 GCP Vertex AI (SA JSON) | 🔵 Gemini API (API Key) | 🏆 Winner 优胜者 |
| :--- | :--- | :--- | :--- |
| **总测试样本 (Total Trials)** | 3 次 | 3 次 | 双方等量 |
| **成功调用次数 (Success)** | 2 次 | 3 次 | Gemini API |
| **测试成功率 (Success Rate)** | **66.7%** | **100.0%** | 双方持平 |
| **平均端到端延迟 (Avg Latency)** | **4.648 秒** | **4.642 秒** | 🔵 Gemini API (更低延迟) |
| **最小/最大延迟 (Min/Max)** | 4.50s / 4.80s | 4.37s / 5.12s | - |
| **总预估消耗费用 (Total Cost)** | **$0.19360** | **$0.15300** | 🔵 Gemini API (更低价格) |

## 📝 Trial-by-Trial Raw Results
### GCP Vertex AI (sa_vertex_ai)
| Trial # | Status | Latency | Cost | Error details (if any) |
| :---: | :---: | :--- | :--- | :--- |
| 1 | 🟢 OK | 4.797s | $0.09680 | - |
| 2 | 🟢 OK | 4.499s | $0.09680 | - |
| 3 | 🔴 FAIL | 0.000s | $0.00000 | 429 RESOURCE_EXHAUSTED. {'error': {'code': 429, 'message': 'Resource has been exhausted (e.g. check quota).', 'status': 'RESOURCE_EXHAUSTED'}} |

### Gemini API (gemini_api)
| Trial # | Status | Latency | Cost | Error details (if any) |
| :---: | :---: | :--- | :--- | :--- |
| 1 | 🔵 OK | 5.125s | $0.05100 | - |
| 2 | 🔵 OK | 4.371s | $0.05100 | - |
| 3 | 🔵 OK | 4.430s | $0.05100 | - |
