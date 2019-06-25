.. _CommandReference:

Command Reference
=================

.. _help:

Help
----

.. code-block:: none

      Cylc ("silk") is a workflow engine for orchestrating complex
   *suites* of inter-dependent distributed cycling (repeating) tasks, as well as
   ordinary non-cycling workflows.
   For detailed documentation see the Cylc User Guide (cylc doc --help).
   
   Version 8.0a0
   
   USAGE:
     % cylc -V,--version,version           # print cylc version
     % cylc version --long                 # print cylc version and path
     % cylc help,--help,-h,?               # print this help page
   
     % cylc help CATEGORY                  # print help by category
     % cylc CATEGORY help                  # (ditto)
     % cylc help [CATEGORY] COMMAND        # print command help
     % cylc [CATEGORY] COMMAND --help      # (ditto)
     % cylc COMMAND --help                 # (ditto)
   
     % cylc COMMAND [options] SUITE [arguments]
     % cylc COMMAND [options] SUITE TASK [arguments]
   
   Commands can be abbreviated as long as there is no ambiguity in
   the abbreviated command:
   
     % cylc trigger SUITE TASK             # trigger TASK in SUITE
     % cylc trig SUITE TASK                # ditto
     % cylc tr SUITE TASK                  # ditto
   
     % cylc get                            # Error: ambiguous command
   
   TASK IDENTIFICATION IN CYLC SUITES
     Tasks are identified by NAME.CYCLE_POINT where POINT is either a
     date-time or an integer.
     Date-time cycle points are in an ISO 8601 date-time format, typically
     CCYYMMDDThhmm followed by a time zone - e.g. 20101225T0600Z.
     Integer cycle points (including those for one-off suites) are integers
     - just '1' for one-off suites.
   
   HOW TO DRILL DOWN TO COMMAND USAGE HELP:
     % cylc help           # list all available categories (this page)
     % cylc help prep      # list commands in category 'preparation'
     % cylc help prep edit # command usage help for 'cylc [prep] edit'
   
   Command CATEGORIES:
     all ........... The complete command set.
     preparation ... Suite editing, validation, visualization, etc.
     information ... Interrogate suite definitions and running suites.
     discovery ..... Detect running suites.
     control ....... Suite start up, monitoring, and control.
     utility ....... Cycle arithmetic and templating, etc.
     task .......... The task messaging interface.
     hook .......... Suite and task event hook scripts.
     admin ......... Cylc installation, testing, and example suites.

Command Categories
------------------


.. _command-cat-admin:

admin
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: none

      CATEGORY: admin - Cylc installation, testing, and example suites.
   
   HELP: cylc [admin] COMMAND help,--help
     You can abbreviate admin and COMMAND.
     The category admin may be omitted.
   
   COMMANDS:
     check-software ... Check required software is installed


.. _command-cat-all:

all
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: none

      CATEGORY: all - The complete command set.
   
   HELP: cylc [all] COMMAND help,--help
     You can abbreviate all and COMMAND.
     The category all may be omitted.
   
   COMMANDS:
     broadcast|bcast ............................. Change suite [runtime] settings on the fly
     cat-log|log ................................. Print various suite and task log files
     check-software .............................. Check required software is installed
     check-triggering ............................ A suite shutdown event hook for cylc testing
     check-versions .............................. Compare cylc versions on task host accounts
     checkpoint .................................. Tell suite to checkpoint its current state
     client ...................................... (Internal) Invoke suite runtime client, expect JSON input
     cycle-point|cyclepoint|datetime|cycletime ... Cycle point arithmetic and filename templating
     diff|compare ................................ Compare two suite definitions and print differences
     documentation|browse ........................ Display cylc documentation (User Guide etc.)
     dump ........................................ Print the state of tasks in a running suite
     edit ........................................ Edit suite definitions, optionally inlined
     ext-trigger|external-trigger ................ Report an external trigger event to a suite
     extract-pkg-resources ....................... Extract cylc.flow library package resources
     function-run ................................ (Internal) Run a function in the process pool
     get-directory ............................... Retrieve suite source directory paths
     get-host-metrics ............................ Print localhost metric data
     get-site-config|get-global-config ........... Print site/user configuration items
     get-suite-config|get-config ................. Print suite configuration items
     get-suite-contact|get-contact ............... Print contact information of a suite server program
     get-suite-version|get-cylc-version .......... Print cylc version of a suite server program
     graph ....................................... Plot suite dependency graphs and runtime hierarchies
     graph-diff .................................. Compare two suite dependencies or runtime hierarchies
     hold ........................................ Hold (pause) suites or individual tasks
     insert ...................................... Insert tasks into a running suite
     jobs-kill ................................... (Internal) Kill task jobs
     jobs-poll ................................... (Internal) Retrieve status for task jobs
     jobs-submit ................................. (Internal) Submit task jobs
     jobscript ................................... Generate a task job script and print it to stdout
     kill ........................................ Kill submitted or running tasks
     list|ls ..................................... List suite tasks and family namespaces
     ls-checkpoints .............................. Display task pool etc at given events
     message|task-message ........................ Report task messages
     monitor ..................................... An in-terminal suite monitor
     nudge ....................................... Cause the cylc task processing loop to be invoked
     ping ........................................ Check that a suite is running
     poll ........................................ Poll submitted or running tasks
     print ....................................... Print registered suites
     register .................................... Register a suite for use
     release|unhold .............................. Release (unpause) suites or individual tasks
     reload ...................................... Reload the suite definition at run time
     remote-init ................................. (Internal) Initialise a task remote
     remote-tidy ................................. (Internal) Tidy a task remote
     remove ...................................... Remove tasks from a running suite
     report-timings .............................. Generate a report on task timing data
     reset ....................................... Force one or more tasks to change state
     restart ..................................... Restart a suite from a previous state
     run|start ................................... Start a suite at a given cycle point
     scan ........................................ Scan a host for running suites
     scp-transfer ................................ Scp-based file transfer for cylc suites
     search|grep ................................. Search in suite definitions
     set-verbosity ............................... Change a running suite's logging verbosity
     show ........................................ Print task state (prerequisites and outputs etc.)
     spawn ....................................... Force one or more tasks to spawn their successors
     stop|shutdown ............................... Shut down running suites
     submit|single ............................... Run a single task just as its parent suite would
     suite-state ................................. Query the task states in a suite
     trigger ..................................... Manually trigger or re-trigger a task
     validate .................................... Parse and validate suite definitions
     view ........................................ View suite definitions, inlined and Jinja2 processed


.. _command-cat-control:

control
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: none

      CATEGORY: control - Suite start up, monitoring, and control.
   
   HELP: cylc [control] COMMAND help,--help
     You can abbreviate control and COMMAND.
     The category control may be omitted.
   
   COMMANDS:
     broadcast|bcast ................ Change suite [runtime] settings on the fly
     checkpoint ..................... Tell suite to checkpoint its current state
     client ......................... (Internal) Invoke suite runtime client, expect JSON input
     ext-trigger|external-trigger ... Report an external trigger event to a suite
     hold ........................... Hold (pause) suites or individual tasks
     insert ......................... Insert tasks into a running suite
     kill ........................... Kill submitted or running tasks
     nudge .......................... Cause the cylc task processing loop to be invoked
     poll ........................... Poll submitted or running tasks
     release|unhold ................. Release (unpause) suites or individual tasks
     reload ......................... Reload the suite definition at run time
     remove ......................... Remove tasks from a running suite
     reset .......................... Force one or more tasks to change state
     restart ........................ Restart a suite from a previous state
     run|start ...................... Start a suite at a given cycle point
     set-verbosity .................. Change a running suite's logging verbosity
     spawn .......................... Force one or more tasks to spawn their successors
     stop|shutdown .................. Shut down running suites
     trigger ........................ Manually trigger or re-trigger a task


.. _command-cat-discovery:

discovery
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: none

      CATEGORY: discovery - Detect running suites.
   
   HELP: cylc [discovery] COMMAND help,--help
     You can abbreviate discovery and COMMAND.
     The category discovery may be omitted.
   
   COMMANDS:
     check-versions ... Compare cylc versions on task host accounts
     ping ............. Check that a suite is running
     scan ............. Scan a host for running suites


.. _command-cat-hook:

hook
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: none

      CATEGORY: hook - Suite and task event hook scripts.
   
   HELP: cylc [hook] COMMAND help,--help
     You can abbreviate hook and COMMAND.
     The category hook may be omitted.
   
   COMMANDS:
     check-triggering ... A suite shutdown event hook for cylc testing


.. _command-cat-information:

information
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: none

      CATEGORY: information - Interrogate suite definitions and running suites.
   
   HELP: cylc [information] COMMAND help,--help
     You can abbreviate information and COMMAND.
     The category information may be omitted.
   
   COMMANDS:
     cat-log|log .......................... Print various suite and task log files
     documentation|browse ................. Display cylc documentation (User Guide etc.)
     dump ................................. Print the state of tasks in a running suite
     extract-pkg-resources ................ Extract cylc.flow library package resources
     get-host-metrics ..................... Print localhost metric data
     get-site-config|get-global-config .... Print site/user configuration items
     get-suite-config|get-config .......... Print suite configuration items
     get-suite-contact|get-contact ........ Print contact information of a suite server program
     get-suite-version|get-cylc-version ... Print cylc version of a suite server program
     list|ls .............................. List suite tasks and family namespaces
     monitor .............................. An in-terminal suite monitor
     show ................................. Print task state (prerequisites and outputs etc.)


.. _command-cat-preparation:

preparation
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: none

      CATEGORY: preparation - Suite editing, validation, visualization, etc.
   
   HELP: cylc [preparation] COMMAND help,--help
     You can abbreviate preparation and COMMAND.
     The category preparation may be omitted.
   
   COMMANDS:
     diff|compare .... Compare two suite definitions and print differences
     edit ............ Edit suite definitions, optionally inlined
     get-directory ... Retrieve suite source directory paths
     graph ........... Plot suite dependency graphs and runtime hierarchies
     graph-diff ...... Compare two suite dependencies or runtime hierarchies
     jobscript ....... Generate a task job script and print it to stdout
     list|ls ......... List suite tasks and family namespaces
     print ........... Print registered suites
     register ........ Register a suite for use
     search|grep ..... Search in suite definitions
     validate ........ Parse and validate suite definitions
     view ............ View suite definitions, inlined and Jinja2 processed


.. _command-cat-task:

task
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: none

      CATEGORY: task - The task messaging interface.
   
   HELP: cylc [task] COMMAND help,--help
     You can abbreviate task and COMMAND.
     The category task may be omitted.
   
   COMMANDS:
     jobs-kill .............. (Internal) Kill task jobs
     jobs-poll .............. (Internal) Retrieve status for task jobs
     jobs-submit ............ (Internal) Submit task jobs
     message|task-message ... Report task messages
     remote-init ............ (Internal) Initialise a task remote
     remote-tidy ............ (Internal) Tidy a task remote
     submit|single .......... Run a single task just as its parent suite would


.. _command-cat-utility:

utility
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: none

      CATEGORY: utility - Cycle arithmetic and templating, etc.
   
   HELP: cylc [utility] COMMAND help,--help
     You can abbreviate utility and COMMAND.
     The category utility may be omitted.
   
   COMMANDS:
     cycle-point|cyclepoint|datetime|cycletime ... Cycle point arithmetic and filename templating
     function-run ................................ (Internal) Run a function in the process pool
     ls-checkpoints .............................. Display task pool etc at given events
     report-timings .............................. Generate a report on task timing data
     scp-transfer ................................ Scp-based file transfer for cylc suites
     suite-state ................................. Query the task states in a suite


Commands
--------


.. _command-broadcast:

broadcast
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: none

      Usage: cylc [control] broadcast|bcast [OPTIONS] REG
   
   Override [runtime] config in targeted namespaces in a running suite.
   
   Uses for broadcast include making temporary changes to task behaviour,
   and task-to-downstream-task communication via environment variables.
   
   A broadcast can target any [runtime] namespace for all cycles or for a
   specific cycle.  If a task is affected by specific-cycle and all-cycle
   broadcasts at once, the specific takes precedence. If a task is affected
   by broadcasts to multiple ancestor namespaces, the result is determined
   by normal [runtime] inheritance. In other words, it follows this order:
   
   all:root -> all:FAM -> all:task -> tag:root -> tag:FAM -> tag:task
   
   Broadcasts persist, even across suite restarts, until they expire when
   their target cycle point is older than the oldest current in the suite,
   or until they are explicitly cancelled with this command.  All-cycle
   broadcasts do not expire.
   
   For each task the final effect of all broadcasts to all namespaces is
   computed on the fly just prior to job submission.  The --cancel and
   --clear options simply cancel (remove) active broadcasts, they do not
   act directly on the final task-level result. Consequently, for example,
   you cannot broadcast to "all cycles except Tn" with an all-cycle
   broadcast followed by a cancel to Tn (there is no direct broadcast to Tn
   to cancel); and you cannot broadcast to "all members of FAMILY except
   member_n" with a general broadcast to FAMILY followed by a cancel to
   member_n (there is no direct broadcast to member_n to cancel).
   
   To broadcast a variable to all tasks (quote items with internal spaces):
     % cylc broadcast -s "[environment]VERSE = the quick brown fox" REG
   To do the same with a file:
     % cat >'broadcast.rc' <<'__RC__'
     % [environment]
     %     VERSE = the quick brown fox
     % __RC__
     % cylc broadcast -F 'broadcast.rc' REG
   To cancel the same broadcast:
     % cylc broadcast --cancel "[environment]VERSE" REG
   If -F FILE was used, the same file can be used to cancel the broadcast:
     % cylc broadcast -G 'broadcast.rc' REG
   
   Use -d/--display to see active broadcasts. Multiple --cancel options or
   multiple --set and --set-file options can be used on the same command line.
   Multiple --set and --set-file options are cumulative.
   
   The --set-file=FILE option can be used when broadcasting multiple values, or
   when the value contains newline or other metacharacters. If FILE is "-", read
   from standard input.
   
   Broadcast cannot change [runtime] inheritance.
   
   See also 'cylc reload' - reload a modified suite definition at run time.
   
   Arguments:
      REG               Suite name
   
   Options:
     -h, --help            show this help message and exit
     -p CYCLE_POINT, --point=CYCLE_POINT
                           Target cycle point. More than one can be added.
                           Defaults to '*' with --set and --cancel, and nothing
                           with --clear.
     -n NAME, --namespace=NAME
                           Target namespace. Defaults to 'root' with --set and
                           --cancel, and nothing with --clear.
     -s [SEC]ITEM=VALUE, --set=[SEC]ITEM=VALUE
                           A [runtime] config item and value to broadcast.
     -F FILE, --set-file=FILE, --file=FILE
                           File with config to broadcast. Can be used multiple
                           times.
     -c [SEC]ITEM, --cancel=[SEC]ITEM
                           An item-specific broadcast to cancel.
     -G FILE, --cancel-file=FILE
                           File with broadcasts to cancel. Can be used multiple
                           times.
     -C, --clear           Cancel all broadcasts, or with -p/--point,
                           -n/--namespace, cancel all broadcasts to targeted
                           namespaces and/or cycle points. Use "-C -p '*'" to
                           cancel all all-cycle broadcasts without canceling all
                           specific-cycle broadcasts.
     -e CYCLE_POINT, --expire=CYCLE_POINT
                           Cancel any broadcasts that target cycle points earlier
                           than, but not inclusive of, CYCLE_POINT.
     -d, --display         Display active broadcasts.
     -k TASKID, --display-task=TASKID
                           Print active broadcasts for a given task
                           (NAME.CYCLE_POINT).
     -b, --box             Use unicode box characters with -d, -k.
     -r, --raw             With -d/--display or -k/--display-task, write out the
                           broadcast config structure in raw Python form.
     --user=USER           Other user account name. This results in command
                           reinvocation on the remote account.
     --host=HOST           Other host name. This results in command reinvocation
                           on the remote account.
     -v, --verbose         Verbose output mode.
     --debug               Output developer information and show exception
                           tracebacks.
     --port=INT            Suite port number on the suite host. NOTE: this is
                           retrieved automatically if non-interactive ssh is
                           configured to the suite host.
     --use-ssh             Use ssh to re-invoke the command on the suite host.
     --ssh-cylc=SSH_CYLC   Location of cylc executable on remote ssh commands.
     --no-login            Do not use a login shell to run remote ssh commands.
                           The default is to use a login shell.
     --comms-timeout=SEC, --pyro-timeout=SEC
                           Set a timeout for network connections to the running
                           suite. The default is no timeout. For task messaging
                           connections see site/user config file documentation.
     -f, --force           Do not ask for confirmation before acting. Note that
                           it is not necessary to use this option if interactive
                           command prompts have been disabled in the site/user
                           config files.


