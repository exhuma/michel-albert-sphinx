"""Margin notes, the start-page lede and their switches."""

import re
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).parent.parent


def build(out: Path, *defines: str) -> Path:
    args = [sys.executable, "-m", "sphinx", "-W", "--keep-going", "-b", "html"]
    for d in defines:
        args += ["-D", d]
    result = subprocess.run([*args, str(ROOT / "docs"), str(out)], capture_output=True, text=True)
    assert result.returncode == 0, result.stdout + result.stderr
    return out


@pytest.fixture(scope="module")
def site(tmp_path_factory):
    return build(tmp_path_factory.mktemp("default"))


def asides(html: str) -> list[str]:
    """The HTML of each margin-note group, outermost wrapper only."""
    groups, depth, start = [], 0, None
    for m in re.finditer(r'<div class="ma-aside[ "]|<div\b|</div>', html):
        tag = m.group(0)
        if tag.startswith('<div class="ma-aside') and not tag.startswith('<div class="ma-aside-notes'):
            if depth == 0:
                start = m.start()
            depth += 1 if start is not None else 0
        elif tag.startswith("<div") and start is not None:
            depth += 1
        elif tag == "</div>" and start is not None:
            depth -= 1
            if depth == 0:
                groups.append(html[start : m.end()])
                start = None
    return groups


def test_notes_after_prose_go_to_the_margin(site):
    groups = asides((site / "style-reference.html").read_text(encoding="utf-8"))
    assert len(groups) == 2
    first, second = groups
    assert "<ul" in first and "note" in first  # a list and the note that follows it
    assert "tip" in second and "seealso" in second  # consecutive notes stack together


def test_source_order_is_kept(site):
    group = asides((site / "style-reference.html").read_text(encoding="utf-8"))[1]
    assert group.index("<p>") < group.index("ma-aside-notes")


def test_inline_class_and_warnings_stay_in_text(site):
    html = (site / "style-reference.html").read_text(encoding="utf-8")
    for group in asides(html):
        assert "ma-inline" not in group
        assert "warning" not in group
    assert "ma-inline" in html


def test_start_page_lede(site):
    assert 'class="ma-lede"' in (site / "index.html").read_text(encoding="utf-8")
    assert "ma-lede" not in (site / "usage.html").read_text(encoding="utf-8")


def test_switches(tmp_path):
    out = build(tmp_path, "michel_albert_margin_notes=0", "michel_albert_home_header=0")
    assert not asides((out / "style-reference.html").read_text(encoding="utf-8"))
    assert "ma-lede" not in (out / "index.html").read_text(encoding="utf-8")
