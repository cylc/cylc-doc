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