.. _command-cat-log:

cat-log
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: none

      Usage: cylc [info] cat-log|log [OPTIONS] REG [TASK-ID] 
   
   Print, view-in-editor, or tail-follow content, print path, or list directory,
   of local or remote task job and suite server logs. Batch-system view commands
   (e.g. 'qcat') are used if defined in global config and the job is running.
   
   For standard log types use the short-cut option argument or full filename (e.g.
   for job stdout "-f o" or "-f job.out" will do).
   
   To list the local job log directory of a remote task, choose "-m l" (directory
   list mode) and a local file, e.g. "-f a" (job-activity.log).
   
   If remote job logs are retrieved to the suite host on completion (global config
   '[JOB-HOST]retrieve job logs = True') and the job is not currently running, the
   local (retrieved) log will be accessed unless '-o/--force-remote' is used.
   
   Custom job logs (written to $CYLC_TASK_LOG_DIR on the job host) can be 
   listed in 'extra log files' in the suite definition. The file
   name must be given here, but can be discovered with '--mode=l' (list-dir).
   
   The correct cycle point format of the suite must be for task job logs.
   
   Note the --host/user options are not needed to view remote job logs. They are
   the general command reinvocation options for sites using ssh-based task
   messaging.
   
   Arguments:
      REG                     Suite name
      [TASK-ID]               Task ID
   
   Options:
     -h, --help            show this help message and exit
     -f LOG, --file=LOG      Job log: j(job), o(job.out), e(job.err), a(job-
                           activity.log), s(job.status), x(job.xtrace), d(job-
                           edit.diff); default o(out).  Or <filename> for custom
                           (and standard) job logs.
     -m MODE, --mode=MODE  Mode: p(print), l(list-dir), d(print-dir), c(cat),
                           t(tail), e(edit). Default c(cat).
     -r INT, --rotation=INT
                           Suite log integer rotation number. 0 for current, 1
                           for next oldest, etc.
     -o, --force-remote    View remote logs remotely even if they have been
                           retrieved to the suite host (default False).
     -s INT, -t INT, --submit-number=INT, --try-number=INT
                           Job submit number (default=NN, i.e. latest).
     -g, --geditor         edit mode: use your configured GUI editor.
     --remote-arg=REMOTE_ARGS
                           (for internal use: continue processing on job host)
     --user=USER           Other user account name. This results in command
                           reinvocation on the remote account.
     --host=HOST           Other host name. This results in command reinvocation
                           on the remote account.
     -v, --verbose         Verbose output mode.
     --debug               Output developer information and show exception
                           tracebacks.


.. _command-check-software:

check-software
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: none

      cylc [admin] check-software [MODULES]
   
   Check for Cylc external software dependencies, including minimum versions.
   
   With no arguments, prints a table of results for all core & optional external
   module requirements, grouped by functionality. With module argument(s),
   provides an exit status for the collective result of checks on those modules.
   
   Arguments:
       [MODULES]   Modules to include in the software check, which returns a
                   zero ('pass') or non-zero ('fail') exit status, where the
                   integer is equivalent to the number of modules failing. Run
                   the bare check-software command to view the full list of
                   valid module arguments (lower-case equivalents accepted).
   


.. _command-check-triggering:

check-triggering
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: none

      cylc [hook] check-triggering ARGS
   
   This is a cylc shutdown event handler that compares the newly generated
   suite log with a previously generated reference log "reference.log"
   stored in the suite definition directory. Currently it just compares
   runtime triggering information, disregarding event order and timing, and
   fails the suite if there is any difference. This should be sufficient to
   verify correct scheduling of any suite that is not affected by different
   run-to-run conditional triggering.
   
   1) run your suite with "cylc run --generate-reference-log" to generate
   the reference log with resolved triggering information. Check manually
   that the reference run was correct.
   2) run reference tests with "cylc run --reference-test" - this
   automatically sets the shutdown event handler along with a suite timeout
   and "abort if shutdown handler fails", "abort on timeout", and "abort if
   any task fails".
   
   Reference tests can use any run mode:
    * simulation mode - tests that scheduling is equivalent to the reference
    * dummy mode - also tests that task hosting, job submission, job script
      evaluation, and cylc messaging are not broken.
    * live mode - tests everything (but takes longer with real tasks!)
   
    If any task fails, or if cylc itself fails, or if triggering is not
    equivalent to the reference run, the test will abort with non-zero exit
    status - so reference tests can be used as automated tests to check
    that changes to cylc have not broken your suites.


.. _command-check-versions:

