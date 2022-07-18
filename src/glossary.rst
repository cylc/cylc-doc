.. Glossary Conventions - for consistency

   1) Linking to other glossary items in the text:
      - there's no need to link multiple instances of the same term in the same
        paragraph
      - but duplicate links may be desirable if further apart

   2) Examples can be given but should be brief and on point

   3) "seealso" blocks should contain, in order:
      - config reference links
      - glossary items not linked in the main text
      - documentation links (e.g. User Guide)
      - external web site links

      To avoid unnecessarily long lists and repetition don't duplicate glossary
      links from the main text

   4) To avoid surprising users by jumping out of the page, non-glossary links
      should:
      - primarily be in the "seealso" list
      - not look like another glossary term,
        e.g. :ref:`Cylc User Guide <blah>` not just :ref:`blah`.

     5) Use singular rather than plural terms for glossary definitions (e.g. task rather than tasks).


.. TODO Add more user guide and config links to all items, where appropriate.

Glossary
========

.. glossary::
   :sorted:

   validation
   workflow validation
      Validation parses a ``flow.cylc`` file to report any illegal items,
      syntax errors, deprecation warnings, and other problems.

      It is done automatically at start up, and should be done manually with
      the ``cylc validate`` command after making changes.


   retry
   task retry
   try number
      Tasks can be configured to retry automatically on failure, one or more
      times. They return to the ``waiting`` state with a :term:`clock trigger`
      to delay the retry, and only go to the ``failed`` :term:`state <task
      state>` once the final try fails.

      The task try number increments with every automatic retry, and is
      passed to the job environment as ``$CYLC_TASK_TRY_NUMBER``.

      .. seealso::

         * :ref:`Cylc User Guide <TaskRetries>`


   submit number
   task submit number
      Every time a task re-runs, whether by automatic :term:`retry` or manual
      triggering, its submit number increments. It is passed to
      the job environment as ``$CYLC_TASK_SUBMIT_NUMBER``.

      Submit number also appears in the job log path so that job log files
      don't get overwritten.


   window
   n-window
   active window
   workflow window
   active task pool
      This is a :term:`graph`-based window or view of the workflow at runtime,
      including tasks out to ``n`` graph edges from current :term:`active
      tasks<active task>`. The *active window* is ``n=0``.

      .. seealso::

         * :ref:`Cylc User Guide <n-window>`


   artificial dependency
      An artificial :term:`dependency` in the :term:`graph` does not reflect
      real dependence between the tasks involved. This can sometimes be
      useful but should be avoided if possible. Artificial dependencies muddy
      the real dependencies of the workflow and they may unnecessarily
      constrain the scheduler.

      In the following :term:`cycling` workflow, if the task ``foo`` does not
      actually depend on any real outputs of ``baz`` in the previous cycle,
      then the intercycle dependence is artificial.

      .. code-block:: cylc-graph

         P1 = """
            foo => bar => baz
            baz[-P1] => foo
         """


   workflow
   cylc workflow
      A workflow is a collection of :term:`tasks <task>` with
      :term:`dependencies <dependency>` between them that govern the order in
      which they can run.

      Cylc workflows are defined in :cylc:conf:`flow.cylc` files.

      For example, the following workflow represents the beer brewing process:

      .. code-block:: cylc
         :caption: flow.cylc

         [scheduling]
             cycling mode = integer
             initial cycle point = 1
             [[graph]]
                 # repeat this for each batch
                 P1 = """
                     # the stages of brewing in the order they must occur in:
                     malt => mash => sparge => boil => chill => ferment => rack
                     # finish the sparge of one batch before starting the next:
                     sparge[-P1] => mash
                 """

      .. admonition:: Cylc 7
         :class: tip

         In Cylc 7 and earlier, "workflows" were referred to as "suites".


   workflow name
      The workflow name is a path relative to the cylc-run directory which
      contains one or more workflow :term:`run directories <run directory>`.

      Task jobs can get the workflow name from ``$CYLC_WORKFLOW_NAME`` in their
      runtime environment.

      Unlike :term:`workflow id` the name is not always a unique identifier. In
      the example below ``run1`` and ``run2`` would both have the same name,
      ``my_workflow``:

      .. code-block:: bash

         `- my_workflow
           |- runN
           |- run1
           `- run2

      .. note::
         If you are not using named or numbered runs, the workflow name will be
         the same as :term:`workflow id`.


   active
   active task
      An active task is a task in the submitted or running state.


   active-waiting
   active-waiting task
      An active-waiting task is a task in the :term:`scheduler's <scheduler>`
      ``n=0`` :term:`active window` that is ready to run according to its task
      prerequisites, but is still waiting on a limiting mechanism such as a
      :term:`clock trigger`, task :term:`hold`, or :term:`internal queue`.


   external trigger
   xtrigger
      External triggers allow :term:`tasks <task>` in the :term:`graph` to
      depend on external events, such as a file being delivered to some
      location, or a database being updated in some way.

      The :term:`scheduler` can repeatedly call a user-supplied Python function
      to check that the external event has occurred.

      Cylc has a built in external trigger for triggering off of events in
      other workflows.

      .. seealso::

         * :cylc:conf:`[scheduling][xtriggers]`
         * :term:`clock trigger`
         * :ref:`Cylc User Guide <Section External Triggers>`
         * :ref:`Cylc User Guide <Built-in Workflow State Triggers>`


   queue
   internal queue
      Internal queues (so called to distinguish them from external batch
      queueing systems) allow you to limit how many :term:`tasks <task>` can be
      active (submitted or running) at once, across defined groups of tasks.

      Use queues prevent large or busy workflows from swamping their
      :term:`job platforms <job platform>` with too many jobs at once.

      .. seealso::

         * :cylc:conf:`[scheduling][queues]`
         * :ref:`Cylc User Guide <InternalQueues>`


   workflow id
      A workflow can be uniquely identified by the relative path between the :term:`cylc-run directory`
      (``~/cylc-run``) and its :term:`run directory`.

      This ID is used on the command line and in the GUI, to target the right
      workflow.

      For example, the ID of the workflow in ``~/cylc-run/foo/bar/run1``
      is ``foo/bar/run1``.

      Unlike :term:`workflow name` the ID is always a unique identifier. In the
      example below each run has a different ID despite sharing the same
      :term:`workflow name` (``my_workflow``).

      .. code-block:: bash

         `- my_workflow
           |- runN
           |- run1      # CYLC_WORKFLOW_ID = my_workflow/run1
           `- run2      # CYLC_WORKFLOW_ID = my_workflow/run2


   graph
      A workflow graph is defined by one or more :term:`graph strings<graph string>`
      under the :cylc:conf:`[scheduling][graph]` section of a :term:`workflow<Cylc
      workflow>` definition.

      For example, the following is, collectively, a graph:

      .. code-block:: cylc-graph

         P1D = foo => bar
         PT12H = baz

      .. digraph:: Example
         :align: center

         size = "7,15"

         subgraph cluster_1 {
             label = "2000-01-01T00:00Z"
             style = dashed
             "01T00/foo" [label="foo\n2000-01-01T00:00Z"]
             "01T00/bar" [label="bar\n2000-01-01T00:00Z"]
             "01T00/baz" [label="baz\n2000-01-01T00:00Z"]
         }

         subgraph cluster_2 {
             label = "2000-01-01T12:00Z"
             style = dashed
             "b01T12/az" [label="baz\n2000-01-01T12:00Z"]
         }

         subgraph cluster_3 {
             label = "2000-01-02T00:00Z"
             style = dashed
             "02T00/foo" [label="foo\n2000-01-02T00:00Z"]
             "02T00/bar" [label="bar\n2000-01-02T00:00Z"]
             "02T00/baz" [label="baz\n2000-01-02T00:00Z"]
         }

         "01T00/foo" -> "01T00/bar"
         "02T00/foo" -> "02T00/bar"


   graph string
      A graph string is a collection of task :term:`dependencies <dependency>`
      in the :cylc:conf:`[scheduling][graph]` section of a workflow definition,
      with an associated recurrence that defines its sequence of cycle points.

      The example below shows one graph string in a datetime cycling workflow,
      with a daily cycle point sequence:

      .. code-block:: cylc-graph

         R/^/P1D = """
            foo => bar => baz & pub => qux
            pub => bool
         """


   cycle
      In a :term:`cycling workflow`, cycles are repetitions of a :term:`graph
      string`. Each cycle is identified by a :term:`cycle point`. The sequence
      of cycle points is defined by the graph string's :term:`recurrence`
      pattern.

      This defines the structure of the :term:`graph`. At runtime, however,
      Cylc does not impose a global loop over cycles. Each individual task,
      with its own cycle point, advances according to its own
      :term:`dependencies <dependency>`.

      For example, in the following workflow each dotted box represents a cycle
      and the :term:`tasks<task>` within it are the :term:`tasks<task>`
      belonging to that cycle. The numbers (i.e. ``1``, ``2``, ``3``) are the
      :term:`cycle points <cycle point>`.

      .. digraph:: Example
         :align: center

         size = "3,5"

         subgraph cluster_1 {
             label = "1"
             style = dashed
             "1/foo" [label="foo\n1"]
             "1/bar" [label="bar\n1"]
             "1/baz" [label="baz\n1"]
         }

         subgraph cluster_2 {
             label = "2"
             style = dashed
             "2/foo" [label="foo\n2"]
             "2/bar" [label="bar\n2"]
             "2/baz" [label="baz\n2"]
         }

         subgraph cluster_3 {
             label = "3"
             style = dashed
             "3/foo" [label="foo\n3"]
             "3/bar" [label="bar\n3"]
             "3/baz" [label="baz\n3"]
         }

         "1/foo" -> "1/bar" -> "1/baz"
         "2/foo" -> "2/bar" -> "2/baz"
         "3/foo" -> "3/bar" -> "3/baz"
         "1/bar" -> "2/bar" -> "3/bar"



      .. seealso::

         * :ref:`tutorial-integer-cycling`
         * :ref:`tutorial-datetime-cycling`


   cycling
   cycling workflow
      A cycling :term:`workflow` in Cylc is defined by a graph of
      repeating tasks with individual :term:`cycle points <cycle point>`.

      .. seealso::

         * :term:`cycle`


   cycle point
      The unique label given to tasks that belong to a particular :term:`cycle`.
      For :term:`integer cycling` these will be integers, e.g. ``1``, ``2``,
      ``3``, etc.
      For :term:`datetime cycling` they will be :term:`ISO 8601` datetimes,
      e.g. ``2000-01-01T00:00Z``.

      .. seealso::

         * :term:`initial cycle point`
         * :term:`final cycle point`
         * :term:`start cycle point`


   cycle point time zone
      The time zone used for task :term:`cycle points <cycle point>`.

      .. seealso::

         * :cylc:conf:`flow.cylc[scheduler]cycle point time zone`


   initial cycle point
      In a :term:`cycling workflow <cycling>` the initial cycle point is the
      first :term:`cycle point` in the :term:`graph`.

      .. seealso::

         * :cylc:conf:`[scheduling]initial cycle point`.
         * :term:`start cycle point`


   final cycle point
      In a :term:`cycling workflow <cycling>` the final cycle point, if there
      is one, is the last :term:`cycle point` in the :term:`graph`.

      .. seealso::

         * :cylc:conf:`[scheduling]final cycle point`.
         * :term:`stop cycle point`


   start cycle point
      In a :term:`cycling workflow <cycling>` the start cycle point is the
      :term:`cycle point` where the :term:`scheduler` :term:`starts <start>`
      running the workflow.

      This may be at or after the :term:`initial cycle point`.

      .. seealso::

         * :term:`stop cycle point`
         * :ref:`Cylc User Guide <start_stop_cycle_point>`


   stop cycle point
      The stop cycle point is the :term:`cycle point` where :term:`scheduler`
      stops running the workflow and :term:`shuts down <shutdown>`.

      This may be at or before the :term:`final cycle point`.

      .. seealso::

         * :term:`start cycle point`
         * :ref:`Cylc User Guide <start_stop_cycle_point>`


   integer cycling
      An integer :term:`cycling workflow` uses integer :term:`cycle points
      <cycle point>` and :term:`recurrences <recurrence>` (e.g. ``P3`` means
      every third cycle).

      .. seealso::

         * :cylc:conf:`[scheduling]cycling mode`
         * :term:`datetime cycling`
         * :ref:`Cylc tutorial <tutorial-integer-cycling>`


   datetime cycling
      A datetime :term:`cycling` workflow uses
      :term:`ISO 8601 datetime` :term:`cycle points <cycle point>`
      (e.g.  ``2000-01-01T00:00Z``) and :term:`recurrences <recurrence>`
      (e.g. ``P3D`` means every third day).

      .. seealso::

         * :cylc:conf:`[scheduling]cycling mode`
         * :term:`integer cycling`
         * :ref:`Cylc tutorial <tutorial-datetime-cycling>`


   wallclock time
      The actual time (in the real world).

      .. seealso::

         * :term:`datetime cycling`
         * :term:`clock trigger`


   ISO 8601
   ISO8601
      ISO 8601 is an international standard for writing datetimes, durations,
      and :term:`recurrences <recurrence>` (sequences of datetimes). Cylc uses
      ISO 8601 for :term:`datetime cycling`.

      .. seealso::

         * :term:`ISO 8601 datetime`
         * `Wikipedia (ISO 8601) <https://en.wikipedia.org/wiki/ISO_8601>`_
         * `International Organisation For Standardisation
           <https://www.iso.org/iso-8601-date-and-time-format.html>`_
         * `a summary of the international standard date and time notation
           <http://www.cl.cam.ac.uk/%7Emgk25/iso-time.html>`_


   ISO 8601 datetime
   ISO8601 datetime
      A datetime written in the :term:`ISO 8601` format, e.g:

      * ``2000-01-01T00:00Z``: midnight on the 1st of January 2000, UTC.

      .. seealso::

         * :ref:`Cylc tutorial <tutorial-iso8601-datetimes>`


   ISO 8601 duration
   ISO8601 duration
      A duration written in the ISO 8601 format e.g:

      * ``PT1H30M``: one hour and thirty minutes.

      .. seealso::

         * :term:`ISO 8601`
         * :ref:`Cylc tutorial <tutorial-iso8601-durations>`


   recurrence
      In a :term:`cycling workflow<cycling>` a recurrence determines the
      sequence of cycle points given to task instances that appear in the
      associated :term:`graph string`.

      Recurrences for :term:`datetime cycling` are based on the :term:`ISO8601`
      standard. Those for :term:`integer cycling` are designed to have similar
      syntax, but are much simpler.


   exact datetime unit
      An exact datetime unit is any unit of a datetime that has a fixed
      duration, which does not depend on its position in the calendar.
      In Cylc, the following are exact units:

      * second: SI base unit
      * minute: 60 seconds
      * hour: 60 minutes
      * day: 24 hours
      * week: 7 days

      .. note::
         Although the :term:`ISO 8601` standard specifies that weeks and days
         are :term:`inexact <inexact datetime unit>` due to the possibility of
         daylight saving time, leap seconds etc., they are always exact in
         Cylc because workflows always maintain the same time zone, and leap
         seconds are not supported.

      .. seealso::

         * :term:`inexact datetime unit`


   inexact datetime unit
   nominal duration
      An inexact datetime unit is any unit of a datetime that does not have
      a fixed duration; it instead depends on its position in the calendar.
      In Cylc, the following are inexact units (when using the Gregorian
      calendar):

      * year: either 365 or 366 days depending on whether it is a leap year
      * month: between 28 - 31 days depending on the specific month and year

      .. seealso::

         * :term:`exact datetime unit`


   clock trigger
      Clock triggers connect cycle points to the :term:`wallclock time`, in
      :term:`datetime cycling` workflows. Tasks that depend on a clock trigger
      will not trigger until the wallclock time is equal to their cycle point
      plus or minus some offset.

      .. seealso::

         * :ref:`Cylc User Guide <Built-in Clock Triggers>`
         * :ref:`Cylc Tutorial <tutorial-cylc-clock-trigger>`


   intercycle dependence
   intercycle dependency
   intercycle trigger
      In a :term:`cycling workflow <cycling>`, intercycle dependence refers to
      a :term:`task` depending on other tasks at different cycle points.

      For example, in the following workflow the task ``bar`` depends on
      its own previous instance:

      .. code-block:: cylc

         [scheduling]
             initial cycle point = 1
             cycling mode = integer
             [[graph]]
                 P1 = """
                     foo => bar => baz
                     bar[-P1] => bar
                 """

      .. digraph:: Example
         :align: center

         size = "3,5"

         subgraph cluster_1 {
             label = "1"
             style = dashed
             "1/foo" [label="foo\n1"]
             "1/bar" [label="bar\n1"]
             "1/baz" [label="baz\n1"]
         }

         subgraph cluster_2 {
             label = "2"
             style = dashed
             "2/foo" [label="foo\n2"]
             "2/bar" [label="bar\n2"]
             "2/baz" [label="baz\n2"]
         }

         subgraph cluster_3 {
             label = "3"
             style = dashed
             "3/foo" [label="foo\n3"]
             "3/bar" [label="bar\n3"]
             "3/baz" [label="baz\n3"]
         }

         "1/foo" -> "1/bar" -> "1/baz"
         "2/foo" -> "2/bar" -> "2/baz"
         "3/foo" -> "3/bar" -> "3/baz"
         "1/bar" -> "2/bar" -> "3/bar"


   qualifier
      A qualifier is what follows :term:`task` or family :term:`family` names
      after a colon ``:`` in :term:`triggers <trigger>`, in the :term:`graph`,
      to specify exactly which :term:`task outputs <task output>` must be
      completed for the :term:`dependency` to be satisfied.

      For example, in ``foo:start => bar``, the ``:start`` qualifier means that
      the ``started`` output of task ``foo`` must be completed to satisfy the
      dependency.

      .. seealso::

         * :term:`task triggers <task trigger>`
         * :term:`family triggers <family trigger>`
         * :ref:`Cylc tutorial <tutorial-qualifiers>`


   future trigger
      A future trigger makes one task depend on another with a later
      :term:`cycle point`.

      Here, ``1/bar`` triggers off ``2/foo``; and ``2/bar`` off of
      ``3/foo``; and so on:

      .. code-block:: cylc

         [scheduling]
             initial cycle point = 1
             cycling mode = integer
             [[graph]]
                 P1 = "foo[+P1] => bar"

      .. seealso::

         * :term:`intercycle trigger`


   task
      A task represents an activity in a :term:`workflow`. The workflow
      definition specifies how tasks depends on other tasks, what they
      should do, how and where to run them, and details of their
      runtime environment.

      Task definitions are used to create a :term:`job script` that is
      executed as a :term:`job` on behalf of the task.

      Tasks submit :term:`jobs <job>`. Each :term:`job` belongs to one task,
      but one task can submit multiple :term:`jobs <job>`.


   task state
      A :term:`task` progresses through a series of states in its lifetime.
      These include the ``submitted`` state after :term:`job` submission;
      ``running`` after execution commences, and ``succeeded`` after
      successful job execution.

      .. seealso::

         * :ref:`Cylc User Guide <task-job-states>`
         * :ref:`Cylc tutorial <tutorial-tasks-and-jobs>`


   implicit task
      Implicit tasks are :term:`tasks <task>` which are not defined in
      the :cylc:conf:`[runtime]` section.

      Like regular tasks they :term:`inherit <family inheritance>` from the ``root``
      :term:`family`.

      Implicit tasks submit real jobs that just exit without doing anything
      useful. They may be useful placeholders during workflow development but
      are not allowed by default because they can be created accidentally by
      simply misspelling a task name in the graph or under ``[runtime]``.

      Here ``bar`` is implicit:

      .. code-block:: cylc

         [scheduling]
             [[graph]]
                 R1 = foo & bar
         [runtime]
             [[foo]]
         # eof

      .. seealso::

         * :cylc:conf:`flow.cylc[scheduler]allow implicit tasks`
         * :ref:`Cylc User Guide <ImplicitTasks>`

      .. admonition:: Cylc 7
         :class: tip

         In Cylc 7 and earlier, implicit tasks were known as "naked dummy tasks".


   work directory
      Cylc executes task :term:`jobs <job>` inside a job-specific working
      directory, automatically created under the workflow :term:`run
      directory`.

      .. code-block:: sub

         <run-directory>/work/<cycle-point>/<task-name>

      Task jobs can get their own work directory path at runtime from
      the ``CYLC_TASK_WORK_DIR`` environment variable or the Posix ``pwd``
      command.

      .. seealso::

         * :term:`run directory`
         * :term:`share directory`


   share directory
      Cylc automatically creates a share directory inside the workflow
      :term:`run directory` as a place to store files that need to be
      shared between tasks.

      .. code-block:: sub

         <run-directory>/share

      Task jobs can get their own share directory path at runtime from
      the ``CYLC_WORKFLOW_SHARE_DIR`` environment variable.

      In cycling workflows files are typically stored in cycle point
      sub-directories of the share directory.

      .. seealso::

         * :term:`run directory`
         * :term:`work directory`


   workflow log
   scheduler log
   workflow log directory
      At runtime the scheduler logs timestamped events and other information to
      files under the workflow :term:`run directory`. These logs take the format
      <log-number>-<start/restart>-<start-number>.log, with the latest log being
      automatically symlinked to ``<run-directory>/log/scheduler/log``

      .. code-block:: sub

         <run-directory>/log/scheduler/

      You can print the scheduler log at the terminal with ``cylc cat-log
      <workflow-name>``.


   job log
   job log directory
      Task :term:`job` log files are stored in job specific log directories
      under the workflow :term:`run directory`. These include:

      ``job``
         The task :term:`job script`.
      ``job.out``
         Job stdout.
      ``job.err``
         Job stderr.
      ``job.status``
         Job status data in case of lost contact with the scheduler.
      ``job-activity.log``
         Job data logged by the scheduler, rather than
         the job itself, such as output from the job submission command.
      ``job.xtrace``
         Debugging information from Bash captured when Cylc is run in
         ``--debug`` mode.

      .. code-block:: sub

         <run-directory>/log/job/<cycle-point>/<task-name>/<job-submit-num>


      You can print task job logs at the terminal with ``cylc cat-log
      <workflow-name> <task-id>``. By default this prints ``job.out``.
      There are command options to select the other logs.


   service directory
      The hidden service directory, under the workflow :term:`run directory`,
      stores information for internal use by Cylc. It is created at
      :term:`install` time.

      .. code-block:: sub

         <run-directory>/.service/


   contact file
      The contact file, in the :term:`service directory`, records information
      about a running :term:`scheduler` such as host, TCP port, and process ID.
      It is read by Cylc client commands so they can target the right scheduler.

      The contact file is created at scheduler startup and removed on clean
      shutdown. If you delete it, the scheduler will (after a delay) notice
      this and shut down.

      .. code-block:: sub

         <run-directory>/.service/contact

      .. warning::
         If the scheduler dies in an uncontrolled way, for example if the
         process is killed or the host goes down, the contact file may be
         left behind. Some Cylc commands automatically detect these files
         and remove them, otherwise they should be manually removed.


   job
      Jobs are real processes that perform :term:`tasks <task>` in a
      :term:`workflow`. In Cylc, they are implemented by :term:`job scripts
      <job script>` prepared by the :term:`scheduler`.


   job script
      A Cylc job script is a file containing bash code to implement a task
      definition in a workflow. It prepared and submitted to run by the
      :term:`scheduler` when the task is ready to run.

      Job scripts can be found in the task :term:`job log directory`.


   job host
      A job host is a compute resource that a :term:`job` runs on. For
      example ``node_1`` would be one of two possible job hosts on the
      :term:`platform` ``my_hpc`` for the task ``solver`` in the
      following workflow:

      .. code-block:: cylc
         :caption: global.cylc

         [platforms]
             [[my_hpc]]
                 hosts = node_1, node_2
                 job runner = slurm

      .. code-block:: cylc
         :caption: flow.cylc

         [runtime]
             [[solver]]
                 platform = my_hpc


   job submission number
      A single :term:`task` may run multiple :term:`jobs <job>` as a result of
      automatic :term:`retries <retry>` or manually retriggering.
      The job submission number is incremented each time, starting from 1.


   job runner
      A job runner is a system for submitting task :term:`jobs <job>` to run on
      a :term:`job platform <platform>`.

      Cylc supports various job runners, from direct background process
      execution to HPC batch queueing systems like PBS and Slurm (these are
      also known as *job schedulers* and *resource managers*).

      Job runners are configured on a per-platform basis in ``global.cylc``.

      .. seealso::

         * :cylc:conf:`global.cylc[platforms][<platform name>]job runner`.
         * :term:`directive`
         * `Wikipedia (job scheduler) <https://en.wikipedia.org/wiki/Job_scheduler>`_

      .. admonition:: Cylc 7
         :class: tip

         In Cylc 7 and earlier, job runners were referred to as "batch systems".


   directive
      Directives request task :term:`jobs <job>` resources such as memory and
      node count from external :term:`job runners <job runner>`. They are job
      runner-specific.

      .. seealso::

         * :cylc:conf:`[runtime][<namespace>][directives]`


   platform
   job platform
      A platform for running Cylc task :term:`jobs <job>` is primarily defined
      by the combination of a :term:`job runner` and a group of :term:`hosts
      <job host>` that share a file system.

      For example ``my_hpc`` could be the platform for the task ``solver``
      in the following workflow:

      .. code-block:: cylc
         :caption: Global configuration (``global.cylc``)

         [platforms]
             [[my_hpc]]
                 hosts = node_1, node_2
                 job runner = slurm

      .. code-block:: cylc
         :caption: Workflow configuration (``flow.cylc``)

         [runtime]
             [[solver]]
                 platform = my_hpc

      .. seealso::

         * :term:`platform group`


   platform group
      A set of :term:`platforms <platform>` grouped under a common name.

      Platforms are configured by :cylc:conf:`global.cylc[platform groups]`.


   scheduler
      The Cylc scheduler is a program responsible for managing a single
      Cylc :term:`workflow`. It determines when each :term:`tasks <task>` is
      ready to run, submits its :term:`jobs <job>` to selected job runners,
      tracks job status, maintains the workflow state, and listens for queries
      and commands from the user.

      By default, Cylc schedulers run as daemons (and potentially on a remote
      host) so they won't be killed if you log out.

      .. seealso::

         * `Wikipedia: daemon <https://en.wikipedia.org/wiki/Daemon_(computing)>`_

      .. admonition:: Cylc 7
         :class: tip

         In Cylc 7 and earlier, schedulers were known as "suite daemons".


   start
   startup
      This refers to starting a new instance of the Cylc :term:`scheduler`
      program to manage a particular :term:`workflow`. This can be from
      scratch, for installed workflows that haven't run previously, or to
      restart one that shut down prior to :term:`completion <workflow completion>`.

      .. seealso::

         * :term:`cold start`
         * :term:`warm start`
         * :term:`start task`
         * :term:`restart`
         * :term:`reload`
         * :term:`shutdown`


   cold start
      A cold start is when the :term:`scheduler` :term:`starts <startup>` a
      :term:`workflow` at the beginning of :term:`graph`. In a :term:`cycling
      workflow` this is determined by the :term:`initial cycle point`.

      This is the default behaviour of ``cylc play`` for an installed workflow
      that hasn't run yet.

      To satisfy unbounded :term:`intercycle dependence` in the graph, tasks
      prior to the initial cycle point are treated as if they have succeeded.

      .. seealso::

         * :cylc:conf:`[scheduling]initial cycle point`
         * :term:`warm start`
         * :term:`start task`
         * :term:`restart`
         * :term:`shutdown`


   warm start
      A warm start is when the :term:`scheduler` :term:`starts <start>` a
      :term:`cycling workflow` running from a :term:`start cycle point` after
      the :term:`initial cycle point`.

      To satisfy unbounded :term:`intercycle dependence` in the graph, tasks
      prior to the start cycle point are treated as if they have succeeded.

      .. seealso::

         * :term:`cold start`
         * :term:`start task`
         * :term:`restart`
         * :term:`shutdown`


   start task
      A start task is :term:`task` in the :term:`graph` from which the
      :term:`scheduler` :term:`starts <start>` running a :term:`workflow` from
      scratch.

      Earlier tasks depended on by start tasks are treated as if they have
      succeeded.

      .. seealso::

         * :term:`cold start`
         * :term:`warm start`
         * :term:`start cycle point`
         * :term:`shutdown`

      .. admonition:: Cylc 7
         :class: tip

         Cylc 7 and earlier did not have the capability to start from any task
         in the graph.


   cylc-run directory
      This refers to the top level directory for :term:`installed <workflow
      installation>` workflows: ``~/cylc-run``.

      Cylc can be configured to symlink cylc-run sub-directories to
      other locations.

      .. seealso::

         * :cylc:conf:`global.cylc[install][symlink dirs]`.
         * :term:`run directory`

      .. caution::

         The cylc-run directory should not be confused with specific
         :term:`workflow run directories <run directory>` below it.

   install
   installation
   workflow installation
      The ``cylc install`` command installs workflow :term:`source files
      <source directory>` into a new :term:`run directory` under the
      :term:`cylc-run directory`.

      .. seealso::

         * :term:`reinstall`


   reinstall
   reinstallation
      The ``cylc reinstall`` command reinstalls workflow :term:`source files
      <source directory>` into an existing :term:`run directory` under the
      :term:`cylc-run directory`.

      .. seealso::

         * :term:`install`


   source directory
   source workflow
      A source directory is any location where :term:`workflows <workflow>` are
      written and stored in preparation for installation with ``cylc install``
      or reinstallation with ``cylc reinstall``.

      These locations are configurable. The default is ``~/cylc-src``.

      .. seealso::

         * :term:`run directory`
         * :cylc:conf:`global.cylc[install]source dirs`
         * :ref:`Installing-workflows`


   run directory
   workflow run directory
      This is a location under the :term:`cylc-run directory` that contains the
      :term:`installed <install>` configuration used to run a :term:`workflow`.

      At runtime, task :term:`jobs <job>` can get their workflow run
      directory from the environment variable ``CYLC_WORKFLOW_RUN_DIR``.

      .. seealso::

         * :term:`source directory`
         * :term:`work directory`
         * :term:`share directory`
         * :term:`job log directory`


   play
      The ``cylc play`` command runs an instance of the :term:`scheduler`
      program to :term:`start` or :term:`restart` a :term:`workflow`.

      You can :term:`play`, :term:`pause` and :term:`stop` a :term:`workflow`,
      Cylc will always carry on where it left off.


   pause
      When a :term:`workflow` is "paused" the :term:`scheduler` is still
      running but it will not submit any new jobs.

      This can be useful if you want to make a change to a running workflow.

      Pause a workflow with ``cylc pause`` and resume it with ``cylc play``.

      .. seealso::

         * :term:`play`
         * :term:`stop`
         * :term:`hold`


   stop
   shutdown
      A :term:`scheduler` can shut down on request, or automatically on
      :term:`workflow completion`. The :term:`workflow` is then stopped and no
      further :term:`jobs <job>` will be submitted.

      By default, the scheduler waits for any submitted or running task
      :term:`jobs <job>` to finish (either succeed or fail) before shutting
      down.

      .. seealso::

         * :term:`play`
         * :term:`pause`
         * :term:`start`
         * :term:`restart`
         * :term:`reload`
         * :ref:`Tutorial <tutorial.start_stop_restart>`.


   restart
      When a :term:`stopped <stop>` :term:`workflow` is :term:`played <play>`
      again, the :term:`scheduler` picks up where it left off rather than
      starting again from scratch. It also detects any orphaned :term:`jobs
      <job>` that changed state (e.g. succeeded) while the system was down.

      Changes made to the :term:`installed <install>` :cylc:conf:`flow.cylc`
      file will be picked at restart. We recommend that changes are
      :term:`reinstalled <reinstall>` from the workflow :term:`source
      directory` before restart, rather than made by editing the installed
      files directly.

      .. seealso::

         * :term:`start`
         * :term:`stop`
         * :term:`reload`
         * :ref:`Tutorial <tutorial.start_stop_restart>`.


   reload
      :term:`Schedulers <scheduler>` can reload their :term:`workflow`
      configuration from the :term:`installed <install>` :cylc:conf:`flow.cylc`
      file, to pick up changes made at runtime.

      We recommend that changes are :term:`reinstalled <reinstall>` from the
      workflow :term:`source directory` before reload, rather than made by
      editing the installed files directly.

      :ref:`RemoteInit` will be redone for each job platform, when the first job is submitted there after a reload.

      Any :term:`task` that is active at reload will continue with its
      pre-reload configuration. It's next instance (at the next cycle point)
      will adopt the new configuration.

      Reloading changes is safe providing they don't affect the
      :term:`workflow's <workflow>` :term:`graph`. Changes to the graph have
      certain caveats attached, see the
      :ref:`Cylc User Guide <Reloading The Workflow Configuration At Runtime>`
      for details.

      .. seealso::

         * :term:`restart`


   hold
   held task
   hold after cycle point
      A :term:`task` held with ``cylc hold`` will not submit its :term:`jobs
      <job>` when ready to run.

      It is also possible to set a "hold after cycle point"; all tasks after
      this cycle point will be held.

      .. note::
         :term:`Workflows <workflow>` can be :term:`paused <pause>` with ``cylc
         pause``, and unpaused/resumed with ``cylc play``.

         :term:`Tasks <task>` can be :term:`held <hold>` with ``cylc hold`` and
         :term:`released <release>` with ``cylc release``.

         When a workflow is resumed, any held tasks remain held.


   release
      :term:`Held tasks <hold>` can be released with ``cylc release``,
      allowing submission of task :term:`jobs <job>` once again.

      It is also possible to remove the "hold after cycle point" if set,
      using ``cylc release --all``. This will also release all held tasks.


   task parameters
   parameterisation
      Task parameterisation is one way of consolidating configuration in the
      :cylc:conf:`flow.cylc` file. Cylc implicitly loops over ranges or lists
      of pre-defined parameters to automatically generate sets of similar
      tasks.

      Other ways of consolidating configuration include :term:`runtime
      inheritance` and templating with :ref:`Jinja2 <Jinja>` or :ref:`Empy
      <User Guide Empy>`.

      .. code-block:: cylc

         [task parameters]
             m = 1..3
         [scheduling]
             [[graph]]
                 R1 = bar<m> => baz<m>

      .. minicylc::
         :theme: none

         bar_m1 => baz_m1
         bar_m2 => baz_m2
         bar_m3 => baz_m3

      .. seealso::

         * :ref:`Cylc User Guide <User Guide Param>`
         * :ref:`Cylc tutorial <tutorial-cylc-parameterisation>`


   family
      In Cylc a family is a collection of :term:`tasks <task>` that share
      common configuration and which can be referred to collectively in the
      :term:`graph`.

      By convention, family names are upper case, with the exception of the
      special ``root`` family that all tasks inherit from.

      .. seealso::

         * :term:`family inheritance`
         * :term:`family trigger`
         * :ref:`Cylc User Guide <User Guide Runtime>`
         * :ref:`Cylc tutorial <tutorial-cylc-families>`


   runtime inheritance
   family inheritance
      A :term:`task` is a member of a :term:`family` if it inherits the
      family configuration via :cylc:conf:`[runtime][<namespace>]inherit`.

      For example the :term:`task` ``cheddar`` "belongs" to the :term:`family`
      ``CHEESE`` in the following snippet:

      .. code-block:: cylc

         [runtime]
             [[CHEESE]]
                 [[[environment]]]
                     COLOR = yellow
             [[cheddar]]
                 inherit = FAMILY

      Families can also inherit from other families. All tasks implicitly
      inherit from a special ``root`` family at the base of the inheritance
      hierarchy.

      Tasks can inherit from multiple families at once using a comma-separated
      list:

      .. code-block:: cylc

         inherit = foo, bar, baz

      .. seealso::

         * :term:`family trigger`
         * :ref:`Cylc User Guide <User Guide Runtime>`
         * :ref:`Cylc Tutorial <tutorial-inheritance>`


   family trigger
      :term:`Tasks <task>` that belong to a :term:`family` can be
      referred to collectively in the :term:`graph` using a family
      :term:`trigger`.

      Family triggers take the form ``family-name:qualifier``, where
      the :term:`qualifier` describes the collective state of member tasks
      needed for the dependency to be met. Some commonly used qualifiers
      are:

      ``succeed-all``
          All members succeeded.
      ``succeed-any``
          Any one member succeeded.
      ``fail-all``
          All members failed.
      ``finish-all``
          All members finished (succeeded or failed).

      .. seealso::

         * :term:`dependency`
         * :ref:`Cylc Tutorial <tutorial-cylc-family-triggers>`
         * :ref:`Cylc User Guide <FamilyTriggers>`


   standard output
     Every :term:`task` has a set of standard :term:`outputs <task output>`
     that trigger :term:`task state` changes:

      - ``:submitted``, or ``:submit-failed``
      - ``:started``
      - ``:succeeded``, or ``:failed``


   task output
      Task outputs mark the progression of a :term:`task` from waiting (for
      prerequisites to be satisfied) through to success or failure at run
      time. Downstream tasks can trigger off of the outputs of other tasks, as
      determined by the :term:`graph`.

      Outputs are written as ``task-name:output`` in the :term:`graph`, and can
      be :term:`expected <expected output>` or :term:`optional <optional output>`.

      Tasks may have :term:`custom outputs <custom output>` as well as
      :term:`standard outputs <standard output>`.

      Here the task ``bar`` depends on the standard ``:started`` output of
      ``foo``:

      .. code-block:: cylc-graph

         foo:started => bar

      The standard ``:succeeded`` output is usually implicit:

      .. code-block:: cylc-graph

         foo => bar  # means foo:succeeded => bar


   dependence
   dependency
      Dependencies in the :term:`graph` show how :term:`tasks <task>` depend on
      some combination of the :term:`outputs <task output>` of other tasks.

      For example, in the following dependency the task ``baz`` depends on both
      ``foo`` and ``bar`` succeeding:

      .. code-block:: cylc-graph

         foo & bar => baz

      .. seealso::

          * :term:`task trigger`
          * :term:`conditional dependence`
          * :term:`intercycle dependence`


   conditional dependence
   conditional dependency
   conditional trigger
      Conditional :term:`dependence` is when a :term:`task` depends on a
      combination of multiple upstream :term:`task outputs <task output>`.

      .. code-block:: cylc-graph

         a & (b:fail | c) => d

      The left hand side of a conditional dependency can be called a
      conditional :term:`trigger`.


   trigger
   task trigger
      A trigger is the left-hand side of a :term:`dependency` in the
      :term:`graph`. It defines the combination of :term:`task outputs <task
      output>` that must be completed before downstream tasks can run.

      In this example, the task ``bar`` can be said to trigger off of
      completion of the ``foo:started`` output:

      .. code-block:: cylc-graph

         foo:started => bar

      Triggers can be based on :term:`standard <standard output>` or
      :term:`custom <custom output>` task outputs. In the latter case they
      are known as :term:`message triggers <message trigger>`.


   message trigger
      A message trigger is a :term:`trigger` based on a
      :term:`custom task output <custom output>`. The task :term:`job` must
      send a user-defined message to the scheduler to complete the output.

      For brevity, the trigger in the :term:`graph` uses the output name, not
      the full message:

      .. code-block:: cylc

         [scheduling]
             [[graph]]
                 R1 = """
                    foo:out1 => proc-out-1
                    foo:out2 => proc-out-2
                 """
         [runtime]
             [[foo]]
                 script = """
                     # ...
                     cylc message "Output 1 completed"
                     # ...
                     cylc message "Output 2 completed"
                 """
                 [[[outputs]]]
                     # output name = output message
                     out1 = "Output 1 completed"
                     out2 = "Output 2 completed"

      However, if you don't need a descriptive message for the workflow
      log, you can make the message the same as its name:

      .. code-block:: cylc

         [[[outputs]]]
             out1 = out1


   custom output
      A custom task output is a user-defined :term:`task output` that marks
      an event runtime event between task :term:`job` start and finish. To
      complete a custom output, the job must send a message defined in the
      :cylc:conf:`flow.cylc` file to the :term:`scheduler`.

      Triggers based on custom outputs are called :term:`message triggers
      <message trigger>`.

      .. code-block:: cylc

         [runtime]
             [[foo]]
                 [[[outputs]]]
                     # output name = output message
                     out1 = "Output 1 completed"
                     out2 = "Output 2 completed"

      .. seealso::

         * :term:`standard output`
         * :ref:`Cylc Tutorial <tutorial-cylc-message-triggers>`
         * :ref:`Cylc User Guide <MessageTriggers>`


   optional output
      Optional :term:`task outputs <task output>` are marked with a question
      mark in the :term:`graph`, e.g. ``foo:x?``, or ``foo:fail?``,  or
      ``foo?`` (short for ``foo:succeed?``). The may or may not be completed at
      runtime. Optional outputs are primarily used for :term:`graph branching`.

      .. seealso::

         * :term:`expected output`
         * :ref:`Cylc User Guide <User Guide Optional Outputs>`


   expected output
      Task outputs that are not marked as :term:`optional <optional output>`
      in the :term:`graph` are expected to be completed at runtime. If not, the
      :term:`scheduler` retains the task as :term:`incomplete` pending user
      intervention.

      .. seealso::

         * :ref:`Cylc User Guide <expected outputs>`


   incomplete
   incomplete task
      Incomplete tasks are :term:`tasks <task>` that finish (succeed or fail)
      without completing all :term:`expected outputs <expected output>`. They
      are retained by the :term:`scheduler` in the :term:`n=0 window
      <n-window>` pending user intervention, and will cause a :term:`stall`
      if there are no more tasks to run.

      .. seealso::

         * :term:`optional output`
         * :ref:`Cylc User Guide <incomplete tasks>`


   stall
   stalled workflow
   stalled state
      If there are no more tasks to run according to the :term:`graph`, but
      :term:`incomplete tasks <incomplete task>` are present, the
      :term:`scheduler` will stall and stay up for a time instead of
      shutting down with the workflow :term:`complete <workflow completion>`.

      Stalls are usually caused by unexpected task failures:

      .. digraph:: Example
         :align: center

         foo [style="filled" color="#ada5a5"]
         bar [style="filled" color="#ff0000" fontcolor="white"]
         baz [color="#88c6ff"]

         foo -> bar -> baz

      In this example the task ``bar`` has failed, so  that ``baz`` cannot
      run, but ``bar:fail`` was not marked as an :term:`optional output`.

      User intervention is required to fix a stall, e.g. by retriggering
      incomplete tasks after fixing the problems that caused them to fail.


   suicide trigger
      Suicide triggers remove :term:`tasks <task>` from the :term:`scheduler's
      <scheduler>` active (:term:`n=0 <n-window>`) window at runtime.

      They are denoted by exclamation marks, and are triggered like normal
      dependencies. For instance, the following suicide trigger will remove the
      task ``bar`` from the active window if ``foo`` succeeds:

      .. code-block:: cylc-graph

         foo => ! bar

      .. warning::
         Suicide triggers are not needed in Cylc 8 for :term:`graph branching`.
         They are retained for backward compatibility and rare edge cases.

      .. seealso::

         * :ref:`Cylc User Guide <SuicideTriggers>`

   branching
   graph branching
      Cylc handles workflow :term:`graphs <graph>` in an event-driven way.
      It can automatically follow different paths depending on events at
      runtime. This relies on :term:`optional outputs <optional output>` and is
      called *branching*.

      For example, the following workflow follows one of two possible paths
      depending on the outcome of task ``b``:

      .. code-block:: cylc-graph

         # the success branch
         a => b? => c
         # the fail branch
         b:fail? => r
         # joining the two branches together
         c | r => d

      .. digraph:: example
         :align: center

         subgraph cluster_success {
            label = ":succeed"
            color = "green"
            fontcolor = "green"
            style = "dashed"

            c
         }

         subgraph cluster_failure {
            label = ":fail"
            color = "red"
            fontcolor = "red"
            style = "dashed"

            r
         }

         a -> b -> c -> d
         b -> r -> d

      .. seealso::

         * :term:`optional output`
         * :ref:`Cylc User Guide <Graph Branching>`


   flow
      A flow is a self-propagating run through the a Cylc :term:`workflow`
      :term:`graph` starting from some initial task or tasks.

      Cylc :term:`schedulers <scheduler>` can manage multiple flows at once.

      Flows are identified by a :term:`flow number`. The original flow
      started automatically by ``cylc play`` has flow number ``1``.

      .. seealso::
         * :ref:`user-guide-reflow`


   flow number
      Flow numbers are integers passed down from parent task to child task in
      the :term:`graph` as a flow progresses, to identify which :term:`flow`
      (or flows) the tasks belong to. They are passed to job environments as
      ``$CYLC_TASK_FLOW_NUMBERS``.


   flow front
      Active (submitted or running) tasks, i.e. tasks in the ``n=0``
      :term:`active window`, with a common :term:`flow number` comprise the
      active front of that flow.


   flow merge
      When a :term:`flow` tries to spawn a child task and finds an instance
      with the same task ID already exists in the ``n=0`` :term:`active
      window`, the one active task will carry both flow numbers forward.


   event
      An event is a milestone in the lifecycle of a :term:`workflow` or
      :term:`task` at which the :term:`scheduler` provides a hook for
      attaching :term:`event handlers <event handler>`.

      Workflow events include :term:`startup`, :term:`stall`, and
      :term:`shutdown`.

      Task events include :term:`task state` changes, to ``running`` or
      ``failed``, for example, or when the scheduler receivers CRITICAL or
      WARNING messages from a task :term:`job`.


   .. TODO cylc-flow cfgspec/workflow.py references "event handlers" plural

   handler
   event handler
   event handlers
      An event handler is a user-defined executable that the
      :term:`scheduler` runs when selected :term:`task` or :term:`workflow`
      :term:`events <event>` occur.

      Use-cases include:

      - Send an email message.
      - Run a Cylc command.
      - Run *any* user-specified script or command.

      .. seealso::

         - :cylc:conf:`task events <[runtime][<namespace>][events]>`
         - :cylc:conf:`workflow events <[scheduler][events]>`
         - :ref:`Cylc User Guide <EventHandling>`


   runahead limit
   runahead
      In a :term:`cycling workflow`, the runahead limit holds the fastest tasks
      back if they get too far ahead of the slowest ones. The default limit is
      5 cycles.

      .. seealso::

         * :cylc:conf:`[scheduling]runahead limit`
         * :ref:`Runahead Limiting`


   workflow completion
      A workflow is deemed complete if there are no more tasks to run,
      according to the graph, and there are no :term:`incomplete task
      <incomplete task>` present.

      If the workflow is complete, the scheduler will automatically :term:`shut
      down <shutdown>`.

      If there are no more tasks to run, but there are incomplete tasks
      present, the scheduler will :term:`stall` rather than shut down.
