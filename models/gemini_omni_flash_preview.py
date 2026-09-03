import asyncio
from google import genai
from google.genai import types
from .base_tester import BaseModelTester, PRICING_GCP, PRICING_API

# Ensure pricing tables have the model definitions
PRICING_GCP["gemini-omni-flash-preview"] = {"in": 0.075 / 1000000.0, "out": 0.30 / 1000000.0}
PRICING_API["gemini-omni-flash-preview"] = {"in": 0.075 / 1000000.0, "out": 0.30 / 1000000.0}

class GeminiOmniFlashTester(BaseModelTester):
    """
    Plugin tester for gemini-omni-flash-preview (Omni modality flash model using Interactions API).
    """
    def __init__(self, project_id, location, sa_key, api_key, timestamp):
        # gemini-omni-flash-preview requires location 'global', 'us', or 'eu'
        target_location = location if location in ["global", "us", "eu"] else "global"
        super().__init__(
            model_id="gemini-omni-flash-preview",
            project_id=project_id,
            location=target_location,
            sa_key=sa_key,
            api_key=api_key,
            timestamp=timestamp
        )

    @classmethod
    def get_traffic_profiles(cls):
        return {
            "standard": {"name": "标准巡检 (Omni Flash Standard)", "trials": 5, "delay": 1.5, "desc": "常规同频延迟与通道连通比对"},
            "concurrency_stress": {"name": "高并发性能 (Omni Flash Concurrency Stress)", "trials": 20, "delay": 0.4, "desc": "高并发下全模态接口的多通道分发压力校验"},
            "heavy_burst": {"name": "极速吞吐爆破 (Omni Flash Heavy Burst)", "trials": 40, "delay": 0.1, "desc": "极短延迟下的吞吐爆破压力测试"}
        }

    def get_default_prompt(self):
        return "Explain how omni modality natively processes audio and video streaming inputs in exactly 50 words."

    async def execute_gcp_call(self, prompt, index):
        loop = asyncio.get_running_loop()
        
        self._log_channel("sa_vertex_ai", f"Dispatching interactions.create request to Vertex AI ({self.location}).")
        response = await loop.run_in_executor(
            None,
            lambda: self.gcp_client.interactions.create(
                model=self.model_id,
                input=prompt
            )
        )
        
        usage = getattr(response, "usage", None)
        in_tokens = getattr(usage, "total_input_tokens", 0) if usage else 0
        out_tokens = getattr(usage, "total_output_tokens", 0) if usage else 0
        
        rates = PRICING_GCP[self.model_id]
        cost = (in_tokens * rates["in"]) + (out_tokens * rates["out"])
        output_text = getattr(response, "output_text", "") or ""
        response_len = len(output_text)
        
        self._log_channel("sa_vertex_ai", f"✅ Success | Prompt tokens: {in_tokens} | Output tokens: {out_tokens} | Cost: ${cost:.6f}")
        self._log_channel("sa_vertex_ai", f"Response snippet: \"{output_text[:120].strip()}...\"")
        
        return True, cost, response_len, "", in_tokens, out_tokens

    async def execute_api_call(self, prompt, index):
        loop = asyncio.get_running_loop()
        
        self._log_channel("gemini_api", f"Dispatching interactions.create request to Gemini API Studio.")
        response = await loop.run_in_executor(
            None,
            lambda: self.api_client.interactions.create(
                model=self.model_id,
                input=prompt
            )
        )
        
        usage = getattr(response, "usage", None)
        in_tokens = getattr(usage, "total_input_tokens", 0) if usage else 0
        out_tokens = getattr(usage, "total_output_tokens", 0) if usage else 0
        
        rates = PRICING_API[self.model_id]
        cost = (in_tokens * rates["in"]) + (out_tokens * rates["out"])
        output_text = getattr(response, "output_text", "") or ""
        response_len = len(output_text)
        
        self._log_channel("gemini_api", f"✅ Success | Prompt tokens: {in_tokens} | Output tokens: {out_tokens} | Cost: ${cost:.6f}")
        self._log_channel("gemini_api", f"Response snippet: \"{output_text[:120].strip()}...\"")
        
        return True, cost, response_len, "", in_tokens, out_tokens

export_class = GeminiOmniFlashTester
