.. _User Guide Runtime:

Task Configuration
==================

.. tutorial:: Runtime Tutorial <tutorial-runtime>

The :cylc:conf:`[runtime]` section of the :cylc:conf:`flow.cylc` file
defines what job each :term:`task` should run, and where and how to
submit each one to run.

It is an inheritance hierarchy that allows common settings to be factored
out and defined once in task :term:`families <family>` (duplication
of configuration is a maintenance risk in a complex workflow).


.. _namespace-names:

Task and Family Names
---------------------

Task and family names must match in the graph and runtime sections of the
workflow config file. They do not need to match the names of the external
applications wrapped by the tasks.

.. autoclass:: cylc.flow.unicode_rules.TaskNameValidator

.. note::

   At runtime, tasks can access their own workflow task name as
   ``$CYLC_TASK_NAME`` in the job environment :ref:`job environment
   <TaskExecutionEnvironment>` if needed.


The following runtime configuration defines one family called ``FAM`` and two
member tasks ``fm1`` and ``fm2`` that inherit settings from it. Members can
also override inherited settings and define their own private settings.

.. code-block:: cylc

   [runtime]
       [[FAM]]  # <-- a family
           #...  settings for all FAM members

       [[fm1]]  # <-- task
           inherit = FAM
           #...  fm1-specific settings

       [[fm2]]  # <-- a task
           inherit = FAM
           #...  fm2-specific settings

Note that families are not nested in terms of the file sub-heading structure. A
runtime subsection defines a family if others inherit from it, otherwise
it defines a task.


The Root Family
---------------

All tasks inherit implicitly from a family called ``root`` that can provide
default settings for all tasks in the workflow (non-root families require an
explicit ``inherit`` statement).

For example, if all tasks are to run on the same platform, that could
can be specified once for all tasks under ``root``:

.. code-block:: cylc

   [runtime]
       [[root]]
           # all tasks run on hpc1 (unless they override this setting)
           platform = hpc1



.. _MultiTaskDef:

Defining Multiple Tasks or Families at Once
-------------------------------------------

Runtime sub-section headings can be a comma-separated list of task or family
names, in which case the settings below it apply to each list member.

Here a group of three related tasks all run the same script on the same
:term:`platform`, but pass their own names to it on the command line:

.. code-block:: cylc

   [runtime]
       [[ENSEMBLE]]
           platform = hpc1
           script = "run-model.sh $CYLC_TASK_NAME"

       [[m1, m2, m3]]
           inherit = ENSEMBLE

       [[m1]]
           #...  m1-specific settings

Particular tasks (such as ``m1`` above) can still be singled out to add
task-specific settings.


.. note::

   :ref:`Task parameters <User Guide Param>` or template processing (see
   :ref:`User Guide Jinja2` and :ref:`User Guide EmPy`) can be used to
   programmatically generate family members and associated dependencies.


Families of Families
--------------------

Families can inherit from other families, to any depth.

.. code-block:: cylc

   [runtime]
       [[HPC1]]
           platform = hpc1

       [[BIG-HPC1]]
           inherit = HPC1
           #...  add in high memory batch system directives

       [[model]]  # a big task that runs on hpc1
           inherit = BIG-HPC1

If the same item is defined (and redefined) at several levels in the family
tree, the highest level (closest to the task) takes precedence.


Inheriting from Multiple Parents
--------------------------------

Sometimes a multi-level single-parent tree is not sufficient to avoid all
duplication of settings. Fortunately tasks can inherit from multiple parents at
once [1]_:

.. code-block:: cylc

   [runtime]
       [[HPC1]]
           platform = hpc1

       [[BIG]]  # high memory batch system directives
           #...

       [[model]]  # a big task that runs on hpc1
           inherit = BIG, HPC1



.. tip::

  Use ``cylc config`` to check exactly what settings a task or family ends up
  with after inheritance processing:

  .. code-block:: console

     $ cylc config --item "[runtime][model]environment" <workflow-id>


First-parent Family Hierarchy for Visualization
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Tasks can be collapsed into first-parent families in the Cylc GUI, so first
parents should reflect the logical purpose of a task where possible, rather
than (say) shared technical settings:

.. code-block:: cylc

   [runtime]
       [[HPC]]
           # technical platform settings

       [[MODEL]]
           # atmospheric model tasks

       [[atmos]]
           inherit = MODEL, HPC  # (not HPC, MODEL)


