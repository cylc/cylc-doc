.. _User Guide Runtime:

Runtime - Task Configuration
============================

.. tutorial:: Runtime Tutorial <tutorial-runtime>

The :cylc:conf:`flow.cylc` file's :cylc:conf:`[runtime]` section configures
what each should run, and where and how to run it. It is a multiple inheritance
hierarchy that allows all common settings to be factored out into task families
and defined once only (duplication of configuraiton is a maintenance risk in a
complex workflow).

.. _namespace-names:

Task and Family Names
---------------------

Task and family names must match in the graph and runtime sections of the
workflow config file. They do not need to match the names of the external
applications wrapped by the tasks.

.. autoclass:: cylc.flow.unicode_rules.TaskNameValidator

.. note::

   At runtime, task jobs can access their own workflow task name as
   ``$CYLC_TASK_NAME`` the job environment :ref:`job environment
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

For example, if all task jobs are to run on the same job platform, that could
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

Specific tasks (such as ``m1`` above) can still be singled out to add
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

If an item is defined at several levels in the family tree the highest level
(closest to the task) takes precedence.


Inheriting from Multiple Parents
--------------------------------

Sometimes a multi-level single-parent tree is not sufficient to avoid all
duplication of settings, however you can inherit from multiple parents
at once [1]_:

.. code-block:: cylc

   [runtime]
       [[HPC1]]
           platform = hpc1

       [[BIG]]  # high memory batch system directives
           #...

       [[model]]  # a big task that runs on hpc1
           inherit = BIG, HPC1



.. tip::

  Use ``cylc config`` to check task or family settings after inheritance:

  .. code-block:: console

     $ cylc config --item "[runtime][model]environment" <workflow-name>
     # (prints model's environment as inherited from all parents)


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

Task Job Environment
--------------------

Task job environments (see :cylc:conf:`[runtime][<namespace>][environment]`)
contain workflow and task identity variables provided by the :term:`scheduler`,
and user-defined variables inherited through the runtime tree.

Environment variables are exported in the task job script prior to running the
``script`` items (see :ref:`TaskJobSubmission`). Identity variables are
defined first so that user-defined variables can reference them, and order of
definition is preserved so that new variable assignments can reference
previously-defined ones.

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

Here the task *foo* ends up with ``SHAPE=circle``, ``COLOR=blue``,
and ``TEXTURE=rough`` in its environment.

Task job access to Cylc itself is configured first of all so that variable
assignment expressions (as well as scripting) can make use of Cylc commands:

.. code-block:: cylc

   [runtime]
       [[foo]]
           [[[environment]]]
               REFERENCE_TIME = $(cylc cyclepoint --offset-hours=6)

.. note::

  Task environment variables are evaluated at run time, by task jobs, on the
  job platform. So ``$HOME`` in a task environment, for instance, evaluates at
  run time to the home directory on the job platform, not on the scheduler
  platform.


Overriding Inherited Environment Variables
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. warning::

  If you override a task environment variable that is inherited, the parent
  config item gets *replaced* before it is used to define a shell variable in
  the job script. Consequently the job cannot see the parent value as well as
  the task value:

.. code-block:: cylc

   [runtime]
       [[FOO]]
           [[[environment]]]
               COLOR = red
       [[bar]]
           inherit = FOO
           [[[environment]]]
               tmp = $COLOR        # !! ERROR: $COLOR is undefined here
               COLOR = dark-$tmp   # !! as this overrides COLOR in FOO.

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

Task Job Script Variables
^^^^^^^^^^^^^^^^^^^^^^^^^

These variables provided by the :term:`scheduler` are available to task job scripts:

.. code-block:: sub

   CYLC_DEBUG                         # Debug mode, true or not defined
   CYLC_VERSION                       # Version of cylc installation used

   CYLC_CYCLING_MODE                  # Cycling mode, e.g. gregorian
   ISODATETIMECALENDAR                # Calendar mode for the `isodatetime` command,
                                      #   defined with the value of CYLC_CYCLING_MODE
                                      #     when in any datetime cycling mode

   CYLC_WORKFLOW_FINAL_CYCLE_POINT    # Final cycle point
   CYLC_WORKFLOW_INITIAL_CYCLE_POINT  # Initial cycle point
   CYLC_WORKFLOW_ID                   # Workflow ID - the WORKFLOW_NAME plus the run directory
   CYLC_WORKFLOW_NAME                 # Workflow name
   CYLC_UTC                           # UTC mode, True or False
   CYLC_VERBOSE                       # Verbose mode, True or False
   TZ                                 # Set to "UTC" in UTC mode or not defined

   CYLC_WORKFLOW_RUN_DIR              # Location of the run directory in
                                      # job host, e.g. ~/cylc-run/foo
   CYLC_WORKFLOW_HOST                 # Host running the workflow process
   CYLC_WORKFLOW_OWNER                # User ID running the workflow process

   CYLC_WORKFLOW_SHARE_DIR            # Workflow (or task!) shared directory (see below)
   CYLC_WORKFLOW_UUID                 # Workflow UUID string
   CYLC_WORKFLOW_WORK_DIR             # Workflow work directory (see below)

   CYLC_TASK_JOB                      # Task job identifier expressed as
                                      # CYCLE-POINT/TASK-NAME/SUBMIT-NUMBER
                                      #   e.g. 20110511T1800Z/t1/01
                                      
   CYLC_TASK_CYCLE_POINT              # Cycle point, e.g. 20110511T1800Z
   ISODATETIMEREF                     # Reference time for the `isodatetime` command,
                                      #   defined with the value of CYLC_TASK_CYCLE_POINT
                                      #     when in any datetime cycling mode

   CYLC_TASK_NAME                     # Job's task name, e.g. t1
   CYLC_TASK_SUBMIT_NUMBER            # Job's submit number, e.g. 1,
                                      #   increments with every submit
   CYLC_TASK_TRY_NUMBER               # Number of execution tries, e.g. 1
                                      #   increments with automatic retry-on-fail
   CYLC_TASK_ID                       # Task instance identifier TASK-NAME.CYCLE-POINT
                                      #   e.g. t1.20110511T1800Z
   CYLC_TASK_LOG_DIR                  # Location of the job log directory
                                      #   e.g. ~/cylc-run/foo/log/job/20110511T1800Z/t1/01/
   CYLC_TASK_LOG_ROOT                 # The task job file path
                                      #   e.g. ~/cylc-run/foo/log/job/20110511T1800Z/t1/01/job
   CYLC_TASK_WORK_DIR                 # Location of task work directory (see below)
                                      #   e.g. ~/cylc-run/foo/work/20110511T1800Z/t1
   CYLC_TASK_NAMESPACE_HIERARCHY      # Linearised family namespace of the task,
                                      #   e.g. root postproc t1
   CYLC_TASK_DEPENDENCIES             # List of met dependencies that triggered the task
                                      #   e.g. foo.1 bar.1

   CYLC_TASK_COMMS_METHOD             # Set to "ssh" if communication method is "ssh"
   CYLC_TASK_SSH_LOGIN_SHELL          # With "ssh" communication, if set to "True",
                                      #   use login shell on workflow host

Some global shell variables may be defined in the task job script too, but are
not exported to the environment). These include:

.. code-block:: sub

   CYLC_FAIL_SIGNALS               # List of signals trapped by the error trap
   CYLC_VACATION_SIGNALS           # List of signals trapped by the vacation trap
   CYLC_TASK_MESSAGE_STARTED_PID   # PID of "cylc message" job started" command
   CYLC_TASK_WORK_DIR_BASE         # Alternate task work directory,
                                   #   relative to the workflow work directory


Workflow Share Directories
^^^^^^^^^^^^^^^^^^^^^^^^^^

The workflow :term:`share directory` is created automatically under the
workflow run directory as a convenient shared space for tasks. The location is
available to tasks as ``$CYLC_WORKFLOW_SHARE_DIR``. In a cycling workflow,
output files are typically held in cycle point sub-directories of this.

The top level share directory location can be changed, e.g. to a large data
area, by global config settings under :cylc:conf:`global.cylc[install][symlink dirs]`.


Task Work Directories
^^^^^^^^^^^^^^^^^^^^^

Task job scripts are executed from within :term:`work directories <work
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

