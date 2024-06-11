.. _workflow completion:

Workflow Completion
===================

   A workflow is complete, and the scheduler will automatically
   :term:`shut down <shutdown>`, if no tasks remain in the
   :term:`n=0 <n-window>`.

   That is, all active tasks have finished, and no tasks remain waiting on
   :term:`prerequisites <prerequisite>` or "external" constraints (such as
   :term:`xtriggers <xtrigger>` or task :term:`hold`).

   If no active tasks remain and all external constraints are satisfied,
   but the n=0 window contains tasks waiting with partially satisfied
   :term:`prerequisites`, or tasks with :term:`final status` and
     :term:`incomplete outputs <output completion>`, then the workflow is
   not complete and the scheduler will :term:`stall` pending manual intervention.


.. _scheduler stall:

Scheduler Stall
===============

A stalled workflow has not run to :term:`completion <workflow completion>`
but cannot continue without manual intervention. 

A stalled scheduler stays alive for a configurable timeout period
pending manual intervention. If it shuts down (on the stall timeout
or otherwise) it will remain in the stalled state on restart.

Stalls are often caused by unexpected task failures, either directly (tasks
with :term:`final status` and :term:`incomplete outputs <output completion>`)
or indirectly (tasks with partially satisfed prerequisites, downstream of an
unexpected failure).

.. warning::

   At present you have to consult the :term:`scheduler log` to see the reason
   for a stall.


.. seealso::

   * :cylc:conf:`[scheduler][events]stall timeout`  
   * :cylc:conf:`[scheduler][events]abort on stall timeout`  
   * :cylc:conf:`[scheduler][events]stall handlers`  
