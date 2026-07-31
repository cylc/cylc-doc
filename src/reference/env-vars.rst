.. _reference.environment_variables:

Environment Variables
=====================

This section documents the environment variables that Cylc provides or uses in
different contexts.

.. envvar:: CYLC_PYTHONPATH

   Cylc has been configured to ignore the ``PYTHONPATH`` environment variable.

   This means that ``PYTHONPATH`` can safely be used in Cylc job scripts
   without corrupting the installation of Cylc itself.

   There are some niche cases in which you might want to add a package into the
   Cylc environment itself. For these purposes, use ``CYLC_PYTHONPATH`` as you
   would use ``PYTHONPATH`` normally.

   For more information see, :ref:`changes.CYLC_PYTHONPATH`.


.. _reference.wrapper_script_environment_variables:

Wrapper Script Environment Variables
------------------------------------

The recommended way to manage Cylc deployments is via a "wrapper script".

Cylc provides a wrapper script which can be used to manage multiple parallel
deployments of different versions of Cylc and a mechanism for switching between
them. For more information on the wrapper scrip, see :Ref:`managing
environments`.

The Cylc wrapper script uses / defines the following environment variables:

.. envvar:: CYLC_VERSION

   Can be set by users (e.g. in ``.bash_profile``) in order to select a
   specific Cylc environment.

   If set this wrapper will look for an installed environment called
   ``cylc-$CYLC_VERSION`` in the ROOT locations (if not set it will
   look for an installed environment called ``cylc``).
   e.g, ``export CYLC_VERSION=8.0.0-1``.

.. envvar:: CYLC_HOME_ROOT

   The location of installed Cylc environments.

   Usually defined in this wrapper script.

.. envvar:: CYLC_HOME_ROOT_ALT

   An alternate location of installed Cylc environments.

   Can be set by users for use with their own Cylc environments, typically for
   development purposes. If used it must be set on workflow and job hosts, e.g.
   in ``.bash_profile``.
   e.g, ``export CYLC_HOME_ROOT_ALT=$HOME/miniconda3/envs``

.. envvar:: CYLC_ENV_NAME

   Is set to the basename of the selected environment.

   If set this defines the environment name rather than :envvar:`CYLC_VERSION`.
   The scheduler sets ``CYLC_ENV_NAME`` for all remote commands to ensure the
   same environment is used on all platforms. Users should not set
   ``CYLC_ENV_NAME`` (use :envvar:`CYLC_VERSION`).

.. envvar:: CYLC_HOME

   Full path to the Cylc environment.

   Can be set by users in order to use an environment outside of the ROOT
   locations. However, it is not passed by the scheduler to remote platforms so
   use of :envvar:`CYLC_VERSION` & :envvar:`CYLC_HOME_ROOT_ALT` is preferred.



.. _job-script-environment-variables:

Job Script Environment Variables
--------------------------------

These environment variables provided by the :term:`scheduler` are available
to :ref:`Cylc job scripts <Task Job Script Variables>` at run time:


.. describe:: CYLC_VERSION

   The version of cylc this workflow is running with.


.. envvar:: CYLC_VERBOSE

   Verbose mode, ``true`` or ``false``.

   Cylc workflows can be run in verbose mode using the ``cylc play -v``
   option.


.. envvar:: CYLC_DEBUG

   Debug mode (even more verbose), true or false

   Cylc workflows can be run in debug mode using the ``cylc play --debug``
   option (note, ``--debug`` is equivalent to ``-vv``).


.. envvar:: CYLC_CYCLING_MODE

   Cycling mode, e.g. ``gregorian`` or ``integer``.


.. envvar:: ISODATETIMECALENDAR

   Calendar mode for the ``isodatetime`` command, defined with the value of
    :envvar:`CYLC_CYCLING_MODE` when in any datetime cycling mode.


.. envvar:: CYLC_UTC

   UTC mode, ``True`` or ``False``.

   See :cylc:conf:`flow.cylc[scheduler]UTC mode`.


.. envvar:: TZ

   Set to "UTC" in :cylc:conf:`UTC mode <flow.cylc[scheduler]UTC mode>` or not
   defined


.. envvar:: CYLC_WORKFLOW_INITIAL_CYCLE_POINT

   The workflow's
   :cylc:conf:`initial cycle point <flow.cylc[scheduling]initial cycle point>`.


.. envvar:: CYLC_WORKFLOW_FINAL_CYCLE_POINT

   The workflow's
   :cylc:conf:`final cycle point <flow.cylc[scheduling]final cycle point>`.


