"""Build the package's own docs and check what the extension promises."""

import re
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).parent.parent


def test_generated_css_is_current():
    result = subprocess.run([sys.executable, str(ROOT / "scripts/generate_css.py"), "--check"], capture_output=True, text=True)
    assert result.returncode == 0, result.stderr


@pytest.fixture(scope="module")
def site(tmp_path_factory):
    out = tmp_path_factory.mktemp("html")
    result = subprocess.run(
        [sys.executable, "-m", "sphinx", "-W", "--keep-going", "-b", "html", str(ROOT / "docs"), str(out)],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    return out


def test_uses_immaterial_and_stylesheet(site):
    html = (site / "style-reference.html").read_text(encoding="utf-8")
    assert "md-header" in html, "sphinx-immaterial markup missing"
    assert re.search(r'href="_static/michel-albert\.css', html)
    assert re.search(r'src="_static/michel-albert\.js', html)


def test_follows_os_colour_scheme(site):
    html = (site / "style-reference.html").read_text(encoding="utf-8")
    assert "(prefers-color-scheme: dark)" in html
    assert 'data-md-color-scheme="slate"' in html or "slate" in html


def test_no_google_fonts(site):
    for page in site.glob("*.html"):
        assert "fonts.googleapis.com" not in page.read_text(encoding="utf-8"), page.name


def test_fonts_shipped(site):
    fonts = sorted(p.name for p in (site / "_static/fonts").glob("*.woff2"))
    assert len(fonts) == 12
    css = (site / "_static/michel-albert.css").read_text(encoding="utf-8")
    for name in fonts:
        assert f"fonts/{name}" in css


def test_code_does_not_wrap(site):
    css = (site / "_static/michel-albert.css").read_text(encoding="utf-8")
    assert "pre-wrap" not in css
    assert "white-space: pre !important" in css
