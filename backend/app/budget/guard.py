"""Budget guard."""

import hashlib
import time
from datetime import UTC, datetime

from backend.app.settings import get_settings


class BudgetExhaustedError(Exception):
    pass


class RateLimitExceededError(Exception):
    pass


class BudgetGuard:
    def __init__(self):
        self.daily_spend = 0.0
        self.active_runs = 0
        self.ip_runs = {}  # type: dict[str, list[float]]

        # Per-run tracking
        self.run_tokens = {}
        self.run_dollars = {}
        self.run_start_times = {}
        self.run_sandbox_ops = {}
        self.run_llm_calls = {}

    def _get_salt(self) -> str:
        return datetime.now(UTC).strftime("%Y-%m-%d")

    def hash_ip(self, ip_address: str) -> str:
        salt = self._get_salt()
        return hashlib.sha256(f"{ip_address}:{salt}".encode()).hexdigest()

    def check_rate_limit(self, client_hash: str) -> None:
        settings = get_settings()
        now = time.time()

        if client_hash not in self.ip_runs:
            self.ip_runs[client_hash] = []

        # Clean up older than 1 hour
        self.ip_runs[client_hash] = [t for t in self.ip_runs[client_hash] if now - t < 3600]

        if len(self.ip_runs[client_hash]) >= settings.live_runs_per_ip_per_hour:
            raise RateLimitExceededError("Too many runs from this IP in the last hour.")

        self.ip_runs[client_hash].append(now)

    def check_daily_budget(self) -> float:
        settings = get_settings()
        remaining = settings.daily_budget_usd - self.daily_spend
        if remaining <= 0:
            raise BudgetExhaustedError("Daily budget exhausted.")
        return remaining

    def check_run_budget(self, run_id: str, mode: str = "quick") -> None:
        settings = get_settings()
        limit = (
            settings.run_budget_usd_thorough
            if mode == "thorough"
            else settings.run_budget_usd_quick
        )

        dollars = self.run_dollars.get(run_id, 0.0)
        if dollars > limit:
            raise BudgetExhaustedError(f"Run budget of ${limit} exhausted.")

    def record_llm_call(self, run_id: str, tokens: int, cost: float) -> None:
        self.run_tokens[run_id] = self.run_tokens.get(run_id, 0) + tokens
        self.run_dollars[run_id] = self.run_dollars.get(run_id, 0.0) + cost
        self.run_llm_calls[run_id] = self.run_llm_calls.get(run_id, 0) + 1
        self.daily_spend += cost

    def record_sandbox_op(self, run_id: str) -> None:
        self.run_sandbox_ops[run_id] = self.run_sandbox_ops.get(run_id, 0) + 1
