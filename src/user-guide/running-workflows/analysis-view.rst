.. _user-guide.analysis-view:

Analysing Job Performance
=========================

.. versionadded:: 8.7.0

   Max RSS and CPU time metrics, and the Cylc job profiler which records
   them.

The Cylc GUI includes an **Analysis View** which presents statistics about
the :term:`jobs <job>` that have been run by a workflow. It can be used to
spot slow, inefficient or memory-hungry tasks, and to help choose suitable
resource requests (e.g. wall-clock and memory
:cylc:conf:`directives <flow.cylc[runtime][<namespace>][directives]>`)
for your tasks.

The data shown in the Analysis View is read from the
:ref:`workflow database <Workflow Run Databases>`, so statistics are available
for jobs from previous runs of the workflow, as well as the current run.


Metrics
-------

Use the drop-down menu at the top of the view to choose which metric to
display:

Total times
   The time from job submission to job completion (queue time + run time).

Run times
   The time from job start to job completion (i.e. the wall-clock time spent
   running the job).

Queue times
   The time from job submission to job start (i.e. time spent waiting in the
   job runner's queue).

Max RSS
   The maximum amount of physical memory used by the job.
   See :ref:`below <user-guide.analysis-view.max-rss>` for an exact
   definition.

CPU time
   The total amount of processor time consumed by the job.
   See :ref:`below <user-guide.analysis-view.cpu-time>` for an exact
   definition.

The Max RSS and CPU time metrics are only available for jobs which were run
with the :ref:`Cylc job profiler <user-guide.analysis-view.profiler>`
active.


.. _user-guide.analysis-view.max-rss:

Max RSS
^^^^^^^

**RSS** (Resident Set Size) is the amount of a job's memory which is held in
physical memory (RAM). It does not include memory which has been swapped out
to disk, or memory which has been reserved (allocated) but never used.

**Max RSS** (maximum Resident Set Size, see :term:`max RSS`) is the highest
RSS value recorded over the lifetime of a :term:`job`, i.e. the largest
amount of physical memory used by the job at any one time.

.. note::

   Max RSS is a *per-job* value. The statistics shown in the Analysis View
   (minimum, quartiles, mean and maximum) are calculated across the Max RSS
   values of all of a task's jobs. For example, the "Min Max RSS" of a task is
   the smallest Max RSS recorded by any of its jobs.

In Cylc, Max RSS is measured by the
:ref:`Cylc job profiler <user-guide.analysis-view.profiler>` as follows:

* It is the memory used by **all** processes in the job's
  `control group (cgroup) <https://docs.kernel.org/admin-guide/cgroup-v2.html>`_,
  i.e. the job script and any child processes it starts, not just a single
  process.
* It counts only *anonymous* memory (see
  :ref:`below <user-guide.analysis-view.max-rss.source>` for exactly what
  this does and does not include).
* The value is *sampled* at the profiler's
  :cylc:conf:`polling interval
  <global.cylc[platforms][<platform name>][profiler]polling interval>`
  and the largest sample is kept. Very short-lived memory spikes which occur
  between samples may therefore not be captured, so the reported Max RSS is a
  lower bound on the true maximum memory usage.
* Values are recorded in bytes and displayed in binary units
  (KiB, MiB or GiB, where 1 KiB = 1024 bytes).


.. _user-guide.analysis-view.max-rss.source:

Where the Max RSS Value Comes From
""""""""""""""""""""""""""""""""""

The Linux kernel keeps memory accounting statistics for every cgroup in a
file called ``memory.stat``. The profiler finds the job's cgroup by reading
``/proc/<pid>/cgroup`` for its own process (the profiler runs inside the
job's cgroup), then reads the ``memory.stat`` file for that cgroup from the
directory given by
:cylc:conf:`global.cylc[platforms][<platform name>][profiler]cgroups path`
(default ``/sys/fs/cgroup``):

.. list-table::
   :header-rows: 1

   * - cgroups version
     - File read
     - Field used
   * - v2
     - ``<cgroups path>/<job cgroup>/memory.stat``
     - ``anon``
   * - v1
     - ``<cgroups path>/memory/<job cgroup>/memory.stat``
     - ``total_rss``

On each poll the profiler reads this field and, if it is larger than any
value seen previously, records it. The value reported as Max RSS is the
largest value read.

.. tip::

   This is the same cgroup memory accounting which the kernel's Out Of
   Memory (OOM) mechanism uses to enforce a job's memory limit, rather than
   an estimate from a separate tool. Max RSS can therefore be used as a
   reliable guide when reducing the amount of memory requested for a job,
   without accidentally causing the job to be killed for running out of
   memory. Leave some headroom above the Max RSS of previous runs to allow
   for short spikes between samples and for the non-anonymous memory
   described in the notes below.

Both fields report the amount of *anonymous* memory which is resident in RAM
and charged to the cgroup, including any child cgroups beneath it
(``total_rss`` is the hierarchical version of the v1 ``rss`` field, and
also includes the swap cache; the v2
``anon`` field is hierarchical by default). Anonymous memory is memory which
is not backed by a file, i.e. memory a program obtains for its own data.

**Included** in Max RSS:

* The heap, i.e. memory obtained with ``malloc``/``new``/``allocate``,
  ``brk``/``sbrk`` or private ``mmap(MAP_ANONYMOUS)`` calls. This includes
  arrays, data structures and any I/O buffers which a program allocates
  *within its own memory* (e.g. the buffers used by C ``stdio``, Fortran
  I/O libraries or Python file objects).
* The stacks of all processes and threads.
* Private, modified (copy-on-write) pages of memory-mapped files and of
  shared libraries, which become anonymous once written to.
* Transparent huge pages backing anonymous memory (the ``anon_thp`` field
  is a subset of ``anon``).
* Memory which has been freed by the program but not returned to the
  operating system (e.g. retained by the ``malloc`` implementation for
  reuse).
* The memory of the Cylc job profiler itself and of the job script's shell,
  since these run within the job's cgroup. This is usually small compared
  with the job itself, but may be significant for jobs which use very little
  memory.

**Not included** in Max RSS:

* **Kernel I/O buffers and the page cache** (the ``file`` field in v2, or
  ``total_cache`` in v1). When a job reads or writes files, the kernel
  keeps copies of the data in memory to speed up later access, and holds
  written data in memory until it is flushed to disk (the ``file_dirty``
  and ``file_writeback`` fields). This memory is charged to the job's
  cgroup but is *not* counted in Max RSS. A job which reads or writes large
  files may therefore show a much higher memory usage in tools such as
  ``free`` or in the cgroup's ``memory.current`` file than its Max RSS.
* **Memory-mapped files** (``file_mapped``), including the code of the
  executable and shared libraries, and input files accessed with ``mmap``,
  except for pages which have been modified privately (see above).
* **Shared memory** (``shmem``), i.e. files in ``tmpfs`` filesystems such as
  ``/dev/shm``, System V and POSIX shared memory segments and shared
  anonymous mappings (``mmap(MAP_SHARED | MAP_ANONYMOUS)``). Note that MPI
  libraries commonly use shared memory for communication between processes
  on the same node.
* **Kernel memory** used on behalf of the job, such as kernel stacks
  (``kernel_stack``), page tables (``pagetables``), slab caches
  (``slab``, e.g. the inode and directory entry caches) and network socket
  buffers (``sock``).
* **Swapped-out memory** (``swap`` / ``zswap``), since by definition this is
  no longer resident in RAM.
* Memory which has been allocated (reserved) but never written to. Linux
  only assigns physical memory to a page when it is first used, so a large
  ``malloc`` or ``allocate`` call does not increase RSS until the memory is
  touched.
* Pages from ``hugetlbfs`` (explicitly reserved huge pages), which are
  accounted separately from ``anon``.

.. note::

   Because of the above, Max RSS as reported by Cylc may differ from the
   "maximum resident set size" reported by other tools:

   * Tools such as ``ps``, ``top`` and ``/usr/bin/time`` (and the
     ``ru_maxrss`` value from ``getrusage``) report the RSS of a *single*
     process, and include resident file-backed and shared memory
     (``RssFile`` and ``RssShmem`` in ``/proc/<pid>/status``). They may
     report a higher value than Cylc for a single process, but a lower value
     for a job made up of many processes.
   * Job runner accounting (e.g. Slurm's ``sacct``) may use a different
     method of measuring memory and a different sampling interval.

.. note::

   A job runner's memory limit (``memory.max``) is enforced against the
   cgroup's *total* memory usage (``memory.current``), which includes
   the page cache, shared memory and kernel memory as well as anonymous
   memory. The kernel will normally reclaim clean page cache before killing
   a job, but memory such as ``tmpfs`` files and shared memory segments
   cannot be reclaimed in the same way. A job may therefore run out of
   memory even though its Max RSS is below its memory limit, for example if
   it writes large files to ``/dev/shm``.

.. note::

   Max RSS is a measure of memory *used*, not memory *requested*.
   Job runners such as Slurm and PBS will typically kill a job which
   exceeds its memory request, so it is advisable to request somewhat more
   memory than the Max RSS of previous runs.

When viewing Max RSS in the box plot, the memory limit of the job's cgroup
(the memory allocated to the job, read from ``memory.max``) is shown as a
red line where it is available, making it easy to compare memory usage
against the memory requested. The memory allocation is only available on
systems using cgroups v2.


.. _user-guide.analysis-view.cpu-time:

CPU Time
^^^^^^^^

**CPU time** is the total time that processors spent executing the job's
processes (both user and system time), summed across all processes in the
job's cgroup and across all CPU cores.

It is read from the ``usage_usec`` field of the cgroup's ``cpu.stat`` file
(cgroups v2) or from ``cpuacct.usage`` (cgroups v1) when the job finishes.

CPU time differs from run time (wall-clock time):

* A single-threaded job which spends time waiting (e.g. for I/O) will have a
  CPU time *less* than its run time.
* A parallel or multi-threaded job may have a CPU time *greater* than its
  run time, e.g. a job which keeps 4 cores busy for 10 minutes will have a
  CPU time of approximately 40 minutes.

Comparing CPU time against run time multiplied by the number of cores
requested gives an indication of how efficiently a job uses the cores it
has been allocated.

When the CPU time metric is selected, the **Total CPU Time** consumed by all
jobs shown in the view is displayed at the top of the view.


Displays
--------

The Analysis View offers three displays:

Table
   Shows summary statistics for each task: the mean, minimum, lower quartile
   (Q1), median, upper quartile (Q3) and maximum value of the selected metric
   across all of the task's jobs (plus the standard deviation for the
   timing metrics). If each task has only run once, a single value is shown
   instead.

Box plot
   Shows the distribution of the selected metric for each task as a
   box-and-whisker plot.

Time series
   Plots the selected metric for each job against :term:`cycle point`,
   which is useful for spotting trends or changes in behaviour over time.


.. _user-guide.analysis-view.profiler:

The Cylc Job Profiler
---------------------

Max RSS and CPU time are collected by the Cylc job profiler, a lightweight
process which Cylc starts alongside each :term:`job` (within the
:ref:`job script <JobScripts>`). The profiler:

1. Locates the cgroup that the job is running in (under
   :cylc:conf:`global.cylc[platforms][<platform name>][profiler]cgroups path`).
2. Polls the cgroup's memory statistics every
   :cylc:conf:`global.cylc[platforms][<platform name>][profiler]polling interval`,
   keeping track of the maximum value (the Max RSS).
3. When the job finishes (successfully or otherwise), reads the total CPU time
   and the memory allocation from the cgroup, then sends the results back to
   the :term:`scheduler` as a task message which is stored in the workflow
   database.

The profiler requires a job runner which places each job in its own cgroup,
for example Slurm or PBS when configured to use cgroups. Both
cgroups v1 and cgroups v2 are supported (note the memory allocation is
only available with cgroups v2).

The profiler is configured per :term:`platform` in the
:cylc:conf:`global.cylc[platforms][<platform name>][profiler]` section, see
:ref:`ProfilingConfigurations` for details. It is active by default; to
turn it off for a platform, set
:cylc:conf:`global.cylc[platforms][<platform name>][profiler]activate`
to ``False``.

.. note::

   If a job finishes very quickly, the profiler may not have time to take a
   memory sample, in which case Max RSS and CPU time will be reported as
   zero.

   On platforms where jobs do not run in their own cgroup, the profiler will
   not be able to report meaningful values for individual jobs and should be
   deactivated by setting
   :cylc:conf:`global.cylc[platforms][<platform name>][profiler]activate`
   to ``False``.
