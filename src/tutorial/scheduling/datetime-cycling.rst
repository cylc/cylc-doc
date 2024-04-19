.. _nowcasting: https://en.wikipedia.org/wiki/Nowcasting_(meteorology)

.. _tutorial-datetime-cycling:

Datetime Cycling
================

.. admonition:: Aims
   :class: aims

   | You should be able to:
   | ✅ Write workflows  with datetime cycle points.


In the last section we created an :term:`integer cycling` workflow
with numbered :term:`cycle points <cycle point>`.

.. ifnotslides::

   Workflows may need to be repeated at a regular time intervals, say every day
   or every few hours. To support this Cylc can generate datetime sequences
   as :term:`cycle points <cycle point>` instead of integers.

   .. admonition:: Reminder
      :class: tip

      In Cylc, :term:`cycle points <cycle point>` are task labels that anchor the
      dependencies between individual tasks: this task depends on that task in
      that cycle. Tasks can run as soon as their individual dependencies are met,
      so cycles do not necessarily run in order, or at the real world time
      corresponding to the cycle point value (to do that, see
      :ref:`tutorial-clock-triggers`).


.. _tutorial-iso8601:

ISO8601
-------

Cylc uses the :term:`ISO8601` datetime standard to represent datetimes and durations.

.. _tutorial-iso8601-datetimes:

ISO8601 Datetimes
^^^^^^^^^^^^^^^^^

.. ifnotslides::

   ISO8601 datetimes are written from the largest unit to the smallest
   (year, month, day, hour, minute, second) with a ``T`` separating the date
   and time components. For example, midnight on the 1st of January 2000 is
   written ``20000101T000000``.

   For brevity we can omit seconds (or minutes) from the time:
   ``20000101T0000`` (or ``20000101T00``).

   .. note::

      The smallest interval for a datetime cycling sequence in Cylc is 1 minute.

   For readability we can add hyphens (``-``) between the date components
   and colons (``:``) between the time components.
   This is optional, but if you do it you must use both hyphens *and* colons.

   Time-zone information can be added onto the end. UTC is written ``Z``,
   UTC+1 is written ``+01``, etc. E.G: ``2000-01-01T00:00Z``.

.. Diagram of an iso8601 datetime's components.

.. image:: ../img/iso8601-dates.svg
   :width: 75%
   :align: center

.. _tutorial-iso8601-durations:

ISO8601 Durations
^^^^^^^^^^^^^^^^^

.. ifnotslides::

   ISO8601 durations are prefixed with a ``P`` (for "period") and
   special characters following each unit:

* ``Y`` for year.
* ``M`` for month.
* ``D`` for day.
* ``W`` for week.
* ``H`` for hour.
* ``M`` for minute.
* ``S`` for second.

.. nextslide::

.. ifnotslides::

   As for datetimes, duration components are written in order from largest to
   smallest, and the date and time components are separated by a ``T``:

* ``P1D``: one day.
* ``PT1H``: one hour.
* ``P1DT1H``: one day and one hour.
* ``PT1H30M``: one and a half hours.
* ``P1Y1M1DT1H1M1S``: a year and a month and a day and an hour and a
  minute and a second.


Datetime Recurrences
--------------------

In :term:`integer cycling`, workflows, recurrences are written ``P1``, ``P2``,
etc.

In :term:`datetime cycling <datetime cycling>` workflows, there are two ways to
write recurrences:

1. Using ISO8601 durations (e.g. ``P1D``, ``PT1H``).
2. Using ISO8601 datetimes with inferred recurrence.

.. _tutorial-inferred-recurrence:

Inferred Recurrence
^^^^^^^^^^^^^^^^^^^

.. ifnotslides::

   Recurrence can be inferred from a datetime by omitting  components from the
   front. For example, if the year is omitted then the recurrence can be
   inferred to be annual. E.g.:

