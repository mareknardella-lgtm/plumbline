"""Replay streaming API: unknown ids, path traversal, and the happy path.

An unknown replay used to return an empty 200 stream, which a browser
EventSource cannot distinguish from a finished replay and retries forever.
"""

import json
from pathlib import Path

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from backend.app.api.replays import router as replays_router
from backend.app.replay.engine import ReplayEngine

REPLAY_NAME = "invoice_totals_2026-09-30"

EVENTS = [
    {
        "v": 1,
        "run_id": "run-demo",
        "seq": 1,
        "ts": "2026-09-30T12:00:00Z",
        "type": "log",
        "data": {"message": "start"},
    },
    {
        "v": 1,
        "run_id": "run-demo",
        "seq": 2,
        "ts": "2026-09-30T12:00:01Z",
        "type": "dossier.ready",
        "data": {"artifacts": ["dossier.md"]},
    },
]


@pytest.fixture
def replays_dir(tmp_path: Path) -> Path:
    directory = tmp_path / "replays"
    directory.mkdir()
    lines = "\n".join(json.dumps(event) for event in EVENTS)
    (directory / f"{REPLAY_NAME}.jsonl").write_text(lines + "\n", encoding="utf-8")
    return directory


@pytest.fixture
def client(replays_dir: Path) -> TestClient:
    app = FastAPI()
    app.state.replay_engine = ReplayEngine(replays_dir=replays_dir)
    app.include_router(replays_router, prefix="/api/replays")
    return TestClient(app)


def test_missing_replay_returns_404(client: TestClient) -> None:
    """An unknown id must be a 404, not an empty 200 stream."""
    response = client.get("/api/replays/does-not-exist/events?speed=0")

    assert response.status_code == 404
    assert "does-not-exist" in response.json()["detail"]


def test_existing_replay_streams_events(client: TestClient) -> None:
    response = client.get(f"/api/replays/{REPLAY_NAME}/events?speed=0")

    assert response.status_code == 200
    assert "data:" in response.text
    assert "dossier.ready" in response.text


def test_list_replays(client: TestClient) -> None:
    response = client.get("/api/replays")

    assert response.status_code == 200
    assert REPLAY_NAME in [replay["id"] for replay in response.json()]


def test_replay_ids_cannot_escape_replays_dir(tmp_path: Path) -> None:
    """A replay id is used as a filename, so it must never resolve outside the directory."""
    engine = ReplayEngine(replays_dir=tmp_path)
    (tmp_path.parent / "secret.jsonl").write_text("{}\n", encoding="utf-8")

    assert engine.has_replay("../secret") is False
    assert engine.has_replay("..") is False
    with pytest.raises(ValueError, match="Invalid replay id"):
        engine.replay_path("../secret")


@pytest.mark.asyncio
async def test_stream_replay_rejects_traversal(tmp_path: Path) -> None:
    engine = ReplayEngine(replays_dir=tmp_path)

    with pytest.raises(FileNotFoundError):
        async for _ in engine.stream_replay("../secret", speed=0):
            pass