check-versions
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: none

      Usage: cylc [discovery] check-versions [OPTIONS] SUITE 
   
   Check the version of cylc invoked on each of SUITE's task host accounts when
   CYLC_VERSION is set to *the version running this command line tool*.
   Different versions are reported but are not considered an error unless the
   -e|--error option is specified, because different cylc versions from 6.0.0
   onward should at least be backward compatible.
   
   It is recommended that cylc versions be installed in parallel and access
   configured via the cylc version wrapper as described in the cylc INSTALL
   file and User Guide. This must be done on suite and task hosts. Users then get
   the latest installed version by default, or (like tasks) a particular version
   if $CYLC_VERSION is defined.
   
   Use -v/--verbose to see the command invoked to determine the remote version
   (all remote cylc command invocations will be of the same form, which may be
   site dependent -- see cylc global config documentation.
   
   Arguments:
      SUITE               Suite name or path
   
   Options:
     -h, --help            show this help message and exit
     -e, --error           Exit with error status if 8.0a0 is not available on
                           all remote accounts.
     -v, --verbose         Verbose output mode.
     --debug               Output developer information and show exception
                           tracebacks.
     --suite-owner=OWNER   Specify suite owner
     -s NAME=VALUE, --set=NAME=VALUE
                           Set the value of a Jinja2 template variable in the
                           suite definition. This option can be used multiple
                           times on the command line. NOTE: these settings
                           persist across suite restarts, but can be set again on
                           the "cylc restart" command line if they need to be
                           overridden.
     --set-file=FILE       Set the value of Jinja2 template variables in the
                           suite definition from a file containing NAME=VALUE
                           pairs (one per line). NOTE: these settings persist
                           across suite restarts, but can be set again on the
                           "cylc restart" command line if they need to be
                           overridden.


.. _command-checkpoint:

checkpoint
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: none

      Usage: cylc [control] checkpoint [OPTIONS] REG CHECKPOINT-NAME 
   
   Tell suite to checkpoint its current state.
   
   
   Arguments:
      REG                           Suite name
      CHECKPOINT-NAME               Checkpoint name
   
   Options:
     -h, --help            show this help message and exit
     --user=USER           Other user account name. This results in command
                           reinvocation on the remote account.
     --host=HOST           Other host name. This results in command reinvocation
                           on the remote account.
     -v, --verbose         Verbose output mode.
     --debug               Output developer information and show exception
                           tracebacks.
     --port=INT            Suite port number on the suite host. NOTE: this is
                           retrieved automatically if non-interactive ssh is
                           configured to the suite host.
     --use-ssh             Use ssh to re-invoke the command on the suite host.
     --ssh-cylc=SSH_CYLC   Location of cylc executable on remote ssh commands.
     --no-login            Do not use a login shell to run remote ssh commands.
                           The default is to use a login shell.
     --comms-timeout=SEC, --pyro-timeout=SEC
                           Set a timeout for network connections to the running
                           suite. The default is no timeout. For task messaging
                           connections see site/user config file documentation.
     -f, --force           Do not ask for confirmation before acting. Note that
                           it is not necessary to use this option if interactive
                           command prompts have been disabled in the site/user
                           config files.


.. _command-client:

client
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: none

      Usage: cylc client [OPTIONS] REG METHOD 
   
   (This command is for internal use.)
   Invoke suite runtime client, expect JSON from STDIN for keyword arguments.
   Use the -n option if client function requires no keyword arguments.
   
   
   Arguments:
      REG                  Suite name
      METHOD               Network API function name
   
   Options:
     -h, --help            show this help message and exit
     -n, --no-input        Do not read from STDIN, assume null input
     --user=USER           Other user account name. This results in command
                           reinvocation on the remote account.
     --host=HOST           Other host name. This results in command reinvocation
                           on the remote account.
     -v, --verbose         Verbose output mode.
     --debug               Output developer information and show exception
                           tracebacks.
     --port=INT            Suite port number on the suite host. NOTE: this is
                           retrieved automatically if non-interactive ssh is
                           configured to the suite host.
     --use-ssh             Use ssh to re-invoke the command on the suite host.
     --ssh-cylc=SSH_CYLC   Location of cylc executable on remote ssh commands.
     --no-login            Do not use a login shell to run remote ssh commands.
                           The default is to use a login shell.
     --comms-timeout=SEC, --pyro-timeout=SEC
                           Set a timeout for network connections to the running
                           suite. The default is no timeout. For task messaging
                           connections see site/user config file documentation.
     -f, --force           Do not ask for confirmation before acting. Note that
                           it is not necessary to use this option if interactive
                           command prompts have been disabled in the site/user
                           config files.


.. _command-cycle-point:

cycle-point
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: none

      Usage: cylc [util] cycle-point [OPTIONS] [POINT] 
   
   Cycle point date-time offset computation, and filename templating.
   
   Filename templating replaces elements of a template string with corresponding
   elements of the current or given cycle point.
   
   Use ISO 8601 or posix date-time format elements:
     % cylc cyclepoint 2010080T00 --template foo-CCYY-MM-DD-Thh.nc
     foo-2010-08-08-T00.nc
     % cylc cyclepoint 2010080T00 --template foo-%Y-%m-%d-T%H.nc
     foo-2010-08-08-T00.nc
   
   Other examples:
   
   1) print offset from an explicit cycle point:
     % cylc [util] cycle-point --offset-hours=6 20100823T1800Z
     20100824T0000Z
   
   2) print offset from $CYLC_TASK_CYCLE_POINT (as in suite tasks):
     % export CYLC_TASK_CYCLE_POINT=20100823T1800Z
     % cylc cycle-point --offset-hours=-6
     20100823T1200Z
   
   3) cycle point filename templating, explicit template:
     % export CYLC_TASK_CYCLE_POINT=2010-08
     % cylc cycle-point --offset-years=2 --template=foo-CCYY-MM.nc
     foo-2012-08.nc
   
   4) cycle point filename templating, template in a variable:
     % export CYLC_TASK_CYCLE_POINT=2010-08
     % export MYTEMPLATE=foo-CCYY-MM.nc
     % cylc cycle-point --offset-years=2 --template=MYTEMPLATE
     foo-2012-08.nc
   
   Arguments:
      [POINT]               ISO8601 date-time, default=$CYLC_TASK_CYCLE_POINT
   
   Options:
     -h, --help            show this help message and exit
     --offset-hours=HOURS  Add N hours to CYCLE (may be negative)
     --offset-days=DAYS    Add N days to CYCLE (N may be negative)
     --offset-months=MONTHS
                           Add N months to CYCLE (N may be negative)
     --offset-years=YEARS  Add N years to CYCLE (N may be negative)
     --offset=ISO_OFFSET   Add an ISO 8601-based interval representation to CYCLE
     --equal=POINT2        Succeed if POINT2 is equal to POINT (format agnostic).
     --template=TEMPLATE   Filename template string or variable
     --time-zone=TEMPLATE  Control the formatting of the result's timezone e.g.
                           (Z, +13:00, -hh
     --num-expanded-year-digits=NUMBER
                           Specify a number of expanded year digits to print in
                           the result
     --print-year          Print only CCYY of result
     --print-month         Print only MM of result
     --print-day           Print only DD of result
     --print-hour          Print only hh of result
     -v, --verbose         Verbose output mode.
     --debug               Output developer information and show exception
                           tracebacks.


.. _command-diff:

diff
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: none

      Usage: cylc [prep] diff|compare [OPTIONS] SUITE1 SUITE2
   
   Compare two suite definitions and display any differences.
   
   Differencing is done after parsing the suite.rc files so it takes
   account of default values that are not explicitly defined, it disregards
   the order of configuration items, and it sees any include-file content
   after inlining has occurred.
   
   Files in the suite bin directory and other sub-directories of the
   suite definition directory are not currently differenced.
   
   Arguments:
      SUITE1               Suite name or path
      SUITE2               Suite name or path
   
   Options:
     -h, --help            show this help message and exit
     -n, --nested          print suite.rc section headings in nested form.
     --user=USER           Other user account name. This results in command
                           reinvocation on the remote account.
     --host=HOST           Other host name. This results in command reinvocation
                           on the remote account.
     -v, --verbose         Verbose output mode.
     --debug               Output developer information and show exception
                           tracebacks.
     --suite-owner=OWNER   Specify suite owner
     -s NAME=VALUE, --set=NAME=VALUE
                           Set the value of a Jinja2 template variable in the
                           suite definition. This option can be used multiple
                           times on the command line. NOTE: these settings
                           persist across suite restarts, but can be set again on
                           the "cylc restart" command line if they need to be
                           overridden.
     --set-file=FILE       Set the value of Jinja2 template variables in the
                           suite definition from a file containing NAME=VALUE
                           pairs (one per line). NOTE: these settings persist
                           across suite restarts, but can be set again on the
                           "cylc restart" command line if they need to be
                           overridden.
     --icp=CYCLE_POINT     Set initial cycle point. Required if not defined in
                           suite.rc.


.. _command-documentation:

documentation
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: none

      Usage: cylc [info] documentation|browse [OPTIONS] [TARGET] 
   
   View documentation in the browser, as per Cylc global config.
   
   % cylc doc [--local] [OPTIONS]
       Open the Cylc documentation.
   % cylc doc [-t TASK] SUITE
       View suite or task documentation, if URLs are specified in the suite. This
       parses the suite definition to extract the requested URL.
   
   Arguments:
      [TARGET]               File or suite name
   
   Options:
     -h, --help            show this help message and exit
     --local               Open the local documentation (if it has been built).
     -t TASK_NAME, --task=TASK_NAME
                           Browse task documentation URLs.
     -s, --stdout          Just print the URL to stdout.
     --debug               Print exception traceback on error.
     -v, --verbose         Verbose output mode.


.. _command-dump:

dump
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: none

      Usage: cylc [info] dump [OPTIONS] REG 
   
   Print state information (e.g. the state of each task) from a running
   suite. For small suites 'watch cylc [info] dump SUITE' is an effective
   non-GUI real time monitor (but see also 'cylc monitor').
   
   For more information about a specific task, such as the current state of
   its prerequisites and outputs, see 'cylc [info] show'.
   
   Examples:
    Display the state of all running tasks, sorted by cycle point:
    % cylc [info] dump --tasks --sort SUITE | grep running
   
    Display the state of all tasks in a particular cycle point:
    % cylc [info] dump -t SUITE | grep 2010082406
   
   Arguments:
      REG               Suite name
   
   Options:
     -h, --help            show this help message and exit
     -g, --global          Global information only.
     -t, --tasks           Task states only.
     -r, --raw, --raw-format
                           Display raw format.
     -s, --sort            Task states only; sort by cycle point instead of name.
     --user=USER           Other user account name. This results in command
                           reinvocation on the remote account.
     --host=HOST           Other host name. This results in command reinvocation
                           on the remote account.
     -v, --verbose         Verbose output mode.
     --debug               Output developer information and show exception
                           tracebacks.
     --port=INT            Suite port number on the suite host. NOTE: this is
                           retrieved automatically if non-interactive ssh is
                           configured to the suite host.
     --use-ssh             Use ssh to re-invoke the command on the suite host.
     --ssh-cylc=SSH_CYLC   Location of cylc executable on remote ssh commands.
     --no-login            Do not use a login shell to run remote ssh commands.
                           The default is to use a login shell.
     --comms-timeout=SEC, --pyro-timeout=SEC
                           Set a timeout for network connections to the running
                           suite. The default is no timeout. For task messaging
                           connections see site/user config file documentation.


.. _command-edit:

edit
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: none

      Usage: cylc [prep] edit [OPTIONS] SUITE 
   
   Edit suite definitions without having to move to their directory
   locations, and with optional reversible inlining of include-files. Note
   that Jinja2 suites can only be edited in raw form but the processed
   version can be viewed with 'cylc [prep] view -p'.
   
   1/cylc [prep] edit SUITE
   Change to the suite definition directory and edit the suite.rc file.
   
   2/ cylc [prep] edit -i,--inline SUITE
   Edit the suite with include-files inlined between special markers. The
   original suite.rc file is temporarily replaced so that the inlined
   version is "live" during editing (i.e. you can run suites during
   editing and cylc will pick up changes to the suite definition). The
   inlined file is then split into its constituent include-files
   again when you exit the editor. Include-files can be nested or
   multiply-included; in the latter case only the first inclusion is
   inlined (this prevents conflicting changes made to the same file).
   
   3/ cylc [prep] edit --cleanup SUITE
   Remove backup files left by previous INLINED edit sessions.
   
   INLINED EDITING SAFETY: The suite.rc file and its include-files are
   automatically backed up prior to an inlined editing session. If the
   editor dies mid-session just invoke 'cylc edit -i' again to recover from
   the last saved inlined file. On exiting the editor, if any of the
   original include-files are found to have changed due to external
   intervention during editing you will be warned and the affected files
   will be written to new backups instead of overwriting the originals.
   Finally, the inlined suite.rc file is also backed up on exiting
   the editor, to allow recovery in case of accidental corruption of the
   include-file boundary markers in the inlined file.
   
   The edit process is spawned in the foreground as follows:
     % <editor> suite.rc
   Where <editor> is defined in the cylc site/user config files.
   
   See also 'cylc [prep] view'.
   
   Arguments:
      SUITE               Suite name or path
   
   Options:
     -h, --help           show this help message and exit
     -i, --inline         Edit with include-files inlined as described above.
     --cleanup            Remove backup files left by previous inlined edit
                          sessions.
     -g, --gui            Force use of the configured GUI editor.
     --user=USER          Other user account name. This results in command
                          reinvocation on the remote account.
     --host=HOST          Other host name. This results in command reinvocation
                          on the remote account.
     -v, --verbose        Verbose output mode.
     --debug              Output developer information and show exception
                          tracebacks.
     --suite-owner=OWNER  Specify suite owner


.. _command-ext-trigger:

ext-trigger
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: none

      Usage: cylc [control] ext-trigger [OPTIONS] REG MSG ID 
   
   Report an external event message to a suite server program. It is expected that
   a task in the suite has registered the same message as an external trigger - a
   special prerequisite to be satisfied by an external system, via this command,
   rather than by triggering off other tasks.
   
   The ID argument should uniquely distinguish one external trigger event from the
   next. When a task's external trigger is satisfied by an incoming message, the
   message ID is broadcast to all downstream tasks in the cycle point as
   $CYLC_EXT_TRIGGER_ID so that they can use it - e.g. to identify a new data file
   that the external triggering system is responding to.
   
   Use the retry options in case the target suite is down or out of contact.
   
   The suite passphrase must be installed in $HOME/.cylc/<SUITE>/.
   
   Note: to manually trigger a task use 'cylc trigger', not this command.
   
   Arguments:
      REG               Suite name
      MSG               External trigger message
      ID                Unique trigger ID
   
   Options:
     -h, --help            show this help message and exit
     --max-tries=INT       Maximum number of send attempts (default 5).
     --retry-interval=SEC  Delay in seconds before retrying (default 10.0).
     --user=USER           Other user account name. This results in command
                           reinvocation on the remote account.
     --host=HOST           Other host name. This results in command reinvocation
                           on the remote account.
     -v, --verbose         Verbose output mode.
     --debug               Output developer information and show exception
                           tracebacks.
     --port=INT            Suite port number on the suite host. NOTE: this is
                           retrieved automatically if non-interactive ssh is
                           configured to the suite host.
     --use-ssh             Use ssh to re-invoke the command on the suite host.
     --ssh-cylc=SSH_CYLC   Location of cylc executable on remote ssh commands.
     --no-login            Do not use a login shell to run remote ssh commands.
                           The default is to use a login shell.
     --comms-timeout=SEC, --pyro-timeout=SEC
                           Set a timeout for network connections to the running
                           suite. The default is no timeout. For task messaging
                           connections see site/user config file documentation.
     -f, --force           Do not ask for confirmation before acting. Note that
                           it is not necessary to use this option if interactive
                           command prompts have been disabled in the site/user
                           config files.


.. _command-extract-pkg-resources:

extract-pkg-resources
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: none

      cylc [info] get-pkg-resources [OPTIONS] DIR [RESOURCES]
   
   Extract resources from the cylc.flow package and write them to DIR.
   
   Options:
       --list      List available resources
   Arguments:
       DIR         Target Directory
       [RESOURCES] Specific resources to extract (default all).
   


.. _command-function-run:

function-run
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: none

      USAGE: cylc function-run <name> <json-args> <json-kwargs> <src-dir>
   
   INTERNAL USE (asynchronous external trigger function execution)
   
   Run a Python function "<name>(*args, **kwargs)" in the process pool. It must be
   defined in a module of the same name. Positional and keyword arguments must be
   passed in as JSON strings. <src-dir> is the suite source dir, needed to find
   local xtrigger modules.
   


.. _command-get-directory:

get-directory
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: none

      Usage: cylc [prep] get-directory REG
   
   Retrieve and print the source directory location of suite REG.
   Here's an easy way to move to a suite source directory:
     $ cd $(cylc get-dir REG).
   
   Arguments:
      SUITE               Suite name or path
   
   Options:
     -h, --help           show this help message and exit
     --user=USER          Other user account name. This results in command
                          reinvocation on the remote account.
     --host=HOST          Other host name. This results in command reinvocation
                          on the remote account.
     -v, --verbose        Verbose output mode.
     --debug              Output developer information and show exception
                          tracebacks.
     --suite-owner=OWNER  Specify suite owner


.. _command-get-host-metrics:

get-host-metrics
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: none

      Usage: cylc get-host-metrics [OPTIONS]
   
   Get metrics for localhost, in the form of a JSON structure with top-level
   keys as requested via the OPTIONS:
   
   1. --load
          1, 5 and 15 minute load averages (as keys) from the 'uptime' command.
   2. --memory
          Total free RAM memory, in kilobytes, from the 'free -k' command.
   3. --disk-space=PATH / --disk-space=PATH1,PATH2,PATH3 (etc)
          Available disk space from the 'df -Pk' command, in kilobytes, for one
          or more valid mount directory PATHs (as listed under 'Mounted on')
          within the filesystem of localhost. Multiple PATH options can be
          specified via a comma-delimited list, each becoming a key under the
          top-level disk space key.
   
   If no options are specified, --load and --memory are invoked by default.
   
   
   Options:
     -h, --help         show this help message and exit
     -l, --load         1, 5 and 15 minute load averages from the 'uptime'
                        command.
     -m, --memory       Total memory not in use by the system, buffer or cache,
                        in KB, from '/proc/meminfo'.
     --disk-space=DISK  Available disk space, in KB, from the 'df -Pk' command.


.. _command-get-site-config:

get-site-config
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: none

      Usage: cylc [admin] get-site-config [OPTIONS]
   
   Print cylc site/user configuration settings.
   
   By default all settings are printed. For specific sections or items
   use -i/--item and wrap parent sections in square brackets:
      cylc get-site-config --item '[editors]terminal'
   Multiple items can be specified at once.
   
   Options:
     -h, --help            show this help message and exit
     -i [SEC...]ITEM, --item=[SEC...]ITEM
                           Item or section to print (multiple use allowed).
     --sparse              Only print items explicitly set in the config files.
     -p, --python          Print native Python format.
     --print-run-dir       Print the configured cylc run directory.
     --print-site-dir      Print the cylc site configuration directory location.
     -v, --verbose         Verbose output mode.
     --debug               Output developer information and show exception
                           tracebacks.


.. _command-get-suite-config:

get-suite-config
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: none

      Usage: cylc [info] get-suite-config [OPTIONS] SUITE 
   
   Print parsed suite configuration items, after runtime inheritance.
   
   By default all settings are printed. For specific sections or items
   use -i/--item and wrap sections in square brackets, e.g.:
      cylc get-suite-config --item '[scheduling]initial cycle point'
   Multiple items can be retrieved at once.
   
   By default, unset values are printed as an empty string, or (for
   historical reasons) as "None" with -o/--one-line. These defaults
   can be changed with the -n/--null-value option.
   
   Example:
     |# SUITE.RC
     |[runtime]
     |    [[modelX]]
     |        [[[environment]]]
     |            FOO = foo
     |            BAR = bar
   
   $ cylc get-suite-config --item=[runtime][modelX][environment]FOO SUITE
   foo
   
   $ cylc get-suite-config --item=[runtime][modelX][environment] SUITE
   FOO = foo
   BAR = bar
   
   $ cylc get-suite-config --item=[runtime][modelX] SUITE
   ...
   [[[environment]]]
       FOO = foo
       BAR = bar
   ...
   
   Arguments:
      SUITE               Suite name or path
   
   Options:
     -h, --help            show this help message and exit
     -i [SEC...]ITEM, --item=[SEC...]ITEM
                           Item or section to print (multiple use allowed).
     -r, --sparse          Only print items explicitly set in the config files.
     -p, --python          Print native Python format.
     -a, --all-tasks       For [runtime] items (e.g. --item='script') report
                           values for all tasks prefixed by task name.
     -n STRING, --null-value=STRING
                           The string to print for unset values (default
                           nothing).
     -m, --mark-up         Prefix each line with '!cylc!'.
     -o, --one-line        Print multiple single-value items at once.
     -t, --tasks           Print the suite task list [DEPRECATED: use 'cylc list
                           SUITE'].
     -u RUN_MODE, --run-mode=RUN_MODE
                           Get config for suite run mode.
     --user=USER           Other user account name. This results in command
                           reinvocation on the remote account.
     --host=HOST           Other host name. This results in command reinvocation
                           on the remote account.
     -v, --verbose         Verbose output mode.
     --debug               Output developer information and show exception
                           tracebacks.
     --suite-owner=OWNER   Specify suite owner
     -s NAME=VALUE, --set=NAME=VALUE
                           Set the value of a Jinja2 template variable in the
                           suite definition. This option can be used multiple
                           times on the command line. NOTE: these settings
                           persist across suite restarts, but can be set again on
                           the "cylc restart" command line if they need to be
                           overridden.
     --set-file=FILE       Set the value of Jinja2 template variables in the
                           suite definition from a file containing NAME=VALUE
                           pairs (one per line). NOTE: these settings persist
                           across suite restarts, but can be set again on the
                           "cylc restart" command line if they need to be
                           overridden.
     --icp=CYCLE_POINT     Set initial cycle point. Required if not defined in
                           suite.rc.


.. _command-get-suite-contact:

get-suite-contact
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: none

      Usage: cylc [info] get-suite-contact [OPTIONS] REG 
   
   Print contact information of running suite REG.
   
   Arguments:
      REG               Suite name
   
   Options:
     -h, --help     show this help message and exit
     --user=USER    Other user account name. This results in command reinvocation
                    on the remote account.
     --host=HOST    Other host name. This results in command reinvocation on the
                    remote account.
     -v, --verbose  Verbose output mode.
     --debug        Output developer information and show exception tracebacks.


.. _command-get-suite-version:

get-suite-version
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: none

      Usage: cylc [info] get-suite-version [OPTIONS] REG 
   
   Interrogate running suite REG to find what version of cylc is running it.
   
   To find the version you've invoked at the command line see "cylc version".
   
   Arguments:
      REG               Suite name
   
   Options:
     -h, --help            show this help message and exit
     --user=USER           Other user account name. This results in command
                           reinvocation on the remote account.
     --host=HOST           Other host name. This results in command reinvocation
                           on the remote account.
     -v, --verbose         Verbose output mode.
     --debug               Output developer information and show exception
                           tracebacks.
     --port=INT            Suite port number on the suite host. NOTE: this is
                           retrieved automatically if non-interactive ssh is
                           configured to the suite host.
     --use-ssh             Use ssh to re-invoke the command on the suite host.
     --ssh-cylc=SSH_CYLC   Location of cylc executable on remote ssh commands.
     --no-login            Do not use a login shell to run remote ssh commands.
                           The default is to use a login shell.
     --comms-timeout=SEC, --pyro-timeout=SEC
                           Set a timeout for network connections to the running
                           suite. The default is no timeout. For task messaging
                           connections see site/user config file documentation.
     -f, --force           Do not ask for confirmation before acting. Note that
                           it is not necessary to use this option if interactive
                           command prompts have been disabled in the site/user
                           config files.


.. _command-graph:

graph
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: none

      Usage: Usage:
       cylc graph SUITE [START] [STOP]
   
   Implement the old ``cylc graph --reference command`` for producing a textural
   graph of a suite.
   
   
   
   Arguments:
      [SUITE]               Suite name or path
      [START]               Initial cycle point (default: suite initial point)
      [STOP]                Final cycle point (default: initial + 3 points)
   
   Options:
     -h, --help            show this help message and exit
     -u, --ungrouped       Start with task families ungrouped (the default is
                           grouped).
     -n, --namespaces      Plot the suite namespace inheritance hierarchy (task
                           run time properties).
     -r, --reference       Output in a sorted plain text format for comparison
                           purposes. If not given, assume --output-file=-.
     --show-suicide        Show suicide triggers.  They are not shown by default,
                           unless toggled on with the tool bar button.
     --icp=CYCLE_POINT     Set initial cycle point. Required if not defined in
                           suite.rc.
     --user=USER           Other user account name. This results in command
                           reinvocation on the remote account.
     --host=HOST           Other host name. This results in command reinvocation
                           on the remote account.
     -v, --verbose         Verbose output mode.
     --debug               Output developer information and show exception
                           tracebacks.
     --suite-owner=OWNER   Specify suite owner
     -s NAME=VALUE, --set=NAME=VALUE
                           Set the value of a Jinja2 template variable in the
                           suite definition. This option can be used multiple
                           times on the command line. NOTE: these settings
                           persist across suite restarts, but can be set again on
                           the "cylc restart" command line if they need to be
                           overridden.
     --set-file=FILE       Set the value of Jinja2 template variables in the
                           suite definition from a file containing NAME=VALUE
                           pairs (one per line). NOTE: these settings persist
                           across suite restarts, but can be set again on the
                           "cylc restart" command line if they need to be
                           overridden.


.. _command-graph-diff:

graph-diff
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: none

      Usage: cylc graph-diff [OPTIONS] SUITE1 SUITE2 -- [GRAPH_OPTIONS_ARGS]
   
   Difference 'cylc graph --reference' output for SUITE1 and SUITE2.
   
   OPTIONS: Use '-g' to launch a graphical diff utility.
            Use '--diff-cmd=MY_DIFF_CMD' to use a custom diff tool.
   
   SUITE1, SUITE2: Suite names to compare.
   GRAPH_OPTIONS_ARGS: Options and arguments passed directly to cylc graph.


.. _command-hold:

hold
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: none

      Usage: cylc [control] hold [OPTIONS] REG [TASK_GLOB ...] 
   
   Hold one or more waiting tasks (cylc hold REG TASK_GLOB ...), or
   a whole suite (cylc hold REG).
   
   Held tasks do not submit even if they are ready to run.
   
   See also 'cylc [control] release'.
   
   TASK_GLOB is a pattern to match task proxies or task families,
   or groups of them:
   * [CYCLE-POINT-GLOB/]TASK-NAME-GLOB[:TASK-STATE]
   * [CYCLE-POINT-GLOB/]FAMILY-NAME-GLOB[:TASK-STATE]
   * TASK-NAME-GLOB[.CYCLE-POINT-GLOB][:TASK-STATE]
   * FAMILY-NAME-GLOB[.CYCLE-POINT-GLOB][:TASK-STATE]
   
   For example, to match:
   * all tasks in a cycle: '20200202T0000Z/*' or '*.20200202T0000Z'
   * all tasks in the submitted status: ':submitted'
   * retrying 'foo*' tasks in 0000Z cycles: 'foo*.*0000Z:retrying' or
     '*0000Z/foo*:retrying'
   * retrying tasks in 'BAR' family: '*/BAR:retrying' or 'BAR.*:retrying'
   * retrying tasks in 'BAR' or 'BAZ' families: '*/BA[RZ]:retrying' or
     'BA[RZ].*:retrying'
   
   Arguments:
      REG                           Suite name
      [TASK_GLOB ...]               Task matching patterns
   
   Options:
     -h, --help            show this help message and exit
     --after=CYCLE_POINT   Hold whole suite AFTER this cycle point.
     --user=USER           Other user account name. This results in command
                           reinvocation on the remote account.
     --host=HOST           Other host name. This results in command reinvocation
                           on the remote account.
     -v, --verbose         Verbose output mode.
     --debug               Output developer information and show exception
                           tracebacks.
     --port=INT            Suite port number on the suite host. NOTE: this is
                           retrieved automatically if non-interactive ssh is
                           configured to the suite host.
     --use-ssh             Use ssh to re-invoke the command on the suite host.
     --ssh-cylc=SSH_CYLC   Location of cylc executable on remote ssh commands.
     --no-login            Do not use a login shell to run remote ssh commands.
                           The default is to use a login shell.
     --comms-timeout=SEC, --pyro-timeout=SEC
                           Set a timeout for network connections to the running
                           suite. The default is no timeout. For task messaging
                           connections see site/user config file documentation.
     -f, --force           Do not ask for confirmation before acting. Note that
                           it is not necessary to use this option if interactive
                           command prompts have been disabled in the site/user
                           config files.


.. _command-insert:

insert
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: none

      Usage: cylc [control] insert [OPTIONS] REG TASKID [...] 
   
   Insert task proxies into a running suite. Uses of insertion include:
    1) insert a task that was excluded by the suite definition at start-up.
    2) reinstate a task that was previously removed from a running suite.
    3) re-run an old task that cannot be retriggered because its task proxy
    is no longer live in the a suite.
   
   Be aware that inserted cycling tasks keep on cycling as normal, even if
   another instance of the same task exists at a later cycle (instances of
   the same task at different cycles can coexist, but a newly spawned task
   will not be added to the pool if it catches up to another task with the
   same ID).
   
   See also 'cylc submit', for running tasks without the scheduler.
   
   TASK_GLOB is a pattern to match task proxies or task families,
   or groups of them:
   * [CYCLE-POINT-GLOB/]TASK-NAME-GLOB[:TASK-STATE]
   * [CYCLE-POINT-GLOB/]FAMILY-NAME-GLOB[:TASK-STATE]
   * TASK-NAME-GLOB[.CYCLE-POINT-GLOB][:TASK-STATE]
   * FAMILY-NAME-GLOB[.CYCLE-POINT-GLOB][:TASK-STATE]
   
   For example, to match:
   * all tasks in a cycle: '20200202T0000Z/*' or '*.20200202T0000Z'
   * all tasks in the submitted status: ':submitted'
   * retrying 'foo*' tasks in 0000Z cycles: 'foo*.*0000Z:retrying' or
     '*0000Z/foo*:retrying'
   * retrying tasks in 'BAR' family: '*/BAR:retrying' or 'BAR.*:retrying'
   * retrying tasks in 'BAR' or 'BAZ' families: '*/BA[RZ]:retrying' or
     'BA[RZ].*:retrying'
   
   Arguments:
      REG                        Suite name
      TASKID [...]               Task identifier
   
   Options:
     -h, --help            show this help message and exit
     --stop-point=CYCLE_POINT, --remove-point=CYCLE_POINT
                           Optional hold/stop cycle point for inserted task.
     --no-check            Add task even if the provided cycle point is not valid
                           for the given task.
     --user=USER           Other user account name. This results in command
                           reinvocation on the remote account.
     --host=HOST           Other host name. This results in command reinvocation
                           on the remote account.
     -v, --verbose         Verbose output mode.
     --debug               Output developer information and show exception
                           tracebacks.
     --port=INT            Suite port number on the suite host. NOTE: this is
                           retrieved automatically if non-interactive ssh is
                           configured to the suite host.
     --use-ssh             Use ssh to re-invoke the command on the suite host.
     --ssh-cylc=SSH_CYLC   Location of cylc executable on remote ssh commands.
     --no-login            Do not use a login shell to run remote ssh commands.
                           The default is to use a login shell.
     --comms-timeout=SEC, --pyro-timeout=SEC
                           Set a timeout for network connections to the running
                           suite. The default is no timeout. For task messaging
                           connections see site/user config file documentation.
     -f, --force           Do not ask for confirmation before acting. Note that
                           it is not necessary to use this option if interactive
                           command prompts have been disabled in the site/user
                           config files.


