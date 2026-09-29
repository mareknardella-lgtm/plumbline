import time
from dataclasses import dataclass, field

from backend.app.events.models import (
    RunCancelledData,
    RunFailedData,
    StageCompletedData,
    StageStartedData,
)
from backend.app.stages.stage1_survey import Stage1Survey, SurveyReport
from backend.app.stages.stage2_record import PinsResult, Stage2Record
from backend.app.stages.stage3_mutate import MutationResult, Stage3Mutate
from backend.app.stages.stage4_refactor import CandidateResult, Stage4Refactor
from backend.app.stages.stage5_compare import ComparisonResult, Stage5Compare
from backend.app.stages.stage6_dossier import DossierResult, Stage6Dossier


@dataclass
class Evidence:
    survey: SurveyReport | None = None
    pins: PinsResult | None = None
    mutations: MutationResult | None = None
    candidates: list[CandidateResult] = field(default_factory=list)
    comparison: ComparisonResult | None = None
    dossier: DossierResult | None = None


class PipelineOrchestrator:
    def __init__(self, event_bus):
        self.event_bus = event_bus
        self._cancel_flag = False

    def cancel(self):
        self._cancel_flag = True

    async def run(self, run_id: str, source_code: str, goal: str, mode: str):
        evidence = Evidence()
        stages = [
            (
                1,
                "Read the code",
                Stage1Survey(self.event_bus),
                {"source_code": source_code, "goal": goal},
            ),
            (
                2,
                "Record behavior",
                Stage2Record(self.event_bus),
                {"source_code": source_code, "evidence": evidence, "mode": mode},
            ),
            (
                3,
                "Plant bugs to test the tests",
                Stage3Mutate(self.event_bus),
                {"source_code": source_code, "evidence": evidence, "mode": mode},
            ),
            (
                4,
                "Try refactors",
                Stage4Refactor(self.event_bus),
                {"source_code": source_code, "goal": goal, "evidence": evidence, "mode": mode},
            ),
            (
                5,
                "Compare with the original",
                Stage5Compare(self.event_bus),
                {"source_code": source_code, "evidence": evidence},
            ),
            (6, "Write the dossier", Stage6Dossier(self.event_bus), {"evidence": evidence}),
        ]

        start_time = time.time()
        timeout = 360 if mode == "quick" else 720

        for stage_num, stage_name, stage_obj, kwargs in stages:
            if self._cancel_flag:
                await self.event_bus.emit(
                    "run.cancelled", RunCancelledData(reason="User cancelled")
                )
                break

            if time.time() - start_time > timeout:
                await self.event_bus.emit(
                    "run.failed", RunFailedData(reason="Timeout exceeded", stage=stage_name)
                )
                break

            await self.event_bus.emit(
                "stage.started", StageStartedData(stage=stage_num, name=stage_name)
            )
            stage_start = time.time()

            try:
                result = await stage_obj.run(**kwargs)
                if stage_num == 1:
                    evidence.survey = result
                elif stage_num == 2:
                    evidence.pins = result
                elif stage_num == 3:
                    evidence.mutations = result
                elif stage_num == 4:
                    evidence.candidates = result
                elif stage_num == 5:
                    evidence.comparison = result
                elif stage_num == 6:
                    evidence.dossier = result

                elapsed = time.time() - stage_start
                await self.event_bus.emit(
                    "stage.completed",
                    StageCompletedData(
                        stage=stage_num, name=stage_name, elapsed_seconds=elapsed, summary="Success"
                    ),
                )
            except Exception as e:
                await self.event_bus.emit(
                    "run.failed", RunFailedData(reason=str(e), stage=stage_name)
                )
                break

        return evidence
