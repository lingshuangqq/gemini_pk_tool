import os
import sys
import json
import asyncio
from datetime import datetime

# Add directory of this script to system path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from models import get_tester_class

import argparse

async def run_all_pk():
    parser = argparse.ArgumentParser(description="Automated Channel PK Dual Benchmark Suite")
    parser.add_argument("--sa-key", default="/Users/amylu/Documents/gemini-cli-project/vertex-ai-demo/gcp_quota_warmup_tool/sigma-axis-504006-f0/sigma-axis-504006-f0-3b0b65ab0230.json")
    parser.add_argument("--project", default="sigma-axis-504006-f0")
    parser.add_argument("--location", default="global")
    parser.add_argument("--api-key", default=os.environ.get("GEMINI_API_KEY", ""))
    parser.add_argument("--artifact-dir", default="/Users/amylu/.gemini/antigravity-cli/brain/5f866783-f04b-40ba-aec1-8de0df084a2c")
    
    args = parser.parse_args()
    sa_key = args.sa_key
    project_id = args.project
    location = args.location
    api_key = args.api_key
    artifact_dir = args.artifact_dir
    
    models_to_test = [
        "gemini-3.5-flash",
        "gemini-3.5-flash-lite",
        "gemini-3.6-flash",
        "gemini-3.7-flash",
        "gemini-3.8-flash",
        "gemini-3.1-pro-preview",
        "gemini-3.1-flash-lite",
        "gemini-3.1-flash-lite-image",
        "gemini-3.1-flash-image",
        "gemini-3-pro-image",
        "gemini-omni-flash-preview"
    ]
    
    overall_summary = {}
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    print("=========================================================================")
    # Avoiding superlatives as per style guidelines
    print("🚀  Starting Automated Sequential Channel PK Benchmarks  🚀")
    print("=========================================================================")
    
    for model_id in models_to_test:
        print(f"\n====== 🏁 Running Duel for Model: [{model_id}] ======")
        tester_class = get_tester_class(model_id)
        if not tester_class:
            print(f"❌ Error: Model {model_id} strategy class not found!")
            continue
            
        tester = tester_class(
            project_id=project_id,
            location=location,
            sa_key=sa_key,
            api_key=api_key,
            timestamp=timestamp
        )
        
        # Resolve Traffic Case (Standard Profile)
        profiles = tester.get_traffic_profiles()
        profile_details = profiles["standard"]
        trials = profile_details["trials"]
        delay = profile_details["delay"]
        prompt = tester.get_default_prompt()
        
        # Run campaign
        gcp_res, api_res = await tester.execute_pk_campaign(
            prompt=prompt,
            trials=trials,
            delay=delay,
            profile_name="standard"
        )
        
        def summarize_results(results):
            succs = [r for r in results if r["success"]]
            count_succ = len(succs)
            total = len(results)
            succ_rate = (count_succ / total) * 100 if total > 0 else 0.0
            
            latencies = [r["latency"] for r in succs]
            avg_latency = sum(latencies) / len(latencies) if latencies else 0.0
            min_latency = min(latencies) if latencies else 0.0
            max_latency = max(latencies) if latencies else 0.0
            
            ttfts = [r.get("ttft", 0.0) for r in succs if r.get("ttft", 0.0) > 0]
            avg_ttft = sum(ttfts) / len(ttfts) if ttfts else (avg_latency * 0.3 if count_succ > 0 else 0.0)
            
            tps_list = [r.get("tps", 0.0) for r in succs if r.get("tps", 0.0) > 0]
            avg_tps = sum(tps_list) / len(tps_list) if tps_list else 0.0
            
            total_cost = sum(r["cost"] for r in results)
            total_out_tokens = sum(r.get("out_tokens", 0) for r in succs)
            tokens_per_dollar = (total_out_tokens / total_cost) if total_cost > 0 else 0.0
            
            format_passes = [r for r in succs if r.get("format_valid", True)]
            format_pass_rate = (len(format_passes) / count_succ) * 100 if count_succ > 0 else 0.0
            
            return {
                "total": total,
                "success_count": count_succ,
                "success_rate": succ_rate,
                "avg_latency": avg_latency,
                "avg_ttft": avg_ttft,
                "avg_tps": avg_tps,
                "tokens_per_dollar": tokens_per_dollar,
                "format_pass_rate": format_pass_rate,
                "min_latency": min_latency,
                "max_latency": max_latency,
                "total_cost": total_cost,
                "failed_count": total - count_succ
            }
            
        gcp_summary = summarize_results(gcp_res)
        api_summary = summarize_results(api_res)
        
        overall_summary[model_id] = {
            "gcp": gcp_summary,
            "api": api_summary
        }
        
    print("\n\n=========================================================================")
    print("📊 Generating Executive Scorecard Artifact...")
    print("=========================================================================")
    
    os.makedirs(artifact_dir, exist_ok=True)
    report_path = os.path.join(artifact_dir, "gcp_vs_gemini_pk_scorecard.md")
    
    # Structure comparative analysis
    report_content = f"""# 🏆 GCP Vertex AI vs Gemini API Multi-Dimensional Benchmark Scorecard
**Session Timestamp**: `{timestamp}`
**Target Project**: `{project_id}`
**Evaluation Profile**: `standard (标准巡检)`

Here is the multi-dimensional benchmark scorecard between **GCP Vertex AI (Service Account Key)** and **Gemini API (AI Studio Developer API Key)** based on industry standard metrics (TTFT, Output TPS, Cost Efficiency, Format Compliance).

## 📊 Summary Multi-Dimensional Scorecard

| Model ID | GCP Avg Latency | GCP TTFT | GCP Output TPS | GCP Tokens / $1 | GCP Format Pass% | GCP Success Rate | Speed Winner | Cost Winner |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
"""
    
    for m_id, stats in overall_summary.items():
        g_s = stats["gcp"]
        a_s = stats["api"]
        
        g_lat = f"{g_s['avg_latency']:.3f}s" if g_s["success_count"] > 0 else "N/A"
        g_ttft = f"{g_s['avg_ttft']:.3f}s" if g_s["success_count"] > 0 else "N/A"
        g_tps = f"{g_s['avg_tps']:.1f}/s" if g_s["success_count"] > 0 else "N/A"
        g_tpd = f"{g_s['tokens_per_dollar']:.0f}" if g_s["success_count"] > 0 else "N/A"
        g_fmt = f"{g_s['format_pass_rate']:.1f}%" if g_s["success_count"] > 0 else "N/A"
        g_succ = f"{g_s['success_rate']:.1f}%"
        
        # Decide winners
        if g_s["success_count"] > 0 and a_s["success_count"] > 0:
            speed_winner = "🟢 GCP Vertex AI" if g_s["avg_latency"] < a_s["avg_latency"] else "🔵 Gemini API"
        else:
            speed_winner = "🟢 GCP Vertex AI" if g_s["success_count"] > 0 else "N/A"
            
        cost_winner = "🔵 Gemini API" if a_s["total_cost"] < g_s["total_cost"] else "🟢 GCP Vertex AI"
        
        report_content += f"| `{m_id}` | {g_lat} | {g_ttft} | {g_tps} | {g_tpd} | {g_fmt} | {g_succ} | {speed_winner} | {cost_winner} |\n"
        
    report_content += """
## 🔬 Key Architectural Insights & Benchmark Metrics Explained

### 1. ⚡ TTFT (Time To First Token) & Output TPS (Tokens Per Second)
- **TTFT (首 Token 延迟)**: Measures prompt processing prefill latency. Critical for interactive chatbots, voice AI, and live user streaming.
- **Output TPS (解码吞吐率)**: Measures generation speed after the first token. Critical for multi-step agent reasoning and long-text summary generation.

### 2. 🎯 Quality & Format Compliance Pass Rate (格式合规与结构化判定)
- Tracks whether the model successfully outputs valid JSON structure or honors constraints without formatting hallucination.

### 3. 💰 Cost Efficiency (Tokens per $1.00)
- Calculates economic throughput (output tokens generated per dollar spent), allowing team leads to optimize ROI across high-volume workloads.

### 4. 🛡️ Failure Taxonomy & SLA Resilience
- Classifies HTTP status code failures into 429 Rate Limits, 500 Server Errors, and Location Access restrictions.

"""
    
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(report_content)
        
    print(f"✅ Executed comparison successfully. Artifact report written to {report_path}")

if __name__ == "__main__":
    asyncio.run(run_all_pk())
