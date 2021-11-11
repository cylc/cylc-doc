.. _tutorial-cylc-clock-trigger:

Clock Triggered Tasks
=====================

In a :term:`datetime cycling` workflow the time represented by the
:term:`cycle points <cycle point>` bear no relation to the real-world time.
Using clock-triggers we can make tasks wait until their cycle point time before
running.

Clock-triggering effectively enables us to tether the "cycle time" to the
"real world time" which we refer to as the :term:`wallclock time`.

.. note::

   Clock triggers are :ref:`Section External Triggers`. They differ from
   custom external triggers only in that they are provided with Cylc.


Clock Triggering
----------------

When clock-triggering tasks we can use different
:ref:`offsets <tutorial-iso8601-durations>` to the cycle time as follows:

.. code-block:: cylc

   my_clock_trigger = wall_clock(offset=<iso8601 duration>)

.. note::

   Regardless of the offset used, the task still belongs to the cycle from
   which the offset has been applied.


Example
-------

Our example workflow will simulate a clock chiming on the hour.

Within your ``~/cylc-run`` directory create a new directory called
``clock-trigger``::

   mkdir ~/cylc-run/clock-trigger
   cd ~/cylc-run/clock-trigger

Paste the following code into a ``flow.cylc`` file:

.. code-block:: cylc

   [scheduler]
       UTC mode = True # Ignore DST

   [scheduling]
       initial cycle point = TODO
       final cycle point = +P1D # Run for one day
       [[graph]]
           PT1H = bell

   [runtime]
       [[root]]
           [[[events]]]
               mail events = failed
       [[bell]]
           script = printf 'bong%.0s\n' $(seq 1 $(cylc cyclepoint --print-hour))

Change the initial cycle point to 00:00 this morning (e.g. if it was
the first of January 2000 we would write ``2000-01-01T00Z``).

We now have a simple workflow with a single task that prints "bong" a number
of times equal to the (cycle point) hour.

Run your workflow using::

   cylc play clock-trigger

Stop the workflow after a few cycles using ``cylc stop --now --now clock-trigger``.
Notice how the tasks run as soon as possible rather than
waiting for the actual time to be equal to the cycle point.

.. TODO - check this tutorial still works now that cylc run/restart has been
   replaced by cylc play


Clock-Triggering Tasks
----------------------

We want our clock to only ring in real-time rather than the simulated
cycle time.

To do this, modify the ``[scheduling][graph]`` section of
your ``flow.cylc``:

.. code-block:: cylc

   PT1H = @wall_clock  => bell

This tells the workflow to clock trigger the ``bell`` task with a cycle
offset of ``0`` hours.

Save your changes and run your workflow.

Your workflow should now be running the ``bell`` task in real-time. Any cycle times
that have already passed (such as the one defined by ``initial cycle time``)
will be run as soon as possible, while those in the future will wait for that
time to pass.

At this point you may want to leave your workflow running until the next hour
has passed in order to confirm the clock triggering is working correctly.
Once you are satisfied, stop your workflow.

By making the ``bell`` task a clock triggered task we have made it run in
real-time. Thus, when the wallclock time caught up with the cycle time, the
``bell`` task triggered.


Adding More Clock-Triggered Tasks
---------------------------------

Running clock triggered tests at the cycle time is a special case:
We will now modify our workflow to run tasks at quarter-past, half-past and
quarter-to the hour.

Open your ``flow.cylc`` and modify the ``[runtime]`` section by adding the
following:

.. code-block:: cylc

   [[quarter_past, half_past, quarter_to]]
       script = echo 'chimes'

Edit the ``[[scheduling]]`` section to read:

.. code-block:: cylc

   [[xtriggers]]
       quarter_past_trigger = wall_clock(offset=PT15M):PT30S
       half_past_trigger = wall_clock(offset=PT30M):PT30S
       quarter_to_trigger = wall_clock(offset=PT45M):PT30S
   [[graph]]
       PT1H = """
           @wall_clock => bell
           @quarter_past_trigger => quarter_past
           @half_past_trigger => half_past
           @quarter_to_trigger => quarter_to
       """

Note the different values used for the cycle offsets of the clock-trigger tasks.

Save your changes and run your workflow using::

   cylc play clock-trigger now

.. note::

   The ``now`` argument will run your workflow using the current time for the
   initial cycle point.

Again, notice how the tasks trigger until the current time is reached.

Leave your workflow running for a while to confirm it is working as expected
and then shut it down using the :guilabel:`stop` button in the ``cylc gui``.


.. note::

   You may have noticed the ``:PT30S`` at the end of each clock trigger
   definition. This how often the :ref:`Section External Triggers` is checked.
   By default external triggers are checked every 10 seconds, but if there
   are a lot of external triggers this can be hard work for the computer
   running the workflow and it may not be necessary to check this often.


Summary
-------

* Clock triggers are a type of :term:`dependency` which cause
  :term:`tasks <task>` to wait for the :term:`wallclock time` to reach the
  :term:`cycle point` time.
* Clock triggers are a built in example of :ref:`Section External Triggers`.
* Clock triggers can only be used in datetime cycling workflows.

For more information see the `Cylc User Guide`_.