.. csv-table::
   :header: Recurrence, Description
   :align: left
   :widths: 30, 70

   ``2000-01-01T00``, Midnight on the 1st of January 2000
   ``01-01T00``, Every year on the 1st of January
   ``01T00``, Every month on the first of the month
   ``T00``, Every day at midnight
   ``T-00``, Every hour at zero minutes past (i.e. every hour on the hour)

.. note::

   To omit hours from a date time, place a ``-`` after the ``T`` character.


Recurrence Formats
^^^^^^^^^^^^^^^^^^

.. ifnotslides::

   As with integer cycling, recurrences start at the :term:`initial cycle
   point` by default. We can override this in two ways:

.. rubric::
   By giving an arbitrary start cycle point (``datetime/recurrence``):

``2000/P4Y``
   Every fourth year, starting with the year 2000.
``2000-01-01T00/P1D``
   Every day at midnight, starting on the 1st of January 2000.

.. nextslide::

.. _tutorial-cylc-datetime-offset-icp:

.. rubric::
   By offset, relative to the initial cycle point (``offset/recurrence``).

The offset must be an ISO8601 duration preceded by a plus character:

``+PT1H/PT1H``
   Every hour starting one hour after the initial cycle point.
``+P1Y/P1Y``
   Every year starting one year after the initial cycle point.

Durations and the Initial Cycle Point
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

When using durations, beware that a change in the initial cycle point
might produce different results for the recurrences.

.. nextslide::

.. list-table::
   :class: grid-table
   :width: 50%

   * - .. code-block:: cylc
          :emphasize-lines: 3

          [scheduling]
              initial cycle point = \
                  2000-01-01T00
              [[graph]]
                  P1D = foo[-P1D] => foo

     - .. code-block:: cylc
          :emphasize-lines: 3

          [scheduling]
              initial cycle point = \
                  2000-01-01T12
              [[graph]]
                  P1D = foo[-P1D] => foo

   * - .. digraph:: Example
          :align: center

          size = "3,3"

          "1/foo" [label="foo\n2000-01-01T00"]
          "2/foo" [label="foo\n2000-01-02T00"]
          "3/foo" [label="foo\n2000-01-03T00"]

          "1/foo" -> "2/foo" -> "3/foo"

     - .. digraph:: Example
          :align: center

          size = "3,3"

          "1/foo" [label="foo\n2000-01-01T12"]
          "2/foo" [label="foo\n2000-01-02T12"]
          "3/foo" [label="foo\n2000-01-03T12"]

          "1/foo" -> "2/foo" -> "3/foo"

.. nextslide::

We could write the recurrence "every midnight" independent of the initial
cycle point by:

* Using an `inferred recurrence`_ instead (i.e. ``T00``).
* Overriding the recurrence start point (i.e. ``T00/P1D``)
* Using ``[scheduling]initial cycle point constraints`` to
  constrain the initial cycle point (e.g. to a particular time of day). See
  the `Cylc User Guide`_ for details.

The Initial and Final Cycle Points
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. ifnotslides::

   There are two special recurrences for the initial and final cycle points:

* ``R1``: run once at the initial cycle point.
* ``R1/P0Y``: run once at the final cycle point.

.. TODO - change terminology as done in the cylc user guide, "repeat" can be
   confusing. Use occur?

Intercycle Dependencies
^^^^^^^^^^^^^^^^^^^^^^^

.. ifnotslides::

   Intercycle dependencies are written as ISO8601 durations, e.g:

* ``foo[-P1D]``: the task ``foo`` from the cycle one day before.
* ``bar[-PT1H30M]``: the task ``bar`` from the cycle 1 hour 30 minutes before.

.. ifnotslides::

   The initial cycle point can be referenced using a caret character ``^``, e.g:

* ``baz[^]``: the task ``baz`` from the initial cycle point.


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

   For example in the following workflow the cycle ``2050-01-01T12Z`` will wait
   until 12:00 on the 1st of January 2050 before running:

.. code-block:: cylc

   [scheduling]
       initial cycle point = 2050-01-01T00Z
       [[xtriggers]]
           clock = wall_clock()
       [[graph]]
           T12 = @clock => do_this_on_or_after_noon

