"""Syntax roles: which Pygments token types get which `code-*` token of the design system.

One table drives both outputs, so they can never disagree:

* the CSS rules in the shipped stylesheet (``css_rules``), used by the Sphinx theme, and
* the Pygments styles ``michel-albert-light`` and ``michel-albert-dark`` (``pygments_styles``).

A token type takes the role of its nearest listed ancestor, so ``Name.Builtin.Pseudo``
(``self``) is a built-in and ``Keyword.Constant`` (``None``) a constant.
"""

from __future__ import annotations

from typing import NamedTuple

from pygments.token import (
    STANDARD_TYPES,
    Comment,
    Error,
    Generic,
    Keyword,
    Literal,
    Name,
    Number,
    Operator,
    Punctuation,
    String,
    Token,
    _TokenType,
)


class Role(NamedTuple):
    token: str  # design-system colour token, without the "code-" prefix
    bold: bool = False
    italic: bool = False


ROLES: dict[_TokenType, Role] = {
    Token: Role("name"),
    Name: Role("name"),
    Keyword: Role("keyword", bold=True),
    Operator.Word: Role("keyword", bold=True),  # and, or, not, in, is
    Keyword.Constant: Role("constant"),  # True, False, None, null
    Keyword.Type: Role("builtin"),
    Name.Builtin: Role("builtin"),  # print, len, str; Name.Builtin.Pseudo: self
    Name.Function: Role("function", bold=True),
    Name.Class: Role("function", bold=True),
    Name.Exception: Role("function", bold=True),
    Name.Decorator: Role("decorator"),
    Name.Tag: Role("key"),  # YAML and JSON keys, HTML tags
    Name.Attribute: Role("key"),
    Literal: Role("string"),  # e.g. YAML plain scalars
    String: Role("string"),
    Number: Role("number"),
    Comment: Role("comment", italic=True),
    Generic.Prompt: Role("comment"),
    Generic.Output: Role("comment"),
    Operator: Role("operator"),
    Punctuation: Role("operator"),
    Error: Role("error", bold=True),
    Generic.Error: Role("error", bold=True),
    Generic.Traceback: Role("error", bold=True),
}


def role_of(token_type: _TokenType) -> Role:
    t = token_type
    while t not in ROLES:
        t = t.parent
    return ROLES[t]


def css_rules(scope: str = ".highlight") -> str:
    """CSS for every standard Pygments class, coloured with ``var(--ma-code-<role>)``."""
    by_role: dict[Role, list[str]] = {}
    for token_type, short in STANDARD_TYPES.items():
        if not short:
            continue
        by_role.setdefault(role_of(token_type), []).append(short)
    rules = []
    for role, classes in sorted(by_role.items(), key=lambda item: item[0]):
        selector = ", ".join(f"{scope} .{c}" for c in sorted(classes))
        rules.append(
            f"{selector} {{ color: var(--ma-code-{role.token}) !important; "
            f"font-weight: {600 if role.bold else 400} !important; "
            f"font-style: {'italic' if role.italic else 'normal'} !important; }}"
        )
    return "\n".join(rules)
