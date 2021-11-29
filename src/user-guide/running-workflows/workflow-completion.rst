.. _workflow completion:

Workflow Completion
===================

If there is nothing more to do, according to the graph, when current active
tasks finish, the scheduler will report workflow completion and shut down so
long as there are no incomplete tasks present. 

If there are incomplete tasks present, the scheduler will :term:`stall` and
stay alive for 1 hour (by default) awaiting user intervention to allow the
workflow to continue.

Restarting a stalled workflow will trigger a new stall timer.

.. note::

   Partially satisfied prerequisites can also cause a stall. If ``a & b => c``,
   and ``a`` succeeds but ``b`` never even runs, the scheduler will take
   partial completion of ``c``'s prerequisites as a sign that the workflow did
   not run to completion as expected.
