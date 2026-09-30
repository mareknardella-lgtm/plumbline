"""Runs API."""

import asyncio
import logging
import uuid
from datetime import UTC, datetime
from pathlib import Path

from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import FileResponse
from pydantic import BaseModel

from backend.app.orchestrator.pipeline import PipelineOrchestrator
from backend.app.store.db import create_run, get_artifacts, get_run, list_runs, update_run_status

logger = logging.getLogger(__name__)
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

    source_code = req.code or ""
    if req.source == "specimen" and req.specimen_name:
        specimen_file = (
            Path(__file__).resolve().parent.parent.parent
            / "specimens"
            / req.specimen_name
            / "src"
            / f"{req.specimen_name}.py"
        )
        if specimen_file.exists():
            source_code = specimen_file.read_text(encoding="utf-8")
        else:
            logger.warning(f"Specimen file not found: {specimen_file}")

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

    # Launch orchestrator pipeline in background
    orchestrator = PipelineOrchestrator(
        event_bus=app.state.event_bus,
        llm_client=getattr(app.state, "llm_client", None),
        sandbox=getattr(app.state, "sandbox", None),
        budget_guard=getattr(app.state, "budget_guard", None),
    )

    asyncio.create_task(
        orchestrator.run(
            run_id=run_id,
            source_code=source_code,
            goal=req.goal or "Modernize and preserve behavior",
            mode=req.mode,
            specimen_name=req.specimen_name or "invoice_totals",
        )
    )

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
            p = Path(art["path"])
            if p.exists():
                return FileResponse(p, filename=name)
            return {"url": art["path"]}
    raise HTTPException(status_code=404, detail="Artifact not found")
