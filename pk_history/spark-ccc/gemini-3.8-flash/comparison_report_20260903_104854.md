# 🏁 Channel PK Multi-Dimensional Benchmark Report
**Session Timestamp**: `20260903_104854`
**Target Project**: `spark-ccc`
**Target Model Tested**: `gemini-3.8-flash`
**Traffic Stress Profile**: `标准巡检 (3.8 Flash Standard)`

## 📊 Summary Performance Matrix (多维度测试矩阵)

| Metrics 评估维度 | 🟢 GCP Vertex AI (SA JSON) | 🔵 Gemini API (API Key) | 🏆 Winner 优胜者 |
| :--- | :--- | :--- | :--- |
| **测试样本总数 (Total Trials)** | 5 次 | 5 次 | 双方等量 |
| **成功率 (Success Rate)** | **100.0%** | **0.0%** | 🟢 GCP Vertex AI |
| **首 Token 延迟 (TTFT)** | **2.553 秒** | **0.000 秒** | 暂无数据 |
| **解码吞吐速率 (Output TPS)** | **2.9 Tokens/s** | **0.0 Tokens/s** | 🟢 GCP Vertex AI |
| **平均端到端延迟 (Avg Latency)** | **2.644 秒** | **0.000 秒** | 暂无数据 |
| **延迟波动标准差 (Latency StdDev)** | 0.404s | 0.000s | - |
| **结构化格式符合率 (Format Pass%)** | **0.0%** | **0.0%** | - |
| **每美元 Token 产出 (Tokens / $1)** | **1549439 Tokens** | **0 Tokens** | 🟢 GCP Vertex AI |
| **总预估消耗费用 (Total Cost)** | **$0.00002** | **$0.00000** | 🔵 Gemini API |

## 🛡️ Error Categorization Taxonomy (错误归因统计)
- **GCP Vertex AI**: `Clean (无错误)`
- **Gemini API**: `{'400_LOCATION_UNSUPPORTED': 5}`

## 📝 Trial-by-Trial Raw Results
### GCP Vertex AI (sa_vertex_ai)
| Trial # | Status | Latency | TTFT | TPS | Cost | Error details (if any) |
| :---: | :---: | :--- | :--- | :--- | :--- | :--- |
| 1 | 🟢 OK | 3.259s | 2.929s | 2.8/s | $0.00001 | - |
| 2 | 🟢 OK | 2.645s | 2.598s | 3.4/s | $0.00001 | - |
| 3 | 🟢 OK | 2.124s | 2.054s | 2.8/s | $0.00000 | - |
| 4 | 🟢 OK | 2.582s | 2.581s | 3.5/s | $0.00001 | - |
| 5 | 🟢 OK | 2.610s | 2.605s | 1.9/s | $0.00000 | - |

### Gemini API (gemini_api)
| Trial # | Status | Latency | TTFT | TPS | Cost | Error details (if any) |
| :---: | :---: | :--- | :--- | :--- | :--- | :--- |
| 1 | 🔴 FAIL | 0.000s | 0.000s | 0.0/s | $0.00000 | 400 FAILED_PRECONDITION. {'error': {'code': 400, 'message': 'User location is not supported for the API use.', 'status': 'FAILED_PRECONDITION'}} |
| 2 | 🔴 FAIL | 0.000s | 0.000s | 0.0/s | $0.00000 | 400 FAILED_PRECONDITION. {'error': {'code': 400, 'message': 'User location is not supported for the API use.', 'status': 'FAILED_PRECONDITION'}} |
| 3 | 🔴 FAIL | 0.000s | 0.000s | 0.0/s | $0.00000 | 400 FAILED_PRECONDITION. {'error': {'code': 400, 'message': 'User location is not supported for the API use.', 'status': 'FAILED_PRECONDITION'}} |
| 4 | 🔴 FAIL | 0.000s | 0.000s | 0.0/s | $0.00000 | 400 FAILED_PRECONDITION. {'error': {'code': 400, 'message': 'User location is not supported for the API use.', 'status': 'FAILED_PRECONDITION'}} |
| 5 | 🔴 FAIL | 0.000s | 0.000s | 0.0/s | $0.00000 | 400 FAILED_PRECONDITION. {'error': {'code': 400, 'message': 'User location is not supported for the API use.', 'status': 'FAILED_PRECONDITION'}} |
