"""
Model specifications, family definitions, and taxonomy for Gemini Benchmark.
"""
from enum import Enum
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional

class ModelFamily(str, Enum):
    PRO = "pro"                    # Pro 系列文本/深度推理模型 (如 gemini-3.1-pro-preview)
    FLASH = "flash"                # Flash 系列文本主力通用模型 (如 gemini-3.8-flash, gemini-3.7-flash, gemini-3.6-flash)
    FLASH_LITE = "flash_lite"      # Flash Lite 系列轻量极速文本模型 (如 gemini-3.5-flash-lite, gemini-3.1-flash-lite)
    NANO_BANANA = "nano_banana"    # NB 系列图像生成模型 (如 gemini-3-pro-image / nano-banana-pro, gemini-3.1-flash-image)
    OMNI = "omni"                  # Omni 系列全能多模态模型 (如 gemini-omni-flash-preview)

@dataclass
class ModelSpec:
    model_id: str
    display_name: str
    family: ModelFamily
    description: str
    input_price_per_1m: float      # 每 100 万输入 Token 价格 (美元)
    output_price_per_1m: float     # 每 100 万输出 Token 价格 (美元)
    modalities: List[str] = field(default_factory=lambda: ["text"])
    default_prompt: str = "Return a JSON object with keys 'model_name', 'primary_use_case', and 'performance_highlights' describing yourself in under 50 words."
    supported_channels: List[str] = field(default_factory=lambda: ["vertex_ai", "gemini_api"])
    is_image_model: bool = False
    aliases: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "model_id": self.model_id,
            "display_name": self.display_name,
            "family": self.family.value,
            "description": self.description,
            "input_price_per_1m": self.input_price_per_1m,
            "output_price_per_1m": self.output_price_per_1m,
            "modalities": self.modalities,
            "supported_channels": self.supported_channels,
            "is_image_model": self.is_image_model,
            "aliases": self.aliases
        }
