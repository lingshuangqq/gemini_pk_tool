import time
import asyncio
import json
from google.genai import types
from .base_tester import BaseModelTester, PRICING_GCP, PRICING_API

# Ensure pricing tables have the new model definitions
PRICING_GCP["gemini-3.8-flash"] = {"in": 0.075 / 1000000.0, "out": 0.30 / 1000000.0}
PRICING_API["gemini-3.8-flash"] = {"in": 0.075 / 1000000.0, "out": 0.30 / 1000000.0}

class Gemini38FlashTester(BaseModelTester):
    """
    Plugin tester for gemini-3.8-flash (Latest 3.8 Flash generation model).
    Supports multi-dimensional benchmarking: E2E Latency, TTFT (Time to First Token), 
    Output TPS, Format Compliance, and Cost-efficiency.
    """
    def __init__(self, project_id, location, sa_key, api_key, timestamp):
        super().__init__(
            model_id="gemini-3.8-flash",
            project_id=project_id,
            location=location,
            sa_key=sa_key,
            api_key=api_key,
            timestamp=timestamp
        )

    @classmethod
    def get_traffic_profiles(cls):
        return {
            "standard": {"name": "标准巡检 (3.8 Flash Standard)", "trials": 5, "delay": 1.5, "desc": "常规同频延迟与通信比对测试"},
            "concurrency_stress": {"name": "高频并发压力 (3.8 Flash Concurrency Stress)", "trials": 25, "delay": 0.3, "desc": "模拟高负载高突发情况下的并发测试"},
            "heavy_burst": {"name": "极限频发冲击 (3.8 Flash Heavy Burst)", "trials": 50, "delay": 0.1, "desc": "极短延迟下的吞吐爆破压测"}
        }

    def get_default_prompt(self):
        return "Return a JSON object with keys 'model', 'latency_optimization', and 'agentic_capabilities' describing Gemini 3.8 Flash in under 40 words."

    def _call_stream(self, client, prompt, config):
        start_t = time.perf_counter()
        ttft = 0.0
        full_text = ""
        first_chunk = True
        usage = None
        
        response_stream = client.models.generate_content_stream(
            model=self.model_id,
            contents=prompt,
            config=config
        )
        for chunk in response_stream:
            if first_chunk:
                ttft = time.perf_counter() - start_t
                first_chunk = False
            if chunk.text:
                full_text += chunk.text
            if hasattr(chunk, "usage_metadata") and chunk.usage_metadata:
                usage = chunk.usage_metadata
                
        return full_text, ttft, usage

    async def execute_gcp_call(self, prompt, index):
        loop = asyncio.get_running_loop()
        config = types.GenerateContentConfig(temperature=0.7, max_output_tokens=500, response_mime_type="application/json")
        
        self._log_channel("sa_vertex_ai", f"Dispatching generate_content_stream request to Vertex AI.")
        full_text, ttft, usage = await loop.run_in_executor(
            None,
            lambda: self._call_stream(self.gcp_client, prompt, config)
        )
        
        in_tokens = usage.prompt_token_count if usage else 0
        out_tokens = usage.candidates_token_count if usage else 0
        
        rates = PRICING_GCP[self.model_id]
        cost = (in_tokens * rates["in"]) + (out_tokens * rates["out"])
        response_len = len(full_text)
        
        format_valid = True
        if "JSON" in prompt.upper() or "{" in prompt:
            try:
                cleaned = full_text.strip()
                if "```json" in cleaned:
                    cleaned = cleaned.split("```json")[1].split("```")[0].strip()
                elif "```" in cleaned:
                    cleaned = cleaned.split("```")[1].split("```")[0].strip()
                json.loads(cleaned)
            except Exception:
                format_valid = False
                
        self._log_channel("sa_vertex_ai", f"✅ Success | TTFT: {ttft:.3f}s | In: {in_tokens} | Out: {out_tokens} | Cost: ${cost:.6f} | Format Valid: {format_valid}")
        self._log_channel("sa_vertex_ai", f"Response snippet: \"{full_text[:120].strip()}...\"")
        
        return True, cost, response_len, "", in_tokens, out_tokens, ttft, format_valid

    async def execute_api_call(self, prompt, index):
        loop = asyncio.get_running_loop()
        config = types.GenerateContentConfig(temperature=0.7, max_output_tokens=500, response_mime_type="application/json")
        
        self._log_channel("gemini_api", f"Dispatching generate_content_stream request to Gemini API Studio.")
        full_text, ttft, usage = await loop.run_in_executor(
            None,
            lambda: self._call_stream(self.api_client, prompt, config)
        )
        
        in_tokens = usage.prompt_token_count if usage else 0
        out_tokens = usage.candidates_token_count if usage else 0
        
        rates = PRICING_API[self.model_id]
        cost = (in_tokens * rates["in"]) + (out_tokens * rates["out"])
        response_len = len(full_text)
        
        format_valid = True
        if "JSON" in prompt.upper() or "{" in prompt:
            try:
                cleaned = full_text.strip()
                if "```json" in cleaned:
                    cleaned = cleaned.split("```json")[1].split("```")[0].strip()
                elif "```" in cleaned:
                    cleaned = cleaned.split("```")[1].split("```")[0].strip()
                json.loads(cleaned)
            except Exception:
                format_valid = False
                
        self._log_channel("gemini_api", f"✅ Success | TTFT: {ttft:.3f}s | In: {in_tokens} | Out: {out_tokens} | Cost: ${cost:.6f} | Format Valid: {format_valid}")
        self._log_channel("gemini_api", f"Response snippet: \"{full_text[:120].strip()}...\"")
        
        return True, cost, response_len, "", in_tokens, out_tokens, ttft, format_valid

export_class = Gemini38FlashTester
