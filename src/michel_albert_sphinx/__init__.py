"""Michel Albert's design system for Sphinx documentation.

Add ``"michel_albert_sphinx"`` to ``extensions`` in ``conf.py``. The extension

* enables the ``sphinx_immaterial`` theme,
* applies the design system's colours, type and shapes (light and dark),
* ships its own fonts, so pages make no requests to Google Fonts,
* makes overflowing code blocks reachable by keyboard,
* sets notes, tips, hints and "see also" in the margin beside the paragraph they follow
  (``michel_albert_margin_notes = False`` turns this off),
* styles the start page's first paragraph as a lede (``michel_albert_home_header = False``
  turns this off),
* sets the page on a raised sheet over contour lines generated from the project name
  (``michel_albert_backdrop_seed`` changes the seed, ``michel_albert_backdrop = False``
  turns it off).
"""

from __future__ import annotations

from importlib.metadata import PackageNotFoundError, version
from pathlib import Path
from typing import Any

from docutils import nodes
from sphinx import addnodes
from sphinx.application import Sphinx
from sphinx.config import Config
from sphinx.transforms.post_transforms import SphinxPostTransform
from sphinx.util import logging

from . import backdrop

try:
    __version__ = version("michel-albert-sphinx")
except PackageNotFoundError:  # running from a source checkout
    __version__ = "0.0.0"

logger = logging.getLogger(__name__)
STATIC = Path(__file__).parent / "static"
THEME = "sphinx_immaterial"

#: Theme options the identity depends on. A project's own ``html_theme_options`` win key by key.
DEFAULT_THEME_OPTIONS: dict[str, Any] = {
    # Fonts come from this package; don't load Google Fonts.
    "font": False,
    # Follow the reader's OS setting; the header toggle lets them override it.
    "palette": [
        {
            "media": "(prefers-color-scheme: light)",
            "scheme": "default",
            "toggle": {"icon": "material/weather-night", "name": "Switch to dark mode"},
        },
        {
            "media": "(prefers-color-scheme: dark)",
            "scheme": "slate",
            "toggle": {"icon": "material/weather-sunny", "name": "Switch to light mode"},
        },
    ],
}


#: Callouts that go to the margin, by kind. Warnings, cautions and dangers always stay in the
#: text. sphinx-immaterial turns every callout into a generic admonition node that carries its
#: kind as a class, so the kind is read from the classes, with the node type as a fallback.
MARGIN_KINDS = frozenset({"note", "tip", "hint", "seealso"})
MARGIN_NODES = (nodes.note, nodes.tip, nodes.hint, addnodes.seealso)


def _is_margin_note(node: nodes.Node) -> bool:
    if isinstance(node, MARGIN_NODES):
        return True
    return isinstance(node, nodes.Admonition) and bool(MARGIN_KINDS & set(node.get("classes", [])))
#: Blocks a margin note can sit beside.
PROSE = (
    nodes.paragraph,
    nodes.bullet_list,
    nodes.enumerated_list,
    nodes.definition_list,
    nodes.field_list,
    nodes.block_quote,
)
INLINE_CLASS = "ma-inline"


class MarginNotes(SphinxPostTransform):
    """Pair each note with the prose block before it.

    ``<prose> <note>`` becomes ``div.ma-aside > (<prose>, div.ma-aside-notes > <note>)``.
    The stylesheet sets the note beside its block on wide screens; on narrow screens the
    wrapper vanishes and the note follows its block. Source and reading order never change.

    A note stays in the text when it follows anything but prose (code, a table, a heading),
    when it is nested (in a list or another callout), or when it has the class ``ma-inline``.
    """

    default_priority = 400
    formats = ("html",)

    def run(self, **kwargs: Any) -> None:
        if not self.config.michel_albert_margin_notes:
            return
        for note in list(self.document.findall(_is_margin_note)):
            if INLINE_CLASS in note["classes"]:
                continue
            parent = note.parent
            if not isinstance(parent, (nodes.section, nodes.document)):
                continue
            index = parent.index(note)
            if index == 0:
                continue
            prev = parent[index - 1]
            if isinstance(prev, nodes.container) and "ma-aside" in prev["classes"]:
                parent.remove(note)
                prev[-1].append(note)  # a further note for the same block
            elif isinstance(prev, PROSE):
                notes = nodes.container(classes=["ma-aside-notes"])
                wrapper = nodes.container(classes=["ma-aside"])
                parent.remove(prev)
                parent.remove(note)
                notes += note
                wrapper += prev
                wrapper += notes
                parent.insert(index - 1, wrapper)


