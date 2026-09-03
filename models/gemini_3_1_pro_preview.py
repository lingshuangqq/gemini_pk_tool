import asyncio
from google.genai import types
from .base_tester import BaseModelTester, PRICING_GCP, PRICING_API

class ProTextTester(BaseModelTester):
    """
    Plugin tester for gemini-3.1-pro-preview (Advanced reasoning text model).
    """
    def __init__(self, project_id, location, sa_key, api_key, timestamp):
        super().__init__(
            model_id="gemini-3.1-pro-preview",
            project_id=project_id,
            location=location,
            sa_key=sa_key,
            api_key=api_key,
            timestamp=timestamp
        )

    @classmethod
    def get_traffic_profiles(cls):
        return {
            "standard": {"name": "标准巡检 (Pro Standard)", "trials": 5, "delay": 2.0, "desc": "常规同频推理压测"},
            "reasoning_stress": {"name": "中载推理压力 (Pro Reasoning Stress)", "trials": 10, "delay": 1.0, "desc": "高阶逻辑推理高并发测试"},
            "extreme_depth": {"name": "极限吞吐测试 (Pro Extreme Depth)", "trials": 15, "delay": 0.6, "desc": "触发密集配额保护极限压测"}
        }

    def get_default_prompt(self):
        return "Solve the logical riddle: A box has 3 apples. You take 2. How many do you have?"

    async def execute_gcp_call(self, prompt, index):
        loop = asyncio.get_running_loop()
        config = types.GenerateContentConfig(temperature=0.3, max_output_tokens=300)
        
        self._log_channel("sa_vertex_ai", f"Dispatching generate_content reasoning request to Vertex AI.")
        response = await loop.run_in_executor(
            None,
            lambda: self.gcp_client.models.generate_content(
                model=self.model_id,
                contents=prompt,
                config=config
            )
        )
        
        usage = response.usage_metadata
        in_tokens = usage.prompt_token_count
        out_tokens = usage.candidates_token_count
        
        rates = PRICING_GCP[self.model_id]
        cost = (in_tokens * rates["in"]) + (out_tokens * rates["out"])
        response_len = len(response.text) if response.text else 0
        
        self._log_channel("sa_vertex_ai", f"✅ Success | Prompt tokens: {in_tokens} | Output tokens: {out_tokens} | Cost: ${cost:.6f}")
        self._log_channel("sa_vertex_ai", f"Response snippet: \"{response.text[:120].strip()}...\"")
        
        return True, cost, response_len, ""

    async def execute_api_call(self, prompt, index):
        loop = asyncio.get_running_loop()
        config = types.GenerateContentConfig(temperature=0.3, max_output_tokens=300)
        
        self._log_channel("gemini_api", f"Dispatching generate_content reasoning request to Gemini API Studio.")
        response = await loop.run_in_executor(
            None,
            lambda: self.api_client.models.generate_content(
                model=self.model_id,
                contents=prompt,
                config=config
            )
        )
        
        usage = response.usage_metadata
        in_tokens = usage.prompt_token_count
        out_tokens = usage.candidates_token_count
        
        rates = PRICING_API[self.model_id]
        cost = (in_tokens * rates["in"]) + (out_tokens * rates["out"])
        response_len = len(response.text) if response.text else 0
        
        self._log_channel("gemini_api", f"✅ Success | Prompt tokens: {in_tokens} | Output tokens: {out_tokens} | Cost: ${cost:.6f}")
        self._log_channel("gemini_api", f"Response snippet: \"{response.text[:120].strip()}...\"")
        
        return True, cost, response_len, ""
export_class = ProTextTester
