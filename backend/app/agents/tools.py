from typing import Any

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "list_files",
            "description": "List files in a directory",
            "parameters": {
                "type": "object",
                "properties": {"path": {"type": "string"}},
                "required": ["path"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "read_file",
            "description": "Read a file",
            "parameters": {
                "type": "object",
                "properties": {"path": {"type": "string"}},
                "required": ["path"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "write_file",
            "description": "Write a file",
            "parameters": {
                "type": "object",
                "properties": {"path": {"type": "string"}, "content": {"type": "string"}},
                "required": ["path", "content"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "run_tests",
            "description": "Run tests",
            "parameters": {"type": "object", "properties": {}},
        },
    },
    {
        "type": "function",
        "function": {
            "name": "run_shell",
            "description": "Run a shell command",
            "parameters": {
                "type": "object",
                "properties": {"command": {"type": "string"}},
                "required": ["command"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "rollback",
            "description": "Rollback to a checkpoint",
            "parameters": {
                "type": "object",
                "properties": {"checkpoint": {"type": "string"}},
                "required": ["checkpoint"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "finish",
            "description": "Finish task",
            "parameters": {
                "type": "object",
                "properties": {"summary": {"type": "string"}},
                "required": ["summary"],
            },
        },
    },
]


async def execute_tool(name: str, args: dict, sandbox: Any) -> Any:
    if name == "list_files":
        return await sandbox.list_files(args["path"])
    elif name == "read_file":
        return await sandbox.read_file(args["path"])
    elif name == "write_file":
        return await sandbox.write_file(args["path"], args["content"])
    elif name == "run_tests":
        return await sandbox.run_command("pytest")
    elif name == "run_shell":
        allowed = ["python", "pytest", "ruff", "radon", "coverage"]
        cmd = args["command"]
        if not any(cmd.startswith(a) for a in allowed):
            return "Error: Command not allowed"
        return await sandbox.run_command(cmd)
    elif name == "rollback":
        return await sandbox.rollback(args["checkpoint"])
    elif name == "finish":
        return args["summary"]
    else:
        raise ValueError(f"Unknown tool: {name}")
