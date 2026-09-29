from dataclasses import dataclass
from typing import Any

from backend.app.events.models import PinsResultData, PinsWrittenData


@dataclass
class PinsResult:
    test_count: int
    coverage: float
    baseline_checkpoint: str


class Stage2Record:
    def __init__(self, event_bus):
        self.event_bus = event_bus

    async def run(self, source_code: str, evidence: Any, mode: str) -> PinsResult:
        await self.event_bus.emit("pins.written", PinsWrittenData(count=10, coverage_percent=85.0))
        await self.event_bus.emit("pins.result", PinsResultData(total=10, passed=10, run_index=1))
        return PinsResult(test_count=10, coverage=85.0, baseline_checkpoint="checkpoint-123")
