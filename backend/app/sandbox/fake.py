"""Fake sandbox for testing."""

import uuid
from typing import Any


class FakeSandbox:
    def __init__(self):
        self.ops = []

    async def prepare_image(self, tag: str, files: dict[str, str], packages: list[str]) -> str:
        return str(uuid.uuid4())

    async def run(
        self,
        image: str,
        shell: str,
        files: dict[str, str] | None = None,
        env: dict[str, str] | None = None,
        cwd: str | None = None,
        timeout: int = 60,
        disposable: bool = True,
    ) -> Any:
        self.ops.append("run")
        return {"exit_code": 0, "stdout": "fake ok", "stderr": ""}

    async def fork(self, image_uuid: str) -> str:
        return str(uuid.uuid4())

    async def rollback(self, to_uuid: str) -> None:
        pass

    async def list_checkpoints(self) -> list[str]:
        return []
