.. _Scheduler Logs:

Scheduler Logs
--------------

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
