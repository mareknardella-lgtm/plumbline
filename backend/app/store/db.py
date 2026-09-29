"""SQLite database store using aiosqlite."""

import json
import os
from pathlib import Path

import aiosqlite

from backend.app.events.models import EventEnvelope
from backend.app.settings import get_settings


def _db_path() -> Path:
    settings = get_settings()
    os.makedirs(settings.data_dir, exist_ok=True)
    return Path(settings.data_dir) / "plumbline.db"


async def init_db() -> None:
    """Initialize the database schema."""
    async with aiosqlite.connect(_db_path()) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS runs (
                id TEXT PRIMARY KEY,
                created_at TEXT,
                mode TEXT,
                source TEXT,
                goal TEXT,
                status TEXT,
                specimen_name TEXT,
                client_hash TEXT
            )
        """)
        await db.execute("""
            CREATE TABLE IF NOT EXISTS events (
                run_id TEXT,
                seq INTEGER,
                ts TEXT,
                type TEXT,
                payload_json TEXT,
                PRIMARY KEY (run_id, seq)
            )
        """)
        await db.execute("""
            CREATE TABLE IF NOT EXISTS artifacts (
                run_id TEXT,
                name TEXT,
                path TEXT,
                sha256 TEXT
            )
        """)
        await db.commit()


async def create_run(
    run_id: str,
    created_at: str,
    mode: str,
    source: str,
    goal: str,
    status: str,
    specimen_name: str,
    client_hash: str,
) -> None:
    async with aiosqlite.connect(_db_path()) as db:
        await db.execute(
            "INSERT INTO runs (id, created_at, mode, source, goal, status, specimen_name, client_hash) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (run_id, created_at, mode, source, goal, status, specimen_name, client_hash),
        )
        await db.commit()


async def update_run_status(run_id: str, status: str) -> None:
    async with aiosqlite.connect(_db_path()) as db:
        await db.execute("UPDATE runs SET status = ? WHERE id = ?", (status, run_id))
        await db.commit()


async def get_run(run_id: str) -> dict | None:
    async with aiosqlite.connect(_db_path()) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute("SELECT * FROM runs WHERE id = ?", (run_id,)) as cursor:
            row = await cursor.fetchone()
            return dict(row) if row else None


async def list_runs() -> list[dict]:
    async with aiosqlite.connect(_db_path()) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute("SELECT * FROM runs ORDER BY created_at DESC") as cursor:
            return [dict(row) for row in await cursor.fetchall()]


async def insert_event(env: EventEnvelope) -> None:
    async with aiosqlite.connect(_db_path()) as db:
        await db.execute(
            "INSERT INTO events (run_id, seq, ts, type, payload_json) VALUES (?, ?, ?, ?, ?)",
            (env.run_id, env.seq, env.ts.isoformat(), env.type, json.dumps(env.data)),
        )
        await db.commit()


async def get_events(run_id: str, after_seq: int = 0) -> list[EventEnvelope]:
    async with aiosqlite.connect(_db_path()) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute(
            "SELECT * FROM events WHERE run_id = ? AND seq > ? ORDER BY seq ASC",
            (run_id, after_seq),
        ) as cursor:
            rows = await cursor.fetchall()
            return [
                EventEnvelope(
                    run_id=r["run_id"],
                    seq=r["seq"],
                    ts=r["ts"],
                    type=r["type"],
                    data=json.loads(r["payload_json"]),
                )
                for r in rows
            ]


async def save_artifact(run_id: str, name: str, path: str, sha256: str = "") -> None:
    async with aiosqlite.connect(_db_path()) as db:
        await db.execute(
            "INSERT INTO artifacts (run_id, name, path, sha256) VALUES (?, ?, ?, ?)",
            (run_id, name, path, sha256),
        )
        await db.commit()


async def get_artifacts(run_id: str) -> list[dict]:
    async with aiosqlite.connect(_db_path()) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute("SELECT * FROM artifacts WHERE run_id = ?", (run_id,)) as cursor:
            return [dict(row) for row in await cursor.fetchall()]


async def delete_old_runs(days: int = 7) -> None:
    async with aiosqlite.connect(_db_path()) as db:
        await db.execute(
            "DELETE FROM runs WHERE created_at < datetime('now', ?)", (f"-{days} days",)
        )
        await db.commit()
