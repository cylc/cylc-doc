.. _Section External Triggers:

External Triggers (Xtriggers)
=============================

Overview
--------

Xtriggers allow tasks to trigger off of arbitrary external conditions. The
:term:`scheduler` periodically calls a Python function, to check on the
condition, until it returns success to satisfy dependent tasks.


.. note::
   Compared to the older :ref:`Old-Style External Triggers`, xtriggers are
   visible in the graph, they are shared efficiently by all dependent tasks,
   and they are entirely contained within the workflow.


You can write :ref:`Custom Trigger Functions`, and Cylc has several built in:

- :ref:`Clock xtriggers <Built-in Clock Triggers>` - real time trigger relative to task cycle point
- :ref:`Workflow state xtriggers <Built-in Workflow State Triggers>` - trigger off tasks in other workflows
- :ref:`Toy xtriggers <Built-in Toy Xtriggers>` - to facilitate understanding


Periodic Checking
-----------------

Xtrigger calls commence when the first dependent task enters the
:term:`active window`, repeating at configurable intervals until success
is achieved. The default call interval is 10 seconds.

.. TODO - 

   Adjust the following once we can distinguish "not called" from "not satisfied".
   See https://github.com/cylc/cylc-flow/pull/6560.

.. note::

   The xtrigger prerequisites of future tasks that have yet to enter the
   :term:`active window`, will always show as unsatisfied because the
   associated xtrigger function has not been called yet.

The scheduler satisfies future tasks when they enter the active window, if
they depend on the same xtrigger, without calling the function again - see
:ref:`xtrigger Specificity`.

Xtriggers must return quickly, or be killed by the
:cylc:conf:`global.cylc[scheduler]process pool timeout`.

.. warning::

   Each xtrigger call is made in a new Python subprocess. Consider increasing the
   call interval if you have many xtriggers, to reduce the associated system load.


Declaring Xtriggers
-------------------

Xtriggers are declared under :cylc:conf:`flow.cylc[scheduling][xtriggers]`
by associating a short *label* with a function name, arguments, and optional
custom check interval.

The label must be prefixed by "@" for use in the graph, and must comply with
basic naming rules: 

.. autoclass:: cylc.flow.unicode_rules.XtriggerNameValidator


The following workflow declares an xtrigger ``x1 = check_data``. The function
has one argument, a file path, and will be called every 30 seconds until
it succeeds - at which point ``process_data`` can trigger:

.. code-block:: cylc

   [scheduling]
       [[xtriggers]]
           x1 = check_data(loc="/path/to/data/source"):PT30S
       [[graph]]
           P1D = "@x1 => process_data"
   [runtime]
       [[process_data]]


Argument keywords can be omitted, so long as argument order is preserved:

.. code-block:: cylc

   [scheduling]
       [[xtriggers]]
           x1 = check_data("/path/to/data/source"):PT30S


.. note::

   Trigger labels can be used with ``&`` (AND) operators in the graph, but
   currently not with ``|`` (OR) - attempts to do that will fail validation.


.. _Xtrigger Results:

Xtrigger Results
----------------

Xtrigger functions must return a flat *dictionary* of results to be
:ref:`broadcast <cylc-broadcast>` to dependent tasks, via environment
variables named as ``<xtrigger_label>_<dictionary_key>``.

For example, if the ``x1`` xtrigger returns this dictionary:

.. code-block:: python

   # returned by check_data() on success:
   {
       "data_path": "/path/to/data",
       "data_type": "netcdf"
   }

Then the ``process_data`` task, which depends on ``x1``, will see the
following environment variables:

.. code-block:: shell

   # job environment of process_data:
   x1_data_path="/path/to/data"
   x1_data_type="netcdf"


The ``process_data`` task would likely run an application that needs this
information in terms of its native configuration. You can translate from
xtrigger to application in the workflow configuration:

.. code-block:: cylc

   [runtime]
       [[process_data]]
           script = run-process.py
           [[[environment]]]
               INPUT_DATA_LOCN = $x1_data_path
               INPUT_DATA_TYPE = $x1_date_type


.. _Xtrigger Specificity:

Task and Cycle Specificity
--------------------------

Cylc makes a call sequence for each unique xtrigger with one or more dependent
tasks in the :term:`active window`. Uniqueness is determined by the
*function signature*, i.e. the function name and arguments.

Depending on the argument list, an xtrigger can be universal - the same for
all tasks that depend on it; or specific - to the name and/or cycle point of
tasks that depend on it.

