import asyncio
from google.genai import types
from .base_tester import BaseModelTester, PRICING_GCP, PRICING_API

# Ensure pricing tables have the model definitions
PRICING_GCP["gemini-3.5-flash-lite"] = {"in": 0.05 / 1000000.0, "out": 0.20 / 1000000.0}
PRICING_API["gemini-3.5-flash-lite"] = {"in": 0.05 / 1000000.0, "out": 0.20 / 1000000.0}

class Gemini35FlashLiteTester(BaseModelTester):
    """
    Plugin tester for gemini-3.5-flash-lite.
    """
    def __init__(self, project_id, location, sa_key, api_key, timestamp):
        super().__init__(
            model_id="gemini-3.5-flash-lite",
            project_id=project_id,
            location=location,
            sa_key=sa_key,
            api_key=api_key,
            timestamp=timestamp
        )

    @classmethod
    def get_traffic_profiles(cls):
        return {
            "standard": {"name": "标准巡检 (3.5 Flash-Lite Standard)", "trials": 5, "delay": 1.5, "desc": "常规同频延迟与通信比对测试"},
            "concurrency_stress": {"name": "高频并发压力 (3.5 Flash-Lite Concurrency Stress)", "trials": 20, "delay": 0.4, "desc": "模拟高负载高突发情况下的并发测试"},
            "heavy_burst": {"name": "极限频发冲击 (3.5 Flash-Lite Heavy Burst)", "trials": 40, "delay": 0.1, "desc": "极短延迟下的吞吐爆破压测"}
        }

    def get_default_prompt(self):
        return "Summarize the key advantages of Gemini 3.5 Flash-Lite for high-throughput edge workloads in 30 words."

    async def execute_gcp_call(self, prompt, index):
        loop = asyncio.get_running_loop()
        config = types.GenerateContentConfig(temperature=0.7, max_output_tokens=200)
        
        self._log_channel("sa_vertex_ai", f"Dispatching generate_content request to Vertex AI.")
        response = await loop.run_in_executor(
            None,
            lambda: self.gcp_client.models.generate_content(
                model=self.model_id,
                contents=prompt,
                config=config
            )
        )
        
        usage = response.usage_metadata
        in_tokens = usage.prompt_token_count if usage else 0
        out_tokens = usage.candidates_token_count if usage else 0
        
        rates = PRICING_GCP[self.model_id]
        cost = (in_tokens * rates["in"]) + (out_tokens * rates["out"])
        response_len = len(response.text) if response.text else 0
        
        self._log_channel("sa_vertex_ai", f"✅ Success | Prompt tokens: {in_tokens} | Output tokens: {out_tokens} | Cost: ${cost:.6f}")
        return True, cost, response_len, ""

    async def execute_api_call(self, prompt, index):
        loop = asyncio.get_running_loop()
        config = types.GenerateContentConfig(temperature=0.7, max_output_tokens=200)
        
        self._log_channel("gemini_api", f"Dispatching generate_content request to Gemini API Studio.")
        response = await loop.run_in_executor(
            None,
            lambda: self.api_client.models.generate_content(
                model=self.model_id,
                contents=prompt,
                config=config
            )
        )
        
        usage = response.usage_metadata
        in_tokens = usage.prompt_token_count if usage else 0
        out_tokens = usage.candidates_token_count if usage else 0
        
        rates = PRICING_API[self.model_id]
        cost = (in_tokens * rates["in"]) + (out_tokens * rates["out"])
        response_len = len(response.text) if response.text else 0
        
        self._log_channel("gemini_api", f"✅ Success | Prompt tokens: {in_tokens} | Output tokens: {out_tokens} | Cost: ${cost:.6f}")
        return True, cost, response_len, ""

export_class = Gemini35FlashLiteTester
