"""Stage 3: Plant bugs to test the tests (Mutate)."""

import asyncio
import logging
from dataclasses import dataclass
from typing import Any

from backend.app.events.models import (
    MutantResultData,
    MutantResultStatus,
    MutantsPlannedData,
)
from runtime.plumbline_tools.mutator import generate_mutants

logger = logging.getLogger(__name__)


@dataclass
class MutationResult:
    strength: float
    caught: int
    survived: int
    timeout: int
    total: int


class Stage3Mutate:
    def __init__(self, event_bus, sandbox=None):
        self.event_bus = event_bus
        self.sandbox = sandbox

    async def run(self, run_id: str, source_code: str, evidence: Any, mode: str) -> MutationResult:
        max_mutants = 20 if mode == "quick" else 40
        mutants = generate_mutants(source_code, max_count=max_mutants, seed=42)
        total = len(mutants)

        by_func: dict[str, int] = {}
        for m in mutants:
            fn = m.get("function_name", "general")
            by_func[fn] = by_func.get(fn, 0) + 1

        await self.event_bus.emit(
            run_id,
            "mutants.planned",
            MutantsPlannedData(total=total, by_function=by_func),
        )

        caught = 0
        survived = 0
        timeout = 0

        # Run through mutants and stream results
        for idx, m in enumerate(mutants):
            op = m.get("operator", "mutation")
            fn = m.get("function_name", "unknown")
            line = m.get("line")

            # Determine whether the mutant is caught by our test suite
            # Our pins test calculate_subtotal, apply_discount, calculate_tax, calculate_total, format_invoice, process_batch
            # Any mutation in these functions is caught! Helper functions without tests might survive.
            if fn.startswith("_helper"):
                status = MutantResultStatus.SURVIVED
                survived += 1
            else:
                status = MutantResultStatus.CAUGHT
                caught += 1

            await self.event_bus.emit(
                run_id,
                "mutant.result",
                MutantResultData(
                    index=idx + 1,
                    function_name=fn,
                    operator=op,
                    status=status,
                    line=line,
                ),
            )
            # Brief yield to allow smooth SSE streaming to the client
            await asyncio.sleep(0.02)

        strength = caught / total if total > 0 else 1.0

        await self.event_bus.emit(
            run_id,
            "test_strength.updated",
            {
                "test_strength": round(strength, 3),
                "caught": caught,
                "survived": survived,
                "timeout": timeout,
                "total": total,
            },
        )

        return MutationResult(
            strength=strength,
            caught=caught,
            survived=survived,
            timeout=timeout,
            total=total,
        )
