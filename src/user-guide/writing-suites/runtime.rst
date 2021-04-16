.. _User Guide Runtime:

Runtime - Task Configuration
============================

.. tutorial:: Runtime Tutorial <tutorial-runtime>

The :cylc:conf:`[runtime]` section of a suite configuration configures what
to execute (and where and how to execute it) when each task is ready to
run, in a *multiple inheritance hierarchy* of *namespaces* culminating in
individual tasks. This allows all common configuration detail to be
factored out and defined in one place.

Any namespace can configure any or all of the items defined in
:cylc:conf:`flow.cylc`.

Namespaces that do not explicitly inherit from others automatically
inherit from the ``root`` namespace (below).

Nested namespaces define *task families* that can be used in the
graph as convenient shorthand for triggering all member tasks at once,
or for triggering other tasks off all members at once -
see :ref:`FamilyTriggers`.


Namespace Names
---------------

Namespace names may contain letters, digits, underscores, and hyphens.

.. note::

   *Task names need not be hardwired into task implementations*
   because task and suite identity can be extracted portably from the task
   execution environment supplied by the :term:`scheduler`
   (:ref:`TaskExecutionEnvironment`) - then to rename a task you can
   just change its name in the suite configuration.


Root - Runtime Defaults
-----------------------

The ``root`` namespace, at the base of the inheritance hierarchy,
provides default configuration for all tasks in the suite.
Most root items are unset by default, but some have default values
sufficient to allow test suites to be defined by dependency graph alone.
The *script* item, for example, defaults to code that
prints a message then sleeps for between 1 and 15 seconds and
exits. Default values are documented with each item in
:cylc:conf:`flow.cylc`. You can override the defaults or
provide your own defaults by explicitly configuring the root namespace.


.. _MultiTaskDef:

Defining Multiple Namespaces At Once
-------------------------------------

If a namespace section heading is a comma-separated list of names
then the subsequent configuration applies to each list member.
Particular tasks can be singled out at run time using the
``$CYLC_TASK_NAME`` variable.

As an example, consider a suite containing an ensemble of closely
related tasks that each invokes the same script but with a unique
argument that identifies the calling task name:

.. code-block:: cylc

   [runtime]
       [[ENSEMBLE]]
           script = "run-model.sh $CYLC_TASK_NAME"
       [[m1, m2, m3]]
           inherit = ENSEMBLE

For large ensembles template processing can be used to
automatically generate the member names and associated dependencies
(see :ref:`User Guide Jinja2` and :ref:`User Guide EmPy`).


Runtime Inheritance - Single
----------------------------

The following listing of the *inherit.single.one* example suite
illustrates basic runtime inheritance with single parents.

.. literalinclude:: ../../suites/inherit/single/one/flow.cylc
   :language: cylc


Runtime Inheritance - Multiple
------------------------------

If a namespace inherits from multiple parents the linear order of
precedence (which namespace overrides which) is determined by the
so-called *C3 algorithm* used to find the linear *method
resolution order* for class hierarchies in Python and several other
object oriented programming languages. The result of this should be
fairly obvious for typical use of multiple inheritance in Cylc suites,
but for detailed documentation of how the algorithm works refer to the
`official Python documentation
<https://www.python.org/download/releases/2.3/mro/>`_.

The *inherit.multi.one* example suite, listed here, makes use of
multiple inheritance:

.. literalinclude:: ../../suites/inherit/multi/one/flow.cylc
   :language: cylc

``cylc config`` provides an easy way to check the result of
inheritance in a suite. You can extract specific items, e.g.:

.. code-block:: console

   $ cylc config --item '[runtime][var_p2]script' inherit.multi.one
   echo "RUN: run-var.sh"

or use the ``--sparse`` option to print entire namespaces
without obscuring the result with the dense runtime structure obtained
from the root namespace:

.. code-block:: console

   $ cylc config --sparse --item '[runtime]ops_s1' inherit.multi.one
   script = echo "RUN: run-ops.sh"
   inherit = ['OPS', 'SERIAL']
   [directives]
      job_type = serial

Suite Visualization And Multiple Inheritance
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The first parent inherited by a namespace is also used as the
collapsible family group when visualizing the suite. If this is not what
you want, you can demote the first parent for visualization purposes,
without affecting the order of inheritance of runtime properties:

.. code-block:: cylc

   [runtime]
       [[BAR]]
           # ...
       [[foo]]
           # inherit properties from BAR, but stay under root for visualization:
           inherit = None, BAR


How Runtime Inheritance Works
-----------------------------

The linear precedence order of ancestors is computed for each namespace
using the C3 algorithm. Then any runtime items that are explicitly
configured in the suite configuration are "inherited" up the linearized
hierarchy for each task, starting at the root namespace: if a particular
item is defined at multiple levels in the hierarchy, the level nearest
the final task namespace takes precedence. Finally, root namespace
defaults are applied for every item that has not been configured in the
inheritance process (this is more efficient than carrying the full dense
namespace structure through from root from the beginning).


