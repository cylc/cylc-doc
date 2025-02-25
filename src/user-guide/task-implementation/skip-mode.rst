.. _task-run-modes.skip:

.. cylc-scope:: flow.cylc[runtime][<namespace>]

Skip Mode
=========

.. versionadded:: 8.4.0

Skip mode is designed as an aid to workflow control:

* It allows creation of :term:`dummy tasks<dummy task>` as part of workflow
  design.
* It allows skipping of tasks in a running workflow using either:
  * ``cylc broadcast -s 'run mode = skip'`` (for when it is ready to run).
  This will work with any future task or family.
  * ``cylc set --out skip`` (to immediately skip). Note that globs only match
  tasks in the :term:`active window` of the workflow. Otherwise task names must be explicit.

.. note::

   Setting :cylc:conf:`run mode=skip` in your ``flow.cylc``
   will lead to ``cylc validate`` returning a warning::

      WARNING - The following tasks are set to run in skip mode:
        * example_task

   This is designed to prevent users running a task in skip mode by mistake.
   If you are using skip mode deliberately then this can be
   ignored.

.. _skip_mode.task_outputs:

Task Outputs
------------

Skip mode allows the user to specify which task outputs
will be emitted using :cylc:conf:`[skip]outputs`.

By default:

* All required outputs will be generated.
* ``succeeded`` will be generated even if success is :term:`optional <optional output>`.
* If :cylc:conf:`[skip]outputs` is specified and does not include either
  ``succeeded`` or ``failed``, then ``succeeded`` will still be generated.

The outputs submitted and started are always generated and do not
need to be defined in outputs.

Task Event Handlers
-------------------

By default task event handlers are disabled by skip mode, but they
can be enabled using
:cylc:conf:`[skip]disable task event handlers`.

Skip Mode Examples
------------------

Set task to succeeded
^^^^^^^^^^^^^^^^^^^^^

.. admonition:: Scenario

   We want to turn off a future task or cycle of a workflow.
   We don't want to set the outputs right now.
   But when it would have run we want to set it to succeed.

Broadcast :cylc:conf:`run mode` setting the
value to ``skip``.

.. code-block:: console

   # Set a single future task to run in skip mode:
   cylc broadcast myworkflow// -p 4 -n mytask -s 'run mode = skip'

   # Skip Cycle 4:
   cylc broadcast myworkflow// -p 4 -n '*' -s 'run mode = skip'

   # Skip mytask for all cycles:
   cylc broadcast myworkflow// -n mytask -s 'run mode = skip'


Create a Graph Control Task
^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. admonition:: Scenario

   We have a large family to large family trigger.

   If we increase N, the number of dependencies being tracked
   by the scheduler is N^2.

In this scenario the addition of a skip-mode task between two
families improves the efficiency of the Cylc scheduler.

.. seealso::

   This scenario is explained in detail in
   :ref:`EfficientInterFamilyTriggering`

.. _skip_mode.parameter_exclusion:

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

.. cylc-scope::
