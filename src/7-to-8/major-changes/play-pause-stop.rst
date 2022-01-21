.. _728.play_pause_stop:

Play Pause Stop
===============

.. admonition:: Does This Change Affect Me?
   :class: tip

   Yes if you run Cylc workflows.


Overview
--------

Cylc 8 uses a simplfied model for controlling workflows based on the controls
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
interrupting the workflow. The play command will always pick up where it left
off. If you want to run again from the start, install a new run or start a
:term:`reflow`.


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
