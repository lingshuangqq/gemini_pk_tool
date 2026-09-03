# 🏁 Channel PK Duel Report (Strategy Module)
**Session Timestamp**: `20260803_110628`
**Target Project**: `spark-ccc`
**Target Model Tested**: `gemini-3.6-flash`
**Traffic Stress Profile (压测用例)**: `standard`

## 📊 Summary Performance Comparison
| Metrics 比较维度 | 🟢 GCP Vertex AI (SA JSON) | 🔵 Gemini API (API Key) | 🏆 Winner 优胜者 |
| :--- | :--- | :--- | :--- |
| **总测试样本 (Total Trials)** | 5 次 | 5 次 | 双方等量 |
| **成功调用次数 (Success)** | 4 次 | 5 次 | Gemini API |
| **测试成功率 (Success Rate)** | **80.0%** | **100.0%** | 双方持平 |
| **平均端到端延迟 (Avg Latency)** | **3.204 秒** | **2.778 秒** | 🔵 Gemini API (更低延迟) |
| **最小/最大延迟 (Min/Max)** | 2.68s / 4.21s | 2.13s / 3.68s | - |
| **总预估消耗费用 (Total Cost)** | **$0.00002** | **$0.00002** | 🟢 GCP Vertex AI (更低价格) |

## 📝 Trial-by-Trial Raw Results
### GCP Vertex AI (sa_vertex_ai)
| Trial # | Status | Latency | Cost | Error details (if any) |
| :---: | :---: | :--- | :--- | :--- |
| 1 | 🔴 FAIL | 0.000s | $0.00000 | 429 RESOURCE_EXHAUSTED. {'error': {'code': 429, 'message': 'Resource has been exhausted (e.g. check quota).', 'status': 'RESOURCE_EXHAUSTED'}} |
| 2 | 🟢 OK | 4.209s | $0.00000 | - |
| 3 | 🟢 OK | 2.683s | $0.00000 | - |
| 4 | 🟢 OK | 2.972s | $0.00000 | - |
| 5 | 🟢 OK | 2.951s | $0.00000 | - |

### Gemini API (gemini_api)
| Trial # | Status | Latency | Cost | Error details (if any) |
| :---: | :---: | :--- | :--- | :--- |
| 1 | 🔵 OK | 3.684s | $0.00000 | - |
| 2 | 🔵 OK | 2.128s | $0.00000 | - |
| 3 | 🔵 OK | 2.640s | $0.00000 | - |
| 4 | 🔵 OK | 2.467s | $0.00000 | - |
| 5 | 🔵 OK | 2.969s | $0.00000 | - |
