.. _workflow completion:

Workflow Completion
===================

A workflow can :term:`shut down <shutdown>` once all
:term:`active tasks <active task>` complete without spawning further
downstream activity - i.e., when :term:`n=0 window <n-window>` empties out.

.. _scheduler stall:

Scheduler Stall
===============

A workflow has stalled if:

* No tasks are waiting on unstatisfied external events, like clock triggers and xtriggers.
* AND All activity has ceased.
* AND The workflow has not run to completion.

A workflow which has stalled requires manual intervention to continue.

Stalls are caused by :term:`final status incomplete tasks <output completion>`
and :term:`partially satisfied tasks <prerequisite>`.

These most often result from task failures that the workflow does not
handle automatically by retries or optional branching.

A stalled scheduler stays alive for a configurable timeout period
to allow you to intervene, e.g. by manually triggering an incomplete
task after fixing the bug that caused it to fail.

If a stalled workflow does eventually shut down, on the stall timeout
or by stop command, it will immediately stall again on restart.

.. warning::

   At present you have to look at the :term:`scheduler log` to see
   which tasks caused a stall.

.. seealso::

   * :cylc:conf:`[scheduler][events]stall timeout`  
   * :cylc:conf:`[scheduler][events]abort on stall timeout`  
   * :cylc:conf:`[scheduler][events]stall handlers`  
