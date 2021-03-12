.. _RunningSuites:

Running Suites
==============

.. TODO - platformise

This chapter currently features a diverse collection of topics related
to running suites.

.. _SuiteStartUp:

Suite Start-Up
--------------

There are three ways to start a suite running: *cold start* and *warm start*,
which start from scratch; and *restart*, which starts from a prior
suite state checkpoint. The only difference between cold starts and warm starts
is that warm starts start from a point beyond the suite initial cycle point.

Once a suite is up and running it is typically a restart that is needed most
often (but see also ``cylc reload``).

.. warning::

   Cold and warm starts wipe out prior suite state, so you can't go back to a
   restart if you decide you made a mistake.


.. _Cold Start:

Cold Start
^^^^^^^^^^

A cold start is the primary way to start a suite run from scratch:

.. code-block:: console

   $ cylc run SUITE [INITIAL_CYCLE_POINT]

The initial cycle point may be specified on the command line or in the :cylc:conf:`flow.cylc`
file. The scheduler starts by loading the first instance of each task at the
suite initial cycle point, or at the next valid point for the task.


.. _Warm Start:

Warm Start
^^^^^^^^^^

A warm start runs a suite from scratch like a cold start, but from the
beginning of a given :term:`cycle point` that is beyond the suite
:term:`initial cycle point`. This is generally inferior to a *restart* (which
loads a previously recorded suite state - see :ref:`RestartingSuites`) because
it may result in some tasks rerunning. However, a warm start may be required if
a restart is not possible, e.g. because the suite run database was accidentally
deleted. The warm start cycle point must be given on the command line:

.. code-block:: console

   $ cylc run --warm SUITE [START_CYCLE_POINT]

The original suite initial cycle point is preserved, but all tasks and
dependencies before the given warm start cycle point are ignored.

The scheduler starts by loading a first instance of each task at the warm
start cycle point, or at the next valid point for the task.
``R1`` type tasks behave exactly the same as other tasks - if their
cycle point is at or later than the given start cycle point, they will run; if
not, they will be ignored.

.. _start_stop_cycle_point:

Start Cycle Point & Stop Cycle Point
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

All workflows have an :term:`initial cycle point` and many have a
:term:`final cycle point`. These determine the range between which Cylc will
schedule tasks to run.

By default when you launch a Cylc :term:`scheduler` to run the workflow,
it will start at the :term:`initial cycle point` and stop at the
:term:`final cycle point`. However, it is possible to start and stop the
scheduler at any arbitrary point.

To do this we use a :term:`start cycle point` and/or :term:`stop cycle point`
when we launch the scheduler
(e.g. ``--start-cycle-point`` and ``--stop-cycle-point`` CLI arguments).

For example if we were to run the following workflow:

.. code-block:: cylc

   [scheduling]
       cycling mode = integer
       initial cycle point = 1
       final cycle point = 5
       [[graph]]
           # every cycle: 1, 2, 3, 4, 5
           P1 = foo
           # every other cycle: 1, 3, 5
           P2 = bar

With a :term:`start cycle point` of ``2`` and a :term:`stop cycle point` of
``4``, then the task ``foo`` would run at cycles 2, 3 & 4 and the task ``bar``
would only run at cycle ``3``.

.. image:: ../img/initial-start-stop-final-cp.svg
   :align: center

* The initial and final cycle points are at the start and end of the graph.
* The start and stop cycle points determine the part of the graph that the scheduler runs.


.. _RestartingSuites:

Restart and Suite State Checkpoints
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

At restart (see ``cylc restart --help``) a :term:`scheduler`
initializes its task pool from a previously recorded checkpoint state. By
default the latest automatic checkpoint - which is updated with every task
state change - is loaded so that the suite can carry on exactly as it was just
before being shut down or killed.

.. code-block:: console

   $ cylc restart SUITE

Tasks recorded in the "submitted" or "running" states are automatically polled
(see :ref:`Task Job Polling`) at start-up to determine what happened to
them while the suite was down.


Restart From Latest Checkpoint
""""""""""""""""""""""""""""""

To restart from the latest checkpoint simply invoke the ``cylc restart``
command with the suite name.

.. code-block:: console

   $ cylc restart SUITE


Restart From Another Checkpoint
"""""""""""""""""""""""""""""""

Suite server programs automatically update the "latest" checkpoint every time
a task changes state, and at every suite restart, but you can also take
checkpoints at other times. To tell a :term:`scheduler` to checkpoint its
current state:

.. code-block:: console

   $ cylc checkpoint SUITE-NAME CHECKPOINT-NAME

The 2nd argument is a name to identify the checkpoint later with:

.. code-block:: console

   $ cylc ls-checkpoints SUITE-NAME

For example, with checkpoints named "bob", "alice", and "breakfast":

.. code-block:: console

   $ cylc ls-checkpoints SUITE-NAME
   #######################################################################
   # CHECKPOINT ID (ID|TIME|EVENT)
   1|2017-11-01T15:48:34+13|bob
   2|2017-11-01T15:48:47+13|alice
   3|2017-11-01T15:49:00+13|breakfast
   ...
   0|2017-11-01T17:29:19+13|latest

To see the actual task state content of a given checkpoint ID (if you need to),
for the moment you have to interrogate the suite DB, e.g.:

.. code-block:: console

   $ sqlite3 ~/cylc-run/SUITE-NAME/log/db \
       'select * from task_pool_checkpoints where id == 3;'
   3|2012|model|1|running|
   3|2013|pre|0|waiting|
   3|2013|post|0|waiting|
   3|2013|model|0|waiting|
   3|2013|upload|0|waiting|

.. note::

   A checkpoint captures the instantaneous state of every task in the
   suite, including any tasks that are currently active, so you may want
   to be careful where you do it. Tasks recorded as active are polled
   automatically on restart to determine what happened to them.

The checkpoint ID 0 (zero) is always used for latest state of the suite, which
is updated continuously as the suite progresses. The checkpoint IDs of earlier
states are positive integers starting from 1, incremented each time a new
checkpoint is stored. Currently suites automatically store checkpoints before
and after reloads, and on restarts (using the latest checkpoints before the
restarts).

Once you have identified the right checkpoint, restart the suite like this:

