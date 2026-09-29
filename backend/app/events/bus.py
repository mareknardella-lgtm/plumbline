"""Async event bus for run events."""

import asyncio
from collections.abc import AsyncGenerator
from typing import Any

from backend.app.events.models import EventEnvelope
from backend.app.store.db import get_events, insert_event


class EventBus:
    """Async event bus that stores and broadcasts events."""

    def __init__(self):
        self._subscribers: dict[str, set[asyncio.Queue[EventEnvelope]]] = {}
        self._seqs: dict[str, int] = {}
        self._lock = asyncio.Lock()

    async def emit(self, run_id: str, event_type: str, data: Any) -> None:
        """Emit an event, store it, and broadcast."""
        async with self._lock:
            seq = self._seqs.get(run_id, 0) + 1
            self._seqs[run_id] = seq

        payload = data.model_dump(mode="json") if hasattr(data, "model_dump") else data
        env = EventEnvelope(run_id=run_id, seq=seq, type=event_type, data=payload)

        # Store in DB
        await insert_event(env)

        # Broadcast
        async with self._lock:
            subs = self._subscribers.get(run_id, set())
            for q in subs:
                await q.put(env)

    async def subscribe(self, run_id: str) -> AsyncGenerator[EventEnvelope, None]:
        """Subscribe to events for a given run_id."""
        q: asyncio.Queue[EventEnvelope] = asyncio.Queue()
        async with self._lock:
            if run_id not in self._subscribers:
                self._subscribers[run_id] = set()
            self._subscribers[run_id].add(q)

        try:
            while True:
                yield await q.get()
        finally:
            async with self._lock:
                self._subscribers[run_id].discard(q)
                if not self._subscribers[run_id]:
                    del self._subscribers[run_id]

    async def get_events(self, run_id: str, after_seq: int = 0) -> list[EventEnvelope]:
        """Get past events from the store."""
        return await get_events(run_id, after_seq)