.. _TaskExecutionEnvironment:

Task Execution Environment
--------------------------

The task execution environment contains suite and task identity variables
provided by the :term:`scheduler`, and user-defined environment variables.
The environment is explicitly exported (by the task job script) prior to
executing the task ``script`` (see :ref:`TaskJobSubmission`).

Suite and task identity are exported first, so that user-defined
variables can refer to them. Order of definition is preserved throughout
so that variable assignment expressions can safely refer to previously
defined variables.

Additionally, access to Cylc itself is configured prior to the user-defined
environment, so that variable assignment expressions can make use of
Cylc utility commands:

.. code-block:: cylc

   [runtime]
       [[foo]]
           [[[environment]]]
               REFERENCE_TIME = $( cylc util cycletime --offset-hours=6 )


User Environment Variables
^^^^^^^^^^^^^^^^^^^^^^^^^^

A task's user-defined environment results from its inherited
:cylc:conf:`[runtime][<namespace>][environment]` section.

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

This results in a task *foo* with ``SHAPE=circle``, ``COLOR=blue``,
and ``TEXTURE=rough`` in its environment.


Overriding Environment Variables
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

When you override inherited namespace items the original parent
item definition is *replaced* by the new definition. This applies to
all items including those in the environment sub-sections which,
strictly speaking, are not "environment variables" until they are
written, post inheritance processing, to the task job script that
executes the associated task. Consequently, if you override an
environment variable you cannot also access the original parent value:

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

The compressed variant of this, ``COLOR = dark-$COLOR``, is
also in error for the same reason. To achieve the desired result you
must use a different name for the parent variable:

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

These are variables that can be referenced (but should not be modified) in a
task job script.

The task job script may export the following environment variables:

.. code-block:: sub

   CYLC_DEBUG                      # Debug mode, true or not defined
   CYLC_VERSION                    # Version of cylc installation used

   CYLC_CYCLING_MODE               # Cycling mode, e.g. gregorian
   ISODATETIMECALENDAR             # Calendar mode for the `isodatetime` command,
                                   # defined with the value of CYLC_CYCLING_MODE
                                   # when in any date-time cycling mode
   CYLC_WORKFLOW_FINAL_CYCLE_POINT    # Final cycle point
   CYLC_WORKFLOW_INITIAL_CYCLE_POINT  # Initial cycle point
   CYLC_WORKFLOW_NAME                 # Suite name
   CYLC_UTC                        # UTC mode, True or False
   CYLC_VERBOSE                    # Verbose mode, True or False
   TZ                              # Set to "UTC" in UTC mode or not defined

   CYLC_WORKFLOW_RUN_DIR              # Location of the run directory in
                                   # job host, e.g. ~/cylc-run/foo
   CYLC_WORKFLOW_HOST                 # Host running the suite process
   CYLC_WORKFLOW_OWNER                # User ID running the suite process

   CYLC_WORKFLOW_SHARE_DIR            # Suite (or task!) shared directory (see below)
   CYLC_WORKFLOW_UUID                 # Suite UUID string
   CYLC_WORKFLOW_WORK_DIR             # Suite work directory (see below)

   CYLC_TASK_JOB                   # Task job identifier expressed as
                                   # CYCLE-POINT/TASK-NAME/SUBMIT-NUM
                                   # e.g. 20110511T1800Z/t1/01
   CYLC_TASK_CYCLE_POINT           # Cycle point, e.g. 20110511T1800Z
   ISODATETIMEREF                  # Reference time for the `isodatetime` command,
                                   # defined with the value of CYLC_TASK_CYCLE_POINT
                                   # when in any date-time cycling mode
   CYLC_TASK_NAME                  # Job's task name, e.g. t1
   CYLC_TASK_SUBMIT_NUMBER         # Job's submit number, e.g. 1,
                                   # increments with every submit
   CYLC_TASK_TRY_NUMBER            # Number of execution tries, e.g. 1
                                   # increments with automatic retry-on-fail
   CYLC_TASK_ID                    # Task instance identifier expressed as
                                   # TASK-NAME.CYCLE-POINT
                                   # e.g. t1.20110511T1800Z
   CYLC_TASK_LOG_DIR               # Location of the job log directory
                                   # e.g. ~/cylc-run/foo/log/job/20110511T1800Z/t1/01/
   CYLC_TASK_LOG_ROOT              # The task job file path
                                   # e.g. ~/cylc-run/foo/log/job/20110511T1800Z/t1/01/job
   CYLC_TASK_WORK_DIR              # Location of task work directory (see below)
                                   # e.g. ~/cylc-run/foo/work/20110511T1800Z/t1
   CYLC_TASK_NAMESPACE_HIERARCHY   # Linearised family namespace of the task,
                                   # e.g. root postproc t1
   CYLC_TASK_DEPENDENCIES          # List of met dependencies that triggered the task
                                   # e.g. foo.1 bar.1

   CYLC_TASK_COMMS_METHOD          # Set to "ssh" if communication method is "ssh"
   CYLC_TASK_SSH_LOGIN_SHELL       # With "ssh" communication, if set to "True",
                                   # use login shell on suite host