.. ifnotslides::

   Clock triggers take an argument - ``offset`` which allows you to specify
   an offset. For example, it might be ok for a task to run up to an hour
   before the specified cycle point:

``wall_clock(-PT1H)``

.. ifnotslides::

   All xtriggers take a ``:recurrance`` indicating how often the scheduler
   will run the check.

   It is good practice not to check more often than necessary:

``wall_clock():PT17M``

.. tip::

   See the :ref:`tutorial-cylc-clock-trigger` tutorial for more information.


.. _tutorial-cylc-datetime-utc:

UTC Mode
--------

.. ifnotslides::

   Cylc can generate datetime cycle points in any time zone, but "daylight saving"
   boundaries can cause problems so we typically use UTC, i.e. the ``+00`` time
   zone:

.. code-block:: cylc

   [scheduler]
       UTC mode = True

.. note::

   UTC is sometimes also labelled ``Z`` ("Zulu" from the NATO phonetic alphabet)
   according to the
   `military time zone convention <https://en.wikipedia.org/wiki/List_of_military_time_zones>`_.

.. _tutorial-datetime-cycling-practical:

Putting It All Together
-----------------------

.. ifslides::

   We will now develop a simple weather forecasting workflow.

.. ifnotslides::

   Cylc was originally developed for running operational weather forecasting. In
   this section we will outline how to implement a basic weather-forecasting workflow.

   .. note::

      Technically this example is a `nowcasting`_ workflow,
      but the distinction doesn't matter here.

   A basic weather forecasting workflow has three main steps:

1. Gathering Observations
^^^^^^^^^^^^^^^^^^^^^^^^^

.. ifnotslides::

   We gather observations from different weather stations to build a picture of
   the current weather. Our dummy weather forecast will get wind observations
   from four weather stations:

   * Aldergrove (Near Belfast in NW of the UK)
   * Camborne (In Cornwall, the far SW of England)
   * Heathrow (Near London in the SE)
   * Shetland (The northernmost part of the UK)

   The tasks that retrieve observation data will be called
   ``get_observations_<site>`` where ``site`` is the name of the weather
   station.

   Next we need to consolidate the observations so that our forecasting
   system can work with them. To do this we have a
   ``consolidate_observations`` task.

   We will fetch wind observations **every three hours, starting from the
   initial cycle point**.

   The ``consolidate_observations`` task must run after the
   ``get_observations<site>`` tasks.

.. digraph:: example
   :align: center

   size = "7,4"

   get_observations_aldergrove -> consolidate_observations
   get_observations_camborne -> consolidate_observations
   get_observations_heathrow -> consolidate_observations
   get_observations_shetland -> consolidate_observations

   hidden [style="invis"]
   get_observations_aldergrove -> hidden [style="invis"]
   get_observations_camborne -> hidden [style="invis"]
   hidden -> consolidate_observations [style="invis"]

.. ifnotslides::

   We will also use the UK radar network to get rainfall data with a task
   called ``get_rainfall``.

   We will fetch rainfall data *every six hours, from six hours after the
   initial cycle point*.

2. Running Computer Models to Generate Forecast Data
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. ifnotslides::

   We will do this with a task called ``forecast`` that runs
   *every six hours, from six hours after the initial cycle point*.
   The ``forecast`` task will depend on:

   * The ``consolidate_observations`` task from the previous two cycles and
     the present cycle.
   * The ``get_rainfall`` task from the present cycle.

.. digraph:: example
   :align: center

   size = "7,4"

   subgraph cluster_T00 {
       label="+PT0H"
       style="dashed"
       "observations.t00" [label="consolidate observations\n+PT0H"]
   }

   subgraph cluster_T03 {
       label="+PT3H"
       style="dashed"
       "observations.t03" [label="consolidate observations\n+PT3H"]
   }

   subgraph cluster_T06 {
       label="+PT6H"
       style="dashed"
       "forecast.t06" [label="forecast\n+PT6H"]
       "get_rainfall.t06" [label="get_rainfall\n+PT6H"]
       "observations.t06" [label="consolidate observations\n+PT6H"]
   }

   "observations.t00" -> "forecast.t06"
   "observations.t03" -> "forecast.t06"
   "observations.t06" -> "forecast.t06"
   "get_rainfall.t06" -> "forecast.t06"

