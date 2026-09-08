#!/usr/bin/env python3
"""
Cross-Project Vertex AI Benchmark Runner
Compare model latency, TTFT, and throughput TPS across different GCP Projects
using dedicated Vertex AI API Keys (or Service Accounts).
"""

import os
import sys
import argparse
import asyncio
from datetime import datetime
from typing import List, Optional

from core.specs import ModelSpec
from core.registry import ModelRegistry
from core.benchmark_engine import get_vertex_client, benchmark_model

def parse_args():
    parser = argparse.ArgumentParser(
        description="Benchmark and compare models across different GCP Projects on Vertex AI using Vertex API Keys."
    )
    # Project A args
    parser.add_argument("--project-a", required=True, help="GCP Project ID for Project A")
    parser.add_argument("--key-a", default=None, help="Vertex AI API Key for Project A (or set VERTEX_API_KEY_A)")
    parser.add_argument("--sa-a", default=None, help="Service Account JSON path for Project A (optional)")
    parser.add_argument("--location-a", default="global", help="Location for Project A (default: global)")

    # Project B args
    parser.add_argument("--project-b", required=True, help="GCP Project ID for Project B")
    parser.add_argument("--key-b", default=None, help="Vertex AI API Key for Project B (or set VERTEX_API_KEY_B)")
    parser.add_argument("--sa-b", default=None, help="Service Account JSON path for Project B (optional)")
    parser.add_argument("--location-b", default="global", help="Location for Project B (default: global)")

    # Test settings
    parser.add_argument("--models", nargs="+", default=None, help="Model IDs to test (e.g. gemini-3.8-flash gemini-3.1-pro-preview)")
    parser.add_argument("--families", nargs="+", default=None, help="Model families to test (e.g. flash pro flash_lite)")
    parser.add_argument("--trials", type=int, default=3, help="Number of repeated trials per model (default: 3)")
    parser.add_argument("--delay", type=float, default=1.0, help="Interval seconds between trials (default: 1.0)")
    parser.add_argument("--prompt", type=str, default=None, help="Custom prompt for the benchmark")

    return parser.parse_args()

