"""Plumbline screenshot gallery validator and capture coordinator.

Validates the six required Devpost submission screenshots in docs/images/:
01-home, 02-cockpit-running, 03-graph-verdict, 04-dossier, 05-ledger, 06-architecture.

Usage:
    uv run python scripts/screenshots.py
"""

from __future__ import annotations

import struct
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
IMAGES_DIR = ROOT / "docs" / "images"

SCREENSHOTS = [
    {
        "filename": "01-home.png",
        "caption": "Plumbline home screen with specimen selection and verification depth controls.",
        "alt": "Plumbline home screen showing title, specimen selector cards, and start run button.",
    },
    {
        "filename": "02-cockpit-running.png",
        "caption": "Cockpit stream executing AST mutations across parallel Token Factory sandboxes.",
        "alt": "Cockpit interface displaying stage progression and live Plumb Graph tripwire ticks.",
    },
    {
        "filename": "03-graph-verdict.png",
        "caption": "Plumb Graph showing lateral candidate deflection and HOLDS TRUE verdict settle.",
        "alt": "Plumb Graph SVG diagram highlighting settled plumb line and candidate drift angles.",
    },
    {
        "filename": "04-dossier.png",
        "caption": "Final verification dossier with verified diff patch and probe evidence report.",
        "alt": "Dossier report showing verification verdict, code diff, and test evidence metrics.",
    },
    {
        "filename": "05-ledger.png",
        "caption": "Model usage ledger tracking Nemotron token consumption and sub-2ms sandbox forks.",
        "alt": "Execution ledger tab listing model calls, token counts, and sandbox fork timings.",
    },
    {
        "filename": "06-architecture.png",
        "caption": "Architecture drawer detailing Nemotron model roles and copy-on-write fork hierarchy.",
        "alt": "System architecture diagram illustrating model tiers and sandbox fork tree.",
    },
]


def get_png_dimensions(file_path: Path) -> tuple[int, int] | None:
    """Read width and height of a PNG from the IHDR chunk without dependencies."""
    if not file_path.exists():
        return None
    try:
        with open(file_path, "rb") as f:
            header = f.read(24)
            if len(header) >= 24 and header.startswith(b"\x89PNG\r\n\x1a\n"):
                width, height = struct.unpack(">II", header[16:24])
                return width, height
    except Exception:
        return None
    return None


def main() -> int:
    print(f"\n{'=' * 70}")
    print("  PLUMBLINE SUBMISSION SCREENSHOT GALLERY CHECK")
    print(f"{'=' * 70}")
    print(f"Directory: {IMAGES_DIR}\n")

    all_valid = True
    for item in SCREENSHOTS:
        fname = item["filename"]
        target = IMAGES_DIR / fname
        caption = item["caption"]
        alt = item["alt"]

        if not target.exists():
            print(f"[MISSING] {fname}")
            all_valid = False
            continue

        size_kb = target.stat().st_size / 1024
        dims = get_png_dimensions(target)
        dim_str = f"{dims[0]}x{dims[1]}" if dims else "unknown"

        # Validate caption length <= 100 characters per §15.2
        if len(caption) > 100:
            print(f"[WARN] Caption exceeds 100 chars ({len(caption)}): {fname}")
            all_valid = False

        print(f"[OK] {fname:<22} | {dim_str:<10} | {size_kb:>6.1f} KB")
        print(f"     Caption: {caption}")
        print(f"     Alt text: {alt}")

    print(f"\n{'=' * 70}")
    if all_valid:
        print("  All 6 submission captures are present, verified, and conform to §15.2.")
        print(f"{'=' * 70}\n")
        return 0
    else:
        print("  Some screenshots are missing or failed verification.")
        print(f"{'=' * 70}\n")
        return 1


if __name__ == "__main__":
    sys.exit(main())
