.. _troubleshooting:

Troubleshooting
===============

.. Generate a local table of contents to make it easier to skim the entries on
   this page.

.. contents::
   :depth: 3
   :local:
   :backlinks: none


.. _troubleshooting.log_files:

Log Files
---------

If things have gone wrong and you're not sure why, there are few files which
you'll find in the workflow's :term:`run directory` that should contain the
required information to work out what's going on:

``log/scheduler/log``
   There's a log file for each workflow in
   ``~/cylc-run/<workflow>/log/scheduler/log``.

   This records all the essential information including every job submission
   and task state change.

   You can view this in the GUI, Tui or on the command line using
   ``cylc cat-log <workflow>``.
``job.err``
   This contains the stderr captured when the job ran. It's useful for
   debugging job failures.

   You can view this in the GUI, Tui or on the command line using
   ``cylc cat-log <workflow>//<cycle>/<task>/<job> -f e``.
``job-activity.log``
   This file records the interaction Cylc has had with a job, namely submission
   and polling. This can be useful in determining the cause of job submission
   failures.

   You can view this in the GUI, Tui or on the command line using
   ``cylc cat-log <workflow>//<cycle>/<task>/<job> -f a``.

Additionally, these directories contain extra information which can be useful
for debugging some specific issues:

``log/install/``
   Contains logging from local workflow installation (e.g.``cylc install``).

   This can be useful for inspecting Rose file installation.
``log/remote-install/``
   Records information about file installation on remote platforms
   (see :ref:`RemoteInit`).
``log/config/``
   Records the workflow configuration (and the Rose suite configuration if one
   is used).

   These files can allow you to see how the configuration was changed between
   restarts and reloads.

   Each time a workflow is

   * Played for the first time
   * Played from stopped
   * Reloaded

   the configuration used is recorded in a file in ``log/config``.
   This provides a series of snapshots of the configuration.
   These files are named:

   ``<LOG FILE NUMBER>-<EVENT>-<RESTART NUMBER>``.

   If for example we did:

   .. code-block:: console

      # Command            # File created
      cylc play workflow   # 01-start-01.cylc
      cylc vr workflow     # 02-reload-01.cylc
      cylc stop workflow
      cylc play workflow   # 03-restart-02.cylc


Shell Login/Profile Files
-------------------------

Cylc runs many commands using
`Bash login shells <https://linuxhandbook.com/login-shell/>`_.

This allows you to configure aspects of Cylc's behaviour using login files
such as ``.bash_profile`` and ``.bashrc``.

However, it also means that the contents of these files can interfere with
Cylc (and potentially other systems too).

If you have things in your login files which are only intended for use in
interactive terminal sessions, wrap them inside an ``if`` block so they only
run for interactive sessions like so:

.. code-block:: bash

   if [[ $- == *i* ]]; then
      # only run this for interactive (terminal) sessions
      # (and not for non-interactive login sessions)
      echo "Hello $USER"
      alias rsync='rsync -v'
      conda activate my_env
      export PS1="\$ $(tput bold)[$PREFIX]$(tput sgr 0) "
   fi

   # this runs for all sessions including non-interactive login sessions
   export PATH="$HOME/bin:$PATH"
   export MY_LIB_PATH="$HOME/my-lib/1.0/"

Some things to check your login files for:

* Don't write to stdout (e.g. using ``echo`` or ``printf``), this can interfere
  with command output.
* Avoid loading modules or environments by default, you can create short cuts
  for loading these using functions, aliases or commands.
* Don't add non-existent directories into your ``$PATH``, this can cause
  commands to hang.
* Always prepend or append to ``$PATH``, never overwrite it.
* Don't override (i.e. clobber) standard commands with aliases, functions,
  scripts or the like. This can prevent tools from being able to access the
  original command.


Problems
--------


Job Status Isn't Updating
^^^^^^^^^^^^^^^^^^^^^^^^^

Cylc keeps track of a job's progress in one of two ways (according to how
the platform the job was submitted to is configured):

* Jobs send messages to the scheduler (push).
* The scheduler polls jobs (pull).

In either case, the job will also write its updates to the ``job.status`` file.

This is what the ``job.status`` file should look like for a successful job,
note the ``SUCCEEDED`` line:

