import os
import sys
import time
import json
import argparse
import asyncio
import random
import logging
from datetime import datetime
from google import genai
from google.genai import types

# Model Definitions
MODEL_FLASH_LITE_TEXT = "gemini-3.1-flash-lite"
MODEL_PRO_TEXT = "gemini-3.1-pro-preview"
MODEL_FLASH_LITE_IMAGE = "gemini-3.1-flash-lite-image"
MODEL_FLASH_IMAGE = "gemini-3.1-flash-image"
MODEL_PRO_IMAGE = "gemini-3-pro-image"

# Pricing Table (2026 Latest)
PRICING_GCP = {
    # Vertex AI Billing
    MODEL_FLASH_LITE_TEXT: {"in": 0.25 / 1000000.0, "out": 1.50 / 1000000.0},
    MODEL_PRO_TEXT: {"in": 1.25 / 1000000.0, "out": 5.00 / 1000000.0},
    MODEL_FLASH_LITE_IMAGE: 0.0968,
    MODEL_FLASH_IMAGE: 0.0968,
    MODEL_PRO_IMAGE: 0.0968
}

PRICING_API = {
    # AI Studio Billing
    MODEL_FLASH_LITE_TEXT: {"in": 0.075 / 1000000.0, "out": 0.30 / 1000000.0},
    MODEL_PRO_TEXT: {"in": 1.25 / 1000000.0, "out": 5.00 / 1000000.0},
    MODEL_FLASH_LITE_IMAGE: 0.0510,
    MODEL_FLASH_IMAGE: 0.1510,
    MODEL_PRO_IMAGE: 0.2400
}

