.. _Jinja:
.. _User Guide Jinja2:

Jinja2
======

.. tutorial::
   Configuration Consolidation Tutorial <tutorial-cylc-consolidating-configuration>

.. note::

   This section needs to be revised - the Parameterized Task feature
   introduced in cylc-6.11.0 (see :ref:`User Guide Param`) provides
   a cleaner way to auto-generate tasks without coding messy Jinja2 loops.

Cylc has built in support for the `Jinja2`_ template processor in suite
configurations. Jinja2 variables, mathematical expressions, loop control
structures, conditional logic, etc., are automatically processed to
generate the final suite configuration seen by Cylc.

The need for Jinja2 processing must be declared with a hash-bang
comment as the first line of the :cylc:conf:`flow.cylc` file:

.. code-block:: cylc

   #!jinja2
   # ...

Potential uses for this include automatic generation of repeated groups
of similar tasks and dependencies, and inclusion or exclusion of entire
suite sections according to the value of a single flag. Consider a
large complicated operational suite and several related parallel test
suites with slightly different task content and structure (the parallel
suites, for instance, might take certain large input files from the
operation or the archive rather than downloading them again) - these can
now be maintained as a single master suite configuration that reconfigures
itself according to the value of a flag variable indicating the intended use.

Template processing is the first thing done on parsing a suite
configuration so Jinja2 expressions can appear anywhere in the file (inside
strings and namespace headings, for example).

Jinja2 is `well documented <https://jinja.palletsprojects.com/>`_, so here
we just provide an example suite that uses it. The meaning of the
embedded Jinja2 code should be reasonably self-evident to anyone familiar
with standard programming techniques.

.. _fig-jinja2-ensemble:

.. figure:: ../../img/jinja2-ensemble-graph.png
   :align: center

   The Jinja2 ensemble example suite graph.


The ``jinja2.ensemble`` example :ref:`graphed above <fig-jinja2-ensemble>`
shows an ensemble of similar tasks generated using Jinja2:

.. code-block:: cylc

   #!jinja2
   {% set N_MEMBERS = 5 %}
   [scheduling]
       [[graph]]
           R1 = """
   {# generate ensemble dependencies #}
   {% for I in range( 0, N_MEMBERS ) %}
               foo => mem_{{ I }} => post_{{ I }} => bar
   {% endfor %}"""

Here is the generated suite configuration, after Jinja2 processing:

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

And finally, the ``jinja2.cities`` example uses variables,
includes or excludes special cleanup tasks according to the value of a
logical flag, and it automatically generates all dependencies and family
relationships for a group of tasks that is repeated for each city in the
suite. To add a new city and associated tasks and dependencies simply
add the city name to list at the top of the file. Here is the suite graphed,
with the New York City task family expanded:

.. literalinclude:: ../../suites/jinja2/cities/flow.cylc
   :language: cylc

.. _fig-jinja2-cities:

.. figure:: ../../img/jinja2-suite-graph.png
   :align: center

   The Jinja2 cities example suite graph, with the
   New York City task family expanded.


Accessing Environment Variables With Jinja2
-------------------------------------------

This functionality is not provided by Jinja2 by default, but Cylc
automatically imports the user environment to template's global namespace
(see :ref:`CustomJinja2Filters`) in a dictionary structure called
*environ*. A usage example:

.. code-block:: cylc

   #!Jinja2
   #...
   [runtime]
       [[root]]
           [[[environment]]]
               SUITE_OWNER_HOME_DIR_ON_SUITE_HOST = {{environ['HOME']}}

In addition, the following variables are exported to this environment
prior to configuration parsing to provide suite context:

.. code-block:: sub

   CYLC_DEBUG                      # Debug mode, true or not defined
   CYLC_VERBOSE                    # Verbose mode, True or False
   CYLC_VERSION                    # Version of cylc installation used

   CYLC_SUITE_NAME                 # Suite name

   CYLC_SUITE_LOG_DIR              # Suite log directory.
   CYLC_SUITE_RUN_DIR              # Location of the run directory in
                                   # suite host, e.g. ~/cylc-run/foo
   CYLC_SUITE_SHARE_DIR            # Suite (or task post parsing!)
                                   # shared directory.
   CYLC_SUITE_WORK_DIR             # Suite work directory.


.. note::

   The example above emphasizes that *the environment - including the suite
   context variables - is read on the suite host when the suite configuration
   is parsed*, not at task run time on job hosts.

.. _CustomJinja2Filters:

Custom Jinja2 Filters, Tests and Globals
----------------------------------------

Jinja2 has three different namespaces used to separate "globals",
"filters" and "tests". Globals are template-wide accessible variables
and functions. Cylc extends this namespace with "environ" dictionary and
:ref:`raise <jinja2-raise>` and :ref:`assert <jinja2-assert>`
functions for raising exceptions.