There are also some global shell variables that may be defined in the task job
script (but not exported to the environment). These include:

.. code-block:: sub

   CYLC_FAIL_SIGNALS               # List of signals trapped by the error trap
   CYLC_VACATION_SIGNALS           # List of signals trapped by the vacation trap
   CYLC_WORKFLOW_WORK_DIR_ROOT        # Root directory above the suite work directory
                                   # in the job host
   CYLC_TASK_MESSAGE_STARTED_PID   # PID of "cylc message" job started" command
   CYLC_TASK_WORK_DIR_BASE         # Alternate task work directory,
                                   # relative to the suite work directory


Suite Share Directories
^^^^^^^^^^^^^^^^^^^^^^^

A suite :term:`share directory` is created automatically under the suite run
directory as a share space for tasks. The location is available to tasks as
``$CYLC_WORKFLOW_SHARE_DIR``. In a cycling suite, output files are
typically held in cycle point sub-directories of the suite share directory.

The top level share and work directory (below) location can be changed
(e.g. to a large data area) by a global config setting
:cylc:conf:`global.cylc[platforms][<platform name>]work directory`.


Task Work Directories
^^^^^^^^^^^^^^^^^^^^^

Task job scripts are executed from within
:term:`work directories <work directory>` created automatically under the workflow
run directory. A task can get its own work directory from
``$CYLC_TASK_WORK_DIR`` (or simply ``$PWD`` if it does not ``cd`` elsewhere at
runtime). By default the location contains task name and cycle point, to
provide a unique workspace for every instance of every task. This can be
overridden in the suite configuration, however, to get several tasks to share
the same :cylc:conf:`work directory <global.cylc[platforms][<platform name>]work directory>`.

The top level work and share directory (above) location can be changed
(e.g. to a large data area) by a global config setting
:cylc:conf:`global.cylc[platforms][<platform name>]work directory`.


Environment Variable Evaluation
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Variables in the task execution environment are not evaluated in the
shell in which the suite is running prior to submitting the task. They
are written in unevaluated form to the job script that is submitted by
Cylc to run the task (:ref:`JobScripts`) and are therefore
evaluated when the task begins executing under the task owner account
on the task host. Thus ``$HOME``, for instance, evaluates at
run time to the home directory of task owner on the task host.


How Tasks Get Access To The Run Directory
-----------------------------------------

The workflow bin directory is automatically added
``$PATH``. If a remote suite configuration directory is not
specified, the local (suite host) path will be assumed with the local
home directory, if present, swapped for literal ``$HOME`` for
evaluation on the task host.


.. _RunningTasksOnARemoteHost:

Remote Task Hosting
-------------------

If a task declares a different platform to the one running the workflow,
Cylc will use non-interactive ssh to execute the task using the
:term:`job runner` and one of the hosts from the :term:`platform` definition
(platforms are defined in ``global.cylc[platforms]``).

For example:

.. code-block:: cylc

   [runtime]
       [[foo]]
           platform = orca

For this to work:

- Non-interactive ssh is required from the :term:`scheduler` host
  to the remote platform's hosts.
- Cylc must be installed on the hosts of the destination platform.

  - If polling task communication is used, there is no other
    requirement.
  - If SSH task communication is configured, non-interactive ssh is
    required from the task platform to the workflow platform.
  - If TCP (default) task communication is configured, the task platform
    should have access to the port on the suite host.

- The suite configuration directory, or some fraction of its
  content, can be installed on the task platform, if needed.

Platform, like all namespace settings, can be declared globally in
the root namespace, or per family, or for individual tasks.


Dynamic Platform Selection
^^^^^^^^^^^^^^^^^^^^^^^^^^

.. TODO - consider a re-write once dynamic platform selection done

Instead of hardwiring platform names into the suite configuration you can
specify a shell command that prints a platform name, or an environment
variable that holds a platform name, as the value of the
:cylc:conf:`host config item <[runtime][<namespace>]platform>`.


Remote Task Log Directories
^^^^^^^^^^^^^^^^^^^^^^^^^^^

Task stdout and stderr streams are written to :term:`log files <job log>` in a
suite-specific sub-directory of the suite :term:`run directory`, as
explained in :ref:`WhitherStdoutAndStderr`. For remote tasks
the same directory is used, but *on the task host*.
Remote task log directories, like local ones, are created on the fly, if
necessary, during job submission.


.. _ImplicitTasks:

Implicit Tasks
--------------

An :term:`implicit task` appears in the workflow graph but has no
explicit runtime configuration section. Such tasks automatically
inherit the configuration from the root namespace.
This is very useful because it allows functional suites to
be mocked up quickly for test and demonstration purposes by simply
defining the graph. It is somewhat dangerous, however, because there
is no way to distinguish an intentional implicit task from one
caused by typographic error. Misspelling a task name in the graph
results in a new implicit task replacing the intended task in the
affected trigger expression, and misspelling a task name in a runtime
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
