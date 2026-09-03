# 🏁 Channel PK Multi-Dimensional Benchmark Report
**Session Timestamp**: `20260903_105116`
**Target Project**: `spark-ccc`
**Target Model Tested**: `gemini-3.8-flash`
**Traffic Stress Profile**: `标准巡检 (3.8 Flash Standard)`

## 📊 Summary Performance Matrix (多维度测试矩阵)

| Metrics 评估维度 | 🟢 GCP Vertex AI (SA JSON) | 🔵 Gemini API (API Key) | 🏆 Winner 优胜者 |
| :--- | :--- | :--- | :--- |
| **测试样本总数 (Total Trials)** | 5 次 | 5 次 | 双方等量 |
| **成功率 (Success Rate)** | **80.0%** | **0.0%** | 🟢 GCP Vertex AI |
| **首 Token 延迟 (TTFT)** | **3.183 秒** | **0.000 秒** | 暂无数据 |
| **解码吞吐速率 (Output TPS)** | **15.9 Tokens/s** | **0.0 Tokens/s** | 🟢 GCP Vertex AI |
| **平均端到端延迟 (Avg Latency)** | **3.508 秒** | **0.000 秒** | 暂无数据 |
| **延迟波动标准差 (Latency StdDev)** | 0.551s | 0.000s | - |
| **结构化格式符合率 (Format Pass%)** | **75.0%** | **0.0%** | - |
| **每美元 Token 产出 (Tokens / $1)** | **2862903 Tokens** | **0 Tokens** | 🟢 GCP Vertex AI |
| **总预估消耗费用 (Total Cost)** | **$0.00007** | **$0.00000** | 🔵 Gemini API |

## 🛡️ Error Categorization Taxonomy (错误归因统计)
- **GCP Vertex AI**: `{'500_SERVER_INTERNAL': 1}`
- **Gemini API**: `{'400_LOCATION_UNSUPPORTED': 5}`

## 📝 Trial-by-Trial Raw Results
### GCP Vertex AI (sa_vertex_ai)
| Trial # | Status | Latency | TTFT | TPS | Cost | Error details (if any) |
| :---: | :---: | :--- | :--- | :--- | :--- | :--- |
| 1 | 🟢 OK | 4.034s | 3.429s | 17.1/s | $0.00002 | - |
| 2 | 🟢 OK | 3.493s | 3.226s | 15.7/s | $0.00002 | - |
| 3 | 🟢 OK | 2.750s | 2.374s | 26.2/s | $0.00002 | - |
| 4 | 🔴 FAIL | 0.000s | 0.000s | 0.0/s | $0.00000 | 500 INTERNAL. {'error': {'code': 500, 'message': 'Internal error encountered.', 'status': 'INTERNAL'}} |
| 5 | 🟢 OK | 3.755s | 3.702s | 4.5/s | $0.00001 | - |

### Gemini API (gemini_api)
| Trial # | Status | Latency | TTFT | TPS | Cost | Error details (if any) |
| :---: | :---: | :--- | :--- | :--- | :--- | :--- |
| 1 | 🔴 FAIL | 0.000s | 0.000s | 0.0/s | $0.00000 | 400 FAILED_PRECONDITION. {'error': {'code': 400, 'message': 'User location is not supported for the API use.', 'status': 'FAILED_PRECONDITION'}} |
| 2 | 🔴 FAIL | 0.000s | 0.000s | 0.0/s | $0.00000 | 400 FAILED_PRECONDITION. {'error': {'code': 400, 'message': 'User location is not supported for the API use.', 'status': 'FAILED_PRECONDITION'}} |
| 3 | 🔴 FAIL | 0.000s | 0.000s | 0.0/s | $0.00000 | 400 FAILED_PRECONDITION. {'error': {'code': 400, 'message': 'User location is not supported for the API use.', 'status': 'FAILED_PRECONDITION'}} |
| 4 | 🔴 FAIL | 0.000s | 0.000s | 0.0/s | $0.00000 | 400 FAILED_PRECONDITION. {'error': {'code': 400, 'message': 'User location is not supported for the API use.', 'status': 'FAILED_PRECONDITION'}} |
| 5 | 🔴 FAIL | 0.000s | 0.000s | 0.0/s | $0.00000 | 400 FAILED_PRECONDITION. {'error': {'code': 400, 'message': 'User location is not supported for the API use.', 'status': 'FAILED_PRECONDITION'}} |
