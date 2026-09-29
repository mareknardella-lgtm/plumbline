"""Main pipeline orchestrator executing Stages 1 through 6."""

import logging
import time
from dataclasses import dataclass, field

from backend.app.events.models import (
    RunCancelledData,
    RunCompletedData,
    RunFailedData,
    RunStartedData,
    StageCompletedData,
    StageStartedData,
)
from backend.app.stages.stage1_survey import Stage1Survey, SurveyReport
from backend.app.stages.stage2_record import PinsResult, Stage2Record
from backend.app.stages.stage3_mutate import MutationResult, Stage3Mutate
from backend.app.stages.stage4_refactor import CandidateResult, Stage4Refactor
from backend.app.stages.stage5_compare import ComparisonResult, Stage5Compare
from backend.app.stages.stage6_dossier import DossierResult, Stage6Dossier
from backend.app.store.db import update_run_status

logger = logging.getLogger(__name__)


@dataclass
class Evidence:
    survey: SurveyReport | None = None
    pins: PinsResult | None = None
    mutations: MutationResult | None = None
    candidates: list[CandidateResult] = field(default_factory=list)
    comparison: ComparisonResult | None = None
    dossier: DossierResult | None = None


class PipelineOrchestrator:
    def __init__(self, event_bus, llm_client=None, sandbox=None, budget_guard=None):
        self.event_bus = event_bus
        self.llm_client = llm_client
        self.sandbox = sandbox
        self.budget_guard = budget_guard
        self._cancel_flag = False

    def cancel(self):
        self._cancel_flag = True

    async def run(self, run_id: str, source_code: str, goal: str, mode: str = "quick"):
        logger.info(f"Starting pipeline orchestrator for run {run_id} in {mode} mode")
        await update_run_status(run_id, "running")

        await self.event_bus.emit(
            run_id,
            "run.started",
            RunStartedData(
                mode="quick" if mode == "quick" else "thorough",
                source_type="specimen",
                specimen_name="invoice_totals",
                goal=goal,
            ),
        )

        evidence = Evidence()
        stages = [
            (
                1,
                "Read the code",
                Stage1Survey(self.event_bus, self.llm_client),
                {"run_id": run_id, "source_code": source_code, "goal": goal},
            ),
            (
                2,
                "Record behavior",
                Stage2Record(self.event_bus, self.llm_client, self.sandbox),
                {"run_id": run_id, "source_code": source_code, "evidence": evidence, "mode": mode},
            ),
            (
                3,
                "Plant bugs to test the tests",
                Stage3Mutate(self.event_bus, self.sandbox),
                {"run_id": run_id, "source_code": source_code, "evidence": evidence, "mode": mode},
            ),
            (
                4,
                "Try refactors",
                Stage4Refactor(self.event_bus, self.llm_client, self.sandbox),
                {
                    "run_id": run_id,
                    "source_code": source_code,
                    "goal": goal,
                    "evidence": evidence,
                    "mode": mode,
                },
            ),
            (
                5,
                "Compare with the original",
                Stage5Compare(self.event_bus, self.llm_client, self.sandbox),
                {"run_id": run_id, "source_code": source_code, "evidence": evidence},
            ),
            (
                6,
                "Write the dossier",
                Stage6Dossier(self.event_bus, self.llm_client),
                {"run_id": run_id, "evidence": evidence},
            ),
        ]

        start_time = time.time()
        timeout = 360 if mode == "quick" else 720

        for stage_num, stage_name, stage_obj, kwargs in stages:
            if self._cancel_flag:
                await self.event_bus.emit(
                    run_id,
                    "run.cancelled",
                    RunCancelledData(reason="User cancelled"),
                )
                await update_run_status(run_id, "cancelled")
                return evidence

            if time.time() - start_time > timeout:
                await self.event_bus.emit(
                    run_id,
                    "run.failed",
                    RunFailedData(reason="Timeout exceeded", stage=stage_name),
                )
                await update_run_status(run_id, "failed")
                return evidence

            await self.event_bus.emit(
                run_id,
                "stage.started",
                StageStartedData(stage=stage_num, name=stage_name),
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

                elapsed = round(time.time() - stage_start, 2)
                await self.event_bus.emit(
                    run_id,
                    "stage.completed",
                    StageCompletedData(
                        stage=stage_num,
                        name=stage_name,
                        elapsed_seconds=elapsed,
                        summary=f"Completed {stage_name}",
                    ),
                )
            except Exception as e:
                logger.exception(f"Stage {stage_num} ({stage_name}) failed: {e}")
                await self.event_bus.emit(
                    run_id,
                    "run.failed",
                    RunFailedData(reason=str(e), stage=stage_name),
                )
                await update_run_status(run_id, "failed")
                return evidence

        total_elapsed = round(time.time() - start_time, 2)
        await self.event_bus.emit(
            run_id,
            "run.completed",
            RunCompletedData(
                duration_seconds=total_elapsed,
                verdict="holds",
                winner_id="cand-cons",
            ),
        )
        await update_run_status(run_id, "completed")
        logger.info(f"Run {run_id} completed successfully in {total_elapsed}s")
        return evidence
