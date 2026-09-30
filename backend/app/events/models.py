"""Pydantic models for every SSE event type.

These are the single source of truth for the event protocol (§8).
TypeScript types are generated from these via scripts/gen_types.py.
"""

from __future__ import annotations

from datetime import UTC, datetime
from enum import StrEnum
from typing import Any, Literal

from pydantic import BaseModel, Field

# ---------------------------------------------------------------------------
# Envelope
# ---------------------------------------------------------------------------


class EventEnvelope(BaseModel):
    """SSE event envelope. The UI is a pure function of a stream of these."""

    v: Literal[1] = 1
    run_id: str
    seq: int
    ts: datetime = Field(default_factory=lambda: datetime.now(UTC))
    type: str
    data: dict[str, Any] = Field(default_factory=dict)


# ---------------------------------------------------------------------------
# Run lifecycle
# ---------------------------------------------------------------------------


class RunStatus(StrEnum):
    QUEUED = "queued"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class RunQueuedData(BaseModel):
    position: int = 1
    estimated_wait_seconds: int | None = None


class RunStartedData(BaseModel):
    mode: Literal["quick", "thorough"] = "quick"
    source_type: Literal["paste", "specimen", "zip"] = "specimen"
    specimen_name: str | None = None
    goal: str = ""


class RunFailedData(BaseModel):
    reason: str
    stage: str | None = None


class RunCancelledData(BaseModel):
    reason: str = "User cancelled"


class RunCompletedData(BaseModel):
    duration_seconds: float = 0.0
    verdict: str = "holds"
    winner_id: str | None = None


# ---------------------------------------------------------------------------
# Stage lifecycle
# ---------------------------------------------------------------------------


