.. _MajorChangesExcludingTasksAtStartup:

Excluding Tasks at Start-up is Not Supported
============================================

.. admonition:: Does This Change Affect Me?
   :class: tip

   This will affect you if your workflows use the following configurations:

   * ``[scheduling][special tasks]include at start-up``
   * ``[scheduling][special tasks]exclude at start-up``


Overview
--------

The Cylc 7 sheduler allowed you to exclude tasks from the scheduler at start-up: 

.. code-block:: cylc

   # Cylc 7 only 
   [scheduling]
      [[special tasks]]
           include at start-up = foo, bar, baz  # Cylc 8 ERROR!
           exclude at start-up = bar  # Cylc 8 ERROR!

The first config item above excludes all task names not in the include-list;
the second excludes specific tasks that would otherwise be included.

The Cylc 7 scheduler started up with an instance of every task in its "task
pool", and the workflow evolved by each task spawning its own next-cycle
instance at the right time. So, if you excluded a task a start-up it would not
run in the workflow at all unless manually inserted later at runtime.

The Cylc 8 scheduler starts up with only the initial tasks in the graph and the 
workflow evolves by spawning new tasks on demand as dictated by the graph.
Consequently excluding a task at start up as described above would have no
effect at all on most tasks.

This feature also predated the current Cylc dependency graph configuration. To
exclude tasks now without entirely removing them from the workflow definition,
just comment them out of the graph.
