Remote Job Management
=====================

Managing tasks in a workflow requires more than just job execution: Cylc
performs additional actions with ``rsync`` for file transfer, and
direct execution of ``cylc`` sub-commands over non-interactive SSH.


SSH-free Job Management?
------------------------

Some sites may want to restrict access to job hosts by whitelisting SSH
connections to allow only ``rsync`` for file transfer, and allowing job
execution only via a local batch system that sees the job hosts [1]_ .
We are investigating the feasibility of SSH-free job management when a local
batch system is available, but this is not yet possible unless your suite
and job hosts also share a filesystem, which allows Cylc to treat jobs as
entirely local [2]_ .


SSH-based Job Management
------------------------

Cylc does not have persistent agent processes running on job hosts to act on
instructions received over the network [3]_ so instead we execute job
management commands directly on job hosts over SSH. Reasons for this include:

- It works equally for batch system and background jobs.
- SSH is *required* for background jobs, and for batch jobs if the
  batch system is not available on the suite host.
- Querying the batch system alone is not sufficient for full job
  polling functionality.
  
  - This is because jobs can complete (and then be forgotten by
    the batch system) while the network, suite host, or :term:`scheduler` is
    down (e.g. between suite shutdown and restart).
  - To handle this we get the automatic job wrapper code to write
    job messages and exit status to *job status files* that are
    interrogated by :term:`schedulers <scheduler>` during job polling
    operations.
  - Job status files reside on the job host, so the interrogation
    is done over SSH.

- Job status files also hold batch system name and job ID; this is
  written by the job submit command, and read by job poll and kill commands


Other Cases Where Cylc Uses SSH Directly
----------------------------------------

.. TODO - do a scan through the codebase to assert that this is still the only
          uses of SSH in Cylc Flow.

- To see if a suite is running on another host with a shared
  filesystem - see ``cylc/flow/suite_files:detect_old_contact_file``.


.. [1] A malicious script could be ``rsync``'d and run from a batch
       job, but batch jobs are considered easier to audit.
.. [2] The job ID must also be valid to query and kill the job via the local
       batch system. This is not the case for Slurm, unless the ``--cluster``
       option is explicitly used in job query and kill commands, otherwise
       the job ID is not recognized by the local Slurm instance.
.. [3] This would be a more complex solution, in terms of implementation,
       administration, and security.
