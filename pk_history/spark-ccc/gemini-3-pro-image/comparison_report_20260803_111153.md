# 🏁 Channel PK Duel Report (Strategy Module)
**Session Timestamp**: `20260803_111153`
**Target Project**: `spark-ccc`
**Target Model Tested**: `gemini-3-pro-image`
**Traffic Stress Profile (压测用例)**: `标准画质巡检 (Pro Image Standard)`

## 📊 Summary Performance Comparison
| Metrics 比较维度 | 🟢 GCP Vertex AI (SA JSON) | 🔵 Gemini API (API Key) | 🏆 Winner 优胜者 |
| :--- | :--- | :--- | :--- |
| **总测试样本 (Total Trials)** | 2 次 | 2 次 | 双方等量 |
| **成功调用次数 (Success)** | 0 次 | 2 次 | Gemini API |
| **测试成功率 (Success Rate)** | **0.0%** | **100.0%** | 双方持平 |
| **平均端到端延迟 (Avg Latency)** | **0.000 秒** | **43.890 秒** | 暂无成功数据 |
| **最小/最大延迟 (Min/Max)** | 0.00s / 0.00s | 40.51s / 47.27s | - |
| **总预估消耗费用 (Total Cost)** | **$0.00000** | **$0.48000** | 🟢 GCP Vertex AI (更低价格) |

## 📝 Trial-by-Trial Raw Results
### GCP Vertex AI (sa_vertex_ai)
| Trial # | Status | Latency | Cost | Error details (if any) |
| :---: | :---: | :--- | :--- | :--- |
| 1 | 🔴 FAIL | 0.000s | $0.00000 | 429 RESOURCE_EXHAUSTED. {'error': {'code': 429, 'message': 'Resource has been exhausted (e.g. check quota).', 'status': 'RESOURCE_EXHAUSTED'}} |
| 2 | 🔴 FAIL | 0.000s | $0.00000 | 429 RESOURCE_EXHAUSTED. {'error': {'code': 429, 'message': 'Resource has been exhausted (e.g. check quota).', 'status': 'RESOURCE_EXHAUSTED'}} |

### Gemini API (gemini_api)
| Trial # | Status | Latency | Cost | Error details (if any) |
| :---: | :---: | :--- | :--- | :--- |
| 1 | 🔵 OK | 47.273s | $0.24000 | - |
| 2 | 🔵 OK | 40.507s | $0.24000 | - |
