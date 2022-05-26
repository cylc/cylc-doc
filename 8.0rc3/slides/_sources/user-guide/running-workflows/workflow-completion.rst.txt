.. _workflow completion:

Workflow Completion
===================

If there is nothing more to run (according to the graph) and there are no
:term:`incomplete tasks <incomplete task>` present, the scheduler will report
workflow completion and shut down when current active tasks finish. 


.. _scheduler stall:

Scheduler Stall
===============

If there is nothing more to run (according to the graph) but there are
:term:`incomplete tasks <incomplete task>` present, the scheduler will
:term:`stall` and stay alive for 1 hour (by default) awaiting user intervention
to allow the workflow to continue.

The presence of incomplete tasks means that the workflow did not run to
completion as expected, because some :term:`expected task outputs
<expected output>` were not completed at runtime.

Restarting a stalled workflow triggers a new stall timer.


.. note::

   Partially satisfied prerequisites can also cause a stall. If ``a & b => c``,
   and ``a`` succeeds but ``b`` never even runs, the scheduler will take
   partial completion of ``c``'s prerequisites as a sign that the workflow did
   not run to completion as expected.


.. warning::

   At present you have to consult the :term:`scheduler log` to see the reason
   for a stall.


.. seealso::

   * :cylc:conf:`[scheduler][events]stall timeout`  
   * :cylc:conf:`[scheduler][events]abort on stall timeout`  
   * :cylc:conf:`[scheduler][events]stall handlers`  
