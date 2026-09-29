"""Health check endpoint."""

from fastapi import APIRouter

from backend.app.settings import get_settings

router = APIRouter()


@router.get("/health")
async def health() -> dict:
    """Report service reachability, budget left and live runs available."""
    settings = get_settings()
    return {
        "status": "ok" if settings.has_api_key else "replay_only",
        "replay_only": settings.is_replay_only,
        "models_reachable": None,  # TODO: check in Phase 1
        "sandboxes_reachable": None,  # TODO: check in Phase 1
        "daily_budget_remaining_usd": settings.daily_budget_usd,  # TODO: track usage
        "live_runs_left_today": None,  # TODO: implement
    }
