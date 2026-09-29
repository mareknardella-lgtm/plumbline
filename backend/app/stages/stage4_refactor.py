from dataclasses import dataclass
from typing import Any

from backend.app.events.models import CandidateStartedData, CandidateStrategy


@dataclass
class CandidateResult:
    candidate_id: str
    strategy: str
    status: str
    iterations: int
    tests_passed: int
    tests_total: int


class Stage4Refactor:
    def __init__(self, event_bus):
        self.event_bus = event_bus

    async def run(
        self, source_code: str, goal: str, evidence: Any, mode: str
    ) -> list[CandidateResult]:
        await self.event_bus.emit(
            "candidate.started",
            CandidateStartedData(candidate_id="c1", strategy=CandidateStrategy.BALANCED),
        )
        return [
            CandidateResult(
                candidate_id="c1",
                strategy="balanced",
                status="green",
                iterations=2,
                tests_passed=10,
                tests_total=10,
            )
        ]
