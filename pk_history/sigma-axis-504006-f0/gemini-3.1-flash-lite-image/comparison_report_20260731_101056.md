# 🏁 Channel PK Duel Report (Strategy Module)
**Session Timestamp**: `20260731_101056`
**Target Project**: `sigma-axis-504006-f0`
**Target Model Tested**: `gemini-3.1-flash-lite-image`
**Traffic Stress Profile (压测用例)**: `standard`

## 📊 Summary Performance Comparison
| Metrics 比较维度 | 🟢 GCP Vertex AI (SA JSON) | 🔵 Gemini API (API Key) | 🏆 Winner 优胜者 |
| :--- | :--- | :--- | :--- |
| **总测试样本 (Total Trials)** | 3 次 | 3 次 | 双方等量 |
| **成功调用次数 (Success)** | 2 次 | 0 次 | GCP Vertex AI |
| **测试成功率 (Success Rate)** | **66.7%** | **0.0%** | 🟢 GCP Vertex AI |
| **平均端到端延迟 (Avg Latency)** | **5.964 秒** | **0.000 秒** | 暂无成功数据 |
| **最小/最大延迟 (Min/Max)** | 5.04s / 6.89s | 0.00s / 0.00s | - |
| **总预估消耗费用 (Total Cost)** | **$0.19360** | **$0.00000** | 🔵 Gemini API (更低价格) |

## 📝 Trial-by-Trial Raw Results
### GCP Vertex AI (sa_vertex_ai)
| Trial # | Status | Latency | Cost | Error details (if any) |
| :---: | :---: | :--- | :--- | :--- |
| 1 | 🟢 OK | 5.040s | $0.09680 | - |
| 2 | 🟢 OK | 6.887s | $0.09680 | - |
| 3 | 🔴 FAIL | 0.000s | $0.00000 | 429 RESOURCE_EXHAUSTED. {'error': {'code': 429, 'message': 'Resource has been exhausted (e.g. check quota).', 'status': 'RESOURCE_EXHAUSTED'}} |

### Gemini API (gemini_api)
| Trial # | Status | Latency | Cost | Error details (if any) |
| :---: | :---: | :--- | :--- | :--- |
| 1 | 🔴 FAIL | 0.000s | $0.00000 | 429 RESOURCE_EXHAUSTED. {'error': {'code': 429, 'message': 'Your billing account has exceeded its monthly spending cap. Please go to AI Studio at https://ai.studio/billing to manage your billing. Learn more at https://ai.google.dev/gemini-api/docs/billing#tier-spend-caps. ', 'status': 'RESOURCE_EXHAUSTED'}} |
| 2 | 🔴 FAIL | 0.000s | $0.00000 | 429 RESOURCE_EXHAUSTED. {'error': {'code': 429, 'message': 'Your billing account has exceeded its monthly spending cap. Please go to AI Studio at https://ai.studio/billing to manage your billing. Learn more at https://ai.google.dev/gemini-api/docs/billing#tier-spend-caps. ', 'status': 'RESOURCE_EXHAUSTED'}} |
| 3 | 🔴 FAIL | 0.000s | $0.00000 | 429 RESOURCE_EXHAUSTED. {'error': {'code': 429, 'message': 'Your billing account has exceeded its monthly spending cap. Please go to AI Studio at https://ai.studio/billing to manage your billing. Learn more at https://ai.google.dev/gemini-api/docs/billing#tier-spend-caps. ', 'status': 'RESOURCE_EXHAUSTED'}} |
