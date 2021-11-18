
.. _Task Job Polling:

Task Job Polling
----------------

At any point after job submission, task jobs can be *polled* to check that
their true state matches what scheduler expects based on received job status
messages or previous polls.

Polling may be necessary if, for example, a task job gets killed by the
untrappable SIGKILL signal (e.g. ``kill -9 PID``), or after a network
outage that prevents job status messages getting back to the scheduler, or if
the :term:`scheduler` itself was down when active task jobs finished.

To poll a job the :term:`scheduler` interrogates the :term:`job runner`, and
the ``job.status`` file of the task, on the job host. This information is
enough to determine correct task status even if the job finished while the
:term:`scheduler` was down or unreachable on the network.

.. seealso::
   - ``cylc poll --help``


Routine Polling
^^^^^^^^^^^^^^^

Task jobs are automatically polled at certain times: once on job submission
timeout; several times on exceeding the job execution time limit; and at
workflow restart any tasks recorded as active are polled to find out what
happened to them while the workflow was down.

Routine polling can also be configured as a way to track job status on platforms
that do not allow routing back to the workflow host for task messaging by TCP
or SSH. See :ref:`Polling To Track Job Status`.


.. _TaskComms:

Tracking Task State
-------------------

Cylc supports three ways of tracking task state on job hosts:

- task-to-workflow messaging via TCP (using ZMQ protocol)
- task-to-workflow messaging via non-interactive SSH to the workflow host, then
  local TCP.
- regular polling by the :term:`scheduler`

These can be configured per platform using
:cylc:conf:`global.cylc[platforms][<platform name>]communication method`.

If your site prohibits TCP and SSH back from job hosts to workflow hosts,
before resorting to the polling method you should consider installing dedicated
Cylc servers or VMs inside the HPC trust zone (where TCP and SSH should be
allowed).

It is possible to run Cylc :term:`schedulers <scheduler>` on HPC login nodes,
but be aware of scheduler resource requirements (which depend on workflow size
and run duration)

Port forwarding could potentially provide another solution, but the idea has
been rejected at this stage. Organisations often disable port forwarding for
security reasons.

.. note::
   Use Cylc 8 platform configuration via
   :cylc:conf:`flow.cylc[runtime][<namespace>]platform`, not the
   deprecated ``host`` setting, to ensure the intended task communication
   method is applied.

TCP Task Messaging
^^^^^^^^^^^^^^^^^^

Task job wrappers automatically invoke ``cylc message`` to report
progress back to the :term:`scheduler` when they begin executing,
at normal exit (success) and abnormal exit (failure).

By default job status messaging goes by an authenticated TCP connection to the
:term:`scheduler`, using the ZMQ protocol.  This is the preferred task
communications method because it is efficient and direct.

Schedulers automatically install workflow :term:`contact information
<contact file>` and credentials on job hosts.


.. obsolete? Users only need to do this manually for remote access to workflows
   on other hosts, or workflows owned by other users - see :ref:`RemoteControl`.


SSH Task Communication
^^^^^^^^^^^^^^^^^^^^^^

Cylc can be configured to re-invoke task messaging commands on the workflow
host via non-interactive SSH (from job platform to workflow host).

User-invoked client commands also support this communication method, when
:cylc:conf:`global.cylc[platforms][<platform name>]communication method` is
configured to ``ssh``.

This is less efficient than direct ZMQ protocol messaging, but it may be useful at
sites where the ZMQ ports are blocked but non-interactive SSH is allowed.

.. warning::

   Ensure SSH keys are in place for the remote task platform(s) before enabling
   this feature. Failure to do so, will result in ``Host key verification
   failed`` errors.


.. _Polling To Track Job Status:

Polling to Track Job Status
^^^^^^^^^^^^^^^^^^^^^^^^^^^

Schedulers can actively poll task jobs at configured intervals, via
non-interactive SSH to the job platform.

This is the least efficient communication method because task status updates
are delayed by up to the polling interval. However, it may be needed at sites
that do not allow TCP or non-interactive SSH from job host to workflow host.

Be careful to avoid spamming task hosts with polling operations. Each poll
opens (and then closes) a new SSH connection.

Polling intervals are configurable under :cylc:conf:`[runtime]` because they
may depend on expected job execution time. You may want to poll a job
frequently at first, to check that it started running properly; frequently
near the expected end of its run time, to get a timely task finished update;
and infrequently between times. Configured intervals are used in sequence until
the last value, which is used repeatedly until the job is finished:

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
submission. If these items are not configured default values from
site and user global config will be used for
:cylc:conf:`communication method = polling`.

Polling is not done by default under the other task communications methods, but
it can be configured as well if you like.


