"""SSE endpoint for events."""

import asyncio

from fastapi import APIRouter, Request
from sse_starlette.sse import EventSourceResponse

router = APIRouter()


@router.get("/{run_id}/events")
async def get_run_events(run_id: str, request: Request):
    # Determine if it's a replay or live run
    app = request.app
    last_event_id = request.headers.get("Last-Event-ID")
    after_seq = int(last_event_id) if last_event_id and last_event_id.isdigit() else 0

    async def event_generator():
        # First yield missed events
        events = await app.state.event_bus.get_events(run_id, after_seq=after_seq)
        for env in events:
            yield {"event": "message", "id": str(env.seq), "data": env.model_dump_json()}

        # Then subscribe to new events
        subscriber = app.state.event_bus.subscribe(run_id)

        # Keepalive / Heartbeat every 15s
        async def heartbeat():
            while True:
                await asyncio.sleep(15)
                yield {"event": "ping", "data": ""}

        async def merged_stream():
            pending = {
                asyncio.create_task(anext(subscriber)): "events",
                asyncio.create_task(anext(heartbeat())): "heartbeat",
            }

            while True:
                if await request.is_disconnected():
                    break

                done, _ = await asyncio.wait(pending.keys(), return_when=asyncio.FIRST_COMPLETED)

                for task in done:
                    task_type = pending.pop(task)
                    try:
                        result = task.result()
                        if task_type == "events":
                            yield {
                                "event": "message",
                                "id": str(result.seq),
                                "data": result.model_dump_json(),
                            }
                            pending[asyncio.create_task(anext(subscriber))] = "events"
                        else:
                            yield result
                            pending[asyncio.create_task(anext(heartbeat()))] = "heartbeat"
                    except StopAsyncIteration:
                        pass
                    except Exception:
                        pass

        async for item in merged_stream():
            yield item

    return EventSourceResponse(
        event_generator(), headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"}
    )
