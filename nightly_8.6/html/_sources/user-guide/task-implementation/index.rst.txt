Task Implementation
-------------------

This section covers the technical detail of how Cylc runs :term:`tasks <task>`.

In Cylc :term:`tasks <task>` represent activities within the workflow.
:term:`Tasks <task>` submit :term:`jobs <job>` when they are run.

Tasks are the "abstract" workflow component. Jobs are the concrete
representation of a task. One task could submit many jobs (for example if the
job fails and the task is re-run).

.. toctree::
   :maxdepth: 2

   job-scripts
   job-submission
   ssh-job-management
   skip-mode
