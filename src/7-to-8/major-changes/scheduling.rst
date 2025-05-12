.. _728.scheduling_algorithm:

Scheduling Algorithm
====================

.. seealso::

   Migration Guide:

   * :ref:`728.optional_outputs`

   User Guide:

   * :ref:`User Guide Required Outputs`
   * :ref:`User Guide Optional Outputs`
   * :ref:`user-guide-reflow`
   * :ref:`n-window`

Cylc can manage infinite workflows of repeating tasks:

.. image:: ../../img/cycling.png
   :align: center

Cylc 8 has a new scheduling algorithm that:

- Is much more efficient because it only has to manage :term:`active tasks`.

  - Tasks are not loaded into memory before they are needed.
  - Tasks are not retained in memory once they complete.
  - There is no costly indiscriminate dependency matching.
- Distinguishes between :term:`optional <optional output>` and
  :term:`required <required output>` task outputs, to support:

  - :term:`graph branching` without :term:`suicide triggers <suicide trigger>`
  - correct diagnosis of :ref:`workflow completion`
- Causes no implicit dependence on previous-instance job submit

  - instances of same task can run out of cycle point order
  - the workflow will not unnecessarily stall downstream of failed tasks
- Provides a sensible activity-based window on the evolving workflow

  - (to fully understand which tasks appeared in the Cylc 7 GUI you had to
    understand the scheduling algorithm)
- Supports multiple concurrent :term:`flows<flow>` within the same workflow.
- Can start a workflow from any task or tasks in the graph (no need for
  checkpoint restart)
- Can limit activity within as well as across cycles, without risking a stall
