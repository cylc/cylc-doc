Advanced
========


Scheduler Signals
-----------------

The Cylc scheduler will shutdown gracefully on receipt of any of the following
signals:

* ``SIGINT``
* ``SIGTERM``
* ``SIGHUP``

The signal will cause the scheduler to shutdown in ``--now`` mode.

If the scheduler is already shutting down in ``--now`` mode, the signal will
escalate shutdown to ``--now --now`` mode.

See ``cylc stop --help`` for details on stop modes.


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
file records that).
