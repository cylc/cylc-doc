.. _User Guide Configuration:

Workflow Configuration
======================

Cylc workflows are defined in structured, validated, :cylc:conf:`flow.cylc`
files that specify the properties of, and the relationships between, the
various tasks to be managed by the Cylc scheduler.

Here we will look at:

- Folders which may accompany a workflow configuration.
- The content of the :cylc:conf:`flow.cylc` file.
- How to configure workflows.


.. _WorkflowDefinitionDirectories:

Workflow Configuration Directories
----------------------------------

A Cylc :term:`source directory` contains:

:cylc:conf:`flow.cylc`
   The file which configures the workflow.

``bin/`` (optional)
   A directory for scripts and executables used by workflow tasks. It is
   added to ``$PATH`` in task job environments.

   Task jobs can also run scripting defined in the ``flow.cylc`` file,
   executables installed to user-defined locations of the workflow run
   directory, and external excutables.

``lib/python/`` (optional)
   A directory for Python modules. It is added to ``$PYTHONPATH`` in
   the scheduler and task job execution environments. It can be used by:

   - Task jobs
   - Custom :ref:`job submission modules <CustomJobSubmissionMethods>`
   - Custom :ref:`Jinja2 Filters<CustomJinja2Filters>`

Other files and folders may be placed in the :term:`source directory` too:
documentation, configuration files, etc. When the workflow is :ref:`installed
<Installing-workflows>` these will be copied over to the :term:`run directory`.

.. _FlowConfigFile:

flow.cylc File Overview
-----------------------

The :cylc:conf:`flow.cylc` file is written in a nested `INI`_-based format.

.. _template processors: https://en.wikipedia.org/wiki/Template_processor

Cylc also supports two `template processors`_ for use in the ``flow.cylc`` file:

* `Jinja2`_
* `EmPy`_


.. _Syntax:

Syntax
^^^^^^

:cylc:conf:`flow.cylc` syntax, in general terms:

- **Settings** (config items) are of the form ``item = value``.
- **[Section]** headings are enclosed in square brackets.

  - **Sub-section [[nesting]]** is defined by repeated square brackets.
  - Sections are **closed** implicitly by the next section heading.

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
- **Duplicate items** override, except for ``graph`` strings, which are
  additive.
- **Include-files** ``%include inc/foo.cylc`` can be used as a verbatim
  inlining mechanism.

Workflows that embed templating code (see :ref:`User Guide Jinja2` and
:ref:`User Guide EmPy`) must process to raw :cylc:conf:`flow.cylc` syntax.


Include-Files
^^^^^^^^^^^^^

Cylc has native support for :cylc:conf:`flow.cylc` include-files, which may help to
organize large workflows. Inclusion boundaries are completely arbitrary -
you can think of include-files as chunks of the :cylc:conf:`flow.cylc` file simply
cut-and-pasted into another file. Include-files may be included
multiple times in the same file, and even nested. Include-file paths
can be specified portably relative to the workflow configuration directory,
e.g.:

.. code-block:: cylc

   # include the file ~/cylc-run/workflow/inc/foo.cylc:
   %include inc/foo.cylc

.. note::

   Template processors may have their own include functionality
   which can also be used.


.. _SyntaxHighlighting:

Syntax Highlighting For Workflow Configuration
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

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
   - workflow-wide defaults in the *root* family
   - a nested family hierarchy with common properties
     inherited by related tasks

.. _Validation:

Validation
^^^^^^^^^^

The ``cylc validate`` command evaluates the :cylc:conf:`flow.cylc` file
against a specification that defines all legal entries, values and options.
It also performs some integrity checks designed to catch certain configuration
issues and impossible scheduling constraints.

These checks are also performed by ``cylc play`` before starting a workflow.

All legal entries are documented in the :cylc:conf:`flow.cylc` reference.

If a :cylc:conf:`flow.cylc` file uses include-files ``cylc view`` will
show an inlined copy of the workflow with correct line numbers.
