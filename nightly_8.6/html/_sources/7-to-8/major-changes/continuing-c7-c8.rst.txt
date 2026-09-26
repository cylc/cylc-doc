.. _compat_continuing_c7_with_c8:

Continuing a Cylc 7 Workflow with Cylc 8
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. admonition:: Does This Change Affect Me?
   :class: tip

   Read this if you have a partially complete Cylc 7 workflow that you want to
   continue, rather than start from scratch, with Cylc 8. Some cycling
   workflows, for example, may need to run expensive "cold start" tasks and
   incur a multi-cycle spin-up if started from scratch.

.. warning::

   Cylc 8 cannot restart a Cylc 7 workflow in-place, and continuing in a new
   run directory involves some careful set up (below). So, **if possible you
   should complete the run with Cylc 7**.


To continue a Cylc 7 workflow with Cylc 8:

1. Stop the Cylc 7 workflow at an convenient place

   - Typically the end of a cycle point, to simplify the continuation
2. :ref:`Install <MajorChangesInstall>` a new instance of the workflow from
   source, with Cylc 8

   - Adapt file paths to the new run directory structure, in workflow and task
     configurations
   - Note Cylc 8 does :ref:`remote file installation <728.remote-install>`
     when a job is first submitted to a platform
3. Copy runtime files needed by upcoming tasks from the old to the new run
   directory

   - This could include external files installed by initial tasks at runtime
   - Note different files could be present on different job platforms
4. Start the new Cylc 8 run at the appropriate cycle point or task(s) in the
   graph

   - Don't reset the :term:`initial cycle point` (in the ``flow.cylc`` or on
     the command line) to the :term:`start point <start cycle point>` of the
     Cylc 8 run. That would result in the "cold start" that this continuation
     procedure is designed to avoid. Instead use the ``--start-cycle-point``
     option (or ``--start-task``) with ``cylc play``, to start at the right
     place within the graph.
