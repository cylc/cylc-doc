.. _User Guide Configuration:

Workflow Configuration
======================

.. _FlowConfigFile:

The ``flow.cylc`` File
----------------------

Cylc workflows are defined in :cylc:conf:`flow.cylc` files that specify the
tasks to be managed by the Cylc scheduler, the dependencies between them,
and the schedules to run time on.

General file syntax is described in the :ref:`File Format Reference
<file-format>`.

Legal configuration settings are documented in :ref:`workflow-configuration`.

.. _template processors: https://en.wikipedia.org/wiki/Template_processor

Cylc also supports two `template processors`_ for use in the ``flow.cylc`` file:

* `Jinja2`_
* `EmPy`_


.. _WorkflowDefinitionDirectories:

Workflow Configuration Directories
----------------------------------

A Cylc :term:`source directory` contains:

:cylc:conf:`flow.cylc`
   The file which configures the workflow.

``bin/`` (optional)
   A directory for scripts and executables used by workflow tasks. It is
   added to ``$PATH`` in job environments.

   Jobs can also run scripting defined in the :cylc:conf:`flow.cylc` file,
   executables installed to user-defined locations of the workflow run
   directory, and external executables.

``lib/python/`` (optional)
   A directory for Python modules. It is added to ``$PYTHONPATH`` in
   the scheduler and job execution environments. It can be used by:

   - Tasks
   - Custom :ref:`job submission modules <CustomJobSubmissionMethods>`
   - Custom :ref:`Jinja2 Filters<CustomJinja2Filters>`

Other files and folders may be placed in the :term:`source directory` too:
documentation, configuration files, etc. When the workflow is :ref:`installed
<Installing-workflows>` these will be copied over to the :term:`run directory`.

.. note::

   If your workflow needs to create or install scripts or executables at runtime
   and you don't want Cylc to delete them on re-installation, you can use
   equivalent directories in the :ref:`workflow_share_directories`.


.. _SyntaxHighlighting:

Syntax Highlighting For Workflow Configuration
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Cylc provides syntax plugins for the following editors:

.. _language-cylc: https://github.com/cylc/language-cylc
.. _Cylc.tmbundle: https://github.com/cylc/Cylc.tmbundle
.. _vscode-cylc: https://marketplace.visualstudio.com/items?itemName=cylc.vscode-cylc

Atom
   install the `language-cylc`_ extension.
Emacs
   The syntax file can be obtained from the Cylc library by
   running the following command
   ``cylc get-resources syntax/cylc-mode.el .``
   installation instructions are at the top of the file.
Gedit
   The syntax file can be obtained from the Cylc library by
   running the following command
   ``cylc get-resources syntax/cylc.lang .``
   installation instructions are at the top of the file.
Kate
   The syntax file can be obtained from the Cylc library by
   running the following command
   ``cylc get-resources syntax/cylc.xml .``
   installation instructions are at the top of the file.
PyCharm
   Install the `Cylc.tmbundle`_.
Vim
   The syntax file can be obtained from the Cylc library by
   running the following command
   ``cylc get-resources syntax/cylc.vim .``
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

.. _cylc_lint_script:

``cylc lint``
^^^^^^^^^^^^^

.. seealso::

   :ref:`How to configure Cylc lint at project level <lint.pyproject.toml>`
   using a ``pyproject.toml``.

.. automodule:: cylc.flow.scripts.lint

.. _lint.pyproject.toml:

Configure ``cylc lint`` at project level
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

You can configure ``cylc lint`` for each workflow using a
``pyproject.toml`` file.

To define settings for ``cylc lint`` use a ``[cylc-lint]`` section.
Within the ``[cylc-lint]`` section you may define the following:

rulesets
   A list of rulesets to use. If you run cylc lint without setting rulesets
   on the command line this value will override
   the default (``['728', 'style']``).

   Allowed Values: '728', 'style'

ignore
   Individual rules to ignore: A list of rule codes, such as ``S007``.

exclude
   A list of files or glob patterns for files which will not be checked.

max-line-length
   Set longest line length to permit in Cylc Configs for this project.
   If unset, line length is not checked.


An example ``pyproject.toml`` might look like this:

.. code-block:: toml

   [cylc-lint]
   # Enforce a line limit of 99 chars
   max-line-length = 99

   # Ignore style [S] rule 007 (It's good practice comment with a reason)
   ignore = ['S007']   # Family names start with lowercase in this workflow

   # Don't check files matching these globs
   exclude = ['history/*.old.cylc', 'someother.cylc']

   # By default check for style
   rulesets = ['style']

   [some-other-section]
   # Cylc lint won't pay any attention to this.
