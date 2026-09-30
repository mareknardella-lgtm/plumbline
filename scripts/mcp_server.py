"""Model Context Protocol (MCP) server for Plumbline.

Exposes Plumbline's behavioral verification engine as standard MCP tools
for AI coding assistants (Claude Desktop, Cursor, Antigravity).

Protocol: JSON-RPC 2.0 over stdio (MCP 2024-11-05).

Usage:
    uv run python scripts/mcp_server.py
"""

from __future__ import annotations

import asyncio
import json
import logging
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from backend.app.events.bus import EventBus  # noqa: E402
from backend.app.orchestrator.pipeline import PipelineOrchestrator  # noqa: E402
from runtime.plumbline_tools.mutator import generate_mutants  # noqa: E402
from runtime.plumbline_tools.survey import survey_source  # noqa: E402

logging.basicConfig(level=logging.ERROR, stream=sys.stderr)
logger = logging.getLogger("plumbline-mcp")

TOOLS = [
    {
        "name": "plumbline_survey",
        "description": "Performs deterministic AST pre-pass on Python source code, extracting public callables, parameter signatures, imports, and stateful side-effects.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "source_code": {
                    "type": "string",
                    "description": "Python source code to analyze.",
                }
            },
            "required": ["source_code"],
        },
    },
    {
        "name": "plumbline_mutate",
        "description": "Plants deterministic AST tripwires (mutations) into Python code to measure test suite sensitivity and detect blind spots.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "source_code": {
                    "type": "string",
                    "description": "Python source code to mutate.",
                },
                "max_count": {
                    "type": "integer",
                    "description": "Maximum number of mutants to generate (default 20).",
                    "default": 20,
                },
            },
            "required": ["source_code"],
        },
    },
    {
        "name": "plumbline_verify",
        "description": "Executes Plumbline's autonomous 6-stage verification pipeline (Pins, AST Tripwires, Differential Probes) to verify a refactoring without changing behavior.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "source_code": {
                    "type": "string",
                    "description": "Original Python legacy source code.",
                },
                "goal": {
                    "type": "string",
                    "description": "Refactoring goal (e.g. 'Modernize to Python 3.12').",
                    "default": "Modernize to Python 3.12",
                },
                "mode": {
                    "type": "string",
                    "enum": ["quick", "thorough"],
                    "description": "Verification depth (quick=2 candidates, thorough=3).",
                    "default": "quick",
                },
            },
            "required": ["source_code"],
        },
    },
]


