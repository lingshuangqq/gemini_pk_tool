import os
import sys
import json
import time
import asyncio
from datetime import datetime

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from models import get_tester_class, list_registered_models

import argparse

async def run_vertex_benchmark():
    parser = argparse.ArgumentParser(description="Vertex AI Multi-Model Concurrency & Latency Benchmark")
    parser.add_argument("--sa-key", default="/Users/amylu/Documents/gemini-cli-project/vertex-ai-demo/gcp_quota_warmup_tool/sigma-axis-504006-f0/sigma-axis-504006-f0-3b0b65ab0230.json")
    parser.add_argument("--project", default="sigma-axis-504006-f0")
    parser.add_argument("--location", default="global")
    parser.add_argument("--artifact-dir", default="/Users/amylu/.gemini/antigravity-cli/brain/b3746d93-00f3-45e4-975e-31bef1628362")
    
    args = parser.parse_args()
    vertex_key = args.sa_key
    project_id = args.project
    location = args.location
    artifact_dir = args.artifact_dir
    dummy_api_key = "dummy_api_key_placeholder"
    
    models = list_registered_models()
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    print("=========================================================================")
    print("🚀 Starting Vertex AI Multi-Model Concurrency & Latency Benchmark 🚀")
    print(f"Target Project: {project_id}")
    print(f"Vertex Key/SA : {vertex_key}")
    print(f"Total Models  : {len(models)}")
    print("=========================================================================\n")
    
    benchmark_summary = {}
    
    for model_id in models:
        print(f"-------------------------------------------------------------------------")
        print(f"🔎 Testing Model: [{model_id}]")
        print(f"-------------------------------------------------------------------------")
        
        tester_class = get_tester_class(model_id)
        if not tester_class:
            print(f"❌ Error: No strategy found for {model_id}")
            continue
            
        tester = tester_class(
            project_id=project_id,
            location=location,
            sa_key=vertex_key,
            api_key=dummy_api_key,
            timestamp=timestamp
        )
        
        profiles = tester.get_traffic_profiles()
        # Default to standard profile for quick latency/token validation across all models
        profile_key = "standard"
        p_info = profiles[profile_key]
        trials = p_info["trials"]
        prompt = tester.get_default_prompt()
        
        print(f"  - Profile : {p_info['name']} ({profile_key})")
        print(f"  - Payload : \"{prompt[:60]}...\"")
        print(f"  - Concurrency Test: Dispatching {trials} parallel requests...")
        
        start_time = time.perf_counter()
        
        # Fire all requests concurrently
        tasks = [tester.run_single_test("sa_vertex_ai", prompt, i+1) for i in range(trials)]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        total_time = time.perf_counter() - start_time
        
        valid_results = []
        for r in results:
            if isinstance(r, dict):
                valid_results.append(r)
            else:
                valid_results.append({
                    "channel": "GCP Vertex AI",
                    "success": False,
                    "latency": 0.0,
                    "error": str(r),
                    "cost": 0.0,
                    "size": 0,
                    "in_tokens": 0,
                    "out_tokens": 0,
                    "index": 0
                })
                
        successes = [r for r in valid_results if r["success"]]
        succ_count = len(successes)
        fail_count = len(valid_results) - succ_count
        succ_rate = (succ_count / len(valid_results)) * 100 if valid_results else 0.0
        
        latencies = [r["latency"] for r in successes]
        avg_lat = sum(latencies) / len(latencies) if latencies else 0.0
        min_lat = min(latencies) if latencies else 0.0
        max_lat = max(latencies) if latencies else 0.0
        
        total_in_tokens = sum(r.get("in_tokens", 0) for r in valid_results)
        total_out_tokens = sum(r.get("out_tokens", 0) for r in valid_results)
        avg_in_tokens = total_in_tokens / succ_count if succ_count > 0 else 0.0
        avg_out_tokens = total_out_tokens / succ_count if succ_count > 0 else 0.0
        
        rps = succ_count / total_time if total_time > 0 else 0.0
        total_cost = sum(r["cost"] for r in valid_results)
        
        benchmark_summary[model_id] = {
            "profile_name": p_info['name'],
            "total_trials": trials,
            "success_count": succ_count,
            "fail_count": fail_count,
            "success_rate": succ_rate,
            "avg_latency": avg_lat,
            "min_latency": min_lat,
            "max_latency": max_lat,
            "total_time": total_time,
            "rps": rps,
            "total_cost": total_cost,
            "total_in_tokens": total_in_tokens,
            "total_out_tokens": total_out_tokens,
            "avg_in_tokens": avg_in_tokens,
            "avg_out_tokens": avg_out_tokens,
            "details": valid_results
        }
        
        status_str = f"🟢 PASS ({succ_rate:.1f}%)" if succ_rate > 0 else "🔴 FAIL"
        print(f"  - Result  : {status_str} | Succ: {succ_count}/{trials} | Avg Latency: {avg_lat:.3f}s | RPS: {rps:.2f}")
        print(f"  - Tokens  : In Total: {total_in_tokens} (Avg: {avg_in_tokens:.1f}) | Out Total: {total_out_tokens} (Avg: {avg_out_tokens:.1f})")
        print()

    # Save summary report
    os.makedirs(artifact_dir, exist_ok=True)
    report_file = os.path.join(artifact_dir, "vertex_all_models_concurrency_scorecard.md")
    
    report_md = f"""# ⚡ Vertex AI All-Models Performance & Token Consumption Scorecard
**Project ID**: `{project_id}`
**Execution Timestamp**: `{timestamp}`
**Authorization Mode**: `Vertex AI Express API Key`

This report details the concurrent request performance, latency distribution, throughput (RPS), and **Input/Output Token consumption** across all supported Vertex AI models.

## 📊 Performance & Token Consumption Scorecard

| Model ID | Test Case | Success Rate | Avg Latency | Throughput (RPS) | Total Input Tokens (Avg/req) | Total Output Tokens (Avg/req) | Total Cost | Status |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
"""
    for m_id, stats in benchmark_summary.items():
        succ_str = f"**{stats['success_rate']:.1f}%** ({stats['success_count']}/{stats['total_trials']})"
        avg_l = f"{stats['avg_latency']:.3f}s" if stats['success_count'] > 0 else "N/A"
        rps_str = f"{stats['rps']:.2f} req/s"
        
        in_tok_str = f"**{stats['total_in_tokens']}** ({stats['avg_in_tokens']:.0f})"
        out_tok_str = f"**{stats['total_out_tokens']}** ({stats['avg_out_tokens']:.0f})"
        
        cost_str = f"${stats['total_cost']:.5f}"
        status_tag = "🟢 OK" if stats['success_rate'] == 100 else ("🟡 Partial" if stats['success_rate'] > 0 else "🔴 Fail")
        
        report_md += f"| `{m_id}` | {stats['profile_name']} | {succ_str} | **{avg_l}** | {rps_str} | {in_tok_str} | {out_tok_str} | {cost_str} | {status_tag} |\n"

    report_md += """
## 📝 Detailed Model Breakdown

"""
    for m_id, stats in benchmark_summary.items():
        report_md += f"### Model: `{m_id}`\n"
        report_md += f"- **Profile Used**: {stats['profile_name']}\n"
        report_md += f"- **Success / Total**: {stats['success_count']} / {stats['total_trials']} ({stats['success_rate']:.1f}%)\n"
        report_md += f"- **Latency Profile**: Avg `{stats['avg_latency']:.3f}s` | Min `{stats['min_latency']:.2f}s` | Max `{stats['max_latency']:.2f}s`\n"
        report_md += f"- **Token Statistics**: Input Total `{stats['total_in_tokens']}` (Avg `{stats['avg_in_tokens']:.1f}`) | Output Total `{stats['total_out_tokens']}` (Avg `{stats['avg_out_tokens']:.1f}`)\n\n"
        report_md += "| Trial # | Status | Latency | Input Tokens | Output Tokens | Cost | Error Details (if any) |\n"
        report_md += "| :---: | :---: | :--- | :---: | :---: | :--- | :--- |\n"
        for d in stats["details"]:
            st = "🟢 OK" if d["success"] else "🔴 FAIL"
            report_md += f"| {d['index']} | {st} | {d['latency']:.3f}s | {d.get('in_tokens', 0)} | {d.get('out_tokens', 0)} | ${d['cost']:.5f} | {d['error'] if d['error'] else '-'} |\n"
        report_md += "\n"

    with open(report_file, "w", encoding="utf-8") as f:
        f.write(report_md)
        
    print("=========================================================================")
    print(f"🎉 Vertex AI Benchmark Completed! Scorecard saved to:")
    print(f"📄 {report_file}")
    print("=========================================================================")

if __name__ == "__main__":
    if sys.platform == 'darwin':
        asyncio.set_event_loop_policy(asyncio.DefaultEventLoopPolicy())
    asyncio.run(run_vertex_benchmark())
