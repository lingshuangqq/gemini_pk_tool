# 🏁 Channel PK Duel Report (Strategy Module)
**Session Timestamp**: `20260803_105225`
**Target Project**: `sigma-axis-504006-f0`
**Target Model Tested**: `gemini-3.5-flash`
**Traffic Stress Profile (压测用例)**: `standard`

## 📊 Summary Performance Comparison
| Metrics 比较维度 | 🟢 GCP Vertex AI (SA JSON) | 🔵 Gemini API (API Key) | 🏆 Winner 优胜者 |
| :--- | :--- | :--- | :--- |
| **总测试样本 (Total Trials)** | 5 次 | 5 次 | 双方等量 |
| **成功调用次数 (Success)** | 5 次 | 5 次 | 双方持平 |
| **测试成功率 (Success Rate)** | **100.0%** | **100.0%** | 双方持平 |
| **平均端到端延迟 (Avg Latency)** | **2.926 秒** | **1.950 秒** | 🔵 Gemini API (更低延迟) |
| **最小/最大延迟 (Min/Max)** | 2.67s / 3.31s | 1.69s / 2.23s | - |
| **总预估消耗费用 (Total Cost)** | **$0.00002** | **$0.00002** | 🔵 Gemini API (更低价格) |

## 📝 Trial-by-Trial Raw Results
### GCP Vertex AI (sa_vertex_ai)
| Trial # | Status | Latency | Cost | Error details (if any) |
| :---: | :---: | :--- | :--- | :--- |
| 1 | 🟢 OK | 3.231s | $0.00000 | - |
| 2 | 🟢 OK | 2.729s | $0.00000 | - |
| 3 | 🟢 OK | 2.695s | $0.00000 | - |
| 4 | 🟢 OK | 2.667s | $0.00000 | - |
| 5 | 🟢 OK | 3.308s | $0.00000 | - |

### Gemini API (gemini_api)
| Trial # | Status | Latency | Cost | Error details (if any) |
| :---: | :---: | :--- | :--- | :--- |
| 1 | 🔵 OK | 2.230s | $0.00000 | - |
| 2 | 🔵 OK | 1.766s | $0.00001 | - |
| 3 | 🔵 OK | 2.150s | $0.00001 | - |
| 4 | 🔵 OK | 1.692s | $0.00000 | - |
| 5 | 🔵 OK | 1.913s | $0.00001 | - |
