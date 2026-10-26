# michel-albert-sphinx

Michel Albert's design system for Sphinx documentation. One line in `conf.py`
gives a project the same type, colours and shapes as the rest of the identity,
in light and dark, on the [sphinx-immaterial](https://jbms.github.io/sphinx-immaterial/) theme.

## Use it in a project

Add the dependency (pin a tag):

```toml
[project.optional-dependencies]
docs = ["michel-albert-sphinx @ git+https://github.com/exhuma/michel-albert-sphinx@v0.3.0"]
```

Add the extension to `conf.py` and leave `html_theme` unset:

```python
extensions = ["michel_albert_sphinx"]
```

Build with warnings as errors:

```console
sphinx-build -W --keep-going -b html docs docs/_build/html
```

The extension enables `sphinx_immaterial`, sets a light/dark palette that follows
the reader's OS, turns off Google Fonts (the fonts ship with the package), and adds
the stylesheet. A project's own `html_theme_options` win key by key.

## What it looks like

- Source Sans 3 for text, Source Code Pro for code, headings at weight 600.
- Warm brown neutrals, one teal accent, flat surfaces with 1px hairlines, 4px radii.
- Running text in a column of about 65 characters. Type grows with the screen
  (16 px on laptops, about 18, 19 and 22 px at 1600, 2000 and 2800 px wide); the
  line length in characters stays the same.
- One centred frame on every page: navigation, text, an optional margin and the
  table of contents. Navigation, header and search never move between pages.
- Notes, tips, hints and "see also" that follow a paragraph or list sit in the margin
  beside it on wide screens, and below it on narrow ones; reading order never changes.
  On pages with margin notes, code, tables and API signatures span text and margin.
- The start page's first paragraph is a lede with a clay band.
- On screens wider than the frame, the page is a raised sheet over topographic contour
  lines. The terrain is generated from the project name, so every project gets its own
  in the same style; the text never sits on the pattern.
- Links in running text are underlined; navigation links are not.
- Code and other preformatted text never wrap. Long lines scroll inside the block,
  which can be reached with Tab and scrolled with the arrow keys.
- Callouts: `note` (accent), `tip`/`hint` (done), `warning`/`caution` (check),
  `danger`/`error` (blocked).

`docs/style-reference.rst` shows every styled element on one page.

Options in `conf.py`:

| Setting | Default | Effect |
|---|---|---|
| `michel_albert_margin_notes` | `True` | Notes after prose go to the margin. |
| `michel_albert_home_header` | `True` | The start page's first paragraph is a lede. |
| `michel_albert_backdrop` | `True` | Contour-line backdrop outside the frame. |
| `michel_albert_backdrop_seed` | `project` | Seed for the backdrop's terrain. |

Give a single note `:class: ma-inline` to keep it in the text.

## Change the look

Never add CSS to a project; change it here.

1. Copy the design system's `project/tokens.json` to `src/michel_albert_sphinx/tokens.json`,
   or edit `styles/base.css` (content rules), `styles/immaterial.css` (theme colours)
   or `styles/layout.css` (sizes, columns, margin notes).
2. Regenerate the shipped stylesheet: `python scripts/generate_css.py`.
3. Run `pytest`. It checks WCAG contrast for every colour pair in both themes, builds
   these docs with `-W`, and fails if the generated stylesheet is stale.
4. Bump `version` in `pyproject.toml`, tag `vX.Y.Z`, push.

## Claude Code

This repository is also a Claude Code plugin marketplace. The `michel-albert-docs`
plugin adds a skill that makes Claude Code use this package whenever it creates,
builds or restyles Sphinx documentation.

```console
claude plugin marketplace add exhuma/michel-albert-sphinx
claude plugin install michel-albert-docs@michel-albert
```

## Licences

Code: MIT (see `LICENSE`). Fonts: SIL Open Font License 1.1
(`src/michel_albert_sphinx/static/fonts/OFL-*.txt`).
