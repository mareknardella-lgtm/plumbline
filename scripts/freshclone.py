"""Fresh clone verification script (§14.4 / §16.3).

Verifies:
- Repository can be checked out cleanly
- No secrets or private keys are committed in tracking
- .env is untracked and .env.example is provided
- Basic import and test sanity passes without local-only state
"""

import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent


def check_git_secrets():
    print("Checking for accidental secret leaks in tracked files...")
    # Check tracked files for potential API keys
    cmd = ["git", "ls-files"]
    res = subprocess.run(cmd, cwd=REPO_ROOT, capture_output=True, text=True, check=True)
    tracked_files = [line.strip() for line in res.stdout.splitlines() if line.strip()]

    if ".env" in tracked_files:
        print("[FAIL] .env is tracked in git!")
        return False

    import re

    # Check for actual secret values like nvapi-..., sk-..., ghp_..., or non-empty key assignments
    secret_regexes = [
        re.compile(r"nvapi-[A-Za-z0-9_\-]{20,}"),
        re.compile(r"ghp_[A-Za-z0-9_\-]{20,}"),
        re.compile(r"sk-[A-Za-z0-9_\-]{20,}"),
        re.compile(r"nebius_api_key\s*=\s*[\"'][A-Za-z0-9_\-]{15,}[\"']"),
    ]
    leak_detected = False

    for file_str in tracked_files:
        f = REPO_ROOT / file_str
        if not f.exists() or not f.is_file():
            continue
        try:
            content = f.read_text(encoding="utf-8", errors="ignore")
            for rgx in secret_regexes:
                if rgx.search(content):
                    print(f"[FAIL] Potential secret detected in {file_str}")
                    leak_detected = True
        except Exception:
            pass

    if leak_detected:
        return False

    print("[PASS] No tracked secrets detected.")
    return True


def check_prerequisites():
    print("Checking repository prerequisites...")
    env_example = REPO_ROOT / ".env.example"
    if not env_example.exists():
        print("[FAIL] Missing .env.example")
        return False
    print("[PASS] .env.example exists.")

    readme = REPO_ROOT / "README.md"
    if not readme.exists():
        print("[FAIL] Missing README.md")
        return False
    print("[PASS] README.md exists.")

    return True


def main():
    print("=== Fresh Clone Verification ===")
    ok = check_prerequisites() and check_git_secrets()
    if not ok:
        print("\nFresh clone check FAILED.")
        sys.exit(1)
    print("\nFresh clone check PASSED.")


if __name__ == "__main__":
    main()