If a task declares a different platform to the one where the scheduler is running,
Cylc will use non-interactive SSH to submit the task job using the platform
:term:`job runner` on one of the hosts that comprise the :term:`platform`.
(platforms are defined in ``global.cylc[platforms]``). Workflow source files
will be installed to the platform just before the first job is submitted there.

For example:

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
family, or in other families or in individual tasks.


Dynamic Platform Selection
^^^^^^^^^^^^^^^^^^^^^^^^^^

.. TODO - consider a re-write once dynamic platform selection done

Instead of hardwiring platform names into the workflow configuration you can
specify a shell command that prints a platform name, or an environment
variable that holds a platform name, as the value of the
:cylc:conf:`host config item <[runtime][<namespace>]platform>`.


Remote Task Log Directories
^^^^^^^^^^^^^^^^^^^^^^^^^^^

Task stdout and stderr streams are written to :term:`log files <job log>` in a
workflow-specific sub-directory of the workflow :term:`run directory`, as
explained in :ref:`WhitherStdoutAndStderr`. For remote tasks
the same directory is used, but *on the task host*.
Remote task log directories, like local ones, are created on the fly, if
necessary, during job submission.


.. _ImplicitTasks:

Implicit Tasks
--------------

An :term:`implicit task` appears in the graph but has no matching runtime
configuration section. These tasks (like all tasks) inherit from root.
This can be useful because it allows functional workflows to be mocked up
quickly for test purposes by simply defining the graph. It is somewhat
dangerous, however, because there is no way to distinguish an intentional
implicit task from one caused by typographic error. Misspelling a task name in
the graph results in a new implicit task replacing the intended task in the
affected trigger expression; and misspelling a task name in a runtime
section heading results in the intended task becoming an implicit task
itself (by divorcing it from its intended runtime config section).

