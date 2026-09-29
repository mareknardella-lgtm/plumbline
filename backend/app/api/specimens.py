"""Specimen listing endpoint."""

from fastapi import APIRouter

router = APIRouter()


@router.get("/specimens")
async def list_specimens() -> dict:
    """List available bundled specimens."""
    # TODO: Phase 2
    return {"specimens": []}