class ChannelPKRunner:
    def __init__(self, project_id, location, sa_key, api_key, target_dir, timestamp):
        self.project_id = project_id
        self.location = location
        self.sa_key = sa_key
        self.api_key = api_key
        self.target_dir = target_dir
        self.timestamp = timestamp
        
        self.gcp_client = None
        self.api_client = None
        
        # Buffer structured log lines in memory to write them down at the end of the run
        self.sa_log_buffer = []
        self.api_log_buffer = []
        
        self._init_clients()
        
    def _log_channel(self, channel, message):
        timestamp_str = datetime.now().strftime('%Y-%m-%d %H:%M:%S,%f')[:-3]
        log_line = f"{timestamp_str} [INFO] {message}"
        if channel == "GCP_SA":
            self.sa_log_buffer.append(log_line)
        else:
            self.api_log_buffer.append(log_line)

    def _init_clients(self):
        # 1. Initialize GCP Vertex AI Client (using SA json)
        if self.sa_key:
            os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = self.sa_key
        os.environ["GOOGLE_CLOUD_PROJECT"] = self.project_id
        os.environ["GCLOUD_PROJECT"] = self.project_id
        
        self._log_channel("GCP_SA", "=========================================================")
        self._log_channel("GCP_SA", "🚀 INITIALIZING GCP VERTEX AI CHANNEL CLIENT (SA JSON)")
        self._log_channel("GCP_SA", "=========================================================")
        self._log_channel("GCP_SA", f"Project ID: {self.project_id} | Location: {self.location}")
        self._log_channel("GCP_SA", f"SA Key Path: {self.sa_key}")
        
        try:
            self.gcp_client = genai.Client(
                vertexai=True,
                project=self.project_id,
                location=self.location,
                http_options=types.HttpOptions(headers={"Api-Revision": "2026-05-20"}),
            )
            self._log_channel("GCP_SA", "✅ GCP Client initialized successfully using API Revision 2026-05-20.")
        except Exception as e:
            self._log_channel("GCP_SA", f"❌ Failed to initialize GCP Client: {e}")
            
        # 2. Initialize Gemini API Studio Client (using API Key)
        self._log_channel("GEMINI_API", "=========================================================")
        self._log_channel("GEMINI_API", "🚀 INITIALIZING GEMINI API STUDIO CHANNEL CLIENT (API KEY)")
        self._log_channel("GEMINI_API", "=========================================================")
        self._log_channel("GEMINI_API", f"API Key Masked: {self.api_key[:6]}...{self.api_key[-6:] if len(self.api_key) > 12 else ''}")
        
        try:
            self.api_client = genai.Client(
                api_key=self.api_key,
                http_options=types.HttpOptions(headers={"Api-Revision": "2026-05-20"}),
            )
            self._log_channel("GEMINI_API", "✅ Gemini API Studio Client initialized successfully using API Revision 2026-05-20.")
        except Exception as e:
            self._log_channel("GEMINI_API", f"❌ Failed to initialize Gemini API Client: {e}")

    async def run_single_test(self, channel, model_id, model_type, prompt, index):
        client = self.gcp_client if channel == "GCP_SA" else self.api_client
        pricing = PRICING_GCP if channel == "GCP_SA" else PRICING_API
        
        self._log_channel(channel, f"---------------------------------------------------------")
        self._log_channel(channel, f"🏃 TRIAL #{index} | Model: {model_id} | Type: {model_type}")
        self._log_channel(channel, f"Prompt: \"{prompt}\"")
        
        if not client:
            err = "Client not initialized"
            self._log_channel(channel, f"❌ Request failed: {err}")
            return {"channel": channel, "success": False, "latency": 0.0, "error": err, "cost": 0.0}
            
        start_time = time.perf_counter()
        success = False
        error_msg = ""
        cost = 0.0
        response_len = 0
        response_text_snippet = ""
        
        try:
            loop = asyncio.get_running_loop()
            
            if model_type == "TEXT":
                config = types.GenerateContentConfig(temperature=0.7, max_output_tokens=300)
                
                self._log_channel(channel, "Sending text generation request to endpoint...")
                response = await loop.run_in_executor(
                    None,
                    lambda: client.models.generate_content(
                        model=model_id,
                        contents=prompt,
                        config=config
                    )
                )
                
                usage = response.usage_metadata
                in_tokens = usage.prompt_token_count
                out_tokens = usage.candidates_token_count
                
                rates = pricing.get(model_id, {"in": 0.0, "out": 0.0})
                cost = (in_tokens * rates["in"]) + (out_tokens * rates["out"])
                response_len = len(response.text) if response.text else 0
                response_text_snippet = response.text[:200].replace('\n', ' ') if response.text else ""
                success = True
                
                self._log_channel(channel, f"✅ Response received successfully!")
                self._log_channel(channel, f"   Tokens: In {in_tokens} | Out {out_tokens} | Calculated Cost: ${cost:.6f}")
                self._log_channel(channel, f"   Snippet: \"{response_text_snippet}...\"")
                
            elif model_type == "IMAGE":
                size = "1K" if model_id == MODEL_FLASH_LITE_IMAGE else "2K"
                modalities = ["IMAGE"] if model_id == MODEL_FLASH_LITE_IMAGE else ["TEXT", "IMAGE"]
                
                self._log_channel(channel, f"Sending image generation request (size: {size}) to endpoint...")
                response = await loop.run_in_executor(
                    None,
                    lambda: client.models.generate_content(
                        model=model_id,
                        contents=prompt,
                        config=types.GenerateContentConfig(
                            response_modalities=modalities,
                            image_config=types.ImageConfig(image_size=size)
                        )
                    )
                )
                
                cost = pricing.get(model_id, 0.0)
                response_len = 1
                success = True
                
                self._log_channel(channel, f"✅ Image generation completed successfully!")
                self._log_channel(channel, f"   Pricing tier cost: ${cost:.4f}")
                
        except Exception as e:
            error_msg = str(e)
            self._log_channel(channel, f"❌ Request failed with exception: {error_msg}")
            
        end_time = time.perf_counter()
        latency = end_time - start_time if success else 0.0
        
        if success:
            self._log_channel(channel, f"⏱️ Trial completed in {latency:.3f} seconds.")
        
        return {
            "channel": channel,
            "success": success,
            "latency": latency,
            "error": error_msg,
            "cost": cost,
            "size": response_len,
            "index": index
        }

    async def execute_pk_campaign(self, model_id, model_type, prompt, iterations=5, delay=1.0):
        print(f"🏁 Starting PK Duel: Model [{model_id}] | Type [{model_type}] | Trials [{iterations}]")
        gcp_results = []
        api_results = []
        
        for i in range(1, iterations + 1):
            print(f"👉 Trial #{i}/{iterations} dispatching...")
            
            # Dispatch GCP SA and Gemini API concurrently
            task_gcp = self.run_single_test("GCP_SA", model_id, model_type, prompt, i)
            task_api = self.run_single_test("GEMINI_API", model_id, model_type, prompt, i)
            
            res_gcp, res_api = await asyncio.gather(task_gcp, task_api)
            
            gcp_results.append(res_gcp)
            api_results.append(res_api)
            
            status_gcp = f"🟢 GCP Success ({res_gcp['latency']:.2f}s, ${res_gcp['cost']:.4f})" if res_gcp["success"] else f"🔴 GCP Fail ({res_gcp['error'][:50]})"
            status_api = f"🔵 API Success ({res_api['latency']:.2f}s, ${res_api['cost']:.4f})" if res_api["success"] else f"🔴 API Fail ({res_api['error'][:50]})"
            print(f"   ↳ Result: {status_gcp} vs {status_api}")
            
            if i < iterations:
                await asyncio.sleep(delay)
                
        # Write channel logs inside the specific target_dir matching user specified folder hierarchy
        self._write_channel_logs()
                
        return gcp_results, api_results

    def _write_channel_logs(self):
        os.makedirs(self.target_dir, exist_ok=True)
        
        # Write GCP SA running log
        sa_log_path = os.path.join(self.target_dir, f"sa_vertex_ai_run_{self.timestamp}.log")
        with open(sa_log_path, "w", encoding="utf-8") as f:
            f.write("\n".join(self.sa_log_buffer))
            
        # Write Gemini API running log
        api_log_path = os.path.join(self.target_dir, f"gemini_api_run_{self.timestamp}.log")
        with open(api_log_path, "w", encoding="utf-8") as f:
            f.write("\n".join(self.api_log_buffer))
            
        print(f"💾 Saved SA running log to       : {sa_log_path}")
        print(f"💾 Saved Gemini API running log to: {api_log_path}")