Universal xtriggers
^^^^^^^^^^^^^^^^^^^

If an xtrigger has no arguments that vary as the workflow runs, a single call
sequence will satisfy every dependent task in the entire graph.

Below, every cycle point instance of ``process_data`` depends on the same
xtrigger, which presumably checks data for the entire workflow. Once satisfied
it allows every instance of the task to run:

.. code-block:: cylc

   [scheduling]
       cycling mode = integer
       initial cycle point = 1
       final cycle point = 10
       [[xtriggers]]
           x = check_data("/path/to/data")
       [[graph]]
           P1 = "@x => process_data"
   [runtime]
       [[check_data]]


Task and Cycle-Specific Xtriggers
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Xtrigger arguments can incorporate string templates as placeholders for certain
workflow parameters - see :ref:`Custom Trigger Functions`. Several of these
are specific to the cycle point or name of tasks that depend on the xtrigger:

  - ``%(point)s`` - cycle point of the dependent task
  - ``%(names)s`` - name of the dependent task
  - ``%(id)s`` - identity (``point/name``) of the dependent task 

If these are used, a new call sequence, with new arguments, will commence
whenever a dependent task with a new name or cycle point enters the
:term:`active window`.

Below, every instance of ``process_data`` depends on a different, cycle
point-specific xtrigger, which presumably checks data just for that instance.
Each xtrigger, once satisfied, allows just one instance of the task to run:

.. code-block:: cylc

   [scheduling]
       cycling mode = integer
       initial cycle point = 1
       final cycle point = 10
       [[xtriggers]]
           x = check_data(loc="/path/to/data", cycle="%(point)s")
       [[graph]]
           P1 = "@x => process_data"


.. note::

   You have to inspect the function signature to see the cycle
   and task specificity of xtriggers.


The following working example shows four xtriggers based on the
:ref:`toy "echo" xtrigger <Built-in Toy Xtriggers>`,
which takes an arbitrary list of arguments:

.. code-block:: cylc

   [scheduling]
       cycling mode = integer
       initial cycle point = 1
       final cycle point = 2
       [[xtriggers]]
           w1 = echo(succeed=True)  # universal
           x2 = echo(succeed=True, task="%(name)s")  # task name specific
           y2 = echo(succeed=True, cycle="%(point)s")  # cycle point specific
           z4 = echo(succeed=True, task="%(name)s", cycle="%(point)s")  # both
       [[graph]]
           P1 = "@w1 & @x1 & @y2 & @z4 => foo & bar"
   [runtime]
       [[foo, bar]]

Run this with ``cylc play --no-detach`` and watch when each xtrigger is called:
``w1`` will be called once, because it has only static arguments; ``x2`` will
be called twice, once for each task name (regardless of cycle point); ``y2``
will be called twice, once for each cycle point (regardless of task name); and
``z4`` will be called four times, once for each task in each cycle point:

.. code-block:: console

   $ cylc cat-log xtr | grep 'xtrigger succeeded'
   INFO - xtrigger succeeded: w1 = echo(succeed=True)
   INFO - xtrigger succeeded: x2 = echo(succeed=True, task=bar)
   INFO - xtrigger succeeded: y2 = echo(cycle=1, succeed=True)
   INFO - xtrigger succeeded: z4 = echo(cycle=1, succeed=True, task=bar)
   INFO - xtrigger succeeded: x2 = echo(succeed=True, task=foo)
   INFO - xtrigger succeeded: z4 = echo(cycle=1, succeed=True, task=foo)
   INFO - xtrigger succeeded: y2 = echo(cycle=2, succeed=True)
   INFO - xtrigger succeeded: z4 = echo(cycle=2, succeed=True, task=bar)
   INFO - xtrigger succeeded: z4 = echo(cycle=2, succeed=True, task=foo)


.. _Sequential Xtriggers:

Sequential Xtriggers
--------------------

:term:`Parentless tasks <parentless>`, which often depend on clock or other
xtriggers, automatically spawn into the :term:`active window`, multiple
cycles ahead (to the :term:`runahead limit`). If they depend on xtriggers
that will only be satisfied in cycle point order, this causes
unnecessary xtrigger checking and UI clutter.

Sequential xtriggers prevent this by delaying the spawning of the next
dependent task instance until the current one is satisfied. To do this
(in reverse order of precedence):

  - set
    :cylc:conf:`[scheduling]sequential xtriggers = True <flow.cylc[scheduling]sequential xtriggers>`
    for all xtriggers in the workflow
  - add a ``sequential=True`` argument to function definitions (in Python source files)
  - add a ``sequential=True`` argument to function declarations (in workflow configurations)

