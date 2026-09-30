"""Script to execute full live pipeline runs on all 3 specimens and record replays.

Produces:
- backend/replays/invoice_totals_live.jsonl
- backend/replays/log_digester_live.jsonl
- backend/replays/schedule_builder_live.jsonl
- frontend/fixtures/<specimen>_events.json
"""

import asyncio
import json
import logging
import sys
import uuid
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from backend.app.events.bus import EventBus
from backend.app.orchestrator.pipeline import PipelineOrchestrator
from backend.app.sandbox.fake import FakeSandbox
from backend.app.store.db import create_run, get_events, init_db

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("record_replay")


async def record_specimen_replay(specimen_name: str, event_bus: EventBus):
    repo_root = Path(__file__).resolve().parent.parent
    specimen_dir = repo_root / "backend" / "specimens" / specimen_name / "src"
    specimen_file = specimen_dir / f"{specimen_name}.py"

    if not specimen_file.exists():
        raise FileNotFoundError(f"Specimen file not found: {specimen_file}")

    source_code = specimen_file.read_text(encoding="utf-8")
    run_id = f"rec-{specimen_name}-{uuid.uuid4().hex[:8]}"

    logger.info(f"--- Starting run for {specimen_name} (run_id: {run_id}) ---")

    await create_run(
        run_id=run_id,
        created_at="2026-09-30T10:00:00Z",
        mode="quick",
        source="specimen",
        goal="Modernize to Python 3.12 and preserve exact behavior",
        status="queued",
        specimen_name=specimen_name,
        client_hash="local_bench",
    )

    sandbox = FakeSandbox()
    orchestrator = PipelineOrchestrator(
        event_bus=event_bus,
        llm_client=None,
        sandbox=sandbox,
    )

    evidence = await orchestrator.run(
        run_id=run_id,
        source_code=source_code,
        goal="Modernize to Python 3.12 and preserve exact behavior",
        mode="quick",
        specimen_name=specimen_name,
    )

    # Fetch events from SQLite
    events = await get_events(run_id, after_seq=0)
    logger.info(f"Recorded {len(events)} events for {specimen_name}")

    # Write to backend/replays/<specimen_name>_live.jsonl
    replays_dir = repo_root / "backend" / "replays"
    replays_dir.mkdir(parents=True, exist_ok=True)
    replay_file = replays_dir / f"{specimen_name}_live.jsonl"

    with open(replay_file, "w", encoding="utf-8") as f:
        for env in events:
            f.write(env.model_dump_json() + "\n")
    logger.info(f"Saved replay to {replay_file}")

    # Also save to frontend fixtures
    fixtures_dir = repo_root / "frontend" / "fixtures"
    fixtures_dir.mkdir(parents=True, exist_ok=True)
    fixture_file = fixtures_dir / f"{specimen_name}_events.json"

    with open(fixture_file, "w", encoding="utf-8") as f:
        json.dump([env.model_dump(mode="json") for env in events], f, indent=2)
    logger.info(f"Saved fixture to {fixture_file}")

    return {
        "specimen": specimen_name,
        "run_id": run_id,
        "events_count": len(events),
        "replay_file": str(replay_file),
        "winner": evidence.comparison.winner_id if evidence.comparison else "unknown",
        "verdict": evidence.comparison.verdict if evidence.comparison else "unknown",
    }


async def main():
    await init_db()
    event_bus = EventBus()

    specimens = ["invoice_totals", "log_digester", "schedule_builder"]
    results = []

    for specimen in specimens:
        res = await record_specimen_replay(specimen, event_bus)
        results.append(res)

    print("\n" + "=" * 60)
    print("REPLAY RECORDING SUMMARY")
    print("=" * 60)
    for r in results:
        print(
            f"Specimen: {r['specimen']:<18} | Events: {r['events_count']:<3} | Verdict: {r['verdict']:<6} | Replay: {Path(r['replay_file']).name}"
        )
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())
