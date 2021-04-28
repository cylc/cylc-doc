Cylc |version| Caveats
======================

This is an early release of Cylc, there are some loose ends and features which
have not yet been (re)implemented.

The documentation has not been fully reviewed and command line information may
be out of date in some cases.


Cylc Flow
---------

Run Numbers
   By default when you install a workflow with ``cylc install`` it is installed
   into a numbered subdirectory e.g. ``run1``. A subsequent installation
   would go into ``run2``, etc.

   At present the full workflow registration *including* this run number must
   be provided to Cylc commands e.g::

      $ cylc play myflow/run1

   We plan to infer the most recent run to make this easier e.g::

      $ cylc play myflow

   * https://github.com/cylc/cylc-flow/issues/3895
CLI Change
   We plan to move to a new way of specifying workflow, cycles, tasks and jobs
   on the command line (with back support for the old format).

   This will open up performing operations on multiple workflows in a single
   command e.g::

      $ cylc stop '*'  # stop everything

   * https://github.com/cylc/cylc-flow/pull/3931   
Platform Selection
   When Cylc needs to perform an action on a platform (e.g. submit a job)
   it picks a random host from the platform. If this host is down the operation
   will fail.

   In a later relase Cylc will pick another host in order to provide resilience
   to system issues.

   * https://github.com/cylc/cylc-flow/issues/3827
Trigger Edit
   Functionality removed pending reimplementation.

   * https://github.com/cylc/cylc-flow/issues/3751
Hold / Release
   The ability to hold tasks is in place, however, doesn't work for most uses.
   This will be fixed in a future beta release.

   * https://github.com/cylc/cylc-flow/issues/3743
Reflow
   The new "reflow" functionality which allows multiple
   (potentially parallel) executions of the same workflow in a single
   :term:`scheduler` is not fully supported by all commands and is
   yet to be documented.


Browser Based UI
----------------

The old "GUI" has been replaced by the new browser-based "UI".

Graph View
   There is no graph view in the Cylc UI as yet. A new graph view will be 
   developed providing both "live" (AKA ``cylc gui``) and "offline"
   (AKA ``cylc graph``) functionalities.

   * https://github.com/cylc/cylc-ui/issues/74
   * https://github.com/cylc/cylc-ui/issues/82
Log Files
   The ability to view job log and other files is yet to be implemented.
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
   At present there is no way to view uninstalled workflows in the UI.
   We will add the ability to view and install workflows from the UI.
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

The ``cylc tui`` command (Tui) replaces the old ``cylc monitor``, it provides a
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
   The old ``cylc gscan`` command has been removed. You can now find the gscan
   display on the left-hand side of the Cylc UI.

   In a future release ``cylc tui`` will be able to list workflows in a similar
   way.

   * https://github.com/cylc/cylc-flow/issues/3464


UI Server
---------

Authorisation
   Only "binary" authorisation (i.e. no access / full control) is currently
   supported.

   * https://github.com/cylc/cylc-uiserver/issues/10
CLI Via UIS
   The ability to route Cylc commands via the UIS is planned for a future relase

   * https://github.com/cylc/cylc-flow/issues/3528
