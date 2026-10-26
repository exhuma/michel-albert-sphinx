Usage
=====

Install
-------

Add the package to the project's documentation dependencies:

.. code-block:: toml

   [project.optional-dependencies]
   docs = ["michel-albert-sphinx @ git+https://github.com/exhuma/michel-albert-sphinx@v0.3.1"]

Configure
---------

Add the extension to ``conf.py``. Leave ``html_theme`` unset: the extension
selects ``sphinx_immaterial`` itself.

.. code-block:: python

   extensions = [
       "michel_albert_sphinx",
   ]

Build with warnings treated as errors:

.. code-block:: console

   $ sphinx-build -W --keep-going -b html docs docs/_build/html

What the extension sets
-----------------------

- ``html_theme`` is ``sphinx_immaterial`` unless the project chose another
  theme, in which case the build warns.
- ``html_theme_options`` gets ``font: False`` and a light/dark palette that
  follows the reader's OS setting. Keys the project sets itself win.
- The stylesheet, the fonts and a small keyboard-scroll script are added to
  the static files.

Margin notes
------------

A ``note``, ``tip``, ``hint`` or ``seealso`` that directly follows a paragraph
or a list is set beside it in the margin on wide screens, and below it on
narrow screens. The build pairs the two in one block, so reading order is the
same for everyone. Several notes in a row stack in the margin.

A note stays in the text when it follows code, a table or a heading, or when it
sits inside a list or another callout. Warnings, cautions and dangers always
stay in the text. To keep one note in the text, give it a class:

.. code-block:: rst

   .. note::
      :class: ma-inline

      This note stays in the text.

Pages with margin notes get the margin column; code blocks, tables and API
signatures on those pages span the text and the margin.

Options
-------

``michel_albert_margin_notes``
   ``True`` by default. ``False`` keeps every note in the text.

``michel_albert_home_header``
   ``True`` by default. Styles the start page's first paragraph as a lede with
   a clay band. ``False`` turns it off.

``michel_albert_backdrop``
   ``True`` by default. On screens wider than the frame, the page sits on a
   raised sheet over contour lines. ``False`` turns it off.

``michel_albert_backdrop_seed``
   The contour lines are generated from this text, by default the ``project``
   name, so each project gets its own terrain. The same seed always gives the
   same lines.

Change the look
---------------

Don't add CSS to a project. Change this package instead:

1. Update ``src/michel_albert_sphinx/tokens.json`` from the design system, or
   edit ``styles/base.css``, ``styles/immaterial.css`` or ``styles/layout.css``.
2. Run ``python scripts/generate_css.py``.
3. Run the tests, bump the version and tag a release.

.. autofunction:: michel_albert_sphinx.setup
