---
name: sphinx-docs
description: Use whenever you create, set up, build, migrate or restyle Sphinx documentation (conf.py, docs/ folder, .rst pages, Read the Docs config) in one of Michel Albert's projects. Applies his design system through the michel-albert-sphinx package on the sphinx-immaterial theme, and his writing rules for docs.
---

# Sphinx documentation in Michel's identity

All of Michel's Sphinx documentation uses one look: his design system on the
`sphinx_immaterial` theme, delivered by the `michel-albert-sphinx` package
(https://github.com/exhuma/michel-albert-sphinx). The package owns every visual
decision. Projects only add it as an extension.

## Rules

- Use the extension `michel_albert_sphinx`. Do not set `html_theme`; the
  extension selects `sphinx_immaterial` itself.
- Never add styling to a project: no `html_css_files`, no `_static/*.css`, no
  template overrides, no `font` or `palette` theme options, no `pygments_style`.
  If something looks wrong, tell Michel and propose the change for the package
  repository instead.
- Other `sphinx_immaterial` options (features, repo links, edit links) are fine
  in a project's `html_theme_options`.
- Do not switch a project from another generator (MkDocs, plain Markdown) to
  Sphinx without asking.

## Set up docs in a project

1. Find the newest release tag:
   `git ls-remote --tags --refs https://github.com/exhuma/michel-albert-sphinx`
   and use the highest `vX.Y.Z`.
2. Add the docs dependency in `pyproject.toml` (create the extra if missing):

   ```toml
   [project.optional-dependencies]
   docs = ["michel-albert-sphinx @ git+https://github.com/exhuma/michel-albert-sphinx@vX.Y.Z"]
   ```

   If the project manages docs dependencies elsewhere (`docs/requirements.txt`,
   a uv dependency group), add the same requirement there instead.
3. Create `docs/conf.py`:

   ```python
   project = "<project name>"
   author = "Michel Albert"
   copyright = "<year>, Michel Albert"

   extensions = [
       "sphinx.ext.autodoc",       # only for Python packages with an API to document
       "michel_albert_sphinx",
   ]
   ```

4. Create `docs/index.rst` with a one-paragraph summary of what the project
   does and a `toctree` of the pages.
5. If the project has `.readthedocs.yaml`, make sure it installs the `docs`
   extra (`python.install: - method: pip, path: ., extra_requirements: [docs]`).

## Migrate existing Sphinx docs

1. Add the dependency as above and `"michel_albert_sphinx"` to `extensions`.
2. Remove `html_theme`, any theme-specific `html_theme_options` from the old
   theme, `html_css_files`, `html_style`, `pygments_style`, and custom CSS or
   templates that only restyle. Keep content, extensions and real
   functionality (for example a custom template that adds a page, not a look).
3. Remove the old theme package from the docs dependencies.
4. Tell Michel what you removed.

## Writing the pages

Follow the design system's content rules:

- Write plainly and directly. Short sentences. Say what a thing does, then stop.
- Docs address no one and use imperatives ("Install the package", not "You can
  install the package").
- Sentence case for every heading. No emoji, no exclamation marks, no marketing
  adjectives. Quote real names, paths and numbers.
- Callouts: `note` for neutral information, `tip` for a recommended or
  confirmed path, `warning` for something to check, `danger` for something that
  fails or breaks. Use them sparingly.
- Margin notes: a `note`, `tip`, `hint` or `seealso` placed directly after a
  paragraph or list appears beside it in the margin on wide screens. Put each
  note right after the paragraph it qualifies, keep it short (a few sentences),
  and use it for asides the reader can skip. Anything the reader must not miss
  is a `warning` or `danger`, which always stays in the text. A note after a
  code block or table stays in the text; to force that elsewhere, add
  `:class: ma-inline`.
- The start page's first paragraph is shown as a lede: make it a one-paragraph
  summary of what the project does.
- Code blocks: always give a language (`.. code-block:: python`, `console` for
  shell sessions with a `$` prompt). Long lines are fine; code never wraps and
  scrolls inside its block, so do not hand-break lines to fit.
- Keep headings shallow: page title, sections, at most one level below.

## Build and check

Build with warnings as errors and fix every warning before you finish:

```console
sphinx-build -W --keep-going -b html docs docs/_build/html
```

Then check the output:

- The pages use `sphinx_immaterial` (the HTML contains `md-header`) and link
  `_static/michel-albert.css`.
- No page references `fonts.googleapis.com`.
- The build printed no warning about `html_theme`; if it did, a theme is still
  set somewhere in `conf.py`.

Add `docs/_build/` to `.gitignore` if it is not there.
