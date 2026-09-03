import asyncio
from google.genai import types
from .base_tester import BaseModelTester, PRICING_GCP, PRICING_API

class ProImageTester(BaseModelTester):
    """
    Plugin tester for gemini-3-pro-image (Ultra-premium multimodal image generation model).
    """
    def __init__(self, project_id, location, sa_key, api_key, timestamp):
        super().__init__(
            model_id="gemini-3-pro-image",
            project_id=project_id,
            location=location,
            sa_key=sa_key,
            api_key=api_key,
            timestamp=timestamp
        )

    @classmethod
    def get_traffic_profiles(cls):
        return {
            "standard": {"name": "标准画质巡检 (Pro Image Standard)", "trials": 2, "delay": 5.0, "desc": "常规同频单图生成，低并发校准"},
            "stress_blast": {"name": "图像并发压力 (Pro Image Stress Blast)", "trials": 5, "delay": 3.0, "desc": "极速冲击 4K 图像通道配额极限测试"}
        }

    def get_default_prompt(self):
        return "An epic 4K masterpiece illustration showing artificial intelligence contesting with humans in a neon-lit cyberpunk arena."

    async def execute_gcp_call(self, prompt, index):
        loop = asyncio.get_running_loop()
        config = types.GenerateContentConfig(
            response_modalities=["TEXT", "IMAGE"],
            image_config=types.ImageConfig(image_size="4K")
        )
        
        self._log_channel("sa_vertex_ai", f"Dispatching image generation (4K) request to Vertex AI.")
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
            response_modalities=["TEXT", "IMAGE"],
            image_config=types.ImageConfig(image_size="4K")
        )
        
        self._log_channel("gemini_api", f"Dispatching image generation (4K) request to Gemini API Studio.")
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
export_class = ProImageTester
