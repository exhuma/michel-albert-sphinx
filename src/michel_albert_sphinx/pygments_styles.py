"""Pygments styles built from the design-system tokens.

Registered as ``michel-albert-light`` and ``michel-albert-dark``, so any tool that highlights
with Pygments can use them by name::

    pygmentize -O style=michel-albert-dark -f terminal256 example.py
"""

from __future__ import annotations

import json
from pathlib import Path

from pygments.style import Style
from pygments.token import STANDARD_TYPES

from .code_roles import role_of

_TOKENS = json.loads((Path(__file__).parent / "tokens.json").read_text(encoding="utf-8"))
_COLORS = {t["name"]: t["value"] for t in _TOKENS["color"]["tokens"]}


def color(name: str, theme: str, _depth: int = 0) -> str:
    """Resolve a colour token (following ``{alias}`` values) to a hex value for a theme."""
    if _depth > 16:
        raise ValueError(f"alias chain too deep at {name!r}")
    value = _COLORS[name]
    if isinstance(value, dict):
        value = value.get(theme, next(iter(value.values())))
    if value.startswith("{") and value.endswith("}"):
        return color(value[1:-1], theme, _depth + 1)
    return value


def _styles(theme: str) -> dict:
    styles = {}
    for token_type in STANDARD_TYPES:
        role = role_of(token_type)
        parts = [color(f"code-{role.token}", theme)]
        parts.append("bold" if role.bold else "nobold")
        parts.append("italic" if role.italic else "noitalic")
        styles[token_type] = " ".join(parts)
    return styles


class MichelAlbertLight(Style):
    name = "michel-albert-light"
    background_color = color("surface-300", "light")
    highlight_color = color("accent-subtle", "light")
    line_number_color = color("ink-muted", "light")
    styles = _styles("light")


class MichelAlbertDark(Style):
    name = "michel-albert-dark"
    background_color = color("surface-300", "dark")
    highlight_color = color("accent-subtle", "dark")
    line_number_color = color("ink-muted", "dark")
    styles = _styles("dark")
