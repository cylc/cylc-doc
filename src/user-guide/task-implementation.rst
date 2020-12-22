.. _TaskImplementation:

Task Implementation
===================

Existing scripts and executables can be used as Cylc tasks without
modification so long as they return standard exit status - zero on success,
non-zero for failure - and do not spawn detaching processes internally (see
:ref:`DetachingJobs`).


.. _JobScripts:

Task Job Scripts
----------------

When the :term:`scheduler` determines that a task is ready to run it
generates a *job script* for the task, and submits it to run (see
:ref:`TaskJobSubmission`).

.. cylc-scope:: flow.cylc[runtime][<namespace>]

:term:`Job scripts <job script>` encapsulate configured task runtime settings:
:cylc:conf:`script` and :cylc:conf:`[environment]` items, if defined, are just
concatenated in the order shown below, to make the job script. Everything
executes in the same shell, so each part of the script can potentially affect
the environment of subsequent parts.

.. digraph:: example

   rankdir="LR"

   subgraph cluster_legend {
      style="dashed"
      label="Legend"

      "user defined script"
      "cylc defined script" [shape="rect"]

      "user defined script" -> "cylc defined script" [style="invis"]
   }

   subgraph cluster_diagram {
      style="invis"

      "cylc-env" [shape="rect"]
      "user-env" [shape="rect"]

      "init-script" ->
      "cylc-env" ->
      "env-script" ->
      "user-env" ->
      "pre-script" ->
      "script" ->
      "post-script" -> "err-script"
      "post-script" -> "exit-script"
   }

The two "Cylc defined scripts" are:

``cylc-env``
   Which provides default ``CYLC_*`` environment variables e.g.
   ``CYLC_TASK_NAME``.
``user-env``
   Which is the contents of the :cylc:conf:`[environment]` section.

Task job scripts are written to the suite's job log directory. They can be
printed with ``cylc cat-log``.

.. cylc-scope::


Inlined Tasks
-------------

Task *script* items can be multi-line strings of ``bash``  code, so many tasks
can be entirely inlined in the :cylc:conf:`flow.cylc` file.

For anything more than a few lines of code, however, we recommend using
external shell scripts to allow independent testing, re-use, and shell mode
editing.


Interpreter
-----------

The job script (which incorporates the ``*-script`` items) runs in the
``bash`` interpreter.

Cylc searches for ``bash`` in the ``$PATH`` by first running a login bash
shell which means you can choose the bash interpreter used by modifying
the ``$PATH`` in your bash configuration files (e.g. ``.bashrc``).


Task Messages
-------------

Task jobs send status messages back to the :term:`scheduler` to report that
execution has started, succeeded, or failed. Custom messages can also be sent
by the same mechanism, with various severity levels. These can be used to
trigger other tasks off specific task outputs (see :ref:`MessageTriggers`), or
to trigger execution of event handlers by the scheduler (see
:ref:`EventHandling`), or just to write information to the scheduler log.

.. cylc-scope:: global.cylc[platforms][<platform name>]

(If polling is configured as the :cylc:conf:`communication method` for a
:cylc:conf:`platform <[..]>`, the messaging system just writes messages to the
local job status file for recovery by the scheduler at the next poll).

.. cylc-scope::

Normal severity messages are printed to ``job.out`` and logged by the scheduler:

.. code-block:: bash

   cylc message -- "${CYLC_SUITE_NAME}" "${CYLC_TASK_JOB}" \
     "Hello from ${CYLC_TASK_ID}"

"CUSTOM" severity messages are printed to ``job.out``, logged by the
:term:`scheduler`, and can be used to trigger *custom*
event handlers:

.. code-block:: bash

   cylc message -- "${CYLC_SUITE_NAME}" "${CYLC_TASK_JOB}" \
     "CUSTOM:data available for ${CYLC_TASK_CYCLE_POINT}"

These can be used to signal special events that are neither routine
information nor an error condition, such as production of a particular data
file (a "data availability" event).

"WARNING" severity messages are printed to ``job.err``, logged by the
:term:`scheduler`, and can be passed to *warning* event handlers:

