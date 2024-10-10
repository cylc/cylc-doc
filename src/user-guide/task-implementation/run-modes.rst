.. _task-run-modes:

Task Run Modes
==============

.. versionadded:: 8.4.0

   Before 8.4.0 run modes could only be set for the workflow, not
   for individual tasks.

   Skip mode is new at 8.4.0.

As well as the default task implementation ("live" mode)
other implementations can be selected:

* By setting the scheduler run mode as an argument to the
  ``cylc play --mode`` command ("simulation" and "dummy" modes).
* By setting :cylc:conf:`[runtime][<namespace>]run mode` for
  "skip" mode.

.. note::

   :cylc:conf:`[runtime][<namespace>]run mode` will override the
   run mode set on the scheduler for any task for which it it set.

#. :ref:`task-run-modes.simulation`: Intended to be used
   when developing a workflow, the scheduler simulates
   running a task without creating a "real" job.
#. :ref:`task-run-modes.dummy`: Intended to be used
   when developing a workflow, the scheduler replaces
   the workflow scripts with dummy scripts and returns
   to the default ("live") submission pathway.
#. :ref:`task-run-modes.skip`: Intended to allow more control of the workflow,
   the scheduler marks task outputs as completed.

.. _task-run-modes.dummy:

Dummy Mode
----------

**Dummy mode** replaces real jobs with background jobs on the
scheduler host which use ``sleep`` to simulate the run length according to
the settings described for simulation mode.
This avoids :term:`job runner` directives that request compute
resources for real workflow tasks, and it allows any workflow configuration to
be run locally in dummy mode.

Limitations
^^^^^^^^^^^

Dummy tasks run locally, so dummy mode does not test communication with remote
job platforms. However, it is easy to write a live-mode test workflow with
simple ``sleep 10`` tasks that submit to a remote platform.


.. _task-run-modes.simulation:

Simulation Mode
---------------

**Simulation mode** does not run real jobs, and does not generate job
log files.


Simulated Run Length
^^^^^^^^^^^^^^^^^^^^

The default dummy or simulated job run length is 10 seconds. It can be
changed with :cylc:conf:`[runtime][<namespace>][simulation]default run length`.

If :cylc:conf:`[runtime][<namespace>]execution time limit` and
:cylc:conf:`[runtime][<namespace>][simulation]speedup factor` are both set,
run length is computed by dividing the
:cylc:conf:`[runtime][<namespace>]execution time limit` by
:cylc:conf:`[runtime][<namespace>][simulation]` speedup factor.

Simulated Failure
^^^^^^^^^^^^^^^^^

Tasks always complete all custom outputs, by default they succeed.

   If you want to test individual pathways, use
   :ref:`skip mode <task-run-modes.skip>`.

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
       [[[simulation]]]
          fail try 1 only = false
          fail cycle points = 2022-01-01T03:00Z

Limitations
^^^^^^^^^^^

Alternate path branching is difficult to simulate effectively. You can
configure certain tasks to fail via
:cylc:conf:`[runtime][<namespace>][simulation]`, but all branches based
on mutually exclusive custom outputs will run because all custom outputs get
artificially completed in dummy mode and in simulation mode.


.. _task-run-modes.skip:

Skip Mode
---------

Skip mode is designed as an aid to workflow control:

* Allows creation of dummy tasks as part of workflow design.
* Allows skipping of tasks in a running workflow.

Skip mode allows the user to specify which task outputs
will be emitted using :cylc:conf:`[runtime][<namespace>][skip]outputs`.

By default task event handlers are disabled by skip mode, but they
can be enabled using
:cylc:conf:`[runtime][<namespace>][skip]disable task event handlers`.

Set task to succeeded
^^^^^^^^^^^^^^^^^^^^^

.. admonition:: Scenario

   We don't need a task to run, but want to set it to succeed.

Broadcast :cylc:conf:`[runtime][<namespace>]run mode` setting the
value to ``skip``.

Create a Dummy Task
^^^^^^^^^^^^^^^^^^^

.. admonition:: Scenario

   We have a large family to large family trigger.

   .. code-block:: cylc

      [task parameters]
          x = 1..N   # Where N is big.
      [scheduling]
          [[graph]]
              R1 = FAMILY:succeed-all => FAMILY2
      [runtime]
         [[FAMILY, FAMILY2]]
         [[task1<x>]]
            inherit = FAMILY
         [[task2<x>]]
            inherit = FAMILY2

   If we increase N, the number of dependencies being tracked
   by the scheduler is N^2.

Adding a skip mode task between the families:

.. code-block:: cylc

   FAMILY:succeed-all => skiptask => FAMILY2

Will reduce the number of dependencies to 2x.

Parameter Exclusion
^^^^^^^^^^^^^^^^^^^

.. admonition:: Scenario

   We want to skip a small number of tasks from a parameterized
   group of tasks:

   .. code-block:: cylc

      [task parameters]
          # House number 13 doesn't actually exist on this street...
          house_number = 1..20

We can use skip mode to make sure that a parameter task always
succeeds without running anything:

.. code-block:: cylc

   [runtime]
       [[post parcel<house_number>]]
           script = send letter
       [[post parcel<house_number=13>]]
           run mode = skip
