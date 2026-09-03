"""
Core Benchmark Execution Engine.
Measures TTFT, Output TPS, E2E Latency, Jitter, JSON Compliance, and Cost across Vertex AI & Gemini API.
"""
import os
import time
import math
import json
import asyncio
from typing import Dict, Any, List, Optional
from google import genai
from google.genai import types
from .specs import ModelSpec, ModelFamily

def classify_error(err_str: str) -> str:
    err_upper = err_str.upper()
    if "429" in err_upper or "RESOURCE_EXHAUSTED" in err_upper:
        return "429_RATE_LIMIT"
    elif "500" in err_upper or "503" in err_upper or "INTERNAL" in err_upper:
        return "500_SERVER_INTERNAL"
    elif "LOCATION IS NOT SUPPORTED" in err_upper or "FAILED_PRECONDITION" in err_upper:
        return "400_LOCATION_UNSUPPORTED"
    elif "401" in err_upper or "403" in err_upper or "PERMISSION_DENIED" in err_upper or "UNAUTHENTICATED" in err_upper:
        return "401_403_AUTH_DENIED"
    elif "404" in err_upper or "NOT_FOUND" in err_upper:
        return "404_NOT_FOUND"
    return "OTHER_ERROR"

def get_vertex_client(project_id: str, location: str = "global", sa_key: Optional[str] = None) -> genai.Client:
    """Create a Google GenAI Client configured for Vertex AI."""
    if sa_key and os.path.exists(sa_key):
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = sa_key
    return genai.Client(vertexai=True, project=project_id, location=location)

def get_gemini_api_client(api_key: Optional[str] = None) -> Optional[genai.Client]:
    """Create a Google GenAI Client configured for Gemini API Studio."""
    key = api_key or os.environ.get("GEMINI_API_KEY", "")
    if not key:
        return None
    try:
        return genai.Client(api_key=key, vertexai=False)
    except Exception:
        return None

async def execute_stream_trial(client: genai.Client, spec: ModelSpec, prompt: str) -> Dict[str, Any]:
    """Execute a single streaming call to measure TTFT, TPS, format validity, and cost."""
    loop = asyncio.get_running_loop()
    start_t = time.perf_counter()

    if spec.is_image_model:
        # Image model flow
        def _call_img():
            return client.models.generate_images(
                model=spec.model_id,
                prompt=prompt,
                config=types.GenerateImagesConfig(number_of_images=1)
            )
        try:
            resp = await loop.run_in_executor(None, _call_img)
            latency = time.perf_counter() - start_t
            cost = spec.output_price_per_1m  # per image cost
            return {
                "success": True,
                "latency": latency,
                "ttft": latency,
                "tps": 1.0 / latency if latency > 0 else 0.0,
                "in_tokens": len(prompt.split()),
                "out_tokens": 1,
                "cost": cost,
                "format_valid": True,
                "error": ""
            }
        except Exception as e:
            err = str(e)
            return {
                "success": False,
                "latency": 0.0,
                "ttft": 0.0,
                "tps": 0.0,
                "in_tokens": 0,
                "out_tokens": 0,
                "cost": 0.0,
                "format_valid": False,
                "error": err,
                "error_type": classify_error(err)
            }

    # Text / Flash / Pro streaming flow
    def _call_text():
        config = types.GenerateContentConfig(
            temperature=0.7,
            max_output_tokens=500,
            response_mime_type="application/json"
        )
        stream = client.models.generate_content_stream(
            model=spec.model_id,
            contents=prompt,
            config=config
        )
        first_chunk = True
        ttft = 0.0
        full_text = ""
        usage = None
        for chunk in stream:
            if first_chunk:
                ttft = time.perf_counter() - start_t
                first_chunk = False
            if chunk.text:
                full_text += chunk.text
            if hasattr(chunk, "usage_metadata") and chunk.usage_metadata:
                usage = chunk.usage_metadata
        return full_text, ttft, usage

    try:
        full_text, ttft, usage = await loop.run_in_executor(None, _call_text)
        latency = time.perf_counter() - start_t
        in_tokens = usage.prompt_token_count if usage else 0
        out_tokens = usage.candidates_token_count if usage else 0
        
        in_cost = (in_tokens / 1e6) * spec.input_price_per_1m
        out_cost = (out_tokens / 1e6) * spec.output_price_per_1m
        cost = in_cost + out_cost
        tps = (out_tokens / latency) if (latency > 0 and out_tokens > 0) else 0.0

        # Validate JSON format
        format_valid = True
        try:
            cleaned = full_text.strip()
            if "```json" in cleaned:
                cleaned = cleaned.split("```json")[1].split("```")[0].strip()
            elif "```" in cleaned:
                cleaned = cleaned.split("```")[1].split("```")[0].strip()
            data = json.loads(cleaned)
            if not isinstance(data, dict):
                format_valid = False
        except Exception:
            format_valid = False

        return {
            "success": True,
            "latency": latency,
            "ttft": ttft,
            "tps": tps,
            "in_tokens": in_tokens,
            "out_tokens": out_tokens,
            "cost": cost,
            "format_valid": format_valid,
            "error": ""
        }
    except Exception as e:
        err = str(e)
        return {
            "success": False,
            "latency": 0.0,
            "ttft": 0.0,
            "tps": 0.0,
            "in_tokens": 0,
            "out_tokens": 0,
            "cost": 0.0,
            "format_valid": False,
            "error": err,
            "error_type": classify_error(err)
        }