.. envvar:: CYLC_WORKFLOW_ID

   Workflow ID e.g. ``foo/run1`` or ``a/b/c/run1``.


.. envvar:: CYLC_WORKFLOW_NAME

   Workflow ID with the run name removed (use :envvar:`CYLC_WORKFLOW_ID` for
   most purposes) e.g. ``foo`` or ``a/b/c``.


.. envvar:: CYLC_WORKFLOW_NAME_BASE

   The basename of the workflow name (use :envvar:`CYLC_WORKFLOW_ID` for most
   purposes) e.g. ``foo`` or ``c``


.. envvar:: CYLC_WORKFLOW_UUID

   Workflow UUID string.

   Every workflow run is assigned a UUID string to identify it. This is
   preserved when the workflow is restarted.


.. envvar:: CYLC_WORKFLOW_HOST

   The host running the workflow process.


.. envvar:: CYLC_WORKFLOW_OWNER

   The user ID running the workflow process.


.. envvar:: CYLC_WORKFLOW_RUN_DIR

   Location of the run directory in job host, e.g. ``~/cylc-run/foo/run1``.


.. envvar:: CYLC_WORKFLOW_LOG_DIR

   Location of the scheduler's log files, e.g.
   ``~/cylc-run/foo/run1/log/scheduler``.


.. envvar:: CYLC_WORKFLOW_SHARE_DIR

   Workflow (or task!) shared directory e.g. ``~/cylc-run/foo/run1/share``


.. envvar:: CYLC_WORKFLOW_WORK_DIR

   Workflow work directory, e.g. ~/cylc-run/foo/run1/work


.. envvar:: CYLC_TASK_JOB

   Job identifier expressed as ``CYCLE-POINT/TASK-NAME/SUBMIT-NUMBER`` e.g.
   ``20110511T1800Z/t1/01``.


.. envvar:: CYLC_TASK_ID

   Task instance identifier ``CYCLE-POINT/TASK-NAME`` e.g.
   ``20110511T1800Z/t1``.


.. envvar:: CYLC_TASK_NAME

   The name of the :term:`task` which submitted this :term:`job`, e.g. ``t1``.


.. envvar:: CYLC_TASK_CYCLE_POINT

   Cycle point, e.g. ``20110511T1800Z``.


.. envvar:: ISODATETIMEREF

   Reference time for the ``isodatetime`` command, defined with the value of
    :envvar:`CYLC_TASK_CYCLE_POINT` when in any datetime cycling mode.


.. envvar:: CYLC_TASK_SUBMIT_NUMBER

   Job's submit number, e.g. ``1``, this increments with every submit.


.. envvar:: CYLC_TASK_TRY_NUMBER

   This job's (re)try number.

   The try number starts at ``1`` with the first submission and is incremented
   for each automated execution retry (but not for manual resubmissions).

   Execution retries can be configured using
   :cylc:conf:`flow.cylc[runtime][<namespace>]execution retry delays`.


.. envvar:: CYLC_TASK_FLOW_NUMBERS

   The :term:`flows <flow>` this task belongs to, e.g. ``1,2``.


.. envvar:: CYLC_TASK_LOG_DIR

   Location of the job log directory e.g.
   ``~/cylc-run/foo/run1/log/job/20110511T1800Z/t1/01/``.


.. envvar:: CYLC_TASK_LOG_ROOT

   The job script path e.g.
   ``~/cylc-run/foo/run1/log/job/20110511T1800Z/t1/01/job``.


.. envvar:: CYLC_TASK_SHARE_CYCLE_DIR

   Cycle point-specific shared directory for this task. e.g.
   ``~/cylc-run/foo/run1/share/cycle/20110511T1800Z``.


.. envvar:: CYLC_TASK_WORK_DIR

   Location of task work directory (see below) e.g.
   ``~/cylc-run/foo/run1/work/20110511T1800Z/t1``.


.. envvar:: CYLC_TASK_NAMESPACE_HIERARCHY

   Linearised family namespace of the task, e.g. ``root postproc t1``.


.. envvar:: CYLC_TASK_COMMS_METHOD

   Set to "ssh" if
   :cylc:conf:`communication method <global.cylc[platforms][<platform name>]communication method>`,
   is "ssh".


.. envvar:: CYLC_TASK_SSH_LOGIN_SHELL

   For use with 
   :cylc:conf:`SSH communication <global.cylc[platforms][<platform name>]communication method>`,
   if set to "True", use login shell on workflow host.


.. envvar:: CYLC_TASK_PARAM_<param>

   If this task is a parameterized task, the value of the parameter named
   ``<param>``.
