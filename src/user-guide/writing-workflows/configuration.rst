.. _User Guide Configuration:

Workflow Configuration
======================

.. _FlowConfigFile:

The ``flow.cylc`` File
----------------------

Cylc workflows are defined in :cylc:conf:`flow.cylc` files that specify the
tasks to be managed by the Cylc scheduler, the dependencies between them,
and the schedules to run them to.

The ``.cylc`` file syntax is described in the :ref:`File Format Reference
<file-format>`.

The configurations you can use are documented in :ref:`workflow-configuration`.

.. _template processors: https://en.wikipedia.org/wiki/Template_processor

Cylc also supports the `Jinja2`_
`template processor <https://en.wikipedia.org/wiki/Template_processor>`_
for use in the `flow.cylc` file.


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
   - Custom :ref:`job runners <CustomJobSubmissionMethods>`
   - Custom :ref:`Jinja2 Filters<CustomJinja2Filters>`

Other files and folders
   Such as documentation, configuration files, etc.

When the workflow is :ref:`installed <Installing-workflows>`
these will be copied over to the :term:`run directory`.

.. note::

   If your workflow needs to create or install scripts or executables at runtime
   and you don't want Cylc to delete them on re-installation, you can use
   equivalent directories in the :ref:`workflow_share_directories`.


.. _UnderstandingCodeInCylcConfigurations:

Understanding Variables and Code in Workflow Configurations
-----------------------------------------------------------

A workflow configuration is not executable code. It configures the scheduler
program at startup to run your workflow.

Nevertheless, a `flow.cylc` file may contain:

- Embedded Python-like Jinja2 templating code, such as
  ``{% set PLANET = "earth" %}``
- Bash shell environment variable assignments and scripting, such as
  ``script = "run-model.exe $DATA_FILE"``

Jinja2 templating code gets executed as a preprocessing step when the
file is parsed. It can generate any part of a workflow configuration including
section headings, and item keys and values - so long as the result is valid
Cylc config.

To see the result of template processing:

.. code-block:: shell

    # print the workflow configuration, processed but not parsed:
    $ cylc view --process <workflow-id>

    # print the workflow configuration, processed and parsed:
    $ cylc config <workflow-id>

Here's an example of a simple Jinja2 template:

.. code-block:: cylc

    #!Jinja2
    {% set tasks = ["cat", "dog", "fish"] %}
    [scheduling]
        [[graph]]
            R1 = """
    {% for task in tasks %}
               start => {{task}} 
    {% endfor %}
            """
    [runtime]
        [[start]]
           script = "echo 'hello'"
    {% for task in tasks %}
        [[{{task}}]]
            script = "echo 'I am a {{task}}'"
    {% endfor %}

And the resulting workflow configuration:

.. code-block:: cylc

    [scheduling]
        [[graph]]
            R1 = """
                start => cat
                start => dog
                start => fish
            """
    [runtime]
        [[start]]
            script = "echo 'hello'"
        [[cat]]
            script = "echo 'I am a cat'"
        [[dog]]
            script = "echo 'I am a dog'"
        [[fish]]
            script = "echo 'I am a fish'"


Here's an example of (good and bad) use of a Jinja2 variable:

.. code-block:: cylc

    {% set OWNER = "bob-the-wizard" %}
    [runtime]
        # OK: this preprocesses to a valid task name "bob-the-wizard":
        [[{{OWNER}}]]
            # OK: this preprocesses to 'echo "I am bob-the-wizard"'
            # which will be written as a string to the job script.
            script = 'echo "I am {{OWNER}}"'
    # ERROR: [bob] is not a valid top-level Cylc config item:
    [{{OWNER}}]


The scheduler does not interpret shell syntax or environment variables
(it is not a shell script!) but certain string-valued config items may
contain shell code that gets written verbatim to job scripts. This code
will be evaluated by the Bash interpreter when (and where) the task job
runs.

Here's an example of (good and bad) use of a shell environment variable:

.. code-block:: cylc

    [runtime]
        # ERROR: the literal "${USER}-the-wizard" is not a valid task name:
        [[${USER}-the-wizard]]
            # OK: Bash will evaluate $OWNER and $USER when the task job runs:
            script = 'echo "I am $OWNER"'  # OK
            [[[environment]]]
                OWNER = "${USER}-the-wizard"  # OK


Note that Jinja2 code can also access the local environment during
template processing, when your `flow.cylc` file is parsed - *this may be
very different to task job environments.*:

.. code-block:: cylc

    {# This evaluates $USER immediately when the file is parsed. #}
    {% set OWNER = environ["USER"] ~ "-the-wizard" %}
    [runtime]
        # OK: generates a valid task name "bob-the-wizard":
        [[{{OWNER}}]]

Finally, here's an example of (good and bad) use of Jinja2 to generate strings
that reference task environment variables:

.. code-block:: cylc

    {# This does not evaluate $USER, it's just a string literal #}
    {% set OWNER = "${USER}-the-wizard" %}
    [runtime]
        # ERROR: literal "${USER}-the-wizard" is not a valid task name:
        [[{{OWNER}}]]
            # OK: this generates 'echo "my name is ${USER}-the-wizard"'.
            # Bash will evaluate "$USER" when the task job runs:
            script = 'echo "my name is {{OWNER}}"'


Some things to be aware of:

- Jinja2 code is evaluated once when the workflow is started.
- Jinja2 code can only reference Jinja2 variables, not Cylc config items
  (however Jinja2 can manipulate text to generate Cylc config items)
- Jinja2 (like Python) has its own syntax for reading environment variables.
- Jinja2 code that reads the environment or the filesystem will do so
  during config file parsing, not on task job hosts.
  Beware of doing this inside task definitions - do you want the scheduler
  environment to affect shell code that runs in the job environment?
- Shell code destined for task job scripts will read the environment or
  access the filesystem when the job runs on the job host, not on the
  scheduler host.


.. _SyntaxHighlighting:

Syntax Highlighting For Workflow Configuration
----------------------------------------------

Cylc provides syntax plugins for the following editors:

.. _language-cylc: https://github.com/cylc/language-cylc
.. _Cylc.tmbundle: https://github.com/cylc/Cylc.tmbundle
.. _vscode-cylc: https://marketplace.visualstudio.com/items?itemName=cylc.vscode-cylc
.. _cylc.vim: https://github.com/cylc/cylc.vim
.. _zed-cylc: https://github.com/elliotfontaine/zed-cylc

Atom & Pulsar
   Install the `language-cylc`_ extension.
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
Helix
   Built-in support.
Kate
   The syntax file can be obtained from the Cylc library by
   running the following command
   ``cylc get-resources syntax/cylc.xml .``
   installation instructions are at the top of the file.
Nano
   The syntax file can be obtained from the Cylc library by
   running the following command
   ``cylc get-resources syntax/cylc.nanorc ~/.config/nano``
   installation instructions are at the top of the file.
NeoVim
   Install the `cylc.vim`_ plugin.
PyCharm
   Install the `Cylc.tmbundle`_.
Vim
   Install the `cylc.vim`_ plugin.
Visual Studio Code
   Install the `vscode-cylc`_ extension.
Sublime Text 3
   Install the `Cylc.tmbundle`_.
TextMate
   Install the `Cylc.tmbundle`_.
WebStorm
   Install the `Cylc.tmbundle`_.
Zed
   Install the `zed-cylc`_ extension.


Gross File Structure
--------------------

Cylc :cylc:conf:`flow.cylc` files consist of configuration items grouped under
several top level section headings:

:cylc:conf:`[meta]`
   Information about the workflow e.g. title and description.
:cylc:conf:`[scheduler]`
   Non task-specific workflow configuration.
:cylc:conf:`[task parameters]`
   Parameters for use when defining graphs and tasks.
   See :ref:`user guide param`.
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
----------

The ``cylc validate`` command evaluates the :cylc:conf:`flow.cylc` file
against a specification that defines all legal entries, values and options.
It also performs some integrity checks designed to catch certain configuration
issues and impossible scheduling constraints.

These checks are also performed by ``cylc play`` before starting a workflow.

All legal entries are documented in the :cylc:conf:`flow.cylc` reference.

If a :cylc:conf:`flow.cylc` file uses include-files ``cylc view`` will
show an inlined copy of the workflow with correct line numbers.

.. _cylc_lint_script:

Linting
-------

The ``cylc lint`` command checks code style, deprecated syntax and other
issues in Cylc configuration files.

.. seealso::

   :ref:`How to configure Cylc lint at project level <lint.pyproject.toml>`
   using a ``pyproject.toml``.

``cylc lint``
^^^^^^^^^^^^^

.. automodule:: cylc.flow.scripts.lint

.. _lint.pyproject.toml:

Configure ``cylc lint`` at project level
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

You can configure ``cylc lint`` for each workflow using a
``pyproject.toml`` file.

To define settings for ``cylc lint`` use a ``[tool.cylc.lint]`` section.
Within the ``[tool.cylc.lint]`` section you may define the following:

``rulesets``
   A list of rulesets to use.

   Allowed values: ``'728'``, ``'style'``, ``'all'``.

   (You can override this on the command line.)

``ignore``
   Individual rules to ignore: A list of rule codes, such as ``S007``.

``exclude``
   A list of files or glob patterns for files which will not be checked.

``max-line-length``
   Set longest line length to permit in Cylc configs for this project.

   Default: ``130``.


.. note::

   .. versionchanged:: 8.3.0

      The ``[cylc-lint]`` section has been deprecated in favour of
      ``[tool.cylc.lint]``.

An example ``pyproject.toml`` might look like this:

.. code-block:: toml

   [tool.cylc.lint]
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
