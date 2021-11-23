
Start, Restart, and Reload
==========================

.. _WorkflowStartUp:


The ``cylc play`` command starts a new instance of the Cylc scheduler program
to manage the target workflow, for the duration of its run (it also resumes
paused workflows that are already running).

There are several ways to start a scheduler for workflow that is not already
running:


* ``cylc play`` **from the initial cycle point**

  - This is the default for a workflow that has not run yet
  - The ``initial cycle point`` is taken from ``flow.cylc`` or the command line
  - Dependence on earlier tasks is ignored, for convenience
  - (In Cylc 7, this was called a *cold start*)
  

* ``cylc play --start-cycle-point=POINT`` **from a later start cycle point**
 
  - This is an option for a workflow that has not run yet
  - The start point must be given on the command line
  - Dependence on earlier tasks is ignored, for convenience
  - The initial cycle point value defined in :cylc:conf:`flow.cylc` is preserved
  - (In Cylc 7, this was called a *warm start*)


* ``cylc play --start-task=TASK-ID`` **from any task(s) in the graph**

  - This is an option for a workflow that has not run yet
  - The start task(s) must be given on the command line
  - The flow will follow the graph onward from the start task(s)
  - (In Cylc 7, this was not possible)
  - (The makes Cylc 7 restart-from-checkpoint obsolete)


* ``cylc play`` to **restart from previous state**

  - This is automatic for a workflow that previously ran
  - The scheduler will carry on from exactly where it got to before
  - At start-up, it will automatically find out what happened to any active
    tasks that were orphaned during shutdown
  - Failed tasks are not automatically resubmitted at restart, in case the
    underlying problem has not been addressed
  - (In Cylc 7, this used the now-obsolete restart command)


.. note::

   If a workflow gets stopped or killed it can be restarted, but to avoid
   corrupting an existing run directory it cannot be started again from scratch
   (unless you delete certain files from the run directory). To start from
   scratch again, install a new copy of the workflow to a new run directory.

.. seealso::
  * :ref:`Installing-workflows`

.. _start_stop_cycle_point:

Start and Stop vs Initial and Final Cycle Points
------------------------------------------------

All workflows have an :term:`initial cycle point` and some may have a
:term:`final cycle point`. These define extent of the graph of tasks that Cylc
can schedule to run.

Start and stop cycle points, if used, define a sub-section of the graph that
the scheduler actually does run. For example:

.. code-block:: cylc

   [scheduling]
       cycling mode = integer
       initial cycle point = 1
       final cycle point = 5
       [[graph]]
           # every cycle: 1, 2, 3, 4, 5
           P1 = foo
           # every other cycle: 1, 3, 5
           P2 = bar

With a :term:`start cycle point` of ``2`` and a :term:`stop cycle point` of
``4``, the task ``foo`` would run at cycles 2, 3 & 4 and the task ``bar``
would only run at cycle ``3``.

.. image:: ../../img/initial-start-stop-final-cp.svg
   :align: center


.. _Reloading The Workflow Configuration At Runtime:

Reloading the Workflow Configuration at Runtime
-----------------------------------------------

The ``cylc reload`` command tells the target :term:`scheduler` to reload its
workflow configuration at run time. This is an alternative to shutting a
workflow down and restarting it after making changes.

.. note::
   Before reload, be sure to :ref:`reinstall <Reinstalling a workflow>` your
   changes from source to run directory


Restarting or Reloading after Graph Changes
-------------------------------------------

If dependencies have changed, tasks that were already active will spawn
children according to their original outputs. Subsequent instances will have
the new settings.

If tasks were removed from the graph, any active instances will be left to
finish, but they will not spawn children. They can be removed manually if
necessary, with ``cylc remove``.

If new tasks were added to the graph, instances will be spawned automatically
as upstream tasks complete the outputs that they depend on. If they have no
parents to do that, you can trigger the first ones manually with ``cylc trigger``.


.. _The Workflow Contact File:

The Workflow Contact File
-------------------------

At start-up, the :term:`scheduler` writes a :term:`contact file`
``$HOME/cylc-run/WORKFLOW/.service/contact`` that records workflow host,
user, port number, process ID, Cylc version, and other information. Client
commands read this file to find the :term:`scheduler`.

The contact file gets removed automatically at shutdown, if the scheduler shuts
down cleanly.
