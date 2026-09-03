import asyncio
from google.genai import types
from .base_tester import BaseModelTester, PRICING_GCP, PRICING_API

class FlashLiteTextTester(BaseModelTester):
    """
    Plugin tester for gemini-3.1-flash-lite (Standard text model).
    """
    def __init__(self, project_id, location, sa_key, api_key, timestamp):
        super().__init__(
            model_id="gemini-3.1-flash-lite",
            project_id=project_id,
            location=location,
            sa_key=sa_key,
            api_key=api_key,
            timestamp=timestamp
        )

    @classmethod
    def get_traffic_profiles(cls):
        return {
            "standard": {"name": "标准巡检 (Lite Standard)", "trials": 5, "delay": 1.5, "desc": "常规的同频状态基准校验"},
            "concurrency_stress": {"name": "中载压力测试 (Lite Concurrency Stress)", "trials": 20, "delay": 0.4, "desc": "模拟持续高负载并发测试"},
            "heavy_burst": {"name": "极限高频冲击 (Lite Heavy Burst)", "trials": 40, "delay": 0.1, "desc": "极短延迟下的吞吐爆破压测"}
        }

    def get_default_prompt(self):
        return "Summarize the architectural differences between Vertex AI and Google AI Studio in exactly 40 words."

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
        
        # Calculate cost
        rates = PRICING_GCP[self.model_id]
        cost = (in_tokens * rates["in"]) + (out_tokens * rates["out"])
        response_len = len(response.text) if response.text else 0
        
        self._log_channel("sa_vertex_ai", f"✅ Success | Prompt tokens: {in_tokens} | Output tokens: {out_tokens} | Cost: ${cost:.6f}")
        
        return True, cost, response_len, "", in_tokens, out_tokens

    async def execute_api_call(self, prompt, index):
        loop = asyncio.get_running_loop()
        config = types.GenerateContentConfig(temperature=0.7, max_output_tokens=300)
        
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
        
        # Calculate cost
        rates = PRICING_API[self.model_id]
        cost = (in_tokens * rates["in"]) + (out_tokens * rates["out"])
        response_len = len(response.text) if response.text else 0
        
        self._log_channel("gemini_api", f"✅ Success | Prompt tokens: {in_tokens} | Output tokens: {out_tokens} | Cost: ${cost:.6f}")
        
        return True, cost, response_len, "", in_tokens, out_tokens
export_class = FlashLiteTextTester
