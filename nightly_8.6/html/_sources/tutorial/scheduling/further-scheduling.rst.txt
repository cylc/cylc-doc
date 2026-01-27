.. _tutorial-cylc-further-scheduling:

Further Scheduling
==================

.. admonition:: Aims
   :class: aims

   | You should be aware of some more advanced scheduling features:
   | ✅ Task state qualifiers.
   | ✅ Clock triggers.
   | ✅ Alternative calendars.


.. _tutorial-qualifiers:

Qualifiers
----------

.. ifnotslides::

   So far we have written dependencies like ``foo => bar``. This is, in fact,
   shorthand for ``foo:succeed => bar``. It means that the task ``bar`` will run
   once ``foo`` has finished successfully. If ``foo`` were to fail then ``bar``
   would not run. We will talk more about these :term:`task states <task state>`
   in the :ref:`Runtime Section <tutorial-tasks-and-jobs>`.

   We refer to the ``:succeed`` descriptor as a :term:`qualifier`.
   There are qualifiers for different :term:`task states <task state>` e.g:

.. ifslides::

   .. code-block:: cylc-graph

      foo => bar
      foo:succeed => bar
      foo:fail => bar

``:start``
   When the task has started running.
``:fail``
   When the task finishes if it fails (produces non-zero return code).
``:finish``
   When the task has completed (either succeeded or failed).

.. nextslide::

It is also possible to create your own :term:`qualifiers <qualifier>`
to handle events within your code (custom outputs).

.. ifnotslides::

   *For more information see the* `Cylc User Guide`_.


.. _tutorial-clock-triggers:

Clock Triggers
--------------

.. ifnotslides::

   In Cylc, :term:`cycle points <cycle point>` are just task labels. Tasks are
   triggered when their dependencies are met, regardless of cycle point.
   But *clock triggers* can be used to force tasks to wait for a particular
   real time, relative to their cycle point, before running.
   This is necessary for certain operational and monitoring systems, e.g. for
   tasks that process real-time data.

   For example in the following workflow the cycle ``2000-01-01T12Z`` will wait
   until 11:00 on the 1st of January 2000 before running:

.. code-block:: cylc

   [scheduling]
       initial cycle point = 2000-01-01T00Z
       [[xtriggers]]
           PT1H_trigger = wall_clock(offset=-PT1H)
       [[graph]]
           # "daily" will run, at the earliest, one hour before midday.
           T12 = @PT1H_trigger => daily

.. tip::

   See the :ref:`tutorial-cylc-clock-trigger` tutorial for more information.


Alternative Calendars
---------------------

.. ifnotslides::

   By default Cylc uses the Gregorian calendar for :term:`datetime cycling`,
   but it also supports:

   - Integer cycling.
   - 360-day calendar (12 months of 30 days each in a year).
   - 365-day calendar (never a leap year).
   - 366-day calendar (always a leap year).

.. code-block:: cylc

   [scheduling]
       cycling mode = 360day

.. ifnotslides::

   .. seealso:: :cylc:conf:`[scheduling]cycling mode`

.. nextslide::

.. ifslides::

   Next section: :ref:`Runtime Introduction
   <tutorial-cylc-runtime-introduction>`
