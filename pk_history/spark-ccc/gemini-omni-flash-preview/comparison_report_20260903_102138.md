# 🏁 Channel PK Duel Report (Strategy Module)
**Session Timestamp**: `20260903_102138`
**Target Project**: `spark-ccc`
**Target Model Tested**: `gemini-omni-flash-preview`
**Traffic Stress Profile (压测用例)**: `standard`

## 📊 Summary Performance Comparison
| Metrics 比较维度 | 🟢 GCP Vertex AI (SA JSON) | 🔵 Gemini API (API Key) | 🏆 Winner 优胜者 |
| :--- | :--- | :--- | :--- |
| **总测试样本 (Total Trials)** | 5 次 | 5 次 | 双方等量 |
| **成功调用次数 (Success)** | 5 次 | 0 次 | GCP Vertex AI |
| **测试成功率 (Success Rate)** | **100.0%** | **0.0%** | 🟢 GCP Vertex AI |
| **平均端到端延迟 (Avg Latency)** | **4.754 秒** | **0.000 秒** | 暂无成功数据 |
| **最小/最大延迟 (Min/Max)** | 3.94s / 5.70s | 0.00s / 0.00s | - |
| **总预估消耗费用 (Total Cost)** | **$0.00011** | **$0.00000** | 🔵 Gemini API (更低价格) |

## 📝 Trial-by-Trial Raw Results
### GCP Vertex AI (sa_vertex_ai)
| Trial # | Status | Latency | Cost | Error details (if any) |
| :---: | :---: | :--- | :--- | :--- |
| 1 | 🟢 OK | 4.163s | $0.00002 | - |
| 2 | 🟢 OK | 5.696s | $0.00002 | - |
| 3 | 🟢 OK | 5.585s | $0.00002 | - |
| 4 | 🟢 OK | 3.939s | $0.00002 | - |
| 5 | 🟢 OK | 4.389s | $0.00002 | - |

### Gemini API (gemini_api)
| Trial # | Status | Latency | Cost | Error details (if any) |
| :---: | :---: | :--- | :--- | :--- |
| 1 | 🔴 FAIL | 0.000s | $0.00000 | Error code: 400 - {'error': {'message': 'This API is not available in your current location. See https://ai.google.dev/gemini-api/docs/available-regions.', 'code': 'invalid_request'}} |
| 2 | 🔴 FAIL | 0.000s | $0.00000 | Error code: 400 - {'error': {'message': 'This API is not available in your current location. See https://ai.google.dev/gemini-api/docs/available-regions.', 'code': 'invalid_request'}} |
| 3 | 🔴 FAIL | 0.000s | $0.00000 | Error code: 400 - {'error': {'message': 'This API is not available in your current location. See https://ai.google.dev/gemini-api/docs/available-regions.', 'code': 'invalid_request'}} |
| 4 | 🔴 FAIL | 0.000s | $0.00000 | Error code: 400 - {'error': {'message': 'This API is not available in your current location. See https://ai.google.dev/gemini-api/docs/available-regions.', 'code': 'invalid_request'}} |
| 5 | 🔴 FAIL | 0.000s | $0.00000 | Error code: 400 - {'error': {'message': 'This API is not available in your current location. See https://ai.google.dev/gemini-api/docs/available-regions.', 'code': 'invalid_request'}} |
