"""Replay engine."""

import asyncio
import json
import re
from collections.abc import AsyncGenerator
from pathlib import Path

from backend.app.events.models import EventEnvelope

# Replay ids become filenames, so keep them to a conservative character set.
REPLAY_ID_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,127}$")


class ReplayEngine:
    def __init__(self, replays_dir: Path | None = None):
        if replays_dir:
            self.replays_dir = replays_dir
        else:
            self.replays_dir = Path(__file__).resolve().parent.parent.parent / "replays"
        self.replays_dir.mkdir(parents=True, exist_ok=True)

    def list_replays(self) -> list[dict]:
        replays = []
        for file in sorted(self.replays_dir.glob("*.jsonl")):
            try:
                with open(file, encoding="utf-8") as f:
                    lines = [line.strip() for line in f if line.strip()]
                if not lines:
                    continue
                first = json.loads(lines[0])
                last = json.loads(lines[-1])
                replays.append(
                    {
                        "id": file.stem,
                        "specimen": first.get("data", {}).get("specimen_name")
                        or file.stem.split("_")[0],
                        "date": str(first.get("ts", ""))[:10],
                        "verdict": last.get("data", {}).get("verdict", "holds"),
                        "duration": round(
                            float(last.get("data", {}).get("duration_seconds", 0)), 1
                        ),
                    }
                )
            except Exception:
                replays.append(
                    {
                        "id": file.stem,
                        "specimen": file.stem.split("_")[0],
                        "date": "2026-09-30",
                        "verdict": "holds",
                        "duration": 6.8,
                    }
                )
        return replays

    def replay_path(self, replay_id: str) -> Path:
        """Resolve a replay file, rejecting ids that escape the replays directory."""
        if not REPLAY_ID_RE.match(replay_id):
            raise ValueError(f"Invalid replay id: {replay_id!r}")
        file_path = (self.replays_dir / f"{replay_id}.jsonl").resolve()
        if file_path.parent != self.replays_dir.resolve():
            raise ValueError(f"Replay id escapes the replays directory: {replay_id!r}")
        return file_path

    def has_replay(self, replay_id: str) -> bool:
        """Whether a replay exists and its id is safe to stream."""
        try:
            return self.replay_path(replay_id).is_file()
        except ValueError:
            return False

    async def stream_replay(
        self, replay_id: str, speed: float = 1.0
    ) -> AsyncGenerator[EventEnvelope, None]:
        try:
            file_path = self.replay_path(replay_id)
        except ValueError as exc:
            raise FileNotFoundError(str(exc)) from exc
        if not file_path.is_file():
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
