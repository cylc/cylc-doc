.. _style_guide:

Style Guidelines
================

Coding style is largely subjective, but for collaborative development of
complex systems it is important to settle on a clear and consistent style to
avoid getting into a mess. The following style rules are recommended.

.. seealso::

   :ref:`cylc lint -r style <cylc_lint_script>` is a tool designed to help
   you check your code style.

Tab Characters
--------------

Do not use tab characters. Tab width depends on editor settings, so a mixture
of tabs and spaces in the same file can render to a mess.

Use ``grep -InPr "\t" *`` to find tabs recursively in files in
a directory.

In *vim* use ``%retab`` to convert existing tabs to spaces,
and set ``expandtab`` to automatically convert new tabs.

In *emacs* use *whitespace-cleanup*.

In *gedit*, use the *Draw Spaces* plugin to display tabs and spaces.


Trailing Whitespace
-------------------

Trailing whitespace is untidy, it makes quick reformatting of paragraphs
difficult, and it can result in hard-to-find bugs (space after intended
line continuation markers).

To remove existing trailing whitespace in a file use a ``sed`` or
``perl`` one-liner:

.. code-block:: console

   $ perl -pi -e "s/ +$//g" /path/to/file
   # or:
   $ sed --in-place 's/[[:space:]]\+$//' path/to/file

Or do a similar search-and-replace operation in your editor. Editors like
*vim* and *emacs* can also be configured to highlight or automatically
remove trailing whitespace on the fly.


Indentation
-----------

Consistent indentation makes a workflow definition more readable, it shows section
nesting clearly, and it makes block re-indentation operations easier in text
editors. Indent :cylc:conf:`flow.cylc` syntax four spaces per nesting level:


Settings (Config Items)
^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: cylc

   [SECTION]
       # A comment.
       title = the quick brown fox
       [[SUBSECTION]]
           # Another comment.
           a short item = value1
           a very very long item = value2

Don't align ``item = value`` pairs on the ``=`` character
like this:

.. code-block:: cylc

   [SECTION]  # Avoid this.
                a short item = value1
       a very very long item = value2

or like this:

.. code-block:: cylc

   [SECTION]  # Avoid this.
       a short item          = value1
       a very very long item = value2

because the whole block may need re-indenting after a single change, which will
pollute your revision history with spurious changes.

Comments should be indented to the same level as the section or item they refer
to, and trailing comments should be preceded by two spaces, as shown above.


Script String Lines
^^^^^^^^^^^^^^^^^^^

Script strings are written verbatim to :term:`job scripts <job script>`.

.. code-block:: cylc

   [runtime]
       [[foo]]
           script = echo "Hello, Mr. Thompson"

If using a triple-quoted string, any common leading whitespace is trimmed
using the logic of :py:func:`textwrap.dedent`. As such, it is recommended to
indent like any other triple-quoted string setting in Cylc:

.. code-block:: cylc

   [runtime]
       [[foo]]
           # Recommended.
           script = """
               if [[ "$RESULT" == "bad" ]]; then
                   echo "Goodbye World!"
                   exit 1
               fi
           """

The example above would result in the following being written to the job
script:

.. code-block:: bash

   if [[ "$RESULT" == "bad" ]]; then
       echo "Goodbye World!"
       exit 1
   fi

.. tip::

   Take care when indenting here documents (aka heredocs) to match the
   common leading whitespace.

   For the following example, each line in ``log.txt`` would end up with
   4 leading white spaces:

   .. code-block:: cylc

      [runtime]
          [[foo]]
           script = """
               cat >> log.txt <<_EOF_
                   The quick brown fox jumped
                   over the lazy dog.
               _EOF_
           """

   The following will give you lines with no white spaces:

   .. code-block:: cylc

      [runtime]
          [[foo]]
           script = """
               cat >> log.txt <<_EOF_
               The quick brown fox jumped
               over the lazy dog.
               _EOF_
           """

Graph String Lines
^^^^^^^^^^^^^^^^^^

