"""Replays API."""

from fastapi import APIRouter, Request
from sse_starlette.sse import EventSourceResponse

router = APIRouter()


@router.get("")
async def list_available_replays(request: Request):
    engine = request.app.state.replay_engine
    return engine.list_replays()


@router.get("/{replay_id}/events")
async def stream_replay_events(replay_id: str, request: Request, speed: float = 1.0):
    engine = request.app.state.replay_engine

    async def event_generator():
        try:
            async for env in engine.stream_replay(replay_id, speed):
                if await request.is_disconnected():
                    break
                yield {"event": env.type, "id": str(env.seq), "data": env.model_dump_json()}
        except FileNotFoundError:
            pass  # In real app handle properly

    return EventSourceResponse(
        event_generator(), headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"}
    )
