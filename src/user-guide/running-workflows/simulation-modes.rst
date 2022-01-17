.. _SimulationMode:

Simulating Workflow Behaviour
-----------------------------

Several workflow run modes allow you to simulate workflow behaviour quickly without
running the workflow's real jobs - which may be long-running and resource-hungry:

dummy mode
   Runs tasks as background jobs on configured job hosts.

   This simulates scheduling, job host connectivity, and generates all job
   files on workflow and job hosts.
dummy-local mode
   Runs real tasks as background jobs on the workflow host, which allows
   dummy-running workflows from other sites.

   This simulates scheduling and generates all job files on the workflow host.
simulation mode
   Does not run any real tasks.

   This simulates scheduling without generating any job files.

Set the run mode (default ``live``) on the command line:

.. code-block:: console

   $ cylc play --mode=dummy <workflow-id>

You can get specified tasks to fail in these modes, for more flexible workflow
testing. See :cylc:conf:`[runtime][<namespace>][simulation]`.


Proportional Simulated Run Length
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

If :cylc:conf:`[runtime][<namespace>]execution time limit` is set, Cylc
divides it by :cylc:conf:`[runtime][<namespace>][simulation]speedup factor` to compute simulated task
run lengths.


Limitations Of Workflow Simulation
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Dummy mode ignores :term:`job runner` settings because Cylc does not know which
job resource directives (requested memory, number of compute nodes, etc.) would
need to be changed for the dummy jobs. If you need to dummy-run jobs on a
job runner, manually comment out ``script`` items and modify
directives in your live workflow, or else use a custom live mode test workflow.

.. note::

   The dummy modes ignore all configured task ``script`` items
   including ``init-script``. If your ``init-script`` is required
   to run even blank/empty tasks on a job host, note that host environment
   setup should be done elsewhere.


Restarting Workflows With A Different Run Mode?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The run mode is recorded in the workflow run database files. Cylc will not let
you *restart* a non-live mode workflow in live mode, or vice versa. To
test a live workflow in simulation mode just take a quick copy of it and run the
the copy in simulation mode.



