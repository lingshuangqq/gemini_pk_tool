# 🏁 Channel PK Duel Report (Strategy Module)
**Session Timestamp**: `20260903_102138`
**Target Project**: `spark-ccc`
**Target Model Tested**: `gemini-3.8-flash`
**Traffic Stress Profile (压测用例)**: `standard`

## 📊 Summary Performance Comparison
| Metrics 比较维度 | 🟢 GCP Vertex AI (SA JSON) | 🔵 Gemini API (API Key) | 🏆 Winner 优胜者 |
| :--- | :--- | :--- | :--- |
| **总测试样本 (Total Trials)** | 5 次 | 5 次 | 双方等量 |
| **成功调用次数 (Success)** | 4 次 | 0 次 | GCP Vertex AI |
| **测试成功率 (Success Rate)** | **80.0%** | **0.0%** | 🟢 GCP Vertex AI |
| **平均端到端延迟 (Avg Latency)** | **2.474 秒** | **0.000 秒** | 暂无成功数据 |
| **最小/最大延迟 (Min/Max)** | 2.25s / 2.78s | 0.00s / 0.00s | - |
| **总预估消耗费用 (Total Cost)** | **$0.00002** | **$0.00000** | 🔵 Gemini API (更低价格) |

## 📝 Trial-by-Trial Raw Results
### GCP Vertex AI (sa_vertex_ai)
| Trial # | Status | Latency | Cost | Error details (if any) |
| :---: | :---: | :--- | :--- | :--- |
| 1 | 🟢 OK | 2.580s | $0.00001 | - |
| 2 | 🟢 OK | 2.784s | $0.00000 | - |
| 3 | 🟢 OK | 2.281s | $0.00000 | - |
| 4 | 🔴 FAIL | 0.000s | $0.00000 | 500 INTERNAL. {'error': {'code': 500, 'message': 'Internal error encountered.', 'status': 'INTERNAL'}} |
| 5 | 🟢 OK | 2.252s | $0.00000 | - |

### Gemini API (gemini_api)
| Trial # | Status | Latency | Cost | Error details (if any) |
| :---: | :---: | :--- | :--- | :--- |
| 1 | 🔴 FAIL | 0.000s | $0.00000 | 400 FAILED_PRECONDITION. {'error': {'code': 400, 'message': 'User location is not supported for the API use.', 'status': 'FAILED_PRECONDITION'}} |
| 2 | 🔴 FAIL | 0.000s | $0.00000 | 400 FAILED_PRECONDITION. {'error': {'code': 400, 'message': 'User location is not supported for the API use.', 'status': 'FAILED_PRECONDITION'}} |
| 3 | 🔴 FAIL | 0.000s | $0.00000 | 400 FAILED_PRECONDITION. {'error': {'code': 400, 'message': 'User location is not supported for the API use.', 'status': 'FAILED_PRECONDITION'}} |
| 4 | 🔴 FAIL | 0.000s | $0.00000 | 400 FAILED_PRECONDITION. {'error': {'code': 400, 'message': 'User location is not supported for the API use.', 'status': 'FAILED_PRECONDITION'}} |
| 5 | 🔴 FAIL | 0.000s | $0.00000 | 400 FAILED_PRECONDITION. {'error': {'code': 400, 'message': 'User location is not supported for the API use.', 'status': 'FAILED_PRECONDITION'}} |
