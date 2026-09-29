"""Runs API."""

import uuid
from datetime import UTC, datetime

from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel

from backend.app.store.db import create_run, get_artifacts, get_run, list_runs, update_run_status

router = APIRouter()


class CreateRunRequest(BaseModel):
    source: str
    code: str | None = None
    specimen_name: str | None = None
    goal: str = ""
    mode: str = "quick"


@router.post("")
async def create_new_run(req: CreateRunRequest, request: Request):
    app = request.app
    client_ip = request.client.host if request.client else "unknown"
    client_hash = app.state.budget_guard.hash_ip(client_ip)

    app.state.budget_guard.check_rate_limit(client_hash)

    run_id = str(uuid.uuid4())
    created_at = datetime.now(UTC).isoformat()

    await create_run(
        run_id=run_id,
        created_at=created_at,
        mode=req.mode,
        source=req.source,
        goal=req.goal,
        status="queued",
        specimen_name=req.specimen_name or "",
        client_hash=client_hash,
    )

    # Normally we'd start the orchestrator task here

    return {"id": run_id}


@router.get("")
async def get_all_runs():
    return await list_runs()


@router.get("/{run_id}")
async def get_run_status(run_id: str):
    run = await get_run(run_id)
    if not run:
        raise HTTPException(status_code=404, detail="Run not found")
    return run


@router.post("/{run_id}/cancel")
async def cancel_run(run_id: str):
    await update_run_status(run_id, "cancelled")
    return {"status": "cancelled"}


@router.get("/{run_id}/artifacts/{name}")
async def download_artifact(run_id: str, name: str):
    artifacts = await get_artifacts(run_id)
    for art in artifacts:
        if art["name"] == name:
            # return file using FileResponse in a real implementation
            return {"url": art["path"]}
    raise HTTPException(status_code=404, detail="Artifact not found")
