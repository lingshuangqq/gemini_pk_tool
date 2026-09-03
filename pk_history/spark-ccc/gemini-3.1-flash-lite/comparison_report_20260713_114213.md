# 🏁 Channel PK Duel Report (Strategy Module)
**Session Timestamp**: `20260713_114213`
**Target Project**: `spark-ccc`
**Target Model Tested**: `gemini-3.1-flash-lite`
**Traffic Stress Profile (压测用例)**: `standard`

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
| 1 | 🔴 FAIL | 0.000s | $0.00000 | File ../spark-ccc/spark-ccc-4d9d470f717a.json was not found. |
| 2 | 🔴 FAIL | 0.000s | $0.00000 | File ../spark-ccc/spark-ccc-4d9d470f717a.json was not found. |
| 3 | 🔴 FAIL | 0.000s | $0.00000 | File ../spark-ccc/spark-ccc-4d9d470f717a.json was not found. |
| 4 | 🔴 FAIL | 0.000s | $0.00000 | File ../spark-ccc/spark-ccc-4d9d470f717a.json was not found. |
| 5 | 🔴 FAIL | 0.000s | $0.00000 | File ../spark-ccc/spark-ccc-4d9d470f717a.json was not found. |

### Gemini API (gemini_api)
| Trial # | Status | Latency | Cost | Error details (if any) |
| :---: | :---: | :--- | :--- | :--- |
| 1 | 🔴 FAIL | 0.000s | $0.00000 | 403 PERMISSION_DENIED. {'error': {'code': 403, 'message': 'Requests to this API aiplatform.googleapis.com method google.cloud.aiplatform.v1beta1.PredictionService.GenerateContent are blocked.', 'status': 'PERMISSION_DENIED', 'details': [{'@type': 'type.googleapis.com/google.rpc.ErrorInfo', 'reason': 'API_KEY_SERVICE_BLOCKED', 'domain': 'googleapis.com', 'metadata': {'methodName': 'google.cloud.aiplatform.v1beta1.PredictionService.GenerateContent', 'apiName': 'aiplatform.googleapis.com', 'service': 'aiplatform.googleapis.com', 'consumer': 'projects/385887862987'}}, {'@type': 'type.googleapis.com/google.rpc.LocalizedMessage', 'locale': 'en-US', 'message': 'Requests to this API aiplatform.googleapis.com method google.cloud.aiplatform.v1beta1.PredictionService.GenerateContent are blocked.'}]}} |
| 2 | 🔴 FAIL | 0.000s | $0.00000 | 403 PERMISSION_DENIED. {'error': {'code': 403, 'message': 'Requests to this API aiplatform.googleapis.com method google.cloud.aiplatform.v1beta1.PredictionService.GenerateContent are blocked.', 'status': 'PERMISSION_DENIED', 'details': [{'@type': 'type.googleapis.com/google.rpc.ErrorInfo', 'reason': 'API_KEY_SERVICE_BLOCKED', 'domain': 'googleapis.com', 'metadata': {'methodName': 'google.cloud.aiplatform.v1beta1.PredictionService.GenerateContent', 'service': 'aiplatform.googleapis.com', 'consumer': 'projects/385887862987', 'apiName': 'aiplatform.googleapis.com'}}, {'@type': 'type.googleapis.com/google.rpc.LocalizedMessage', 'locale': 'en-US', 'message': 'Requests to this API aiplatform.googleapis.com method google.cloud.aiplatform.v1beta1.PredictionService.GenerateContent are blocked.'}]}} |
| 3 | 🔴 FAIL | 0.000s | $0.00000 | 403 PERMISSION_DENIED. {'error': {'code': 403, 'message': 'Requests to this API aiplatform.googleapis.com method google.cloud.aiplatform.v1beta1.PredictionService.GenerateContent are blocked.', 'status': 'PERMISSION_DENIED', 'details': [{'@type': 'type.googleapis.com/google.rpc.ErrorInfo', 'reason': 'API_KEY_SERVICE_BLOCKED', 'domain': 'googleapis.com', 'metadata': {'service': 'aiplatform.googleapis.com', 'consumer': 'projects/385887862987', 'methodName': 'google.cloud.aiplatform.v1beta1.PredictionService.GenerateContent', 'apiName': 'aiplatform.googleapis.com'}}, {'@type': 'type.googleapis.com/google.rpc.LocalizedMessage', 'locale': 'en-US', 'message': 'Requests to this API aiplatform.googleapis.com method google.cloud.aiplatform.v1beta1.PredictionService.GenerateContent are blocked.'}]}} |
| 4 | 🔴 FAIL | 0.000s | $0.00000 | 403 PERMISSION_DENIED. {'error': {'code': 403, 'message': 'Requests to this API aiplatform.googleapis.com method google.cloud.aiplatform.v1beta1.PredictionService.GenerateContent are blocked.', 'status': 'PERMISSION_DENIED', 'details': [{'@type': 'type.googleapis.com/google.rpc.ErrorInfo', 'reason': 'API_KEY_SERVICE_BLOCKED', 'domain': 'googleapis.com', 'metadata': {'consumer': 'projects/385887862987', 'service': 'aiplatform.googleapis.com', 'apiName': 'aiplatform.googleapis.com', 'methodName': 'google.cloud.aiplatform.v1beta1.PredictionService.GenerateContent'}}, {'@type': 'type.googleapis.com/google.rpc.LocalizedMessage', 'locale': 'en-US', 'message': 'Requests to this API aiplatform.googleapis.com method google.cloud.aiplatform.v1beta1.PredictionService.GenerateContent are blocked.'}]}} |
| 5 | 🔴 FAIL | 0.000s | $0.00000 | 403 PERMISSION_DENIED. {'error': {'code': 403, 'message': 'Requests to this API aiplatform.googleapis.com method google.cloud.aiplatform.v1beta1.PredictionService.GenerateContent are blocked.', 'status': 'PERMISSION_DENIED', 'details': [{'@type': 'type.googleapis.com/google.rpc.ErrorInfo', 'reason': 'API_KEY_SERVICE_BLOCKED', 'domain': 'googleapis.com', 'metadata': {'methodName': 'google.cloud.aiplatform.v1beta1.PredictionService.GenerateContent', 'apiName': 'aiplatform.googleapis.com', 'service': 'aiplatform.googleapis.com', 'consumer': 'projects/385887862987'}}, {'@type': 'type.googleapis.com/google.rpc.LocalizedMessage', 'locale': 'en-US', 'message': 'Requests to this API aiplatform.googleapis.com method google.cloud.aiplatform.v1beta1.PredictionService.GenerateContent are blocked.'}]}} |
