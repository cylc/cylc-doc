.. _SimulationMode:

Simulation Modes
----------------

Cylc can run a workflow without running the real jobs, which may be
long-running and resource-hungry.

**Dummy mode** replaces real jobs with background ``sleep`` jobs on the
scheduler host. This avoids :term:`job runner` directives that request compute
resources for real workflow tasks, and it allows any workflow configuration to
be run locally in dummy mode.

.. code-block:: console

   $ cylc play --mode=dummy <workflow-id>  # real dummy jobs

.. note::

   All configured task ``script`` items including ``init-script`` are ignored
   in dummy mode. If your ``init-script`` is required to run even local dummy
   jobs, the relevant environment setup should be done elsewhere.


**Simulation mode** does not run real jobs at all, and does not generate job
log files.

.. code-block:: console

   $ cylc play --mode=simulation <workflow-id>  # no real jobs


Simulated Run Length
^^^^^^^^^^^^^^^^^^^^

The default dummy or simulated job run length is 10 seconds. It can be
changed with :cylc:conf:`[runtime][<namespace>][simulation]default run length`.

If :cylc:conf:`[runtime][<namespace>]execution time limit` and
:cylc:conf:`[runtime][<namespace>][simulation]speedup factor` are both set,
run length is computed by dividing the time limit by the speedup factor.


Simulated Failure
^^^^^^^^^^^^^^^^^

Tasks always complete custom outputs.

By default they succeed, and return a succeeded output.

.. warning::

   In simulation mode a succeeded output may not imply that
   submitted and/or started outputs are generated - so you will not
   be able to test graph pathways such as ``task:started => do_something``.

You can set some or all instances of a task to fail using
:cylc:conf:`[runtime][<namespace>][simulation]fail cycle points`.
``fail cycle points`` takes either a list of cycle point strings or "all".

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
       [[[outputs]]]
          server_broken = "data server unreachable"
       [[[simulation]]]
          fail try 1 only = false
          fail cycle points = 2022-01-01T03:00Z

Limitations
^^^^^^^^^^^

Dummy tasks run locally, so dummy mode does not test communication with remote
job platforms. However, it is easy to write a live-mode test workflow with
simple ``sleep 10`` tasks that submit to a remote platform.

Alternate path branching is difficult to simulate effectively. You can
configure certain tasks to fail via
:cylc:conf:`[runtime][<namespace>][simulation]`, but all branches based
on mutually exclusive custom outputs will run because all custom outputs get
artificially completed in dummy mode and in simulation mode.

.. note::

   Run mode is recorded in the workflow run database. Cylc will not let you
   *restart* a dummy mode workflow in live mode, or vice versa. Instead,
   install a new instance of the workflow and run it from scratch in the new mode.