.. note::

   The built in ``wall_clock`` xtrigger is sequential by default.


.. TODO - update this once we have static visualisation

   External triggers are visible in workflow visualizations as bare graph nodes
   (just the trigger names). They are plotted against all dependent tasks, not
   in a cycle point specific way like tasks. This is because external triggers
   may or may not be cycle point (or even task name) specific - it depends on
   the arguments passed to the corresponding trigger functions. For example, if
   an external trigger does not depend on task name or cycle point it will only
   be called once - albeit repeatedly until satisfied - for the entire workflow
   run, after which the function result will be remembered for all dependent
   tasks throughout the workflow run.


Forcing Xtriggers
-----------------

You can manually satisfy a task's xtrigger prerequisites via the GUI or
command line, so the task can run even if the xtrigger has not yet succeeded.

This will not affect other tasks that depend on the same xtrigger, but the
scheduler will stop checking the xtrigger if no other active tasks depend on it.

.. code-block:: console

   # Satisfy @x1 => foo in cycle point 1
   $ cylc set --pre=xtrigger/x1 my_workflow//1/foo
   # See cylc set --help


For this to work without causing task failure, set appropriate default values
for :ref:`xtrigger results <Xtrigger Results>` in task scripting.


.. NOTE - from here on all references can start [xtriggers]

.. cylc-scope:: flow.cylc[scheduling]


.. _Built-in Clock Triggers:

Built-in Clock Triggers
-----------------------

Clock xtriggers succeed when the real ("wall clock") time reaches some offset
from the task's cycle point value.

.. note::

   These should be used instead of the older task clock triggers documented in
   :ref:`ClockTriggerTasks`.

The clock xtrigger function signature looks like this:

.. autofunction:: cylc.flow.xtriggers.wall_clock.wall_clock

.. note::

   Clock xtriggers are cycle-point specific by nature; you don't need
   to :ref:`use function arguments <Xtrigger Specificity>` to achieve this.

In the following workflow, task ``foo`` has a daily cycle point sequence, and
each task instance will trigger when the real time is one hour past its cycle
point value.

.. code-block:: cylc

   [scheduling]
       initial cycle point = 2018-01-01
       [[xtriggers]]
           clock_1 = wall_clock(offset=PT1H)
       [[graph]]
           P1D = "@clock_1 => foo"
   [runtime]
       [[foo]]
           script = run-foo.sh

Or omitting the argument keyword:

.. code-block:: cylc

   [scheduling]
       [[xtriggers]]
           clock_1 = wall_clock(PT1H)

A zero-offset clock trigger does not need to be declared before use:

.. code-block:: cylc

   [scheduling]
       initial cycle point = 2018-01-01
       [[graph]]
            # zero-offset clock trigger:
           P1D = "@wall_clock => foo"
   [runtime]
       [[foo]]
           script = run-foo.sh


.. _Built-in Workflow State Triggers:

Built-in Workflow State Triggers
--------------------------------

Workflow-state xtriggers succeed when a given task in another workflow achieves
a given state or output.

.. note::

   These should be used instead of the older workflow state polling tasks described
   in :ref:`WorkflowStatePolling`.

The workflow state trigger function signature looks like this:

.. autofunction:: cylc.flow.xtriggers.workflow_state.workflow_state

The first argument identifies the target workflow, cycle, task, and status or
output trigger name. The function arguments mirror the arguments and options of
the ``cylc workflow-state`` command - see ``cylc workflow-state --help``.

As a simple example, consider the following "upstream"
workflow (which we want to trigger off of):

.. literalinclude:: ../../workflows/xtrigger/workflow_state/upstream/flow.cylc
   :language: cylc

It must be installed and run under the name *up*, as referenced in the
"downstream" workflow that depends on it:

.. literalinclude:: ../../workflows/xtrigger/workflow_state/downstream/flow.cylc
   :language: cylc

Try starting the downstream workflow first, then the upstream, and watch what
happens. In each cycle point the ``@upstream`` trigger in the downstream workflow
waits for the upstream task ``foo`` (with the same cycle point) workflow to generate
the "data ready" message.

.. note::

  - The ``workflow_state`` trigger function, like the ``cylc workflow-state`` command,
    must have read-access to the upstream workflow's public database.
  - The task cycle point is supplied by a string template ``%(point)s``.
    See :ref:`Custom Trigger Functions`) for other string templates available
    to xtriggers.