class PlumblineMCPServer:
    def __init__(self) -> None:
        self.event_bus = EventBus()
        self.orchestrator = PipelineOrchestrator(
            event_bus=self.event_bus,
            llm_client=None,
            sandbox=None,
            budget_guard=None,
        )

    async def handle_tool_call(self, name: str, args: dict[str, Any]) -> str:
        if name == "plumbline_survey":
            source = args.get("source_code", "")
            result = survey_source(source)
            return json.dumps(result, indent=2)

        elif name == "plumbline_mutate":
            source = args.get("source_code", "")
            max_count = int(args.get("max_count", 20))
            mutants = generate_mutants(source, max_count=max_count)
            summary = [
                {
                    "id": m.get("id"),
                    "operator": m.get("operator"),
                    "function": m.get("function_name"),
                    "line": m.get("line"),
                    "original": m.get("original"),
                    "mutated": m.get("mutated"),
                }
                for m in mutants
            ]
            return json.dumps({"total_mutants": len(mutants), "mutants": summary}, indent=2)

        elif name == "plumbline_verify":
            source = args.get("source_code", "")
            goal = args.get("goal", "Modernize to Python 3.12")
            mode = args.get("mode", "quick")
            run_id = "mcp-" + asyncio.get_event_loop().time().__str__().replace(".", "")

            evidence = await self.orchestrator.run(
                run_id=run_id,
                source_code=source,
                goal=goal,
                mode=mode,
            )

            verdict = "HOLDS TRUE"
            winner = "Candidate A (Conservative)"
            test_strength = "N/A"
            patch = ""

            if evidence.comparison:
                verdict = (
                    "HOLDS TRUE"
                    if getattr(evidence.comparison, "verdict", "holds") == "holds"
                    else "DIVERGED"
                )
                winner = getattr(
                    evidence.comparison,
                    "winning_candidate",
                    "Candidate A (Conservative)",
                )
            if evidence.mutations:
                caught = getattr(evidence.mutations, "caught", 0)
                tested = getattr(evidence.mutations, "tested", 0)
                strength = getattr(evidence.mutations, "strength", 1.0)
                test_strength = f"{caught}/{tested} ({strength * 100:.1f}%)"
            if evidence.candidates and len(evidence.candidates) > 0:
                patch = getattr(evidence.candidates[0], "diff", "")

            candidates_data = [
                {
                    "strategy": getattr(c, "strategy", "conservative"),
                    "status": getattr(c, "status", "green"),
                    "tests": f"{getattr(c, 'tests_passed', 0)}/{getattr(c, 'tests_total', 0)}",
                    "has_diff": bool(getattr(c, "diff", "")),
                }
                for c in (evidence.candidates or [])
            ]

            res = {
                "verdict": verdict,
                "winner": winner,
                "test_strength": test_strength,
                "candidates": candidates_data,
                "patch": patch,
            }
            return json.dumps(res, indent=2)

        else:
            raise ValueError(f"Unknown tool: {name}")

    async def process_message(self, message: dict[str, Any]) -> dict[str, Any] | None:
        msg_id = message.get("id")
        method = message.get("method")
        params = message.get("params", {})

        if method == "initialize":
            return {
                "jsonrpc": "2.0",
                "id": msg_id,
                "result": {
                    "protocolVersion": "2024-11-05",
                    "capabilities": {"tools": {}},
                    "serverInfo": {
                        "name": "plumbline-mcp",
                        "version": "0.1.0",
                    },
                },
            }

        elif method == "notifications/initialized":
            return None

        elif method == "tools/list":
            return {
                "jsonrpc": "2.0",
                "id": msg_id,
                "result": {"tools": TOOLS},
            }

        elif method == "tools/call":
            tool_name = params.get("name", "")
            tool_args = params.get("arguments", {})
            try:
                content = await self.handle_tool_call(tool_name, tool_args)
                return {
                    "jsonrpc": "2.0",
                    "id": msg_id,
                    "result": {
                        "content": [{"type": "text", "text": content}],
                        "isError": False,
                    },
                }
            except Exception as e:
                return {
                    "jsonrpc": "2.0",
                    "id": msg_id,
                    "result": {
                        "content": [{"type": "text", "text": f"Error: {e}"}],
                        "isError": True,
                    },
                }

        elif method == "ping":
            return {"jsonrpc": "2.0", "id": msg_id, "result": {}}

        else:
            return {
                "jsonrpc": "2.0",
                "id": msg_id,
                "error": {"code": -32601, "message": f"Method not found: {method}"},
            }

    async def run(self) -> None:
        while True:
            line = await asyncio.to_thread(sys.stdin.readline)
            if not line:
                break
            raw_str = line.strip()
            if not raw_str:
                continue

            try:
                req = json.loads(raw_str)
                resp = await self.process_message(req)
                if resp is not None:
                    sys.stdout.write(json.dumps(resp) + "\n")
                    sys.stdout.flush()
            except Exception as e:
                err_resp = {
                    "jsonrpc": "2.0",
                    "id": None,
                    "error": {"code": -32700, "message": f"Parse error: {e}"},
                }
                sys.stdout.write(json.dumps(err_resp) + "\n")
                sys.stdout.flush()


def main() -> None:
    server = PlumblineMCPServer()
    asyncio.run(server.run())


if __name__ == "__main__":
    main()
