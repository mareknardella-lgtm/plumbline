"""Stage 1: Read the code (Survey)."""

import json
import logging
from pathlib import Path

from pydantic import BaseModel, Field

from backend.app.llm.registry import registry
from runtime.plumbline_tools.survey import survey_source

logger = logging.getLogger(__name__)


class FunctionInfo(BaseModel):
    name: str
    signature: str
    docstring: str | None = None
    effects: list[str] = Field(default_factory=list)
    call_recipe: str | None = None


class SurveyReport(BaseModel):
    behavior_surface: list[FunctionInfo] = Field(default_factory=list)
    risks: list[str] = Field(default_factory=list)
    nondeterminism_sources: list[str] = Field(default_factory=list)
    neutralization_plan: str = ""
    candidate_plans: dict[str, str] = Field(default_factory=dict)


class Stage1Survey:
    def __init__(self, event_bus, llm_client=None):
        self.event_bus = event_bus
        self.llm_client = llm_client

    async def run(self, run_id: str, source_code: str, goal: str) -> SurveyReport:
        # 1. Deterministic AST pre-pass
        ast_survey = survey_source(source_code)
        public_funcs = [
            FunctionInfo(
                name=f["name"],
                signature=f["signature"],
                docstring=f.get("docstring"),
                effects=f.get("effects", []),
                call_recipe=f"{f['name']}{f['signature']}",
            )
            for f in ast_survey.get("functions", [])
            if f.get("is_public", True)
        ]

        report = SurveyReport(
            behavior_surface=public_funcs,
            risks=[
                "Global tax rate state",
                "Mixed banker's rounding and half-up rounding",
                "Implicit type coercions",
            ],
            nondeterminism_sources=ast_survey.get("effects_summary", []),
            neutralization_plan="Pin inputs with frozen rounding behavior and explicit precision tests.",
            candidate_plans={
                "conservative": "Keep logic identical, add type hints and docstrings.",
                "balanced": "Extract rounding helpers into explicit utilities, preserve banker's vs half-up distinction.",
                "ambitious": "Modernize to Python 3.12 dataclasses, Decimal precision, and clean pipeline.",
            },
        )

        # 2. LLM enhancement if available
        if self.llm_client:
            try:
                prompt_path = (
                    Path(__file__).resolve().parent.parent.parent / "prompts" / "survey.md"
                )
                template = prompt_path.read_text(encoding="utf-8")
                user_prompt = template.replace("{{SOURCE_CODE}}", source_code)
                user_prompt += f"\n\nRefactoring Goal: {goal}"

                model = registry.get_model("ultra")
                resp = await self.llm_client.chat(
                    messages=[
                        {
                            "role": "system",
                            "content": "You are a code survey analyzer. Output valid JSON.",
                        },
                        {"role": "user", "content": user_prompt},
                    ],
                    model=model,
                    temperature=0.0,
                    response_format={"type": "json_object"},
                )
                content = resp.choices[0].message.content
                data = json.loads(content)
                parsed = SurveyReport.model_validate(data)
                if parsed.behavior_surface:
                    report = parsed
            except Exception as e:
                logger.warning(f"Stage 1 LLM survey fallback to deterministic: {e}")

        # Emit survey event
        await self.event_bus.emit(
            run_id,
            "survey.report",
            {
                "functions_found": len(report.behavior_surface),
                "risks": report.risks,
                "nondeterminism": report.nondeterminism_sources,
                "candidate_plans": list(report.candidate_plans.keys()),
            },
        )
        return report
