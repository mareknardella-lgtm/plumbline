"""Single quality command for Plumbline.

Usage:
    uv run python scripts/check.py          # default checks
    uv run python scripts/check.py --fast   # skip build
    uv run python scripts/check.py --e2e    # include Playwright e2e
    uv run python scripts/check.py --live   # include live-service tests
"""

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def run(cmd: list[str], label: str) -> bool:
    """Run a command, print its label, and return True on success."""
    print(f"\n{'=' * 60}")
    print(f"  {label}")
    print(f"{'=' * 60}")
    result = subprocess.run(cmd, cwd=str(ROOT), shell=(sys.platform == "win32"))
    ok = result.returncode == 0
    print(f"  {'PASS' if ok else 'FAIL'}: {label}")
    return ok


def main() -> None:
    args = set(sys.argv[1:])
    fast = "--fast" in args
    e2e = "--e2e" in args
    live = "--live" in args

    results: list[tuple[str, bool]] = []

    # Python lint and format check
    results.append(("ruff check", run(["uv", "run", "ruff", "check", "."], "Ruff lint")))
    results.append(
        ("ruff format", run(["uv", "run", "ruff", "format", "--check", "."], "Ruff format check"))
    )

    # Type check
    results.append(("pyright", run(["uv", "run", "pyright", "backend/"], "Pyright type check")))

    # Backend tests
    pytest_args = ["uv", "run", "pytest", "backend/tests/", "-v"]
    if not live:
        pytest_args.extend(["-m", "not live"])
    results.append(("backend tests", run(pytest_args, "Backend tests")))

    # Frontend checks
    if not fast:
        frontend_dir = ROOT / "frontend"
        if (frontend_dir / "package.json").exists():
            results.append(
                (
                    "npm typecheck",
                    run(["npm", "--prefix", "frontend", "run", "typecheck"], "Frontend typecheck"),
                )
            )
            results.append(
                ("npm lint", run(["npm", "--prefix", "frontend", "run", "lint"], "Frontend lint"))
            )
            results.append(
                (
                    "npm test",
                    run(
                        ["npm", "--prefix", "frontend", "run", "test:run"],
                        "Frontend unit tests",
                    ),
                )
            )
            results.append(
                (
                    "npm build",
                    run(["npm", "--prefix", "frontend", "run", "build"], "Frontend build"),
                )
            )

    # E2E
    if e2e:
        results.append(
            (
                "playwright",
                run(["npx", "playwright", "test", "--project=chromium"], "Playwright e2e"),
            )
        )

    # Summary
    print(f"\n{'=' * 60}")
    print("  SUMMARY")
    print(f"{'=' * 60}")
    all_pass = True
    for label, ok in results:
        icon = "[OK]" if ok else "[XX]"
        print(f"  {icon} {label}")
        if not ok:
            all_pass = False

    if not all_pass:
        print("\n  Some checks FAILED.")
        sys.exit(1)
    else:
        print("\n  All checks PASSED.")


if __name__ == "__main__":
    main()
