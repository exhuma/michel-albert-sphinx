"""Michel Albert's design system for Sphinx documentation.

Add ``"michel_albert_sphinx"`` to ``extensions`` in ``conf.py``. The extension

* enables the ``sphinx_immaterial`` theme,
* applies the design system's colours, type and shapes (light and dark),
* ships its own fonts, so pages make no requests to Google Fonts,
* makes overflowing code blocks reachable by keyboard.
"""

from __future__ import annotations

from importlib.metadata import PackageNotFoundError, version
from pathlib import Path
from typing import Any

from sphinx.application import Sphinx
from sphinx.config import Config
from sphinx.util import logging

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


def setup(app: Sphinx) -> dict[str, Any]:
    app.setup_extension("sphinx_immaterial")
    app.connect("config-inited", _configure, priority=400)
    app.add_css_file("michel-albert.css", priority=900)
    app.add_js_file("michel-albert.js", priority=900)
    return {"version": __version__, "parallel_read_safe": True, "parallel_write_safe": True}