.. code-block::

   CYLC_JOB_RUNNER_NAME=background
   CYLC_JOB_ID=12345
   CYLC_JOB_RUNNER_SUBMIT_TIME=2000-01-01T00:00:00
   CYLC_JOB_PID=108179
   CYLC_JOB_INIT_TIME=2000-01-01T00:10:00
   CYLC_JOB_EXIT=SUCCEEDED
   CYLC_JOB_EXIT_TIME=2000-01-01T01:30:00

If the ``job.status`` file is showing something different to what the GUI or
Tui is showing, then...

.. rubric:: If your platform uses push communication:

If messages aren't getting back to the scheduler, there should be some
evidence of this in the ``job.err`` file, likely either an error or a
traceback. Likely causes:

* There is a network issue.
* TCP ports are not open (zmq communications).
* Non-interactive SSH has not been correctly configured (ssh communications).

.. rubric:: If your platform uses pull communication:

Firstly, check the polling interval, it's possible that the scheduler has been
configured to poll infrequently and you need to wait for the next poll, or
request a poll manually using the ``cylc poll`` command (also available in the
GUI & Tui).

Use the ``cylc config`` command to inspect the platform's configuration to
determine the configured polling schedule.

Then check the ``job-activity.log`` file, there may have been a problem polling
the remote platform, e.g. a network or configuration error.

Likely causes:

* The platform is down (e.g. all login nodes are offline).
* There is a network issue.
* Non-interactive SSH has not been correctly configured.


My Job Submit-Failed
^^^^^^^^^^^^^^^^^^^^

A submit-failed job means one of three things:

1. There is a Bash syntax error in the task configuration.

   E.G. the following ``script`` has a syntax error, it is missing a
   ``"`` character after ``$WORLD``:

   .. code-block:: cylc

      [runtime]
          [[foo]]
              script = """
                  echo "Hello $WORLD
              """

   This will result in a submission-failure which should appear in the
   ``job-activity.log`` file (and also the scheduler log) something like this:

   .. code-block::

      [jobs-submit cmd] (prepare job file)
      [jobs-submit ret_code] 1
      [jobs-submit err]
      /path/to/job.tmp: line 46: unexpected EOF while looking for matching `"'
      /path/to/job.tmp: line 50: syntax error: unexpected end of file

2. There was an error submitting the job to the specified platform (including
   network issues).

   See the ``job-activity.log`` and the scheduler log. Diagnostic information
   should be in one or both of those files.

3. The platform is not correctly configured.

   See also :ref:`troubleshooting.remote_init_did_not_complete`.


.. _troubleshooting.my_job_failed:

My Job Failed
^^^^^^^^^^^^^

This means something went wrong executing the job.
To find out more, see the ``job.err`` file.

.. note::

   To ensure Cylc jobs fail when they are supposed to, Cylc configures Bash
   to be stricter than it is by default by running ``set -euo pipefail``.

   .. cylc-scope:: flow.cylc[runtime][<namespace>]

   This only applies to scripts you've configured in the Cylc script
   settings (i.e. `script`, `pre-script`, `post-script`, etc), not to any
   Bash scripts to call *from* the job script.

   .. cylc-scope::

.. note::

   One particularly common issue when developing a workflow is failure
   to make a script executable. Use ``ls -l`` to check.

If you're struggling to track down the error, you might want to put the
workflow into debug mode::

   cylc verbosity DEBUG <workflow-id>

When a workflow is running in debug mode, all jobs will create a ``job.xtrace``
file when run in addition to ``job.err``. This can help you to locate the error
within the job script.

You can also start workflows in debug mode::

   cylc play --debug <workflow-id>


My workflow shut down unexpectedly
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

When a Cylc scheduler shuts down, it should leave behind a log message explaining why.

E.G. this message means that a workflow shut down because it was told to:

.. code-block::

   Workflow shutting down - REQUEST(CLEAN)

If a workflow shut down due to a critical problem, you should find some
traceback in this log. If this traceback doesn't look like it comes from your
system, please report it to the Cylc developers for investigation (on
GitHub or Discourse).

In some extreme cases, Cylc might not be able to write a log message e.g:

* There's not enough disk space for Cylc to write a log message.
* If the scheduler was killed in a nasty way e.g. ``kill -9``.
* If the scheduler host goes down (e.g. power off).

If the issue is external to the workflow, once the issue is resolved it should
be possible to restart it as you would normally using ``cylc play``. Cylc
will pick up where it left off.


Why isn't my task running?
^^^^^^^^^^^^^^^^^^^^^^^^^^

To find out why a task is not being run, use the ``cylc show`` command.
This will list the task's prerequisites and xtriggers.

Note, at present ``cylc show`` can only display
:term:`active tasks <active task>`. Waiting tasks beyond the
:term:`n=0 window <n-window>` have no satisfied prerequisites.

Note, tasks which are held |task-held| will not be run, use ``cylc release``
to release a held task.

Note, Cylc will not submit jobs if the scheduler is paused, use ``cylc play``
to resume a paused workflow.


Required files are not being installed on remote platforms
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Cylc installs selected workflow files onto remote platforms when the first task
submits to it.

See :ref:`RemoteInit` for the list of directories installed and how to
configure them.

If something has gone wrong during installation, an error should have been
logged a file in this directory:
``$HOME/cylc-run/<workflow-id>/log/remote-install/``.

If you need to access files from a remote platform (e.g. 2-stage ``fcm_make``),
ensure that a task has submitted to it before you do so. If needed you can use
a blank "dummy" task to ensure that remote installation is completed *before*
you run any tasks which require this e.g:

.. code-block:: cylc-graph

   dummy => fetch_files


Conda / Mamba environment activation fails
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Some Conda packages rely on activation scripts which are run when you call the
activate command.

Unfortunately, some of these scripts don't defend against command failure or
unset environment variables causing them to fail when configured in Cylc
``*script`` (see also :ref:`troubleshooting.my_job_failed` for details).

To avoid this, run ``set +eu`` before activating your environment. This turns
off some Bash safety features, allowing environment activation to complete.
Remember to run ``set -eu`` afterwards to turn these features back on.

.. code-block:: cylc

   [runtime]
       [[my_task]]
            script = """
               set +eu
               conda activate <my_environment>
               set -eu

               do-something
               do-something-else
            """


Error Messages
--------------

Cylc should normally present you with a simple, short error message when things
go wrong.

To see the full traceback, run the command / workflow in debug mode, e.g. using
the ``--debug`` option.

If you are presented with traceback when you are *not* running in debug mode,
then this is not an expected error, please report the traceback to us.


``FileNotFoundError: No such file or directory``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This is the error message Python gives when you try to call an executable which
does not exist in the ``$PATH``. It means there's something wrong with the Cylc
installation, or something missing from the environment or system in which Cylc has been installed.

E.G. the following error:

.. code-block::

   FileNotFoundError: [Errno 2] No such file or directory: 'ssh'

Means that ``ssh`` is not installed or not in your ``$PATH``.

See :ref:`non-python-requirements` for details on system requirements.


.. _troubleshooting.remote_init_did_not_complete:

``platform: <name> - initialisation did not complete``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This means that Cylc was unable to install the required workflow files onto
a remote platform.

This either means that:

1. The platform is down (e.g. all login nodes are offline).
2. Or, there is a network problem (e.g. you cannot connect to the login nodes).
3. Or, the platform is not correctly configured.

Check the scheduler log, you might find some stderr associated with this
message.

If your site has configured this platform for you, it's probably (1) or (2),
check you are able to access the platform and notify the site administrator as
appropriate.

If you are in the progress of setting up a new platform, it's probably (3).
You might want to check that you've configured the
:cylc:conf:`global.cylc[platforms][<platform name>]install target` correctly,
note that this defaults to the platform name if not explicitly set.


``OperationalError: disk I/O error``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This means that Cylc was unable to write to the database.

This error usually occurs if when you have exceeded your filesystem quota.

If a Cylc scheduler cannot write to the filesystem, it will shut down. Once
you've cleared out enough space for the workflow to continue you should be able
to safely restart it as you would normally using ``cylc play``. The workflow
will continue from where it left off.


``socket.gaierror``
^^^^^^^^^^^^^^^^^^^

This usually means that a host could not be found on the network. The likely
cause is DNS configuration.

Cylc is a distributed system so needs to be able to identify the hosts it has
been configured to use (e.g. the servers where you run Cylc workflows or any
login nodes you submit jobs to).
Cylc expects each host to have a unique and stable fully qualified domain name
(FQDN) and to be identifiable from other hosts on the network using this name.

I.e., If a host identifies itself with an FQDN, then we should be able to look it
from another host by this FQDN. If we can't, then Cylc can't tell which host is
which and will not be able to function properly.

If the FQDN of a host is reported differently from different hosts on the
network, then Cylc commands will likely fail. To fix the issue, ensure that the
DNS setup is consistent.

Sometimes we do not have control over the platforms we use and it is not
possible to compel system administrators to address these issues. If this is
the case, you can fall back to IP address based host identification which may
work (i.e. use IP addresses rather than host names, which makes logs less human
readable). As a last resort you can also hard-code the host name for each host.

For more information, see
:cylc:conf:`global.cylc[scheduler][host self-identification]`.


``failed/XCPU``
^^^^^^^^^^^^^^^

``XCPU`` is the signal that most batch systems will use when a job hits its
execution time limit.

Use :cylc:conf:`flow.cylc[runtime][<namespace>]execution time limit` to
increase this limit.


``Cannot determine whether workflow is running on <host>``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

When Cylc runs a workflow, it creates a :term:`contact file` which tells us on
which host and port it can be contacted.

If the scheduler cannot be contacted, Cylc will attempt to check whether the
process is still running to ensure it hasn't crashed.

If you are seeing this error message, it means that Cylc was unable to
determine whether the workflow is running. Likely cause:

* SSH issues.
* Network issues.
* Cylc server is down.

It's possible that this check might not work correctly in some containerised
environments. If you encounter this issue in combination with containers,
please let us know.


Debugging Workflow Configurations
---------------------------------

Cylc Debugging Utilites
^^^^^^^^^^^^^^^^^^^^^^^

.. seealso::

   :ref:`user-guide.cheat_sheet`


Cylc comes with a number of utilies designed to allow inspection of
workflows:

``cylc view``
   Prints workflow configurations before full parsing by Cylc. This
   can include :ref:`Jinja2 <troubleshooting.jinja2>` (use ``-j``)
   or Empy template processing.

   Include files can be inlined (use ``-i``).

``cylc config``
   Prints workflow configuration after Cylc has parsed the runtime
   configuration.

   It is useful because it shows you how inheritance is expanded -
   for example:

   .. code-block:: cylc

      [runtime]
          [[root]]
              execution time limit = PT5S
          [[FAMILY]]
              pre-script = sleep 15
          [[foo, bar]]
              script = echo 'Hello'
          [[bar]]
              inherit = FAMILY
              post-script = echo 'World'

   would be shown as (revealing in this example why task ``bar``
   always fails):

   .. code-block:: cylc

      [runtime]
          [[root]]
              execution time limit = PT5S
          [[FAMILY]]
              execution time limit = PT5S
              pre-script = sleep 15
          [[foo]]
              execution time limit = PT5S
              script = echo 'Hello'
          [[bar]]
              execution time limit = PT5S
              pre-script = sleep 15
              script = echo 'Hello'
              inherit = FAMILY
              post-script = echo 'World'


``cylc lint``
   #. Checks the config against the :ref:`style_guide`.
   #. Looks deprecated Cylc 7 configurations and recommends
      Cylc 8 configurations to replace them.

   .. seealso::

      :ref:`cylc_lint_script`

``cylc validate``

   Validate a workflow configuration.

   .. seealso::

      :ref:`Validation`

.. _troubleshooting.jinja2:

See what the Jinja2 is doing
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Sometimes understanding what Jinja2 templating is doing
to a workflow configuration can be difficult.

``cylc view --process`` (or ``-p``) shows you what the
configuration will look like after Jinja2 processing.

For example:

.. code-block::

   {% for n in my_function(3) %}
       R/1983/P{{n}}Y = cicada_{{n}}[-P{{n}}Y] => cicada_{{n}}
   {% endfor %}

is much easier to understand as:

.. code-block:: cylc-graph

      R/1983/P2Y = cicada_2[-P2Y] => cicada_2
      R/1983/P3Y = cicada_3[-P3Y] => cicada_3
      R/1983/P5Y = cicada_5[-P5Y] => cicada_5

If you have installed and played a workflow
(even using ``play --pause``) this processed content
is shown in ``log/config/flow-processed.cylc``.


Getting Help
------------

If your site has deployed and configured Cylc for you and your issue appears
related to the platforms you are using or the Cylc setup, please contact your
site's administrator.

For general Cylc issues, create a post on the Cylc `Discourse`_ forum.
Please include any relevant error messages, workflow configuration and sections
of logs to help us debug your issue.

For Cylc / plugin development issues, you might prefer to contact us on the
`developer's chat <https://matrix.to/#/#cylc-general:matrix.org>`_.
