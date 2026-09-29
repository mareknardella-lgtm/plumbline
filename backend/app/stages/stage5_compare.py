from dataclasses import dataclass
from typing import Any

from backend.app.events.models import VerdictData, VerdictOutcome


@dataclass
class ComparisonResult:
    drift_score: float
    verdict: str


class Stage5Compare:
    def __init__(self, event_bus):
        self.event_bus = event_bus

    async def run(self, source_code: str, evidence: Any) -> ComparisonResult:
        await self.event_bus.emit(
            "verdict", VerdictData(outcome=VerdictOutcome.HOLDS, test_strength=0.9)
        )
        return ComparisonResult(drift_score=0.0, verdict="holds")
