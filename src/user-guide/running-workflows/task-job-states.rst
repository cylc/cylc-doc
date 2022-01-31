.. _task-job-states:

Task & Job States
=================

**Tasks** are a workflow abstraction; they represent future and past jobs as
well as current active jobs. In the Cylc UI, task states have monochromatic
icons like this: |task-running|.

**Jobs** are less abstract; they represent real job scripts submitted to run
on a :term:`job platform`, or the final status of those real jobs. In the Cylc
UI, job states have colored icons like this: |job-running|.

A single task can have multiple jobs, by automatic retry or manual triggering.


.. table::

    =======================================================     ===========
    Task & Job States                                           Description
    =======================================================     ===========
    |task-waiting|       |job-blank|          waiting           waiting on prerequisites
    |task-expired|       |job-blank|          expired           will not submit job (too far behind)
    |task-preparing|     |job-blank|          preparing         job being prepared
    |task-submitted|     |job-submitted|      submitted         job submitted
    |task-submit-failed| |job-submit-failed|  submit-failed     job submission failed
    |task-running|       |job-running|        running           job running
    |task-succeeded|     |job-succeeded|      succeeded         job succeeded
    |task-failed|        |job-failed|         failed            job failed
    =======================================================     ===========
