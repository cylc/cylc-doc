Troubleshooting
===============

If things have gone wrong and you're not sure why, there are few files which
should contain the required information to work out what's going on.

``log/scheduler/log``
   There's a log file for each workflow in
   ``~/cylc-run/<workflow>/log/scheduler/log``.

   You can view this in the GUI or on the command line using
   ``cylc cat-log <workflow>``.
``job.err``
   This contains the stderr captured when the job ran. It's useful for
   debugging job failures.

   You can view this in the GUI or on the command line using
   ``cylc cat-log <workflow>//<cycle>/<task>/<job> -f e``.
``job-activity.log``
   This file records the interaction Cylc has had with a job, namely submission
   and polling. This can be useful in determining the cause of job submission
   failures.

   You can view this in the GUI or on the command line using
   ``cylc cat-log <workflow>//<cycle>/<task>/<job> -f a``.


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
traceback.

Likely causes:

* There is a network issue.
* TCP ports are not open (zmq communications).
* Non-interactive SSH has not been correctly configured (ssh communications).

.. rubric:: If your platform uses pull communication:

Firstly, check the polling interval, it's possible that the scheduler has been
configured to poll infrequently and you need to wait for the next poll, or use
the ``cylc poll`` command (also available in the GUI).

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
   ``"`` character:
   
   .. code-block:: cylc
   
      [runtime]
          [[foo]]
              script = echo "Hello $WORLD
   
   This will result in a submission-failure which should appear in the
   ``job-activity.log`` file (and also the scheduler log) something like this:
   
   .. code-block::
   
      /path/to/job.tmp: line 46: unexpected EOF while looking for matching `"'
      /path/to/job.tmp: line 50: syntax error: unexpected end of file

2. There was an error submitting the job to the specified platform (including
   network issues).

   See the ``job-activity.log`` and the scheduler log. The error should be in
   one or both of those files.

3. The platform is not correctly configured.


My Job Failed
^^^^^^^^^^^^^

This means something went wrong executing the job.

To find out more, see the ``job.err`` file.

If you're struggling to track down the error, you might want to restart the
workflow in debug mode and run the task again:

.. code-block:: console

   # shut the workflow down (leave any active jobs running)
   $ cylc stop --now --now <workflow>
   # restart the workflow in debug mode
   $ cylc play <workflow> --debug
   # re-run all failed task(s)
   $ cylc trigger '<workflow>//*:failed'

When a workflow is running in debug mode, all jobs will create a ``job.xtrace``
file which can help you to locate the error within the job script.


My workflow shutdown unexpectedly
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

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
* If the scheduler will killed in a nasty way e.g. ``kill -9``.
* If the scheduler host goes down (e.g. power off).


Error Messages
--------------


FileNotFoundError: No such file or directory
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This is the error message Python gives when you try to call an exectuable which
does not exist in the ``$PATH``. It means there's something wrong with the Cylc
installation.

E.G. the following error:

.. code-block::

   FileNotFoundError: [Errno 2] No such file or directory: 'ssh'

Means that ``ssh`` is not installed.

See :ref:`non-python-requirements` for details on system requirements.


platform: <name> - initialisation did not complete
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This means that Cylc was unable to install the required workflow files onto
a remote platform.

This either means that:

1. The platform is down (e.g. all login nodes are offline).
2. There is a network problem (e.g. you cannot connect to the login nodes).
3. The platform is not correctly configured.

Check the scheduler log, you might find some stderr associated with this
message.
