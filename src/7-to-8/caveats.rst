Cylc |version| Caveats
======================

This is a beta release of Cylc. There are some loose ends and features which
have not yet been (re)implemented.


Cylc Flow
---------

Trigger Edit
   Functionality removed pending reimplementation.

   * https://github.com/cylc/cylc-flow/issues/3743
Reflow
   The new "reflow" functionality, which allows multiple
   (potentially concurrent) executions of the same workflow in a single
   :term:`scheduler`, is not fully supported by all commands


Browser Based UI
----------------

The old "GUI" has been replaced by the new browser-based "UI".

Graph View
   There is no graph view in the new Cylc UI as yet. A new graph view will be
   developed providing both "live" (AKA ``cylc gui``) and "offline"
   (AKA ``cylc graph``) functionalities.

   * https://github.com/cylc/cylc-ui/issues/74
   * https://github.com/cylc/cylc-ui/issues/82

Static Graph Visualization
   Not yet reimplemented for Cylc 8. As an interim measure the
   ``cylc graph``` command can generate a basic PNG image of a workflow
   graph if Graphviz is installed in the Cylc environment.

Log Files
   The ability to view job logs and other files in the web UI is yet to be
   implemented. For the moment:

   * use ``cylc cat-log``
   * look in your ``cylc-run`` directory
   * use Cylc Review from Cylc 7.9.5/7.8.10 (the latest version is compatible
     with Cylc 8)

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
   At present there is no way to view or install non-installed workflows (a.k.a.
   :term:`source workflows <source directory>`) in the UI.
Rose Edit
   Rose Edit is awaiting reimplementation in the UI.
Trigger Edit
   Functionality removed pending reimplementation.
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

Authorization
   A full-featured authorization system has been implemented for Cylc 8, but
   the UI doesn't yet provide easy access to other users' UI Servers.

CLI Via UIS
   The ability to route Cylc commands via the UIS is planned for a future release

   furbulgulbleguvb

   * https://github.com/cylc/cylc-flow/issues/3528
