Glossary
========

.. glossary::
   :sorted:

   suite
   Cylc suite
      A Cylc suite is a directory containing a :cylc:conf:`flow.cylc` file
      which contains :term:`graphing<graph>` representing a workflow.

   suite directory
      The suite directory contains all of the configuration for a suite e.g.
      the :cylc:conf:`flow.cylc` file.

      This is the directory which is registered using ``cylc reg``.

      .. note::

         If a suite is written in the ``cylc-run`` directory the suite
         directory is also the :term:`run directory`.

      See also:

      * :term:`run directory`

   graph
      The graph of a :term:`suite<Cylc suite>` refers to the
      :term:`graph strings<graph string>` contained within the
      :cylc:conf:`[scheduling][graph]` section. For example the following is,
      collectively, a graph:

      .. code-block:: cylc

         P1D = foo => bar
         PT12H = baz

      .. digraph:: example
         :align: center

         size = "7,15"

         subgraph cluster_1 {
             label = "2000-01-01T00:00Z"
             style = dashed
             "foo.01T00" [label="foo\n2000-01-01T00:00Z"]
             "bar.01T00" [label="bar\n2000-01-01T00:00Z"]
             "baz.01T00" [label="baz\n2000-01-01T00:00Z"]
         }

         subgraph cluster_2 {
             label = "2000-01-01T12:00Z"
             style = dashed
             "baz.01T12" [label="baz\n2000-01-01T12:00Z"]
         }

         subgraph cluster_3 {
             label = "2000-01-02T00:00Z"
             style = dashed
             "foo.02T00" [label="foo\n2000-01-02T00:00Z"]
             "bar.02T00" [label="bar\n2000-01-02T00:00Z"]
             "baz.02T00" [label="baz\n2000-01-02T00:00Z"]
         }

         "foo.01T00" -> "bar.01T00"
         "foo.02T00" -> "bar.02T00"

   graph string
      A graph string is a collection of dependencies which are placed inside the
      :cylc:conf:`[scheduling][graph]` section e.g:

      .. code-block:: cylc-graph

         foo => bar => baz & pub => qux
         pub => bool

   dependency
      A dependency is a relationship between two :term:`tasks<task>` which
      describes a constraint on one.

      For example the dependency
      ``foo => bar`` means that the :term:`task` ``bar`` is *dependent* on the
      task ``foo``. This means that the task ``bar`` will only run once the
      task ``foo`` has successfully completed.

      See also:

      * :term:`task trigger`
      * :term:`conditional dependency`

   conditional dependency
   conditional trigger
      A conditional dependency is a :term:`dependency` which uses the ``&`` (and)
      or ``|`` (or) operators for example:

      .. code-block:: cylc-graph

         a & (b | c) => d

      See also:

      * :term:`dependency`
      * :term:`task trigger`

   trigger
   task trigger
      :term:`Dependency <dependency>` relationships can be thought of the other
      way around as "triggers".

      For example the dependency ``foo => bar`` could be described in several ways:

      * "``bar`` depends on ``foo``"
      * "``foo`` triggers ``bar``"
      * "``bar`` triggers off of ``foo``"

      In practice a trigger is the left-hand side of a dependency (``foo`` in
      this example).

      See also:

      * :term:`dependency`
      * :term:`qualifier`
      * :term:`family trigger`

   cycle
      In a :term:`cycling suite<cycling>` one cycle is one repetition of the
      workflow.

      For example, in the following workflow each dotted box represents a cycle
      and the :term:`tasks<task>` within it are the :term:`tasks<task>`
      belonging to that cycle. The numbers (i.e. ``1``, ``2``, ``3``) are the
      :term:`cycle points<cycle point>`.

      .. digraph:: example
         :align: center

         size = "3,5"

         subgraph cluster_1 {
             label = "1"
             style = dashed
             "foo.1" [label="foo\n1"]
             "bar.1" [label="bar\n1"]
             "baz.1" [label="baz\n1"]
         }

         subgraph cluster_2 {
             label = "2"
             style = dashed
             "foo.2" [label="foo\n2"]
             "bar.2" [label="bar\n2"]
             "baz.2" [label="baz\n2"]
         }

         subgraph cluster_3 {
             label = "3"
             style = dashed
             "foo.3" [label="foo\n3"]
             "bar.3" [label="bar\n3"]
             "baz.3" [label="baz\n3"]
         }

         "foo.1" -> "bar.1" -> "baz.1"
         "foo.2" -> "bar.2" -> "baz.2"
         "foo.3" -> "bar.3" -> "baz.3"
         "bar.1" -> "bar.2" -> "bar.3"

   cycling
      A cycling :term:`suite<Cylc suite>` is one in which the workflow repeats.

      See also:

      * :term:`cycle`
      * :term:`cycle point`

   cycle point
      A cycle point is the unique label given to a particular :term:`cycle`.
      If the :term:`suite<Cylc suite>` is using :term:`integer cycling` then
      the cycle points will be numbers e.g. ``1``, ``2``, ``3``, etc. If the
      :term:`suite<Cylc suite>` is using :term:`datetime cycling` then the
      labels will be :term:`ISO8601` datetimes e.g. ``2000-01-01T00:00Z``.

      See also:

      * :term:`initial cycle point`
      * :term:`final cycle point`

   initial cycle point
      In a :term:`cycling suite <cycling>` the initial cycle point is the point
      from which cycling begins.
      It is set by :cylc:conf:`[scheduling]initial cycle point`.

      If the initial cycle point were 2000 then the first cycle would
      be on the 1st of January 2000.

      See also:

      * :term:`cycle point`
      * :term:`final cycle point`

   final cycle point
      In a :term:`cycling suite <cycling>` the final cycle point is the point
      at which cycling ends.
      It is set by :cylc:conf:`[scheduling]final cycle point`.

      If the final cycle point were 2001 then the final cycle would be no later
      than the 1st of January 2001.

      See also:

      * :term:`cycle point`
      * :term:`initial cycle point`

   integer cycling
      An integer cycling suite is a :term:`cycling suite<cycling>` which has
      been configured to use integer cycling. When a suite uses integer cycling
      integer :term:`recurrences <recurrence>` may be used in the :term:`graph`,
      e.g. ``P3`` means every third cycle. This is configured by setting
      :cylc:conf:`[scheduling]cycling mode = integer`.

      See also:

      * :ref:`Cylc tutorial <tutorial-integer-cycling>`

   datetime cycling
      A datetime cycling is the default for a :term:`cycling suite<cycling>`.
      When using datetime cycling :term:`cycle points<cycle point>` will be
      :term:`ISO8601 datetimes <ISO8601 datetime>` e.g. ``2000-01-01T00:00Z``
      and ISO8601 :term:`recurrences<recurrence>` can be used e.g. ``P3D``
      means every third day.

      See also:

      * :ref:`Cylc tutorial <tutorial-datetime-cycling>`

   wall-clock time
      In a Cylc suite the wall-clock time refers to the actual time (in the
      real world).

      See also:

      * :term:`datetime cycling`
      * :ref:`Clock Trigger Tutorial <tutorial-cylc-clock-trigger>`

   ISO8601
      ISO8601 is an international standard for writing dates and times which is
      used in Cylc with :term:`datetime cycling`.

      See also:

      * :term:`ISO8601 datetime`
      * :term:`recurrence`
      * `Wikipedia (ISO8601) <https://en.wikipedia.org/wiki/ISO_8601>`_
      * `International Organisation For Standardisation
        <https://www.iso.org/iso-8601-date-and-time-format.html>`_
      * `a summary of the international standard date and time notation
        <http://www.cl.cam.ac.uk/%7Emgk25/iso-time.html>`_

   ISO8601 datetime
      A date-time written in the ISO8601
      format, e.g:

      * ``2000-01-01T00:00Z``: midnight on the 1st of January 2000

      See also:

      * :ref:`Cylc tutorial <tutorial-iso8601-datetimes>`
      * :term:`ISO8601`

   ISO8601 duration
      A duration written in the ISO8601 format e.g:

      * ``PT1H30M``: one hour and thirty minutes.

      See also:

      * :ref:`Cylc tutorial <tutorial-iso8601-durations>`
      * :term:`ISO8601`

   recurrence
      A recurrence is a repeating sequence which may be used to define a
      :term:`cycling suite<cycling>`. Recurrences determine how often something
      repeats and take one of two forms depending on whether the
      :term:`suite<Cylc suite>` is configured to use :term:`integer cycling`
      or :term:`datetime cycling`.

      See also:

      * :term:`integer cycling`
      * :term:`datetime cycling`

   inter-cycle dependency
   inter-cycle trigger
      In a :term:`cycling suite <cycling>` an inter-cycle dependency
      is a :term:`dependency` between two tasks in different cycles.

      For example in the following suite the task ``bar`` is dependent on
      its previous occurrence:

      .. code-block:: cylc

         [scheduling]
             initial cycle point = 1
             cycling mode = integer
             [[graph]]
                 P1 = """
                     foo => bar => baz
                     bar[-P1] => bar
                 """

      .. digraph:: example
         :align: center

         size = "3,5"

         subgraph cluster_1 {
             label = "1"
             style = dashed
             "foo.1" [label="foo\n1"]
             "bar.1" [label="bar\n1"]
             "baz.1" [label="baz\n1"]
         }

         subgraph cluster_2 {
             label = "2"
             style = dashed
             "foo.2" [label="foo\n2"]
             "bar.2" [label="bar\n2"]
             "baz.2" [label="baz\n2"]
         }

         subgraph cluster_3 {
             label = "3"
             style = dashed
             "foo.3" [label="foo\n3"]
             "bar.3" [label="bar\n3"]
             "baz.3" [label="baz\n3"]
         }

         "foo.1" -> "bar.1" -> "baz.1"
         "foo.2" -> "bar.2" -> "baz.2"
         "foo.3" -> "bar.3" -> "baz.3"
         "bar.1" -> "bar.2" -> "bar.3"

   qualifier
      A qualifier is used to determine the :term:`task state` to which a
      :term:`dependency` relates.

      See also:

      * :ref:`Cylc tutorial <tutorial-qualifiers>`
      * :term:`task state`

   task
      A task represents an activity in a workflow. It is a specification of
      that activity consisting of the script or executable to run and certain
      details of the environment it is run in.

      The task specification is used to create a :term:`job` which is executed
      on behalf of the task.

      Tasks submit :term:`jobs <job>` and therefore each :term:`job` belongs
      to one task. Each task can submit multiple :term:`jobs <job>`.

      See also:

      * :term:`job`
      * :term:`job script`

   task state
      During a :term:`task's <task>` life it will proceed through various
      states. These include:

      * waiting
      * running
      * succeeded

      See also:

      * :ref:`Cylc tutorial <tutorial-tasks-and-jobs>`
      * :term:`task`
      * :term:`job`
      * :term:`qualifier`

   run directory
      When a :term:`suite <Cylc suite>` is run a directory is created for all
      of the files generated whilst the suite is running. This is called the
      run directory and typically resides in the ``cylc-run`` directory:

      ``~/cylc-run/<suite-name>``

      .. note::

         If a suite is written in the ``cylc-run`` directory the run
         directory is also the :term:`suite directory`.

      The run directory can be accessed by a running suite using the
      environment variable ``CYLC_SUITE_RUN_DIR``.

      See also:

      * :term:`suite directory`
      * :ref:`Suite Directory Vs Run Directory`
      * :term:`work directory`
      * :term:`share directory`
      * :term:`job log directory`

   work directory
      When Cylc executes a :term:`job` it does so inside the
      :term:`job's <job>` working directory. This directory is created by Cylc
      and lies within the directory tree inside the relevant suite's
      :term:`run directory`.

      .. code-block:: sub

         <run directory>/work/<cycle>/<task-name>

      The location of the work directory can be accessed by a :term:`job` via
      the environment variable ``CYLC_TASK_WORK_DIR``.

      See also:

      * :term:`run directory`
      * :term:`share directory`

   share directory
      The share directory resides within a suite's :term:`run directory`. It
      serves the purpose of providing a storage place for any files which need
      to be shared between different tasks.

      .. code-block:: sub

         <run directory>/share

      The location of the share directory can be accessed by a :term:`job` via
      the environment variable ``CYLC_SUITE_SHARE_DIR``.

      In cycling suites files are typically stored in cycle sub-directories.

      See also:

      * :term:`run directory`
      * :term:`work directory`

   suite log
   suite log directory
      A Cylc suite logs events and other information to the suite log files
      when it runs. There are three log files:

      * ``out`` - the stdout of the suite.
      * ``err`` - the stderr of the suite, which may contain useful debugging
        information in the event of any error(s).
      * ``log`` - a log of suite events, consisting of information about
        user interaction.

      The suite log directory lies within the :term:`run directory`:

      .. code-block:: sub

         <run directory>/log/suite

   job log
   job log directory
      When Cylc executes a :term:`job`, stdout and stderr are redirected to the
      ``job.out`` and ``job.err`` files which are stored in the job log
      directory.

      The job log directory lies within the :term:`run directory`:

      .. code-block:: sub

         <run directory>/log/job/<cycle>/<task-name>/<submission-no>

      Other files stored in the job log directory:

      * ``job``: the :term:`job script`.
      * ``job-activity.log``: a log file containing details of the
        :term:`job's <job>` progress.
      * ``job.status``: a file holding Cylc's most up-to-date
        understanding of the :term:`job's <job>` present status.

   service directory
      This directory is used to store information for internal use by Cylc.

      It is called ``.service`` and is located in the :term:`run directory`, it
      should exist for all registered suites.

   contact file
      The contact file records information about a running suite such as the host it
      is running on, the TCP port(s) it is listening on and the process ID.
      The file is called ``contact`` and lives inside the suite's
      :term:`service directory`.

      The contact file only exists when the suite is running, if you delete the
      contact file, the suite will (after a delay) notice this and shut down.

      .. warning::

         In the event that a suite process dies in an uncontrolled way, for
         example if the process is killed or the host which is running the
         process crashes, the contact file may be erroneously left behind. Some
         Cylc commands will automatically detect such files and remove them,
         otherwise they should be manually removed.

   job
      A job is the realisation of a :term:`task` consisting of a file called
      the :term:`job script` which is executed when the job "runs".

      See also:

      * :term:`task`
      * :term:`job script`

   job script
      A job script is the file containing a bash script which is executed when
      a :term:`job` runs. A task's job script can be found in the
      :term:`job log directory`.

      See also:

      * :term:`task`
      * :term:`job`
      * :term:`job submission number`

   job host
      The job host is the compute platform that a :term:`job` runs on. For
      example ``some-host`` would be the job host for the task ``some-task`` in
      the following suite:

      .. code-block:: cylc

         [runtime]
             [[some-task]]
                 [[[remote]]]
                     host = some-host

   job submission number
      Cylc may run multiple :term:`jobs <job>` per :term:`task` (e.g. if the
      task failed and was re-tried). Each time Cylc runs a :term:`job` it is
      assigned a submission number. The submission number starts at 1,
      incrementing with each submission.

      See also:

      * :term:`job`
      * :term:`job script`

   batch system
      A batch system or job scheduler is a system for submitting
      :term:`jobs <job>` onto a compute platform.

      See also:

      * `Wikipedia (job scheduler)
        <https://en.wikipedia.org/wiki/Job_scheduler>`_
      * :term:`directive`

   directive
      Directives are used by :term:`batch systems <batch system>` to determine
      what a :term:`job's <job>` requirements are, e.g. how much memory
      it requires.

      Directives are set in :cylc:conf:`[runtime][<namespace>][directives]`.

      See also:

      * :term:`batch system`

   scheduler
      When we say that a :term:`suite` is "running" we mean that the cylc
      scheduler is running.

      The scheduler is responsible for running the suite. It submits
      :term:`jobs <job>`, monitors their status and maintains the suite state.

      .. _daemon: https://en.wikipedia.org/wiki/Daemon_(computing)

      By default a scheduler is a `daemon`_ meaning that it runs in
      the background (potentially on another host).

   start
   startup
      When a :term:`suite` starts the Cylc :term:`scheduler` is
      run. This program controls the suite and is what we refer to as
      "running".

      A suite start can be either :term:`cold <cold start>` or :term:`warm <warm
      start>` (cold by default).

      See also:

      * :ref:`Starting Suites`
      * :term:`scheduler`
      * :term:`warm start`
      * :term:`cold start`
      * :term:`shutdown`
      * :term:`restart`
      * :term:`reload`

   cold start
      A cold start is one in which the :term:`suite` :term:`starts <start>`
      from the :term:`initial cycle point`. This is the default behaviour of
      ``cylc run``.

      See also:

      * :term:`warm start`

   warm start
      In a :term:`cycling suite <cycling>`
      a warm start is one in which the :term:`suite` :term:`starts <start>`
      from a :term:`cycle point` after the :term:`initial cycle point`.
      Tasks in cycles before this point as assumed to have succeeded.

      See also:

      * :term:`cold start`

   stop
   shutdown
      When a :term:`suite` is shutdown the :term:`scheduler` is
      stopped. This means that no further :term:`jobs <job>` will be submitted.

      By default Cylc waits for any submitted or running :term:`jobs <job>` to
      complete (either succeed or fail) before shutting down.

      See also:

      * :ref:`Stopping Suites`
      * :term:`start`
      * :term:`restart`
      * :term:`reload`

   restart
      When a :term:`stopped <stop>` :term:`suite` is "restarted" Cylc will pick
      up where it left off. Cylc will detect any :term:`jobs <job>` which
      have changed state (e.g. succeeded) during the period in which the
      :term:`suite` was :term:`shutdown`.

      See also:

      * :ref:`Restarting Suites`
      * :term:`start`
      * :term:`Stop <stop>`
      * :term:`Reload <reload>`

   reload
      Any changes made to the :cylc:conf:`flow.cylc` file whilst the suite is
      running will not have any effect until the suite is either:

      * :term:`Shutdown <shutdown>` and :term:`rerun <start>`
      * :term:`Shutdown <shutdown>` and :term:`restarted <restart>`
      * "Reloaded"

      Reloading does not require the suite to be :term:`shutdown`. When a suite
      is reloaded any currently "active" :term:`tasks <task>` will continue with
      their "pre-reload" configuration, whilst new tasks will use the new
      configuration.

      Reloading changes is safe providing they don't affect the
      :term:`suite's <suite>` :term:`graph`. Changes to the graph have certain
      caveats attached, see the `Cylc User Guide`_ for details.

      See also:

      * :ref:`Reloading Suites`
      * `Cylc User Guide`_

   parameterisation
      Parameterisation is a way to consolidate configuration in the Cylc
      :cylc:conf:`flow.cylc` file by implicitly looping over a set of
      pre-defined variables e.g:

      .. code-block:: cylc

         [cylc]
             [[parameters]]
                 foo = 1..3
         [scheduling]
             [[graph]]
                 R1 = bar<foo> => baz<foo>

      .. minicylc::
         :theme: none

         bar_foo1 => baz_foo1
         bar_foo2 => baz_foo2
         bar_foo3 => baz_foo3

      See also:

      * :ref:`Cylc tutorial <tutorial-cylc-parameterisation>`

   family
      In Cylc a family is a collection of :term:`tasks <task>` which share a
      common configuration and which can be referred to collectively in the
      :term:`graph`.

      By convention families are named in upper case with the exception of the
      special ``root`` family from which all tasks inherit.

      See also:

      * :ref:`Cylc tutorial <tutorial-cylc-families>`
      * :term:`family inheritance`
      * :term:`family trigger`

   family inheritance
      A :term:`task` can be "added" to a :term:`family` by "inheriting" from
      it using the :cylc:conf:`[runtime][<namespace>]inherit` configuration.

      For example the :term:`task` ``task`` "belongs" to the :term:`family`
      ``FAMILY`` in the following snippet:

      .. code-block:: cylc

         [runtime]
             [[FAMILY]]
                 [[[environment]]]
                     FOO = foo
             [[task]]
                 inherit = FAMILY

      A task can inherit from multiple families by writing a comma-separated
      list e.g:

      .. code-block:: cylc

         inherit = foo, bar, baz

      See also:

      * `Cylc User Guide`_
      * :term:`family`
      * :term:`family trigger`

   family trigger
      :term:`Tasks <task>` which "belong" to
      (:term:`inherit <family inheritance>` from) a :term:`family` can be
      referred to collectively in the :term:`graph` using a family trigger.

      A family trigger is written using the name of the family followed by a
      special qualifier i.e. ``FAMILY_NAME:qualifier``. The most commonly used
      qualifiers are:

      ``succeed-all``
          The dependency will only be met when **all** of the tasks in the
          family have **succeeded**.
      ``succeed-any``
          The dependency will be met as soon as **any one** of the tasks in the
          family has **succeeded**.
      ``finish-all``
          The dependency will only be met once **all** of the tasks in the
          family have **finished** (either succeeded or failed).

      See also:

      * `Cylc User Guide`_
      * :term:`family`
      * :term:`task trigger`
      * :term:`dependency`
      * :ref:`Family Trigger Tutorial <tutorial-cylc-family-triggers>`

   message trigger
      A `message trigger` can be used to trigger a dependent
      :term:`task <task>` before the upstream task has completed.

      We can use :term:`custom task outputs <custom task output>` as triggers.

      Messages should be defined in the runtime section of the suite and
      the graph trigger notation refers to each message.

      See also:

      * :ref:`Message Trigger Tutorial <tutorial-cylc-message-triggers>`
      * :term:`custom task output`

   custom task output
      A `custom task output` is a user-defined message sent from the
      :term:`job` to the workflow server.
      These can be used as :term:`message triggers <message trigger>`.

      See also:

      * `Cylc User Guide`_
      * :term:`message trigger`

   stalled suite
   stalled state
      If Cylc is unable to proceed running a workflow due to unmet dependencies
      the suite is said to be *stalled*.

      This usually happens because of a task failure as in the following
      diagram:

      .. digraph:: Example
         :align: center

         foo [style="filled" color="#ada5a5"]
         bar [style="filled" color="#ff0000" fontcolor="white"]
         baz [color="#88c6ff"]

         foo -> bar -> baz

      In this example the task ``bar`` has failed meaning that ``baz`` is
      unable to run as its dependency (``bar:succeed``) has not been met.

      When a Cylc detects that a suite has stalled an email will be sent to the
      user. Human interaction is required to escape a stalled state.

   suicide trigger
      Suicide triggers remove :term:`tasks <task>` from the :term:`graph`.

      This allows Cylc to dynamically alter the graph based on events in the
      workflow.

      .. warning::

         Since Cylc 8 suicide triggers have been surpassed by
         :term:`graph branching` which provides a simpler, superior
         solution.

      Suicide triggers are denoted using an exclamation mark, ``!foo`` would
      mean "remove the task foo from this cycle".

      .. code-block:: cylc-graph

         a => b

         # suicide trigger which removes the task "b" if "a" fails
         # NOTE: since Cylc 8 this suicide trigger is not necessary
         a:fail => !b

   branching
   graph branching
      Cylc handles :term:`graphs <graph>` in an event-driven manner which means
      that a workflow can follow different paths in different eventualities.
      This is called "branching".

      For example the following workflow follows one of two possible paths
      depending on the outcome of task ``b``:

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

      See also:

      * :ref:`Graph Branching`