Filters can be used to modify variable values and are applied using pipe
notation. For example, the built-in ``trim`` filter strips leading
and trailing white space from a string:

.. code-block:: cylc

   {% set MyString = "   dog   " %}
   {{ MyString | trim() }}  # "dog"

Variable values can be tested using the ``is`` keyword followed by
the name of the test, e.g. ``VARIABLE is defined``.
See official Jinja2 documentation for available built-in globals, filters
and tests.

Cylc also supports custom Jinja2 globals, filters and tests. A custom global,
filter or test is a single Python function in a source file with the same name
as the function (plus ``.py`` extension) and stored in one of the following
locations:

In the argument list of filter or test function, the first argument is
the variable value to be "filtered" or "tested", respectively, and
subsequent arguments can be whatever else is needed. Currently there are three
custom filters:

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

Associative arrays (*dicts* in Python) can be very useful.
Here's an example:

.. TODO - platformise?

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

   $ cylc get-suite-config -i [runtime][airs]directives SUITE
   -I = ncpus=9


Jinja2 Default Values And Template Inputs
-----------------------------------------

The values of Jinja2 variables can be passed in from the Cylc command
line rather than hardwired in the suite configuration.

This can be done on a case-by-case basis using the ``-s`` option e.g:

.. code-block:: console

   $ # set the Jinja2 variable "answer" to 42
   $ cylc play <flow> -s answer=42

Or for multiple options using a Cylc "set file" with ``--set-file``
e.g:

.. code-block:: console

   $ # create a set file
   $ cat > my-set-file <<__SET_FILE__
   question='the meaning of life, the universe and everything'
   answer=42
   host='deep-thought'
   __SET_FILE__

   $ # run using the options in the set file
   $ cylc play <flow> --set-file my-set-file

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
      $ cylc play <flow> -s 'my_string="a b c"'

Here's an example:

.. literalinclude:: ../../suites/jinja2/defaults/flow.cylc
   :language: cylc

Here's the result:

.. code-block:: console

   $ cylc list SUITE
   Jinja2 Template Error
   'FIRST_TASK' is undefined
   cylc-list SUITE  failed:  1

   $ # Note: quoting "bob" so that it is evaluated as a string
   $ cylc list --set 'FIRST_TASK="bob"' SUITE
   bob
   baz
   mem_2
   mem_1
   mem_0

   $ cylc list --set 'FIRST_TASK="bob"' --set 'LAST_TASK="alice"' SUITE
   bob
   alice
   mem_2
   mem_1
   mem_0

   $ # Note: no quotes required for N_MEMBERS since it is an integer
   $ cylc list --set 'FIRST_TASK="bob"' --set N_MEMBERS=10 SUITE
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

Note also that ``cylc view --set FIRST_TASK=bob --jinja2 SUITE``
will show the suite with the Jinja2 variables as set.

.. note::

   Suites started with template variables set on the command
   line will :term:`restart` with the same settings. However, you can set
   them again on the ``cylc play`` command line if they need to
   be overridden.


Jinja2 Variable Scope
---------------------

Jinja2 variable scoping rules may be surprising. Variables set inside a
*for loop* block, for instance, are not accessible outside of the block,
so the following will print ``# FOO is 0``, not ``# FOO is 9``:

.. code-block:: cylc

   {% set FOO = false %}
   {% for item in items %}
       {% if item.check_something() %}
           {% set FOO = true %}
       {% endif %}
   {% endfor %}
   # FOO is {{FOO}}

Jinja2 documentation suggests using alternative constructs like the loop else
block or the special ``loop`` variable. More complex use cases can be
handled using ``namespace`` objects which allow propagating of changes
across scopes:

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

Cylc provides two functions for raising exceptions using Jinja2. These
exceptions are raised when the :cylc:conf:`flow.cylc` file is loaded and will prevent a suite
from running.

.. note::

   These functions must be contained within ``{{`` Jinja2
   blocks as opposed to ``{%`` blocks.

.. _jinja2-raise:

Raise
^^^^^

The ``raise`` function will result in an error containing the provided text.

.. code-block:: cylc

   {% if not VARIABLE is defined %}
       {{ raise('VARIABLE must be defined for this suite.') }}
   {% endif %}

.. _jinja2-assert:

Assert
^^^^^^

The ``assert`` function will raise an exception containing the text provided in
the second argument providing that the first argument evaluates as False. The
following example is equivalent to the "raise" example above.

.. code-block:: cylc

   {{ assert(VARIABLE is defined, 'VARIABLE must be defined for this suite.') }}


Importing additional Python modules
-----------------------------------

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
messages will appear on the console when running or validating a suite.
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

Log messages will appear whenever the suite configuration is loaded so it is
advisable to use the ``DEBUG`` logging level which is suppressed unless the
``--debug`` option is provided.
