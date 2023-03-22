.. _TaskJobSubmission:

Job Submission and Management
=============================

This section explains how the Cylc scheduler submits :term:`jobs <job>`
when they are ready to run, and how to define new :term:`job runner` handlers.

.. note::

   For the requirements a command, script, or program, must fulfil in order to
   function as a Cylc task, see :ref:`TaskImplementation`.

When a task is ready Cylc generates a :term:`job script` (see :ref:`JobScripts`).
The job script is submitted to be run by the job runner from the
:term:`platform` chosen for the task.
Like other runtime properties, you can set a workflow default platform and
override it for specific tasks or families:

.. code-block:: cylc

   [runtime]
      [[root]] # workflow defaults
           platform = platform_with_loadleveler
      [[foo]] # just task foo
           platform = platform_with_at


.. _AvailableMethods:

Supported Job Submission Methods
--------------------------------

Cylc provided built-in support for the following batch submission systems:

.. NOTE this builds and links stub-pages for each of the job runners

.. automodule:: cylc.flow.job_runner_handlers

See :ref:`CustomJobSubmissionMethods` for how to add new job
submission methods.

Default Directives Provided
^^^^^^^^^^^^^^^^^^^^^^^^^^^

For :term:`job runners <job runner>` that use job file directives (PBS, Loadleveler,
etc.) default directives are provided to set the job name, stdout and stderr
file paths, and the execution time limit (if specified).

Cylc constructs the job name string using a combination of the task ID and the
workflow name. PBS fails a job submit if the job name in ``-N name`` is
too long. For version 12 or below, this is 15 characters. For version 13, this
is 236 characters. The default setting will truncate the job name string to 236
characters. If you have PBS 12 or older at your site, you should modify your
site's global configuration file to allow the job name to be truncated at 15
characters using
:cylc:conf:`global.cylc[platforms][<platform name>]job name length maximum`.

Directives Section Quirks (PBS, SGE, ...)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

To specify an option with no argument, such as ``-V`` in PBS or
``-cwd`` in SGE you must give a null string as the directive value in
the :cylc:conf:`flow.cylc` file.

The left hand side of a setting (i.e. the string before the first equal sign)
must be unique. To specify multiple values using an option such as
``-l`` option in PBS, SGE, etc., either specify all items in a single
line:

.. code-block:: none

   -l=select=28:ncpus=36:mpiprocs=18:ompthreads=2:walltime=12:00:00

(Left hand side is ``-l``. A second ``-l=...`` line will override the first.)

Or separate the items:

.. code-block:: none

   -l select=28
   -l ncpus=36
   -l mpiprocs=18
   -l ompthreads=2
   -l walltime=12:00:00

.. note::

   There is no equal sign after ``-l``.

(Left hand sides are now ``-l select``, ``-l ncpus``, etc.)


.. _WhitherStdoutAndStderr:

Task stdout and stderr Logs
---------------------------

When a task is ready to run Cylc generates a filename root to be used
for the job script and log files. The file path contains the task
name, cycle point, and a submit number that increments if the same task is
re-triggered multiple times:

.. code-block:: sub

   # job script:
   ~/cylc-run/my-workflow/basic/log/job/1/hello/01/job
   # stdout:
   ~/cylc-run/my-workflow/basic/log/job/1/hello/01/job.out
   # stderr:
   ~/cylc-run/my-workflow/basic/log/job/1/hello/01/job.err

How the stdout and stderr streams are directed into these files depends on the
:term:`job runner`. The
:py:mod:`background <cylc.flow.job_runner_handlers.background>` method just
uses appropriate output redirection on the command line, as shown above. The
:py:mod:`loadleveler <cylc.flow.job_runner_handlers.loadleveler>` method writes
appropriate directives to the job script that is submitted to loadleveler.

Cylc obviously has no control over the stdout and stderr output from
tasks that do their own internal output management (e.g. tasks
that submit internal jobs and direct the associated output to other
files). For less internally complex tasks, however, the files referred
to here will be complete job logs.

