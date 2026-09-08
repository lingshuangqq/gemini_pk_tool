"""
Unified Model Registry for Gemini Benchmark and PK Tool.
Enables plug-and-play addition of new models and categorized query by family.
"""
from typing import Dict, List, Optional
from .specs import ModelFamily, ModelSpec

class ModelRegistry:
    _registry: Dict[str, ModelSpec] = {}
    _alias_map: Dict[str, str] = {}

    @classmethod
    def register(cls, spec: ModelSpec) -> None:
        """Register a new model specification."""
        cls._registry[spec.model_id] = spec
        cls._alias_map[spec.model_id.lower()] = spec.model_id
        for alias in spec.aliases:
            cls._alias_map[alias.lower()] = spec.model_id

    @classmethod
    def get(cls, model_id_or_alias: str) -> Optional[ModelSpec]:
        """Lookup model spec by model ID or alias."""
        key = model_id_or_alias.lower().strip()
        actual_id = cls._alias_map.get(key)
        if actual_id:
            return cls._registry.get(actual_id)
        return cls._registry.get(model_id_or_alias)

    @classmethod
    def list_models(cls, family: Optional[str] = None) -> List[ModelSpec]:
        """List registered models, optionally filtered by family name."""
        if not family or family.lower() in ("all", "*"):
            return list(cls._registry.values())
        
        target_family = family.lower().strip()
        # Support aliases for family query: 'nb' -> 'nano_banana', 'lite' -> 'flash_lite'
        if target_family in ("nb", "nanobanana", "nano-banana"):
            target_family = ModelFamily.NANO_BANANA.value
        elif target_family in ("lite", "flashlite", "flash-lite"):
            target_family = ModelFamily.FLASH_LITE.value

        return [m for m in cls._registry.values() if m.family.value == target_family]

    @classmethod
    def list_families(cls) -> List[str]:
        """List all supported model family identifiers."""
        return [f.value for f in ModelFamily]

    @classmethod
    def clear(cls) -> None:
        cls._registry.clear()
        cls._alias_map.clear()

# =========================================================================
# Default Built-in Model Registrations
# =========================================================================

# 1. Pro 系列文本模型 (Pro Family)
ModelRegistry.register(ModelSpec(
    model_id="gemini-3.1-pro-preview",
    display_name="Gemini 3.1 Pro (Preview)",
    family=ModelFamily.PRO,
    description="最新旗舰深度逻辑推理与代码生成大模型",
    input_price_per_1m=1.25,
    output_price_per_1m=5.00,
    modalities=["text", "json", "code"],
    aliases=["3.1-pro", "gemini-3.1-pro"]
))

ModelRegistry.register(ModelSpec(
    model_id="gemini-3-pro-preview",
    display_name="Gemini 3 Pro (Preview)",
    family=ModelFamily.PRO,
    description="Google 3代基础旗舰推理模型",
    input_price_per_1m=1.25,
    output_price_per_1m=5.00,
    modalities=["text", "json", "code"],
    aliases=["3-pro", "gemini-3-pro"]
))

# 2. Flash 系列文本模型 (Flash Family)
ModelRegistry.register(ModelSpec(
    model_id="gemini-3.8-flash",
    display_name="Gemini 3.8 Flash (2026 最新主力)",
    family=ModelFamily.FLASH,
    description="2026年最新主力模型，针对多步 Agent 与高并发解码进行极速优化",
    input_price_per_1m=0.10,
    output_price_per_1m=0.40,
    modalities=["text", "json", "streaming"],
    aliases=["3.8-flash", "38-flash"],
    is_promotional=True,
    promo_discount=0.5,
    promo_end_date="2026-12-31"
))

ModelRegistry.register(ModelSpec(
    model_id="gemini-3.7-flash",
    display_name="Gemini 3.7 Flash",
    family=ModelFamily.FLASH,
    description="混合自适应思考 Flash 模型，具备深度思考与快速响应双模式",
    input_price_per_1m=0.075,
    output_price_per_1m=0.30,
    modalities=["text", "json"],
    aliases=["3.7-flash"],
    is_promotional=True,
    promo_discount=0.5,
    promo_end_date="2026-12-31"
))

ModelRegistry.register(ModelSpec(
    model_id="gemini-3.6-flash",
    display_name="Gemini 3.6 Flash",
    family=ModelFamily.FLASH,
    description="早期通用 Flash 模型",
    input_price_per_1m=0.075,
    output_price_per_1m=0.30,
    modalities=["text", "json"],
    aliases=["3.6-flash"],
    is_promotional=True,
    promo_discount=0.5,
    promo_end_date="2026-12-31"
))

