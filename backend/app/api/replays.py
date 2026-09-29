"""Replay endpoints."""

from fastapi import APIRouter

router = APIRouter()


@router.get("/replays")
async def list_replays() -> dict:
    """List available recorded replays."""
    # TODO: Phase 2
    return {"replays": []}
