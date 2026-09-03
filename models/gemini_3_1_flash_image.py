import asyncio
from google.genai import types
from .base_tester import BaseModelTester, PRICING_GCP, PRICING_API

class FlashImageTester(BaseModelTester):
    """
    Plugin tester for gemini-3.1-flash-image (Standard multimodal image generation model).
    """
    def __init__(self, project_id, location, sa_key, api_key, timestamp):
        super().__init__(
            model_id="gemini-3.1-flash-image",
            project_id=project_id,
            location=location,
            sa_key=sa_key,
            api_key=api_key,
            timestamp=timestamp
        )

    @classmethod
    def get_traffic_profiles(cls):
        return {
            "standard": {"name": "标准画质巡检 (Flash Image Standard)", "trials": 3, "delay": 4.0, "desc": "常规同频单图生成，低并发校准"},
            "stress_blast": {"name": "图像并发压力 (Flash Image Stress Blast)", "trials": 6, "delay": 2.0, "desc": "中高并发下 2K 图像通道配额吞吐压力校验"}
        }

    def get_default_prompt(self):
        return "A sleek, masterfully designed, high-resolution visual of a coding contest under dramatic studio spotlight."

    async def execute_gcp_call(self, prompt, index):
        loop = asyncio.get_running_loop()
        config = types.GenerateContentConfig(
            response_modalities=["TEXT", "IMAGE"],
            image_config=types.ImageConfig(image_size="2K")
        )
        
        self._log_channel("sa_vertex_ai", f"Dispatching image generation (2K) request to Vertex AI.")
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
            image_config=types.ImageConfig(image_size="2K")
        )
        
        self._log_channel("gemini_api", f"Dispatching image generation (2K) request to Gemini API Studio.")
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
export_class = FlashImageTester
