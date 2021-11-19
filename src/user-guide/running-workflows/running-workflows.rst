.. _RunningWorkflows:

Running Workflows
=================

.. TODO - platformise

This chapter currently features a diverse collection of topics related
to running workflows.

.. _WorkflowStartUp:

Workflow Start-Up
-----------------

There are three ways to start a workflow running:

* Cold start: start from scratch
* Warm start: start from scratch, but after the initial cycle point
* Restart: continue from prior workflow state

Once a workflow has been started, it cannot start from scratch again without a
re-install. At this point, it is typically a restart that is needed most
often (but see also :ref:`Reloading The Workflow Configuration At Runtime`).

.. note::

   In Cylc 7 it was posssible to cold/warm start a workflow without having to
   reinstall it. In Cylc 8, you must reinstall the workflow or remove its
   database in order to cold/warm start it.

.. _Cold Start:

Cold Start
^^^^^^^^^^

A cold start is the primary way to run a workflow for the first time:

.. code-block:: console

   $ cylc play WORKFLOW

The initial cycle point may be specified on the command line or in the :cylc:conf:`flow.cylc`
file. The scheduler starts by loading the first instance of each task at the
workflow initial cycle point, or at the next valid point for the task.

.. _Warm Start:

Warm Start
^^^^^^^^^^

A warm start runs a workflow for the first time, like a cold start,
but from the beginning of a given :term:`start cycle point` that is beyond the
workflow :term:`initial cycle point`. The warm start cycle point must be given
on the command line:

.. code-block:: console

   $ cylc play WORKFLOW --start-cycle-point=CYCLE_POINT

The initial cycle point defined in :cylc:conf:`flow.cylc` is preserved, but
all tasks and dependencies before the start cycle point are ignored.

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

.. image:: ../../img/initial-start-stop-final-cp.svg
   :align: center

* The initial and final cycle points are at the start and end of the graph.
* The start and stop cycle points determine the part of the graph that the scheduler runs.


.. _RestartingWorkflows:

Restart
^^^^^^^

At restart, the :term:`scheduler` initializes its task pool from the previous
state at shutdown. This allows the workflow to carry on exactly as it was just
before being shut down or killed.

.. code-block:: console

   $ cylc play WORKFLOW

Tasks recorded in the "submitted" or "running" states are automatically polled
(see :ref:`Task Job Polling`) at start-up to determine what happened to
them while the workflow was down.


