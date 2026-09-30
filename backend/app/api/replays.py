"""Replays API."""

import logging

from fastapi import APIRouter, HTTPException, Request
from sse_starlette.sse import EventSourceResponse

from backend.app.events.models import EventEnvelope, RunFailedData

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("")
async def list_available_replays(request: Request):
    engine = request.app.state.replay_engine
    return engine.list_replays()


@router.get("/{replay_id}/events")
async def stream_replay_events(replay_id: str, request: Request, speed: float = 1.0):
    engine = request.app.state.replay_engine

    # Validate before opening the stream: once the response starts we can no
    # longer set a status code, and an empty 200 body makes EventSource
    # reconnect forever against an id that will never resolve.
    if not engine.has_replay(replay_id):
        raise HTTPException(status_code=404, detail=f"Replay '{replay_id}' not found")

    async def event_generator():
        try:
            async for env in engine.stream_replay(replay_id, speed):
                if await request.is_disconnected():
                    break
                yield {"event": "message", "id": str(env.seq), "data": env.model_dump_json()}
        except FileNotFoundError as exc:
            # The replay file vanished mid-stream. Report it instead of
            # ending the stream silently, which looks like a successful run.
            logger.warning("Replay '%s' disappeared mid-stream: %s", replay_id, exc)
            failure = EventEnvelope(
                run_id=replay_id,
                seq=0,
                type="run.failed",
                data=RunFailedData(
                    reason=f"Replay '{replay_id}' is no longer available"
                ).model_dump(mode="json"),
            )
            yield {"event": "message", "data": failure.model_dump_json()}

    return EventSourceResponse(
        event_generator(), headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"}
    )