The return value of the ``workflow_state`` trigger function looks like this:

.. code-block:: python

   results = {
       'workflow': workflow_id,
       'task': task_name,
       'point': cycle_point,
       'status': task_status,  # or
       'trigger': task_output_trigger,  # or
       'message': task_output_message,
       'flow_num': flow_num  # if given
   }
   return (satisfied, results)

The ``results`` dictionary contains the names and values of the
target workflow state parameters. Each name gets qualified with the
unique trigger name ("upstream" here) and passed to the environment of
dependent tasks (the members of the ``FAM`` family in this case).
To see this, take a look at the job script for one of the downstream tasks:

.. code-block:: console

   % cylc cat-log -f j dn//2011/f22011
   ...
   cylc__job__inst__user_env() {
       # TASK RUNTIME ENVIRONMENT:
       export upstream_workflow upstream_cylc_run_dir upstream_offset \
         upstream_message upstream_status upstream_point upstream_task
       upstream_workflow="up"
       upstream_task="foo"
       upstream_point="2011"
       upstream_status="succeeded"
   }
   ...

.. note::

   The dependent task has to know the name of the xtrigger that it
   depends on - "upstream" in this case - in order to use this information.
   However the name could be given to the task environment in the workflow
   configuration.


.. _Built-in Toy Xtriggers:

Built-in Toy Xtriggers
----------------------

echo
^^^^

The toy ``echo`` trigger simply prints any arguments that you give it to stdout,
and then fails (trigger condition not met) or succeeds (trigger condition met)
according to the value of a ``succeed=True`` argument (which defaults to
``False``). On success, it returns all arguments in the result dictionary.

.. autofunction:: cylc.flow.xtriggers.echo.echo

.. code-block:: cylc

   [scheduling]
       initial cycle point = now
       [[xtriggers]]
           echo_1 = echo(succeeded=True, hello, 99, point=%(point)s, foo=10)
       [[graph]]
           PT1H = "@echo_1 => foo"
   [runtime]
       [[foo]]
           script = "printenv | grep echo_1"

Run this with ``cylc play --no-detach <workflow>`` and watch your terminal to see
the xtrigger calls. View the task job log with ``cylc cat-log <workflow_id>//1/foo``
to confirm that the dependent task received the xtrigger results.


xrandom
^^^^^^^

The toy ``xrandom`` function sleeps for a configurable amount of time (useful for
testing the effect of a long-running trigger function - which should be avoided)
and has a configurable random chance of success. The function signature is:

.. automodule:: cylc.flow.xtriggers.xrandom
   :members: xrandom, validate
   :member-order: bysource

An example xrandom trigger workflow:

.. literalinclude:: ../../workflows/xtrigger/xrandom/flow.cylc
   :language: cylc


.. _Custom Trigger Functions:

Custom Xtrigger Functions
-------------------------

Xtrigger functions are Python functions with some special requirements.


Requirements
^^^^^^^^^^^^

Xtrigger functions must be compatible with the Python version that runs the
scheduler (see :ref:`Requirements` for the latest version specification).

Xtrigger functions must return a Tuple of ``(Boolean, Dictionary)``:

  - ``(False, {})`` - failed: trigger condition not met
  - ``(True, results)`` - succeeded: trigger condition met

where ``results`` is a flat (non-nested) dictionary of information to be passed
to dependent tasks - see :ref:`Xtrigger Results`. Each dictionary key must be
valid as an
`environment variable <https://pubs.opengroup.org/onlinepubs/9699919799/basedefs/V1_chap08.html>`_
name.

Xtrigger functions can take arbitrary positional and keyword arguments, except
for the keyword ``sequential``, which is
reserved for :ref:`sequential xtriggers <Sequential Xtriggers>`.

Xtrigger functions cannot store data between invocations, because each call
is executed via a wrapper in a new subprocess. If necessary the filesystem
could be used for persistent data.

If xtriggers depend on files (say) that might not exist when the function is first
called, just return trigger condition not met (i.e., ``(False, {})``). 


Installation
^^^^^^^^^^^^

We recommend using the ``cylc.xtriggers`` entry point to install the xtrigger
as a Python package - see :ref:`developing.xtrigger.plugins`.

Otherwise, e.g., for installing custom xtriggers under your own user account,
xtrigger functions must be:

  - defined in a module with the same name as the function
  - located in:
    - ``<workflow-dir>/lib/python/``;
    - or anywhere in your ``$CYLC_PYTHONPATH``

