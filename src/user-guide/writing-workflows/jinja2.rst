.. _Jinja:
.. _User Guide Jinja2:

Jinja2
======

.. tutorial::
   Configuration Consolidation Tutorial <tutorial-cylc-consolidating-configuration>

Cylc supports use of the `Jinja2`_ template processor in workflow
configurations. Jinja2 variables, expressions, loop control structures,
conditional logic, etc., are processed to generate the final configuration. To
the template processor, Jinja2 code is embedded in arbitrary text, but the
result after processing must be valid Cylc syntax.

To use Jinja2, put a hash-bang comment in the first line of :cylc:conf:`flow.cylc`:

.. code-block:: cylc

   #!jinja2

Template processing is the first thing done on parsing a workflow configuration
so Jinja2 can appear anywhere in the file.

Embedded Jinja2 code should be reasonably easy to understand for those with
coding experience; but if not, Jinja2 is well documented `here
<https://jinja.palletsprojects.com/>`_.

Uses of Jinja2 in Cylc include:

 - Inclusion or exclusion of config sections by logical switch, e.g. to make
   portable workflows
 - Computation of config values from in input data
 - Inclusion of files and sub-templates
 - Loop over parameters to generate groups of similar tasks and associated
   dependencies - but see :ref:`Parameterized Tasks <User Guide Param>` for a
   simpler alternative to this use case

.. _fig-jinja2-ensemble:

.. figure:: ../../img/jinja2-ensemble-graph.png
   :align: center

   The Jinja2 ensemble example workflow graph.


The graph above shows an ensemble of similar tasks generated with a Jinja2 loop:

.. code-block:: cylc

   #!jinja2
   {% set N_MEMBERS = 5 %}
   [scheduling]
       [[graph]]
           R1 = """
   {# generate ensemble dependencies #}
   {% for I in range( 0, N_MEMBERS ) %}
               foo => mem_{{ I }} => post_{{ I }} => bar
   {% endfor %}
           """

