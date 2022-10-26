.. _task-job-states:

Task & Job States
=================

**Tasks** are a workflow abstraction; they represent future and past jobs as
well as current active jobs. In the Cylc UI, task states have monochromatic
icons like this: |task-running|.

**Jobs** are less abstract; they represent real job scripts submitted to run
on a :term:`job platform`, or the final status of those real jobs. In the Cylc
UI, job states have coloured icons like this: |job-running|.

A single task can have multiple jobs, by automatic retry or manual triggering.


.. table::

   ============== ==================== =================== ====================================
   State          Task Icon            Job Icon            Description
   ============== ==================== =================== ====================================
   waiting        |task-waiting|                           waiting on prerequisites
   preparing      |task-preparing|                         job being prepared for submission
   submitted      |task-submitted|     |job-submitted|     job submitted
   running        |task-running|       |job-running|       job running
   succeeded      |task-succeeded|     |job-succeeded|     job succeeded
   failed         |task-failed|        |job-failed|        job failed
   submit-failed  |task-submit-failed| |job-submit-failed| job submission failed
   expired        |task-expired|                           will not submit job (too far behind)
   ============== ==================== =================== ====================================

.. note::

   The running task icon contains a clock face which shows the time elapsed
   as a proportion of the average runtime. For example this task has been running
   for about one third of its average runtime:

   .. image:: ../../img/task-job-icons/task-running.png
      :width: 60px
      :align: center
