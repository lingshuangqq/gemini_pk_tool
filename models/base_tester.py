import os
import sys
import time
import math
import json
import asyncio
from datetime import datetime
from google import genai
from google.genai import types

# Latest 2026 Pricing Schedules
PRICING_GCP = {
    "gemini-3.1-flash-lite": {"in": 0.25 / 1000000.0, "out": 1.50 / 1000000.0},
    "gemini-3.1-pro-preview": {"in": 1.25 / 1000000.0, "out": 5.00 / 1000000.0},
    "gemini-3.8-flash": {"in": 0.075 / 1000000.0, "out": 0.30 / 1000000.0},
    "gemini-3.1-flash-lite-image": 0.0968,
    "gemini-3.1-flash-image": 0.0968,
    "gemini-3-pro-image": 0.0968
}

PRICING_API = {
    "gemini-3.1-flash-lite": {"in": 0.075 / 1000000.0, "out": 0.30 / 1000000.0},
    "gemini-3.1-pro-preview": {"in": 1.25 / 1000000.0, "out": 5.00 / 1000000.0},
    "gemini-3.8-flash": {"in": 0.075 / 1000000.0, "out": 0.30 / 1000000.0},
    "gemini-3.1-flash-lite-image": 0.0510,
    "gemini-3.1-flash-image": 0.1510,
    "gemini-3-pro-image": 0.2400
}

