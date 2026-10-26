"""The Pygments styles and the CSS come from the same role table and the same tokens."""

import re
from pathlib import Path

import pytest
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import PythonLexer
from pygments.styles import get_style_by_name
from pygments.token import Keyword, Name

from michel_albert_sphinx.code_roles import role_of
from michel_albert_sphinx.pygments_styles import color

ROOT = Path(__file__).parent.parent


@pytest.mark.parametrize("name,theme", [("michel-albert-light", "light"), ("michel-albert-dark", "dark")])
def test_styles_are_registered_and_use_the_tokens(name, theme):
    style = get_style_by_name(name)  # found through the pygments.styles entry point
    assert style.background_color == color("surface-300", theme)
    assert style.style_for_token(Name.Builtin)["color"] == color("code-builtin", theme).lstrip("#")
    assert style.style_for_token(Keyword)["bold"]


def test_print_is_a_builtin():
    assert role_of(Name.Builtin).token == "builtin"
    assert role_of(Name.Builtin.Pseudo).token == "builtin"  # self
    assert role_of(Keyword.Constant).token == "constant"


def test_every_highlight_class_is_coloured():
    css = (ROOT / "src/michel_albert_sphinx/static/michel-albert.css").read_text(encoding="utf-8")
    html = highlight("print(len(self.x)); None\n@d\ndef f(): return 'a' # c", PythonLexer(), HtmlFormatter())
    for cls in set(re.findall(r'class="([a-z0-9]+)"', html)) - {"highlight"}:
        assert re.search(rf"\.highlight \.{cls}[ ,]", css), f".{cls} has no colour rule"