async def benchmark_model(client: genai.Client, spec: ModelSpec, trials: int = 3, delay: float = 1.0, prompt: Optional[str] = None) -> Dict[str, Any]:
    """Execute multiple trials on a single model and compute multi-dimensional statistics."""
    test_prompt = prompt or spec.default_prompt
    raw_results = []
    
    for i in range(trials):
        res = await execute_stream_trial(client, spec, test_prompt)
        raw_results.append(res)
        if i < trials - 1:
            await asyncio.sleep(delay)

    succs = [r for r in raw_results if r["success"]]
    fails = [r for r in raw_results if not r["success"]]
    count_succ = len(succs)
    total = len(raw_results)
    succ_rate = (count_succ / total) * 100.0 if total > 0 else 0.0

    latencies = [r["latency"] for r in succs]
    avg_latency = sum(latencies) / len(latencies) if latencies else 0.0
    min_latency = min(latencies) if latencies else 0.0
    max_latency = max(latencies) if latencies else 0.0

    if len(latencies) > 1:
        variance = sum((x - avg_latency) ** 2 for x in latencies) / (len(latencies) - 1)
        std_dev = math.sqrt(variance)
    else:
        std_dev = 0.0

    ttfts = [r["ttft"] for r in succs]
    avg_ttft = sum(ttfts) / len(ttfts) if ttfts else 0.0

    tps_list = [r["tps"] for r in succs]
    avg_tps = sum(tps_list) / len(tps_list) if tps_list else 0.0

    total_cost = sum(r["cost"] for r in succs)
    total_out_tokens = sum(r["out_tokens"] for r in succs)
    tokens_per_dollar = (total_out_tokens / total_cost) if total_cost > 0 else 0.0

    fmt_passes = [r for r in succs if r["format_valid"]]
    fmt_rate = (len(fmt_passes) / count_succ) * 100.0 if count_succ > 0 else 0.0

    error_taxonomy = {}
    for f in fails:
        etype = f.get("error_type", classify_error(f.get("error", "")))
        error_taxonomy[etype] = error_taxonomy.get(etype, 0) + 1

    return {
        "model_id": spec.model_id,
        "display_name": spec.display_name,
        "family": spec.family.value,
        "total_trials": total,
        "success_count": count_succ,
        "success_rate": succ_rate,
        "avg_latency": avg_latency,
        "min_latency": min_latency,
        "max_latency": max_latency,
        "std_dev": std_dev,
        "avg_ttft": avg_ttft,
        "avg_tps": avg_tps,
        "total_cost": total_cost,
        "tokens_per_dollar": tokens_per_dollar,
        "format_pass_rate": fmt_rate,
        "error_taxonomy": error_taxonomy,
        "raw_trials": raw_results
    }