Behaviour of Tasks on Restart
"""""""""""""""""""""""""""""

All tasks are reloaded in exactly their recorded states. Failed tasks are
not automatically resubmitted at restart in case the underlying problem has not
been addressed yet.

Tasks recorded in the submitted or running states are automatically polled on
restart, to see if they are still waiting in a :term:`job runner` queue, still running, or
if they succeeded or failed while the workflow was down. The workflow state will be
updated automatically according to the poll results.

Existing instances of tasks removed from the workflow configuration before restart
are not removed from the task pool automatically, but they will not spawn new
instances. They can be removed manually if necessary,
with ``cylc remove``.

Similarly, instances of new tasks added to the workflow configuration before
restart are not inserted into the task pool automatically, because it is
very difficult in general to automatically determine the cycle point of
the first instance. Instead, the first instance of a new task should be
inserted manually at the right cycle point, with ``cylc insert``.


.. _Reloading The Workflow Configuration At Runtime:

Reloading The Workflow Configuration At Runtime
-----------------------------------------------

The ``cylc reload`` command tells a :term:`scheduler` to reload its
workflow configuration at run time. This is an alternative to shutting a
workflow down and restarting it after making changes.

As for a restart, existing instances of tasks removed from the workflow
configuration before reload are not removed from the task pool
automatically, but they will not spawn new instances. They can be removed
manually if necessary, with ``cylc remove``.

Similarly, instances of new tasks added to the workflow configuration before
reload are not inserted into the pool automatically. The first instance of each
must be inserted manually at the right cycle point, with ``cylc insert``.


Files Created at Workflow Start
-------------------------------

Configuration Logs
^^^^^^^^^^^^^^^^^^

At startup a folder ``log/flow-config`` is created to record the workflow configuration,
with all templating expanded:

- ``flow-processed.cylc`` - A record of the current workflow configuration
  with templating expanded, but without being fully parsed: Duplicate sections
  will not be merged.
- ``<datetime-stamp>-<start/restart/reload>`` - A record of the config at
  the time a workflow was started, restarted or reloaded, parsed by Cylc:
  Duplicate sections will be merged.

.. note::

   These are particularly useful files to look at if you are working with a
   workflow definition containing many template variables as these are filled
   in these files.


.. _The Workflow Contact File:

The Workflow Contact File
^^^^^^^^^^^^^^^^^^^^^^^^^

At start-up, :term:`schedulers <scheduler>` write a :term:`contact file`
``$HOME/cylc-run/WORKFLOW/.service/contact`` that records workflow host,
user, port number, process ID, Cylc version, and other information. Client
commands can read this file, if they have access to it, to find the target
:term:`scheduler`.


.. _Authentication Files:

Authentication Files
^^^^^^^^^^^^^^^^^^^^

Cylc uses `CurveZMQ`_ to ensure that
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
their true state conforms to what is currently recorded by the workflow server
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
timeout; several times on exceeding the job execution time limit; and at workflow
restart any tasks recorded as active are polled
to find out what happened to them while the workflow was down.

Finally, in necessary routine polling can be configured as a way to track job
status on job hosts that do not allow networking routing back to the workflow host
for task messaging by TCP or SSH. See :ref:`Polling To Track Job Status`.


.. _TaskComms:

Tracking Task State
-------------------

Cylc supports three ways of tracking task state on job hosts:

- task-to-workflow messaging via TCP (using ZMQ protocol)
- task-to-workflow messaging via non-interactive SSH to the workflow host, then
  local tcp.
- regular polling by the :term:`scheduler`

These can be configured per platform using
:cylc:conf:`global.cylc[platforms][<platform name>]communication method`.

If your site prohibits TCP and SSH back from job hosts to
workflow hosts, before resorting to the polling method you should
consider installing dedicated Cylc servers or
VMs inside the HPC trust zone (where TCP and SSH should be allowed).

It is also possible to run Cylc :term:`schedulers <scheduler>` on HPC login
nodes, but this is not recommended for load and run duration.

Finally, it has been suggested that *port forwarding* may provide another
solution - this has been investigated and will not be implemented at this time.
Organisations often have port forwarding disabled for security reasons.

.. note::
   It is recommended that you use platform configuration within your workflows
   :cylc:conf:`flow.cylc[runtime][<namespace>]platform`, rather than the
   deprecated ``host`` setting to ensure the intended task communication method
   is applied.

TCP Task Messaging
^^^^^^^^^^^^^^^^^^

Task job wrappers automatically invoke ``cylc message`` to report
progress back to the :term:`scheduler` when they begin executing,
at normal exit (success) and abnormal exit (failure).

By default the messaging occurs via an authenticated, TCP connection to the
:term:`scheduler` using the ZMQ protocol.
This is the preferred task communications method - it is efficient and direct.

Schedulers automatically install workflow :term:`contact information
<contact file>` and credentials on job hosts. Users only need to do this
manually for remote access to workflows on other hosts, or workflows owned by other
users - see :ref:`RemoteControl`.

SSH Task Communication
^^^^^^^^^^^^^^^^^^^^^^
Cylc can be configured to re-invoke task messaging commands on the workflow
host via non-interactive SSH (from job platform to workflow host).

User-invoked client commands have been automatically enabled to support this
method of communication, when
:cylc:conf:`global.cylc[platforms][<platform name>]communication method` is
configured to ``ssh``.

This is less efficient than direct ZMQ protocol messaging, but it may be useful at
sites where the ZMQ ports are blocked but non-interactive SSH is allowed.

.. warning::

   Ensure SSH keys are in place for the remote task platform(s) before enabling
   this feature. Failure to do so, will result in
   ``Host key verification failed`` error.


.. _Polling To Track Job Status:

Polling to Track Job Status
^^^^^^^^^^^^^^^^^^^^^^^^^^^

Schedulers can actively poll task jobs at configurable intervals,
via non-interactive SSH to the job host.

Polling is the least efficient task communications method because task state is
updated only at intervals, not when task events actually occur. However, it
may be needed at sites that do not allow TCP or non-interactive SSH from job
host to workflow host.

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

Schedulers listen on dedicated network ports for
TCP communications from Cylc clients (task jobs and user-invoked commands)

Use ``cylc scan`` to see which workflows are listening on which ports on
scanned hosts.

Cylc generates public-private key pairs on the workflow server and job hosts
which are used for authentication.


.. _RemoteControl:

Remote Control
--------------

Cylc client programs connect to running workflows using information stored in
the :term:`contact file` in the workflow :term:`run directory`.

This means that Cylc can interact with workflows running on another host provided
that they share the filesystem on which the :term:`cylc-run directory`
(``cylc-run``) is located.

If the hosts do not share a filesystem you must use SSH when calling Cylc client
commands.


Task States Explained
---------------------

As a workflow runs, its task proxies may pass through the following states:

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
  automatically held, in effect) until the rest of the workflow catches up
  sufficiently. The amount of runahead allowed is configurable - see
  :ref:`RunaheadLimit`.
- **expired** - will not be submitted to run, due to falling too far
  behind the wall-clock relative to its cycle point -
  see :ref:`ClockExpireTasks`.


.. _Managing External Command Execution:

Managing External Command Execution
-----------------------------------

Job submission commands, event handlers, and job poll and kill commands, are
executed by the :term:`scheduler` in a "pool" of asynchronous
subprocesses, in order to avoid blocking the workflow process. The process pool
is actively managed to limit it to a configurable size, using
:cylc:conf:`global.cylc[scheduler]process pool size`.
Custom event handlers should be lightweight and quick-running because they
will tie up a process pool member until they complete, and the workflow will
appear to stall if the pool is saturated with long-running processes.
However, to guard against rogue commands that hang indefinitely, processes
are killed after a configurable timeout
(:cylc:conf:`global.cylc[scheduler]process pool timeout`).
All process kills are
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


.. _cylc-broadcast:

Cylc Broadcast
--------------

The ``cylc broadcast`` command overrides :cylc:conf:`[runtime]`
settings in a running workflow. This can
be used to communicate information to downstream tasks by broadcasting
environment variables (communication of information from one task to
another normally takes place via the filesystem, i.e. the input/output
file relationships embodied in inter-task dependencies). Variables (and
any other runtime settings) may be broadcast to all subsequent tasks,
or targeted specifically at a specific task, all subsequent tasks with a
given name, or all tasks with a given cycle point; see broadcast command help
for details.

Broadcast settings targeted at a specific task ID or cycle point expire and
are forgotten as the workflow moves on. Un-targeted variables and those
targeted at a task name persist throughout the workflow run, even across
restarts, unless manually cleared using the broadcast command - and so
should be used sparingly.


.. _SimulationMode:

Simulating Workflow Behaviour
-----------------------------

Several workflow run modes allow you to simulate workflow behaviour quickly without
running the workflow's real jobs - which may be long-running and resource-hungry:

dummy mode
   Runs tasks as background jobs on configured job hosts.

   This simulates scheduling, job host connectivity, and generates all job
   files on workflow and job hosts.
dummy-local mode
   Runs real tasks as background jobs on the workflow host, which allows
   dummy-running workflows from other sites.

   This simulates scheduling and generates all job files on the workflow host.
simulation mode
   Does not run any real tasks.

   This simulates scheduling without generating any job files.

Set the run mode (default ``live``) on the command line:

.. code-block:: console

   $ cylc play --mode=dummy WORKFLOW

You can get specified tasks to fail in these modes, for more flexible workflow
testing. See cylc:conf:`[runtime][<namespace>][simulation]`.


Proportional Simulated Run Length
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

If :cylc:conf:`[runtime][<namespace>]execution time limit` is set, Cylc
divides it by :cylc:conf:`[runtime][<namespace>][simulation]speedup factor` to compute simulated task
run lengths.


Limitations Of Workflow Simulation
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Dummy mode ignores :term:`job runner` settings because Cylc does not know which
job resource directives (requested memory, number of compute nodes, etc.) would
need to be changed for the dummy jobs. If you need to dummy-run jobs on a
job runner manually comment out ``script`` items and modify
directives in your live workflow, or else use a custom live mode test workflow.

.. note::

   The dummy modes ignore all configured task ``script`` items
   including ``init-script``. If your ``init-script`` is required
   to run even blank/empty tasks on a job host, note that host environment
   setup should be done elsewhere.


Restarting Workflows With A Different Run Mode?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The run mode is recorded in the workflow run database files. Cylc will not let
you *restart* a non-live mode workflow in live mode, or vice versa. To
test a live workflow in simulation mode just take a quick copy of it and run the
the copy in simulation mode.


.. _AutoRefTests:

Automated Reference Test Workflows
----------------------------------

Reference tests are finite-duration workflow runs that abort with non-zero
exit status if any of the following conditions occur (by default):

- cylc fails
- any task fails
- the workflow times out (e.g. a task dies without reporting failure)
- a nominated shutdown event handler exits with error status

When a reference test workflow shuts down, it compares task triggering
information (what triggers off what at run time) in the test run workflow
log to that from an earlier reference run, disregarding the timing and
order of events - which can vary according to the external queueing
conditions, runahead limit, and so on.

To prepare a reference log for a workflow, run it with the
``--reference-log`` option, and manually verify the
correctness of the reference run.

To reference test a workflow, just run it (in dummy mode for the most
comprehensive test without running real tasks) with the
``--reference-test`` option.

A battery of automated reference tests is used to test cylc before
posting a new release version. Reference tests can also be used to check that
a cylc upgrade will not break your own complex
workflows - the triggering check will catch any bug that causes a task to
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


.. _Workflow Server Logs:

Workflow Server Logs
--------------------

Each workflow maintains its own log of time-stamped events in the
:term:`workflow log directory` (``$HOME/cylc-run/WORKFLOW-NAME/log/workflow/``).

The information logged here includes:

- Event timestamps, at the start of each line
- Workflow server host, port and process ID
- Workflow initial and final cycle points
- Workflow start type (i.e. cold start, warn start, restart)
- Task events (task started, succeeded, failed, etc.)
- Workflow stalled warnings.
- Client commands (e.g. ``cylc hold``)
- Job IDs.
- Information relating to the remote file installation, contained in a
  separate log file, the ``file-installation-log``.

.. note::

   Workflow log files are primarily intended for human eyes. If you need
   to have an external system to monitor workflow events automatically,
   interrogate the sqlite *workflow run database*
   (see :ref:`Workflow Run Databases`) rather than parse the log files.


.. _Workflow Run Databases:

Workflow Run Databases
----------------------

Schedulers maintain two ``sqlite`` databases to record
information on run history:

.. code-block:: console

   $HOME/cylc-run/WORKFLOW-NAME/log/db  # public workflow DB
   $HOME/cylc-run/WORKFLOW-NAME/.service/db  # private workflow DB

The private DB is for use only by the :term:`scheduler`. The identical
public DB is provided for use by external commands such as
``cylc workflow-state``, and ``cylc report-timings``.
If the public DB gets locked for too long by
an external reader, the :term:`scheduler` will eventually delete it and
replace it with a new copy of the private DB, to ensure that both correctly
reflect the workflow state.

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


.. _auto-stop-restart:

Auto Stop-Restart
-----------------

Cylc has the ability to automatically stop workflows running on a particular host
and optionally, restart them on a different host.
This is useful if a host needs to be taken off-line e.g. for
scheduled maintenance.

See :py:mod:`cylc.flow.main_loop.auto_restart` for details.


.. _Alternate Run Directories:

Alternate Run Directories
-------------------------

The ``cylc install`` command normally creates a worflow run directory at
the standard location ``~/cylc-run/<WORKFLOW-NAME>/``. Configure the run
directory in the ``global.cylc`` file: :cylc:conf:`global.cylc[install][symlink dirs]`.

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
    determinant of workflow size and scheduler efficiency (this has a much
    smaller impact from Cylc 8 on, however).

- run a separate cycling workflow over the sub-cycle, inside a main-workflow
  task, for each main-workflow cycle point - i.e. use **sub-workflows**

  - this is very efficient, but monitoring and run-directory housekeeping may
    be more difficult because it creates multiple workflows and run directories

Sub-workflows must be started with ``--no-detach`` so that the containing task
does not finish until the sub-workflow does, and they should be non-cycling
or have a ``final cycle point`` so they don't keep on running indefinitely.

Sub-workflow names should normally incorporate the main-workflow cycle point (use
``$CYLC_TASK_CYCLE_POINT`` in the ``cylc play`` command line to start the
sub-workflow), so that successive sub-workflows can run concurrently if necessary and
do not compete for the same workflow run directory. This will generate a new
sub-workflow run directory for every main-workflow cycle point, so you may want to
put housekeeping tasks in the main workflow to extract the useful products from each
sub-workflow run and then delete the sub-workflow run directory.

For quick-running sub-workflows that generate large numbers of files, consider
using :ref:`Alternate Run Directories` for better performance and easier housekeeping.


