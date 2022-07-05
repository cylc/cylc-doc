.. _MajorChangesCLI:

Command Line Interface
======================

.. admonition:: Does This Change Affect Me?
   :class: tip

   This will affect you if you use the Cylc command line interface.


Overview
--------

* Some commands have been renamed e.g. ``cylc run`` -> ``cylc play``.
* Some tools have been added or removed.
* A new task ID format has been introduced.

For a quick side by side comparison see the :ref:`728.cheat_sheet`.


Full List Of Command Changes
----------------------------

The command line has been simplified from Cylc 7 with some commands being
renamed or removed.

.. _license: https://github.com/cylc/cylc-flow/blob/master/COPYING

.. rubric:: Commands which have been removed or changed:

``cylc checkpoint``
  - Database checkpoints are no longer needed.
  - All task state changes are written to the database when they occur.
  - Remaining use cases can be handled by starting a new :term:`flow`
    which allow a new execution of the graph to be started from an
    arbitrary point in the graph.
``cylc conditions``
  - See the `license`_ file for conditions of usage
  - The Cylc license remains unchanged from Cylc 7.
``cylc documentation``
  - We no longer include a command for locating this documentation.
``cylc edit``
  - Use a text editor to edit the workflow configuration file.
``cylc hold``
  - Now used on tasks only; use ``cylc pause`` to pause an entire workflow
    (i.e. to halt all job submissions).
``cylc insert``
  - Task insertion is now automatic, use ``cylc trigger``.
``cylc jobscript``
  - It is no longer possible generate a jobscript from outside of a workflow.
``cylc monitor``
  - There is now a new more powerful terminal user interface (TUI).
  - Try ``cylc tui``.
``cylc nudge``
  - No longer required.
``cylc print``
  - Equivalent to ``cylc scan --states=all``.
``cylc register``
  - Registration is no longer required, all workflows in the ``~/cylc-run``
    directory are "registered" automatically.
  - To install a workflow from a working copy use ``cylc install``.
``cylc release``
  - Now used on tasks only; use ``cylc play`` to resume a paused workflow.
``cylc reset``
  - It is no longer possible to manually change a task's state.
  - You can, however, override the outputs the task generated which has a
    similar effect with ``cylc set-outputs``.
``cylc restart``
  - Replaced by ``cylc play``.
``cylc review``
  - The read-only ``cylc review`` web GUI has been removed.
  - The latest Cylc 7 version of ``cylc review`` is Cylc 8 compatible
    so can still be used to monitor both Cylc 7 and Cylc 8 workflows
    side by side.
``cylc run``
  - Replaced by ``cylc play``.
``cylc search``
  - Use ``grep`` or a text editor to search the workflow configuration or
    source directory.
``cylc spawn``
  - Spawning is now performed automatically, use ``cylc trigger`` to run a task.
``cylc submit``
  - It is no longer possible to submit a job from outside of a workflow.
``cylc warranty``
  - The Cylc license remains unchanged from Cylc 7.

.. rubric:: Graphical User Interfaces (GUIs):

The GTK based GUI based GUIs have been removed, please use the new web based
GUI. Consequently the following commands have also been removed:

- ``cylc gpanel``
- ``cylc gscan``
- ``cylc gcylc``

The ``cylc gui`` command remains, it launches a standalone version of the
web GUI (providing the `Cylc UI Server`_ is installed).


Cylc 8 Standardised IDs
-----------------------

In Cylc 7 there were two ways to specify a task:

.. code-block:: none

   task.cycle
   cycle/task

In Cylc 8 the former is now deprecated, and the latter has been extended to
provide a unique identifier for all workflows, cycles, tasks and jobs using a
standard format:

.. code-block:: none

   ~user/workflow//cycle/task/job

Consequently task IDs have changed:

.. code-block:: none

   # old
   cycle.task

   # new
   cycle/task

An example using ``cylc trigger``:

.. code-block:: bash

   # old
   cylc trigger workflow task.cycle

   # new
   cylc trigger workflow//cycle/task

Cylc 8 still supports the old format, however, the new format unlocks extra
functionality e.g:

.. code-block:: bash

   # stop all running workflows
   cylc stop '*'

   # pause all running workflows
   cylc pause '*'

   # (re-)trigger all failed tasks in all running workflows
   cylc trigger '*//*:failed'

   # hold all tasks in the cycle "2000" in workflows with IDs
    # beginning with "model"
   cylc hold 'model*//2000'

   # delete the run directories for all workflows with IDs
   # beginning with "model_a/"
   cylc clean 'model_a/*'

For more information run ``cylc help id``.

.. _ID post on Discourse: https://cylc.discourse.group/t/cylc-8-id-changes/425

For a quick overview of the motivation see the `ID post on Discourse`_.
