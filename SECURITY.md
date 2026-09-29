# Security policy

## Reporting a vulnerability

If you discover a security vulnerability in Plumbline, please report it by opening a GitHub issue or contacting the maintainer directly.

## Execution model

Plumbline executes user-supplied Python code **only inside Token Factory Sandboxes**, which provide VM-level isolation. The backend process never imports, evaluates or executes user code.

- API keys never enter a sandbox.
- Sandbox operations have a 60-second timeout.
- A static pre-check flags code that opens network connections, spawns subprocesses or uses crypto-miner patterns. Such code is rejected in live mode.
- The sandbox is the security boundary. The pre-check is a convenience, not a guarantee.

## Web application

- All user and model text is rendered as text, never as HTML.
- Strict Content-Security-Policy headers are set.
- Request bodies are validated with Pydantic.
- No cookies, no third-party analytics, no trackers.
- Runs are deleted after 7 days.
