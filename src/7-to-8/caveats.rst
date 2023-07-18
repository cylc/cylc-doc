Cylc |version| Caveats
======================

There are a few Cylc 7 features which do not yet have direct replacements in
Cylc 8. These features will be re-implemented in future releases.


Cylc Flow
---------

Multiple Flows
   The new :term:`scheduler` can manage multiple flows in the workflow graph.
   Commands and options for interacting with flows are still being refined.


Browser Based UI
----------------

The old "GUI" has been replaced by the new browser-based "UI".

Static Graph Visualization
   Not yet reimplemented for Cylc 8. As an interim measure the
   ``cylc graph`` command can generate a basic PNG image of a workflow
   graph if Graphviz is installed in the Cylc environment.

Multiple Selection
   Multiple selection is yet to be implemented, however, it is possible
   to issue action for multiple tasks (e.g. ``kill``) without using
   multiple selection:

   * From the UI click on a workflow/cycle/task/job.
   * Find the action you want to call (e.g. kill).
   * Click the pencil symbol next to this action.
   * Edit the workflows/cycles/tasks/jobs in the form and press submit.

   * https://github.com/cylc/cylc-ui/issues/434
Installing Workflows
   At present there is no way to view or install
   :term:`source workflows <source directory>` in the UI.
Rose Edit
   Rose Edit is awaiting reimplementation in the UI.
Xtrigger Visibility
   Xtriggers are not yet visible in the UI.

   * https://github.com/cylc/cylc-ui/issues/331
Documentation / Orientation Guide
   Some form of documentation will be provided within the UI itself.

   * https://github.com/cylc/cylc-ui/issues/155


Terminal User Interface
-----------------------

The ``cylc tui`` command (Tui) replaces the old ``cylc monitor``. It provides a
tree view that is very similar to the Cylc UI and supports some control
functionality.

Performance
   TUI currently refreshes its display every second. Large workflows which
   change rapidly may evolve faster than TUI is able to keep pace with which
   will cause TUI to freeze.

   A more performant implementation which does not rely on a scheduled global
   update will follow in due course.

   * https://github.com/cylc/cylc-flow/issues/3527
GScan
   The old ``cylc gscan`` GUI has been removed. You can now find the gscan
   display on the left-hand side of the Cylc UI.

   In a future release ``cylc tui`` will be able to list workflows in a similar
   way.

   * https://github.com/cylc/cylc-flow/issues/3464


UI Server
---------

CLI via UIS
   The ability to route Cylc commands via the UIS is planned for a future release

   * https://github.com/cylc/cylc-flow/issues/3528
