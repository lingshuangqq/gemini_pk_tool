# 🏁 Channel PK Duel Report (Strategy Module)
**Session Timestamp**: `20260903_102138`
**Target Project**: `spark-ccc`
**Target Model Tested**: `gemini-3-pro-image`
**Traffic Stress Profile (压测用例)**: `standard`

## 📊 Summary Performance Comparison
| Metrics 比较维度 | 🟢 GCP Vertex AI (SA JSON) | 🔵 Gemini API (API Key) | 🏆 Winner 优胜者 |
| :--- | :--- | :--- | :--- |
| **总测试样本 (Total Trials)** | 2 次 | 2 次 | 双方等量 |
| **成功调用次数 (Success)** | 2 次 | 0 次 | GCP Vertex AI |
| **测试成功率 (Success Rate)** | **100.0%** | **0.0%** | 🟢 GCP Vertex AI |
| **平均端到端延迟 (Avg Latency)** | **61.399 秒** | **0.000 秒** | 暂无成功数据 |
| **最小/最大延迟 (Min/Max)** | 57.91s / 64.89s | 0.00s / 0.00s | - |
| **总预估消耗费用 (Total Cost)** | **$0.19360** | **$0.00000** | 🔵 Gemini API (更低价格) |

## 📝 Trial-by-Trial Raw Results
### GCP Vertex AI (sa_vertex_ai)
| Trial # | Status | Latency | Cost | Error details (if any) |
| :---: | :---: | :--- | :--- | :--- |
| 1 | 🟢 OK | 64.886s | $0.09680 | - |
| 2 | 🟢 OK | 57.913s | $0.09680 | - |

### Gemini API (gemini_api)
| Trial # | Status | Latency | Cost | Error details (if any) |
| :---: | :---: | :--- | :--- | :--- |
| 1 | 🔴 FAIL | 0.000s | $0.00000 | 400 FAILED_PRECONDITION. {'error': {'code': 400, 'message': 'User location is not supported for the API use.', 'status': 'FAILED_PRECONDITION'}} |
| 2 | 🔴 FAIL | 0.000s | $0.00000 | 400 FAILED_PRECONDITION. {'error': {'code': 400, 'message': 'User location is not supported for the API use.', 'status': 'FAILED_PRECONDITION'}} |
