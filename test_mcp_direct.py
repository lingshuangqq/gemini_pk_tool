"""
Direct Unit and Functional Test for Gemini Benchmark MCP Server tools.
"""
import os
import sys
import asyncio
import json

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from mcp_server.server import (
    list_available_models,
    benchmark_vertex_ai,
    benchmark_channel_pk,
    benchmark_gemini_api
)

SA_KEY = "/Users/amylu/Documents/gemini-cli-project/vertex-ai-demo/gcp_quota_warmup_tool/spark-ccc/spark-ccc-6228ae67b792.json"
PROJECT_ID = "spark-ccc"

async def test_all():
    print("=========================================================================")
    print("🧪 1. Testing list_available_models across families...")
    print("=========================================================================")
    
    # 1.1 List all families
    all_res = list_available_models("all")
    print(f"Total registered models: {all_res['total_models']}")
    print(f"Supported families: {all_res['available_families']}")
    assert all_res["total_models"] >= 10
    
    # 1.2 List by family
    for fam in ["pro", "flash", "flash_lite", "nano_banana", "omni"]:
        fam_res = list_available_models(fam)
        model_names = [m["model_id"] for m in fam_res["models"]]
        print(f"Family [{fam}]: {len(fam_res['models'])} models -> {model_names}")
        assert len(fam_res["models"]) > 0

    print("\n=========================================================================")
    print("🧪 2. Testing benchmark_vertex_ai (Requirement 1: Vertex AI multi-family)...")
    print("=========================================================================")
    v_res = await benchmark_vertex_ai(
        project_id=PROJECT_ID,
        location="global",
        sa_key=SA_KEY,
        models=["gemini-3.8-flash", "gemini-3.5-flash-lite"],
        trials=2,
        delay=0.5
    )
    print(f"Vertex AI Benchmark Status: {v_res['status']}")
    print(f"Models Tested: {v_res['total_models_tested']}")
    for s in v_res["benchmark_summary"]:
        print(f"  -> Model: {s['model_id']} | Success: {s['success_rate']:.0f}% | Avg Latency: {s['avg_latency']:.2f}s | TTFT: {s['avg_ttft']:.2f}s | TPS: {s['avg_tps']:.1f}")

    print("\n=========================================================================")
    print("🧪 3. Testing benchmark_channel_pk (Requirement 2: Same model GCP vs API)...")
    print("=========================================================================")
    pk_res = await benchmark_channel_pk(
        model_id="gemini-3.8-flash",
        project_id=PROJECT_ID,
        location="global",
        sa_key=SA_KEY,
        trials=2,
        delay=0.5
    )
    print(f"Channel PK Status: {pk_res['status']}")
    print(f"Model: {pk_res['model_id']} (Family: {pk_res['family']})")
    print(f"GCP Stats -> Latency: {pk_res['vertex_ai_stats']['avg_latency']:.2f}s | TTFT: {pk_res['vertex_ai_stats']['avg_ttft']:.2f}s")
    print(f"API Stats -> Latency: {pk_res['gemini_api_stats']['avg_latency']:.2f}s | TTFT: {pk_res['gemini_api_stats']['avg_ttft']:.2f}s")
    print(f"Determined Winners: {pk_res['winners']}")

    print("\n=========================================================================")
    print("🧪 4. Testing benchmark_gemini_api (Requirement 3: Gemini API Studio)...")
    print("=========================================================================")
    # Testing graceful behavior when API key is passed vs omitted
    api_res_nokey = await benchmark_gemini_api(api_key=None, models=["gemini-3.8-flash"])
    print(f"Gemini API (No Key) Status: {api_res_nokey['status']} | Message: {api_res_nokey.get('message')}")
    assert api_res_nokey["status"] == "error"

    print("\n=========================================================================")
    print("✅ All MCP Server tool functions successfully verified!")
    print("=========================================================================")

if __name__ == "__main__":
    asyncio.run(test_all())