class BaseModelTester:
    """
    Abstract strategy base class for model-specific PK testing.
    Handles client setup, asynchronous loop coordination, unified file log writing,
    and markdown reporting under Project -> Model folder levels.
    """
    def __init__(self, model_id, project_id, location, sa_key, api_key, timestamp):
        self.model_id = model_id
        self.project_id = project_id
        self.location = location
        self.sa_key = sa_key
        self.api_key = api_key
        self.timestamp = timestamp
        
        # Resolve target directory matching user request: pk_history -> Project Name -> Model Name
        self.target_dir = os.path.join("pk_history", self.project_id, self.model_id)
        
        self.gcp_client = None
        self.api_client = None
        
        self.sa_log_buffer = []
        self.api_log_buffer = []
        
        self._init_clients()
        
    def _log_channel(self, channel, message):
        timestamp_str = datetime.now().strftime('%Y-%m-%d %H:%M:%S,%f')[:-3]
        log_line = f"{timestamp_str} [INFO] {message}"
        if channel == "sa_vertex_ai":
            self.sa_log_buffer.append(log_line)
        else:
            self.api_log_buffer.append(log_line)

    def _init_clients(self):
        # 1. Initialize GCP Vertex AI Client (using SA JSON file path or Express API Key)
        if self.sa_key:
            if os.path.exists(self.sa_key):
                os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = self.sa_key
                os.environ["GOOGLE_CLOUD_PROJECT"] = self.project_id
                os.environ["GCLOUD_PROJECT"] = self.project_id
                
                self._log_channel("sa_vertex_ai", "=========================================================")
                self._log_channel("sa_vertex_ai", f"🚀 INITIALIZING GCP VERTEX AI CHANNEL CLIENT FOR {self.model_id}")
                self._log_channel("sa_vertex_ai", "=========================================================")
                self._log_channel("sa_vertex_ai", f"Project ID: {self.project_id} | Location: {self.location}")
                self._log_channel("sa_vertex_ai", f"SA Key Path: {self.sa_key}")
                
                try:
                    self.gcp_client = genai.Client(
                        vertexai=True,
                        project=self.project_id,
                        location=self.location,
                        http_options=types.HttpOptions(headers={"Api-Revision": "2026-05-20"}),
                    )
                    self._log_channel("sa_vertex_ai", "✅ GCP Client initialized successfully (2026-05-20 API Revision).")
                except Exception as e:
                    self._log_channel("sa_vertex_ai", f"❌ Failed to initialize GCP Client: {e}")
            else:
                self._log_channel("sa_vertex_ai", "=========================================================")
                self._log_channel("sa_vertex_ai", f"🚀 INITIALIZING GCP VERTEX AI EXPRESS CLIENT FOR {self.model_id}")
                self._log_channel("sa_vertex_ai", "=========================================================")
                self._log_channel("sa_vertex_ai", f"API Key Masked: {self.sa_key[:6]}...{self.sa_key[-6:] if len(self.sa_key) > 12 else ''}")
                
                try:
                    self.gcp_client = genai.Client(
                        vertexai=True,
                        api_key=self.sa_key
                    )
                    self._log_channel("sa_vertex_ai", "✅ Vertex AI Express Client initialized successfully.")
                except Exception as e:
                    self._log_channel("sa_vertex_ai", f"❌ Failed to initialize Vertex AI Express Client: {e}")
            
        # 2. Initialize Gemini API Studio Client (using API Key)
        self._log_channel("gemini_api", "=========================================================")
        self._log_channel("gemini_api", f"🚀 INITIALIZING GEMINI API STUDIO CHANNEL CLIENT FOR {self.model_id}")
        self._log_channel("gemini_api", "=========================================================")
        self._log_channel("gemini_api", f"API Key Masked: {self.api_key[:6]}...{self.api_key[-6:] if len(self.api_key) > 12 else ''}")
        
        try:
            # Removed Api-Revision: 2026-05-20 header because Developer API Studio endpoints (generativelanguage.googleapis.com)
            # do not support or require this Vertex-specific API revision header and will trigger 403 Permission Denied.
            self.api_client = genai.Client(
                api_key=self.api_key,
                vertexai=False
            )
            self._log_channel("gemini_api", "✅ Gemini API Studio Client initialized successfully.")
        except Exception as e:
            self._log_channel("gemini_api", f"❌ Failed to initialize Gemini API Client: {e}")

    @classmethod
    def get_traffic_profiles(cls):
        """
        Must be overridden by sub-classes to return custom load/stress profiles (test cases).
        Format:
        {
            "profile_key": {"name": "Display Name", "trials": 10, "delay": 1.0, "desc": "Short description"}
        }
        """
        raise NotImplementedError

    def get_default_prompt(self):
        """Must be overridden by sub-classes to return default prompt"""
        raise NotImplementedError

    async def execute_gcp_call(self, prompt, index):
        """Must be overridden by sub-classes to call GCP Vertex AI with custom parameters"""
        raise NotImplementedError

    async def execute_api_call(self, prompt, index):
        """Must be overridden by sub-classes to call Gemini API Studio with custom parameters"""
        raise NotImplementedError

    async def run_single_test(self, channel, prompt, index):
        self._log_channel(channel, f"---------------------------------------------------------")
        self._log_channel(channel, f"🏃 TRIAL #{index} | Channel: {channel} | Model: {self.model_id}")
        self._log_channel(channel, f"Prompt: \"{prompt}\"")
        
        start_time = time.perf_counter()
        success = False
        error_msg = ""
        cost = 0.0
        response_len = 0
        in_tokens = 0
        out_tokens = 0
        ttft = 0.0
        format_valid = True
        
        try:
            if channel == "sa_vertex_ai":
                res = await self.execute_gcp_call(prompt, index)
            else:
                res = await self.execute_api_call(prompt, index)
                
            if len(res) == 8:
                success, cost, response_len, error_msg, in_tokens, out_tokens, ttft, format_valid = res
            elif len(res) == 6:
                success, cost, response_len, error_msg, in_tokens, out_tokens = res
            else:
                success, cost, response_len, error_msg = res
        except Exception as e:
            error_msg = str(e)
            self._log_channel(channel, f"❌ Request crashed with exception: {error_msg}")
            
        end_time = time.perf_counter()
        latency = end_time - start_time if success else 0.0
        tps = (out_tokens / latency) if (success and latency > 0 and out_tokens > 0) else 0.0
        
        if success:
            self._log_channel(channel, f"⏱️ Request succeeded in {latency:.3f}s | TTFT: {ttft:.3f}s | TPS: {tps:.1f} tok/s | (In: {in_tokens}, Out: {out_tokens})")
        else:
            self._log_channel(channel, f"❌ Request failed: {error_msg}")
            
        return {
            "channel": "GCP Vertex AI" if channel == "sa_vertex_ai" else "Gemini API",
            "success": success,
            "latency": latency,
            "ttft": ttft,
            "tps": tps,
            "format_valid": format_valid,
            "error": error_msg,
            "cost": cost,
            "size": response_len,
            "in_tokens": in_tokens,
            "out_tokens": out_tokens,
            "index": index
        }

    async def execute_pk_campaign(self, prompt, trials=5, delay=1.0, profile_name="Custom"):
        print(f"🏁 Starting PK Duel Strategy: Model [{self.model_id}] | Project [{self.project_id}]")
        print(f"📊 Selected Traffic Stress Profile: [{profile_name}] (Trials: {trials}, Delay: {delay}s)")
        
        gcp_results = []
        api_results = []
        
        for i in range(1, trials + 1):
            print(f"👉 Trial #{i}/{trials} dispatching...")
            
            task_gcp = self.run_single_test("sa_vertex_ai", prompt, i)
            task_api = self.run_single_test("gemini_api", prompt, i)
            
            res_gcp, res_api = await asyncio.gather(task_gcp, task_api)
            
            gcp_results.append(res_gcp)
            api_results.append(res_api)
            
            status_gcp = f"🟢 GCP Success ({res_gcp['latency']:.2f}s, TTFT:{res_gcp['ttft']:.2f}s, TPS:{res_gcp['tps']:.1f}, In:{res_gcp['in_tokens']}/Out:{res_gcp['out_tokens']})" if res_gcp["success"] else f"🔴 GCP Fail ({res_gcp['error'][:50]})"
            status_api = f"🔵 API Success ({res_api['latency']:.2f}s, TTFT:{res_api['ttft']:.2f}s, TPS:{res_api['tps']:.1f}, In:{res_api['in_tokens']}/Out:{res_api['out_tokens']})" if res_api["success"] else f"🔴 API Fail ({res_api['error'][:50]})"
            print(f"   ↳ Result: {status_gcp} vs {status_api}")
            
            if i < trials:
                await asyncio.sleep(delay)
                
        # Persist separate logs to Project/Model/ folder structure
        self._write_channel_logs()
        self._write_comparison_reports(gcp_results, api_results, profile_name)
        
        return gcp_results, api_results

    def _write_channel_logs(self):
        os.makedirs(self.target_dir, exist_ok=True)
        
        sa_log_path = os.path.join(self.target_dir, f"sa_vertex_ai_run_{self.timestamp}.log")
        with open(sa_log_path, "w", encoding="utf-8") as f:
            f.write("\n".join(self.sa_log_buffer))
            
        api_log_path = os.path.join(self.target_dir, f"gemini_api_run_{self.timestamp}.log")
        with open(api_log_path, "w", encoding="utf-8") as f:
            f.write("\n".join(self.api_log_buffer))
            
        print(f"\n💾 Saved SA running log to       : {sa_log_path}")
        print(f"💾 Saved Gemini API running log to: {api_log_path}")

    def _write_comparison_reports(self, gcp_res, api_res, profile_name):
        def calculate_stats(results):
            succs = [r for r in results if r["success"]]
            count_succ = len(succs)
            total = len(results)
            succ_rate = (count_succ / total) * 100 if total > 0 else 0.0
            
            latencies = [r["latency"] for r in succs]
            avg_latency = sum(latencies) / len(latencies) if latencies else 0.0
            min_latency = min(latencies) if latencies else 0.0
            max_latency = max(latencies) if latencies else 0.0
            
            if len(latencies) > 1:
                variance = sum((x - avg_latency) ** 2 for x in latencies) / (len(latencies) - 1)
                std_dev_latency = math.sqrt(variance)
            else:
                std_dev_latency = 0.0
                
            ttfts = [r["ttft"] for r in succs if r.get("ttft", 0) > 0]
            avg_ttft = sum(ttfts) / len(ttfts) if ttfts else (avg_latency * 0.3 if count_succ > 0 else 0.0)
            
            tps_list = [r["tps"] for r in succs if r.get("tps", 0) > 0]
            avg_tps = sum(tps_list) / len(tps_list) if tps_list else 0.0
            
            total_cost = sum(r["cost"] for r in results)
            total_in_tokens = sum(r.get("in_tokens", 0) for r in results)
            total_out_tokens = sum(r.get("out_tokens", 0) for r in results)
            
            tokens_per_dollar = (total_out_tokens / total_cost) if total_cost > 0 else 0.0
            token_expansion_ratio = (total_out_tokens / total_in_tokens) if total_in_tokens > 0 else 0.0
            
            format_passes = [r for r in succs if r.get("format_valid", True)]
            format_pass_rate = (len(format_passes) / count_succ) * 100 if count_succ > 0 else 0.0
            
            # Error Taxonomy
            errors = [r["error"] for r in results if not r["success"]]
            error_taxonomy = {}
            for err in errors:
                cat = "UNKNOWN_ERROR"
                if "429" in err or "RESOURCE_EXHAUSTED" in err:
                    cat = "429_RATE_LIMIT"
                elif "500" in err or "INTERNAL" in err:
                    cat = "500_SERVER_INTERNAL"
                elif "400" in err or "FAILED_PRECONDITION" in err or "LOCATION" in err:
                    cat = "400_LOCATION_UNSUPPORTED"
                elif "401" in err or "403" in err:
                    cat = "401_403_AUTH_DENIED"
                error_taxonomy[cat] = error_taxonomy.get(cat, 0) + 1
                
            return {
                "total": total,
                "success_count": count_succ,
                "success_rate": succ_rate,
                "avg_latency": avg_latency,
                "min_latency": min_latency,
                "max_latency": max_latency,
                "std_dev_latency": std_dev_latency,
                "avg_ttft": avg_ttft,
                "avg_tps": avg_tps,
                "tokens_per_dollar": tokens_per_dollar,
                "token_expansion_ratio": token_expansion_ratio,
                "format_pass_rate": format_pass_rate,
                "total_cost": total_cost,
                "total_in_tokens": total_in_tokens,
                "total_out_tokens": total_out_tokens,
                "error_taxonomy": error_taxonomy
            }
            
        gcp_stats = calculate_stats(gcp_res)
        api_stats = calculate_stats(api_res)
        
        report = f"""# 🏁 Channel PK Multi-Dimensional Benchmark Report
**Session Timestamp**: `{self.timestamp}`
**Target Project**: `{self.project_id}`
**Target Model Tested**: `{self.model_id}`
**Traffic Stress Profile**: `{profile_name}`

## 📊 Summary Performance Matrix (多维度测试矩阵)

| Metrics 评估维度 | 🟢 GCP Vertex AI (SA JSON) | 🔵 Gemini API (API Key) | 🏆 Winner 优胜者 |
| :--- | :--- | :--- | :--- |
| **测试样本总数 (Total Trials)** | {gcp_stats['total']} 次 | {api_stats['total']} 次 | 双方等量 |
| **成功率 (Success Rate)** | **{gcp_stats['success_rate']:.1f}%** | **{api_stats['success_rate']:.1f}%** | { '🟢 GCP Vertex AI' if gcp_stats['success_rate'] > api_stats['success_rate'] else ('🔵 Gemini API' if api_stats['success_rate'] > gcp_stats['success_rate'] else '双方持平') } |
| **首 Token 延迟 (TTFT)** | **{gcp_stats['avg_ttft']:.3f} 秒** | **{api_stats['avg_ttft']:.3f} 秒** | { '🟢 GCP Vertex AI' if gcp_stats['avg_ttft'] < api_stats['avg_ttft'] and gcp_stats['avg_ttft'] > 0 else ('🔵 Gemini API' if api_stats['avg_ttft'] < gcp_stats['avg_ttft'] and api_stats['avg_ttft'] > 0 else '暂无数据') } |
| **解码吞吐速率 (Output TPS)** | **{gcp_stats['avg_tps']:.1f} Tokens/s** | **{api_stats['avg_tps']:.1f} Tokens/s** | { '🟢 GCP Vertex AI' if gcp_stats['avg_tps'] > api_stats['avg_tps'] else ('🔵 Gemini API' if api_stats['avg_tps'] > gcp_stats['avg_tps'] else '暂无数据') } |
| **平均端到端延迟 (Avg Latency)** | **{gcp_stats['avg_latency']:.3f} 秒** | **{api_stats['avg_latency']:.3f} 秒** | { '🟢 GCP Vertex AI' if gcp_stats['avg_latency'] < api_stats['avg_latency'] and gcp_stats['avg_latency'] > 0 else ('🔵 Gemini API' if api_stats['avg_latency'] < gcp_stats['avg_latency'] and api_stats['avg_latency'] > 0 else '暂无数据') } |
| **延迟波动标准差 (Latency StdDev)** | {gcp_stats['std_dev_latency']:.3f}s | {api_stats['std_dev_latency']:.3f}s | { '🟢 GCP Vertex AI (极度稳定)' if gcp_stats['std_dev_latency'] < api_stats['std_dev_latency'] and gcp_stats['std_dev_latency'] > 0 else ('🔵 Gemini API (极度稳定)' if api_stats['std_dev_latency'] < gcp_stats['std_dev_latency'] and api_stats['std_dev_latency'] > 0 else '-') } |
| **结构化格式符合率 (Format Pass%)** | **{gcp_stats['format_pass_rate']:.1f}%** | **{api_stats['format_pass_rate']:.1f}%** | - |
| **每美元 Token 产出 (Tokens / $1)** | **{gcp_stats['tokens_per_dollar']:.0f} Tokens** | **{api_stats['tokens_per_dollar']:.0f} Tokens** | { '🔵 Gemini API' if api_stats['tokens_per_dollar'] > gcp_stats['tokens_per_dollar'] else '🟢 GCP Vertex AI' } |
| **总预估消耗费用 (Total Cost)** | **${gcp_stats['total_cost']:.5f}** | **${api_stats['total_cost']:.5f}** | { '🔵 Gemini API' if api_stats['total_cost'] < gcp_stats['total_cost'] else '🟢 GCP Vertex AI' } |

## 🛡️ Error Categorization Taxonomy (错误归因统计)
- **GCP Vertex AI**: `{gcp_stats['error_taxonomy'] if gcp_stats['error_taxonomy'] else 'Clean (无错误)'}`
- **Gemini API**: `{api_stats['error_taxonomy'] if api_stats['error_taxonomy'] else 'Clean (无错误)'}`

## 📝 Trial-by-Trial Raw Results
### GCP Vertex AI (sa_vertex_ai)
| Trial # | Status | Latency | TTFT | TPS | Cost | Error details (if any) |
| :---: | :---: | :--- | :--- | :--- | :--- | :--- |
"""
        for r in gcp_res:
            report += f"| {r['index']} | {'🟢 OK' if r['success'] else '🔴 FAIL'} | {r['latency']:.3f}s | {r['ttft']:.3f}s | {r['tps']:.1f}/s | ${r['cost']:.5f} | {r['error'] if r['error'] else '-'} |\n"
            
        report += """
### Gemini API (gemini_api)
| Trial # | Status | Latency | TTFT | TPS | Cost | Error details (if any) |
| :---: | :---: | :--- | :--- | :--- | :--- | :--- |
"""
        for r in api_res:
            report += f"| {r['index']} | {'🔵 OK' if r['success'] else '🔴 FAIL'} | {r['latency']:.3f}s | {r['ttft']:.3f}s | {r['tps']:.1f}/s | ${r['cost']:.5f} | {r['error'] if r['error'] else '-'} |\n"
            
        report_path = os.path.join(self.target_dir, f"comparison_report_{self.timestamp}.md")
        with open(report_path, "w", encoding="utf-8") as f:
            f.write(report)
            
        metrics_path = os.path.join(self.target_dir, f"raw_metrics_{self.timestamp}.json")
        with open(metrics_path, "w", encoding="utf-8") as f:
            json.dump({
                "timestamp": self.timestamp,
                "project_id": self.project_id,
                "model_id": self.model_id,
                "profile": profile_name,
                "gcp_summary": gcp_stats,
                "api_summary": api_stats,
                "sa_results": gcp_res,
                "api_results": api_res
            }, f, indent=2)
            
        print(f"💾 Saved comparison report to    : {report_path}")
        print(f"💾 Saved raw metrics JSON to     : {metrics_path}\n")