Custom xtrigger module can also provide a ``validate`` function for checking
configured arguments, see
:ref:`user-guide.xtrigger-validation-functions` for details.


Passing Workflow Parameters to Xtrigger Functions
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Workflow and task parameters can be passed to function arguments from the
workflow configuration via the following string templates. Task parameters
affect :ref:`xtrigger specificity <Xtrigger specificity>`.

.. spelling:word-list::

   vv

.. autoenumvalues:: cylc.flow.xtrigger_mgr.TemplateVariables

.. _user-guide.xtrigger-validation-functions:

Xtrigger Validation Functions
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The arguments you call the xtrigger function with are automatically validated
against the function signature, however, you might wish to add extra validation
logic to your custom xtrigger, e.g. to check argument types or values.

If a function named ``validate`` is present alongside the xtrigger in its
module, it will be automatically called with a dictionary of all the arguments
passed to the xtrigger function in the workflow config. It should raise a
:py:obj:`cylc.flow.exceptions.WorkflowConfigError` exception if an error is
detected.

The :py:mod:`cylc.flow.xtriggers.xrandom` xtrigger module contains an example
of an xtrigger validation function.


Filesystem Events?
^^^^^^^^^^^^^^^^^^

Cylc does not have built-in support for triggering off of filesystem events
such as ``inotify`` on Linux. There is no cross-platform standard for
filesystem events, and they can only be detected on the generating node in
on HPC clusters.


Persistent Event Watchers?
^^^^^^^^^^^^^^^^^^^^^^^^^^

For some applications a process that continually monitors an external condition
might be preferred over periodic checking. This would be more difficult to
support as a Cylc plugin, but we may decide to do it in the future. In the
meantime, consider implementing a small daemon process as the watcher
and have your Cylc xtrigger functions interact with that.




.. _Old-Style External Triggers:

Push External Triggers
----------------------

.. note::

   The external triggering mechanism described here is harder to use than the
   newer method of :ref:`Section External Triggers`. The trigger is a task
   property rather than something the task depends on, it requires the
   external system to push a message to the scheduler, and it has a less
   flexible way to pass information to downstream tasks. However, a push
   mechanism may sometimes be preferred over polling by the scheduler, so we
   have retained support pending something better in a future Cylc 8 release.

These external triggers are hidden task prerequisites that must be satisfied by
using the ``cylc ext-trigger`` client command to send a pre-defined message to
the workflow along with an ID string that distinguishes one instance of the
event from another (the name of the target task and its current cycle point are
not required). The event ID is just an arbitrary string to Cylc, but it can be
used to identify something associated with the event to the workflow - such as
the filename of a new externally-generated dataset. When the :term:`scheduler`
receives the event notification it will trigger the next instance of any task
waiting on that trigger (whatever its cycle point) and then broadcast
(see :ref:`cylc-broadcast`) the event ID to the cycle point of the triggered
task as ``$CYLC_EXT_TRIGGER_ID``. Downstream tasks with the same cycle
point therefore know the new event ID too and can use it, if they need to, to
identify the same new dataset. In this way a whole workflow can be associated
with each new dataset, and multiple datasets can be processed in parallel if
they happen to arrive in quick succession.

An externally-triggered task must register the event it waits on in the workflow
scheduling section:

.. code-block:: cylc

   # workflow "sat-proc"
   [scheduling]
       cycling mode = integer
       initial cycle point = 1
       [[special tasks]]
           external-trigger = get-data("new sat X data avail")
       [[graph]]
           P1 = get-data => conv-data => products

Then, each time a new dataset arrives the external detection system should
notify the workflow like this:

.. code-block:: console

   $ cylc ext-trigger sat-proc "new sat X data avail" passX12334a

where "sat-proc" is the workflow name and "passX12334a" is the ID string for
the new event. The workflow passphrase must be installed on triggering account.

.. note::

   Only one task in a workflow can trigger off a particular external message.
   Other tasks can trigger off the externally triggered task as required,
   of course.

Here is a working example of a simulated satellite processing workflow:

.. literalinclude:: ../../workflows/satellite/ext-trigger/flow.cylc
   :language: cylc

External triggers are not normally needed in datetime cycling workflows driven
by real time data that comes in at regular intervals. In these cases a data
retrieval task can be clock-triggered (and have appropriate retry intervals) to
submit at the expected data arrival time, so little time is wasted in polling.
However, if the arrival time of the cycle-point-specific data is highly
variable, external triggering may be used with the cycle point embedded in the
message:

