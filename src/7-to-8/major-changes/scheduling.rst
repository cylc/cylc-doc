.. _728.scheduling_algorithm:

Scheduling Algorithm
====================

.. seealso::

   User Guide:

   * :ref:`User Guide Expected Outputs`
   * :ref:`User Guide Optional Outputs`
   * :ref:`user-guide-reflow`
   * :ref:`n-window`

Cylc can manage infinite workflows of repeating tasks:

.. image:: ../../img/cycling.png
   :align: center

Cylc 8 has a new scheduling algorithm that:
   - Is much more efficient because it only has to manage active tasks

     - waiting tasks are not pre-spawned before they are needed
     - succeeded tasks are not kept across the active task window
     - no costly indiscriminate dependency matching is done
   - Distinguishes between :term:`optional <optional output>` and
     :term:`expected <expected output>` task outputs, to support:

     - :term:`graph branching` without :term:`suicide triggers <suicide trigger>`
     - correct diagnosis of :term:`workflow completion`
   - Causes no implicit dependence on previous-instance job submit

     - instances of same task can run out of cycle point order
     - the workflow will not unnecessarily stall downstream of failed tasks
   - Provides a sensible active-task based window on the evolving workflow

     - (to fully understand which tasks appeared in the Cylc 7 GUI you had to
       understand the scheduling algorithm)
   - Supports a powerful new capability called :term:`reflow`: you can trigger
     multiple concurrent flows in the same graph at once, managed by the same
     scheduler
   - Can start a workflow from any task or tasks in the graph (no need for
     checkpoint restart)
   - Can limit activity within as well as across cycles, without risking a stall