def compile_report(gcp_res, api_res, model_id, timestamp):
    def calculate_stats(results):
        succs = [r for r in results if r["success"]]
        count_succ = len(succs)
        total = len(results)
        succ_rate = (count_succ / total) * 100 if total > 0 else 0.0
        
        latencies = [r["latency"] for r in succs]
        avg_latency = sum(latencies) / len(latencies) if latencies else 0.0
        min_latency = min(latencies) if latencies else 0.0
        max_latency = max(latencies) if latencies else 0.0
        
        total_cost = sum(r["cost"] for r in results)
        
        return {
            "total": total,
            "success_count": count_succ,
            "success_rate": succ_rate,
            "avg_latency": avg_latency,
            "min_latency": min_latency,
            "max_latency": max_latency,
            "total_cost": total_cost
        }
        
    gcp_stats = calculate_stats(gcp_res)
    api_stats = calculate_stats(api_res)
    
    report = f"""# 🏁 Channel PK Duel Report
**Session Timestamp**: `{timestamp}`
**Target Model Tested**: `{model_id}`

## 📊 Summary Performance Comparison
| Metrics 比较维度 | 🟢 GCP Vertex AI (SA JSON) | 🔵 Gemini API (API Key) | 🏆 Winner 优胜者 |
| :--- | :--- | :--- | :--- |
| **总测试样本 (Total Trials)** | {gcp_stats['total']} 次 | {api_stats['total']} 次 | 双方等量 |
| **成功调用次数 (Success)** | {gcp_stats['success_count']} 次 | {api_stats['success_count']} 次 | { 'GCP Vertex AI' if gcp_stats['success_count'] > api_stats['success_count'] else ('Gemini API' if api_stats['success_count'] > gcp_stats['success_count'] else '双方持平') } |
| **测试成功率 (Success Rate)** | **{gcp_stats['success_rate']:.1f}%** | **{api_stats['success_rate']:.1f}%** | { '🟢 GCP Vertex AI' if gcp_stats['success_rate'] > api_stats['success_rate'] else ('🔵 Gemini API' if api_stats['success_rate'] > gcp_stats['success_rate'] else '双方持平') } |
| **平均端到端延迟 (Avg Latency)** | **{gcp_stats['avg_latency']:.3f} 秒** | **{api_stats['avg_latency']:.3f} 秒** | { '🟢 GCP Vertex AI (更低延迟)' if gcp_stats['avg_latency'] < api_stats['avg_latency'] and gcp_stats['avg_latency'] > 0 else ('🔵 Gemini API (更低延迟)' if api_stats['avg_latency'] < gcp_stats['avg_latency'] and api_stats['avg_latency'] > 0 else '暂无成功数据') } |
| **最小/最大延迟 (Min/Max)** | {gcp_stats['min_latency']:.2f}s / {gcp_stats['max_latency']:.2f}s | {api_stats['min_latency']:.2f}s / {api_stats['max_latency']:.2f}s | - |
| **总预估消耗费用 (Total Cost)** | **${gcp_stats['total_cost']:.5f}** | **${api_stats['total_cost']:.5f}** | { '🔵 Gemini API (更低价格)' if api_stats['total_cost'] < gcp_stats['total_cost'] else '🟢 GCP Vertex AI (更低价格)' } |

## 📝 Trial-by-Trial Raw Results
### GCP Vertex AI (sa_vertex_ai)
| Trial # | Status | Latency | Cost | Error details (if any) |
| :---: | :---: | :--- | :--- | :--- |
"""
    for r in gcp_res:
        report += f"| {r['index']} | {'🟢 OK' if r['success'] else '🔴 FAIL'} | {r['latency']:.3f}s | ${r['cost']:.5f} | {r['error'] if r['error'] else '-'} |\n"
        
    report += """
### Gemini API (gemini_api)
| Trial # | Status | Latency | Cost | Error details (if any) |
| :---: | :---: | :--- | :--- | :--- |
"""
    for r in api_res:
        report += f"| {r['index']} | {'🔵 OK' if r['success'] else '🔴 FAIL'} | {r['latency']:.3f}s | ${r['cost']:.5f} | {r['error'] if r['error'] else '-'} |\n"
        
    return report