.. _command-jobs-kill:

jobs-kill
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: none

      Usage: cylc [control] jobs-kill JOB-LOG-ROOT [JOB-LOG-DIR ...]
   
   (This command is for internal use. Users should use "cylc kill".) Read job
   status files to obtain the names of the batch systems and the job IDs in the
   systems. Invoke the relevant batch system commands to ask the batch systems to
   terminate the jobs.
   
   
   
   Arguments:
      JOB-LOG-ROOT                    The log/job sub-directory for the suite
      [JOB-LOG-DIR ...]               A point/name/submit_num sub-directory
   
   Options:
     -h, --help     show this help message and exit
     --user=USER    Other user account name. This results in command reinvocation
                    on the remote account.
     --host=HOST    Other host name. This results in command reinvocation on the
                    remote account.
     -v, --verbose  Verbose output mode.
     --debug        Output developer information and show exception tracebacks.


.. _command-jobs-poll:

jobs-poll
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: none

      Usage: cylc [control] jobs-poll JOB-LOG-ROOT [JOB-LOG-DIR ...]
   
   (This command is for internal use. Users should use "cylc poll".) Read job
   status files to obtain the statuses of the jobs. If necessary, Invoke the
   relevant batch system commands to ask the batch systems for more statuses.
   
   
   
   Arguments:
      JOB-LOG-ROOT                    The log/job sub-directory for the suite
      [JOB-LOG-DIR ...]               A point/name/submit_num sub-directory
   
   Options:
     -h, --help     show this help message and exit
     --user=USER    Other user account name. This results in command reinvocation
                    on the remote account.
     --host=HOST    Other host name. This results in command reinvocation on the
                    remote account.
     -v, --verbose  Verbose output mode.
     --debug        Output developer information and show exception tracebacks.


.. _command-jobs-submit:

jobs-submit
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: none

      Usage: cylc [control] jobs-submit JOB-LOG-ROOT [JOB-LOG-DIR ...]
   
   (This command is for internal use. Users should use "cylc submit".) Submit task
   jobs to relevant batch systems. On a remote job host, this command reads the
   job files from STDIN.
   
   
   
   Arguments:
      JOB-LOG-ROOT                    The log/job sub-directory for the suite
      [JOB-LOG-DIR ...]               A point/name/submit_num sub-directory
   
   Options:
     -h, --help     show this help message and exit
     --remote-mode  Is this being run on a remote job host?
     --utc-mode     (for remote mode) is the suite running in UTC mode?
     --user=USER    Other user account name. This results in command reinvocation
                    on the remote account.
     --host=HOST    Other host name. This results in command reinvocation on the
                    remote account.
     -v, --verbose  Verbose output mode.
     --debug        Output developer information and show exception tracebacks.


.. _command-jobscript:

jobscript
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: none

      Usage: cylc [prep] jobscript [OPTIONS] REG TASK
   
   Generate a task job script and print it to stdout.
   
   Here's how to capture the script in the vim editor:
     % cylc jobscript REG TASK | vim -
   Emacs unfortunately cannot read from stdin:
     % cylc jobscript REG TASK > tmp.sh; emacs tmp.sh
   
   This command wraps 'cylc [control] submit --dry-run'.
   Other options (e.g. for suite host and owner) are passed
   through to the submit command.
   
   Options:
     -h, --help   Print this usage message.
     -e --edit    Open the jobscript in a CLI text editor.
     -g --gedit   Open the jobscript in a GUI text editor.
     --plain      Don't print the "Task Job Script Generated message."
    (see also 'cylc submit --help')
   
   Arguments:
     REG          Registered suite name.
     TASK         Task ID (NAME.CYCLE_POINT)


.. _command-kill:

kill
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: none

      Usage: cylc [control] kill [OPTIONS] REG [TASK_GLOB ...] 
   
   Kill jobs of active tasks and update their statuses accordingly.
   
   To kill one or more tasks, "cylc kill REG TASK_GLOB ..."; to kill all active
   tasks: "cylc kill REG".
   
   TASK_GLOB is a pattern to match task proxies or task families,
   or groups of them:
   * [CYCLE-POINT-GLOB/]TASK-NAME-GLOB[:TASK-STATE]
   * [CYCLE-POINT-GLOB/]FAMILY-NAME-GLOB[:TASK-STATE]
   * TASK-NAME-GLOB[.CYCLE-POINT-GLOB][:TASK-STATE]
   * FAMILY-NAME-GLOB[.CYCLE-POINT-GLOB][:TASK-STATE]
   
   For example, to match:
   * all tasks in a cycle: '20200202T0000Z/*' or '*.20200202T0000Z'
   * all tasks in the submitted status: ':submitted'
   * retrying 'foo*' tasks in 0000Z cycles: 'foo*.*0000Z:retrying' or
     '*0000Z/foo*:retrying'
   * retrying tasks in 'BAR' family: '*/BAR:retrying' or 'BAR.*:retrying'
   * retrying tasks in 'BAR' or 'BAZ' families: '*/BA[RZ]:retrying' or
     'BA[RZ].*:retrying'
   
   Arguments:
      REG                           Suite name
      [TASK_GLOB ...]               Task matching patterns
   
   Options:
     -h, --help            show this help message and exit
     --user=USER           Other user account name. This results in command
                           reinvocation on the remote account.
     --host=HOST           Other host name. This results in command reinvocation
                           on the remote account.
     -v, --verbose         Verbose output mode.
     --debug               Output developer information and show exception
                           tracebacks.
     --port=INT            Suite port number on the suite host. NOTE: this is
                           retrieved automatically if non-interactive ssh is
                           configured to the suite host.
     --use-ssh             Use ssh to re-invoke the command on the suite host.
     --ssh-cylc=SSH_CYLC   Location of cylc executable on remote ssh commands.
     --no-login            Do not use a login shell to run remote ssh commands.
                           The default is to use a login shell.
     --comms-timeout=SEC, --pyro-timeout=SEC
                           Set a timeout for network connections to the running
                           suite. The default is no timeout. For task messaging
                           connections see site/user config file documentation.
     -f, --force           Do not ask for confirmation before acting. Note that
                           it is not necessary to use this option if interactive
                           command prompts have been disabled in the site/user
                           config files.


.. _command-list:

list
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: none

      Usage: cylc [info|prep] list|ls [OPTIONS] SUITE 
   
   Print runtime namespace names (tasks and families), the first-parent
   inheritance graph, or actual tasks for a given cycle range.
   
   The first-parent inheritance graph determines the primary task family
   groupings that are collapsible in cylc visualisation tools.
   
   To visualize the full multiple inheritance hierarchy use:
     'cylc graph -n'.
   
   Arguments:
      SUITE               Suite name or path
   
   Options:
     -h, --help            show this help message and exit
     -a, --all-tasks       Print all tasks, not just those used in the graph.
     -n, --all-namespaces  Print all runtime namespaces, not just tasks.
     -m, --mro             Print the linear "method resolution order" for each
                           namespace (the multiple-inheritance precedence order
                           as determined by the C3 linearization algorithm).
     -t, --tree            Print the first-parent inheritance hierarchy in tree
                           form.
     -b, --box             With -t/--tree, using unicode box characters. Your
                           terminal must be able to display unicode characters.
     -w, --with-titles     Print namespaces titles too.
     -p START[,STOP], --points=START[,STOP]
                           Print actual task IDs from the START [through STOP]
                           cycle points.
     --user=USER           Other user account name. This results in command
                           reinvocation on the remote account.
     --host=HOST           Other host name. This results in command reinvocation
                           on the remote account.
     -v, --verbose         Verbose output mode.
     --debug               Output developer information and show exception
                           tracebacks.
     --suite-owner=OWNER   Specify suite owner
     -s NAME=VALUE, --set=NAME=VALUE
                           Set the value of a Jinja2 template variable in the
                           suite definition. This option can be used multiple
                           times on the command line. NOTE: these settings
                           persist across suite restarts, but can be set again on
                           the "cylc restart" command line if they need to be
                           overridden.
     --set-file=FILE       Set the value of Jinja2 template variables in the
                           suite definition from a file containing NAME=VALUE
                           pairs (one per line). NOTE: these settings persist
                           across suite restarts, but can be set again on the
                           "cylc restart" command line if they need to be
                           overridden.
     --icp=CYCLE_POINT     Set initial cycle point. Required if not defined in
                           suite.rc.


