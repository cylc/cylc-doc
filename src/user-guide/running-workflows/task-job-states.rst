Task and Job States
===================

**Tasks** are a workflow abstraction; they represent future and past jobs as
well as current active ones.

**Jobs** are less of an abstraction; they represent real job scripts submitted
to run as a process on a computer somewhere, or the final status of those
real processes.

A single task can submit multiple jobs, by automatic retry or manual triggering.

In the Cylc UI, task states are represented by monochromatic task icons, and
job states by coloured job icons.


.. TODO include task and job state images 


.. table::

    ================  ===========
    Task-only states  Description
    ================  ===========
    waiting           waiting on prerequisites, triggers, internal queues, or runahead limit
    expired           will not submit job - too far behind the clock
    preparing         job being prepared for submission by the scheduler
    ================  ===========


.. table::

    ===============   ===========
    Task-job states   Description
    ===============   ===========
    submitted         job submitted to the job runner on the job platform
    submit-failed     job submission failed
    running           job running (*started* message received)
    succeeded         job succeeded (*succeeded* message received)
    failed            job failed (*failed* message received)
    ===============   ===========


The Active Task Window
======================

Cylc graphs can be very large, or even infinite in cycling workflows, but the
scheduler does not need to be aware of every single task in the entire run. It
just keeps track of current active tasks and what comes after them in the
graph. The meaning of *active tasks* here is:

- Tasks in the ``preparing`` state
- Tasks with active jobs: ``submitted``, ``running``
- Any ``succeeded`` or ``failed`` tasks being retained as incomplete (and any
  ``submit-failed`` tasks)
- Any ``waiting`` tasks held back by unsatisfied external triggers

We also call this the ``n=0`` task window. The UI can display more than this,
to a requested number of graph edges around the active tasks. The default
window size is ``n=1``, which is active tasks plus tasks one graph edge away
from them.

.. note::
   Tasks ahead of the n=0 window are displayed by the UI as ``waiting``, but
   unlike the "active" waiting tasks they don't actually exist yet as far as
   the scheduler is concerned.


Waiting Tasks in the Active Window
----------------------------------

Waiting tasks in the ``n=0`` window depend on unsatisfied non-task prerequisites:

- :ref:`InternalQueues`
- :ref:`RunaheadLimit`
- external triggers
- clock triggers
  

A ``waiting`` task that has one or more jobs associated with it must be going
to retry.