Some job runners, such as :py:mod:`PBS <cylc.flow.job_runner_handlers.pbs>`,
redirect a job's stdout
and stderr streams to a separate cache area while the job is running. The
contents are only copied to the normal locations when the job completes. This
means that ``cylc cat-log`` will be unable to find the
job's stdout and stderr streams while the job is running. Some sites with these
job runners are known to provide commands for viewing and/or
tail-follow a job's stdout and stderr streams that are redirected to these
cache areas. If this is the case at your site, you can configure Cylc to make
use of the provided commands by adding some settings to the global site/user
config. E.g.:

.. TODO - re-write this example when default directives arrive for platforms

.. code-block:: cylc

   [hosts]
       [[HOST]]  # <= replace this with a real host name
           [[[batch systems]]]
               [[[[pbs]]]]
                   err tailer = qcat -f -e \%(job_id)s
                   out tailer = qcat -f -o \%(job_id)s
                   err viewer = qcat -e \%(job_id)s
                   out viewer = qcat -o \%(job_id)s


.. _CommandTemplate:

Overriding The Job Submission Command
-------------------------------------

To change the form of the actual command used to submit a job you
need to define a new
:cylc:conf:`global.cylc[platforms][<platform name>]job runner command template`.

.. code-block:: cylc

   [platform]
       [[my_custom_platform]]
           hosts = host1, host2
           job runner = loadleveler
           # Use '-s' to stop llsubmit returning
           # until all job steps have completed:
           job runner command template = llsubmit -s %(job)s

The template's ``%(job)s`` will be substituted by the job file path.


Job Polling
-----------

For supported :term:`job runners <job runner>`, jobs can be *polled* to
check that their true state matches what the scheduler expects based on received
job status messages or previous polls. The :term:`scheduler` executes a process
on the task host, by non-interactive ssh, to interrogate the job runner, and to
read the ``job.status`` file of the task which is automatically generated by the
:term:`job script` as it runs.

Polling may be required to update the workflow state correctly after unusual
events such as

- a job gets killed by the untrappable SIGKILL signal (e.g. ``kill -9 PID``)
- a machine being rebooted with tasks running on it
- network problems prevent task messages from getting back to the workflow host
- the :term:`scheduler` itself was down when active jobs finished

Tasks can be polled on demand by using the
``cylc poll`` command.

.. seealso::
   - ``cylc poll --help``

Tasks are polled automatically, once, if they timeout while queueing in a
job runner and submission timeout is set.
(See :cylc:conf:`[runtime][<namespace>][events]`
for how to configure timeouts).

Tasks are polled multiple times, where necessary, when they exceed their
execution time limits. These are normally set with some initial delays to allow
the job runners to kill the jobs.
(See
:cylc:conf:`execution time limit polling intervals <global.cylc[platforms][<platform name>]execution time limit polling intervals>`
for how to configure the polling intervals).

Any tasks recorded in the *submitted* or *running* states at workflow
restart are automatically polled to determine what happened to them while the
workflow was down.

By default, regular polling also takes place every 15 minutes whilst a job is
submitted or running. The default polling intervals can be overridden in the
global configuration:

* :cylc:conf:`global.cylc[platforms][<platform name>]submission polling intervals`
* :cylc:conf:`global.cylc[platforms][<platform name>]execution polling intervals`

The polling intervals can also be configured for individual tasks:

* :cylc:conf:`[runtime][<namespace>]submission polling intervals`
* :cylc:conf:`[runtime][<namespace>]execution polling intervals`

Polling can be used as the sole method of determining task status on hosts that
do not allow task messages to be routed back to the workflow host.
See :ref:`Polling To Track Job Status`.

.. note::

   For polling to work correctly, the job runner queueing system must have a
   job listing command for listing your jobs, and that the job listing must
   display job IDs as they are returned by the job runner queueing system submit
   command. For example, for pbs, moab and sge, the ``qstat`` command
   should list jobs with their IDs displayed in exactly the same format as they
   are returned by the ``qsub`` command.


Job Killing
-----------

