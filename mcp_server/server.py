"""
Gemini Benchmark MCP Server.
Provides FastMCP tools for Vertex AI vs Gemini API multi-dimensional benchmarking,
family-categorized model testing, and channel PK duels.
"""
import os
import sys
import json
import asyncio
from typing import List, Dict, Any, Optional
from mcp.server.fastmcp import FastMCP

# Ensure parent directory is in sys.path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from core.specs import ModelFamily, ModelSpec
from core.registry import ModelRegistry
from core.benchmark_engine import (
    get_vertex_client,
    get_gemini_api_client,
    benchmark_model
)

mcp = FastMCP("gemini-benchmark-server")

@mcp.tool()
def list_available_models(family: Optional[str] = None) -> Dict[str, Any]:
    """
    List registered Gemini models categorized by family.
    
    Args:
        family: Optional filter. Values: 'all', 'pro', 'flash', 'flash_lite', 'nano_banana' (or 'nb'), 'omni'.
    
    Returns:
        Dictionary with list of models, their family, pricing, and capabilities.
    """
    models = ModelRegistry.list_models(family)
    return {
        "status": "success",
        "filter_family": family or "all",
        "available_families": ModelRegistry.list_families(),
        "total_models": len(models),
        "models": [m.to_dict() for m in models]
    }

@mcp.tool()
async def benchmark_vertex_ai(
    project_id: str = "spark-ccc",
    location: str = "global",
    sa_key: Optional[str] = None,
    families: Optional[List[str]] = None,
    models: Optional[List[str]] = None,
    trials: int = 3,
    delay: float = 1.0,
    prompt: Optional[str] = None
) -> Dict[str, Any]:
    """
    [Requirement 1] Benchmark multiple models on Google Cloud Vertex AI across multi-dimensional metrics.
    
    Measures: TTFT, Output TPS, E2E Latency, Jitter (StdDev), Format Compliance, Cost Efficiency (Tokens/$1).
    
    Args:
        project_id: GCP Project ID (e.g., 'spark-ccc')
        location: Vertex AI region (default: 'global')
        sa_key: Absolute path to Service Account JSON key (optional if ADC is configured)
        families: List of model families to benchmark (e.g., ['flash', 'pro', 'flash_lite', 'nano_banana'])
        models: Explicit list of model IDs to test (e.g., ['gemini-3.8-flash', 'gemini-3.7-flash'])
        trials: Number of repeated requests per model (default: 3)
        delay: Seconds between requests (default: 1.0)
        prompt: Custom prompt to test (optional)
    """
    target_specs: List[ModelSpec] = []
    
    if models:
        for m_id in models:
            spec = ModelRegistry.get(m_id)
            if spec:
                target_specs.append(spec)
    elif families:
        for f in families:
            target_specs.extend(ModelRegistry.list_models(f))
    else:
        # Default: test flash family
        target_specs = ModelRegistry.list_models("flash")

    if not target_specs:
        return {"status": "error", "message": "No matching models found for benchmark."}

    client = get_vertex_client(project_id=project_id, location=location, sa_key=sa_key)
    
    results = []
    for spec in target_specs:
        stats = await benchmark_model(client, spec, trials=trials, delay=delay, prompt=prompt)
        results.append(stats)

    return {
        "status": "success",
        "channel": "Vertex AI",
        "project_id": project_id,
        "location": location,
        "total_models_tested": len(results),
        "benchmark_summary": results
    }

