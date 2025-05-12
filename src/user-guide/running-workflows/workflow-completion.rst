.. _workflow completion:

Workflow Completion
===================

A workflow can :term:`shut down <shutdown>` once all
:term:`active tasks <active task>` complete without spawning further
downstream activity - i.e., when :term:`n=0 window <n-window>` empties out.

.. _scheduler stall:

Scheduler Stall
===============

If there are no tasks waiting on as yet unsatisfied external constraints
such clock and xtriggers, and all activity has ceased but workflow has
not :ref:`run to completion <workflow completion>`, then it
has stalled and requires manual intervention to continue.

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
