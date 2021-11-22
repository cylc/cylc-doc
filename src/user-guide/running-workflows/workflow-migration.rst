.. _auto-stop-restart:

Auto Stop-Restart
-----------------

Cylc has the ability to automatically stop workflows running on a particular host
and optionally, restart them on a different host. This can be useful if a host
needs to be taken off-line, e.g. for scheduled maintenance.

See :py:mod:`cylc.flow.main_loop.auto_restart` for details.
