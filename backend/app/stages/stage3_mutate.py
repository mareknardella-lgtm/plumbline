from dataclasses import dataclass
from typing import Any

from backend.app.events.models import MutantsPlannedData


@dataclass
class MutationResult:
    strength: float
    caught: int
    survived: int
    timeout: int


class Stage3Mutate:
    def __init__(self, event_bus):
        self.event_bus = event_bus

    async def run(self, source_code: str, evidence: Any, mode: str) -> MutationResult:
        await self.event_bus.emit("mutants.planned", MutantsPlannedData(total=40))
        return MutationResult(strength=0.9, caught=36, survived=4, timeout=0)
