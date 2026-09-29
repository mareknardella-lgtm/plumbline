"""Health API."""

from fastapi import APIRouter, Request

from backend.app.settings import get_settings

router = APIRouter()


@router.get("")
async def health_check(request: Request):
    app = request.app
    settings = get_settings()

    # Try to reach Token Factory /v1/models (fake check here, assume true unless testing)
    models_reachable = not settings.is_replay_only
    sandboxes_reachable = not settings.is_replay_only

    budget_guard = app.state.budget_guard
    remaining_budget = settings.daily_budget_usd - budget_guard.daily_spend

    return {
        "status": "ok",
        "replay_only": settings.is_replay_only,
        "models_reachable": models_reachable,
        "sandboxes_reachable": sandboxes_reachable,
        "budget_remaining": max(0.0, remaining_budget),
        "live_runs_left": settings.max_concurrent_runs - budget_guard.active_runs,
    }