class StartPageLede(SphinxPostTransform):
    """Mark the start page's first paragraph as the lede (``p.ma-lede``)."""

    default_priority = 400
    formats = ("html",)

    def run(self, **kwargs: Any) -> None:
        if not self.config.michel_albert_home_header or self.env.docname != self.config.root_doc:
            return
        section = next(iter(self.document.findall(nodes.section)), None)
        if section is None or len(section) < 2:
            return
        if isinstance(section[0], nodes.title) and isinstance(section[1], nodes.paragraph):
            section[1]["classes"].append("ma-lede")


def _configure(app: Sphinx, config: Config) -> None:
    if config.html_theme in (None, "", "alabaster"):  # Sphinx's default: nobody chose a theme
        config.html_theme = THEME
    elif config.html_theme != THEME:
        logger.warning(
            "michel_albert_sphinx: html_theme is %r; the design system is built for %r and may look wrong.",
            config.html_theme,
            THEME,
        )
    config.html_theme_options = {**DEFAULT_THEME_OPTIONS, **(config.html_theme_options or {})}
    config.html_static_path = [*config.html_static_path, str(STATIC)]


BACKDROP_CSS = "michel-albert-backdrop.css"


def _svg_url(svg: str) -> str:
    data = svg.replace('"', "'").replace("%", "%25").replace("#", "%23").replace("<", "%3C").replace(">", "%3E")
    return f'url("data:image/svg+xml,{data}")'


def _backdrop_css(config: Config) -> str:
    """The project's backdrop stylesheet: its two contour tiles plus the frame rules."""
    seed = config.michel_albert_backdrop_seed or config.project or "michel-albert"
    lines, accent = backdrop.contour_tiles(seed)
    rules = (Path(__file__).parent / "backdrop.css").read_text(encoding="utf-8")
    return (
        f"/* Backdrop for seed {seed!r}, generated by michel-albert-sphinx. */\n"
        f":root {{\n  --ma-pattern: {_svg_url(lines)};\n  --ma-pattern-accent: {_svg_url(accent)};\n}}\n"
        + rules
    )


def _write_backdrop(app: Sphinx, exception: Exception | None) -> None:
    if exception is None and app.config.michel_albert_backdrop and app.builder.format == "html":
        static = Path(app.outdir) / "_static"
        static.mkdir(parents=True, exist_ok=True)
        (static / BACKDROP_CSS).write_text(_backdrop_css(app.config), encoding="utf-8")


def _add_backdrop(app: Sphinx) -> None:
    if app.config.michel_albert_backdrop and app.builder.format == "html":
        app.add_css_file(BACKDROP_CSS, priority=910)


def setup(app: Sphinx) -> dict[str, Any]:
    app.setup_extension("sphinx_immaterial")
    app.add_config_value("michel_albert_margin_notes", True, "html", bool)
    app.add_config_value("michel_albert_home_header", True, "html", bool)
    app.add_config_value("michel_albert_backdrop", True, "html", bool)
    app.add_config_value("michel_albert_backdrop_seed", None, "html", (str, type(None)))
    app.add_post_transform(MarginNotes)
    app.add_post_transform(StartPageLede)
    app.connect("config-inited", _configure, priority=400)
    app.connect("builder-inited", _add_backdrop)
    app.connect("build-finished", _write_backdrop)
    app.add_css_file("michel-albert.css", priority=900)
    app.add_js_file("michel-albert.js", priority=900)
    return {"version": __version__, "parallel_read_safe": True, "parallel_write_safe": True}
