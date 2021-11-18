.. _Managing External Command Execution:

External Command Execution
--------------------------

Job submission commands, event handlers, and job poll and kill commands, are
executed by the :term:`scheduler` in a "pool" of asynchronous
subprocesses, in order to avoid blocking the workflow process. The process pool
is actively managed to limit it to a configurable size, using
:cylc:conf:`global.cylc[scheduler]process pool size`.
Custom event handlers should be lightweight and quick-running because they
will tie up a process pool member until they complete, and the workflow will
appear to stall if the pool is saturated with long-running processes.
However, to guard against rogue commands that hang indefinitely, processes
are killed after a configurable timeout
(:cylc:conf:`global.cylc[scheduler]process pool timeout`).
All process kills are
logged by the :term:`scheduler`. For killed job submissions the associated
tasks also go to the *submit-failed* state.