.. _command-ls-checkpoints:

ls-checkpoints
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: none

      Usage: cylc [info] ls-checkpoints [OPTIONS] REG [ID ...] 
   
   In the absence of arguments and the --all option, list checkpoint IDs, their
   time and events. Otherwise, display the latest and/or the checkpoints of suite
   parameters, task pool and broadcast states in the suite runtime database.
   
   
   Arguments:
      REG                    Suite name
      [ID ...]               Checkpoint ID (default=latest)
   
   Options:
     -h, --help     show this help message and exit
     -a, --all      Display data of all available checkpoints.
     --user=USER    Other user account name. This results in command reinvocation
                    on the remote account.
     --host=HOST    Other host name. This results in command reinvocation on the
                    remote account.
     -v, --verbose  Verbose output mode.
     --debug        Output developer information and show exception tracebacks.


.. _command-message:

message
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: none

      Usage: cylc [task] message [OPTIONS] -- [REG] [TASK-JOB] [[SEVERITY:]MESSAGE ...] 
   
   Record task job messages.
   
   Send task job messages to:
   - The job stdout/stderr.
   - The job status file, if there is one.
   - The suite server program, if communication is possible.
   
   Task jobs use this command to record and report status such as success and
   failure. Applications run by task jobs can use this command to report messages
   and to report registered task outputs.
   
   Messages can be specified as arguments. A '-' indicates that the command should
   read messages from STDIN. When reading from STDIN, multiple messages are
   separated by empty lines. Examples:
   
   Single message as an argument:
    % cylc message -- "${CYLC_SUITE_NAME}" "${CYLC_TASK_JOB}" 'Hello world!'
   
   Multiple messages as arguments:
    % cylc message -- "${CYLC_SUITE_NAME}" "${CYLC_TASK_JOB}" \
           'Hello world!' 'Hi' 'WARNING:Hey!'
   
   Multiple messages on STDIN:
    % cylc message -- "${CYLC_SUITE_NAME}" "${CYLC_TASK_JOB}" - <<'__STDIN__'
    % Hello
    % world!
    %
    % Hi
    %
    % WARNING:Hey!
    %__STDIN__
   
   Note "${CYLC_SUITE_NAME}" and "${CYLC_TASK_JOB}" are made available in task job
   environments - you do not need to write their actual values in task scripting.
   
   Each message can be prefixed with a severity level using the syntax 'SEVERITY:
   MESSAGE'.
   
   The default message severity is INFO. The --severity=SEVERITY option can be
   used to set the default severity level for all unprefixed messages.
   
   Note: to abort a job script with a custom error message, use cylc__job_abort:
     cylc__job_abort 'message...'
   (For technical reasons this is a shell function, not a cylc sub-command.)
   
   For backward compatibility, if number of arguments is less than or equal to 2,
   the command assumes the classic interface, where all arguments are messages.
   Otherwise, the first 2 arguments are assumed to be the suite name and the task
   job identifier.
   
   
   Arguments:
      [REG]                                  Suite name
      [TASK-JOB]                             Task job identifier CYCLE/TASK_NAME/SUBMIT_NUM
      [[SEVERITY:]MESSAGE ...]               Messages
   
   Options:
     -h, --help            show this help message and exit
     -s SEVERITY, -p SEVERITY, --severity=SEVERITY, --priority=SEVERITY
                           Set severity levels for messages that do not have one
     --user=USER           Other user account name. This results in command
                           reinvocation on the remote account.
     --host=HOST           Other host name. This results in command reinvocation
                           on the remote account.
     -v, --verbose         Verbose output mode.
     --debug               Output developer information and show exception
                           tracebacks.
     --port=INT            Suite port number on the suite host. NOTE: this is
                           retrieved automatically if non-interactive ssh is
                           configured to the suite host.
     --use-ssh             Use ssh to re-invoke the command on the suite host.
     --ssh-cylc=SSH_CYLC   Location of cylc executable on remote ssh commands.
     --no-login            Do not use a login shell to run remote ssh commands.
                           The default is to use a login shell.
     --comms-timeout=SEC, --pyro-timeout=SEC
                           Set a timeout for network connections to the running
                           suite. The default is no timeout. For task messaging
                           connections see site/user config file documentation.
     -f, --force           Do not ask for confirmation before acting. Note that
                           it is not necessary to use this option if interactive
                           command prompts have been disabled in the site/user
                           config files.


.. _command-monitor:

monitor
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: none

      Usage: cylc [info] monitor [OPTIONS] REG [USER_AT_HOST] 
   
   A terminal-based live suite monitor.  Exit with 'Ctrl-C'.
   
   The USER_AT_HOST argument allows suite selection by 'cylc scan' output:
     cylc monitor $(cylc scan | grep <suite_name>)
   
   
   Arguments:
      REG                          Suite name
      [USER_AT_HOST]               user@host:port, shorthand for --user, --host & --port.
   
   Options:
     -h, --help            show this help message and exit
     -a, --align           Align task names. Only useful for small suites.
     -r, --restricted      Restrict display to active task states. This may be
                           useful for monitoring very large suites. The state
                           summary line still reflects all task proxies.
     -s ORDER, --sort=ORDER
                           Task sort order: "definition" or "alphanumeric".The
                           default is definition order, as determined by global
                           config. (Definition order is the order that tasks
                           appear under [runtime] in the suite definition).
     -o, --once            Show a single view then exit.
     -u, --runahead        Display task proxies in the runahead pool (off by
                           default).
     -i SECONDS, --interval=SECONDS
                           Interval between suite state retrievals, in seconds
                           (default 1).
     --user=USER           Other user account name. This results in command
                           reinvocation on the remote account.
     --host=HOST           Other host name. This results in command reinvocation
                           on the remote account.
     -v, --verbose         Verbose output mode.
     --debug               Output developer information and show exception
                           tracebacks.
     --port=INT            Suite port number on the suite host. NOTE: this is
                           retrieved automatically if non-interactive ssh is
                           configured to the suite host.
     --use-ssh             Use ssh to re-invoke the command on the suite host.
     --ssh-cylc=SSH_CYLC   Location of cylc executable on remote ssh commands.
     --no-login            Do not use a login shell to run remote ssh commands.
                           The default is to use a login shell.
     --comms-timeout=SEC, --pyro-timeout=SEC
                           Set a timeout for network connections to the running
                           suite. The default is no timeout. For task messaging
                           connections see site/user config file documentation.


.. _command-nudge:

nudge
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: none

      Usage: cylc [control] nudge [OPTIONS] REG 
   
   Cause the cylc task processing loop to be invoked in a running suite.
   
   This happens automatically when the state of any task changes such that
   task processing (dependency negotiation etc.) is required, or if a
   clock-trigger task is ready to run.
   
   The main reason to use this command is to update the "estimated time till
   completion" intervals, during periods when nothing else is happening.
   
   
   Arguments:
      REG               Suite name
   
   Options:
     -h, --help            show this help message and exit
     --user=USER           Other user account name. This results in command
                           reinvocation on the remote account.
     --host=HOST           Other host name. This results in command reinvocation
                           on the remote account.
     -v, --verbose         Verbose output mode.
     --debug               Output developer information and show exception
                           tracebacks.
     --port=INT            Suite port number on the suite host. NOTE: this is
                           retrieved automatically if non-interactive ssh is
                           configured to the suite host.
     --use-ssh             Use ssh to re-invoke the command on the suite host.
     --ssh-cylc=SSH_CYLC   Location of cylc executable on remote ssh commands.
     --no-login            Do not use a login shell to run remote ssh commands.
                           The default is to use a login shell.
     --comms-timeout=SEC, --pyro-timeout=SEC
                           Set a timeout for network connections to the running
                           suite. The default is no timeout. For task messaging
                           connections see site/user config file documentation.
     -f, --force           Do not ask for confirmation before acting. Note that
                           it is not necessary to use this option if interactive
                           command prompts have been disabled in the site/user
                           config files.


.. _command-ping:

ping
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: none

      Usage: cylc [discovery] ping [OPTIONS] REG [TASK] 
   
   If suite REG is running or TASK in suite REG is currently running,
   exit with success status, else exit with error status.
   
   Arguments:
      REG                  Suite name
      [TASK]               Task NAME.CYCLE_POINT
   
   Options:
     -h, --help            show this help message and exit
     --user=USER           Other user account name. This results in command
                           reinvocation on the remote account.
     --host=HOST           Other host name. This results in command reinvocation
                           on the remote account.
     -v, --verbose         Verbose output mode.
     --debug               Output developer information and show exception
                           tracebacks.
     --port=INT            Suite port number on the suite host. NOTE: this is
                           retrieved automatically if non-interactive ssh is
                           configured to the suite host.
     --use-ssh             Use ssh to re-invoke the command on the suite host.
     --ssh-cylc=SSH_CYLC   Location of cylc executable on remote ssh commands.
     --no-login            Do not use a login shell to run remote ssh commands.
                           The default is to use a login shell.
     --comms-timeout=SEC, --pyro-timeout=SEC
                           Set a timeout for network connections to the running
                           suite. The default is no timeout. For task messaging
                           connections see site/user config file documentation.
     -f, --force           Do not ask for confirmation before acting. Note that
                           it is not necessary to use this option if interactive
                           command prompts have been disabled in the site/user
                           config files.


.. _command-poll:

poll
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: none

      Usage: cylc [control] poll [OPTIONS] REG [TASK_GLOB ...] 
   
   Poll (query) task jobs to verify and update their statuses.
   
   Use "cylc poll REG" to poll all active tasks, or "cylc poll REG TASK_GLOB"
   to poll individual tasks or families, or groups of them.
   
   TASK_GLOB is a pattern to match task proxies or task families,
   or groups of them:
   * [CYCLE-POINT-GLOB/]TASK-NAME-GLOB[:TASK-STATE]
   * [CYCLE-POINT-GLOB/]FAMILY-NAME-GLOB[:TASK-STATE]
   * TASK-NAME-GLOB[.CYCLE-POINT-GLOB][:TASK-STATE]
   * FAMILY-NAME-GLOB[.CYCLE-POINT-GLOB][:TASK-STATE]
   
   For example, to match:
   * all tasks in a cycle: '20200202T0000Z/*' or '*.20200202T0000Z'
   * all tasks in the submitted status: ':submitted'
   * retrying 'foo*' tasks in 0000Z cycles: 'foo*.*0000Z:retrying' or
     '*0000Z/foo*:retrying'
   * retrying tasks in 'BAR' family: '*/BAR:retrying' or 'BAR.*:retrying'
   * retrying tasks in 'BAR' or 'BAZ' families: '*/BA[RZ]:retrying' or
     'BA[RZ].*:retrying'
   
   Arguments:
      REG                           Suite name
      [TASK_GLOB ...]               Task matching patterns
   
   Options:
     -h, --help            show this help message and exit
     -s, --succeeded       Allow polling of succeeded tasks.
     --user=USER           Other user account name. This results in command
                           reinvocation on the remote account.
     --host=HOST           Other host name. This results in command reinvocation
                           on the remote account.
     -v, --verbose         Verbose output mode.
     --debug               Output developer information and show exception
                           tracebacks.
     --port=INT            Suite port number on the suite host. NOTE: this is
                           retrieved automatically if non-interactive ssh is
                           configured to the suite host.
     --use-ssh             Use ssh to re-invoke the command on the suite host.
     --ssh-cylc=SSH_CYLC   Location of cylc executable on remote ssh commands.
     --no-login            Do not use a login shell to run remote ssh commands.
                           The default is to use a login shell.
     --comms-timeout=SEC, --pyro-timeout=SEC
                           Set a timeout for network connections to the running
                           suite. The default is no timeout. For task messaging
                           connections see site/user config file documentation.
     -f, --force           Do not ask for confirmation before acting. Note that
                           it is not necessary to use this option if interactive
                           command prompts have been disabled in the site/user
                           config files.


.. _command-print:

print
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: none

      Usage: cylc [prep] print [OPTIONS] [REGEX]
   
   Print registered (installed) suites.
   
   Note on result filtering:
     (a) The filter patterns are Regular Expressions, not shell globs, so
   the general wildcard is '.*' (match zero or more of anything), NOT '*'.
     (b) For printing purposes there is an implicit wildcard at the end of
   each pattern ('foo' is the same as 'foo/*'); use the string end marker
   to prevent this ('foo$' matches only literal 'foo').
   
   Arguments:
      [REGEX]               Suite name regular expression pattern
   
   Options:
     -h, --help     show this help message and exit
     -t, --tree     Print suites in nested tree form.
     -b, --box      Use unicode box drawing characters in tree views.
     -a, --align    Align columns.
     -x             don't print suite definition directory paths.
     -y             Don't print suite titles.
     --fail         Fail (exit 1) if no matching suites are found.
     --user=USER    Other user account name. This results in command reinvocation
                    on the remote account.
     --host=HOST    Other host name. This results in command reinvocation on the
                    remote account.
     -v, --verbose  Verbose output mode.
     --debug        Output developer information and show exception tracebacks.


.. _command-register:

register
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: none

      Usage: cylc [prep] register [OPTIONS] [REG] [PATH] 
   
   Register the name REG for the suite definition in PATH. The suite server
   program can then be started, stopped, and targeted by name REG. (Note that
   "cylc run" can also register suites on the fly).
   
   Registration creates a suite run directory "~/cylc-run/REG/" containing a
   ".service/source" symlink to the suite definition PATH. The .service directory
   will also be used for server authentication files at run time.
   
   Suite names can be hierarchical, corresponding to the path under ~/cylc-run.
   
     % cylc register dogs/fido PATH
   Register PATH/suite.rc as dogs/fido, with run directory ~/cylc-run/dogs/fido.
   
     % cylc register dogs/fido
   Register $PWD/suite.rc as dogs/fido.
   
     % cylc register
   Register $PWD/suite.rc as the parent directory name: $(basename $PWD).
   
   The same suite can be registered with multiple names; this results in multiple
   suite run directories that link to the same suite definition.
   
   To "unregister" a suite, delete or rename its run directory (renaming it under
   ~/cylc-run effectively re-registers the original suite with the new name).
   
   Use of "--redirect" is required to allow an existing name (and run directory)
   to be associated with a different suite definition. This is potentially
   dangerous because the new suite will overwrite files in the existing run
   directory. You should consider deleting or renaming an existing run directory
   rather than just re-use it with another suite.
   
   Arguments:
      [REG]                Suite name
      [PATH]               Suite definition directory (defaults to $PWD)
   
   Options:
     -h, --help     show this help message and exit
     --redirect     Allow an existing suite name and run directory to be used
                    with another suite.
     --user=USER    Other user account name. This results in command reinvocation
                    on the remote account.
     --host=HOST    Other host name. This results in command reinvocation on the
                    remote account.
     -v, --verbose  Verbose output mode.
     --debug        Output developer information and show exception tracebacks.


