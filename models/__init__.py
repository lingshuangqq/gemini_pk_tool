from .gemini_3_1_flash_lite import FlashLiteTextTester
from .gemini_3_1_pro_preview import ProTextTester
from .gemini_3_1_flash_lite_image import FlashLiteImageTester
from .gemini_3_1_flash_image import FlashImageTester
from .gemini_3_pro_image import ProImageTester
from .gemini_3_5_flash import Gemini35FlashTester
from .gemini_omni_flash_preview import GeminiOmniFlashTester
from .gemini_3_6_flash import Gemini36FlashTester
from .gemini_3_7_flash import Gemini37FlashTester
from .gemini_3_8_flash import Gemini38FlashTester
from .gemini_3_5_flash_lite import Gemini35FlashLiteTester
from .gemini_2_5_flash_image import Gemini25FlashImageTester
from .gemini_3_flash_preview import Gemini3FlashPreviewTester

MODEL_REGISTRY = {
    "gemini-3.1-flash-lite": FlashLiteTextTester,
    "gemini-3.1-pro-preview": ProTextTester,
    "gemini-3.1-flash-lite-image": FlashLiteImageTester,
    "gemini-3.1-flash-image": FlashImageTester,
    "gemini-3-pro-image": ProImageTester,
    "gemini-3.5-flash": Gemini35FlashTester,
    "gemini-omni-flash-preview": GeminiOmniFlashTester,
    "gemini-3.6-flash": Gemini36FlashTester,
    "gemini-3.7-flash": Gemini37FlashTester,
    "gemini-3.8-flash": Gemini38FlashTester,
    "gemini-3.5-flash-lite": Gemini35FlashLiteTester,
    "gemini-2.5-flash-image": Gemini25FlashImageTester,
    "gemini-3-flash-preview": Gemini3FlashPreviewTester,
}

def get_tester_class(model_id):
    """
    Returns the specific model tester strategy class for the given model_id.
    """
    return MODEL_REGISTRY.get(model_id)

def list_registered_models():
    """
    Lists all currently registered model IDs.
    """
    return list(MODEL_REGISTRY.keys())
