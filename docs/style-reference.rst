Style reference
===============

Every element the design system styles, on one page. Use it to check a
change to the stylesheet in light and dark.

Running text
------------

Write plainly and directly. Short sentences. Say what a thing does, then
stop. Links in running text are underlined, like `this one to Sphinx
<https://www.sphinx-doc.org/>`_, and inline code such as ``sphinx-build``
sits on an inset ground. **Strong text** uses weight 600, never heavier.

- Lists keep the same 16/25 px rhythm as paragraphs.
- Second item, with a reference to :doc:`usage`.

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
