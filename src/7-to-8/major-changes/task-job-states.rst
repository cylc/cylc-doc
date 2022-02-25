.. _728.task_job_states:

Task/Job States
===============

.. seealso::

   - User Guide :ref:`task-job-states`

:term:`Tasks <task>` are nodes in the abstract workflow graph representing
processes that should run once their prerequisites are satisfied. :term:`Jobs
<job>` are the real processes submitted to execute these tasks (or at least, at
the submission stage, real job scripts). A task can have multiple jobs, by
automatic retries and manual re-triggering.

Cylc 7 had 13 task/job states. The GUI only showed tasks, with job data
from the latest task job.

Cylc 8 has only 8 task/job states. The Cylc 8 UI shows both task and jobs.
Task icons are monochrome circles; job icons are coloured squares. The running
task icon incorporates a radial progress indicator.