async def main():
    parser = argparse.ArgumentParser(description="Gemini Channels PK Duel Campaign")
    parser.add_argument("--sa-key", required=True, help="Path to GCP Service Account JSON")
    parser.add_argument("--project", required=True, help="GCP Project ID")
    parser.add_argument("--location", default="global", help="GCP Vertex AI Location")
    parser.add_argument("--api-key", required=True, help="Gemini API Key")
    parser.add_argument("--model", default=MODEL_FLASH_LITE_TEXT, choices=[MODEL_FLASH_LITE_TEXT, MODEL_PRO_TEXT, MODEL_FLASH_LITE_IMAGE, MODEL_FLASH_IMAGE, MODEL_PRO_IMAGE], help="Model to PK")
    parser.add_argument("--trials", type=int, default=5, help="Number of side-by-side test trials")
    parser.add_argument("--delay", type=float, default=1.5, help="Cooldown delay between trials in seconds")
    
    args = parser.parse_args()
    
    # Session Suffix
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    # 📁 Directory Hierarchy Requirement: pk_history -> Project Name -> Model Name
    target_dir = os.path.join("pk_history", args.project, args.model)
    os.makedirs(target_dir, exist_ok=True)
    
    print("=========================================================================")
    print("🏆  GCP Vertex AI  VS  Gemini API (AI Studio)  双通道同频竞技  🏆")
    print("=========================================================================")
    print(f"  - Target Project: {args.project}")
    print(f"  - Target Model  : {args.model}")
    print(f"  - Total Trials  : {args.trials} side-by-side trials")
    print(f"  - Cooldown Delay: {args.delay}s")
    print(f"  - Output Folder : {target_dir}")
    print("=========================================================================\n")
    
    # Establish PK Engine
    runner = ChannelPKRunner(args.project, args.location, args.sa_key, args.api_key, target_dir, timestamp)
    
    # Define test payloads
    if args.model in [MODEL_FLASH_LITE_IMAGE, MODEL_FLASH_IMAGE, MODEL_PRO_IMAGE]:
        model_type = "IMAGE"
        prompt = "A masterfully detailed, highly cinematic illustration of a coding duel."
    else:
        model_type = "TEXT"
        prompt = "Summarize the technical differences between Vertex AI and Google AI Studio in 50 words."
        
    gcp_res, api_res = await runner.execute_pk_campaign(
        model_id=args.model,
        model_type=model_type,
        prompt=prompt,
        iterations=args.trials,
        delay=args.delay
    )
    
    # Output PK Report
    report = compile_report(gcp_res, api_res, args.model, timestamp)
    print("\n" + report)
    
    # Save comparison report with timestamp suffix inside target_dir
    report_filename = os.path.join(target_dir, f"comparison_report_{timestamp}.md")
    with open(report_filename, "w", encoding="utf-8") as f:
        f.write(report)
        
    # Save raw structured metrics JSON with timestamp suffix inside target_dir
    metrics_filename = os.path.join(target_dir, f"raw_metrics_{timestamp}.json")
    with open(metrics_filename, "w", encoding="utf-8") as f:
        json.dump({
            "timestamp": timestamp,
            "project_id": args.project,
            "model_id": args.model,
            "sa_results": gcp_res,
            "api_results": api_res
        }, f, indent=2)
        
    print("=========================================================================")
    print(f"🎉 Channel PK Duel completed! All files saved cleanly in Project hierarchy:")
    print(f"📂 Folder Path  : {target_dir}")
    print(f"📄 Summary Report: comparison_report_{timestamp}.md")
    # Clarify exact names to reflect SA vs Gemini API
    print(f"📄 SA Run Log   : sa_vertex_ai_run_{timestamp}.log")
    print(f"📄 API Run Log  : gemini_api_run_{timestamp}.log")
    print(f"📄 Raw Metrics  : raw_metrics_{timestamp}.json")
    print("=========================================================================")

if __name__ == '__main__':
    if sys.platform == 'darwin':
        asyncio.set_event_loop_policy(asyncio.DefaultEventLoopPolicy())
    asyncio.run(main())