If this is not what you want, given that the primary purpose of the family
hierarchy is inheritance of runtime settings, a dummy first parent ``None`` can
be used to disable the visualization usage without affecting inheritance:

.. code-block:: cylc

   [runtime]
       [[BAR]]
           #...
       [[foo]]
           # inherit from BAR but stay under root for visualization
           inherit = None, BAR




.. _TaskExecutionEnvironment:

Job Environment
---------------

:term:`Job scripts <job script>` export various environment variables before
running ``script`` blocks (see :ref:`TaskJobSubmission`).

Scheduler-defined variables appear first to identify the workflow, the task,
and log directory locations. These are followed by user-defined variables from
:cylc:conf:`[runtime][<namespace>][environment]`. Order of variable definition
is preserved so that new variable assignments can reference previous ones.

.. note::

   Task environment variables are evaluated at runtime, by jobs, on the
   job platform. So ``$HOME`` in a task environment, for instance, evaluates at
   runtime to the home directory on the job platform, not on the scheduler
   platform.


In this example the task ``foo`` ends up with ``SHAPE=circle``, ``COLOR=blue``,
and ``TEXTURE=rough`` in its environment:

.. code-block:: cylc

   [runtime]
       [[root]]
           [[[environment]]]
               COLOR = red
               SHAPE = circle
       [[foo]]
           [[[environment]]]
               COLOR = blue  # root override
               TEXTURE = rough # new variable

Job access to Cylc itself is configured first so that variable
assignment expressions (as well as scripting) can use Cylc commands:

.. code-block:: cylc

   [runtime]
       [[foo]]
           [[[environment]]]
               REFERENCE_TIME = $(cylc cyclepoint --offset-hours=6)


Overriding Inherited Environment Variables
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. warning::

   If you override an inherited task environment variable the parent config
   item gets *replaced* before it is ever used to define the shell variable in
   the :term:`job script`. Consequently the job cannot see the parent value as
   well as the task value:

.. code-block:: cylc

   [runtime]
       [[FOO]]
           [[[environment]]]
               COLOR = red
       [[bar]]
           inherit = FOO
           [[[environment]]]
               tmp = $COLOR  # !! ERROR: $COLOR is undefined here
               COLOR = dark-$tmp  # !! as this overrides COLOR in FOO.

The compressed variant of this, ``COLOR = dark-$COLOR``, is also an error for
the same reason. To achieve the desired result, use a different name for the
parent variable:

.. code-block:: cylc

   [runtime]
       [[FOO]]
           [[[environment]]]
               FOO_COLOR = red
       [[bar]]
           inherit = FOO
           [[[environment]]]
               COLOR = dark-$FOO_COLOR  # OK


.. _Task Job Script Variables:

Job Script Variables
^^^^^^^^^^^^^^^^^^^^

These variables provided by the :term:`scheduler` are available to
:term:`job scripts <job script>`:

.. literalinclude:: ../../reference/job-script-vars/var-list.txt
   :language: sub

Some global shell variables are also defined in the job script, but not
exported to subshells:

.. code-block:: sub

   CYLC_FAIL_SIGNALS               # List of signals trapped by the error trap
   CYLC_VACATION_SIGNALS           # List of signals trapped by the vacation trap
   CYLC_TASK_MESSAGE_STARTED_PID   # PID of "cylc message" job started" command
   CYLC_TASK_WORK_DIR_BASE         # Alternate task work directory,
                                   #   relative to the workflow work directory


.. _WorkflowShareDirectories:

Workflow Share Directories
^^^^^^^^^^^^^^^^^^^^^^^^^^

The workflow :term:`share directory` is created automatically under the
workflow run directory as a convenient shared space for tasks. The location is
available to tasks as ``$CYLC_WORKFLOW_SHARE_DIR``. In a cycling workflow,
output files are typically held in cycle point sub-directories of this.

The top level share directory location can be changed, e.g. to a large data
area, by global config settings under :cylc:conf:`global.cylc[install][symlink dirs]`.

If your workflow creates or installs executables or Python libraries
as it is running, these can be placed in:

* ``share/bin`` - for executables.
* ``share/lib/python`` - for Python modules.

These folders are automatically added to ``PATH`` and ``PYTHONPATH`` so they can be
used by jobs in the same way as the
:ref:`top level "bin/" and "lib/python/" directories <WorkflowDefinitionDirectories>`.

