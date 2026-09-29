"""Check color contrast ratios for accessibility compliance.

Usage:
    uv run python scripts/check_contrast.py

Verifies every text/background pair in the design tokens meets WCAG 2.2 AA:
- Text: at least 4.5:1 contrast ratio
- UI components: at least 3:1 contrast ratio
"""

import sys
from typing import NamedTuple


class ColorPair(NamedTuple):
    name: str
    foreground: str
    background: str
    min_ratio: float  # 4.5 for text, 3.0 for UI components


def hex_to_rgb(hex_color: str) -> tuple[float, float, float]:
    """Convert hex color to RGB values (0-255)."""
    h = hex_color.lstrip("#")
    return tuple(int(h[i : i + 2], 16) for i in (0, 2, 4))  # type: ignore


def relative_luminance(r: float, g: float, b: float) -> float:
    """Calculate relative luminance per WCAG 2.0."""

    def linearize(c: float) -> float:
        c = c / 255.0
        return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4

    return 0.2126 * linearize(r) + 0.7152 * linearize(g) + 0.0722 * linearize(b)


def contrast_ratio(fg: str, bg: str) -> float:
    """Calculate contrast ratio between two hex colors."""
    l1 = relative_luminance(*hex_to_rgb(fg))
    l2 = relative_luminance(*hex_to_rgb(bg))
    lighter = max(l1, l2)
    darker = min(l1, l2)
    return (lighter + 0.05) / (darker + 0.05)


# Light theme pairs
LIGHT_PAIRS: list[ColorPair] = [
    # Text on backgrounds
    ColorPair("ink on sheet", "#1B2127", "#EEF1F3", 4.5),
    ColorPair("ink on panel", "#1B2127", "#FAFBFB", 4.5),
    ColorPair("ink-2 on sheet", "#46515C", "#EEF1F3", 4.5),
    ColorPair("ink-2 on panel", "#46515C", "#FAFBFB", 4.5),
    ColorPair("ink-3 on sheet", "#59636E", "#EEF1F3", 4.5),
    ColorPair("ink-3 on panel", "#59636E", "#FAFBFB", 4.5),
    # Brand / links
    ColorPair("plumb on sheet", "#2350C8", "#EEF1F3", 4.5),
    ColorPair("plumb on panel", "#2350C8", "#FAFBFB", 4.5),
    # Status text
    ColorPair("holds on sheet", "#0F6B4F", "#EEF1F3", 4.5),
    ColorPair("drift on sheet", "#A8281A", "#EEF1F3", 4.5),
    ColorPair("caution on sheet", "#8A5F00", "#EEF1F3", 4.5),
    # Status on tints
    ColorPair("holds on holds-tint", "#0F6B4F", "#D8EFE6", 4.5),
    ColorPair("drift on drift-tint", "#A8281A", "#F7DDD8", 4.5),
    ColorPair("caution on caution-tint", "#8A5F00", "#F3E6C4", 4.5),
    ColorPair("plumb on plumb-tint", "#2350C8", "#DCE6FB", 4.5),
    # UI components (3:1)
    ColorPair("rule on sheet (UI)", "#788898", "#EEF1F3", 3.0),
    ColorPair("rule-strong on sheet (UI)", "#506070", "#EEF1F3", 3.0),
]

# Dark theme pairs
DARK_PAIRS: list[ColorPair] = [
    ColorPair("ink on sheet (dark)", "#E7ECF0", "#171E26", 4.5),
    ColorPair("ink on panel (dark)", "#E7ECF0", "#1D2630", 4.5),
    ColorPair("ink-2 on sheet (dark)", "#B6C0CA", "#171E26", 4.5),
    ColorPair("ink-2 on panel (dark)", "#B6C0CA", "#1D2630", 4.5),
    ColorPair("ink-3 on sheet (dark)", "#97A3AF", "#171E26", 4.5),
    ColorPair("ink-3 on panel (dark)", "#97A3AF", "#1D2630", 4.5),
    ColorPair("plumb on sheet (dark)", "#86A8FF", "#171E26", 4.5),
    ColorPair("plumb on panel (dark)", "#86A8FF", "#1D2630", 4.5),
    ColorPair("holds on sheet (dark)", "#63D3A9", "#171E26", 4.5),
    ColorPair("drift on sheet (dark)", "#FF9082", "#171E26", 4.5),
    ColorPair("caution on sheet (dark)", "#E5B44E", "#171E26", 4.5),
    # UI components
    ColorPair("rule on sheet (dark, UI)", "#607080", "#171E26", 3.0),
    ColorPair("rule-strong on sheet (dark, UI)", "#8898A8", "#171E26", 3.0),
]


def main() -> None:
    all_pass = True
    all_pairs = LIGHT_PAIRS + DARK_PAIRS

    print(f"Checking {len(all_pairs)} color pairs...\n")

    for pair in all_pairs:
        ratio = contrast_ratio(pair.foreground, pair.background)
        passed = ratio >= pair.min_ratio
        icon = "OK" if passed else "XX"
        label = "PASS" if passed else "FAIL"

        print(
            f"  [{icon}] {label} {pair.name}: "
            f"{ratio:.2f}:1 (min {pair.min_ratio}:1) "
            f"[{pair.foreground} on {pair.background}]"
        )

        if not passed:
            all_pass = False

    print()
    if all_pass:
        print("All contrast checks PASSED.")
    else:
        print("Some contrast checks FAILED. Adjust colors in tokens.css.")
        sys.exit(1)


if __name__ == "__main__":
    main()
