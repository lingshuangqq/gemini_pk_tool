# 🏁 Channel PK Duel Report (Strategy Module)
**Session Timestamp**: `20260731_101518`
**Target Project**: `sigma-axis-504006-f0`
**Target Model Tested**: `gemini-3.5-flash-lite`
**Traffic Stress Profile (压测用例)**: `标准巡检 (3.5 Flash-Lite Standard)`

## 📊 Summary Performance Comparison
| Metrics 比较维度 | 🟢 GCP Vertex AI (SA JSON) | 🔵 Gemini API (API Key) | 🏆 Winner 优胜者 |
| :--- | :--- | :--- | :--- |
| **总测试样本 (Total Trials)** | 5 次 | 5 次 | 双方等量 |
| **成功调用次数 (Success)** | 5 次 | 0 次 | GCP Vertex AI |
| **测试成功率 (Success Rate)** | **100.0%** | **0.0%** | 🟢 GCP Vertex AI |
| **平均端到端延迟 (Avg Latency)** | **1.076 秒** | **0.000 秒** | 暂无成功数据 |
| **最小/最大延迟 (Min/Max)** | 0.90s / 1.45s | 0.00s / 0.00s | - |
| **总预估消耗费用 (Total Cost)** | **$0.00005** | **$0.00000** | 🔵 Gemini API (更低价格) |

## 📝 Trial-by-Trial Raw Results
### GCP Vertex AI (sa_vertex_ai)
| Trial # | Status | Latency | Cost | Error details (if any) |
| :---: | :---: | :--- | :--- | :--- |
| 1 | 🟢 OK | 1.446s | $0.00001 | - |
| 2 | 🟢 OK | 1.059s | $0.00001 | - |
| 3 | 🟢 OK | 0.955s | $0.00001 | - |
| 4 | 🟢 OK | 1.019s | $0.00001 | - |
| 5 | 🟢 OK | 0.899s | $0.00001 | - |

### Gemini API (gemini_api)
| Trial # | Status | Latency | Cost | Error details (if any) |
| :---: | :---: | :--- | :--- | :--- |
| 1 | 🔴 FAIL | 0.000s | $0.00000 | 429 RESOURCE_EXHAUSTED. {'error': {'code': 429, 'message': 'Your billing account has exceeded its monthly spending cap. Please go to AI Studio at https://ai.studio/billing to manage your billing. Learn more at https://ai.google.dev/gemini-api/docs/billing#tier-spend-caps. ', 'status': 'RESOURCE_EXHAUSTED'}} |
| 2 | 🔴 FAIL | 0.000s | $0.00000 | 429 RESOURCE_EXHAUSTED. {'error': {'code': 429, 'message': 'Your billing account has exceeded its monthly spending cap. Please go to AI Studio at https://ai.studio/billing to manage your billing. Learn more at https://ai.google.dev/gemini-api/docs/billing#tier-spend-caps. ', 'status': 'RESOURCE_EXHAUSTED'}} |
| 3 | 🔴 FAIL | 0.000s | $0.00000 | 429 RESOURCE_EXHAUSTED. {'error': {'code': 429, 'message': 'Your billing account has exceeded its monthly spending cap. Please go to AI Studio at https://ai.studio/billing to manage your billing. Learn more at https://ai.google.dev/gemini-api/docs/billing#tier-spend-caps. ', 'status': 'RESOURCE_EXHAUSTED'}} |
| 4 | 🔴 FAIL | 0.000s | $0.00000 | 429 RESOURCE_EXHAUSTED. {'error': {'code': 429, 'message': 'Your billing account has exceeded its monthly spending cap. Please go to AI Studio at https://ai.studio/billing to manage your billing. Learn more at https://ai.google.dev/gemini-api/docs/billing#tier-spend-caps. ', 'status': 'RESOURCE_EXHAUSTED'}} |
| 5 | 🔴 FAIL | 0.000s | $0.00000 | 429 RESOURCE_EXHAUSTED. {'error': {'code': 429, 'message': 'Your billing account has exceeded its monthly spending cap. Please go to AI Studio at https://ai.studio/billing to manage your billing. Learn more at https://ai.google.dev/gemini-api/docs/billing#tier-spend-caps. ', 'status': 'RESOURCE_EXHAUSTED'}} |
