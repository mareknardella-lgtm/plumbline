"""Run management endpoints."""

from fastapi import APIRouter

router = APIRouter()


@router.post("/runs")
async def create_run() -> dict:
    """Start a new pipeline run."""
    # TODO: Phase 1
    return {"run_id": "placeholder", "status": "not_implemented"}


@router.get("/runs/{run_id}")
async def get_run(run_id: str) -> dict:
    """Get run status and metadata."""
    # TODO: Phase 1
    return {"run_id": run_id, "status": "not_implemented"}