.. code-block:: cylc

   # workflow "data-proc"
   [scheduling]
       initial cycle point = 20150125T00
       final cycle point   = 20150126T00
       [[special tasks]]
           external-trigger = get-data("data arrived for $CYLC_TASK_CYCLE_POINT")
       [[graph]]
           T00 = init-process => get-data => post-process

Once the variable-length waiting is finished, an external detection system
should notify the workflow like this:

.. code-block:: console

   $ cylc ext-trigger data-proc "data arrived for 20150126T00" passX12334a

where "data-proc" is the workflow name, the cycle point has replaced the
variable in the trigger string, and "passX12334a" is the ID string for
the new event. The workflow passphrase must be installed on the triggering
account. In this case, the event will trigger for the second cycle point but
not the first because of the cycle-point matching.


.. _WorkflowStatePolling:

Triggering Off Of Tasks In Other Workflows
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. note::

   Please read :ref:`Built-in Workflow State Triggers` before using the older
   inter-workflow triggering mechanism described in this section.

The ``cylc workflow-state`` command interrogates workflow run databases. It
has a polling mode that waits for a given task in the target workflow to achieve a
given state, or receive a given message. This can be used to make task
scripting wait for a remote task to succeed (for example).

Automatic workflow-state polling tasks can be defined with in the graph. They get
automatically-generated task scripting that uses ``cylc workflow-state``
appropriately (it is an error to give your own ``script`` item for these
tasks).

Here's how to trigger a task ``bar`` off a task ``foo`` in
a remote workflow called ``other.workflow``:

.. code-block:: cylc

   [scheduling]
       [[graph]]
           T00, T12 = "my-foo<other.workflow::foo> => bar"

Local task ``my-foo`` will poll for the success of ``foo``
in workflow ``other.workflow``, at the same cycle point, succeeding only when
or if it succeeds. Other task states can also be polled:

.. code-block:: cylc

   T00, T12 = "my-foo<other.workflow::foo:fail> => bar"

The default polling parameters (e.g. maximum number of polls and the interval
between them) are printed by ``cylc workflow-state --help`` and can be
configured if necessary under the local polling task runtime section:

.. code-block:: cylc

   [scheduling]
       [[graph]]
           T00,T12 = "my-foo<other.workflow::foo> => bar"
   [runtime]
       [[my-foo]]
           [[[workflow state polling]]]
               max-polls = 100
               interval = PT10S

To poll for the target task to receive a message rather than achieve a state,
give the message in the runtime configuration (in which case the task status
inferred from the graph syntax will be ignored):

.. code-block:: cylc

   [runtime]
       [[my-foo]]
           [[[workflow state polling]]]
               message = "the quick brown fox"

For workflows owned by others, or those with run databases in non-standard
locations, use the ``--run-dir`` option, or in-workflow:

.. code-block:: cylc

   [runtime]
       [[my-foo]]
           [[[workflow state polling]]]
               run-dir = /path/to/top/level/cylc/run-directory

If the remote task has a different cycling sequence, just arrange for the
local polling task to be on the same sequence as the remote task that it
represents. For instance, if local task ``cat`` cycles 6-hourly at
``0,6,12,18`` but needs to trigger off a remote task ``dog``
at ``3,9,15,21``:

.. code-block:: cylc

   [scheduling]
       [[graph]]
           T03,T09,T15,T21 = "my-dog<other.workflow::dog>"
           T00,T06,T12,T18 = "my-dog[-PT3H] => cat"

For workflow-state polling, the cycle point is automatically converted to the
cycle point format of the target workflow.

The remote workflow does not have to be running when polling commences because the
command interrogates the workflow run database, not the :term:`scheduler`.

.. note::

   The graph syntax for workflow polling tasks cannot be combined with
   cycle point offsets, family triggers, or parameterized task notation.
   This does not present a problem because workflow polling tasks can be put on
   the same cycling sequence as the remote-workflow target task (as recommended
   above), and there is no point in having multiple tasks (family members or
   parameterized tasks) performing the same polling operation. Task state
   triggers can be used with workflow polling, e.g. to trigger another task if
   polling fails after 10 tries at 10 second intervals:

   .. code-block:: cylc

      [scheduling]
          [[graph]]
              R1 = "poller<other-workflow::foo:succeed>:fail => another-task"
      [runtime]
          [[my-foo]]
              [[[workflow state polling]]]
                  max-polls = 10
                  interval = PT10S
