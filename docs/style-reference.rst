Style reference
===============

Every element the design system styles, on one page. Use it to check a
change to the stylesheet in light and dark.

Text is 18.5 px on laptops, with a line height of 1.62. On screens wider than
the frame, the page is a sheet with a soft halo, and the contour lines around
it fade toward the screen edges.

Running text
------------

Write plainly and directly. Short sentences. Say what a thing does, then
stop. Links in running text are underlined, like `this one to Sphinx
<https://www.sphinx-doc.org/>`_, and inline code such as ``sphinx-build``
sits on an inset ground. **Strong text** uses weight 600, never heavier.

- Lists keep the same rhythm as paragraphs.
- Second item, with a reference to :doc:`usage`.

.. note::

   This note follows the list, so on wide screens it sits in the margin
   beside it.

Margin notes
------------

A note, tip, hint or "see also" that directly follows a paragraph or a list
moves into the margin beside it on wide screens. On narrow screens it follows
the paragraph as a normal callout. Reading order is the same everywhere.

.. tip::

   Put a note right after the paragraph it belongs to.

.. seealso::

   A second note directly after the first stacks below it in the margin.

A note stays in the text when it follows code, a table or a heading, or when
it is nested in a list or another callout. Warnings and dangers always stay in
the text, where nobody can skip them.

.. note::
   :class: ma-inline

   The ``ma-inline`` class keeps this note in the text even though it follows
   a paragraph.

.. warning::

   A warning after a paragraph stays in the text.

Code
----

Code never wraps. Long lines scroll inside the block, and a block that
scrolls can be reached with Tab and scrolled with the arrow keys.

.. code-block:: python

   from http import HTTPStatus

   def check(response) -> bool:
       """Return True when the request succeeded."""
       # A deliberately long line, so this block scrolls sideways instead of wrapping onto a second line.
       return response.status_code == HTTPStatus.OK and response.headers.get("content-type", "").startswith("application/json")

.. code-block:: console

   $ sphinx-build -W --keep-going -b html docs docs/_build/html

Every syntax role has its own colour from the design system's ``code-*``
tokens: keywords, constants, built-ins, function and class names, keys,
decorators, strings, numbers, comments, operators, other names and errors.

.. code-block:: python

   from dataclasses import dataclass


   @dataclass(frozen=True)
   class Entry:
       """One directory entry."""

       dn: str
       retries: int = 3

       def name(self, raw: bytes) -> str:
           # decode, replacing what cannot be mapped
           text = raw.decode("t.61", errors="replace")
           if text is None or not text.strip():
               raise ValueError(f"empty name in {self.dn!r}")
           return text


   print(len(Entry("cn=cafe").name(b"Caf\xc2e")))

.. code-block:: yaml

   - name: Publish documentation
     hosts: vps
     vars:
       replicas: 2
       tls: true
       docs_root: /srv/docs

.. code-block:: json

   {"name": "t61codec", "aliases": ["t61", "t.61"], "strict": true, "replacement": null, "retries": 3}

.. code-block:: sql

   SELECT e.dn, count(*) AS failures
   FROM ldap_entry AS e
   WHERE e.active IS TRUE AND e.retries >= 3
   ORDER BY failures DESC;

Callouts
--------

.. note::

   Note: neutral information, tinted with the accent.

.. tip::

   Done: something worked, or a recommended path.

.. warning::

   Check: something to verify before going on.

.. danger::

   Blocked: something that fails or breaks.

Table
-----

=========  ========  ===========================================
Option     Default   Description
=========  ========  ===========================================
timeout    30        Seconds before a request is abandoned.
retries    3         Number of retry attempts on failure.
=========  ========  ===========================================

API entry
---------

.. py:function:: connect(host: str, port: int = 443, *, timeout: float = 30.0) -> Connection

   Open a connection to *host* on *port*.

   :param host: Host name or address.
   :param port: TCP port.
   :param timeout: Seconds before giving up.
   :returns: An open connection.
