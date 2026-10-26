Usage
=====

Install
-------

Add the package to the project's documentation dependencies:

.. code-block:: toml

   [project.optional-dependencies]
   docs = ["michel-albert-sphinx @ git+https://github.com/exhuma/michel-albert-sphinx@v0.1.0"]

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

Change the look
---------------

Don't add CSS to a project. Change this package instead:

1. Update ``src/michel_albert_sphinx/tokens.json`` from the design system, or
   edit ``styles/base.css`` or ``styles/immaterial.css``.
2. Run ``python scripts/generate_css.py``.
3. Run the tests, bump the version and tag a release.

.. autofunction:: michel_albert_sphinx.setup
