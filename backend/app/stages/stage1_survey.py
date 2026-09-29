from pydantic import BaseModel, Field


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
    def __init__(self, event_bus):
        self.event_bus = event_bus

    async def run(self, source_code: str, goal: str) -> SurveyReport:
        # Placeholder for real sandbox interaction and model call
        return SurveyReport(
            behavior_surface=[
                FunctionInfo(name="main", signature="def main():", effects=["print"])
            ],
            candidate_plans={"conservative": "x", "balanced": "y", "ambitious": "z"},
        )
