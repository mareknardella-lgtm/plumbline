"""Stage 4: Try refactors (Candidates)."""

import asyncio
import logging
from dataclasses import dataclass
from typing import Any

from backend.app.events.models import (
    CandidateIterationData,
    CandidateResultData,
    CandidateResultStatus,
    CandidateStartedData,
    CandidateStrategy,
)

logger = logging.getLogger(__name__)


@dataclass
class CandidateResult:
    candidate_id: str
    strategy: str
    status: str
    iterations: int
    tests_passed: int
    tests_total: int
    code: str
    diff: str = ""
    summary: str = ""


class Stage4Refactor:
    def __init__(self, event_bus, llm_client=None, sandbox=None):
        self.event_bus = event_bus
        self.llm_client = llm_client
        self.sandbox = sandbox

    async def run(
        self, run_id: str, source_code: str, goal: str, evidence: Any, mode: str
    ) -> list[CandidateResult]:
        candidates: list[CandidateResult] = []

        # Candidate A: Conservative (Respects banker's vs half-up tax rounding, adds type hints)
        cand_a_id = "cand-cons"
        await self.event_bus.emit(
            run_id,
            "candidate.started",
            CandidateStartedData(
                candidate_id=cand_a_id,
                strategy=CandidateStrategy.CONSERVATIVE,
                model_tier="nano",
            ),
        )
        await asyncio.sleep(0.1)

        await self.event_bus.emit(
            run_id,
            "candidate.iteration",
            CandidateIterationData(
                candidate_id=cand_a_id,
                iteration=1,
                tests_passed=10,
                tests_failed=0,
                action="Added type hints and preserved exact rounding behavior",
            ),
        )

        code_a = source_code.replace(
            "def calculate_tax(amount, is_luxury=False):",
            "def calculate_tax(amount: float, is_luxury: bool = False) -> float:\n    # Preserved half-up rounding for taxes",
        )

        diff_a = """--- invoice_totals.py (original)
+++ invoice_totals.py (candidate A: conservative)
@@ -4,4 +4,4 @@
-def calculate_tax(amount, is_luxury=False):
+def calculate_tax(amount: float, is_luxury: bool = False) -> float:
+    # Preserved half-up rounding for taxes
     rate = LUXURY_TAX_RATE if is_luxury else DEFAULT_TAX_RATE
"""

        res_a = CandidateResult(
            candidate_id=cand_a_id,
            strategy="conservative",
            status="green",
            iterations=1,
            tests_passed=10,
            tests_total=10,
            code=code_a,
            diff=diff_a,
            summary="Preserved all numerical rounding characteristics while adding type signatures.",
        )
        candidates.append(res_a)

        await self.event_bus.emit(
            run_id,
            "candidate.result",
            CandidateResultData(
                candidate_id=cand_a_id,
                strategy=CandidateStrategy.CONSERVATIVE,
                status=CandidateResultStatus.GREEN,
                iterations=1,
                tests_passed=10,
                tests_total=10,
                summary=res_a.summary,
            ),
        )

        # Candidate B: Balanced (Falls into the trap by naively unifying round())
        cand_b_id = "cand-bal"
        await self.event_bus.emit(
            run_id,
            "candidate.started",
            CandidateStartedData(
                candidate_id=cand_b_id,
                strategy=CandidateStrategy.BALANCED,
                model_tier="super",
            ),
        )
        await asyncio.sleep(0.1)

        await self.event_bus.emit(
            run_id,
            "candidate.iteration",
            CandidateIterationData(
                candidate_id=cand_b_id,
                iteration=1,
                tests_passed=9,
                tests_failed=1,
                action="Unified rounding logic using standard round()",
            ),
        )

        # Naive refactor that unifies rounding to round()
        code_b = source_code.replace(
            "tax_cents = int(tax * 100 + 0.5)\n    return tax_cents / 100.0",
            "return round(tax, 2)  # Refactored to standard round()",
        )

        diff_b = """--- invoice_totals.py (original)
+++ invoice_totals.py (candidate B: balanced)
@@ -29,3 +29,2 @@
-    tax_cents = int(tax * 100 + 0.5)
-    return tax_cents / 100.0
+    return round(tax, 2)  # Unified rounding trap!
"""

        res_b = CandidateResult(
            candidate_id=cand_b_id,
            strategy="balanced",
            status="green",  # It might pass coarse tests if they don't hit the exact boundary
            iterations=2,
            tests_passed=10,
            tests_total=10,
            code=code_b,
            diff=diff_b,
            summary="Refactored rounding functions to standard Python round().",
        )
        candidates.append(res_b)

        await self.event_bus.emit(
            run_id,
            "candidate.result",
            CandidateResultData(
                candidate_id=cand_b_id,
                strategy=CandidateStrategy.BALANCED,
                status=CandidateResultStatus.GREEN,
                iterations=2,
                tests_passed=10,
                tests_total=10,
                summary=res_b.summary,
            ),
        )

        return candidates
