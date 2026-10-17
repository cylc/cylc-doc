.. _728.play_pause_stop:

Play Pause Stop
===============

.. admonition:: Does This Change Affect Me?
   :class: tip

   Yes if you run Cylc workflows.


Overview
--------

Cylc 8 uses a simplified model for controlling workflows based on the controls
of a tape player.

There are now three controls, play, pause and stop:

* When a workflow is playing, the :term:`scheduler` is running.
* When a workflow is paused, no new jobs will be submitted.
* When a workflow is stopped the :term:`scheduler` is no longer running.

These controls are available in the web GUI or on the command line with the
commands:

* ``cylc play``
* ``cylc pause``
* ``cylc stop``

A workflow can be safely played, paused and stopped any number of times without
interrupting the workflow.


Re-Running Workflows
--------------------

The ``cylc play`` command will always pick up where it left off (a
:term:`restart`).

If you want to re-run the entire workflow again from the start either:

* :ref:`Install a new run<Using Cylc Install>`.
* Or if you want to keep the data from the old run start a new :term:`flow` at
  the beginning of the graph, and stop the original flow.

It is still possible to re-run workflows in-place in the Cylc 7 manner, however,
this is discouraged.
To do this remove the workflow database as well as any other evidence of the 
previous run that is no longer desired:

.. code-block:: bash

   # remove the workflow database, the work, share and log directories
   cylc clean <id> --rm .service/db:work:share:log

   # only remove the worflow database
   $ cylc clean <id> --rm .service/db

Then restart with ``cylc play``.


Hold & Release
--------------

The ``cylc hold`` and ``cylc release`` commands are still present. These
work on individual tasks rather than the workflow as a whole.


Mapping To Old Commands
-----------------------

.. list-table::
   :class: grid-table

   * -
     - **Cylc 7**
     - **Rose 2019**
     - **Cylc 8** (Rose 2)

   * - Play
     - ::

         cylc run <id>
     - ::

         rose suite-run
     - ::

         cylc play <id>

   * - Pause
     - ::

         cylc hold <id>
     - ::

         cylc hold <id>
     - ::

         cylc pause <id>

   * - Resume
     - ::

         cylc release <id>
     - ::

         cylc release <id>
     - ::

         cylc play <id>

   * - Stop
     - ::

         cylc stop <id>
     - ::

         rose suite-shutdown
     - ::

         cylc stop <id>
