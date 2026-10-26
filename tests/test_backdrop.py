"""Seeded contour backdrop: the generator and what a build writes."""

import re
import subprocess
import sys
from pathlib import Path

import pytest

from michel_albert_sphinx.backdrop import TILE, contour_tiles

ROOT = Path(__file__).parent.parent
CSS = "michel-albert-backdrop.css"


def coordinates(svg: str) -> list[float]:
    return [float(v) for v in re.findall(r"-?\d+(?:\.\d+)?", svg.split(' d="', 1)[1].split('"', 1)[0])]


def test_same_seed_same_tile():
    assert contour_tiles("t61codec") == contour_tiles("t61codec")


def test_different_seeds_differ():
    assert contour_tiles("t61codec")[0] != contour_tiles("michel-albert-sphinx")[0]


@pytest.mark.parametrize("seed", ["t61codec", "michel-albert-sphinx", "x"])
def test_tile_is_in_bounds_and_small(seed):
    lines, accent = contour_tiles(seed)
    for svg in (lines, accent):
        values = coordinates(svg)
        assert values, "no contour lines drawn"
        assert min(values) >= 0 and max(values) <= TILE
        assert len(svg) < 150_000


def build(out: Path, *defines: str) -> Path:
    args = [sys.executable, "-m", "sphinx", "-W", "--keep-going", "-b", "html"]
    for d in defines:
        args += ["-D", d]
    result = subprocess.run([*args, str(ROOT / "docs"), str(out)], capture_output=True, text=True)
    assert result.returncode == 0, result.stdout + result.stderr
    return out


def test_build_writes_and_links_backdrop(tmp_path):
    out = build(tmp_path)
    css = (out / "_static" / CSS).read_text(encoding="utf-8")
    assert "seed 'michel-albert-sphinx'" in css  # seeded from `project`
    assert css.count("data:image/svg+xml") == 2  # embedded: works from disk without a server
    assert f"_static/{CSS}" in (out / "usage.html").read_text(encoding="utf-8")


def test_seed_override(tmp_path):
    default = build(tmp_path / "a")
    custom = build(tmp_path / "b", "michel_albert_backdrop_seed=something-else")
    assert (default / "_static" / CSS).read_text() != (custom / "_static" / CSS).read_text()


def test_switch_off(tmp_path):
    out = build(tmp_path, "michel_albert_backdrop=0")
    assert not (out / "_static" / CSS).exists()
    assert CSS not in (out / "usage.html").read_text(encoding="utf-8")
