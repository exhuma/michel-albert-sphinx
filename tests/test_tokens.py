"""The colour pairs the stylesheet relies on must meet WCAG contrast in both themes."""

import json
from pathlib import Path

import pytest

TOKENS = json.loads((Path(__file__).parent.parent / "src/michel_albert_sphinx/tokens.json").read_text())
COLORS = {t["name"]: t["value"] for t in TOKENS["color"]["tokens"]}

# (foreground, background, minimum ratio): text 4.5:1, control borders and the focus ring 3:1.
PAIRS = [
    ("ink", "surface-100", 4.5),
    ("ink", "surface-200", 4.5),
    ("ink", "surface-300", 4.5),
    ("ink-muted", "surface-100", 4.5),
    ("ink-muted", "surface-300", 4.5),
    ("accent", "surface-100", 4.5),  # links
    ("accent", "surface-300", 4.5),  # code keywords, linked inline code
    ("accent", "accent-subtle", 4.5),  # callout title
    ("ink", "accent-subtle", 4.5),  # callout text, active nav item
    ("on-accent", "accent", 4.5),
    ("good", "surface-300", 4.5),  # code strings
    ("warn", "surface-300", 4.5),  # code numbers
    ("critical", "surface-300", 4.5),  # code errors
    ("good", "good-subtle", 4.5),
    ("warn", "warn-subtle", 4.5),
    ("critical", "critical-subtle", 4.5),
    ("line-strong", "surface-100", 3.0),
    ("line-strong", "surface-200", 3.0),
    ("accent", "surface-200", 3.0),  # focus ring
]


def luminance(hex_color: str) -> float:
    h = hex_color.lstrip("#")
    channels = [int(h[i : i + 2], 16) / 255 for i in (0, 2, 4)]
    lin = [c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4 for c in channels]
    return 0.2126 * lin[0] + 0.7152 * lin[1] + 0.0722 * lin[2]


def contrast(a: str, b: str) -> float:
    la, lb = luminance(a), luminance(b)
    return (max(la, lb) + 0.05) / (min(la, lb) + 0.05)


@pytest.mark.parametrize("theme", ["light", "dark"])
@pytest.mark.parametrize("fg,bg,minimum", PAIRS)
def test_contrast(theme, fg, bg, minimum):
    ratio = contrast(COLORS[fg][theme], COLORS[bg][theme])
    assert ratio >= minimum, f"{fg} on {bg} ({theme}) is {ratio:.2f}:1, needs {minimum}:1"