.. code-block:: bash

   cylc message -- "${CYLC_SUITE_NAME}" "${CYLC_TASK_JOB}" \
     "WARNING:Uh-oh, something's not right here."

"CRITICAL" severity messages are printed to ``job.err``, logged by the
:term:`scheduler`, and can be passed to *critical* event handlers:

.. code-block:: bash

   cylc message -- "${CYLC_SUITE_NAME}" "${CYLC_TASK_JOB}" \
     "CRITICAL:ERROR occurred in process X!"

Task jobs no longer (since Cylc 8) attempt to resend messages if the server
cannot be reached. Send failures normally imply a network or Cylc
configuration problem that will not recover by itself, in which case a series
of messaging retries just holds up job completion unnecessarily. If a job
status message does not get through, the server will recover the correct task
status by polling on job timeout (or earlier if regular polling is
configured).

Task messages are validated by
:py:class:`cylc.flow.unicode_rules.TaskMessageValidator`.

.. autoclass:: cylc.flow.unicode_rules.TaskMessageValidator

Aborting Job Scripts on Error
-----------------------------

Task job scripts use ``set -x`` to abort on any error, and trap ERR, EXIT, and
SIGTERM to send task failed messages back to the :term:`scheduler` before
aborting. Other scripts called from job scripts should therefore abort with
standard non-zero exit status on error, to trigger the job script error trap.

To prevent a command that is expected to generate a non-zero exit status from
triggering the exit trap, protect it with a control statement such as:

.. code-block:: bash

   if cmp FILE1 FILE2; then
       :  # success: do stuff
   else
       :  # failure: do other stuff
   fi

Task job scripts also use ``set -u`` to abort on referencing any
undefined variable (useful for picking up typos); and ``set -o pipefail``
to abort if any part of a pipe fails (by default the shell only returns the
exit status of the final command in a pipeline).


Custom Failure Messages
^^^^^^^^^^^^^^^^^^^^^^^

Critical events normally warrant aborting a job script rather than just
sending a message. As described just above, ``exit 1`` or any failing command
not protected by the surrounding scripting will cause a job script to abort
and report failure to the :term:`scheduler`, potentially triggering a
*failed* task event handler.

For failures detected by the scripting you could send a critical message back
before aborting, potentially triggering a *critical* task event handler:

.. code-block:: bash

   if ! /bin/false; then
     cylc message -- "${CYLC_SUITE_NAME}" "${CYLC_TASK_JOB}" \
       "CRITICAL:ERROR: /bin/false failed!"
     exit 1
   fi

To abort a job script with a custom message that can be passed to a
*failed* task event handler, use the built-in ``cylc__job_abort`` shell
function:

.. code-block:: bash

   if ! /bin/false; then
     cylc__job_abort "ERROR: /bin/false failed!"
   fi


.. _DetachingJobs:

Avoid Detaching Processes
-------------------------

If a task script starts background sub-processes and does not wait on them, or
internally submits jobs to a :term:`job runner` and then exits immediately, the
detached processes will not be visible to Cylc and the task will appear to
finish when the top-level script finishes. You will need to modify scripts
like this to make them execute all sub-processes in the foreground (or use the
shell ``wait`` command to wait on them before exiting) and to prevent job
submission commands from returning before the job completes (e.g.
``llsubmit -s`` for Loadleveler,
``qsub -sync yes`` for Sun Grid Engine, and
``qsub -W block=true`` for PBS).

If this is not possible - perhaps you don't have control over the script
or can't work out how to fix it - one alternative approach is to use another
task to repeatedly poll for the results of the detached processes:

.. code-block:: cylc

   [scheduling]
       [[graph]]
           R1 = "model => checker => post-proc"
   [runtime]
       [[model]]
           # Uh-oh, this script does an internal job submission to run model.exe:
           script = "run-model.sh"
       [[checker]]
           # Fail and retry every minute (for 10 tries at the most) if model's
           # job.done indicator file does not exist yet.
           script = "[[ ! -f $RUN_DIR/job.done ]] && exit 1"
           execution retry delays = 10 * PT1M
