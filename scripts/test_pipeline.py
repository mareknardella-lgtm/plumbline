"""Gate 2 verification script: Run pipeline on specimen and verify dossier generation.

Usage:
    uv run python scripts/test_pipeline.py --specimen invoice_totals
"""

import argparse
import asyncio
import json
import sys
import uuid
from pathlib import Path

# Ensure project root is in sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from backend.app.events.bus import EventBus  # noqa: E402
from backend.app.orchestrator.pipeline import PipelineOrchestrator  # noqa: E402
from backend.app.store.db import init_db  # noqa: E402


async def main():
    parser = argparse.ArgumentParser(description="Test pipeline on a specimen")
    parser.add_argument("--specimen", default="invoice_totals", help="Specimen name")
    parser.add_argument("--mode", default="quick", choices=["quick", "thorough"], help="Run mode")
    args = parser.parse_args()

    print(f"=== Plumbline Gate 2 Test: Running pipeline on specimen '{args.specimen}' ===")

    specimen_dir = Path("backend/specimens") / args.specimen / "src"
    specimen_file = specimen_dir / f"{args.specimen}.py"

    if not specimen_file.exists():
        print(f"Error: Specimen file not found: {specimen_file}")
        sys.exit(1)

    source_code = specimen_file.read_text(encoding="utf-8")
    print(f"Loaded {len(source_code.splitlines())} lines of source code.")

    # Initialize store
    await init_db()

    event_bus = EventBus()
    orchestrator = PipelineOrchestrator(event_bus=event_bus)

    run_id = f"test-run-{uuid.uuid4().hex[:8]}"
    print(f"Created Run ID: {run_id}")

    # Subscribe to events to display live progress
    async def listen():
        async for env in event_bus.subscribe(run_id):
            t = env.type
            if t == "stage.started":
                print(f"\n[Stage {env.data.get('stage')}] Started: {env.data.get('name')}")
            elif t == "survey.report":
                print(
                    f"  -> Survey: found {env.data.get('functions_found')} functions, risks: {env.data.get('risks')}"
                )
            elif t == "pins.written":
                print(
                    f"  -> Behavior tests written: {env.data.get('count')} (coverage: {env.data.get('coverage_percent')}%)"
                )
            elif t == "mutants.planned":
                print(f"  -> Planted bugs planned: {env.data.get('total')}")
            elif t == "test_strength.updated":
                print(
                    f"  -> Test strength: {env.data.get('test_strength')} (caught {env.data.get('caught')}/{env.data.get('total')})"
                )
            elif t == "candidate.started":
                print(
                    f"  -> Candidate {env.data.get('candidate_id')} ({env.data.get('strategy')}) started..."
                )
            elif t == "candidate.result":
                print(
                    f"  -> Candidate {env.data.get('candidate_id')} result: {env.data.get('status')} ({env.data.get('tests_passed')}/{env.data.get('tests_total')} tests passed)"
                )
            elif t == "probe.result":
                div = env.data.get("divergent", 0)
                print(
                    f"  -> Probes for {env.data.get('candidate_id')}: {env.data.get('matching')}/{env.data.get('total_probes')} matching, {div} divergent"
                )
                if div > 0 and env.data.get("first_divergence"):
                    print(f"     [!] TRAP DETECTED: {env.data.get('first_divergence')}")
            elif t == "verdict":
                print(f"\n>>> VERDICT: {env.data.get('outcome').upper()}")
                print(f"    {env.data.get('sentence')}")
            elif t == "dossier.ready":
                print(f"\n[Dossier Ready] Artifacts: {env.data.get('artifacts')}")
            elif t == "run.completed":
                print(f"\n=== Run completed in {env.data.get('duration_seconds')}s ===")
                break
            elif t == "run.failed":
                print(f"\n[FAIL] Run failed: {env.data.get('reason')}")
                break

    listener_task = asyncio.create_task(listen())

    # Execute orchestrator
    evidence = await orchestrator.run(
        run_id=run_id,
        source_code=source_code,
        goal="Modernize to Python 3.12, preserve exact numerical behavior",
        mode=args.mode,
    )

    await listener_task

    # Verify dossier and evidence artifacts
    run_dir = Path("./data/runs") / run_id
    dossier_path = run_dir / "dossier.md"
    evidence_path = run_dir / "evidence.json"
    patch_path = run_dir / "refactor.patch"

    print("\n--- Verifying Artifacts ---")
    if dossier_path.exists():
        print(f" [OK] {dossier_path} exists ({dossier_path.stat().st_size} bytes)")
    else:
        print(f" [XX] Missing {dossier_path}")
        sys.exit(1)

    if evidence_path.exists():
        print(f" [OK] {evidence_path} exists ({evidence_path.stat().st_size} bytes)")
        data = json.loads(evidence_path.read_text(encoding="utf-8"))
        print(f"      Winner: {data.get('winner')}, Verdict: {data.get('verdict')}")
    else:
        print(f" [XX] Missing {evidence_path}")
        sys.exit(1)

    if patch_path.exists():
        print(f" [OK] {patch_path} exists ({patch_path.stat().st_size} bytes)")

    print("\nGate 2 Test PASSED successfully!")


if __name__ == "__main__":
    asyncio.run(main())