.. code-block:: console

   $ cylc restart --checkpoint=CHECKPOINT-ID SUITE


Checkpointing With A Task
"""""""""""""""""""""""""

Checkpoints can be generated automatically at particular points in the
workflow by coding tasks that run the ``cylc checkpoint`` command:

.. code-block:: cylc

   [scheduling]
      [[graph]]
         PT6H = "pre => model => post => checkpointer"
   [runtime]
      # ...
      [[checkpointer]]
         script = """
             wait "${CYLC_TASK_MESSAGE_STARTED_PID}" 2>/dev/null || true
             cylc checkpoint ${CYLC_SUITE_NAME} CP-${CYLC_TASK_CYCLE_POINT}
         """

.. note::

   We need to "wait" on the "task started" message - which
   is sent in the background to avoid holding tasks up in a network
   outage - to ensure that the checkpointer task is correctly recorded
   as running in the checkpoint (at restart the :term:`scheduler` will
   poll to determine that that task job finished successfully). Otherwise
   it may be recorded in the waiting state and, if its upstream dependencies
   have already been cleaned up, it will need to be manually reset from waiting
   to succeeded after the restart to avoid stalling the suite.


Behaviour of Tasks on Restart
"""""""""""""""""""""""""""""

All tasks are reloaded in exactly their checkpointed states. Failed tasks are
not automatically resubmitted at restart in case the underlying problem has not
been addressed yet.

Tasks recorded in the submitted or running states are automatically polled on
restart, to see if they are still waiting in a :term:`job runner` queue, still running, or
if they succeeded or failed while the suite was down. The suite state will be
updated automatically according to the poll results.

Existing instances of tasks removed from the suite configuration before restart
are not removed from the task pool automatically, but they will not spawn new
instances. They can be removed manually if necessary,
with ``cylc remove``.

Similarly, instances of new tasks added to the suite configuration before
restart are not inserted into the task pool automatically, because it is
very difficult in general to automatically determine the cycle point of
the first instance. Instead, the first instance of a new task should be
inserted manually at the right cycle point, with ``cylc insert``.


Reloading The Suite Configuration At Runtime
--------------------------------------------

The ``cylc reload`` command tells a :term:`scheduler` to reload its
suite configuration at run time. This is an alternative to shutting a
suite down and restarting it after making changes.

As for a restart, existing instances of tasks removed from the suite
configuration before reload are not removed from the task pool
automatically, but they will not spawn new instances. They can be removed
manually if necessary, with ``cylc remove``.

Similarly, instances of new tasks added to the suite configuration before
reload are not inserted into the pool automatically. The first instance of each
must be inserted manually at the right cycle point, with ``cylc insert``.


.. _The Suite Contact File:

The Suite Contact File
----------------------

At start-up, :term:`schedulers <scheduler>` write a :term:`contact file`
``$HOME/cylc-run/SUITE/.service/contact`` that records suite host,
user, port number, process ID, Cylc version, and other information. Client
commands can read this file, if they have access to it, to find the target
:term:`scheduler`.


.. _Authentication Files:

Authentication Files
--------------------

Cylc uses `CurveZMQ <http://curvezmq.org/page:read-the-docs/>`_ to ensure that
any data, sent between the :term:`scheduler <scheduler>` and the client,
remains protected during transmission. Public keys are used to encrypt the
data, private keys for decryption.

Authentication files will be created in your
``$HOME/cylc-run/WORKFLOW/.service/`` directory at start-up. You can expect to
find one client public key per file system for remote jobs.

On the workflow host, the directory structure should contain:

   .. code-block:: none

         ~/cylc-run/workflow_x
         |__.service
            |__client_public_keys
            |  \-- client_localhost.key
            |  \-- <any further client keys>
         |  \-- client.key_secret
         |  \-- server.key
         |  \-- server.key_secret

On the remote job host, the directory structure should contain:

   .. code-block:: none

         ~/cylc-run/workflow_x
         |__.service
            \-- client.key
            \-- client.key_secret
            \-- server.key

Keys are removed as soon as they are no longer required.


.. _Task Job Polling:

Task Job Polling
----------------

At any point after job submission task jobs can be *polled* to check that
their true state conforms to what is currently recorded by the suite server
program. See ``cylc poll --help`` for how to poll one or more tasks
manually.

Polling may be necessary if, for example, a task job gets killed by the
untrappable SIGKILL signal (e.g. ``kill -9 PID``), or if a network
outage prevents task success or failure messages getting through, or if the
:term:`scheduler` itself is down when tasks finish execution.

To poll a task job the :term:`scheduler` interrogates the
:term:`job runner`, and the ``job.status`` file, on the job host. This
information is enough to determine the final task status even if the
job finished while the :term:`scheduler` was down or unreachable on
the network.


Routine Polling
^^^^^^^^^^^^^^^

Task jobs are automatically polled at certain times: once on job submission
timeout; several times on exceeding the job execution time limit; and at suite
restart any tasks recorded as active in the suite state checkpoint are polled
to find out what happened to them while the suite was down.

Finally, in necessary routine polling can be configured as a way to track job
status on job hosts that do not allow networking routing back to the suite host
for task messaging by TCP or SSH. See :ref:`Polling To Track Job Status`.


.. _TaskComms:

Tracking Task State
-------------------

Cylc supports two ways of tracking task state on job hosts:

- task-to-suite messaging via TCP (using ZMQ protocol)
- regular polling by the :term:`scheduler`

These can be configured per job host using
:cylc:conf:`global.cylc[platforms][<platform name>]communication method`.

If your site prohibits TCP and SSH back from job hosts to
suite hosts, before resorting to the polling method you should
consider installing dedicated Cylc servers or
VMs inside the HPC trust zone (where TCP and SSH should be allowed).

It is also possible to run Cylc :term:`schedulers <scheduler>` on HPC login
nodes, but this is not recommended for load and run duration,

Finally, it has been suggested that *port forwarding* may provide another
solution - but that is beyond the scope of this document.


TCP Task Messaging
^^^^^^^^^^^^^^^^^^

Task job wrappers automatically invoke ``cylc message`` to report
progress back to the :term:`scheduler` when they begin executing,
at normal exit (success) and abnormal exit (failure).

By default the messaging occurs via an authenticated, TCP connection to the
:term:`scheduler` using the ZMQ protocol.
This is the preferred task communications method - it is efficient and direct.

Suite server programs automatically install suite :term:`contact information
<contact file>` and credentials on job hosts. Users only need to do this
manually for remote access to suites on other hosts, or suites owned by other
users - see :ref:`RemoteControl`.

.. _Polling To Track Job Status:

Polling to Track Job Status
^^^^^^^^^^^^^^^^^^^^^^^^^^^

Suite server programs can actively poll task jobs at configurable intervals,
via non-interactive SSH to the job host.

Polling is the least efficient task communications method because task state is
updated only at intervals, not when task events actually occur. However, it
may be needed at sites that do not allow TCP or non-interactive SSH from job
host to suite host.

Be careful to avoid spamming task hosts with polling commands. Each poll
opens (and then closes) a new SSH connection.

Polling intervals are configurable under :cylc:conf:`[runtime]` because
they should may depend on the expected execution time. For instance, a
task that typically takes an hour to run might be polled every 10
minutes initially, and then every minute toward the end of its run.
Interval values are used in turn until the last value, which is used
repeatedly until finished:

.. TODO - platformise this example

.. code-block:: cylc

   [runtime]
       [[foo]]
           # poll every minute in the 'submitted' state:
           submission polling intervals = PT1M

           # poll one minute after foo starts running, then every 10
           # minutes for 50 minutes, then every minute until finished:
           execution polling intervals = PT1M, 5*PT10M, PT1M

.. cylc-scope:: global.cylc[platforms][<platform name>]

A list of intervals with optional multipliers can be used for both submission
and execution polling, although a single value is probably sufficient for
submission polling. If these items are not configured default values from
site and user global config will be used for
:cylc:conf:`communication method = polling`; polling is not done by default
under the other task communications methods (but it can still be used
if you like).

.. cylc-scope::


.. _ConnectionAuthentication:

Client-Server Interaction
-------------------------

Cylc server programs listen on dedicated network ports for
TCP communications from Cylc clients (task jobs and user-invoked commands)

Use ``cylc scan`` to see which suites are listening on which ports on
scanned hosts.

Cylc generates public-private key pairs on the suite server and job hosts
which are used for authentication.


.. _RemoteControl:

Remote Control
--------------

Cylc client programs connect to running suites using information stored in
the :term:`contact file` in the suite :term:`run directory`.

This means that Cylc can interact with suites running on another host provided
that they share the filesystem on which the :term:`run directory`
(``cylc-run``) is located.

If the hosts do not share a filesystem you must use SSH when calling Cylc client
commands.


Task States Explained
---------------------

As a suite runs, its task proxies may pass through the following states:

- **waiting** - still waiting for prerequisites (e.g. dependence on
  other tasks, and clock triggers) to be satisfied.
- **queued** - ready to run (prerequisites satisfied) but
  temporarily held back by an *internal cylc queue*
  (see :ref:`InternalQueues`).
- **ready** - ready to run (prerequisites satisfied) and
  handed to cylc's job submission sub-system.
- **submitted** - submitted to run, but not executing yet
  (could be waiting in an external :term:`job runner` queue).
- **submit-failed** - job submission failed *or*
  submitted job killed (cancelled) before commencing execution.
- **submit-retrying** - job submission failed, but a submission retry
  was configured. Will only enter the *submit-failed* state if all
  configured submission retries are exhausted.
- **running** - currently executing (a *task started*
  message was received, or the task polled as running).
- **succeeded** - finished executing successfully (a *task
  succeeded* message was received, or the task polled as succeeded).
- **failed** - aborted execution due to some error condition (a
  *task failed* message was received, or the task polled as failed).
- **retrying** - job execution failed, but an execution retry
  was configured. Will only enter the *failed* state if all configured
  execution retries are exhausted.
- **runahead** - will not have prerequisites checked (and so
  automatically held, in effect) until the rest of the suite catches up
  sufficiently. The amount of runahead allowed is configurable - see
  :ref:`RunaheadLimit`.
- **expired** - will not be submitted to run, due to falling too far
  behind the wall-clock relative to its cycle point -
  see :ref:`ClockExpireTasks`.


.. _RunaheadLimit:

Runahead Limiting
-----------------

Runahead limiting prevents the fastest tasks in a suite from getting too far
ahead of the slowest ones.

For example in the following workflow the runahead limit of ``P5`` restricts the
workflow so that only five consecutive cycles may run simultaneously.

.. code-block:: cylc

   [scheduling]
       initial cycle point = 1
       cycling mode = integer
       runahead limit = P5
       [[graph]]
           P1 = foo

When this workflow is started the tasks ``foo.1`` -> ``foo.5`` will be submitted,
however, the tasks from ``foo.6`` onwards are said to be "runahead limited"
and will not be submitted.

Succeeded and failed tasks are ignored when computing the runahead limit. This
functionality is controlled by the :cylc:conf:`[scheduling]runahead limit`
which can be set to either:

* A number of consecutive cycles.
* Or a time interval between the oldest and newest cycles.

A low runahead limit can prevent Cylc from interleaving cycles, but it will not
stall a suite unless it fails to extend out past a future trigger (see
:ref:`InterCyclePointTriggers`).

A high runahead limit may allow fast tasks
that are not constrained by dependencies or clock-triggers to spawn far ahead
of the pack, which could have performance implications for the
:term:`scheduler` when running very large suites.

See the :cylc:conf:`[scheduling]runahead limit` configuration for more details.


.. _InternalQueues:

Limiting Activity With Internal Queues
--------------------------------------

Large suites can potentially overwhelm task hosts by submitting too many
tasks at once. You can prevent this with *internal queues*, which
limit the number of tasks that can be active (submitted or running)
at the same time.

Internal queues behave in the first-in-first-out (FIFO) manner, i.e. tasks are
released from a queue in the same order that they were queued.

A queue is defined by a *name*; a *limit*, which is the maximum
number of active tasks allowed for the queue; and a list of *members*,
assigned by task or family name.

Queue configuration is done in the :cylc:conf:`[scheduling][queues]` section.

By default every task is assigned to the ``default`` queue, which by default
has a zero limit (interpreted by cylc as no limit). To use a single queue for
the whole suite just set the default queue limit:

.. code-block:: cylc

   [scheduling]
       [[queues]]
           # limit the entire suite to 5 active tasks at once
           [[[default]]]
               limit = 5

To use additional queues just name each one, set their limits, and assign
members:

.. code-block:: cylc

   [scheduling]
       [[queues]]
           [[[q_foo]]]
               limit = 5
               members = foo, bar, baz

Any tasks not assigned to a particular queue will remain in the default
queue. The *queues* example suite illustrates how queues work by
running two task trees side by side each
limited to 2 and 3 tasks respectively:

.. literalinclude:: ../suites/queues/flow.cylc
   :language: cylc


.. _TaskRetries:

Automatic Task Retry On Failure
-------------------------------

See also :cylc:conf:`[runtime][<namespace>]execution retry delays`.

Tasks can be configured with a list of "retry delay" intervals, as
:term:`ISO8601 durations <ISO8601 duration>`. If the task job fails it will go
into the *retrying* state and resubmit after the next configured delay
interval. An example is shown in the suite listed below under
:ref:`EventHandling`.

If a task with configured retries is *killed* (by ``cylc kill``
it goes to the *held* state so that the operator can decide
whether to release it and continue the retry sequence or to abort the retry
sequence by manually resetting it to the *failed* state.


.. _EventHandling:

Task Event Handling
-------------------

* Task events (e.g. task succeeded/failed) are configured by
  :cylc:conf:`task events <[runtime][<namespace>][events]>`.
* Suite events (e.g. suite started/stopped) are configured by
  :cylc:conf:`suite events <[scheduler][events]>`

.. cylc-scope:: flow.cylc[runtime][<namespace>]

Cylc can call nominated event handlers - to do whatever you like - when certain
suite or task events occur. This facilitates centralized alerting and automated
handling of critical events. Event handlers can be used to send a message, call
a pager, or whatever; they can even intervene in the operation of their own
suite using cylc commands.

To send an email, use the built-in setting :cylc:conf:`[events]mail events`
to specify a list of events for which notifications should be sent. (The
name of a registered task output can also be used as an event name in
this case.) E.g. to send an email on (submission) failed and retry:

.. code-block:: cylc

   [runtime]
       [[foo]]
           script = """
               test ${CYLC_TASK_TRY_NUMBER} -eq 3
               cylc message -- "${CYLC_SUITE_NAME}" "${CYLC_TASK_JOB}" 'oopsy daisy'
           """
           execution retry delays = PT0S, PT30S
           [[[events]]]
               mail events = submission failed, submission retry, failed, retry, oops
           [[[outputs]]]
               oops = oopsy daisy

By default, the emails will be sent to the current user with:

- ``to:`` set as ``$USER``
- ``from:`` set as ``notifications@$(hostname)``
- SMTP server at ``localhost:25``

These can be configured using the settings:

.. cylc-scope:: flow.cylc[runtime][<namespace>]

- :cylc:conf:`[mail]to` (list of email addresses)
- :cylc:conf:`[mail]from`

.. cylc-scope::

By default, a cylc suite will send you no more than one task event email every
5 minutes - this is to prevent your inbox from being flooded by emails should a
large group of tasks all fail at similar time. This is configured by
:cylc:conf:`[scheduler][mail]task event batch interval`.

Event handlers can be located in the suite ``bin/`` directory;
otherwise it is up to you to ensure their location is in ``$PATH`` (in
the shell in which the :term:`scheduler` runs). They should require little
resource and return quickly - see :ref:`Managing External Command Execution`.

.. cylc-scope:: flow.cylc[runtime][<namespace>]

Task event handlers can be specified using the
``[events]<event> handler`` settings, where
``<event>`` is one of:

- 'submitted' - the job submit command was successful
- 'submission failed' - the job submit command failed
- 'submission timeout' - task job submission timed out
- 'submission retry' - task job submission failed, but will retry after
  a configured delay
- 'started' - the task reported commencement of execution
- 'succeeded' - the task reported successful completion
- 'warning' - the task reported a WARNING severity message
- 'critical' - the task reported a CRITICAL severity message
- 'custom' - the task reported a CUSTOM severity message
- 'late' - the task is never active and is late
- 'failed' - the task failed
- 'retry' - the task failed but will retry after a configured delay
- 'execution timeout' - task execution timed out

The value of each setting should be a list of command lines or command line
templates (see below).

Alternatively you can use :cylc:conf:`[events]handlers` and
:cylc:conf:`[events]handler events`, where the former is a list of command
lines or command line templates (see below) and the latter is a list of events
for which these commands should be invoked. (The name of a registered task
output can also be used as an event name in this case.)

.. cylc-scope::

Event handler arguments can be constructed from various templates
representing suite name; task ID, name, cycle point, message, and submit
number name; and any :cylc:conf:`suite <[meta]>` or
:cylc:conf:`task <[runtime][<namespace>][meta]>` item.
See :cylc:conf:`suite events <[scheduler][events]>` and
:cylc:conf:`task events <[runtime][<namespace>][events]>` for options.

If no template arguments are supplied the following default command line
will be used:

.. code-block:: none

   <task-event-handler> %(event)s %(suite)s %(id)s %(message)s

.. note::

   Substitution patterns should not be quoted in the template strings.
   This is done automatically where required.

For an explanation of the substitution syntax, see
`String Formatting Operations
<https://docs.python.org/2/library/stdtypes.html#string-formatting>`_
in the Python documentation.

The retry event occurs if a task fails and has any remaining retries
configured (see :ref:`TaskRetries`).
The event handler will be called as soon as the task fails, not after
the retry delay period when it is resubmitted.

.. note::

   Event handlers are called by the :term:`scheduler`, not by
   task jobs. If you wish to pass additional information to them use
   ``[scheduler] -> [[environment]]``, not task runtime environment.

The following two :cylc:conf:`flow.cylc` snippets are examples on how to specify
event handlers using the alternate methods:

.. code-block:: cylc

   [runtime]
       [[foo]]
           script = test ${CYLC_TASK_TRY_NUMBER} -eq 2
           execution retry delays = PT0S, PT30S
           [[[events]]]
               retry handler = "echo '!!!!!EVENT!!!!!' "
               failed handler = "echo '!!!!!EVENT!!!!!' "

.. code-block:: cylc

   [runtime]
       [[foo]]
           script = """
               test ${CYLC_TASK_TRY_NUMBER} -eq 2
               cylc message -- "${CYLC_SUITE_NAME}" "${CYLC_TASK_JOB}" 'oopsy daisy'
           """
           execution retry delays = PT0S, PT30S
           [[[events]]]
               handlers = "echo '!!!!!EVENT!!!!!' "
               # Note: task output name can be used as an event in this method
               handler events = retry, failed, oops
           [[[outputs]]]
               oops = oopsy daisy

The handler command here - specified with no arguments - is called with the
default arguments, like this:

.. code-block:: bash

   echo '!!!!!EVENT!!!!!' %(event)s %(suite)s %(id)s %(message)s


.. _Late Events:

Late Events
^^^^^^^^^^^

You may want to be notified when certain tasks are running late in a real time
production system - i.e. when they have not triggered by *the usual time*.
Tasks of primary interest are not normally clock-triggered however, so their
trigger times are mostly a function of how the suite runs in its environment,
and even external factors such as contention with other suites [3]_ .

But if your system is reasonably stable from one cycle to the next such that a
given task has consistently triggered by some interval beyond its cycle point,
you can configure Cylc to emit a *late event* if it has not triggered by
that time. For example, if a task ``forecast`` normally triggers by 30
minutes after its cycle point, configure late notification for it like this:

.. code-block:: cylc

   [runtime]
      [[forecast]]
           script = run-model.sh
           [[[events]]]
               late offset = PT30M
               late handler = my-handler %(message)s

*Late offset intervals are not computed automatically so be careful
to update them after any change that affects triggering times.*

.. note::

   Cylc can only check for lateness in tasks that it is currently aware
   of. If a suite gets delayed over many cycles the next tasks coming up
   can be identified as late immediately, and subsequent tasks can be
   identified as late as the suite progresses to subsequent cycle points,
   until it catches up to the clock.


.. _Managing External Command Execution:

Managing External Command Execution
-----------------------------------

Job submission commands, event handlers, and job poll and kill commands, are
executed by the :term:`scheduler` in a "pool" of asynchronous
subprocesses, in order to avoid holding the suite up. The process pool is
actively managed to limit it to a configurable size
:cylc:conf:`global.cylc[scheduler]process pool size`
Custom event handlers should be light-weight and quick-running because they
will tie up a process pool member until they complete, and the suite will
appear to stall if the pool is saturated with long-running processes. Processes
are killed after a configurable timeout
:cylc:conf:`global.cylc[scheduler]process pool timeout`
, however,
to guard against rogue commands that hang indefinitely. All process kills are
logged by the :term:`scheduler`. For killed job submissions the associated
tasks also go to the *submit-failed* state.


.. _PreemptionHPC:

Handling Job Preemption
-----------------------

Some HPC facilities allow job preemption: the resource manager can kill
or suspend running low priority jobs in order to make way for high
priority jobs. The preempted jobs may then be automatically restarted
by the resource manager, from the same point (if suspended) or requeued
to run again from the start (if killed).

Suspended jobs will poll as still running (their job status file says they
started running, and they still appear in the resource manager queue).
Loadleveler jobs that are preempted by kill-and-requeue ("job vacation") are
automatically returned to the submitted state by Cylc. This is possible
because Loadleveler sends the SIGUSR1 signal before SIGKILL for preemption.
Other :term:`job runners <job runner>` just send SIGTERM before SIGKILL as normal, so Cylc
cannot distinguish a preemption job kill from a normal job kill. After this the
job will poll as failed (correctly, because it was killed, and the job status
file records that). To handle this kind of preemption automatically you could
use a task failed or retry event handler that queries the job runner queue
(after an appropriate delay if necessary) and then, if the job has been
requeued, uses ``cylc reset`` to reset the task to the submitted state.


Manual Task Triggering and Edit-Run
-----------------------------------

Any task proxy currently present in the suite can be manually triggered at any
time using the ``cylc trigger`` command.
If the task belongs to a limited internal queue
(see :ref:`InternalQueues`), this will queue it; if not, or if it is already
queued, it will submit immediately.

With ``cylc trigger --edit``
you can edit the generated task job script to make one-off changes before the
task submits.


.. _cylc-broadcast:

Cylc Broadcast
--------------

The ``cylc broadcast`` command overrides :cylc:conf:`[runtime]`
settings in a running suite. This can
be used to communicate information to downstream tasks by broadcasting
environment variables (communication of information from one task to
another normally takes place via the filesystem, i.e. the input/output
file relationships embodied in inter-task dependencies). Variables (and
any other runtime settings) may be broadcast to all subsequent tasks,
or targeted specifically at a specific task, all subsequent tasks with a
given name, or all tasks with a given cycle point; see broadcast command help
for details.

Broadcast settings targeted at a specific task ID or cycle point expire and
are forgotten as the suite moves on. Un-targeted variables and those
targeted at a task name persist throughout the suite run, even across
restarts, unless manually cleared using the broadcast command - and so
should be used sparingly.


The Meaning And Use Of Initial Cycle Point
------------------------------------------

When a suite is started with the ``cylc run`` command (cold or
warm start) the cycle point at which it starts can be given on the command
line or hardwired into the :cylc:conf:`flow.cylc` file:

.. code-block:: console

   $ cylc run foo 20120808T06Z

or:

.. code-block:: cylc

   [scheduling]
       initial cycle point = 20100808T06Z

An initial cycle given on the command line will override one in the
flow.cylc file.

.. _setting-the-icp-relative-to-now:

Setting The Initial Cycle Point Relative To The Current Time
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. warning::

   Setting the initial cycle point relative to the current time only works
   for :term:`datetime cycling` suites which use the Gregorian calendar and
   will not work for alternative calendars like the 360, 365 or 366 day
   calendars.

Two additional commands, ``next`` and ``previous``, can be used when setting
the initial cycle point.

The syntax uses truncated ISO8601 time representations, and is of the style:
``next(Thh:mmZ)``, ``previous(T-mm)``; e.g.

* ``initial cycle point = next(T15:00Z)``
* ``initial cycle point = previous(T09:00)``
* ``initial cycle point = next(T12)``
* ``initial cycle point = previous(T-20)``

A list of times, separated by semicolons, can be provided, e.g.
``next(T-00;T-15;T-30;T-45)``. At least one time is required within the
brackets, and if more than one is given, the major time unit in each (hours
or minutes) should all be of the same type.

If an offset from the specified date or time is required, this should be
used in the form: ``previous(Thh:mm) +/- PxTy`` in the same way as is used
for determining cycle periods, e.g.

* ``initial cycle point = previous(T06) +P1D``
* ``initial cycle point = next(T-30) -PT1H``

The section in the bracket attached to the next/previous command is
interpreted first, and then the offset is applied.

The offset can also be used independently without a ``next`` or ``previous``
command, and will be interpreted as an offset from "now".

.. table:: Examples of setting relative initial cycle point for times and offsets using ``now = 2018-03-14T15:12Z`` (and UTC mode)

   ====================================  ==================
   Syntax                                Interpretation
   ====================================  ==================
   ``next(T-00)``                        2018-03-14T16:00Z
   ``previous(T-00)``                    2018-03-14T15:00Z
   ``next(T-00; T-15; T-30; T-45)``      2018-03-14T15:15Z
   ``previous(T-00; T-15; T-30; T-45)``  2018-03-14T15:00Z
   ``next(T00)``                         2018-03-15T00:00Z
   ``previous(T00)``                     2018-03-14T00:00Z
   ``next(T06:30Z)``                     2018-03-15T06:30Z
   ``previous(T06:30) -P1D``             2018-03-13T06:30Z
   ``next(T00; T06; T12; T18)``          2018-03-14T18:00Z
   ``previous(T00; T06; T12; T18)``      2018-03-14T12:00Z
   ``next(T00; T06; T12; T18) +P1W``     2018-03-21T18:00Z
   ``PT1H``                              2018-03-14T16:12Z
   ``-P1M``                              2018-02-14T15:12Z
   ====================================  ==================

The relative initial cycle point also works with truncated dates, including
weeks and ordinal date, using ISO8601 truncated date representations.
Note that day-of-week should always be specified when using weeks. If a time
is not included, the calculation of the next or previous corresponding
point will be done from midnight of the current day.

.. table:: Examples of setting relative initial cycle point for dates using ``now = 2018-03-14T15:12Z`` (and UTC mode)

   ====================================  ==================
   Syntax                                Interpretation
   ====================================  ==================
   ``next(-00)``                         2100-01-01T00:00Z
   ``previous(--01)``                    2018-01-01T00:00Z
   ``next(---01)``                       2018-04-01T00:00Z
   ``previous(--1225)``                  2017-12-25T00:00Z
   ``next(-2006)``                       2020-06-01T00:00Z
   ``previous(-W101)``                   2018-03-05T00:00Z
   ``next(-W-1; -W-3; -W-5)``            2018-03-14T00:00Z
   ``next(-001; -091; -181; -271)``      2018-04-01T00:00Z
   ``previous(-365T12Z)``                2017-12-31T12:00Z
   ====================================  ==================


The Environment Variable CYLC\_SUITE\_INITIAL\_CYCLE\_POINT
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

In the case of a *cold start only* the initial cycle point is passed
through to task execution environments as
``$CYLC_SUITE_INITIAL_CYCLE_POINT``. The value is then stored in
suite database files and persists across restarts, but it does get wiped out
(set to ``None``) after a warm start, because a warm start is really an
implicit restart in which all state information is lost (except that the
previous cycle is assumed to have completed).

The ``$CYLC_SUITE_INITIAL_CYCLE_POINT`` variable allows tasks to
determine if they are running in the initial cold-start cycle point, when
different behaviour may be required, or in a normal mid-run cycle point.
Note however that an initial ``R1`` graph section is now the preferred
way to get different behaviour at suite start-up.


.. _SimulationMode:

Simulating Suite Behaviour
--------------------------

Several suite run modes allow you to simulate suite behaviour quickly without
running the suite's real jobs - which may be long-running and resource-hungry:

dummy mode
   Runs tasks as background jobs on configured job hosts.

   This simulates scheduling, job host connectivity, and generates all job
   files on suite and job hosts.
dummy-local mode
   Runs real tasks as background jobs on the suite host, which allows
   dummy-running suites from other sites.

   This simulates scheduling and generates all job files on the suite host.
simulation mode
   Does not run any real tasks.

   This simulates scheduling without generating any job files.

Set the run mode (default ``live``) on the command line:

.. code-block:: console

   $ cylc run --mode=dummy SUITE
   $ cylc restart --mode=dummy SUITE

You can get specified tasks to fail in these modes, for more flexible suite
testing. See cylc:conf:`[runtime][<namespace>][simulation]`.


Proportional Simulated Run Length
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

If :cylc:conf:`[runtime][<namespace>]execution time limit` is set, Cylc
divides it by :cylc:conf:`[runtime][<namespace>][simulation]speedup factor` to compute simulated task
run lengths.


Limitations Of Suite Simulation
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Dummy mode ignores :term:`job runner` settings because Cylc does not know which
job resource directives (requested memory, number of compute nodes, etc.) would
need to be changed for the dummy jobs. If you need to dummy-run jobs on a
job runner manually comment out ``script`` items and modify
directives in your live suite, or else use a custom live mode test suite.

.. note::

   The dummy modes ignore all configured task ``script`` items
   including ``init-script``. If your ``init-script`` is required
   to run even blank/empty tasks on a job host, note that host environment
   setup should be done elsewhere.


Restarting Suites With A Different Run Mode?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The run mode is recorded in the suite run database files. Cylc will not let
you *restart* a non-live mode suite in live mode, or vice versa. To
test a live suite in simulation mode just take a quick copy of it and run the
the copy in simulation mode.


.. _AutoRefTests:

Automated Reference Test Suites
-------------------------------

Reference tests are finite-duration suite runs that abort with non-zero
exit status if any of the following conditions occur (by default):

- cylc fails
- any task fails
- the suite times out (e.g. a task dies without reporting failure)
- a nominated shutdown event handler exits with error status

When a reference test suite shuts down, it compares task triggering
information (what triggers off what at run time) in the test run suite
log to that from an earlier reference run, disregarding the timing and
order of events - which can vary according to the external queueing
conditions, runahead limit, and so on.

To prepare a reference log for a suite, run it with the
``--reference-log`` option, and manually verify the
correctness of the reference run.

To reference test a suite, just run it (in dummy mode for the most
comprehensive test without running real tasks) with the
``--reference-test`` option.

A battery of automated reference tests is used to test cylc before
posting a new release version. Reference tests can also be used to check that
a cylc upgrade will not break your own complex
suites - the triggering check will catch any bug that causes a task to
run when it shouldn't, for instance; even in a dummy mode reference
test the full task job script (sans ``script`` items) executes on the
proper task host by the proper :term:`job runner`.

Reference tests can be configured with the following settings:

.. code-block:: cylc

   [scheduler]
       [[reference test]]
           expected task failures = t1.1


Roll-your-own Reference Tests
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

If the default reference test is not sufficient for your needs, firstly
note that you can override the default shutdown event handler, and
secondly that the ``--reference-test`` option is merely a short
cut to the following :cylc:conf:`flow.cylc` settings which can also be set manually if
you wish:

.. code-block:: cylc

   [scheduler]
       [[events]]
           timeout = PT5M
           abort if shutdown handler fails = True
           abort on timeout = True


.. _SuiteStatePolling:

Triggering Off Of Tasks In Other Suites
---------------------------------------

.. note::

   Please read :ref:`Section External Triggers` before using
   the older inter-suite triggering mechanism described in this section.

The ``cylc suite-state`` command interrogates suite run databases. It
has a polling mode that waits for a given task in the target suite to achieve a
given state, or receive a given message. This can be used to make task
scripting wait for a remote task to succeed (for example).

Automatic suite-state polling tasks can be defined with in the graph. They get
automatically-generated task scripting that uses ``cylc suite-state``
appropriately (it is an error to give your own ``script`` item for these
tasks).

Here's how to trigger a task ``bar`` off a task ``foo`` in
a remote suite called ``other.suite``:

.. code-block:: cylc

   [scheduling]
       [[graph]]
           T00, T12 = "my-foo<other.suite::foo> => bar"

Local task ``my-foo`` will poll for the success of ``foo``
in suite ``other.suite``, at the same cycle point, succeeding only when
or if it succeeds. Other task states can also be polled:

.. code-block:: cylc

   T00, T12 = "my-foo<other.suite::foo:fail> => bar"

The default polling parameters (e.g. maximum number of polls and the interval
between them) are printed by ``cylc suite-state --help`` and can be
configured if necessary under the local polling task runtime section:

.. code-block:: cylc

   [scheduling]
       [[graph]]
           T00,T12 = "my-foo<other.suite::foo> => bar"
   [runtime]
       [[my-foo]]
           [[[suite state polling]]]
               max-polls = 100
               interval = PT10S

To poll for the target task to receive a message rather than achieve a state,
give the message in the runtime configuration (in which case the task status
inferred from the graph syntax will be ignored):

.. code-block:: cylc

   [runtime]
       [[my-foo]]
           [[[suite state polling]]]
               message = "the quick brown fox"

For suites owned by others, or those with run databases in non-standard
locations, use the ``--run-dir`` option, or in-suite:

.. code-block:: cylc

   [runtime]
       [[my-foo]]
           [[[suite state polling]]]
               run-dir = /path/to/top/level/cylc/run-directory

If the remote task has a different cycling sequence, just arrange for the
local polling task to be on the same sequence as the remote task that it
represents. For instance, if local task ``cat`` cycles 6-hourly at
``0,6,12,18`` but needs to trigger off a remote task ``dog``
at ``3,9,15,21``:

.. code-block:: cylc

   [scheduling]
       [[graph]]
           T03,T09,T15,T21 = "my-dog<other.suite::dog>"
           T00,T06,T12,T18 = "my-dog[-PT3H] => cat"

For suite-state polling, the cycle point is automatically converted to the
cycle point format of the target suite.

The remote suite does not have to be running when polling commences because the
command interrogates the suite run database, not the :term:`scheduler`.

.. note::

   The graph syntax for suite polling tasks cannot be combined with
   cycle point offsets, family triggers, or parameterized task notation.
   This does not present a problem because suite polling tasks can be put on
   the same cycling sequence as the remote-suite target task (as recommended
   above), and there is no point in having multiple tasks (family members or
   parameterized tasks) performing the same polling operation. Task state
   triggers can be used with suite polling, e.g. to trigger another task if
   polling fails after 10 tries at 10 second intervals:

   .. code-block:: cylc

      [scheduling]
          [[graph]]
              R1 = "poller<other-suite::foo:succeed>:fail => another-task"
      [runtime]
          [[my-foo]]
              [[[suite state polling]]]
                  max-polls = 10
                  interval = PT10S


.. _Suite Server Logs:

Suite Server Logs
-----------------

Each suite maintains its own log of time-stamped events in the
:term:`suite log directory` (``$HOME/cylc-run/SUITE-NAME/log/suite/``).

The information logged here includes:

- Event timestamps, at the start of each line
- Suite server host, port and process ID
- Suite initial and final cycle points
- Suite start type (i.e. cold start, warn start, restart)
- Task events (task started, succeeded, failed, etc.)
- Suite stalled warnings.
- Client commands (e.g. ``cylc hold``)
- Job IDs.
- Information relating to the remote file installation, contained in a
  separate log file, the ``file-installation-log``.

.. note::

   Suite log files are primarily intended for human eyes. If you need
   to have an external system to monitor suite events automatically,
   interrogate the sqlite *suite run database*
   (see :ref:`Suite Run Databases`) rather than parse the log files.


.. _Suite Run Databases:

Suite Run Databases
-------------------

Suite server programs maintain two ``sqlite`` databases to record
restart checkpoints and various other aspects of run history:

.. code-block:: console

   $HOME/cylc-run/SUITE-NAME/log/db  # public suite DB
   $HOME/cylc-run/SUITE-NAME/.service/db  # private suite DB

The private DB is for use only by the :term:`scheduler`. The identical
public DB is provided for use by external commands such as
``cylc suite-state``, ``cylc ls-checkpoints``, and
``cylc report-timings``. If the public DB gets locked for too long by
an external reader, the :term:`scheduler` will eventually delete it and
replace it with a new copy of the private DB, to ensure that both correctly
reflect the suite state.

You can interrogate the public DB with the ``sqlite3`` command line tool,
the ``sqlite3`` module in the Python standard library, or any other
sqlite interface.

.. code-block:: console

   $ sqlite3 ~/cylc-run/foo/log/db << _END_
   > .headers on
   > select * from task_events where name is "foo";
   > _END_
   name|cycle|time|submit_num|event|message
   foo|1|2017-03-12T11:06:09Z|1|submitted|
   foo|1|2017-03-12T11:06:09Z|1|output completed|started
   foo|1|2017-03-12T11:06:09Z|1|started|
   foo|1|2017-03-12T11:06:19Z|1|output completed|succeeded
   foo|1|2017-03-12T11:06:19Z|1|succeeded|

The diagram shown below contains the database tables, their columns,
and how the tables are related to each other. For more details on how
to interpret the diagram, refer to the
`Entity–relationship model Wikipedia article <https://en.wikipedia.org/wiki/Entity%E2%80%93relationship_model>`_.

.. cylc-db-graph::
   :align: center


.. _Disaster Recovery:

Disaster Recovery
-----------------

If a suite run directory gets deleted or corrupted, the options for recovery
are:

- restore the run directory from back-up, and restart the suite
- re-install from source, and warm start from the beginning of the
  current cycle point

A warm start (see :ref:`Warm Start`) does not need a suite state
checkpoint, but it wipes out prior run history, and it could re-run
a significant number of tasks that had already completed.

To restart the suite, the critical Cylc files that must be restored are:

.. code-block:: sub

   # On the suite host:
   ~/cylc-run/SUITE-NAME/
       flow.cylc   # live suite configuration (located here in Rose suites)
       log/db  # public suite DB (can just be a copy of the private DB)
       log/rose-suite-run.conf  # (needed to restart a Rose suite)
       .service/db  # private suite DB
       .service/source -> PATH-TO-SUITE-DIR  # symlink to live suite directory

   # On job hosts (if no shared filesystem):
   ~/cylc-run/SUITE-NAME/
       log/job/CYCLE-POINT/TASK-NAME/SUBMIT-NUM/job.status

.. note::

   This discussion does not address restoration of files generated and
   consumed by task jobs at run time. How suite data is stored and recovered
   in your environment is a matter of suite and system design.

In short, you can simply restore the suite :term:`service directory`, the
:term:`suite log directory`, and the :cylc:conf:`flow.cylc` file that is the
target of the symlink in the service directory. The :term:`service directory`
and :term:`suite log directory` will come with extra files that aren't strictly
needed for a restart, but that doesn't matter - although depending on your log
housekeeping the ``log/job`` directory could be huge, so you might want to be
selective about that. (Also in a Rose suite, the ``flow.cylc`` file does not
need to be restored if you restart with ``rose suite-run`` - which re-installs
suite source files to the run directory).

The public DB is not strictly required for a restart - the :term:`scheduler`
will recreate it if need be - but it is required by
``cylc ls-checkpoints`` if you need to identify the right restart
checkpoint.

The job status files are only needed if the restart suite state checkpoint
contains active tasks that need to be polled to determine what happened to them
while the suite was down. Without them, polling will fail and those tasks will
need to be manually set to the correct state.

.. warning::

   It is not safe to copy or rsync a potentially-active sqlite DB - the copy
   might end up corrupted. It is best to stop the suite before copying
   a DB, or else write a back-up utility using the
   `official sqlite backup API <https://www.sqlite.org/backup.html>`_.


.. _auto-stop-restart:

Auto Stop-Restart
-----------------

Cylc has the ability to automatically stop suites running on a particular host
and optionally, restart them on a different host.
This is useful if a host needs to be taken off-line e.g. for
scheduled maintenance.

See :py:mod:`cylc.flow.main_loop.auto_restart` for details.


.. _Alternate Run Directories:

Alternate Run Directories
-------------------------

The ``cylc register`` command normally creates a run directory at
the standard location ``~/cylc-run/<WORKFLOW-NAME>/``. With the ``--run-dir``
option it can create the run directory at some other location, with a symlink
from ``~/cylc-run/<WORKFLOW-NAME>`` to allow access via the standard file path.

This may be useful for quick-running :ref:`Sub-Workflows` that generate large
numbers of files - you could put their run directories on fast local disk or
RAM disk, for performance and housekeeping reasons.


.. _Sub-Workflows:

Sub-Workflows
-------------

A single Cylc workflow can configure multiple cycling sequences in the graph,
but cycles can't be nested. If you need *cycles within cycles* - e.g. to
iterate over many files generated by each run of a cycling task - current
options are:

- parameterize the sub-cycles

  - this is easy but it makes more tasks-per-cycle, which is the primary
    determinant of workflow size and server program efficiency

- run a separate cycling workflow over the sub-cycle, inside a main-workflow
  task, for each main-workflow cycle point - i.e. use **sub-workflows**

  - this is very efficient, but monitoring and run-directory housekeeping may
    be more difficult because it creates multiple workflows and run directories

Sub-workflows must be started with ``--no-detach`` so that the containing task
does not finish until the sub-workflow does, and they should be non-cycling
or have a ``final cycle point`` so they don't keep on running indefinitely.

Sub-workflow names should normally incorporate the main-workflow cycle point (use
``$CYLC_TASK_CYCLE_POINT`` in the ``cylc run`` command line to start the
sub-workflow), so that successive sub-workflows can run concurrently if necessary and
do not compete for the same run directory. This will generate a new sub-workflow
run directory for every main-workflow cycle point, so you may want to put
housekeeping tasks in the main workflow to extract the useful products from each
sub-workflow run and then delete the sub-workflow run directory.

For quick-running sub-workflows that generate large numbers of files, consider
using :ref:`Alternate Run Directories` for better performance and easier housekeeping.

.. [3] Late notification of clock-triggered tasks is not very useful in
       any case because they typically do not depend on other tasks, and as
       such they can often trigger on time even if the suite is delayed to
       the point that downstream tasks are late due to their dependence on
       previous-cycle tasks that are delayed.