Whitespace is ignored in graph string parsing so internal graph lines
should be indented as if part of the :cylc:conf:`flow.cylc` syntax:

.. code-block:: cylc

   [scheduling]
       [[graph]]
           R1 = """
               # Main workflow:
               FAMILY:succeed-all => bar & baz => qux

               # Housekeeping:
               qux => rose_arch => rose_prune
           """


Jinja2 Code
^^^^^^^^^^^

A :cylc:conf:`flow.cylc` file with embedded Jinja2 code is essentially a Jinja2 program to
generate a Cylc workflow definition. It is not possible to consistently indent the
Jinja2 as if it were part of the :cylc:conf:`flow.cylc` syntax (which to the Jinja2 processor
is just arbitrary text), so it should be indented from the left margin on
its own terms:

.. code-block:: cylc

   [runtime]
       [[OPS]]
   {% for T in OPS_TASKS %}
       {% for M in range(M_MAX) %}
       [[ops_{{T}}_{{M}}]]
           inherit = OPS
       {% endfor %}
   {% endfor %}


Comments
--------

Comments should be minimal, but not too minimal. If context and clear
task and variable names will do, leave it at that. Extremely verbose comments
tend to get out of sync with the code they describe, which can be worse
than having no comments.

Avoid long lists of numbered comments - future changes may require mass
renumbering.

Avoid page-width "section divider" comments, especially if they are not
strictly limited to the standard line length (see :ref:`Line Length`).

Indent comments to the same level as the config items they describe.


Titles, Descriptions, And URLs
------------------------------

Document the workflow and its tasks with ``title``,
``description``, and ``url`` items instead of comments.
See the :cylc:conf:`flow.cylc[meta]` and
:cylc:conf:`flow.cylc[runtime][<namespace>][meta]` sections.


.. _Line Length:

Line Length And Continuation
----------------------------

Keep to the standard maximum line length of 79 characters where possible. Very
long lines affect readability and make side-by-side diffs hard to view.

Backslash line continuation markers can be used anywhere in the :cylc:conf:`flow.cylc` file
but should be avoided if possible because they are easily broken by invisible
trailing whitespace.

Continuation markers are not needed in graph strings where trailing
trigger arrows and boolean operators imply line continuation:

.. code-block:: cylc

   [scheduling]
       [[graph]]
           # No line continuation marker is needed here.
           R1 = """
               prep => one => two => three =>
               four => five six => seven => eight &
               nine & ten =>
               eleven |
               twelve
           """
   [runtime]
       [[MY_TASKS]]
       # A line continuation marker *is* needed here:
       [[one, two, three, four, five, six, seven, eight, nine, ten, \
         eleven, twelve, thirteen]]
           inherit = MY_TASKS


Task Naming Conventions
-----------------------

Use ``UPPERCASE`` for family names and ``lowercase``
for tasks, so you can distinguish them at a glance.

Choose a convention for multi-component names and use it consistently. Put the
most general name components first for natural grouping, e.g.
``obs_sonde``, ``obs_radar`` (not ``sonde_obs`` etc.)

Within your convention keep names as short as possible.


UM System Task Names
^^^^^^^^^^^^^^^^^^^^

For UM System workflows we recommend the following full task naming convention:

.. code-block:: none

   model_system_function[_member]

For example, ``glu_ops_process_scatwind`` where ``glu`` refers
to the global (deterministic model) update run, ``ops`` is the system
that owns the task, and ``process_scatwind`` is the function it
performs. The optional ``member`` suffix is intended for use with
ensembles as needed.

Within this convention keep names as short as possible, e.g. use
``fcst`` instead of ``forecast``.

UM forecast apps should be given names that reflect their general science
configuration rather than geographic domain, to allow use on other model
domains without causing confusion.


Rose Config Files
-----------------

Use ``rose config-dump`` to load and re-save new ``rose.conf`` files. This
puts the files in a standard format (ordering of lines etc.) to ensure that
spurious changes aren't generated when you next use ``rose edit``.

See also :ref:`Optional App Config Files` on optional app config files.
