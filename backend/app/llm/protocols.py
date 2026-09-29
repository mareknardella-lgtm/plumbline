"""LLM protocols."""

from typing import Any, Protocol


class LLMProtocol(Protocol):
    async def chat(
        self,
        messages: list[dict],
        model: str,
        temperature: float = 0.0,
        max_tokens: int | None = None,
        tools: list[dict] | None = None,
        response_format: dict | None = None,
    ) -> Any: ...

    async def chat_with_tools(
        self,
        messages: list[dict],
        model: str,
        tools: list[dict],
        temperature: float = 0.0,
        max_tokens: int | None = None,
    ) -> Any: ...


class SandboxProtocol(Protocol):
    async def prepare_image(self, tag: str, files: dict[str, str], packages: list[str]) -> str: ...
    async def run(
        self,
        image: str,
        shell: str,
        files: dict[str, str] | None = None,
        env: dict[str, str] | None = None,
        cwd: str | None = None,
        timeout: int = 60,
        disposable: bool = True,
    ) -> Any: ...
    async def fork(self, image_uuid: str) -> str: ...
    async def rollback(self, to_uuid: str) -> None: ...
    async def list_checkpoints(self) -> list[str]: ...


class SearcherProtocol(Protocol):
    async def search(self, query: str) -> list[dict]: ...
