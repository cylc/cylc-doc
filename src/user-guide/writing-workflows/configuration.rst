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


.. _CodeInCylcConfigurations:

Code in Workflow Configurations
-------------------------------

Cylc workflow configurations are not executable scripts or programs. Rather,
they configure, at start-up, the Cylc scheduler program to run a particular
workflow.

The scheduler understands a static syntax that contains only ``[section
headings]`` and configuration items of the form ``platform = hpc1``. These
configuration items are not even "variables" that can be referenced elsewhere
in the file. Some values may look complicated, but they are still just text
strings with content that is meaningful to the scheduler.

Nevertheless a `flow.cylc` file may appear to contain several kinds of embedded
code:

    - Python-like Jinja2 or EmPy code, such as ``{% set PLANET = "earth" %}``
    - Bash shell variable assignments such as ``PLANET=${PLANET:-earth}``
    - Bash shell scripting, such as ``script = "run-model.exe /path/to/data"``

The documentation below explains exactly what these mean in the context of a
workflow configuration, and when the code is evaluated.


Jinja2 (or EmPy) Code
^^^^^^^^^^^^^^^^^^^^^

If a `flow.cylc` file contains embedded blocks of Jinja2 code in curly
brackets (or the equivalent for EmPy) then it is actually a template for
programmatically generating the static configuration format required by the
scheduler.

The template processor manipulates the surrounding text (which to it is
entirely arbitrary) and the result must be valid configuration syntax that
will pass validation by Cylc.

This is a preprocessing step. Jinja2 code does not execute as the workflow runs.

Use ``cylc view -j`` to see the result, with all Jinja2 code "processed out".

Note that the template processor does not have access to config items from the
surrounding text:

.. code-block:: cylc

   # flow.cylc
   platform = hpc1  # Cylc config item definition
   {{ "Platform is: " ~ platform }}  # ERROR, platform not defined as Jinja2!

However, you can assign a value to a Jinja2 variable and print it to the file
wherever it is needed:

.. code-block:: cylc

   # flow.cylc
   {% set PLATFORM = "hpc1" %}
   platform = {{ PLATFORM }}  # OK
   {{ "Platform is: " ~ PLATFORM }} # OK
 
Jinja2 code does not have access to the environment via normal shell syntax
either, but you can read the local environment with native Jinja2 syntax:

.. code-block:: cylc

   # flow.cylc
   {{ $HOME }}  # ERROR, $HOME is not defined (as a Jinja2 variable)!
   {{ "$HOME" }}  # OK, prints the literal string "$HOME"
   {{ environ["HOME"] }}  # OK, prints the value of $HOME

Note however that this code executes during file parsing, at start-up, on the
scheduler run host, because that is when template preprocessing is done. It
does not read the environment at run time on the job host, even if the
code appears in (i.e., writes to) a task definition section of the workflow.

Similarly, any Jinja2 access (via Python) to the filesystem will happen during
file parsing on the scheduler run host, not when jobs run on job hosts.


Environment Variables and Shell Scripting
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Cylc generates Bash shell job scripts to implement the task definitions in your
``flow.cylc``. These task definitions may configure environment variables and
fragments of shell scripting to be written to the job script. 

Cylc itself does not evaluate this shell syntax during file parsing at start-up,
or at run time. To the scheduler, these are just text strings to be written
verbatim to job scripts. They will only be evaluated, by the shell, when
the job script runs on the job host.

For example, here a config item called ``ARCHIVE`` is assigned the literal
string value ``"$HOME/archive"``:

.. code-block:: cylc

   # flow.cylc
   [[[environment]]]
      ARCHIVE = "$HOME/archive"

The shell variable ``$HOME`` does not get evaluated by Cylc, because a
``flow.cylc`` file is not a shell script. However, the scheduler knows
that config items in this section are to be written to corresponding shell
variable assignment expressions in the job script, using correct Bash syntax:

.. code-block:: cylc

    # job script
    ARCHIVE=$HOME/archive
    export ARCHIVE

Again, this code will be evaluated by the shell when the job script runs on the
job host.

Beware of using Jinja2 to print environment variable values in task definitions.
This may not be what you want because template preprocessing occurs at start-up
on the scheduler run host, not in the job environment on the job host.

.. code-block:: cylc

   # flow.cylc
   [[my-task]]
      [[[environment]]]
         ARCHIVE = {{ environ["HOME"] }}/archive  # BUG? (HOME not on job host!)


.. _SyntaxHighlighting:

Syntax Highlighting For Workflow Configuration
----------------------------------------------

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

.. automodule:: cylc.flow.scripts.lint

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
