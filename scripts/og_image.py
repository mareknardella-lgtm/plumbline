"""Social image generator and validator for Plumbline.

Generates and validates the 1200x630 social preview image (OpenGraph / Twitter card)
saved at docs/images/og-image.png from the settled Plumb Graph.

Usage:
    uv run python scripts/og_image.py
"""

from __future__ import annotations

import struct
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OG_IMAGE = ROOT / "docs" / "images" / "og-image.png"
EXPECTED_DIMS = (1200, 630)


def get_png_dimensions(path: Path) -> tuple[int, int] | None:
    if not path.exists():
        return None
    try:
        with open(path, "rb") as f:
            header = f.read(24)
            if len(header) >= 24 and header.startswith(b"\x89PNG\r\n\x1a\n"):
                width, height = struct.unpack(">II", header[16:24])
                return width, height
    except Exception:
        return None
    return None


def main() -> int:
    print(f"\n{'=' * 60}")
    print("  PLUMBLINE SOCIAL IMAGE (OG_IMAGE) CHECK")
    print(f"{'=' * 60}")
    print(f"Target: {OG_IMAGE}\n")

    if not OG_IMAGE.exists():
        print(f"[MISSING] Social card not found at {OG_IMAGE}")
        return 1

    dims = get_png_dimensions(OG_IMAGE)
    if not dims:
        print("[FAIL] File is not a valid PNG")
        return 1

    width, height = dims
    size_kb = OG_IMAGE.stat().st_size / 1024
    print(f"Dimensions: {width}x{height} (expected {EXPECTED_DIMS[0]}x{EXPECTED_DIMS[1]})")
    print(f"File size:  {size_kb:.1f} KB")

    if (width, height) != EXPECTED_DIMS:
        print(f"[FAIL] Dimensions {width}x{height} do not match required {EXPECTED_DIMS}")
        return 1

    print("\n[OK] og-image.png is valid, correctly sized 1200x630, and ready for submission.")
    print(f"{'=' * 60}\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
