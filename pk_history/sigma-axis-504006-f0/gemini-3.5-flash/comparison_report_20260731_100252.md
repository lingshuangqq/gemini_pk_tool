# 🏁 Channel PK Duel Report (Strategy Module)
**Session Timestamp**: `20260731_100252`
**Target Project**: `sigma-axis-504006-f0`
**Target Model Tested**: `gemini-3.5-flash`
**Traffic Stress Profile (压测用例)**: `standard`

## 📊 Summary Performance Comparison
| Metrics 比较维度 | 🟢 GCP Vertex AI (SA JSON) | 🔵 Gemini API (API Key) | 🏆 Winner 优胜者 |
| :--- | :--- | :--- | :--- |
| **总测试样本 (Total Trials)** | 5 次 | 5 次 | 双方等量 |
| **成功调用次数 (Success)** | 5 次 | 1 次 | GCP Vertex AI |
| **测试成功率 (Success Rate)** | **100.0%** | **20.0%** | 🟢 GCP Vertex AI |
| **平均端到端延迟 (Avg Latency)** | **3.027 秒** | **2.270 秒** | 🔵 Gemini API (更低延迟) |
| **最小/最大延迟 (Min/Max)** | 2.56s / 3.45s | 2.27s / 2.27s | - |
| **总预估消耗费用 (Total Cost)** | **$0.00002** | **$0.00001** | 🔵 Gemini API (更低价格) |

## 📝 Trial-by-Trial Raw Results
### GCP Vertex AI (sa_vertex_ai)
| Trial # | Status | Latency | Cost | Error details (if any) |
| :---: | :---: | :--- | :--- | :--- |
| 1 | 🟢 OK | 3.449s | $0.00000 | - |
| 2 | 🟢 OK | 3.066s | $0.00000 | - |
| 3 | 🟢 OK | 3.215s | $0.00000 | - |
| 4 | 🟢 OK | 2.847s | $0.00000 | - |
| 5 | 🟢 OK | 2.555s | $0.00000 | - |

### Gemini API (gemini_api)
| Trial # | Status | Latency | Cost | Error details (if any) |
| :---: | :---: | :--- | :--- | :--- |
| 1 | 🔵 OK | 2.270s | $0.00001 | - |
| 2 | 🔴 FAIL | 0.000s | $0.00000 | 429 RESOURCE_EXHAUSTED. {'error': {'code': 429, 'message': 'Your billing account has exceeded its monthly spending cap. Please go to AI Studio at https://ai.studio/billing to manage your billing. Learn more at https://ai.google.dev/gemini-api/docs/billing#tier-spend-caps. ', 'status': 'RESOURCE_EXHAUSTED'}} |
| 3 | 🔴 FAIL | 0.000s | $0.00000 | 429 RESOURCE_EXHAUSTED. {'error': {'code': 429, 'message': 'Your billing account has exceeded its monthly spending cap. Please go to AI Studio at https://ai.studio/billing to manage your billing. Learn more at https://ai.google.dev/gemini-api/docs/billing#tier-spend-caps. ', 'status': 'RESOURCE_EXHAUSTED'}} |
| 4 | 🔴 FAIL | 0.000s | $0.00000 | 429 RESOURCE_EXHAUSTED. {'error': {'code': 429, 'message': 'Your billing account has exceeded its monthly spending cap. Please go to AI Studio at https://ai.studio/billing to manage your billing. Learn more at https://ai.google.dev/gemini-api/docs/billing#tier-spend-caps. ', 'status': 'RESOURCE_EXHAUSTED'}} |
| 5 | 🔴 FAIL | 0.000s | $0.00000 | 429 RESOURCE_EXHAUSTED. {'error': {'code': 429, 'message': 'Your billing account has exceeded its monthly spending cap. Please go to AI Studio at https://ai.studio/billing to manage your billing. Learn more at https://ai.google.dev/gemini-api/docs/billing#tier-spend-caps. ', 'status': 'RESOURCE_EXHAUSTED'}} |
