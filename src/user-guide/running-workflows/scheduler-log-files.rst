.. _Scheduler Logs:
.. _user-guide.log_files:

Workflow Logs
=============

Cylc produces a number of log files which record information about the
wortkflow, how it was installed, what tasks have run, their outcomes and more.


Log Files
---------

Cylc log files are located in the workflow :term:`run directory`.

.. describe:: log/scheduler/

   Contains the scheduler log files, these detail everything that a workflow
   did whilst it ran and are key to debugging issues.

   Every time you start or restart a workflow a new log file is created in this
   location:

   .. describe:: log/scheduler/<start_number>-<type>-<file_number>.log

      For more information on this file, see :ref:`log_files.scheduler_log`.

.. describe:: log/config/

   Contains a record of the workflow configuration files:

   .. describe:: log/config/<start_number>-<type>-<file_number>.cylc

      The parsed contents of the ``flow.cylc`` (or ``suite.rc``) file from
      each start, restart or reload of the workflow.

   .. describe:: log/config/flow-processed.cylc

      The un-parsed contents of the ``flow.cylc`` (or ``suite.rc``) file that
      the workflow was most recently started or restarted from. This file has
      not been parsed by Cylc so is still in the definition order, however,
      Jinja2 process has been performed making it useful for debugging Jinja2
      issues.

   .. describe:: log/config/<time>-rose-suite.conf

      The parsed contents of the ``rose-suite.conf`` file if present in the workflow.

.. describe:: log/install/

   Contains the workflow installation log (i.e. the output of the
   ``cylc install`` command.

   .. describe:: log/install/<start_number>-install.log

.. describe:: log/remote-install/

   Contains a record of any remote platforms that the workflow has been
   installed onto.

   .. describe:: log/remote-install/<start_number>-<type>-<platform>.log

.. describe:: log/version/

   If the workflow :term:`source directory` is version controlled with Git or
   SVN, this directory will contain information extracted from the version
   control system at the time the workflow was installed:P

   .. describe:: log/version/uncommitted.diff

      Any uncommitted diff in unified diff format.

   .. describe:: log/version/vcs.json

      Information including the commit hash / revision number.

.. describe:: opt/rose-suite-cylc-install.conf

   If Rose is used, this file will contain any Rose options that were used
   with the ``cylc install`` command (i.e. any overrides which were applied
   when the workflow was installed).

.. note::

   Where the ``<variables>`` in the above paths are:

   .. cylc-scope:: global.cylc[scheduler][logging]

   ``start_number``
      Is ``1`` when you first start the workflow. This number increments with
      each restart.
   ``type``
      Is either ``start``, ``restart`` or ``reload``.
   ``file_number``
      Is initally ``1``, if the log file exceeds the `maximum size in bytes`,
      it will "roll over" into a new log file and this number will increment.
      If the number of "roll over" log files exceeds the
      `rolling archive length`, then Cylc will remove an old log file before
      creating a new one.
   ``time``
      Is a timestamp in ISO8601 format.

.. cylc-scope::


.. _log_files.scheduler_log:

The Scheduler Log File
----------------------

Each workflow maintains its own log of time-stamped events in the
:term:`workflow log directory` (``$HOME/cylc-run/<workflow-id>/log/scheduler/``).

The information logged here includes:

- Event timestamps, at the start of each line
- Workflow server host, port and process ID
- Workflow initial and final cycle points
- Workflow (re)start number (1 for the first play, 2 or more for restarts)
- Task events (task started, succeeded, failed, etc.)
- Workflow stalled warnings.
- Client commands (e.g. ``cylc hold``)
- Job IDs.
- Information relating to the remote file installation is contained in a
  separate log file, which can be found in
  ``$HOME/cylc-run/<workflow-id>/log/remote-install/``.

.. note::

   Workflow log files are primarily intended for human eyes. If you need
   to have an external system to monitor workflow events automatically, use:

   * Event hooks (see :cylc:conf:`flow.cylc[scheduler][events]` and
     :cylc:conf:`flow.cylc[runtime][<namespace>][events]`).
   * The GraphQL interface (can be accessed via GraphiQL in the Cylc GUI).
   * The sqlite *workflow run database*
     (see :ref:`Workflow Run Databases`)

   Rather than parse the log files.


.. _scheduler Logs.Cylc message:

Cylc Message
^^^^^^^^^^^^

The Scheduler Log also records messages sent by ``cylc message`` allowing you
to add custom messages to this log.

For example, if your task contained the following code:

.. code-block:: shell

   cylc message -- "ERROR:some_function failed."

Your log should produce output similar to:

.. code-block:: none

   ERROR - [21491012T0410Z/mytask running job:01 flows:1] (received)some_function failed ERROR at 2023-04-14T11:36:35+01:00

Severity levels are the same as those used by
`Python's logger <https://docs.python.org/3/library/logging.html#logging-levels>`_:

- CRITICAL
- ERROR
- WARNING
- INFO
- DEBUG

Messages logged at "DEBUG" will only appear in the scheduler log if the
workflow is played with ``cylc play --debug``.