.. note::

   Cylc will not create these folders.

.. important::

  These locations will be placed first in the executable and Python module
  search paths, before those in the parent run directory .


Task Work Directories
^^^^^^^^^^^^^^^^^^^^^

Job scripts are executed from within :term:`work directories <work
directory>` created automatically under the workflow run directory. A task can
access its own work directory via ``$CYLC_TASK_WORK_DIR`` (or simply ``$PWD``
if it does not change to another location at runtime). By default the location
contains task name and cycle point, to provide a unique workspace for every
instance of every task.

The top level work directory location can be changed, e.g. to a large data
area, by global config settings under :cylc:conf:`global.cylc[install][symlink dirs]`.


.. _RunningTasksOnARemoteHost:

Remote Task Hosting
-------------------

Job :term:`platforms <platform>` are defined in ``global.cylc[platforms]``.

If a task declares a different platform to that where the scheduler is running,
Cylc uses non-interactive SSH to submit the job to the platform :term:`job
runner` on one of the platform hosts. Workflow source files will be installed
on the platform, via the associated ``global.cylc[install targets]``, just
before the first job is submitted to run there.

.. code-block:: cylc

   [runtime]
      [[foo]]
          platform = orca

For this to work:

- Non-interactive SSH is required from the :term:`scheduler` host
  to the platform hosts
- Cylc must be installed on the hosts of the destination platform

  - If polling task communication is used, there is no other requirement
  - If SSH task communication is configured, non-interactive SSH is required
    from the job platform to the scheduler platform
  - If TCP (default) task communication is configured, the task platform
    should have access to the Cylc ports on the scheduler host

Platforms, like other runtime settings, can be declared globally in the root
family, or in other families, or for individual tasks.

.. note::

   The platform known as ``localhost`` is the platform where the scheduler
   is running, in many cases a dedicated server and *not* your desktop.

Internal Platform and Host Selection
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The :cylc:conf:`[runtime][<namespace>]platform` item points to either a
:cylc:conf:`platform <global.cylc[platforms][<platform name>]>` or a
:cylc:conf:`platform group <global.cylc[platform groups][<group>]>`.

:term:`Cylc platforms <platform>` allow you to configure compute platforms
you wish Cylc to run jobs on.

:term:`Platform groups <platform group>` allow you to group together platforms
any of which would be suitable for a given job.
Platform groups can improve robustness by allowing jobs to be submitted on
any platform in the group, as well as providing an interface for
:cylc:conf:`basic load balancing
<global.cylc[platform groups][<group>][selection]method>`.

:term:`Platforms <platform>` are selected from a :term:`platform group` once,
when a job is submitted.

Hosts within a :term:`platform` are re-selected each time the scheduler
needs to communicate with a job.

.. seealso::

   :ref:`AdminGuide.PlatformConfigs`: For details of how Platforms and
   Platform Groups are set up and in-depth examples.

External Platform Selection Scripts
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. deprecated:: 8.0.0

   Cylc 8 can select hosts from a group of suitable hosts listed in the
   platform config, so in many cases this logic should no longer be necessary.

Instead of hardwiring platform names into the workflow configuration you can
give a command that prints a platform name, or an environment variable, as the
value of :cylc:conf:`[runtime][<namespace>]platform`.

For example:

.. code-block:: cylc
   :caption: flow.cylc

   [runtime]
       [[mytask]]
           platform = $(script-which-returns-a-platform-name)

Job hosts are always selected dynamically, for the chosen platform or
platform group.

.. caution::

   If ``$(script-which-returns-a-platform-name)`` returns a non-zero exit
   code then the scheduler will assign the
   :ref:`submit-failed <task-job-states>` state to this :term:`job`.
   If you have submit retries set up for the job, the scheduler will retry
   running your platform selection script in the same was is it would for
   any other submission failure.

Remote Job Log Directories
^^^^^^^^^^^^^^^^^^^^^^^^^^

Job stdout and stderr streams are written to :term:`log files <job log>`
under the workflow :term:`run directory` (see :ref:`WhitherStdoutAndStderr`).
For remote tasks the same directory is used, on the job host.


.. _ImplicitTasks:

Implicit Tasks
--------------

An implicit task is one that appears in the graph but is not defined under
:cylc:conf:`flow.cylc[runtime]`.

