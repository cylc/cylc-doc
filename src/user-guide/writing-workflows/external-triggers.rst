.. _Section External Triggers:

External Triggers
=================

External triggers allow tasks to trigger directly off of external events, which
is often preferable to implementing long-running polling tasks in the workflow.
The triggering mechanism described in this section is intended to replace the one
one documented in :ref:`Old-Style External Triggers` (however, that one is a push
mechanism, whereas this one involves regular polling by the scheduler).

If you can write a Python function to check the status of an external
condition or event, the :term:`scheduler` can call it at configurable
intervals until it reports success, at which point dependent tasks can trigger
and data returned by the function will be passed to the job environments of
those tasks. Functions can be written for triggering off of almost anything,
such as delivery of a new dataset, creation of a new entry in a database
table, or appearance of new data availability notifications in a message
broker.

.. TODO - update this once we have static visualisation

   External triggers are visible in workflow visualizations as bare graph nodes (just
   the trigger names). They are plotted against all dependent tasks, not in a
   cycle point specific way like tasks. This is because external triggers may or
   may not be cycle point (or even task name) specific - it depends on the
   arguments passed to the corresponding trigger functions. For example, if an
   external trigger does not depend on task name or cycle point it will only be
   called once - albeit repeatedly until satisfied - for the entire workflow run,
   after which the function result will be remembered for all dependent tasks
   throughout the workflow run.

.. TODO - auto-document these once we have a python endpoint for them

Cylc has several built-in external trigger functions:

- :ref:`Built-in Clock Triggers`
- :ref:`Built-in Workflow State Triggers`

Trigger functions are normal Python functions, with certain constraints as
described below in :ref:`Custom Trigger Functions`.

External triggers are configured in the
:cylc:conf:`flow.cylc[scheduling][xtriggers]` section.

.. NOTE - from here on all references can start [xtriggers]

.. cylc-scope:: flow.cylc[scheduling]


.. _Built-in Clock Triggers:

Built-in Clock Triggers
-----------------------

These are more transparent (exposed in the graph) and efficient (shared among
dependent tasks) than the older clock triggers described
in :ref:`ClockTriggerTasks`.

Clock triggers, unlike other trigger functions, are executed synchronously in
the main process. The clock trigger function signature looks like this:

.. autofunction:: cylc.flow.xtriggers.wall_clock.wall_clock

The ``offset`` argument is a datetime duration (``PT1H`` is 1
hour) relative to the dependent task's cycle point (automatically passed to the
function via a second argument not shown above).

In the following workflow, task ``foo`` has a daily cycle point sequence,
and each task instance can trigger once the wallclock time has passed its
cycle point value by one hour:

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

Notice that the short label ``clock_1`` is used to represent the
trigger function in the graph.

Argument keywords can be omitted if called in the right order, so the
``clock_1`` trigger can also be declared like this:

.. code-block:: cylc

   [[xtriggers]]
       clock_1 = wall_clock(PT1H)

A zero-offset clock trigger does not need to be declared under
the :cylc:conf:`[xtriggers]` section:

.. code-block:: cylc

   [scheduling]
       initial cycle point = 2018-01-01
       [[graph]]
            # zero-offset clock trigger:
           P1D = "@wall_clock => foo"
   [runtime]
       [[foo]]
           script = run-foo.sh

However, when xtriggers are declared the name used must adhere to the following
rules:

.. autoclass:: cylc.flow.unicode_rules.XtriggerNameValidator


.. _Built-in Workflow State Triggers:

Built-in Workflow State Triggers
--------------------------------

These can be used instead of the older workflow state polling tasks described
in :ref:`WorkflowStatePolling` for inter-workflow triggering - i.e. to trigger local
tasks off of remote task statuses or messages in other workflows.

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

Try starting the downstream workflow first, then the upstream, and
watch what happens.
In each cycle point the ``@upstream`` trigger in the downstream workflow
waits on the task ``foo`` (with the same cycle point) in the upstream
workflow to emit the *data ready* message.

Some important points to note about this:

- The function call interval, which determines how often the scheduler
  checks the clock, is optional. Here it is
  ``PT10S`` (i.e. 10 seconds, which is also the default value).
- The ``workflow_state`` trigger function, like the
  ``cylc workflow-state`` command, must have read-access to the upstream
  workflow's public database.
- The cycle point is supplied by a string template
  ``%(point)s``. The string templates available to trigger functions
  arguments are described in :ref:`Custom Trigger Functions`).

The return value of the ``workflow_state`` trigger function looks like
this:

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

The ``satisfied`` variable is boolean (value True or False, depending
on whether or not the trigger condition was found to be satisfied). The
``results`` dictionary contains the names and values of the
target workflow state parameters. Each name gets qualified with the
unique trigger label ("upstream" here) and passed to the environment of
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


.. _Sequential Xtriggers:

Sequential Xtriggers
---------------------------

Parentless tasks (which don't depend on other tasks upstream in the graph)
naturally spawn out to the runahead limit. This may cause UI clutter, and
unnecessary xtrigger checking if the xtriggers would only be satisfied in
order.

You can use *sequential* xtriggers to avoid this problem: the next instance
of a task (i.e., at the next cycle point) that depends on a sequential xtrigger
will not be spawned until the previous xtrigger is satisfied. The
``wall_clock`` xtrigger is sequential by default.

A trigger can be set as sequential in any or all of the following ways.

By setting the workflow-wide :cylc:conf:`flow.cylc[scheduling]sequential xtriggers`
(defaults to ``False``) and/or keyword argument ``sequential`` to ``True``/``False`` in
the xtrigger declaration:

.. literalinclude:: ../../workflows/xtrigger/sequential/flow.cylc
   :language: cylc

When implementing a :ref:`custom xtrigger <Custom Trigger Functions>`, you can
set the default for the ``sequential`` keyword argument in the xtrigger function
definition itself:

.. code-block:: python

   def my_xtrigger(my_in, my_out, sequential=True)

Xtrigger declaration takes precedence over function, and function over workflow
wide setting. So the above workflow definition would read:

- ``foo`` spawns out to the runahead limit.
- ``FAM`` spawns only when ``@upstream`` is satisfied.
- All associated xtriggers are checked and, as expected, their satisfaction
  is a prerequisite to task readiness.


.. _Custom Trigger Functions:

Custom Trigger Functions
------------------------

Trigger functions are just normal Python functions, with a few special
properties:

- They must:

  - Be defined in a module with the same name as the function, unless
    provided using the ``cylc.xtriggers`` entry point;
  - be compatible with the same Python version that runs the scheduler
    (see :ref:`Requirements` for the latest version specification).

- They can be located either:

  - In ``<workflow-dir>/lib/python/``;
  - Anywhere in your ``$CYLC_PYTHONPATH``;
  - Defined using the ``cylc.xtriggers`` entry point for an installed
    package - see :ref:`developing.xtrigger.plugins`

- They can take arbitrary positional and keyword arguments
  (except ``sequential``, which is reserved - see :ref:`Sequential Xtriggers`)
- Workflow and task identity, and cycle point, can be passed to trigger
  functions by using string templates in function arguments (see below)
- Integer, float, boolean, and string arguments will be recognized and
  passed to the function as such
- If a trigger function depends on files or directories (for example)
  that might not exist when the function is first called, just return
- The module can also provide a ``validate`` function for checking configured
  arguments / keyword arguments, see
  :ref:`user-guide.xtrigger-validation-functions` for details.

.. note::

   Trigger functions cannot store data Pythonically between invocations
   because each call is executed in an independent process in the process
   pool. If necessary the filesystem can be used for this purpose.


.. spelling:word-list::

   vv

.. autoenumvalues:: cylc.flow.xtrigger_mgr.TemplateVariables

Function return values should be as follows:

- if the trigger condition is *not satisfied*:

  - return ``(False, {})``

- if the trigger condition is *satisfied*:

  - return ``(True, results)``

where ``results`` is an arbitrary dictionary of information to be passed to
dependent tasks, which in terms of format must:

- be *flat* (non-nested);
- contain *only* keys which are
  `valid <https://pubs.opengroup.org/onlinepubs/9699919799/basedefs/V1_chap08.html>`_ as environment variable names.

See :ref:`Built-in Workflow State Triggers` for an example of one such
``results`` dictionary and how it gets processed by the workflow.

The :term:`scheduler` manages trigger functions as follows:

- they are called asynchronously in the process pool
  - (except for clock triggers, which are called from the main process)
- they are called repeatedly on a configurable interval, until satisfied
  - the call interval defaults to ``PT10S`` (10 seconds)
  - repeat calls are not made until the previous call has returned
- they are subject to the normal process pool command time out - if they
  take too long to return, the process will be killed
- they are shared for efficiency: a single call will be made for all
  triggers that share the same function signature - i.e.\ the same function
  name and arguments
- their return status and results are stored in the workflow DB and persist across
  workflow restarts
- their stdout, if any, is redirected to stderr and will be visible in
  the workflow log in debug mode (stdout is needed to communicate return values
  from the sub-process in which the function executes)


.. _user-guide.xtrigger-validation-functions:

Xtrigger Validation Functions
-----------------------------

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


.. _Built-in Toy Xtriggers:

Toy Examples
^^^^^^^^^^^^

echo
""""

The trivial built-in ``echo`` function takes any number of positional
and keyword arguments (from the workflow configuration) and simply prints
them to stdout, and then returns False (i.e. trigger condition not
satisfied).

.. autofunction:: cylc.flow.xtriggers.echo.echo

Here's an example echo trigger workflow:

.. code-block:: cylc

   [scheduling]
       initial cycle point = now
       [[xtriggers]]
           echo_1 = echo(hello, 99, qux=True, point=%(point)s, foo=10)
       [[graph]]
           PT1H = "@echo_1 => foo"
   [runtime]
       [[foo]]
           script = exit 1

To see the result, run this workflow in debug mode and take a look at the
workflow log (or run ``cylc play --debug --no-detach <workflow>`` and watch
your terminal).


xrandom
"""""""

The built-in ``xrandom`` function sleeps for a configurable amount of
time (useful for testing the effect of a long-running trigger function
- which should be avoided) and has a configurable random chance of
success. The function signature is:

.. automodule:: cylc.flow.xtriggers.xrandom
   :members: xrandom, validate
   :member-order: bysource

An example xrandom trigger workflow:

.. literalinclude:: ../../workflows/xtrigger/xrandom/flow.cylc
   :language: cylc

.. _Current Trigger Function Limitations:

Current Limitations
-------------------

The following issues may be addressed in future Cylc releases:

- trigger labels cannot currently be used in conditional (OR) expressions
  in the graph; attempts to do so will fail validation.
- aside from the predefined zero-offset ``wall_clock`` trigger, all
  unique trigger function calls must be declared *with all of
  their arguments* under the :cylc:conf:`[xtriggers]` section, and
  referred to by label alone in the graph. It would be convenient (and less
  verbose, although no more functional) if we could just declare a label
  against the *common* arguments, and give remaining arguments (such as
  different wallclock offsets in clock triggers) as needed in the graph.
- we may move away from the string templating method for providing workflow
  and task attributes to trigger function arguments.


Filesystem Events?
------------------

Cylc does not have built-in support for triggering off of filesystem events
such as ``inotify`` on Linux. There is no cross-platform standard for
this, and in any case filesystem events are not very useful in HPC cluster
environments where events can only be detected at the specific node on which
they were generated.


Continuous Event Watchers?
--------------------------

For some applications a persistent process that continually monitors the
external world is better than discrete periodic checking. This would be more
difficult to support as a plugin mechanism in Cylc, but we may decide to do it
in the future. In the meantime, consider implementing a small daemon process as
the watcher (e.g. to watch continuously for filesystem events) and have your
Cylc trigger functions interact with it.


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
------------------------------------------

.. note::

   Please read :ref:`Section External Triggers` before using the older
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
