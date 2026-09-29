"""Replay engine."""

import asyncio
import json
from collections.abc import AsyncGenerator
from pathlib import Path

from backend.app.events.models import EventEnvelope
from backend.app.settings import get_settings


class ReplayEngine:
    def __init__(self):
        settings = get_settings()
        self.replays_dir = Path(settings.data_dir).parent.parent / "backend" / "replays"
        if not self.replays_dir.exists():
            self.replays_dir.mkdir(parents=True, exist_ok=True)

    def list_replays(self) -> list[dict]:
        replays = []
        for file in self.replays_dir.glob("*.jsonl"):
            # Simple metadata extraction for demo purposes
            replays.append(
                {
                    "id": file.stem,
                    "specimen": file.stem.split("_")[0] if "_" in file.stem else "unknown",
                    "date": "2024-01-01",
                    "verdict": "unknown",
                    "duration": 0,
                }
            )
        return replays

    async def stream_replay(
        self, replay_id: str, speed: float = 1.0
    ) -> AsyncGenerator[EventEnvelope, None]:
        file_path = self.replays_dir / f"{replay_id}.jsonl"
        if not file_path.exists():
            raise FileNotFoundError(f"Replay {replay_id} not found")

        last_ts = None

        with open(file_path, encoding="utf-8") as f:
            for line in f:
                if not line.strip():
                    continue
                data = json.loads(line)
                env = EventEnvelope(**data)

                # We could sleep based on env.ts and last_ts
                # This is a simplified version
                if last_ts is not None and speed > 0:
                    await asyncio.sleep(0.01 / speed)
                last_ts = env.ts

                yield env