@mcp.tool()
async def benchmark_channel_pk(
    model_id: str = "gemini-3.8-flash",
    project_id: str = "spark-ccc",
    location: str = "global",
    sa_key: Optional[str] = None,
    api_key: Optional[str] = None,
    trials: int = 3,
    delay: float = 1.0,
    prompt: Optional[str] = None
) -> Dict[str, Any]:
    """
    [Requirement 2] Benchmark and compare the SAME model across GCP Vertex AI and Gemini API Studio.
    
    Performs head-to-head channel comparison to determine channel winners in TTFT, TPS, Cost, and SLA stability.
    
    Args:
        model_id: Model ID to compare (e.g. 'gemini-3.8-flash', 'gemini-3.1-pro-preview')
        project_id: GCP Project ID for Vertex AI
        location: Vertex AI location (default 'global')
        sa_key: Service account JSON path for Vertex AI
        api_key: Gemini API Key for Gemini API Studio
        trials: Number of trials per channel (default: 3)
        delay: Interval between trials (default: 1.0)
        prompt: Optional benchmark prompt
    """
    spec = ModelRegistry.get(model_id)
    if not spec:
        return {"status": "error", "message": f"Model {model_id} is not registered in ModelRegistry."}

    v_client = get_vertex_client(project_id=project_id, location=location, sa_key=sa_key)
    a_client = get_gemini_api_client(api_key=api_key)

    v_stats = await benchmark_model(v_client, spec, trials=trials, delay=delay, prompt=prompt)
    if a_client:
        a_stats = await benchmark_model(a_client, spec, trials=trials, delay=delay, prompt=prompt)
    else:
        a_stats = {
            "model_id": spec.model_id,
            "display_name": spec.display_name,
            "family": spec.family.value,
            "total_trials": trials,
            "success_count": 0,
            "success_rate": 0.0,
            "avg_latency": 0.0,
            "min_latency": 0.0,
            "max_latency": 0.0,
            "std_dev": 0.0,
            "avg_ttft": 0.0,
            "avg_tps": 0.0,
            "total_cost": 0.0,
            "tokens_per_dollar": 0.0,
            "format_pass_rate": 0.0,
            "error_taxonomy": {"NO_API_KEY_PROVIDED": trials},
            "raw_trials": []
        }

    # Determine winners
    winner_latency = "GCP Vertex AI" if v_stats["avg_latency"] > 0 and (a_stats["avg_latency"] == 0 or v_stats["avg_latency"] < a_stats["avg_latency"]) else ("Gemini API" if a_stats["avg_latency"] > 0 else "Draw / None")
    winner_ttft = "GCP Vertex AI" if v_stats["avg_ttft"] > 0 and (a_stats["avg_ttft"] == 0 or v_stats["avg_ttft"] < a_stats["avg_ttft"]) else ("Gemini API" if a_stats["avg_ttft"] > 0 else "Draw / None")
    winner_tps = "GCP Vertex AI" if v_stats["avg_tps"] > a_stats["avg_tps"] else ("Gemini API" if a_stats["avg_tps"] > v_stats["avg_tps"] else "Draw / None")

    return {
        "status": "success",
        "model_id": spec.model_id,
        "display_name": spec.display_name,
        "family": spec.family.value,
        "trials": trials,
        "vertex_ai_stats": v_stats,
        "gemini_api_stats": a_stats,
        "winners": {
            "latency": winner_latency,
            "ttft": winner_ttft,
            "throughput_tps": winner_tps
        }
    }

@mcp.tool()
async def benchmark_gemini_api(
    api_key: Optional[str] = None,
    families: Optional[List[str]] = None,
    models: Optional[List[str]] = None,
    trials: int = 3,
    delay: float = 1.0,
    prompt: Optional[str] = None
) -> Dict[str, Any]:
    """
    [Requirement 3] Benchmark multiple models on Google Gemini API Studio across multi-dimensional metrics.
    
    Args:
        api_key: Gemini API Key (or defaults to GEMINI_API_KEY environment variable)
        families: List of model families (e.g., ['flash', 'pro', 'flash_lite'])
        models: Explicit list of model IDs
        trials: Trials count per model
        delay: Delay between calls
        prompt: Benchmark prompt
    """
    target_specs: List[ModelSpec] = []
    
    if models:
        for m_id in models:
            spec = ModelRegistry.get(m_id)
            if spec:
                target_specs.append(spec)
    elif families:
        for f in families:
            target_specs.extend(ModelRegistry.list_models(f))
    else:
        target_specs = ModelRegistry.list_models("flash")

    if not target_specs:
        return {"status": "error", "message": "No matching models found for Gemini API benchmark."}

    client = get_gemini_api_client(api_key=api_key)
    if not client:
        return {
            "status": "error",
            "message": "No valid Gemini API key provided. Please pass api_key parameter or set GEMINI_API_KEY environment variable."
        }
    
    results = []
    for spec in target_specs:
        stats = await benchmark_model(client, spec, trials=trials, delay=delay, prompt=prompt)
        results.append(stats)

    return {
        "status": "success",
        "channel": "Gemini API Studio",
        "total_models_tested": len(results),
        "benchmark_summary": results
    }

if __name__ == "__main__":
    mcp.run()
