# 🏁 Channel PK Duel Report (Strategy Module)
**Session Timestamp**: `20260803_105644`
**Target Project**: `sigma-axis-504006-f0`
**Target Model Tested**: `gemini-omni-flash-preview`
**Traffic Stress Profile (压测用例)**: `标准巡检 (Omni Flash Standard)`

## 📊 Summary Performance Comparison
| Metrics 比较维度 | 🟢 GCP Vertex AI (SA JSON) | 🔵 Gemini API (API Key) | 🏆 Winner 优胜者 |
| :--- | :--- | :--- | :--- |
| **总测试样本 (Total Trials)** | 5 次 | 5 次 | 双方等量 |
| **成功调用次数 (Success)** | 0 次 | 0 次 | 双方持平 |
| **测试成功率 (Success Rate)** | **0.0%** | **0.0%** | 双方持平 |
| **平均端到端延迟 (Avg Latency)** | **0.000 秒** | **0.000 秒** | 暂无成功数据 |
| **最小/最大延迟 (Min/Max)** | 0.00s / 0.00s | 0.00s / 0.00s | - |
| **总预估消耗费用 (Total Cost)** | **$0.00000** | **$0.00000** | 🟢 GCP Vertex AI (更低价格) |

## 📝 Trial-by-Trial Raw Results
### GCP Vertex AI (sa_vertex_ai)
| Trial # | Status | Latency | Cost | Error details (if any) |
| :---: | :---: | :--- | :--- | :--- |
| 1 | 🔴 FAIL | 0.000s | $0.00000 | 400 INVALID_ARGUMENT. {'error': {'code': 400, 'message': 'gemini-omni-flash-preview is only supported in the Interactions API and cannot be called directly via generateContent.', 'status': 'INVALID_ARGUMENT'}} |
| 2 | 🔴 FAIL | 0.000s | $0.00000 | 400 INVALID_ARGUMENT. {'error': {'code': 400, 'message': 'gemini-omni-flash-preview is only supported in the Interactions API and cannot be called directly via generateContent.', 'status': 'INVALID_ARGUMENT'}} |
| 3 | 🔴 FAIL | 0.000s | $0.00000 | 400 INVALID_ARGUMENT. {'error': {'code': 400, 'message': 'gemini-omni-flash-preview is only supported in the Interactions API and cannot be called directly via generateContent.', 'status': 'INVALID_ARGUMENT'}} |
| 4 | 🔴 FAIL | 0.000s | $0.00000 | 400 INVALID_ARGUMENT. {'error': {'code': 400, 'message': 'gemini-omni-flash-preview is only supported in the Interactions API and cannot be called directly via generateContent.', 'status': 'INVALID_ARGUMENT'}} |
| 5 | 🔴 FAIL | 0.000s | $0.00000 | 400 INVALID_ARGUMENT. {'error': {'code': 400, 'message': 'gemini-omni-flash-preview is only supported in the Interactions API and cannot be called directly via generateContent.', 'status': 'INVALID_ARGUMENT'}} |

### Gemini API (gemini_api)
| Trial # | Status | Latency | Cost | Error details (if any) |
| :---: | :---: | :--- | :--- | :--- |
| 1 | 🔴 FAIL | 0.000s | $0.00000 | 400 INVALID_ARGUMENT. {'error': {'code': 400, 'message': 'This model only supports Interactions API.', 'status': 'INVALID_ARGUMENT'}} |
| 2 | 🔴 FAIL | 0.000s | $0.00000 | 400 INVALID_ARGUMENT. {'error': {'code': 400, 'message': 'This model only supports Interactions API.', 'status': 'INVALID_ARGUMENT'}} |
| 3 | 🔴 FAIL | 0.000s | $0.00000 | 400 INVALID_ARGUMENT. {'error': {'code': 400, 'message': 'This model only supports Interactions API.', 'status': 'INVALID_ARGUMENT'}} |
| 4 | 🔴 FAIL | 0.000s | $0.00000 | 400 INVALID_ARGUMENT. {'error': {'code': 400, 'message': 'This model only supports Interactions API.', 'status': 'INVALID_ARGUMENT'}} |
| 5 | 🔴 FAIL | 0.000s | $0.00000 | 400 INVALID_ARGUMENT. {'error': {'code': 400, 'message': 'This model only supports Interactions API.', 'status': 'INVALID_ARGUMENT'}} |
