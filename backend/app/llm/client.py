"""LLM client."""

import asyncio
import time
from typing import Any

import openai
from openai import AsyncOpenAI

from backend.app.llm.registry import registry


class LLMClient:
    def __init__(self, base_url: str, api_key: str, concurrency_limit: int = 10):
        self.client = AsyncOpenAI(api_key=api_key or "empty", base_url=base_url)
        self.ledger: list[dict] = []
        # Per-model rate limiter could be a dict of Semaphores, here simple global for example
        self._semaphore = asyncio.Semaphore(concurrency_limit)

    async def chat(
        self,
        messages: list[dict],
        model: str,
        temperature: float = 0.0,
        max_tokens: int | None = None,
        tools: list[dict] | None = None,
        response_format: dict | None = None,
    ) -> Any:
        retries = 0
        max_retries = 3
        base_delay = 1.0

        while retries <= max_retries:
            try:
                start_time = time.time()
                async with self._semaphore:
                    kwargs: dict = {
                        "model": model,
                        "messages": messages,
                        "temperature": temperature,
                    }
                    if max_tokens:
                        kwargs["max_tokens"] = max_tokens
                    if tools:
                        kwargs["tools"] = tools
                    if response_format:
                        kwargs["response_format"] = response_format

                    response = await self.client.chat.completions.create(**kwargs)

                latency_ms = int((time.time() - start_time) * 1000)
                usage = response.usage
                tokens_in = usage.prompt_tokens if usage else 0
                tokens_out = usage.completion_tokens if usage else 0

                prices = registry.pricing.get(model, {"input": 0.0, "output": 0.0})
                cost_estimate = (tokens_in / 1000.0) * prices["input"] + (
                    tokens_out / 1000.0
                ) * prices["output"]

                self.ledger.append(
                    {
                        "model": model,
                        "tokens_in": tokens_in,
                        "tokens_out": tokens_out,
                        "latency_ms": latency_ms,
                        "retries": retries,
                        "cost_estimate": cost_estimate,
                    }
                )

                return response
            except (openai.RateLimitError, openai.APIError):
                retries += 1
                if retries > max_retries:
                    raise
                # Jittered exponential backoff
                await asyncio.sleep(base_delay * (2 ** (retries - 1)))
            except Exception:
                raise

    async def chat_with_tools(
        self,
        messages: list[dict],
        model: str,
        tools: list[dict],
        temperature: float = 0.0,
        max_tokens: int | None = None,
    ) -> Any:
        # Loop for tool calls
        current_messages = list(messages)
        while True:
            response = await self.chat(
                messages=current_messages,
                model=model,
                tools=tools,
                temperature=temperature,
                max_tokens=max_tokens,
            )
            msg = response.choices[0].message
            current_messages.append(msg.model_dump(exclude_none=True))

            if not msg.tool_calls:
                return response

            # If there are tool calls, the caller is expected to handle them
            # Here we just return the response to let caller execute tools and append results
            return response

    def get_ledger(self) -> list[dict]:
        return self.ledger

    def get_ledger_summary(self) -> dict:
        total_cost = sum(entry["cost_estimate"] for entry in self.ledger)
        total_in = sum(entry["tokens_in"] for entry in self.ledger)
        total_out = sum(entry["tokens_out"] for entry in self.ledger)
        return {
            "total_cost": total_cost,
            "total_tokens_in": total_in,
            "total_tokens_out": total_out,
            "calls": len(self.ledger),
        }
