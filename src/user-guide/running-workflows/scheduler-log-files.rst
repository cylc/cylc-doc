.. _Scheduler Logs:

Scheduler Logs
--------------

Each workflow maintains its own log of time-stamped events in the
:term:`workflow log directory` (``$HOME/cylc-run/<workflow-id>/log/scheduler/``).

The information logged here includes:

- Event timestamps, at the start of each line
- Workflow server host, port and process ID
- Workflow initial and final cycle points
- Workflow start type (i.e. cold start, warn start, restart)
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