class StageStatus(StrEnum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    SKIPPED = "skipped"


STAGE_NAMES = [
    "Read the code",
    "Record behavior",
    "Plant bugs to test the tests",
    "Try refactors",
    "Compare with the original",
    "Write the dossier",
]


class StageStartedData(BaseModel):
    stage: int = Field(ge=1, le=6)
    name: str = ""


class StageCompletedData(BaseModel):
    stage: int = Field(ge=1, le=6)
    name: str = ""
    summary: str = ""
    elapsed_seconds: float = 0.0


# ---------------------------------------------------------------------------
# Log
# ---------------------------------------------------------------------------


class LogData(BaseModel):
    message: str
    level: Literal["info", "warn", "error"] = "info"
    stage: int | None = None


# ---------------------------------------------------------------------------
# LLM call
# ---------------------------------------------------------------------------


class LLMCallData(BaseModel):
    model: str
    tier: Literal["ultra", "super", "nano", "fast", "fallback"] = "super"
    tokens_in: int = 0
    tokens_out: int = 0
    latency_ms: int = 0
    retries: int = 0
    cost_estimate_usd: float = 0.0
    stage: int | None = None


# ---------------------------------------------------------------------------
# Sandbox operation
# ---------------------------------------------------------------------------


class SandboxOpData(BaseModel):
    op_type: Literal["run", "fork", "checkpoint", "rollback", "apply_files"] = "run"
    op_id: str = ""
    checkpoint_uuid: str | None = None
    exit_code: int | None = None
    duration_ms: int = 0
    cpu_percent: float | None = None
    memory_mb: float | None = None
    stage: int | None = None


# ---------------------------------------------------------------------------
# Stage 2: Behavior tests (pins)
# ---------------------------------------------------------------------------


class PinsWrittenData(BaseModel):
    count: int = 0
    coverage_percent: float | None = None


class PinsResultData(BaseModel):
    total: int = 0
    passed: int = 0
    failed: int = 0
    flaky: int = 0
    run_index: int = 1  # 1 or 2 (two fresh runs)


# ---------------------------------------------------------------------------
# Stage 3: Planted bugs (mutants / tripwires)
# ---------------------------------------------------------------------------


class MutantsPlannedData(BaseModel):
    total: int = 0
    by_function: dict[str, int] = Field(default_factory=dict)


class MutantResultStatus(StrEnum):
    CAUGHT = "caught"
    SURVIVED = "survived"
    TIMEOUT = "timeout"
    ERROR = "error"


class MutantResultData(BaseModel):
    index: int = 0
    function_name: str = ""
    operator: str = ""
    status: MutantResultStatus = MutantResultStatus.CAUGHT
    line: int | None = None


class StrengthenRoundData(BaseModel):
    round_number: int = 1
    survivors_targeted: int = 0
    tests_added: int = 0
    new_strength: float = 0.0


# ---------------------------------------------------------------------------
# Stage 4: Candidates
# ---------------------------------------------------------------------------


class CandidateStrategy(StrEnum):
    CONSERVATIVE = "conservative"
    BALANCED = "balanced"
    AMBITIOUS = "ambitious"


class CandidateStartedData(BaseModel):
    candidate_id: str = ""
    strategy: CandidateStrategy = CandidateStrategy.BALANCED
    model_tier: str = "super"


class CandidateIterationData(BaseModel):
    candidate_id: str = ""
    iteration: int = 1
    tests_passed: int = 0
    tests_failed: int = 0
    action: str = ""  # e.g. "wrote refactored code", "repaired from failure"


class CandidateResultStatus(StrEnum):
    GREEN = "green"
    RED = "red"
    ERROR = "error"


class CandidateResultData(BaseModel):
    candidate_id: str = ""
    strategy: CandidateStrategy = CandidateStrategy.BALANCED
    status: CandidateResultStatus = CandidateResultStatus.GREEN
    iterations: int = 0
    tests_passed: int = 0
    tests_total: int = 0
    summary: str = ""


# ---------------------------------------------------------------------------
# Stage 5: Probes and comparison
# ---------------------------------------------------------------------------


class ProbeResultData(BaseModel):
    candidate_id: str = ""
    total_probes: int = 0
    matching: int = 0
    divergent: int = 0
    excluded: int = 0
    first_divergence: dict[str, Any] | None = None  # {input, expected, actual}


# ---------------------------------------------------------------------------
# Verdict
# ---------------------------------------------------------------------------


class VerdictOutcome(StrEnum):
    HOLDS = "holds"
    NO_HOLD = "no_hold"
    PARTIAL = "partial"


class VerdictData(BaseModel):
    outcome: VerdictOutcome = VerdictOutcome.NO_HOLD
    winner_id: str | None = None
    winner_strategy: CandidateStrategy | None = None
    sentence: str = ""
    test_strength: float = 0.0
    behavior_tests_total: int = 0
    behavior_tests_passed: int = 0
    planted_bugs_total: int = 0
    planted_bugs_caught: int = 0
    probes_total: int = 0
    probes_matching: int = 0
    api_surface_changed: bool = False
    complexity_before: int | None = None
    complexity_after: int | None = None
    lines_before: int | None = None
    lines_after: int | None = None


# ---------------------------------------------------------------------------
# Dossier ready
# ---------------------------------------------------------------------------


class DossierReadyData(BaseModel):
    artifacts: list[str] = Field(default_factory=list)
    # e.g. ["dossier.md", "refactor.patch", "pins.zip", "evidence.json"]


# ---------------------------------------------------------------------------
# Budget warning
# ---------------------------------------------------------------------------


class BudgetWarningData(BaseModel):
    resource: Literal["tokens", "dollars", "time", "sandbox_ops"] = "dollars"
    used: float = 0.0
    limit: float = 0.0
    message: str = ""


# ---------------------------------------------------------------------------
# Event type registry
# ---------------------------------------------------------------------------

EVENT_DATA_MODELS: dict[str, type[BaseModel]] = {
    "run.queued": RunQueuedData,
    "run.started": RunStartedData,
    "run.failed": RunFailedData,
    "run.cancelled": RunCancelledData,
    "stage.started": StageStartedData,
    "stage.completed": StageCompletedData,
    "log": LogData,
    "llm.call": LLMCallData,
    "sandbox.op": SandboxOpData,
    "pins.written": PinsWrittenData,
    "pins.result": PinsResultData,
    "mutants.planned": MutantsPlannedData,
    "mutant.result": MutantResultData,
    "strengthen.round": StrengthenRoundData,
    "candidate.started": CandidateStartedData,
    "candidate.iteration": CandidateIterationData,
    "candidate.result": CandidateResultData,
    "probe.result": ProbeResultData,
    "verdict": VerdictData,
    "dossier.ready": DossierReadyData,
    "budget.warning": BudgetWarningData,
}
