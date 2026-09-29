from dataclasses import dataclass
from typing import Any

from backend.app.events.models import DossierReadyData


@dataclass
class DossierResult:
    dossier_path: str
    patch_path: str
    pins_path: str


class Stage6Dossier:
    def __init__(self, event_bus):
        self.event_bus = event_bus

    async def run(self, evidence: Any) -> DossierResult:
        await self.event_bus.emit(
            "dossier.ready",
            DossierReadyData(
                artifacts=["dossier.md", "refactor.patch", "pins.zip", "evidence.json"]
            ),
        )
        return DossierResult(
            dossier_path="dossier.md", patch_path="refactor.patch", pins_path="pins.zip"
        )