.. _command-release:

release
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: none

      Usage: cylc [control] release|unhold [OPTIONS] REG [TASK_GLOB ...] 
   
   Release one or more held tasks (cylc release REG TASK_GLOB)
   or the whole suite (cylc release REG). Held tasks do not
   submit even if they are ready to run.
   
   See also 'cylc [control] hold'.
   
   TASK_GLOB is a pattern to match task proxies or task families,
   or groups of them:
   * [CYCLE-POINT-GLOB/]TASK-NAME-GLOB[:TASK-STATE]
   * [CYCLE-POINT-GLOB/]FAMILY-NAME-GLOB[:TASK-STATE]
   * TASK-NAME-GLOB[.CYCLE-POINT-GLOB][:TASK-STATE]
   * FAMILY-NAME-GLOB[.CYCLE-POINT-GLOB][:TASK-STATE]
   
   For example, to match:
   * all tasks in a cycle: '20200202T0000Z/*' or '*.20200202T0000Z'
   * all tasks in the submitted status: ':submitted'
   * retrying 'foo*' tasks in 0000Z cycles: 'foo*.*0000Z:retrying' or
     '*0000Z/foo*:retrying'
   * retrying tasks in 'BAR' family: '*/BAR:retrying' or 'BAR.*:retrying'
   * retrying tasks in 'BAR' or 'BAZ' families: '*/BA[RZ]:retrying' or
     'BA[RZ].*:retrying'
   
   Arguments:
      REG                           Suite name
      [TASK_GLOB ...]               Task matching patterns
   
   Options:
     -h, --help            show this help message and exit
     --user=USER           Other user account name. This results in command
                           reinvocation on the remote account.
     --host=HOST           Other host name. This results in command reinvocation
                           on the remote account.
     -v, --verbose         Verbose output mode.
     --debug               Output developer information and show exception
                           tracebacks.
     --port=INT            Suite port number on the suite host. NOTE: this is
                           retrieved automatically if non-interactive ssh is
                           configured to the suite host.
     --use-ssh             Use ssh to re-invoke the command on the suite host.
     --ssh-cylc=SSH_CYLC   Location of cylc executable on remote ssh commands.
     --no-login            Do not use a login shell to run remote ssh commands.
                           The default is to use a login shell.
     --comms-timeout=SEC, --pyro-timeout=SEC
                           Set a timeout for network connections to the running
                           suite. The default is no timeout. For task messaging
                           connections see site/user config file documentation.
     -f, --force           Do not ask for confirmation before acting. Note that
                           it is not necessary to use this option if interactive
                           command prompts have been disabled in the site/user
                           config files.


.. _command-reload:

reload
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: none

      Usage: cylc [control] reload [OPTIONS] REG 
   
   Tell a suite to reload its definition at run time. All settings
   including task definitions, with the exception of suite log
   configuration, can be changed on reload. Note that defined tasks can be
   be added to or removed from a running suite with the 'cylc insert' and
   'cylc remove' commands, without reloading. This command also allows
   addition and removal of actual task definitions, and therefore insertion
   of tasks that were not defined at all when the suite started (you will
   still need to manually insert a particular instance of a newly defined
   task). Live task proxies that are orphaned by a reload (i.e. their task
   definitions have been removed) will be removed from the task pool if
   they have not started running yet. Changes to task definitions take
   effect immediately, unless a task is already running at reload time.
   
   If the suite was started with Jinja2 template variables set on the
   command line (cylc run --set FOO=bar REG) the same template settings
   apply to the reload (only changes to the suite.rc file itself are
   reloaded).
   
   If the modified suite definition does not parse, failure to reload will
   be reported but no harm will be done to the running suite.
   
   Arguments:
      REG               Suite name
   
   Options:
     -h, --help            show this help message and exit
     --user=USER           Other user account name. This results in command
                           reinvocation on the remote account.
     --host=HOST           Other host name. This results in command reinvocation
                           on the remote account.
     -v, --verbose         Verbose output mode.
     --debug               Output developer information and show exception
                           tracebacks.
     --port=INT            Suite port number on the suite host. NOTE: this is
                           retrieved automatically if non-interactive ssh is
                           configured to the suite host.
     --use-ssh             Use ssh to re-invoke the command on the suite host.
     --ssh-cylc=SSH_CYLC   Location of cylc executable on remote ssh commands.
     --no-login            Do not use a login shell to run remote ssh commands.
                           The default is to use a login shell.
     --comms-timeout=SEC, --pyro-timeout=SEC
                           Set a timeout for network connections to the running
                           suite. The default is no timeout. For task messaging
                           connections see site/user config file documentation.
     -f, --force           Do not ask for confirmation before acting. Note that
                           it is not necessary to use this option if interactive
                           command prompts have been disabled in the site/user
                           config files.


.. _command-remote-init:

remote-init
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: none

      Usage: cylc [task] remote-init [--indirect-comm=ssh] UUID RUND
   
   (This command is for internal use.)
   Install suite service files on a task remote (i.e. a [owner@]host):
       .service/contact: All task -> suite communication methods.
       .service/passphrase: Direct task -> suite communication only.
   
   Content of items to install from a tar file read from STDIN.
   
   Return:
       0:
           On success or if initialisation not required:
           - Print SuiteSrvFilesManager.REMOTE_INIT_NOT_REQUIRED if initialisation
             not required (e.g. remote has shared file system with suite host).
           - Print SuiteSrvFilesManager.REMOTE_INIT_DONE on success.
       1:
           On failure.
   
   
   
   Arguments:
      UUID               UUID of current suite server process
      RUND               The run directory of the suite
   
   Options:
     -h, --help            show this help message and exit
     --indirect-comm=METHOD
                           specify use of indirect communication via e.g. ssh
     --user=USER           Other user account name. This results in command
                           reinvocation on the remote account.
     --host=HOST           Other host name. This results in command reinvocation
                           on the remote account.
     -v, --verbose         Verbose output mode.
     --debug               Output developer information and show exception
                           tracebacks.


.. _command-remote-tidy:

remote-tidy
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: none

      Usage: cylc [task] remote-tidy RUND
   
   (This command is for internal use.)
   Remove ".service/contact" from a task remote (i.e. a [owner@]host).
   Remove ".service" directory on the remote if emptied.
   
   
   
   Arguments:
      RUND               The run directory of the suite
   
   Options:
     -h, --help     show this help message and exit
     --user=USER    Other user account name. This results in command reinvocation
                    on the remote account.
     --host=HOST    Other host name. This results in command reinvocation on the
                    remote account.
     -v, --verbose  Verbose output mode.
     --debug        Output developer information and show exception tracebacks.


.. _command-remove:

remove
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: none

      Usage: cylc [control] remove [OPTIONS] REG TASK_GLOB [...] 
   
   Remove one or more tasks (cylc remove REG TASK_GLOB), or all tasks with a
   given cycle point (cylc remove REG *.POINT) from a running suite.
   
   Tasks will spawn successors first if they have not done so already.
   
   TASK_GLOB is a pattern to match task proxies or task families,
   or groups of them:
   * [CYCLE-POINT-GLOB/]TASK-NAME-GLOB[:TASK-STATE]
   * [CYCLE-POINT-GLOB/]FAMILY-NAME-GLOB[:TASK-STATE]
   * TASK-NAME-GLOB[.CYCLE-POINT-GLOB][:TASK-STATE]
   * FAMILY-NAME-GLOB[.CYCLE-POINT-GLOB][:TASK-STATE]
   
   For example, to match:
   * all tasks in a cycle: '20200202T0000Z/*' or '*.20200202T0000Z'
   * all tasks in the submitted status: ':submitted'
   * retrying 'foo*' tasks in 0000Z cycles: 'foo*.*0000Z:retrying' or
     '*0000Z/foo*:retrying'
   * retrying tasks in 'BAR' family: '*/BAR:retrying' or 'BAR.*:retrying'
   * retrying tasks in 'BAR' or 'BAZ' families: '*/BA[RZ]:retrying' or
     'BA[RZ].*:retrying'
   
   Arguments:
      REG                           Suite name
      TASK_GLOB [...]               Task matching patterns
   
   Options:
     -h, --help            show this help message and exit
     --no-spawn            Do not spawn successors before removal.
     --user=USER           Other user account name. This results in command
                           reinvocation on the remote account.
     --host=HOST           Other host name. This results in command reinvocation
                           on the remote account.
     -v, --verbose         Verbose output mode.
     --debug               Output developer information and show exception
                           tracebacks.
     --port=INT            Suite port number on the suite host. NOTE: this is
                           retrieved automatically if non-interactive ssh is
                           configured to the suite host.
     --use-ssh             Use ssh to re-invoke the command on the suite host.
     --ssh-cylc=SSH_CYLC   Location of cylc executable on remote ssh commands.
     --no-login            Do not use a login shell to run remote ssh commands.
                           The default is to use a login shell.
     --comms-timeout=SEC, --pyro-timeout=SEC
                           Set a timeout for network connections to the running
                           suite. The default is no timeout. For task messaging
                           connections see site/user config file documentation.
     -f, --force           Do not ask for confirmation before acting. Note that
                           it is not necessary to use this option if interactive
                           command prompts have been disabled in the site/user
                           config files.


.. _command-report-timings:

report-timings
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: none

      Usage: cylc [util] report-timings [OPTIONS] REG
   
   Retrieve suite timing information for wait and run time performance analysis.
   Raw output and summary output (in text or HTML format) are available.  Output
   is sent to standard output, unless an output filename is supplied.
   
   Summary Output (the default):
   Data stratified by host and batch system that provides a statistical
   summary of
       1. Queue wait time (duration between task submission and start times)
       2. Task run time (duration between start and succeed times)
       3. Total run time (duration between task submission and succeed times)
   Summary tables can be output in plain text format, or HTML with embedded SVG
   boxplots.  Both summary options require the Pandas library, and the HTML
   summary option requires the Matplotlib library.
   
   Raw Output:
   A flat list of tabular data that provides (for each task and cycle) the
       1. Time of successful submission
       2. Time of task start
       3. Time of task successful completion
   as well as information about the batch system and remote host to permit
   stratification/grouping if desired by downstream processors.
   
   Timings are shown only for succeeded tasks.
   
   For long-running and/or large suites (i.e. for suites with many task events),
   the database query to obtain the timing information may take some time.
   
   
   
   Arguments:
      REG               Suite name
   
   Options:
     -h, --help            show this help message and exit
     -r, --raw             Show raw timing output suitable for custom
                           diagnostics.
     -s, --summary         Show textual summary timing output for tasks.
     -w, --web-summary     Show HTML summary timing output for tasks.
     -O OUTPUT_FILENAME, --output-file=OUTPUT_FILENAME
                           Output to a specific file
     --user=USER           Other user account name. This results in command
                           reinvocation on the remote account.
     --host=HOST           Other host name. This results in command reinvocation
                           on the remote account.
     -v, --verbose         Verbose output mode.
     --debug               Output developer information and show exception
                           tracebacks.


.. _command-reset:

reset
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: none

      Usage: cylc [control] reset [OPTIONS] REG [TASK_GLOB ...] 
   
   Force tasks to a specified state, and modify their prerequisites and outputs
   accordingly.
   
   Outputs are automatically updated to reflect the new task state, except for
   custom message outputs - which can be manipulated directly with "--output".
   
   Prerequisites reflect the state of other  tasks; they are not changed except
   to unset them on resetting the task state to 'waiting' or earlier.
   
   To hold and release tasks use "cylc hold" and "cylc release".
   "cylc reset --state=spawn" is deprecated: use "cylc spawn" instead.
   
   
   TASK_GLOB is a pattern to match task proxies or task families,
   or groups of them:
   * [CYCLE-POINT-GLOB/]TASK-NAME-GLOB[:TASK-STATE]
   * [CYCLE-POINT-GLOB/]FAMILY-NAME-GLOB[:TASK-STATE]
   * TASK-NAME-GLOB[.CYCLE-POINT-GLOB][:TASK-STATE]
   * FAMILY-NAME-GLOB[.CYCLE-POINT-GLOB][:TASK-STATE]
   
   For example, to match:
   * all tasks in a cycle: '20200202T0000Z/*' or '*.20200202T0000Z'
   * all tasks in the submitted status: ':submitted'
   * retrying 'foo*' tasks in 0000Z cycles: 'foo*.*0000Z:retrying' or
     '*0000Z/foo*:retrying'
   * retrying tasks in 'BAR' family: '*/BAR:retrying' or 'BAR.*:retrying'
   * retrying tasks in 'BAR' or 'BAZ' families: '*/BA[RZ]:retrying' or
     'BA[RZ].*:retrying'
   
   Arguments:
      REG                           Suite name
      [TASK_GLOB ...]               Task matching patterns
   
   Options:
     -h, --help            show this help message and exit
     -s STATE, --state=STATE
                           Reset task state to STATE, can be waiting, submitted,
                           running, failed, succeeded, submit-failed, expired
     -O OUTPUT, --output=OUTPUT
                           Find task output by message string or trigger string,
                           set complete or incomplete with !OUTPUT, '*' to set
                           all complete, '!*' to set all incomplete. Can be used
                           more than once to reset multiple task outputs.
     --user=USER           Other user account name. This results in command
                           reinvocation on the remote account.
     --host=HOST           Other host name. This results in command reinvocation
                           on the remote account.
     -v, --verbose         Verbose output mode.
     --debug               Output developer information and show exception
                           tracebacks.
     --port=INT            Suite port number on the suite host. NOTE: this is
                           retrieved automatically if non-interactive ssh is
                           configured to the suite host.
     --use-ssh             Use ssh to re-invoke the command on the suite host.
     --ssh-cylc=SSH_CYLC   Location of cylc executable on remote ssh commands.
     --no-login            Do not use a login shell to run remote ssh commands.
                           The default is to use a login shell.
     --comms-timeout=SEC, --pyro-timeout=SEC
                           Set a timeout for network connections to the running
                           suite. The default is no timeout. For task messaging
                           connections see site/user config file documentation.
     -f, --force           Do not ask for confirmation before acting. Note that
                           it is not necessary to use this option if interactive
                           command prompts have been disabled in the site/user
                           config files.


.. _command-restart:

