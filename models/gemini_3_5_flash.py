import asyncio
from google.genai import types
from .base_tester import BaseModelTester, PRICING_GCP, PRICING_API

# Ensure pricing tables have the new model definitions
PRICING_GCP["gemini-3.5-flash"] = {"in": 0.075 / 1000000.0, "out": 0.30 / 1000000.0}
PRICING_API["gemini-3.5-flash"] = {"in": 0.075 / 1000000.0, "out": 0.30 / 1000000.0}

class Gemini35FlashTester(BaseModelTester):
    """
    Plugin tester for gemini-3.5-flash (Standard 3.5 generation text model).
    """
    def __init__(self, project_id, location, sa_key, api_key, timestamp):
        super().__init__(
            model_id="gemini-3.5-flash",
            project_id=project_id,
            location=location,
            sa_key=sa_key,
            api_key=api_key,
            timestamp=timestamp
        )

    @classmethod
    def get_traffic_profiles(cls):
        return {
            "standard": {"name": "标准巡检 (3.5 Flash Standard)", "trials": 5, "delay": 1.5, "desc": "常规同频延迟与通信比对测试"},
            "concurrency_stress": {"name": "高频并发压力 (3.5 Flash Concurrency Stress)", "trials": 25, "delay": 0.3, "desc": "模拟高负载高突发情况下的并发测试"},
            "heavy_burst": {"name": "极限频发冲击 (3.5 Flash Heavy Burst)", "trials": 50, "delay": 0.1, "desc": "极短延迟下的吞吐爆破压测"}
        }

    def get_default_prompt(self):
        return "Explain the main architectural advantages of Gemini 3.5 Flash compared to 1.5 Flash in exactly 40 words."

    async def execute_gcp_call(self, prompt, index):
        loop = asyncio.get_running_loop()
        config = types.GenerateContentConfig(temperature=0.7, max_output_tokens=250)
        
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
        self._log_channel("sa_vertex_ai", f"Response snippet: \"{response.text[:120].strip()}...\"")
        
        return True, cost, response_len, "", in_tokens, out_tokens

    async def execute_api_call(self, prompt, index):
        loop = asyncio.get_running_loop()
        config = types.GenerateContentConfig(temperature=0.7, max_output_tokens=250)
        
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
        self._log_channel("gemini_api", f"Response snippet: \"{response.text[:120].strip()}...\"")
        
        return True, cost, response_len, "", in_tokens, out_tokens
export_class = Gemini35FlashTester
