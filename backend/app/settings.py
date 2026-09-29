"""Application settings loaded from environment variables."""

from functools import lru_cache

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Plumbline configuration. All values come from .env or environment variables."""

    # Token Factory
    nebius_api_key: str = ""
    nebius_ai_project: str = ""
    token_factory_base_url: str = "https://api.tokenfactory.nebius.com/v1/"
    sandboxes_base_url: str = "https://api.tokenfactory.nebius.com/sandboxes"

    # Optional (P1)
    tavily_api_key: str = ""

    # Model overrides
    model_ultra: str = ""
    model_super: str = ""
    model_nano: str = ""
    model_fast: str = ""

    # Budgets and limits
    daily_budget_usd: float = 0.50
    run_budget_usd_quick: float = 0.60
    run_budget_usd_thorough: float = 1.50
    max_sandbox_concurrency: int = 30
    max_concurrent_runs: int = 2
    live_runs_per_ip_per_hour: int = 3

    # Operations
    replay_only: bool = False
    admin_token: str = ""
    judge_pass: str = ""
    judge_daily_budget_usd: float = 0.0
    allowed_origins: str = "http://localhost:5173"
    data_dir: str = "./data"

    @property
    def allowed_origins_list(self) -> list[str]:
        return [o.strip() for o in self.allowed_origins.split(",") if o.strip()]

    @property
    def has_api_key(self) -> bool:
        return bool(self.nebius_api_key)

    @property
    def is_replay_only(self) -> bool:
        return self.replay_only or not self.has_api_key

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}


@lru_cache
def get_settings() -> Settings:
    return Settings()
