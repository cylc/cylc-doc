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