For supported :term:`job runners <job runner>`, the :term:`scheduler` can execute a process on
the task host, by non-interactive ssh, to kill a submitted or running job
according to its job runner.

Tasks can be killed on demand by using the ``cylc kill`` command.


Execution Time Limit
--------------------

.. cylc-scope:: flow.cylc[runtime][<namespace>]

You can specify an :cylc:conf:`execution time limit` for all supported job
submission methods. E.g.:

.. code-block:: cylc

   [runtime]
       [[task-x]]
           execution time limit = PT1H

For tasks running with
:py:mod:`background <cylc.flow.job_runner_handlers.background>` or
:py:mod:`at <cylc.flow.job_runner_handlers.at>`, their jobs
will be wrapped using the ``timeout`` command. For all other methods,
the relevant time limit directive will be added to their job files.

The :cylc:conf:`execution time limit` setting will also inform the workflow when a
a job should complete by. If a job has not reported completing within
the specified time, the workflow will poll the job. (The default
setting is ``PT1M, PT2M, PT7M``. The accumulated times for these intervals will be
roughly 1 minute, 1 + 2 = 3 minutes and 1 + 2 + 7 = 10 minutes after a job
exceeds its :cylc:conf:`execution time limit`.)

.. cylc-scope::


Execution Time Limit and Execution Timeout
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. cylc-scope:: flow.cylc[runtime][<namespace>]

If you specify an :cylc:conf:`execution time limit` the
execution timeout event handler will only be called if the job has
not completed after the final poll (by default, 10 min after the time limit).
This should only happen if the submission method you are using is not enforcing
wallclock limits (unlikely) or you are unable to contact the machine to confirm
the job status.

If you specify an :cylc:conf:`[events]execution timeout` and not an
:cylc:conf:`execution time limit` then the
execution timeout event handler will be called as soon as the
specified time is reached. The job will also be polled to check its latest
status (possibly resulting in an update in its status and the calling of the
relevant event handler). This behaviour is deprecated, which users should avoid
using.

If you specify an :cylc:conf:`[events]execution timeout` and an
:cylc:conf:`execution time limit` then the execution timeout setting will be
ignored.

.. cylc-scope::


.. _CustomJobSubmissionMethods:

Custom Job Submission Methods
-----------------------------

Defining a new job runner handler requires a little Python programming. Use
the built-in handlers (e.g. :py:mod:`cylc.flow.job_runner_handlers.background`)
as examples.


An Example
^^^^^^^^^^

The following ``qsub.py`` module overrides the built-in *pbs*
job runner handler to change the directive prefix from ``#PBS`` to
``#QSUB``:

.. TODO - double check that this still works, it's been a while

.. code-block:: python

   #!/usr/bin/env python3

   from cylc.flow.job_runner_handlers.pbs import PBSHandler

   class QSUBHandler(PBSHandler):
       DIRECTIVE_PREFIX = "#QSUB "

   JOB_RUNNER_HANDLER = QSUBHandler()

If this is in the Python search path (see
:ref:`Where To Put Job Runner Handler Modules` below) you can use it by
name in your global configuration:

.. code-block:: cylc

   [platforms]
       [[my_platform]]
           hosts = myhostA, myhostB
           job runner = qsub  # <---!

Then in your ``flow.cylc`` file you can use this platform:

.. code-block:: cylc

   [scheduling]
       [[graph]]
           R1 = "a"
   [runtime]
       [[root]]
           execution time limit = PT1M
           platform = my_platform
           [[[directives]]]
               -l nodes = 1
               -q = long
               -V =

Note, this workflow will fail at run time because we only changed the
directive format, and PBS does not accept ``#QSUB`` directives in
reality.


.. _Where To Put Job Runner Handler Modules:

Where To Put Job Runner Handler Modules
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Custom job runner handlers must be installed on workflow and job
hosts in one of these locations:

- under ``WORKFLOW-RUN-DIR/lib/python/``
- under ``CYLC-PATH/cylc/flow/job_runner_handlers/``
- or anywhere in ``$PYTHONPATH``
