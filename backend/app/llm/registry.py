"""Model registry."""

from backend.app.settings import get_settings


class ModelRegistry:
    TIERS = {
        "ultra": "Complex reasoning and architecture",
        "super": "Main coding workhorse",
        "nano": "Fast simple operations",
        "fast": "Lightning fast parsing",
    }

    DEFAULT_MODELS = {
        "ultra": "nvidia/Nemotron-3-Ultra-550b-a55b",
        "super": "nvidia/nemotron-3-super-120b-a12b",
        "nano": "nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B",
        "fast": "nvidia/Nemotron-3_5-Lightning",
    }

    FALLBACK_CHAIN = {"ultra": "super", "super": "nano", "nano": "fast", "fast": "fast"}

    def __init__(self):
        self.pricing: dict[str, dict[str, float]] = {}
        self.context_lengths: dict[str, int] = {}
        self.rate_limits: dict[str, dict] = {}

    async def discover(self, client) -> None:
        try:
            # We assume client is an AsyncOpenAI instance
            response = await client.models.list(extra_query={"verbose": "true"})
            for model in response.data:
                # Store any pricing/limits metadata if provided in model extra fields
                # Defaulting to placeholders as the exact API payload from nebius is mock/unknown here
                self.pricing[model.id] = {"input": 0.001, "output": 0.002}
                self.context_lengths[model.id] = 8192
        except Exception:
            # Fallback to defaults
            pass

    def get_model(self, tier: str) -> str:
        settings = get_settings()
        override = getattr(settings, f"model_{tier}", "")
        if override:
            return override
        return self.DEFAULT_MODELS.get(tier, self.DEFAULT_MODELS["super"])

    def get_fallback(self, tier: str) -> str:
        fallback_tier = self.FALLBACK_CHAIN.get(tier, "super")
        return self.get_model(fallback_tier)


registry = ModelRegistry()