async def main():
    args = parse_args()

    key_a = args.key_a or os.environ.get("VERTEX_API_KEY_A") or os.environ.get("VERTEX_API_KEY")
    key_b = args.key_b or os.environ.get("VERTEX_API_KEY_B") or os.environ.get("VERTEX_API_KEY")

    # Resolve target models
    target_specs: List[ModelSpec] = []
    if args.models:
        for m_id in args.models:
            spec = ModelRegistry.get(m_id)
            if spec:
                target_specs.append(spec)
            else:
                print(f"⚠️ Warning: Model '{m_id}' not found in registry. Skipping.")
    elif args.families:
        for fam in args.families:
            target_specs.extend(ModelRegistry.list_models(fam))
    else:
        # Default models: Flash series and Pro series
        target_specs = [
            ModelRegistry.get("gemini-3.8-flash"),
            ModelRegistry.get("gemini-3.1-pro-preview")
        ]
        target_specs = [s for s in target_specs if s is not None]

    if not target_specs:
        print("❌ Error: No valid models specified for benchmark.")
        sys.exit(1)

    print("=" * 80)
    print("🚀 Vertex AI Cross-Project Speed Benchmark (API Key Auth)")
    print("=" * 80)
    print(f"🏢 Project A : {args.project_a} (Location: {args.location_a}, Auth: {'API Key' if key_a else ('SA' if args.sa_a else 'ADC')})")
    print(f"🏢 Project B : {args.project_b} (Location: {args.location_b}, Auth: {'API Key' if key_b else ('SA' if args.sa_b else 'ADC')})")
    print(f"🎯 Target Models ({len(target_specs)}): {[s.model_id for s in target_specs]}")
    print(f"🔁 Trials/Model: {args.trials} (Interval: {args.delay}s)")
    print("=" * 80)

    # Initialize clients
    client_a = get_vertex_client(
        project_id=args.project_a,
        location=args.location_a,
        sa_key=args.sa_a,
        vertex_api_key=key_a
    )
    client_b = get_vertex_client(
        project_id=args.project_b,
        location=args.location_b,
        sa_key=args.sa_b,
        vertex_api_key=key_b
    )

    results = []

    for idx, spec in enumerate(target_specs, 1):
        print(f"\n[{idx}/{len(target_specs)}] 🔬 Benchmarking Model: {spec.model_id} ({spec.display_name})...")
        
        print(f"  ▶ Testing Project A ({args.project_a})...", end="", flush=True)
        stats_a = await benchmark_model(client_a, spec, trials=args.trials, delay=args.delay, prompt=args.prompt)
        print(f" Done. (Avg Latency: {stats_a['avg_latency']:.2f}s, TTFT: {stats_a['avg_ttft']:.2f}s, TPS: {stats_a['avg_tps']:.1f})")

        print(f"  ▶ Testing Project B ({args.project_b})...", end="", flush=True)
        stats_b = await benchmark_model(client_b, spec, trials=args.trials, delay=args.delay, prompt=args.prompt)
        print(f" Done. (Avg Latency: {stats_b['avg_latency']:.2f}s, TTFT: {stats_b['avg_ttft']:.2f}s, TPS: {stats_b['avg_tps']:.1f})")

        # Winner calculations
        winner_latency = (
            f"Project A ({args.project_a})" if stats_a["avg_latency"] > 0 and (stats_b["avg_latency"] == 0 or stats_a["avg_latency"] < stats_b["avg_latency"])
            else (f"Project B ({args.project_b})" if stats_b["avg_latency"] > 0 else "Draw / None")
        )
        winner_ttft = (
            f"Project A ({args.project_a})" if stats_a["avg_ttft"] > 0 and (stats_b["avg_ttft"] == 0 or stats_a["avg_ttft"] < stats_b["avg_ttft"])
            else (f"Project B ({args.project_b})" if stats_b["avg_ttft"] > 0 else "Draw / None")
        )
        winner_tps = (
            f"Project A ({args.project_a})" if stats_a["avg_tps"] > stats_b["avg_tps"]
            else (f"Project B ({args.project_b})" if stats_b["avg_tps"] > stats_a["avg_tps"] else "Draw / None")
        )

        is_multimodal = spec.is_image_model or "multimodal" in spec.modalities or "audio" in spec.modalities or "image_generation" in spec.modalities
        category_str = "多模态 (Multimodal)" if is_multimodal else "文本/语言 (Text)"

        results.append({
            "model_id": spec.model_id,
            "display_name": spec.display_name,
            "category": category_str,
            "is_multimodal": is_multimodal,
            "stats_a": stats_a,
            "stats_b": stats_b,
            "winner_latency": winner_latency,
            "winner_ttft": winner_ttft,
            "winner_tps": winner_tps
        })

    # Print Summary Tables separated by category
    text_results = [r for r in results if not r["is_multimodal"]]
    mm_results = [r for r in results if r["is_multimodal"]]

    if text_results:
        print("\n" + "=" * 96)
        print("📝 【文本/语言模型组】跨 Project 性能对比汇总表 (Text Models)")
        print("=" * 96)
        print(f"{'Model ID':<26} | {'Proj A (Lat / TTFT / TPS)':<28} | {'Proj B (Lat / TTFT / TPS)':<28} | {'TTFT / TPS Winner':<18}")
        print("-" * 96)
        for r in text_results:
            sa = r["stats_a"]
            sb = r["stats_b"]
            a_str = f"{sa['avg_latency']:.2f}s / {sa['avg_ttft']:.2f}s / {sa['avg_tps']:.1f}" if sa['success_count'] > 0 else "FAIL"
            b_str = f"{sb['avg_latency']:.2f}s / {sb['avg_ttft']:.2f}s / {sb['avg_tps']:.1f}" if sb['success_count'] > 0 else "FAIL"
            winner_str = f"TTFT: {r['winner_ttft'].split()[0]} | TPS: {r['winner_tps'].split()[0]}"
            print(f"{r['model_id']:<26} | {a_str:<28} | {b_str:<28} | {winner_str:<18}")

    if mm_results:
        print("\n" + "=" * 96)
        print("🎨 【多模态/图像生成模型组】跨 Project 性能对比汇总表 (Multimodal Models)")
        print("=" * 96)
        print(f"{'Model ID':<26} | {'Proj A (Avg Latency)':<28} | {'Proj B (Avg Latency)':<28} | {'Latency Winner':<18}")
        print("-" * 96)
        for r in mm_results:
            sa = r["stats_a"]
            sb = r["stats_b"]
            a_str = f"{sa['avg_latency']:.2f}s (Success: {sa['success_count']}/{sa['total_trials']})" if sa['success_count'] > 0 else "FAIL"
            b_str = f"{sb['avg_latency']:.2f}s (Success: {sb['success_count']}/{sb['total_trials']})" if sb['success_count'] > 0 else "FAIL"
            print(f"{r['model_id']:<26} | {a_str:<28} | {b_str:<28} | {r['winner_latency']:<18}")

    print("=" * 96)

if __name__ == "__main__":
    asyncio.run(main())