restart
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: none

      Usage: cylc [control] restart [OPTIONS] [REG] 
   
   Start a suite run from the previous state. To start from scratch (cold or warm
   start) see the 'cylc run' command.
   
   The scheduler runs as a daemon unless you specify --no-detach.
   
   Tasks recorded as submitted or running are polled at start-up to determine what
   happened to them while the suite was down.
   
   Arguments:
      [REG]               Suite name
   
   Options:
     -h, --help            show this help message and exit
     --non-daemon          (deprecated: use --no-detach)
     -n, --no-detach       Do not daemonize the suite
     -a, --no-auto-shutdown
                           Do not shut down the suite automatically when all
                           tasks have finished. This flag overrides the
                           corresponding suite config item.
     --profile             Output profiling (performance) information
     --checkpoint=CHECKPOINT-ID
                           Specify the ID of a checkpoint to restart from
     --ignore-final-cycle-point
                           Ignore the final cycle point in the suite run
                           database. If one is specified in the suite definition
                           it will be used, however.
     --ignore-initial-cycle-point
                           Ignore the initial cycle point in the suite run
                           database. If one is specified in the suite definition
                           it will be used, however.
     --until=CYCLE_POINT   Shut down after all tasks have PASSED this cycle
                           point.
     --hold                Hold (don't run tasks) immediately on starting.
     --hold-after=CYCLE_POINT
                           Hold (don't run tasks) AFTER this cycle point.
     -m STRING, --mode=STRING
                           Run mode: live, dummy, dummy-local, simulation
                           (default live).
     --reference-log       Generate a reference log for use in reference tests.
     --reference-test      Do a test run against a previously generated reference
                           log.
     --host=HOST           Specify the host on which to start-up the suite.
                           Without this set a host will be selected using the
                           'suite servers' global config.
     --user=USER           Other user account name. This results in command
                           reinvocation on the remote account.
     -v, --verbose         Verbose output mode.
     --debug               Output developer information and show exception
                           tracebacks.
     -s NAME=VALUE, --set=NAME=VALUE
                           Set the value of a Jinja2 template variable in the
                           suite definition. This option can be used multiple
                           times on the command line. NOTE: these settings
                           persist across suite restarts, but can be set again on
                           the "cylc restart" command line if they need to be
                           overridden.
     --set-file=FILE       Set the value of Jinja2 template variables in the
                           suite definition from a file containing NAME=VALUE
                           pairs (one per line). NOTE: these settings persist
                           across suite restarts, but can be set again on the
                           "cylc restart" command line if they need to be
                           overridden.


.. _command-run:

run
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: none

      Usage: cylc [control] run|start [OPTIONS] [[REG] [START_POINT] ]
   
   Start a suite run from scratch, ignoring dependence prior to the start point.
   
   WARNING: this will wipe out previous suite state. To restart from a previous
   state, see 'cylc restart --help'.
   
   The scheduler will run as a daemon unless you specify --no-detach.
   
   If the suite is not already registered (by "cylc register" or a previous run)
   it will be registered on the fly before start up.
   
   % cylc run REG
     Run the suite registered with name REG.
   
   % cylc run
     Register $PWD/suite.rc as $(basename $PWD) and run it.
    (Note REG must be given explicitly if START_POINT is on the command line.)
   
   A "cold start" (the default) starts from the suite initial cycle point
   (specified in the suite.rc or on the command line). Any dependence on tasks
   prior to the suite initial cycle point is ignored.
   
   A "warm start" (-w/--warm) starts from a given cycle point later than the suite
   initial cycle point (specified in the suite.rc). Any dependence on tasks prior
   to the given warm start cycle point is ignored. The suite initial cycle point
   is preserved.
   
   Arguments:
      [REG]                       Suite name
      [START_POINT]               Initial cycle point or 'now';
                                  overrides the suite definition.
   
   Options:
     -h, --help            show this help message and exit
     --non-daemon          (deprecated: use --no-detach)
     -n, --no-detach       Do not daemonize the suite
     -a, --no-auto-shutdown
                           Do not shut down the suite automatically when all
                           tasks have finished. This flag overrides the
                           corresponding suite config item.
     --profile             Output profiling (performance) information
     -w, --warm            Warm start the suite. The default is to cold start.
     --ict                 Does nothing, option for backward compatibility only
     --until=CYCLE_POINT   Shut down after all tasks have PASSED this cycle
                           point.
     --hold                Hold (don't run tasks) immediately on starting.
     --hold-after=CYCLE_POINT
                           Hold (don't run tasks) AFTER this cycle point.
     -m STRING, --mode=STRING
                           Run mode: live, dummy, dummy-local, simulation
                           (default live).
     --reference-log       Generate a reference log for use in reference tests.
     --reference-test      Do a test run against a previously generated reference
                           log.
     --host=HOST           Specify the host on which to start-up the suite.
                           Without this set a host will be selected using the
                           'suite servers' global config.
     --user=USER           Other user account name. This results in command
                           reinvocation on the remote account.
     -v, --verbose         Verbose output mode.
     --debug               Output developer information and show exception
                           tracebacks.
     -s NAME=VALUE, --set=NAME=VALUE
                           Set the value of a Jinja2 template variable in the
                           suite definition. This option can be used multiple
                           times on the command line. NOTE: these settings
                           persist across suite restarts, but can be set again on
                           the "cylc restart" command line if they need to be
                           overridden.
     --set-file=FILE       Set the value of Jinja2 template variables in the
                           suite definition from a file containing NAME=VALUE
                           pairs (one per line). NOTE: these settings persist
                           across suite restarts, but can be set again on the
                           "cylc restart" command line if they need to be
                           overridden.


.. _command-scan:

scan
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: none

      Usage: cylc [discovery] scan [OPTIONS] [HOSTS ...]
   
   Print information about running suites.
   
   Use the -o/--suite-owner option to get information of running suites for other
   users.
   
   Suite passphrases are not needed to get identity information (name and owner).
   Titles, descriptions, state totals, and cycle point state totals may also be
   revealed publicly, depending on global and suite authentication settings. Suite
   passphrases still grant full access regardless of what is revealed publicly.
   
   WARNING: a suite suspended with Ctrl-Z will cause port scans to hang until the
   connection times out (see --comms-timeout).
   
   Options:
     -h, --help            show this help message and exit
     --ordered             Display results in order, this may take longer.
     -n PATTERN, --name=PATTERN
                           List suites with name matching PATTERN (regular
                           expression). Defaults to any name. Can be used
                           multiple times.
     -o PATTERN, --suite-owner=PATTERN
                           List suites with owner matching PATTERN (regular
                           expression). Defaults to current user. Use '.*' to
                           match all known users. Can be used multiple times.
     -d, --describe        Print suite metadata if available.
     -s, --state-totals    Print number of tasks in each state if available
                           (total, and by cycle point).
     -f, --full            Print all available information about each suite.
     --color=COLOR, --colour=COLOR
                           Colorize the output, can be "always", "never" or
                           "auto".
     --comms-timeout=SEC   Set a timeout for network connections to each running
                           suite. The default is 5 seconds.
     -t FORMAT, --format=FORMAT
                           Set output format:  * plain (default) - text format
                           for interactive use  * raw - parsable format
                           (suite|owner|host|property|value)  * json - JSON
                           format ({suite: {owner: OWNER, host: HOST ...)
     --user=USER           Other user account name. This results in command
                           reinvocation on the remote account.
     --host=HOST           Other host name. This results in command reinvocation
                           on the remote account.
     -v, --verbose         Verbose output mode.
     --debug               Output developer information and show exception
                           tracebacks.
     --port=INT            Suite port number on the suite host. NOTE: this is
                           retrieved automatically if non-interactive ssh is
                           configured to the suite host.
     --use-ssh             Use ssh to re-invoke the command on the suite host.
     --ssh-cylc=SSH_CYLC   Location of cylc executable on remote ssh commands.
     --no-login            Do not use a login shell to run remote ssh commands.
                           The default is to use a login shell.


.. _command-scp-transfer:

scp-transfer
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: none

      Usage: cylc [util] scp-transfer [OPTIONS]
   
   An scp wrapper for transferring a list of files and/or directories
   at once. The source and target scp URLs can be local or remote (scp
   can transfer files between two remote hosts). Passwordless ssh must
   be configured appropriately.
   
   ENVIRONMENT VARIABLE INPUTS:
   $SRCE  - list of sources (files or directories) as scp URLs.
   $DEST  - parallel list of targets as scp URLs.
   The source and destination lists should be space-separated.
   
   We let scp determine the validity of source and target URLs.
   Target directories are created pre-copy if they don't exist.
   
   Options:
    -v     - verbose: print scp stdout.
    --help - print this usage message.


.. _command-search:

search
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: none

      Usage: cylc [prep] search|grep [OPTIONS] SUITE PATTERN [PATTERN2...] 
   
   Search for pattern matches in suite definitions and any files in the
   suite bin directory. Matches are reported by line number and suite
   section. An unquoted list of PATTERNs will be converted to an OR'd
   pattern. Note that the order of command line arguments conforms to
   normal cylc command usage (suite name first) not that of the grep
   command.
   
   Note that this command performs a text search on the suite definition,
   it does not search the data structure that results from parsing the
   suite definition - so it will not report implicit default settings.
   
   For case insensitive matching use '(?i)PATTERN'.
   
   Arguments:
      SUITE                       Suite name or path
      PATTERN                     Python-style regular expression
      [PATTERN2...]               Additional search patterns
   
   Options:
     -h, --help           show this help message and exit
     -x                   Do not search in the suite bin directory
     --user=USER          Other user account name. This results in command
                          reinvocation on the remote account.
     --host=HOST          Other host name. This results in command reinvocation
                          on the remote account.
     -v, --verbose        Verbose output mode.
     --debug              Output developer information and show exception
                          tracebacks.
     --suite-owner=OWNER  Specify suite owner


.. _command-set-verbosity:

set-verbosity
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: none

      Usage: cylc [control] set-verbosity [OPTIONS] REG LEVEL 
   
   Change the logging severity level of a running suite.  Only messages at
   or above the chosen severity level will be logged; for example, if you
   choose WARNING, only warnings and critical messages will be logged.
   
   Arguments:
      REG                 Suite name
      LEVEL               INFO, NORMAL, WARNING, ERROR, CRITICAL, DEBUG
   
   Options:
     -h, --help            show this help message and exit
     --user=USER           Other user account name. This results in command
                           reinvocation on the remote account.
     --host=HOST           Other host name. This results in command reinvocation
                           on the remote account.
     -v, --verbose         Verbose output mode.
     --debug               Output developer information and show exception
                           tracebacks.
     --port=INT            Suite port number on the suite host. NOTE: this is
                           retrieved automatically if non-interactive ssh is
                           configured to the suite host.
     --use-ssh             Use ssh to re-invoke the command on the suite host.
     --ssh-cylc=SSH_CYLC   Location of cylc executable on remote ssh commands.
     --no-login            Do not use a login shell to run remote ssh commands.
                           The default is to use a login shell.
     --comms-timeout=SEC, --pyro-timeout=SEC
                           Set a timeout for network connections to the running
                           suite. The default is no timeout. For task messaging
                           connections see site/user config file documentation.
     -f, --force           Do not ask for confirmation before acting. Note that
                           it is not necessary to use this option if interactive
                           command prompts have been disabled in the site/user
                           config files.


.. _command-show:

show
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: none

      Usage: cylc [info] show [OPTIONS] REG [TASKS ...] 
   
   Interrogate a suite server program for the suite metadata; or for the metadata
   of one of its tasks; or for the current state of the prerequisites, outputs,
   and clock-triggering of a specific task instance.
   TASK_GLOB is a pattern to match task proxies or task families,
   or groups of them:
   * [CYCLE-POINT-GLOB/]TASK-NAME-GLOB[:TASK-STATE]
   * [CYCLE-POINT-GLOB/]FAMILY-NAME-GLOB[:TASK-STATE]
   * TASK-NAME-GLOB[.CYCLE-POINT-GLOB][:TASK-STATE]
   * FAMILY-NAME-GLOB[.CYCLE-POINT-GLOB][:TASK-STATE]
   
   For example, to match:
   * all tasks in a cycle: '20200202T0000Z/*' or '*.20200202T0000Z'
   * all tasks in the submitted status: ':submitted'
   * retrying 'foo*' tasks in 0000Z cycles: 'foo*.*0000Z:retrying' or
     '*0000Z/foo*:retrying'
   * retrying tasks in 'BAR' family: '*/BAR:retrying' or 'BAR.*:retrying'
   * retrying tasks in 'BAR' or 'BAZ' families: '*/BA[RZ]:retrying' or
     'BA[RZ].*:retrying'
   
   Arguments:
      REG                       Suite name
      [TASKS ...]               Task names or ids (name.cycle)
   
   Options:
     -h, --help            show this help message and exit
     --list-prereqs        Print a task's pre-requisites as a list.
     --json                Print output in JSON format.
     --user=USER           Other user account name. This results in command
                           reinvocation on the remote account.
     --host=HOST           Other host name. This results in command reinvocation
                           on the remote account.
     -v, --verbose         Verbose output mode.
     --debug               Output developer information and show exception
                           tracebacks.
     --port=INT            Suite port number on the suite host. NOTE: this is
                           retrieved automatically if non-interactive ssh is
                           configured to the suite host.
     --use-ssh             Use ssh to re-invoke the command on the suite host.
     --ssh-cylc=SSH_CYLC   Location of cylc executable on remote ssh commands.
     --no-login            Do not use a login shell to run remote ssh commands.
                           The default is to use a login shell.
     --comms-timeout=SEC, --pyro-timeout=SEC
                           Set a timeout for network connections to the running
                           suite. The default is no timeout. For task messaging
                           connections see site/user config file documentation.


.. _command-spawn:

spawn
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: none

      Usage: cylc [control] spawn [OPTIONS] REG [TASK_GLOB ...] 
   
   Force one or more task proxies to spawn successors at the next cycle point
   in their sequences.  This is useful if you need to run successive instances
   of a task out of order.
   
   TASK_GLOB is a pattern to match task proxies or task families,
   or groups of them:
   * [CYCLE-POINT-GLOB/]TASK-NAME-GLOB[:TASK-STATE]
   * [CYCLE-POINT-GLOB/]FAMILY-NAME-GLOB[:TASK-STATE]
   * TASK-NAME-GLOB[.CYCLE-POINT-GLOB][:TASK-STATE]
   * FAMILY-NAME-GLOB[.CYCLE-POINT-GLOB][:TASK-STATE]
   
   For example, to match:
   * all tasks in a cycle: '20200202T0000Z/*' or '*.20200202T0000Z'
   * all tasks in the submitted status: ':submitted'
   * retrying 'foo*' tasks in 0000Z cycles: 'foo*.*0000Z:retrying' or
     '*0000Z/foo*:retrying'
   * retrying tasks in 'BAR' family: '*/BAR:retrying' or 'BAR.*:retrying'
   * retrying tasks in 'BAR' or 'BAZ' families: '*/BA[RZ]:retrying' or
     'BA[RZ].*:retrying'
   
   Arguments:
      REG                           Suite name
      [TASK_GLOB ...]               Task matching patterns
   
   Options:
     -h, --help            show this help message and exit
     --user=USER           Other user account name. This results in command
                           reinvocation on the remote account.
     --host=HOST           Other host name. This results in command reinvocation
                           on the remote account.
     -v, --verbose         Verbose output mode.
     --debug               Output developer information and show exception
                           tracebacks.
     --port=INT            Suite port number on the suite host. NOTE: this is
                           retrieved automatically if non-interactive ssh is
                           configured to the suite host.
     --use-ssh             Use ssh to re-invoke the command on the suite host.
     --ssh-cylc=SSH_CYLC   Location of cylc executable on remote ssh commands.
     --no-login            Do not use a login shell to run remote ssh commands.
                           The default is to use a login shell.
     --comms-timeout=SEC, --pyro-timeout=SEC
                           Set a timeout for network connections to the running
                           suite. The default is no timeout. For task messaging
                           connections see site/user config file documentation.
     -f, --force           Do not ask for confirmation before acting. Note that
                           it is not necessary to use this option if interactive
                           command prompts have been disabled in the site/user
                           config files.


.. _command-stop:

stop
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: none

      Usage: cylc [control] stop|shutdown [OPTIONS] REG [STOP] 
   
   Tell a suite server program to shut down. In order to prevent failures going
   unnoticed, suites only shut down automatically at a final cycle point if no
   failed tasks are present. There are several shutdown methods:
   
     1. (default) stop after current active tasks finish
     2. (--now) stop immediately, orphaning current active tasks
     3. (--kill) stop after killing current active tasks
     4. (with STOP as a cycle point) stop after cycle point STOP
     5. (with STOP as a task ID) stop after task ID STOP has succeeded
     6. (--wall-clock=T) stop after time T (an ISO 8601 date-time format e.g.
        CCYYMMDDThh:mm, CCYY-MM-DDThh, etc).
   
   Tasks that become ready after the shutdown is ordered will be submitted
   immediately if the suite is restarted.  Remaining task event handlers and job
   poll and kill commands, however, will be executed prior to shutdown, unless
   --now is used.
   
   This command exits immediately unless --max-polls is greater than zero, in
   which case it polls to wait for suite shutdown.
   
   Arguments:
      REG                  Suite name
      [STOP]               a/ task POINT (cycle point), or
                               b/ ISO 8601 date-time (clock time), or
                               c/ TASK (task ID).
   
   Options:
     -h, --help            show this help message and exit
     -k, --kill            Shut down after killing currently active tasks.
     -n, --now             Shut down without waiting for active tasks to
                           complete. If this option is specified once, wait for
                           task event handler, job poll/kill to complete. If this
                           option is specified more than once, tell the suite to
                           terminate immediately.
     -w STOP, --wall-clock=STOP
                           Shut down after time STOP (ISO 8601 formatted)
     --max-polls=INT       Maximum number of polls (default 0).
     --interval=SECS       Polling interval in seconds (default 60).
     --user=USER           Other user account name. This results in command
                           reinvocation on the remote account.
     --host=HOST           Other host name. This results in command reinvocation
                           on the remote account.
     -v, --verbose         Verbose output mode.
     --debug               Output developer information and show exception
                           tracebacks.
     --port=INT            Suite port number on the suite host. NOTE: this is
                           retrieved automatically if non-interactive ssh is
                           configured to the suite host.
     --use-ssh             Use ssh to re-invoke the command on the suite host.
     --ssh-cylc=SSH_CYLC   Location of cylc executable on remote ssh commands.
     --no-login            Do not use a login shell to run remote ssh commands.
                           The default is to use a login shell.
     --comms-timeout=SEC, --pyro-timeout=SEC
                           Set a timeout for network connections to the running
                           suite. The default is no timeout. For task messaging
                           connections see site/user config file documentation.
     -f, --force           Do not ask for confirmation before acting. Note that
                           it is not necessary to use this option if interactive
                           command prompts have been disabled in the site/user
                           config files.


.. _command-submit:

submit
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: none

      Usage: cylc [task] submit|single [OPTIONS] REG TASK [...] 
   
   Submit a single task to run just as it would be submitted by its suite.  Task
   messaging commands will print to stdout but will not attempt to communicate
   with the suite (which does not need to be running).
   
   For tasks present in the suite graph the given cycle point is adjusted up to
   the next valid cycle point for the task. For tasks defined under runtime but
   not present in the graph, the given cycle point is assumed to be valid.
   
   WARNING: do not 'cylc submit' a task that is running in its suite at the
   same time - both instances will attempt to write to the same job logs.
   
   Arguments:
      REG                      Suite name
      TASK [...]               Family or task ID (NAME.CYCLE_POINT)
   
   Options:
     -h, --help            show this help message and exit
     -d, --dry-run         Generate the job script for the task, but don't submit
                           it.
     --user=USER           Other user account name. This results in command
                           reinvocation on the remote account.
     --host=HOST           Other host name. This results in command reinvocation
                           on the remote account.
     -v, --verbose         Verbose output mode.
     --debug               Output developer information and show exception
                           tracebacks.
     -s NAME=VALUE, --set=NAME=VALUE
                           Set the value of a Jinja2 template variable in the
                           suite definition. This option can be used multiple
                           times on the command line. NOTE: these settings
                           persist across suite restarts, but can be set again on
                           the "cylc restart" command line if they need to be
                           overridden.
     --set-file=FILE       Set the value of Jinja2 template variables in the
                           suite definition from a file containing NAME=VALUE
                           pairs (one per line). NOTE: these settings persist
                           across suite restarts, but can be set again on the
                           "cylc restart" command line if they need to be
                           overridden.
     --icp=CYCLE_POINT     Set initial cycle point. Required if not defined in
                           suite.rc.


.. _command-suite-state:

suite-state
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: none

      Usage: cylc suite-state REG [OPTIONS]
   
   Print task states retrieved from a suite database; or (with --task,
   --point, and --status) poll until a given task reaches a given state; or (with
   --task, --point, and --message) poll until a task receives a given message.
   Polling is configurable with --interval and --max-polls; for a one-off
   check use --max-polls=1. The suite database does not need to exist at
   the time polling commences but allocated polls are consumed waiting for
   it (consider max-polls*interval as an overall timeout).
   
   Note for non-cycling tasks --point=1 must be provided.
   
   For your own suites the database location is determined by your
   site/user config. For other suites, e.g. those owned by others, or
   mirrored suite databases, use --run-dir=DIR to specify the location.
   
   Example usages:
     cylc suite-state REG --task=TASK --point=POINT --status=STATUS
   returns 0 if TASK.POINT reaches STATUS before the maximum number of
   polls, otherwise returns 1.
   
     cylc suite-state REG --task=TASK --point=POINT --status=STATUS --offset=PT6H
   adds 6 hours to the value of CYCLE for carrying out the polling operation.
   
     cylc suite-state REG --task=TASK --status=STATUS --task-point
   uses CYLC_TASK_CYCLE_POINT environment variable as the value for the CYCLE
   to poll. This is useful when you want to use cylc suite-state in a cylc task.
   
   
   Arguments:
      REG               Suite name
   
   Options:
     -h, --help            show this help message and exit
     -t TASK, --task=TASK  Specify a task to check the state of.
     -p CYCLE, --point=CYCLE
                           Specify the cycle point to check task states for.
     -T, --task-point      Use the CYLC_TASK_CYCLE_POINT environment variable as
                           the cycle point to check task states for. Shorthand
                           for --point=$CYLC_TASK_CYCLE_POINT
     --template=TEMPLATE   Remote cyclepoint template (IGNORED - this is now
                           determined automatically).
     -d DIR, --run-dir=DIR
                           The top level cylc run directory if non-standard. The
                           database should be DIR/REG/log/db. Use to interrogate
                           suites owned by others, etc.; see note above.
     -s OFFSET, --offset=OFFSET
                           Specify an offset to add to the targeted cycle point
     -S STATUS, --status=STATUS
                           Specify a particular status or triggering condition to
                           check for. Valid triggering conditions to check for
                           include: 'fail', 'finish', 'start', 'submit' and
                           'succeed'. Valid states to check for include:
                           'runahead', 'waiting', 'held', 'queued', 'expired',
                           'ready', 'submit-failed', 'submit-retrying',
                           'submitted', 'retrying', 'running', 'failed' and
                           'succeeded'.
     -O MSG, -m MSG, --output=MSG, --message=MSG
                           Check custom task output by message string or trigger
                           string.
     --max-polls=INT       Maximum number of polls (default 10).
     --interval=SECS       Polling interval in seconds (default 60).
     --user=USER           Other user account name. This results in command
                           reinvocation on the remote account.
     --host=HOST           Other host name. This results in command reinvocation
                           on the remote account.
     -v, --verbose         Verbose output mode.
     --debug               Output developer information and show exception
                           tracebacks.


.. _command-trigger:

trigger
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: none

      Usage: cylc [control] trigger [OPTIONS] REG [TASK_GLOB ...] 
   
   Manually trigger one or more tasks. Waiting tasks will be queued (cylc internal
   queues) and will submit as normal when released by the queue; queued tasks will
   submit immediately even if that violates the queue limit (so you may need to
   trigger a queue-limited task twice to get it to submit).
   
   For single tasks you can use "--edit" to edit the generated job script before
   it submits, to apply one-off changes. A diff between the original and edited
   job script will be saved to the task job log directory.
   
   TASK_GLOB is a pattern to match task proxies or task families,
   or groups of them:
   * [CYCLE-POINT-GLOB/]TASK-NAME-GLOB[:TASK-STATE]
   * [CYCLE-POINT-GLOB/]FAMILY-NAME-GLOB[:TASK-STATE]
   * TASK-NAME-GLOB[.CYCLE-POINT-GLOB][:TASK-STATE]
   * FAMILY-NAME-GLOB[.CYCLE-POINT-GLOB][:TASK-STATE]
   
   For example, to match:
   * all tasks in a cycle: '20200202T0000Z/*' or '*.20200202T0000Z'
   * all tasks in the submitted status: ':submitted'
   * retrying 'foo*' tasks in 0000Z cycles: 'foo*.*0000Z:retrying' or
     '*0000Z/foo*:retrying'
   * retrying tasks in 'BAR' family: '*/BAR:retrying' or 'BAR.*:retrying'
   * retrying tasks in 'BAR' or 'BAZ' families: '*/BA[RZ]:retrying' or
     'BA[RZ].*:retrying'
   
   Arguments:
      REG                           Suite name
      [TASK_GLOB ...]               Task matching patterns
   
   Options:
     -h, --help            show this help message and exit
     -e, --edit            Manually edit the job script before running it.
     -g, --geditor         (with --edit) force use of the configured GUI editor.
     --user=USER           Other user account name. This results in command
                           reinvocation on the remote account.
     --host=HOST           Other host name. This results in command reinvocation
                           on the remote account.
     -v, --verbose         Verbose output mode.
     --debug               Output developer information and show exception
                           tracebacks.
     --port=INT            Suite port number on the suite host. NOTE: this is
                           retrieved automatically if non-interactive ssh is
                           configured to the suite host.
     --use-ssh             Use ssh to re-invoke the command on the suite host.
     --ssh-cylc=SSH_CYLC   Location of cylc executable on remote ssh commands.
     --no-login            Do not use a login shell to run remote ssh commands.
                           The default is to use a login shell.
     --comms-timeout=SEC, --pyro-timeout=SEC
                           Set a timeout for network connections to the running
                           suite. The default is no timeout. For task messaging
                           connections see site/user config file documentation.
     -f, --force           Do not ask for confirmation before acting. Note that
                           it is not necessary to use this option if interactive
                           command prompts have been disabled in the site/user
                           config files.


.. _command-validate:

validate
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: none

      Usage: cylc [prep] validate [OPTIONS] SUITE 
   
   Validate a suite definition.
   
   If the suite definition uses include-files reported line numbers
   will correspond to the inlined version seen by the parser; use
   'cylc view -i,--inline SUITE' for comparison.
   
   Arguments:
      SUITE               Suite name or path
   
   Options:
     -h, --help            show this help message and exit
     --strict              Fail any use of unsafe or experimental features.
                           Currently this just means naked dummy tasks (tasks
                           with no corresponding runtime section) as these may
                           result from unintentional typographic errors in task
                           names.
     -o FILENAME, --output=FILENAME
                           Specify a file name to dump the processed suite.rc.
     --profile             Output profiling (performance) information
     -u RUN_MODE, --run-mode=RUN_MODE
                           Validate for run mode.
     --user=USER           Other user account name. This results in command
                           reinvocation on the remote account.
     --host=HOST           Other host name. This results in command reinvocation
                           on the remote account.
     -v, --verbose         Verbose output mode.
     --debug               Output developer information and show exception
                           tracebacks.
     --suite-owner=OWNER   Specify suite owner
     -s NAME=VALUE, --set=NAME=VALUE
                           Set the value of a Jinja2 template variable in the
                           suite definition. This option can be used multiple
                           times on the command line. NOTE: these settings
                           persist across suite restarts, but can be set again on
                           the "cylc restart" command line if they need to be
                           overridden.
     --set-file=FILE       Set the value of Jinja2 template variables in the
                           suite definition from a file containing NAME=VALUE
                           pairs (one per line). NOTE: these settings persist
                           across suite restarts, but can be set again on the
                           "cylc restart" command line if they need to be
                           overridden.
     --icp=CYCLE_POINT     Set initial cycle point. Required if not defined in
                           suite.rc.


.. _command-view:

view
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: none

      Usage: cylc [prep] view [OPTIONS] SUITE 
   
   View a read-only temporary copy of suite NAME's suite.rc file, in your
   editor, after optional include-file inlining and Jinja2 preprocessing.
   
   The edit process is spawned in the foreground as follows:
     % <editor> suite.rc
   Where <editor> can be set in cylc global config.
   
   For remote host or owner, the suite will be printed to stdout unless
   the '-g,--gui' flag is used to spawn a remote GUI edit session.
   
   See also 'cylc [prep] edit'.
   
   Arguments:
      SUITE               Suite name or path
   
   Options:
     -h, --help            show this help message and exit
     -i, --inline          Inline include-files.
     -e, --empy            View after EmPy template processing (implies
                           '-i/--inline' as well).
     -j, --jinja2          View after Jinja2 template processing (implies
                           '-i/--inline' as well).
     -p, --process         View after all processing (EmPy, Jinja2, inlining,
                           line-continuation joining).
     -m, --mark            (With '-i') Mark inclusions in the left margin.
     -l, --label           (With '-i') Label file inclusions with the file name.
                           Line numbers will not correspond to those reported by
                           the parser.
     --single              (With '-i') Inline only the first instances of any
                           multiply-included files. Line numbers will not
                           correspond to those reported by the parser.
     -c, --cat             Concatenate continuation lines (line numbers will not
                           correspond to those reported by the parser).
     -g, --gui             Force use of the configured GUI editor.
     --stdout              Print the suite definition to stdout.
     --mark-for-edit       (With '-i') View file inclusion markers as for 'cylc
                           edit --inline'.
     --user=USER           Other user account name. This results in command
                           reinvocation on the remote account.
     --host=HOST           Other host name. This results in command reinvocation
                           on the remote account.
     -v, --verbose         Verbose output mode.
     --debug               Output developer information and show exception
                           tracebacks.
     --suite-owner=OWNER   Specify suite owner
     -s NAME=VALUE, --set=NAME=VALUE
                           Set the value of a Jinja2 template variable in the
                           suite definition. This option can be used multiple
                           times on the command line. NOTE: these settings
                           persist across suite restarts, but can be set again on
                           the "cylc restart" command line if they need to be
                           overridden.
     --set-file=FILE       Set the value of Jinja2 template variables in the
                           suite definition from a file containing NAME=VALUE
                           pairs (one per line). NOTE: these settings persist
                           across suite restarts, but can be set again on the
                           "cylc restart" command line if they need to be
                           overridden.