Depending on the value of :cylc:conf:`flow.cylc[scheduler]allow implicit tasks`,
Cylc can automatically create default task definitions for these, to submit
local dummy jobs that just return the standard job status messages.

Implicit tasks can be used to mock up functional workflows very quickly. A
default ``script`` can be added to the root family, e.g. to slow job execution
down a little. Here is a complete workflow definition using implicit tasks:

.. code-block:: cylc

   [scheduler]
       allow implicit tasks = True
   [scheduling]
       [[graph]]
           R1 = "prep => run-a & run-b => done"
   [runtime]
       [[root]]
           script = "sleep 10"


.. warning::
   Implicit tasks are somewhat dangerous because they can easily be created by
   mistake: misspelling a task's name divorces it from its ``runtime`` definition.

For this reason implicit tasks are not allowed by default, and if used they
should be turned off once the real task definitions are complete.

You can get the convenience without the danger with a little more effort, by
adding empty runtime placeholders instead of allowing implicit tasks:

.. code-block:: cylc

   [scheduling]
       [[graph]]
           R1 = "prep => run-a & run-b => done"
   [runtime]
       [[root]]
           script = "sleep 10"
       [[prep]]
       [[run-a, run-b]]
       [[done]]


.. _TaskRetries:

Task Retry On Failure
---------------------

.. seealso::

   :cylc:conf:`[runtime][<namespace>]execution retry delays`.

Tasks can have a list of :term:`ISO8601 durations <ISO8601 duration>` as retry
intervals. If the job fails the task will return to the ``waiting`` state
with a clock-trigger configured with the next retry delay.


.. note::

   Tasks only enter the ``submit-failed`` state if job submission fails with no
   retries left. Otherwise they return to the waiting state, to wait on the
   next try.

   Tasks only enter the ``failed`` state if job execution fails with no retries
   left. Otherwise they return to the waiting state, to wait on the next try.



In the following example, tasks ``bad`` and ``flaky`` each have 3 retries
configured, with a 10 second delay between. On the final try, ``bad`` fails
again and goes to the ``failed`` state, while ``flaky`` succeeds and triggers
task ``whizz`` downstream. The scheduler will then stall with
``bad`` retained as an incomplete task.

.. code-block:: cylc

   [scheduling]
       [[graph]]
           R1 = """
               bad => cheese
               flaky => whizz
            """
   [runtime]
       [[bad]]
           # retry 3 times then fail
           script = """
               sleep 10
               false
           """
           execution retry delays = 3*PT10S
       [[flaky]]
           # retry 3 times then succeed
           script = """
               sleep 10
               test $CYLC_TASK_TRY_NUMBER -gt 3
           """
           execution retry delays = 3*PT10S
       [[cheese, whizz]]
           script = "sleep 10"


.. _EventHandling:

Event Handling
--------------

.. seealso::

  * Task events :cylc:conf:`[runtime][<namespace>][events]`
  * Workflow events :cylc:conf:`[scheduler][events]`

.. cylc-scope:: flow.cylc[runtime][<namespace>]

Custom *event handler* scripts can be called when certain workflow and task
events occur. Event handlers can be used to send a message, raise an alarm, or
whatever you like. They can even call ``cylc`` commands to intervene in the
workflow.

.. note::

   Task event handlers are called by the :term:`scheduler`, not by the task
   jobs that generate the events - so they do not see the job environment.

Event handlers can be stored in the workflow ``bin`` directory, or anywhere in
``$PATH`` in the :term:`scheduler` environment.

They should return quickly to avoid tying up the scheduler process pool -
see :ref:`Managing External Command Execution`.


.. cylc-scope::

Event-Specific Handlers
^^^^^^^^^^^^^^^^^^^^^^^

Event-specific handlers are configured by ``<event> handlers``
under :cylc:conf:`[runtime][<namespace>][events]`, where ``<event>``
can be:

.. |br| raw:: html

     <br>


.. table::

   =========================================  ================================
   Event                                      Description
   =========================================  ================================
   submitted                                  job submitted
   submission retry                           job submission failed but will retry later
   submission failed                          job submission failed
   started                                    job started running
   retry                                      job failed but will retry later
   failed                                     job failed
   succeeded                                  job succeeded
   submission timeout                         job timed out in the ``submitted`` state
   execution timeout                          job timed out in the ``running`` state
   warning                                    scheduler received a message of severity WARNING from job
   critical                                   scheduler received a message of severity CRITICAL from job
   custom                                     scheduler received a message of severity CUSTOM from job |br| (note: literally, the word ``CUSTOM``)
   expired                                    task expired and will not submit (too far behind)
   late                                       task running later than expected
   =========================================  ================================