Note that Jinja2 code is encapsulated in curly braces to distinguish it from
the surrounding text.


    ================= ======================
    Jinja2 Syntax     Description
    ================= ======================
    ``{# comment #}`` Comment
    ``{% if true %}`` Expression
    ``{{ var }}``     Print statement
    ================= ======================

Here is the workflow configuration after Jinja2 processing:

.. code-block:: cylc

   #!jinja2
   [scheduling]
       [[graph]]
           R1 = """
               foo => mem_0 => post_0 => bar
               foo => mem_1 => post_1 => bar
               foo => mem_2 => post_2 => bar
               foo => mem_3 => post_3 => bar
               foo => mem_4 => post_4 => bar
           """

This example illustrates Jinja2 loops nicely, but note it is now easier
to generate task names automatically with built-in
:ref:`task parameters <User Guide Param>`:

.. code-block:: cylc

   [task parameters]
       m = 0..4
   [scheduling]
       [[graph]]
           R1 = "foo => mem<m> => post<m> => bar"


The next example, which generates weather forecasts over a number of cities, is
more complex. To add a new city and associated tasks and dependencies just add
the new city name to list at the top of the file. It makes use of Jinja2
variables, loops, math, and logical flags to include or exclude tasks.

.. tip::
   This example could also be simplified with built in
   :ref:`task parameters <User Guide Param>`

.. literalinclude:: ../../workflows/jinja2/cities/flow.cylc
   :language: cylc

.. _fig-jinja2-cities:

.. figure:: ../../img/jinja2-workflow-graph.png
   :align: center

   Jinja2 cities example workflow graph, with the
   New York City task family expanded.


Accessing Environment Variables
-------------------------------

Cylc automatically imports the environment to the template's global namespace
(see :ref:`CustomJinja2Filters`) in a dictionary called ``environ``:

.. code-block:: cylc

   #!Jinja2
   #...
   [runtime]
       [[root]]
           [[[environment]]]
               WORKFLOW_OWNER_HOME_DIR_ON_WORKFLOW_HOST = {{environ['HOME']}}

In addition, the following variables are exported to this environment
(hence are available in the ``environ`` dict) to provide workflow context:

.. code-block:: sub

   CYLC_VERBOSE                    # Verbose mode, true or false
   CYLC_DEBUG                      # Debug mode (even more verbose), true or false

   CYLC_WORKFLOW_ID                # Workflow ID
   CYLC_WORKFLOW_NAME              # Workflow name
                                   # (the ID with the run name removed)

   CYLC_WORKFLOW_LOG_DIR           # Workflow log directory.
   CYLC_WORKFLOW_RUN_DIR           # Location of the run directory in
                                   # workflow host, e.g. ~/cylc-run/foo
   CYLC_WORKFLOW_SHARE_DIR         # Workflow (or task post parsing!)
                                   # shared directory.
   CYLC_WORKFLOW_WORK_DIR          # Workflow work directory.

.. warning::

   The environment is read on the workflow host when the configuration is
   parsed. It is not read at run time by jobs on the job platform.

The following Jinja2 variables are also available (i.e. standalone,
not in the ``environ`` dict):

``CYLC_VERSION``
   Version of Cylc used.

``CYLC_TEMPLATE_VARS``
   All variables set by the ``-s``, ``--set-file`` or ``--set-list`` options,
   or by a plugin.


.. _CustomJinja2Filters:

Custom Jinja2 Filters, Tests and Globals
----------------------------------------

Jinja2 has three namespaces that separate "globals", "filters" and "tests".
Globals are template-wide variables and functions. Cylc extends this namespace
with the ``environ`` dictionary above, and
:ref:`raise <jinja2-raise>` and :ref:`assert <jinja2-assert>`
functions for raising exceptions to abort Cylc config parsing.

Filters can be used to modify variable values and are applied using pipe
notation. For example, the built-in ``trim`` filter strips leading
and trailing white space from a string:

.. code-block:: cylc

   {% set MyString = "   dog   " %}
   {{ MyString | trim() }}  # "dog"

Variable values can be tested using the ``is`` keyword followed by
the name of the test, e.g. ``{% if VARIABLE is defined %}``. See Jinja2
documentation for available built-in globals, filters and tests.

Cylc also supports custom Jinja2 globals, filters and tests. A custom global,
filter or test is a single Python function in a source file with the same name
as the function (plus ``.py`` extension). These must be located in a
subdirectory of the :term:`run directory` called
``Jinja2Filters``, ``Jinja2Globals`` or ``Jinja2Tests`` respectively.

In the argument list of a filter or test function, the first argument is
the variable value to be filtered or tested, and subsequent arguments can be
whatever is needed. Currently three custom filters are supplied:

.. import the filters to allow their doctests to pass (make doctest)

.. testsetup::

   from cylc.flow.jinja.filters.pad import pad
   from cylc.flow.jinja.filters.strftime import strftime
   from cylc.flow.jinja.filters.duration_as import duration_as

.. autosummary::
   :nosignatures:

   cylc.flow.jinja.filters.pad.pad
   cylc.flow.jinja.filters.strftime.strftime
   cylc.flow.jinja.filters.duration_as.duration_as

.. autofunction:: cylc.flow.jinja.filters.pad.pad

.. autofunction:: cylc.flow.jinja.filters.strftime.strftime

.. autofunction:: cylc.flow.jinja.filters.duration_as.duration_as


Associative Arrays In Jinja2
----------------------------

Associative arrays (or **dictionaries**) are very useful. For example:

.. code-block:: cylc

   #!Jinja2
   {% set obs_types = ['airs', 'iasi'] %}
   {% set resource = { 'airs':'ncpus=9', 'iasi':'ncpus=20' } %}

   [scheduling]
       [[graph]]
           R1 = OBS
   [runtime]
       [[OBS]]
           platform = platform_using_pbs
       {% for i in obs_types %}
       [[ {{i}} ]]
           inherit = OBS
           [[[directives]]]
                -I = {{ resource[i] }}
        {% endfor %}

Here's the result:

.. code-block:: console

   $ cylc config -i [runtime][airs]directives <workflow-id>
   -I = ncpus=9


.. _jinja2-template-variables:

Default Values and Template Variables
-------------------------------------

You can provide template variables to Cylc in 4 ways:

- Using the ``--set-file`` (``-S``) option.
- Using the ``--set`` (``-s``) option.
- Using the ``--set-list`` (``-z``) option.
- `Using a plugin`_, such as :ref:`Cylc Rose`.

.. note::

   If the same variable is set by more than one method, the last source in the
   above list is used.


The ``-s``, ``-z`` and ``--set-file`` Options
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: console

   $ # set the Jinja2 variable "answer" to 42
   $ cylc play <workflow-id> -s answer=42

A Python string-list is a valid value, but a lot to type, so ``--set-list``
(``-z``) is provided as a convenience:

.. code-block:: console

   # The set syntax
   $ cylc play <workflow-id> -s "answers=['mice', 'dolphins']"
   # ... can  be shortened to:
   $ cylc play <workflow-id> -z answers=mice,dolphins

If you need to define a lot of variables, you can so in a file
using the ``--set-file`` option:

.. code-block:: console

   $ # create a set file
   $ cat > my-set-file <<__SET_FILE__
   question='the meaning of life, the universe and everything'
   answer=42
   host='deep-thought'
   __SET_FILE__

   $ # run using the options in the set file
   $ cylc play <workflow-id> --set-file my-set-file

Values must be Python literals e.g:

.. code-block:: python

   "string"   # string
   123        # integer
   12.34      # float
   True       # boolean
   None       # None type
   [1, 2, 3]  # list
   (1, 2, 3)  # tuple
   {1, 2, 3}  # set
   {"a": 1, "b": 2, "c": 3}  # dictionary

.. note::

   On the command line you may need to wrap strings with an extra
   pair of quotes as the shell you are using (e.g. Bash) will strip
   the outer pair of quotes.

   .. code-block:: console

      $ # wrap the key=value pair in single quotes stop the shell from
      $ # stripping the inner quotes around the string:
      $ cylc play <workflow-id> -s 'my_string="a b c"'

Here's an example:

.. literalinclude:: ../../workflows/jinja2/defaults/flow.cylc
   :language: cylc

Here's the result:

.. code-block:: console

   $ cylc list <workflow-id>
   Jinja2 Template Error
   'FIRST_TASK' is undefined
   cylc-list <workflow-id>  failed:  1

   $ # Note: quoting "bob" so that it is evaluated as a string
   $ cylc list --set 'FIRST_TASK="bob"' <workflow-id>
   bob
   baz
   mem_2
   mem_1
   mem_0

   $ cylc list --set 'FIRST_TASK="bob"' --set 'LAST_TASK="alice"' <workflow-id>
   bob
   alice
   mem_2
   mem_1
   mem_0

   $ # Note: no quotes required for N_MEMBERS since it is an integer
   $ cylc list --set 'FIRST_TASK="bob"' --set N_MEMBERS=10 <workflow-id>
   mem_9
   mem_8
   mem_7
   mem_6
   mem_5
   mem_4
   mem_3
   mem_2
   mem_1
   mem_0
   baz
   bob

Note also that ``cylc view --set FIRST_TASK=bob --jinja2 <workflow-id>``
will show the workflow with the Jinja2 variables as set.

.. note::

   Workflows started with template variables set on the command
   line will :term:`restart` with the same settings. You can set
   them again on the ``cylc play`` command line if they need to
   be overridden.


Using a plugin
^^^^^^^^^^^^^^

Template plugins such as :ref:`Cylc Rose` should provide a set of template
variables which can be provided to Cylc. For example, using Cylc Rose you
add a ``rose-suite.conf`` file containing a ``[template variables]``
section which the plugin makes available to Cylc:

.. code-block:: ini
   :caption: rose-suite.conf

   [template variables]
   ICP=1068

.. code-block:: cylc
   :caption: flow.cylc

   #!jinja2
   [scheduler]
      allow implicit tasks = True
   [scheduling]
      initial cycle point = {{ICP}}
      [[dependencies]]
         P1Y = Task1


.. code-block:: console

   $ cylc config . -i "[scheduling]initial cycle point"
   1068



Jinja2 Variable Scope
---------------------

Jinja2 variable scoping rules may be surprising. For instance, variables set
inside a ``for`` loop can't be accessed outside of the block,
so the following will not print ``# FOO is True``:

.. code-block:: cylc

   {% set FOO = False %}
   {% for item in items %}
       {% if item.check_something() %}
           {% set FOO = True %}
       {% endif %}
   {% endfor %}
   # FOO is {{FOO}}

Jinja2 documentation suggests using alternative constructs like the loop
``else`` block or the special ``loop`` variable. More complex use cases can be
handled using ``namespace`` objects that allow propagating of changes across scopes:

.. code-block:: cylc

   {% set ns = namespace(foo=false) %}
   {% for item in items %}
       {% if item.check_something() %}
           {% set ns.foo = true %}
       {% endif %}
   {% endfor %}
   # FOO is {{ns.foo}}

For detail, see
`Jinja2 Template Designer Documentation - Assignments
<https://jinja.palletsprojects.com/en/2.11.x/templates/#assignments>`_


.. _Jinja2RaisingExceptions:

Raising Exceptions
------------------

Cylc provides two functions for raising exceptions in Jinja2 code. These
exceptions are raised when the :cylc:conf:`flow.cylc` file is loaded and will
prevent a workflow from running.

.. note::

   These functions must be contained within ``{{`` Jinja2 print statements, not
   ``{%`` code blocks.

.. _jinja2-raise:

Raise
^^^^^

The ``raise`` function will result in an error containing the provided text.

.. code-block:: cylc

   {% if not VARIABLE is defined %}
       {{ raise('VARIABLE must be defined for this workflow.') }}
   {% endif %}

.. _jinja2-assert:

Assert
^^^^^^

The ``assert`` function will raise an exception containing the text provided in
the second argument providing that the first argument evaluates as False. The
following example is equivalent to the "raise" example above.

.. code-block:: cylc

   {{ assert(VARIABLE is defined, 'VARIABLE must be defined for this workflow.') }}


.. _jinja2.importing_python_modules:

Importing Python modules
------------------------

Jinja2 allows to gather variable and macro definitions in a separate template
that can be imported into (and thus shared among) other templates.

.. code-block:: cylc

   {% import "flow-utils.cylc" as utils %}
   {% from "flow-utils.cylc" import VARIABLE as ALIAS %}
   {{ utils.VARIABLE is equalto(ALIAS)) }}

Cylc extends this functionality to allow import of arbitrary Python modules.

.. code-block:: cylc

   {% from "itertools" import product %}
   [runtime]
   {% for group, member in product(['a', 'b'], [0, 1, 2]) %}
       [[{{group}}_{{member}}]]
   {% endfor %}

For better clarity and disambiguation Python modules can be prefixed with
``__python__``:

.. code-block:: cylc

   {% from "__python__.itertools" import product %}


Logging
-------

It is possible to output messages to the Cylc log from within Jinja2, these
messages will appear on the console when validating or starting a workflow.
This can be useful for development or debugging.

Example :cylc:conf:`flow.cylc`:

.. code-block:: cylc

   #!Jinja2
   {% from "cylc.flow" import LOG %}
   {% do LOG.debug("Hello World!") %}

Example output:

.. code-block:: console

   $ cylc validate . --debug
   DEBUG - Loading site/user config files
   DEBUG - Reading file <file>
   DEBUG - Processing with Jinja2
   DEBUG - Hello World!
   ...
   Valid for cylc-<version>

Log messages will appear whenever the workflow configuration is loaded so it is
advisable to use the ``DEBUG`` logging level which is suppressed unless the
``--debug`` option is provided.


Debugging
---------

It is possible to run Python debuggers from within Jinja2 via the
:ref:`import mechanism <jinja2.importing_python_modules>`.

.. _PDB: https://docs.python.org/3/library/pdb.html

For example to use a `PDB`_ breakpoint you could do the following:

.. code-block:: cylc

   #!Jinja2

   {% set ANSWER = 42 %}

   {% from "pdb" import set_trace %}
   {% do set_trace() %}

The debugger will open within the Jinja2 code, local variables can be accessed
via the ``_Context__self`` variable e.g:

.. code-block:: console

   $ cylc validate <id>
   (Pdb) _Context__self['ANSWER']
   42