ModelRegistry.register(ModelSpec(
    model_id="gemini-3.5-flash",
    display_name="Gemini 3.5 Flash",
    family=ModelFamily.FLASH,
    description="高性价比经典主力轻快模型",
    input_price_per_1m=0.075,
    output_price_per_1m=0.30,
    modalities=["text", "json"],
    aliases=["3.5-flash"]
))

ModelRegistry.register(ModelSpec(
    model_id="gemini-3-flash-preview",
    display_name="Gemini 3 Flash (Preview)",
    family=ModelFamily.FLASH,
    description="Gemini 3代初代 Flash 预览版",
    input_price_per_1m=0.075,
    output_price_per_1m=0.30,
    modalities=["text", "json"],
    aliases=["3-flash"]
))

# 3. Flash Lite 系列文本模型 (Flash Lite Family)
ModelRegistry.register(ModelSpec(
    model_id="gemini-3.5-flash-lite",
    display_name="Gemini 3.5 Flash-Lite",
    family=ModelFamily.FLASH_LITE,
    description="超轻量极速文本模型，专为高频吞吐与亚秒级响应设计",
    input_price_per_1m=0.0375,
    output_price_per_1m=0.15,
    modalities=["text", "json"],
    aliases=["3.5-flash-lite", "3.5-lite"]
))

ModelRegistry.register(ModelSpec(
    model_id="gemini-3.1-flash-lite",
    display_name="Gemini 3.1 Flash-Lite",
    family=ModelFamily.FLASH_LITE,
    description="极低延迟轻量级 Flash-Lite 模型",
    input_price_per_1m=0.0375,
    output_price_per_1m=0.15,
    modalities=["text", "json"],
    aliases=["3.1-flash-lite", "3.1-lite"]
))

# 4. NB (Nano-Banana / Image) 系列官方 GA 图像生成模型
ModelRegistry.register(ModelSpec(
    model_id="gemini-3-pro-image",
    display_name="Gemini 3 Pro Image (Nano-Banana Pro)",
    family=ModelFamily.NANO_BANANA,
    description="NB 旗舰图像生成与编辑模型 (代号 nano-banana-pro, GA 官方模型)",
    input_price_per_1m=0.03,  # 每张图或定价
    output_price_per_1m=0.03,
    modalities=["text", "image_generation"],
    default_prompt="A cyberpunk neon cityscape at rainy midnight with flying vehicles, 8k resolution, cinematic lighting",
    is_image_model=True,
    aliases=["nano-banana-pro", "gemini-3-pro-image-preview", "nb-pro"]
))

ModelRegistry.register(ModelSpec(
    model_id="gemini-3.1-flash-image",
    display_name="Gemini 3.1 Flash Image (NB2)",
    family=ModelFamily.NANO_BANANA,
    description="快速多模态文生图模型 (NB2, GA 官方模型)",
    input_price_per_1m=0.02,
    output_price_per_1m=0.02,
    modalities=["text", "image_generation"],
    default_prompt="A cute cartoon cyberpunk robot reading a book, vibrant colors",
    is_image_model=True,
    aliases=["3.1-flash-image", "gemini-3.1-flash-image-preview", "nb-flash", "nb2"]
))

ModelRegistry.register(ModelSpec(
    model_id="gemini-3.1-flash-lite-image",
    display_name="Gemini 3.1 Flash-Lite Image (NB Lite)",
    family=ModelFamily.NANO_BANANA,
    description="轻量极速图像生成模型 (NB Lite, GA 官方模型)",
    input_price_per_1m=0.015,
    output_price_per_1m=0.015,
    modalities=["text", "image_generation"],
    default_prompt="Minimalist geometric logo of a rocket, flat vector",
    is_image_model=True,
    aliases=["3.1-lite-image", "gemini-3.1-flash-lite-image-preview", "nb-lite"]
))

# 5. Omni 系列全能多模态模型
ModelRegistry.register(ModelSpec(
    model_id="gemini-omni-flash-preview",
    display_name="Gemini Omni Flash (Preview)",
    family=ModelFamily.OMNI,
    description="全能多模态实验模型，支持跨模态实时流式交互",
    input_price_per_1m=0.10,
    output_price_per_1m=0.40,
    modalities=["text", "audio", "multimodal"],
    aliases=["omni-flash", "gemini-omni"]
))
