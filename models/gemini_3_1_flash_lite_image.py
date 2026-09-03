import asyncio
from google.genai import types
from .base_tester import BaseModelTester, PRICING_GCP, PRICING_API

class FlashLiteImageTester(BaseModelTester):
    """
    Plugin tester for gemini-3.1-flash-lite-image (Lite multimodal image generation model).
    """
    def __init__(self, project_id, location, sa_key, api_key, timestamp):
        super().__init__(
            model_id="gemini-3.1-flash-lite-image",
            project_id=project_id,
            location=location,
            sa_key=sa_key,
            api_key=api_key,
            timestamp=timestamp
        )

    @classmethod
    def get_traffic_profiles(cls):
        return {
            "standard": {"name": "标准画质巡检 (Lite Image Standard)", "trials": 3, "delay": 3.0, "desc": "常规同频单图生成，低并发校准"},
            "stress_blast": {"name": "高频图像生成 (Lite Image Concurrency Stress)", "trials": 8, "delay": 1.5, "desc": "高并发下 Lite 图像接口吞吐与稳定性测试"}
        }

    def get_default_prompt(self):
        return "An ultra-premium cinematic visual of a high-speed coding duel in progress, dynamic cyan and purple ambient glow."

    async def execute_gcp_call(self, prompt, index):
        loop = asyncio.get_running_loop()
        config = types.GenerateContentConfig(
            response_modalities=["IMAGE"],
            image_config=types.ImageConfig(image_size="1K")
        )
        
        self._log_channel("sa_vertex_ai", f"Dispatching image generation (1K) request to Vertex AI.")
        response = await loop.run_in_executor(
            None,
            lambda: self.gcp_client.models.generate_content(
                model=self.model_id,
                contents=prompt,
                config=config
            )
        )
        
        cost = PRICING_GCP[self.model_id]
        self._log_channel("sa_vertex_ai", f"✅ Success | Image generated successfully. Cost: ${cost:.4f}")
        return True, cost, 1, ""

    async def execute_api_call(self, prompt, index):
        loop = asyncio.get_running_loop()
        config = types.GenerateContentConfig(
            response_modalities=["IMAGE"],
            image_config=types.ImageConfig(image_size="1K")
        )
        
        self._log_channel("gemini_api", f"Dispatching image generation (1K) request to Gemini API Studio.")
        response = await loop.run_in_executor(
            None,
            lambda: self.api_client.models.generate_content(
                model=self.model_id,
                contents=prompt,
                config=config
            )
        )
        
        cost = PRICING_API[self.model_id]
        self._log_channel("gemini_api", f"✅ Success | Image generated successfully. Cost: ${cost:.4f}")
        return True, cost, 1, ""
export_class = FlashLiteImageTester
