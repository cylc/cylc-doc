.. _workflow completion:

Workflow Completion
===================

If there is nothing more to run (according to the graph) and there are no
:term:`incomplete <output completion>` tasks present in :term:`n=0 <n-window>`
the workflow is complete and the scheduler will shut down automatically. 


.. _scheduler stall:

Scheduler Stall
===============

If there is nothing more to run, but there are
:term:`incomplete <output completion>` tasks present in the
:term:`n=0 window <n-window>` the workflow did not run to
completion, so the scheduler will :term:`stall` and stay
alive for 1 hour (by default) awaiting user intervention
to allow the workflow to continue.

A stall can be caused by tasks with partially satisfied
prerequisites or tasks that finished incomplete. However,
partially satisfied prerequisites normally result from
upstream tasks finishing incomplete.

Restarting a stalled workflow resets the stall timer.


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