Values should be a list of commands, command lines, or command line templates
(see below) to call if the specified event is triggered.

General Event Handlers
^^^^^^^^^^^^^^^^^^^^^^

Alternatively you can configure ``handler events`` and ``handlers``
under :cylc:conf:`[runtime][<namespace>][events]`, where the former is a list
of events (as above), and the latter a list of commands, command lines, lines
or command line templates (see below) to call if any of the specified events
are triggered.

.. cylc-scope::

.. _task_event_template_variables:

Task Event Template Variables
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. autoenumvalues:: cylc.flow.task_events_mgr.EventData

Examples
^^^^^^^^

The following :cylc:conf:`flow.cylc` snippets illustrate the two (general and
task-specific) ways to configure event handlers:

.. code-block:: cylc

   [runtime]
       [[foo]]
           script = test ${CYLC_TASK_TRY_NUMBER} -eq 2
           execution retry delays = PT0S, PT30S
           [[[events]]]  # event-specific handlers:
               retry handlers = notify-retry.py
               failed handlers = notify-failed.py

.. code-block:: cylc

   [runtime]
       [[foo]]
           script = """
               test ${CYLC_TASK_TRY_NUMBER} -eq 2
               cylc message -- "${CYLC_WORKFLOW_ID}" "${CYLC_TASK_JOB}" 'oopsy daisy'
           """
           execution retry delays = PT0S, PT30S
           [[[events]]]  # general handlers:
               handlers = notify-events.py
               # Note: task output name can be used as an event in this method
               handler events = retry, failed, oops
           [[[outputs]]]
               oops = oopsy daisy

Built-in Email Event Handler
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

To send an email on task events, configure relevant tasks with a list of events
to handle by email. Custom task output names can also be used as event names,
in which case the event triggers when the output message is received.

E.g. to send an email on task failed, retry, and a custom message event:

.. code-block:: cylc

   [runtime]
       [[foo]]
           script = """
               test ${CYLC_TASK_TRY_NUMBER} -eq 3
               cylc message -- "${CYLC_WORKFLOW_ID}" "${CYLC_TASK_JOB}" 'oopsy daisy'
           """
           execution retry delays = PT0S, PT30S
           [[[events]]]
               mail events = failed, retry, oops
           [[[outputs]]]
               oops = oopsy daisy

By default, event emails will be sent to the current user with:

- ``to:`` set as ``$USER``
- ``from:`` set as ``notifications@$(hostname)``
- SMTP server at ``localhost:25``

These can be configured using the settings:

.. cylc-scope:: flow.cylc[runtime][<namespace>]

- :cylc:conf:`[mail]to` (list of email addresses)
- :cylc:conf:`[mail]from`

.. cylc-scope::

The scheduler batches events over a 5 minute interval, by default, to avoid
flooding your Inbox if many events occur in a short time. The batching interval
can be configured with :cylc:conf:`[scheduler][mail]task event batch interval`.


.. _Late Events:

Late Events
^^^^^^^^^^^

.. warning::

  The scheduler can only check for lateness once a task has appeared in its
  active task window. In Cylc 8 this is usually when the task is actually
  ready to run, which severely limits the usefulness of late events as
  currently implemented.

If a real time (clock-triggered) workflow performs fairly consistently from one
cycle to the next, you may want to be notified when certain tasks are running
late with respect the time they normally trigger in each cycle.

Cylc can generate a *late* event if a task has not triggered by a given offset
from its cycle point in real time. For example, if a task ``forecast`` normally
triggers at 30 minutes after cycle point, a late event could be configured like this:

.. code-block:: cylc

   [runtime]
      [[forecast]]
           script = run-model.sh
           [[[events]]]
               late offset = PT40M  # allow a 10 minute delay
               late handlers = my-handler %(message)s

.. warning::
   Late offset intervals are not computed automatically so be careful to update
   them after any workflow change that affects triggering times.

.. [1] The order of precedence for inheritance from multiple parents is
  determined by the `C3 algorithm
  <https://en.wikipedia.org/wiki/C3_linearization>`_ used to find
  the linear method resolution order for multiple inheritance in Python.
