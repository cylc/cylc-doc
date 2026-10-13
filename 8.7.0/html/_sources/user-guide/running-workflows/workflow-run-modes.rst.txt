.. _workflow-run-modes:

Workflow Run Modes
==================

Cylc can run a workflow without running the real jobs, which may be
useful when developing workflows. Tasks 
in :ref:`workflow-run-modes.dummy` and
:ref:`workflow-run-modes.simulation` can help you to understand how different outcomes
and run lengths will affect the workflow.

To start a workflow in one of these modes:

.. code-block:: console

   $ cylc play --mode=dummy <workflow-id>
   $ cylc play --mode=simulation <workflow-id>

.. admonition:: Limitations

   * A workflow cannot be :term:`restarted <restart>` in a different run mode. Instead,
     install a new instance of the workflow and run it from scratch in the new mode.
   * Workflows run in Dummy and Simulation mode do not allow the run mode of
     individual tasks to be overridden by :ref:`task-run-modes.skip`


.. _workflow-run-modes.dummy:

Dummy Mode
----------

**Dummy mode** replaces real jobs with background jobs on the
scheduler host which use ``sleep`` to simulate the run length according to
the settings described for simulation mode.
This avoids :term:`job runner` directives that request compute
resources for real workflow tasks, and it allows any workflow configuration to
be run locally in dummy mode.

.. admonition:: Limitations

   * Dummy mode can only be applied to a whole workflow.
   * Dummy tasks run locally, so dummy mode does not test communication with remote
     job platforms. However, it is easy to write a live-mode test workflow with
     simple ``sleep 10`` tasks that submit to a remote platform.


.. _workflow-run-modes.simulation:

Simulation Mode
---------------

**Simulation mode** does not run real jobs, and does not generate job
log files.  Instead, the scheduler internally simulates task completion to evolve
the workflow.


Simulated Run Length
^^^^^^^^^^^^^^^^^^^^

The default dummy or simulated job run length is 10 seconds. It can be
changed with :cylc:conf:`[runtime][<namespace>][simulation]default run length`.

If :cylc:conf:`[runtime][<namespace>]execution time limit` and
:cylc:conf:`[runtime][<namespace>][simulation]speedup factor` are both set,
run length is computed by dividing the
execution time limit by the speedup factor.

Simulated Failure
^^^^^^^^^^^^^^^^^

Tasks always complete all custom outputs, and by default they will succeed.

If you want to test emitting only some custom outputs
you can run the workflow in live mode with task run modes
set to :ref:`skip mode <task-run-modes.skip>`.

You can set some or all instances of a task to fail using
:cylc:conf:`[runtime][<namespace>][simulation]fail cycle points`,
which takes either a list of cycle point strings or "all".

Tasks set to fail will succeed on their second or following simulated
submission. If you want all submissions to fail, set
:cylc:conf:`[runtime][<namespace>][simulation]fail try 1 only = False`.

For example, to simulate a task you know to be flaky on the half
hour but not on the hour:

.. code-block:: cylc

   [[get_observations]]
      execution retry delays = PT30S
      [[[simulation]]]
         fail cycle points = 2022-01-01T00:30Z,  2022-01-01T01:30Z

In another case you might not expect the retry to work, and want to test
whether your failure handling works correctly:

.. code-block:: cylc

   [[get_data]]
       execution retry delays = PT30S
       [[[simulation]]]
          fail try 1 only = false
          fail cycle points = 2022-01-01T03:00Z

.. admonition:: Limitations

   * Simulation mode can only be applied to a whole workflow.
   * Alternate path branching is difficult to simulate effectively. You can
     configure certain tasks to fail via
     :cylc:conf:`[runtime][<namespace>][simulation]`, but all branches based
     on mutually exclusive custom outputs will run because all custom outputs get
     artificially completed in dummy mode and in simulation mode.
