"""Test script to verify production deployment readiness.

Verifies:
- /api/health responds with 200 OK
- /api/specimens returns available specimens
- /api/replays returns recorded replays
- / returns the bundled frontend HTML with proper security headers
"""

import sys
import urllib.error
import urllib.request


def test_endpoint(url: str, expected_status: int = 200) -> bytes:
    req = urllib.request.Request(url)
    with urllib.request.urlopen(req, timeout=5) as response:
        assert response.status == expected_status, (
            f"Expected {expected_status}, got {response.status}"
        )
        return response.read()


def test_security_headers(url: str):
    req = urllib.request.Request(url)
    with urllib.request.urlopen(req, timeout=5) as response:
        headers = {k.lower(): v for k, v in response.getheaders()}
        assert "content-security-policy" in headers, "Missing Content-Security-Policy header"
        assert "x-content-type-options" in headers, "Missing X-Content-Type-Options header"
        assert "x-frame-options" in headers, "Missing X-Frame-Options header"
        print("[PASS] Security headers verified.")


def main():
    base_url = "http://localhost:8000"
    print(f"Testing deployment on {base_url}...")

    try:
        # 1. Health
        health_data = test_endpoint(f"{base_url}/api/health")
        print(f"[PASS] /api/health OK ({len(health_data)} bytes)")

        # 2. Specimens
        specimens_data = test_endpoint(f"{base_url}/api/specimens")
        print(f"[PASS] /api/specimens OK ({len(specimens_data)} bytes)")

        # 3. Replays
        replays_data = test_endpoint(f"{base_url}/api/replays")
        print(f"[PASS] /api/replays OK ({len(replays_data)} bytes)")

        # 4. Frontend bundle & headers
        html_data = test_endpoint(f"{base_url}/")
        assert b"<!DOCTYPE html>" in html_data or b"<html" in html_data, (
            "Frontend index.html missing doctype"
        )
        print(f"[PASS] Frontend index.html served OK ({len(html_data)} bytes)")

        test_security_headers(f"{base_url}/")

        print("\nAll deployment verification tests PASSED.")
    except urllib.error.URLError as e:
        print(f"[FAIL] Connection error to {base_url}: {e}")
        print("Note: ensure the backend server is running on port 8000.")
        sys.exit(1)
    except AssertionError as e:
        print(f"[FAIL] Assertion error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