3. Processing the data output to produce user-friendly forecasts
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. ifnotslides::

   This will be done with a task called ``post_process_<location>`` where
   ``location`` is the place we want to generate the forecast for. For
   the moment we will use Exeter.

   The ``post_process_exeter`` task will run *every six hours starting six
   hours after the initial cycle point* and will be dependent on the
   ``forecast`` task.

.. digraph:: example
   :align: center

   size = "2.5,2"

   "forecast" -> "post_process_exeter"

.. nextslide::

.. ifslides::

   .. rubric:: Next Steps

   1. Read through the "Putting It All Together" section.
   2. Complete the practical.

   Next section: :ref:`tutorial-cylc-further-scheduling`


.. _datetime cycling practical:

.. practical::

   .. rubric:: In this practical we will create a dummy forecasting workflow
      using datetime cycling.

   #. **Create A New Workflow.**

      Create a new source directory ``datetime-cycling`` under ``~/cylc-src``,
      and move into it:

      .. code-block:: bash

         mkdir ~/cylc-src/datetime-cycling
         cd ~/cylc-src/datetime-cycling

      Create a :cylc:conf:`flow.cylc` file and paste the following code into it:

      .. code-block:: cylc

         [scheduler]
             UTC mode = True
             allow implicit tasks = True
         [scheduling]
             initial cycle point = 20000101T00Z
             [[graph]]

   #. **Add The Recurrences.**

      The weather-forecasting workflow will require two
      recurrences. Add these under the ``graph`` section
      based on the information given above.

      .. hint::

         See :ref:`Datetime Recurrences<tutorial-cylc-datetime-offset-icp>`.

      .. spoiler:: Solution warning

         The two recurrences you need are

         * ``PT3H``: repeat every three hours starting from the initial cycle
           point.
         * ``+PT6H/PT6H``: repeat every six hours starting six hours after the
           initial cycle point.

         .. code-block:: diff

             [scheduler]
                 UTC mode = True
                 allow implicit tasks = True
             [scheduling]
                 initial cycle point = 20000101T00Z
                 [[graph]]
            +        PT3H =
            +        +PT6H/PT6H =

   #. **Write The Graph.**

      With the help of the the information above add the tasks and dependencies to
      to implement the weather-forecasting workflow.

      You will need to consider the intercycle dependencies between tasks as well.

      Use ``cylc graph`` to inspect your work.

      .. spoiler:: Hint hint

         The dependencies you will need to formulate are as follows:

         * The ``consolidate_observations`` task depends on ``get_observations_<site>``.
         * The ``forecast`` task depends on:

           * the ``get_rainfall`` task;
           * the ``consolidate_observations`` tasks from:

             * the same cycle;
             * the cycle 3 hours before (``-PT3H``);
             * the cycle 6 hours before (``-PT6H``).

         * The ``post_process_exeter`` task depends on the ``forecast``
           task.

         To visualise your workflow run the command:

         .. code-block:: sub

            cylc graph <path/to/flow.cylc>

      .. spoiler:: Solution warning

         .. code-block:: cylc

           [scheduler]
               UTC mode = True
               allow implicit tasks = True
           [scheduling]
               initial cycle point = 20000101T00Z
               [[graph]]
                   PT3H = """
                       get_observations_aldergrove => consolidate_observations
                       get_observations_camborne => consolidate_observations
                       get_observations_heathrow => consolidate_observations
                       get_observations_shetland => consolidate_observations
                   """
                   +PT6H/PT6H = """
                       consolidate_observations => forecast
                       consolidate_observations[-PT3H] => forecast
                       consolidate_observations[-PT6H] => forecast
                       get_rainfall => forecast => post_process_exeter
                   """

   #. **Intercycle Offsets.**

      To ensure the ``forecast`` tasks run in the right order (one cycle
      after another) they each need to depend on their own previous run:

      .. digraph:: example
         :align: center

         size = "4,1.5"
         rankdir=LR

         subgraph cluster_T06 {
             label="T06"
             style="dashed"
             "forecast.t06" [label="forecast\nT06"]
         }

         subgraph cluster_T12 {
             label="T12"
             style="dashed"
             "forecast.t12" [label="forecast\nT12"]
         }

         subgraph cluster_T18 {
             label="T18"
             style="dashed"
             "forecast.t18" [label="forecast\nT18"]
         }

         "forecast.t06" -> "forecast.t12" -> "forecast.t18"

      We can express this dependency as ``forecast[-PT6H] => forecast``.

      .. TODO - re-enable this: https://github.com/cylc/cylc-flow/issues/4638

            Try adding this line to your workflow then visualising it with ``cylc
            graph``.

            .. hint::

               Try adjusting the number of cycles displayed by ``cylc graph``:

               .. code-block:: console

                  $ cylc graph . 2000 20000101T12Z &

            You will notice that there is a dependency which looks like this:


            .. digraph:: example
            :align: center

               size = "4,1"
               rankdir=LR

               "forecast.t00" [label="forecast\n20000101T0000Z"
                              color="#888888"
                              fontcolor="#888888"]
               "forecast.t06" [label="forecast\n20000101T0600Z"]


               "forecast.t00" -> "forecast.t06"

            Note in particular that the ``forecast`` task in the 00:00 cycle is
            grey. The reason for this is that this task does not exist. Remember
            the forecast task runs every six hours
            **starting 6 hours after the initial cycle point**, so the
            dependency is only valid from 12:00 onwards. To fix the problem we
            must add a new dependency section which repeats every six hours
            **starting 12 hours after the initial cycle point**.

            Make the following changes to your workflow and the grey task should
            disappear:

      However, the forecast task runs every six hours
      *starting 6 hours after the initial cycle point*, so the
      dependency is only valid from 12:00 onwards. To fix the problem we
      must add a new dependency section which repeats every six hours
      *starting 12 hours after the initial cycle point*:

      .. code-block:: diff

                    +PT6H/PT6H = """
                        ...
         -              forecast[-PT6H] => forecast
                    """
         +          +PT12H/PT6H = """
         +              forecast[-PT6H] => forecast
         +          """

   #. **Clock Triggers**

      To ensure that the ``get_observations_<location>`` tasks run only
      after the time of the observation, add a clock trigger.
      Observations will be available by 10 minutes past the hour.
      By default, the scheduler will check the clock trigger every 10
      seconds, but there is no point in doing this for any interval
      less than around 5 minutes in this case.

      .. spoiler:: Hint hint

         See :ref:`tutorial-clock-triggers`

      .. spoiler:: Solution warning

         .. note::

            There are a number of ways of writing the dependency: This
            example shows multiple patterns.

         .. code-block:: diff

           [scheduling]
               initial cycle point = 20000101T00Z
           +   [[xtriggers]]
           +       obs_clock_trigger = wall_clock(PT10M):PT5M
               [[graph]]
                   PT3H = """
           +           @obs_clock_trigger => get_observations_aldergrove & get_observations_camborne
           +           @obs_clock_trigger => get_observations_heathrow
                       get_observations_aldergrove => consolidate_observations
                       get_observations_camborne => consolidate_observations
                       get_observations_heathrow => consolidate_observations
           -           get_observations_shetland => consolidate_observations
           +           @obs_clock_trigger => get_observations_shetland => consolidate_observations
                   """
                   +PT6H/PT6H = """
                       consolidate_observations => forecast
                       consolidate_observations[-PT3H] => forecast
                       consolidate_observations[-PT6H] => forecast
                       get_rainfall => forecast => post_process_exeter
                   """
