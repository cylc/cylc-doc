Python 2 => 3
=============

.. admonition:: Does This Change Affect Me?
   :class: tip

   This change will affect you if your workflows extend Cylc or Jinja2 with
   custom Python scripts.

   This does not impact :term:`task` scripts, Cylc can still run Python 2
   tasks if desired.


Overview
--------

.. _six: https://pypi.org/project/six/

Cylc 7 ran under Python 2, Cylc 8 runs under Python 3.

Cylc can be extended with custom Python scripts. These scripts are run under
the same version of Python used by Cylc.

As a result if you are moving from Cylc 7 to Cylc 8 you must upgrade any
scripts from Python 2 to Python 3 in the process.

If you want to support both Cylc 7 and 8 you must support both Python 2 and 3.
There are tools to help you do this. E.g. `six`_.


Impacted Scripts
----------------

The following scripts must be upgraded if used:

:ref:`CustomJinja2Filters`
   These allow you to extend Jinja2 with Python code.

   These scripts are located in the following directories within a workflow:

   * Jinja2Filters
   * Jinja2Tests
   * Jinja2Globals

:ref:`Modules imported by Jinja2 <jinja2.importing_python_modules>`
   Python modules can be imported from Jinja2 e.g:

   .. code-block:: jinja

      {% from "os" import path %}

:ref:`Custom Trigger Functions`
   Any custom x-trigger functions.


Package Name Changes
--------------------

Three Python packages have been renamed between Cylc 7 and Cylc 8:

* ``cylc`` => ``cylc.flow``
* ``isodatetime`` => ``metomi.isodatetime``
* ``rose`` => ``metomi.rose``

If you are importing from these packages you will need to update the package names.

Here are some examples:

.. rubric:: Convert Python code from Cylc 7 to Cylc 8:

.. code-block:: diff

   - from cylc import LOG
   + from cylc.flow import LOG
   - from isodatetime.data import Duration
   + from metomi.isodatetime.data import Duration

.. rubric:: Python code which supports both Cylc 7 & Cylc 8:

.. code-block:: python

   import sys
   if sys.version[0] == '3':
       from cylc.flow import LOG
       from metomi.isodatetime.data import Duration
   else:
       from cylc import LOG
       from isodatetime.data import Duration

.. rubric:: Convert Jinja2 code from Cylc 7 to Cylc 8:

.. code-block:: diff

   #!Jinja2
   - {% from "cylc" import LOG %}
   + {% from "cylc.flow" import LOG %}
     {% do LOG.debug("Hello World!") %}

.. rubric:: Jinja2 code which supports both Cylc 7 & Cylc 8:

.. code-block:: jinja

   #!Jinja2
   {% from "sys" import version -%}
   {% if version[0] == '3' -%}
       {% from "cylc.flow" import LOG -%}
   {% else -%}
       {% from "cylc" import LOG -%}
   {% endif -%}

   {% do LOG.debug("Hello World!") %}


Jinja2 - integers with leading zeros
------------------------------------

Integers with leading zeros in Jinja2 expressions are now illegal and will
cause an error like  ``Jinja2Error: expected token 'x', got 'integer'``.
For example:

.. code-block:: console

   $ cylc validate my-workflow
   Jinja2Error: expected token 'end of statement block', got 'integer'
   File ~/cylc-run/my-workflow/flow.cylc
     {% if START_HOUR == 06 or START_HOUR == 12 %}	 <-- TemplateSyntaxError

The solution in this case is:

.. code-block:: diff

   -{% if START_HOUR == 06 or START_HOUR == 12 %}
   +{% if START_HOUR == 6 or START_HOUR == 12 %}


Rose
----

The same changes also impact Rose extensions:

* :ref:`Rose Macros <rose:api-rose-macro>`
* :ref:`Rose Ana Tasks <rose:builtin.rose_ana>`