You can allow implicit tasks during development of a workflow using
:cylc:conf:`flow.cylc[scheduler]allow implicit tasks`. But, to avoid
the problems mentioned above, any task used in a production/operational
workflow should not be implicit, i.e. it should have an explicit entry in under
the runtime section of ``flow.cylc``, even if the section is empty. This
results in exactly the same task behaviour, via inheritance from root,
but adds a layer of protection against mistakes. Thus, it is recommended to
turn off :cylc:conf:`flow.cylc[scheduler]allow implicit tasks` when the
:cylc:conf:`flow.cylc[runtime]` section has been written.


.. _TaskRetries:

Automatic Task Retry On Failure
-------------------------------

.. seealso::

   cylc:conf:`[runtime][<namespace>]execution retry delays`.

Tasks can be configured with a list of "retry delay" intervals, as
:term:`ISO8601 durations <ISO8601 duration>`. If the task job fails it will go
into the *retrying* state and resubmit after the next configured delay
interval. An example is shown in the workflow listed below under
:ref:`EventHandling`.

If a task with configured retries is *killed* (by ``cylc kill``
it goes to the *held* state so that the operator can decide
whether to release it and continue the retry sequence or to abort the retry
sequence by manually resetting it to the *failed* state.


.. _EventHandling:

Event Handling
--------------

* Task events (e.g. task succeeded/failed) are configured by
  :cylc:conf:`task events <[runtime][<namespace>][events]>`.
* Workflow events (e.g. workflow started/stopped) are configured by
  :cylc:conf:`workflow events <[scheduler][events]>`

.. cylc-scope:: flow.cylc[runtime][<namespace>]

Cylc can call nominated event handlers - to do whatever you like - when certain
workflow or task events occur. This facilitates centralized alerting and automated
handling of critical events. Event handlers can be used to send a message, call
a pager, or whatever; they can even intervene in the operation of their own
workflow using cylc commands.

To send an email, use the built-in setting :cylc:conf:`[events]mail events`
to specify a list of events for which notifications should be sent. (The
name of a registered task output can also be used as an event name in
this case.) E.g. to send an email on (submission) failed and retry:

.. code-block:: cylc

   [runtime]
       [[foo]]
           script = """
               test ${CYLC_TASK_TRY_NUMBER} -eq 3
               cylc message -- "${CYLC_WORKFLOW_ID}" "${CYLC_TASK_JOB}" 'oopsy daisy'
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

By default, a cylc workflow will send you no more than one task event email every
5 minutes - this is to prevent your inbox from being flooded by emails should a
large group of tasks all fail at similar time. This is configured by
:cylc:conf:`[scheduler][mail]task event batch interval`.

Event handlers can be located in the workflow ``bin/`` directory;
otherwise it is up to you to ensure their location is in ``$PATH`` (in
the shell in which the :term:`scheduler` runs). They should require little
resource and return quickly - see :ref:`Managing External Command Execution`.

.. cylc-scope:: flow.cylc[runtime][<namespace>]

Task event handlers can be specified using the
``[events]<event> handler`` settings, where
``<event>`` is one of:

.. TODO - Add link to replaced link of states.

The value of each setting should be a list of command lines or command line
templates (see below).

Alternatively you can use :cylc:conf:`[events]handlers` and
:cylc:conf:`[events]handler events`, where the former is a list of command
lines or command line templates (see below) and the latter is a list of events
for which these commands should be invoked. (The name of a registered task
output can also be used as an event name in this case.)

.. cylc-scope::

Event handler arguments can be constructed from various templates
representing workflow name; task ID, name, cycle point, message, and submit
number name; and any :cylc:conf:`workflow <[meta]>` or
:cylc:conf:`task <[runtime][<namespace>][meta]>` item.
See :cylc:conf:`workflow events <[scheduler][events]>` and
:cylc:conf:`task events <[runtime][<namespace>][events]>` for options.

If no template arguments are supplied the following default command line
will be used:

.. code-block:: none

   <task-event-handler> %(event)s %(workflow)s %(id)s %(message)s

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
               cylc message -- "${CYLC_WORKFLOW_ID}" "${CYLC_TASK_JOB}" 'oopsy daisy'
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

   echo '!!!!!EVENT!!!!!' %(event)s %(workflow)s %(id)s %(message)s


.. _Late Events:

Late Events
^^^^^^^^^^^

You may want to be notified when certain tasks are running late in a real time
production system - i.e. when they have not triggered by *the usual time*.
Tasks of primary interest are not normally clock-triggered however, so their
trigger times are mostly a function of how the workflow runs in its environment,
and even external factors such as contention with other workflows [2]_ .

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
   of. If a workflow gets delayed over many cycles the next tasks coming up
   can be identified as late immediately, and subsequent tasks can be
   identified as late as the workflow progresses to subsequent cycle points,
   until it catches up to the clock.


.. [1] The order of precedence for inheritance from multiple parents
   is determined by the `C3 algorithm
   <https://en.wikipedia.org/wiki/C3_linearization>`_. C3 is
   used to find the linear *method resolution order* for multiple inheritance
   in Python.


.. [2] Late notification of clock-triggered tasks is not very useful in
   any case because they typically do not depend on other tasks, and as
   such they can often trigger on time even if the workflow is delayed to
   the point that downstream tasks are late due to their dependence on
   previous-cycle tasks that are delayed.
