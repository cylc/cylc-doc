.. _User Guide Configuration:

Workflow Configuration
======================

Cylc suites are defined in structured, validated, :cylc:conf:`flow.cylc`
files that concisely specify the properties of, and the relationships
between, the various tasks managed by the suite.

Here we will look at:

- Folders which may (optionally) accompany a workflow configuration.
- The contents of the :cylc:conf:`flow.cylc` file.
- How to configure workflows.


.. _SuiteDefinitionDirectories:

Suite Configuration Directories
-------------------------------

A Cylc :term:`suite directory` contains:

:cylc:conf:`flow.cylc`
   The file which configures the workflow.
``bin/`` (optional)
   A directory where you can put scripts and executables for use
   in the workflow. It is automatically added to ``$PATH`` in the job
   execution environment.

   Alternatively, tasks can call external commands; or they can be
   scripted entirely within the flow.cylc file.
``lib/python/`` (optional)
   A directory for Python modules which can be used for:

   - Tasks; this directory is automatically added to ``$PYTHONPATH``
     in the job execution environment.
   - Custom :ref:`job submission modules <CustomJobSubmissionMethods>`.
   - Custom :ref:`Jinja2 Filters<CustomJinja2Filters>`).

Other files and folders may be placed in the :term:`suite directory` e.g.
documentation, configuration files, etc.


.. _FlowConfigFile:

flow.cylc File Overview
-----------------------

The :cylc:conf:`flow.cylc` file is written in a nested `INI`_-based format.

.. _template processors: https://en.wikipedia.org/wiki/Template_processor

Cylc supports two `template processors`_ for use in the flow.cylc file:

* `Jinja2`_
* `EmPy`_


.. _Syntax:

Syntax
^^^^^^

The following defines legal :cylc:conf:`flow.cylc` syntax:

- **Items** are of the form ``item = value``.
- **[Section]** headings are enclosed in square brackets.
- **Sub-section [[nesting]]** is defined by repeated square brackets.

  - Sections are **closed** by the next section heading.

- **Comments** (line and trailing) follow a hash character: ``#``
- **List values** are comma-separated.
- **Single-line string values** can be single-, double-, or un-quoted.
- **Multi-line string values** are triple-quoted (using
  single or double quote characters).
- **Boolean values** are capitalized: True, False.
- **Leading and trailing whitespace** is ignored.
- **Indentation** is optional but should be used for clarity.
- **Continuation lines** follow a trailing backslash: ``\``
- **Duplicate sections** add their items to those previously
  defined under the same section.
- **Duplicate items** override, *except for dependency
  ``graph`` strings, which are additive*.
- **Include-files** ``%include inc/foo.cylc`` can be
  used as a verbatim inlining mechanism.

Suites that embed templating code (see :ref:`User Guide Jinja2` and
:ref:`User Guide EmPy`) must process to raw :cylc:conf:`flow.cylc` syntax.


Include-Files
^^^^^^^^^^^^^

Cylc has native support for :cylc:conf:`flow.cylc` include-files, which may help to
organize large suites. Inclusion boundaries are completely arbitrary -
you can think of include-files as chunks of the :cylc:conf:`flow.cylc` file simply
cut-and-pasted into another file. Include-files may be included
multiple times in the same file, and even nested. Include-file paths
can be specified portably relative to the suite configuration directory,
e.g.:

.. code-block:: cylc

   # include the file inc/foo.cylc:
   %include inc/foo.cylc

.. note::

   Template processors may have their own include functionality
   which can also be used.

.. note::

   Cylc's native file inclusion mechanism supports optional inlined
   editing:

   .. code-block:: bash

      $ cylc edit --inline SUITE

   The suite will be split back into its constituent include-files when you
   exit the edit session. While editing, the inlined file becomes the
   official suite configuration so that changes take effect whenever you save
   the file. See ``cylc prep edit --help`` for more information.


.. _SyntaxHighlighting:

Syntax Highlighting For Suite Configuration
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Cylc provides syntax plugins for the following editors:

.. _Cylc.tmbundle: https://github.com/cylc/Cylc.tmbundle
.. _vscode-cylc: https://marketplace.visualstudio.com/items?itemName=cylc.vscode-cylc
.. _language-cylc: https://atom.io/packages/language-cylc

Atom
   install the `language-cylc`_ extension.
Emacs
   The syntax file can be obtained from the Cylc library by
   running the following command
   ``cylc extract-resources . etc/syntax/cylc-mode.el``
   installation instructions are at the top of the file.
Gedit
   The syntax file can be obtained from the Cylc library by
   running the following command
   ``cylc extract-resources . etc/syntax/cylc.lang``
   installation instructions are at the top of the file.
Kate
   The syntax file can be obtained from the Cylc library by
   running the following command
   ``cylc extract-resources . etc/syntax/cylc.xml``
   installation instructions are at the top of the file.
PyCharm
   Install the `Cylc.tmbundle`_.
Vim
   The syntax file can be obtained from the Cylc library by
   running the following command
   ``cylc extract-resources . etc/syntax/cylc.vim``
   installation instructions are at the top of the file.
Visual Studio Code
   Install the `vscode-cylc`_ extension.
Sublime Text 3
   Install the `Cylc.tmbundle`_.
TextMate
   Install the `Cylc.tmbundle`_.
WebStorm
      Install the `Cylc.tmbundle`_.

Gross File Structure
^^^^^^^^^^^^^^^^^^^^

Cylc :cylc:conf:`flow.cylc` files consist of configuration items grouped under
several top level section headings:

:cylc:conf:`[meta]`
   Information about the workflow e.g. title and description.
:cylc:conf:`[scheduler]`
   Non task-specific workflow configuration.
:cylc:conf:`[scheduling]`
   Determines when tasks are ready to run.

   - special scheduling constraints e.g.
     :ref:`external triggers <Section External Triggers>`.
   - the dependency graph, which defines the relationships
     between tasks
:cylc:conf:`[runtime]`
   Determines how, where, and what to execute when tasks are ready

   - script, environment, job submission, remote hosting, etc.
   - suite-wide defaults in the *root* namespace
   - a nested family hierarchy with common properties
     inherited by related tasks
:cylc:conf:`[visualization]`
   Suite graph styling

.. _Validation:

Validation
^^^^^^^^^^

The ``cylc validate`` command evaluates the :cylc:conf:`flow.cylc` file
against a specification that defines all legal entries, values and options.
It also performs some integrity checks designed to catch certain configuration
issues and impossible scheduling constraints.

These checks are also performed by ``cylc run`` before starting a workflow.

All legal entries are documented in :cylc:conf:`flow.cylc`.

If the :cylc:conf:`flow.cylc` file uses include-files ``cylc view`` will
show an inlined copy of the suite with correct line numbers
(you can also edit suites in a temporarily inlined state with
``cylc edit --inline``).
