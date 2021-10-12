.. _User Guide Scheduling:

Scheduling - Dependency Graphs
==============================

.. tutorial:: Scheduling Tutorial <tutorial-scheduling>

The :term:`graph` defines the workflow in terms of
:term:`tasks <task>` and the :term:`dependencies <dependency>`
between them.

Graph Syntax
------------

.. tutorial:: Graph Tutorial <tutorial-cylc-graphing>

A Cylc :term:`graph` is composed of one or more
:term:`graph strings <graph string>` which use a special syntax.

* ``=>`` defines a dependency.
* ``&`` and ``|`` meaning *and* & *or* can be used to write
  :term:`conditional dependencies <conditional dependency>`.

For example:

.. code-block:: cylc-graph

   # baz will not be run until both foo and bar have succeeded
   foo & bar => baz

These :term:`graph strings <graph string>` are configured in the
:cylc:conf:`[scheduling][graph]` section e.g:

.. code-block:: cylc

   [scheduling]
       [[graph]]
           R1 = """
               foo & bar => baz
           """

In this example ``R1`` is the :term:`recurrence` which defines the interval
at which this graph string is to be run. ``R1`` means "run once", ``P1D`` means every day.

Graph strings may contain blank lines, arbitrary white space and comments e.g:

.. code-block:: cylc

   [scheduling]
       [[graph]]
           R1 = """

               foo & bar => baz  # baz is dependent on foo and bar

           """


Interpreting Graph Strings
--------------------------

Workflow dependency graphs can be broken down into pairs in which the left
side (which may be a single task or family, or several that are
conditionally related) defines a :term:`trigger` for the task or family on the
right. For instance the "word graph" *C triggers off B which
triggers off A* can be deconstructed into pairs *C triggers off B*
and *B triggers off A*. In this section we use only the default
trigger type, which is to trigger off the upstream task succeeding;
see :ref:`TriggerTypes` for other available triggers.

In the case of cycling tasks, the triggers defined by a graph string are
valid for cycle points matching the list of hours specified for the
graph section. For example this graph:

.. code-block:: cylc

   [scheduling]
       [[graph]]
           T00,T12 = "A => B"

implies that ``B`` triggers off ``A`` for cycle points in which the hour
matches ``00`` or ``12``.

To define inter-cycle dependencies, attach an offset indicator to the
left side of a pair:

.. code-block:: cylc

   [scheduling]
       [[graph]]
           T00,T12 = "A[-PT12H] => B"

This means ``B[time]`` triggers off ``A[time-PT12H]`` (12 hours before) for cycle
points with hours matching ``00`` or ``12``. ``time`` is implicit because
this keeps graphs clean and concise, given that the
majority of tasks will typically
depend only on others with the same cycle point. Cycle point offsets can only
appear on the left of a pair, because a pairs define triggers for the right
task at cycle point ``time``. However, ``A => B[-PT6H]``, which is
illegal, can be reformulated as a *future trigger*
``A[+PT6H] => B`` (see :ref:`InterCyclePointTriggers`). It is also
possible to combine multiple offsets within a cycle point offset e.g.

.. code-block:: cylc

   [scheduling]
       [[graph]]
           T00,T12 = "A[-P1D-PT12H] => B"

This means that ``B[Time]`` triggers off ``A[time-P1D-PT12H]`` (1 day and 12 hours
before).

Triggers can be chained together. This graph:

.. code-block:: cylc

   T00, T12 = """
       A => B  # B triggers off A
       B => C  # C triggers off B
   """

is equivalent to this:

.. code-block:: cylc

   T00, T12 = "A => B => C"

*Each trigger in the graph must be unique* but *the same task
can appear in multiple pairs or chains*. Separately defined triggers
for the same task have an AND relationship. So this:

.. code-block:: cylc

   T00, T12 = """
       A => X  # X triggers off A
       B => X  # X also triggers off B
   """

is equivalent to this:

.. code-block:: cylc

   T00, T12 = "A & B => X"  # X triggers off A AND B

In summary, the branching tree structure of a dependency graph can
be partitioned into lines (in the :cylc:conf:`flow.cylc` graph string) of pairs
or chains, in any way you like, with liberal use of internal white space
and comments to make the graph structure as clear as possible.

.. code-block:: cylc

   # B triggers if A succeeds, then C and D trigger if B succeeds:
       R1 = "A => B => C & D"
   # which is equivalent to this:
       R1 = """
           A => B => C
           B => D
       """
   # and to this:
       R1 = """
           A => B => D
           B => C
       """
   # and to this:
       R1 = """
           A => B
           B => C
           B => D
       """
   # and it can even be written like this:
       R1 = """
           A => B # blank line follows:

           B => C # comment ...
           B => D
       """

Splitting Up Long Graph Lines
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

It is not necessary to use the general line continuation marker
``\`` to split long graph lines. Just break at
dependency arrows (``=>``), boolean operators (``&``, ``|``),
or split long chains into smaller ones. This graph:

.. versionadded:: 8.0.0

   Breaking graph strings on ``&`` and ``|`` is new at Cylc 8

.. code-block:: cylc

   R1 = "A => B => C"

is equivalent to this:

.. code-block:: cylc

   R1 = """
       A => B =>
       C
   """

and also to this:

.. code-block:: cylc

   R1 = """
       A => B
       B => C
   """


.. _GraphTypes:

Graph Types
-----------

A workflow configuration can contain multiple graph strings that are combined
to generate the final graph.

One-off (Non-Cycling)
^^^^^^^^^^^^^^^^^^^^^

The following is a small workflow of one-off non-cycling
tasks; these all share a single cycle point (``1``) and don't spawn
successors (once they're all finished the workflow just exits). The integer
``1`` attached to each graph node is just an arbitrary label here.

.. Need to use a 'container' directive to get centered image with
   left-aligned caption (as required for code block text).

.. container:: twocol

   .. container:: caption

      *One-off (Non-Cycling) Tasks*

      .. code-block:: cylc

         [meta]
             title = some one-off tasks
         [scheduling]
             [[graph]]
                 R1 = "foo => bar & baz => qux"

   .. container:: image

      .. _fig-test1:

      .. figure:: ../../img/test1.png
         :align: center

Cycling Graphs
^^^^^^^^^^^^^^

For cycling tasks the graph section heading defines a sequence of cycle points
for which the subsequent graph section is valid, as demonstrated here for a
small workflow of cycling tasks:

.. Need to use a 'container' directive to get centered image with
   left-aligned caption (as required for code block text).

.. container:: twocol

   .. container:: caption

      *Cycling Tasks*

      .. code-block:: cylc

         [meta]
             title = some cycling tasks
         # (no dependence between cycle points)
         [scheduling]
             [[graph]]
                 T00,T12 = "foo => bar & baz => qux"

   .. container:: image

      .. _fig-test2:

      .. figure:: ../../img/test2.png
         :align: center


Graph Section Headings
----------------------

.. tutorial:: Datetime Tutorial <tutorial-datetime-cycling>

Graph section headings define recurrence expressions, the graph within a graph
section heading defines a workflow at each point of the recurrence. For
example in the following scenario:

.. code-block:: cylc

   [scheduling]
       [[graph]]
           T06 = foo => bar

``T06`` means "Run every day starting at 06:00 after the
initial cycle point". Cylc allows you to start (or end) at any particular
time, repeat at whatever frequency you like, and even optionally limit the
number of repetitions.

Graph section heading can also be used with
:ref:`integer cycling <IntegerCycling>`.

Syntax Rules
^^^^^^^^^^^^

:term:`Date-time cycling <datetime cycling>` information is made up of a
starting :term:`datetime <ISO8601 datetime>`, an interval, and an optional
limit.

The time is assumed to be in the local time zone unless you set
:cylc:conf:`[scheduler]cycle point time zone` or :cylc:conf:`[scheduler]UTC mode`.
The calendar is assumed to be the proleptic Gregorian calendar unless
you set :cylc:conf:`[scheduling]cycling mode`.

The syntax for representations is based on the :term:`ISO8601` date-time standard.
This includes the representation of date-times and intervals. What we
define for Cylc's cycling syntax is our own optionally-heavily-condensed form
of ISO8601 recurrence syntax. The most common full form is:
``R[limit?]/[date-time]/[interval]``. However, we allow omitting
information that can be guessed from the context (rules below). This means
that it can be written as:

.. code-block:: sub

   R[limit?]/[date-time]
   R[limit?]//[interval]
   [date-time]/[interval]
   R[limit?] # Special limit of 1 case
   [date-time]
   [interval]

with example graph headings for each form being:

.. code-block:: sub

   R5/T00           # Run 5 times at 00:00 every day
   R//PT1H          # Run every hour (Note the R// is redundant)
   20000101T00Z/P1D # Run every day starting at 00:00 1st Jan 2000
   R1               # Run once at the initial cycle point
   R1/20000101T00Z  # Run once at 00:00 1st Jan 2000
   P1Y              # Run every year

.. note::

   ``T00`` is an example of ``[date-time]``, with an
   inferred 1 day period and no limit.

Where some or all date-time information is omitted, it is inferred to
be relative to the :term:`initial cycle point`. For example, ``T00``
by itself would mean the next occurrence of midnight that follows, or is, the
initial cycle point. Entering ``+PT6H`` would mean 6 hours after the
initial cycle point. Entering ``-P1D`` would mean 1 day before the
initial cycle point. Entering no information for the date-time implies
the initial cycle point date-time itself.

Where the interval is omitted and some (but not all) date-time
information is omitted, it is inferred to be a single unit above
the largest given specific date-time unit. For example, the largest
given specific unit in ``T00`` is hours, so the inferred interval is
1 day (daily), ``P1D``.

Where the limit is omitted, unlimited cycling is assumed. This will be
bounded by the final cycle point's date-time if given.

Another supported form of ISO8601 :term:`recurrence` is:
``R[limit?]/[interval]/[date-time]``. This form uses the
date-time as the end of the cycling sequence rather than the start.
For example, ``R3/P5D/20140430T06`` means:

.. code-block:: none

   20140420T06
   20140425T06
   20140430T06

This kind of form can be used for specifying special behaviour near the end of
the workflow, at the final cycle point's date-time. We can also represent this in
cylc with a collapsed form:

.. code-block:: none

   R[limit?]/[interval]
   R[limit?]//[date-time]
   [interval]/[date-time]

So, for example, you can write:

.. code-block:: sub

   R1//+P0D  # Run once at the final cycle point
   R5/P1D    # Run 5 times, every 1 day, ending at the final
             # cycle point
   P2W/T00   # Run every 2 weeks ending at 00:00 following
             # the final cycle point
   R//T00    # Run every 1 day ending at 00:00 following the
             # final cycle point

.. _referencing-the-initial-and-final-cycle-points:

Referencing The Initial And Final Cycle Points
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

For convenience the caret and dollar symbols may be used as shorthand for the
initial and final cycle points. Using this shorthand you can write:

.. code-block:: sub

   R1/^+PT12H  # Repeat once 12 hours after the initial cycle point
               # R[limit]/[date-time]
               # Equivalent to R1/+PT12H
   R1/$        # Repeat once at the final cycle point
               # R[limit]/[date-time]
               # Equivalent to R1//+P0D
   $-P2D/PT3H  # Repeat 3 hourly starting two days before the
               # [date-time]/[interval]
               # final cycle point

.. note::

   There can be multiple ways to write the same headings, for instance
   the following all run once at the final cycle point:

   .. code-block:: sub

      R1/P0Y       # R[limit]/[interval]
      R1/P0Y/$     # R[limit]/[interval]/[date-time]
      R1/$         # R[limit]/[date-time]

.. _excluding-dates:


The Meaning And Use Of Initial Cycle Point
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

When a workflow is started with the ``cylc play`` command (cold or
warm start) the cycle point at which it starts can be given on the command
line or hardcoded into the :cylc:conf:`flow.cylc` file:

.. code-block:: console

   $ cylc play foo --initial-cycle-point=20120808T06Z

or:

.. code-block:: cylc

   [scheduling]
       initial cycle point = 20100808T06Z

An initial cycle given on the command line will override one in the
flow.cylc file.

.. _setting-the-icp-relative-to-now:

Setting The Initial Cycle Point Relative To The Current Time
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

.. warning::

   Setting the initial cycle point relative to the current time only works
   for :term:`datetime cycling` workflows which use the Gregorian calendar and
   will not work for alternative calendars like the 360, 365 or 366 day
   calendars.

Two additional commands, ``next`` and ``previous``, can be used when setting
the initial cycle point.

The syntax uses truncated ISO8601 time representations, and is of the style:
``next(Thh:mmZ)``, ``previous(T-mm)``; e.g.

* ``initial cycle point = next(T15:00Z)``
* ``initial cycle point = previous(T09:00)``
* ``initial cycle point = next(T12)``
* ``initial cycle point = previous(T-20)``

A list of times, separated by semicolons, can be provided, e.g.
``next(T-00;T-15;T-30;T-45)``. At least one time is required within the
brackets, and if more than one is given, the major time unit in each (hours
or minutes) should all be of the same type.

If an offset from the specified date or time is required, this should be
used in the form: ``previous(Thh:mm) +/- PxTy`` in the same way as is used
for determining cycle periods, e.g.

* ``initial cycle point = previous(T06) +P1D``
* ``initial cycle point = next(T-30) -PT1H``

The section in the bracket attached to the next/previous command is
interpreted first, and then the offset is applied.

The offset can also be used independently without a ``next`` or ``previous``
command, and will be interpreted as an offset from "now".

.. table:: Examples of setting relative initial cycle point for times and offsets using ``now = 2018-03-14T15:12Z`` (and UTC mode)

   ====================================  ==================
   Syntax                                Interpretation
   ====================================  ==================
   ``next(T-00)``                        2018-03-14T16:00Z
   ``previous(T-00)``                    2018-03-14T15:00Z
   ``next(T-00; T-15; T-30; T-45)``      2018-03-14T15:15Z
   ``previous(T-00; T-15; T-30; T-45)``  2018-03-14T15:00Z
   ``next(T00)``                         2018-03-15T00:00Z
   ``previous(T00)``                     2018-03-14T00:00Z
   ``next(T06:30Z)``                     2018-03-15T06:30Z
   ``previous(T06:30) -P1D``             2018-03-13T06:30Z
   ``next(T00; T06; T12; T18)``          2018-03-14T18:00Z
   ``previous(T00; T06; T12; T18)``      2018-03-14T12:00Z
   ``next(T00; T06; T12; T18) +P1W``     2018-03-21T18:00Z
   ``PT1H``                              2018-03-14T16:12Z
   ``-P1M``                              2018-02-14T15:12Z
   ====================================  ==================

The relative initial cycle point also works with truncated dates, including
weeks and ordinal date, using ISO8601 truncated date representations.
Note that day-of-week should always be specified when using weeks. If a time
is not included, the calculation of the next or previous corresponding
point will be done from midnight of the current day.

.. table:: Examples of setting relative initial cycle point for dates using ``now = 2018-03-14T15:12Z`` (and UTC mode)

   ====================================  ==================
   Syntax                                Interpretation
   ====================================  ==================
   ``next(-00)``                         2100-01-01T00:00Z
   ``previous(--01)``                    2018-01-01T00:00Z
   ``next(---01)``                       2018-04-01T00:00Z
   ``previous(--1225)``                  2017-12-25T00:00Z
   ``next(-2006)``                       2020-06-01T00:00Z
   ``previous(-W101)``                   2018-03-05T00:00Z
   ``next(-W-1; -W-3; -W-5)``            2018-03-14T00:00Z
   ``next(-001; -091; -181; -271)``      2018-04-01T00:00Z
   ``previous(-365T12Z)``                2017-12-31T12:00Z
   ====================================  ==================


The Environment Variable CYLC\_WORKFLOW\_INITIAL\_CYCLE\_POINT
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

In the case of a *cold start only* the initial cycle point is passed
through to task execution environments as
``$CYLC_WORKFLOW_INITIAL_CYCLE_POINT``. The value is then stored in
workflow database files and persists across restarts, but it does get wiped out
(set to ``None``) after a warm start, because a warm start is really an
implicit restart in which all state information is lost (except that the
previous cycle is assumed to have completed).

The ``$CYLC_WORKFLOW_INITIAL_CYCLE_POINT`` variable allows tasks to
determine if they are running in the initial cold-start cycle point, when
different behaviour may be required, or in a normal mid-run cycle point.
Note however that an initial ``R1`` graph section is now the preferred
way to get different behaviour at workflow start-up.




How Multiple Graph Strings Combine
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

For a cycling graph with multiple validity sections for different
hours of the day, the different sections *add* to generate the
complete graph. Different graph sections can overlap (i.e. the same
hours may appear in multiple section headings) and the same tasks may
appear in multiple sections, but individual dependencies should be
unique across the entire graph. For example, the following graph defines
a duplicate prerequisite for task C:

.. code-block:: cylc

   [scheduling]
       [[graph]]
           T00,T06,T12,T18 = "A => B => C"
           T06,T18 = "B => C => X"
           # duplicate prerequisite: B => C already defined at T06, T18

This does not affect scheduling, but for the sake of clarity and brevity
the graph should be written like this:

.. code-block:: cylc

   [scheduling]
       [[graph]]
           T00,T06,T12,T18 = "A => B => C"
           # X triggers off C only at 6 and 18 hours
           T06,T18 = "C => X"


Excluding Dates
^^^^^^^^^^^^^^^

:term:`Date-times <ISO8601 datetime>` can be excluded from a :term:`recurrence`
by an exclamation mark for example ``PT1D!20000101`` means run daily except on
the first of January 2000.

This syntax can be used to exclude one or multiple date-times from a
recurrence. Multiple date-times are excluded using the syntax
``PT1D!(20000101,20000102,...)``. All date-times listed within
the parentheses after the exclamation mark will be excluded.

.. note::

   The ``^`` and ``$`` symbols (shorthand for the initial
   and final cycle points) are both date-times so ``T12!$-PT1D``
   is valid.

If using a run limit in combination with an exclusion, the heading might not
run the number of times specified in the limit. For example in the following
workflow ``foo`` will only run once as its second run has been excluded.

.. code-block:: cylc

   [scheduling]
       initial cycle point = 20000101T00Z
       final cycle point = 20000105T00Z
       [[graph]]
           R2/P1D!20000102 = foo

Excluding Recurrences
^^^^^^^^^^^^^^^^^^^^^

In addition to excluding isolated date-time points or lists of date-time points
from recurrences, exclusions themselves may be date-time recurrence sequences.
Any partial date-time or sequence given after the exclamation mark will be
excluded from the main sequence.

For example, partial date-times can be excluded using the syntax:

.. code-block:: sub

   PT1H ! T12                   # Run hourly but not at 12:00 from the initial
                                # cycle point.
   T-00 ! (T00, T06, T12, T18)  # Run hourly but not at 00:00, 06:00,
                                # 12:00, 18:00.
   PT5M ! T-15                  # Run 5-minutely but not at 15 minutes past the
                                # hour from the initial cycle point.
   T00 ! W-1T00                 # Run daily at 00:00 except on Mondays.

It is also valid to use sequences for exclusions. For example:

.. code-block:: sub

   PT1H ! PT6H         # Run hourly from the initial cycle point but
                       # not 6-hourly from the initial cycle point.
   T-00 ! PT6H         # Run hourly on the hour but not 6-hourly on the hour.
   # Same as T-00 ! T-00/PT6H (T-00 context is implied)
   # Same as T-00 ! (T00, T06, T12, T18)
   # Same as PT1H ! (T00, T06, T12, T18) Initial cycle point dependent

   T12 ! T12/P15D      # Run daily at 12:00 except every 15th day.

   R/^/P1H ! R5/20000101T00/P1D    # Any valid recurrence may be used to
                                   # determine exclusions. This example
                                   # translates to: Repeat every hour from
                                   # the initial cycle point, but exclude
                                   # 00:00 for 5 days from the 1st January
                                   # 2000.

You can combine exclusion sequences and single point exclusions within a
comma separated list enclosed in parentheses:

.. code-block:: sub

   T-00 ! (20000101T07, PT2H)  # Run hourly on the hour but not at 07:00
                               # on the 1st Jan, 2000 and not 2-hourly
                               # on the hour.

.. _HowMultipleGraphStringsCombine:


.. _AdvancedCycling:

Advanced Examples
^^^^^^^^^^^^^^^^^

The following examples show the various ways of writing graph headings in Cylc.

.. code-block:: sub

   R1         # Run once at the initial cycle point
   P1D        # Run every day starting at the initial cycle point
   PT5M       # Run every 5 minutes starting at the initial cycle point
   T00/P2W    # Run every 2 weeks starting at 00:00 after the
              # initial cycle point
   +P5D/P1M   # Run every month, starting 5 days after the initial cycle point
   R1/T06     # Run once at 06:00 after the initial cycle point
   R1/P0Y     # Run once at the final cycle point
   R1/$       # Run once at the final cycle point (alternative form)
   R1/$-P3D   # Run once three days before the final cycle point
   R3/T0830   # Run 3 times, every day at 08:30 after the initial cycle point
   R3/01T00   # Run 3 times, every month at 00:00 on the first
              # of the month after the initial cycle point
   R5/W-1/P1M # Run 5 times, every month starting on Monday
              # following the initial cycle point
   T00!^      # Run at the first occurrence of T00 that isn't the
              # initial cycle point
   PT1D!20000101  # Run every day days excluding 1st Jan 2000
   20140201T06/P1D    # Run every day starting at 20140201T06
   R1/min(T00,T06,T12,T18)  # Run once at the first instance
                            # of either T00, T06, T12 or T18
                            # starting at the initial cycle point

.. _AdvancedStartingUp:

Advanced Starting Up
^^^^^^^^^^^^^^^^^^^^

Dependencies that are only valid at the :term:`initial cycle point` can be
written using the ``R1`` notation. For example:

.. code-block:: cylc

   [scheduler]
       UTC mode = True
       allow implicit tasks = True
   [scheduling]
       initial cycle point = 20130808T00
       final cycle point = 20130812T00
       [[graph]]
           R1 = "prep => foo"
           T00 = "foo[-P1D] => foo => bar"

In the example above, ``R1`` implies ``R1/20130808T00``, so
``prep`` only runs once at that cycle point (the initial cycle point).
At that cycle point, ``foo`` will have a dependence on
``prep`` - but not at subsequent cycle points.

However, it is possible to have a workflow that has multiple effective initial
cycles - for example, one starting at ``T00`` and another starting
at ``T12``. What if they need to share an initial task?

Let's suppose that we add the following section to the workflow example above:

.. code-block:: cylc

   [scheduler]
       UTC mode = True
       allow implicit tasks = True
   [scheduling]
       initial cycle point = 20130808T00
       final cycle point = 20130812T00
       [[graph]]
           R1 = "prep => foo"
           T00 = "foo[-P1D] => foo => bar"
           T12 = "baz[-P1D] => baz => qux"

We'll also say that there should be a starting dependence between
``prep`` and our new task ``baz`` - but we still want to have
a single ``prep`` task, at a single cycle.

We can write this using a special case of the ``task[-interval]`` syntax -
if the interval is null, this implies the task at the initial cycle point.

For example, we can write our workflow like so, to produce the graph as shown:

.. Need to use a 'container' directive to get centered image with
   left-aligned caption (as required for code block text).

.. container:: twocol

   .. container:: caption

      *Staggered Start Workflow*

      .. code-block:: cylc

         [scheduler]
             UTC mode = True
             allow implicit tasks = True
         [scheduling]
             initial cycle point = 20130808T00
             final cycle point = 20130812T00
             [[graph]]
                 R1 = "prep"
                 # ^ implies the initial cycle point:
                 R1/T00 = "prep[^] => foo"
                 # ^ is initial cycle point, as above:
                 R1/T12 = "prep[^] => baz"
                 T00 = "foo[-P1D] => foo => bar"
                 T12 = "baz[-P1D] => baz => qux"

   .. container:: image

      .. _fig-test4:

      .. figure:: ../../img/test4.png
         :align: center


This neatly expresses what we want - a task running at the initial cycle point
that has one-off dependencies with other task sets at different cycles.

Cylc also caters for a different kind of requirement.

Usually, we want to specify additional tasks and dependencies at the initial
cycle point. What if we want our first cycle point to be entirely special,
with some tasks missing compared to subsequent cycle points?

In the workflow below, ``bar`` will not be run at the initial
cycle point, but will still run at subsequent cycle points, where
``+PT6H/PT6H`` means start at ``+PT6H`` (6 hours after
the initial cycle point) and then repeat every ``PT6H`` (6 hours):

.. Need to use a 'container' directive to get centered image with
   left-aligned caption (as required for code block text).

.. container:: twocol

   .. container:: caption

      *Restricted First Cycle Point Workflow*

      .. code-block:: cylc

          [scheduler]
              UTC mode = True
              allow implicit tasks = True
          [scheduling]
              initial cycle point = 20130808T00
              final cycle point = 20130808T18
              [[graph]]
                  R1 = "setup_foo => foo"
                  +PT6H/PT6H = """
                      foo[-PT6H] => foo
                      foo => bar
                  """

   .. container:: image

      .. _fig-test5:

      .. figure:: ../../img/test5.png
         :align: center


Some workflows may have staggered start-up sequences where different tasks need
running once but only at specific cycle points, potentially due to differing
data sources at different cycle points with different possible initial cycle
points. To allow this Cylc provides a ``min( )`` function that can be
used as follows:

.. code-block:: cylc

   [scheduler]
       UTC mode = True
       allow implicit tasks = True
   [scheduling]
       initial cycle point = 20100101T03
       [[graph]]
           R1/min(T00,T12) = "prep1 => foo"
           R1/min(T06,T18) = "prep2 => foo"
           T00,T06,T12,T18 = "foo => bar"


In this example the initial cycle point is ``20100101T03``, so the
``prep1`` task will run once at ``20100101T12`` and the
``prep2`` task will run once at ``20100101T06`` as these are
the first cycle points after the initial cycle point in the respective
``min( )`` entries.

.. _IntegerCycling:

Integer Cycling
^^^^^^^^^^^^^^^

.. tutorial:: Integer Cycling Tutorial <tutorial-integer-cycling>

In addition to non-repeating and :term:`datetime cycling` workflows, Cylc can do
:term:`integer cycling` for repeating workflows that are not date-time based.

To construct an integer cycling workflow, set
:cylc:conf:`[scheduling]cycling mode = integer`, and specify integer values
for the :term:`initial cycle point` and optionally the
:term:`final cycle point`. The notation for intervals,
offsets, and :term:`recurrences <recurrence>` (sequences) is similar to the
date-time cycling notation, except for the simple integer values.

The full integer recurrence expressions supported are:

- ``Rn/start-point/interval # e.g. R3/1/P2``
- ``Rn/interval/end-point # e.g. R3/P2/9``

But, as for date-time cycling, sequence start and end points can be omitted
where workflow initial and final cycle points can be assumed. Some examples:

.. code-block:: sub

   R1        # Run once at the initial cycle point
             # (short for R1/initial-point/?)
   P1        # Repeat with step 1 from the initial cycle point
             # (short for R/initial-point/P1)
   P5        # Repeat with step 5 from the initial cycle point
             # (short for R/initial-point/P5)
   R2//P2    # Run twice with step 3 from the initial cycle point
             # (short for R2/initial-point/P2)
   R/+P1/P2  # Repeat with step 2, from 1 after the initial cycle point
   R2/P2     # Run twice with step 2, to the final cycle point
             # (short for R2/P2/final-point)
   R1/P0     # Run once at the final cycle point
             # (short for R1/P0/final-point)

Advanced Integer Cycling Syntax
"""""""""""""""""""""""""""""""

The same syntax used to reference the initial and final cycle points
(introduced in :ref:`referencing-the-initial-and-final-cycle-points`) for
use with date-time cycling can also be used for integer cycling. For
example you can write:

.. code-block:: sub

   R1/^     # Run once at the initial cycle point
   R1/$     # Run once at the final cycle point
   R3/^/P2  # Run three times with step two starting at the
                    # initial cycle point

Likewise the syntax introduced in :ref:`excluding-dates` for excluding
a particular point from a recurrence also works for integer cycling. For
example:

.. code-block:: sub

   R/P4!8       # Run with step 4, to the final cycle point but not at point 8
   R3/3/P2!5    # Run with step 2 from point 3 but not at point 5
   R/+P1/P6!14  # Run with step 6 from 1 step after the
                # initial cycle point but not at point 14

Multiple integer exclusions are also valid in the same way as the syntax
in :ref:`excluding-dates`. Integer exclusions may be a list of single
integer points, an integer sequence, or a combination of both:

.. code-block:: sub

   R/P1!(2,3,7)  # Run with step 1 to the final cycle point,
                 # but not at points 2, 3, or 7.
   P1 ! P2       # Run with step 1 from the initial to final
                 # cycle point, skipping every other step from
                 # the initial cycle point.
   P1 ! +P1/P2   # Run with step 1 from the initial cycle point,
                 # excluding every other step beginning one step
                 # after the initial cycle point.
   P1 !(P2,6,8)  # Run with step 1 from the initial cycle point,
                 # excluding every other step, and also excluding
                 # steps 6 and 8.

An Integer Cycling Example
""""""""""""""""""""""""""

.. _fig-integer-pipeline:

.. figure::/img/pipe-pub.png
   :align: center

The following workflow definition, as :ref:`graphed above <fig-integer-pipeline>`,
implements a classical linear pipeline using integer cycling. The workflow
ensures that one instance each of A, B, and C runs concurrently and the
pipeline is kept full: when A.1 has finished processing the first dataset, A.2
can start on the second one at the same time as B.1 begins processing the
output of A.1, and so on. The artificial cross-cycle dependence ensures that
only one instance of A can run at a time; and similarly B and C. If available
compute resource supports more than three concurrent jobs, remove the
cross-cycle dependence and Cylc will run many cycles at once. Task runtime
configuration is omitted, but it would likely involve retrieving datasets by
cycle point and processing them in cycle point-specific shared workspaces under
the self-contained run directory.

.. literalinclude:: ../../workflows/integer-pipeline/flow.cylc
   :language: cylc


.. _TriggerTypes:

Task Triggering
---------------

A task is said to :term:`trigger` when it submits its job to run, as soon as all of
its dependencies (also known as its separate "triggers") are met. Tasks can
be made to trigger off of the state of other tasks (indicated by a
``:state`` :term:`qualifier` on the upstream task (or family)
name in the graph) and, and off the clock, and arbitrary external events.

External triggering is relatively more complicated, and is documented
separately in :ref:`Section External Triggers`.


Success Triggers
^^^^^^^^^^^^^^^^

The default, with no trigger type specified, is to trigger off the
upstream task succeeding:

.. code-block:: cylc

   # B triggers if A SUCCEEDS:
       R1 = "A => B"

For consistency and completeness, however, the success trigger can be
explicit:

.. code-block:: cylc

   # B triggers if A SUCCEEDS:
       R1 = "A => B"
   # or:
       R1 = "A:succeed => B"


Failure Triggers
^^^^^^^^^^^^^^^^

To trigger off the upstream task reporting failure:

.. code-block:: cylc

   # B triggers if A FAILS:
       R1 = "A:fail => B"

*Suicide triggers* can be used to remove task ``B`` here if
``A`` does not fail, see :ref:`SuicideTriggers`.


Start Triggers
^^^^^^^^^^^^^^

To trigger off the upstream task starting to execute:

.. code-block:: cylc

   # B triggers if A STARTS EXECUTING:
       R1 = "A:start => B"

This can be used to trigger tasks that monitor other tasks once they
(the target tasks) start executing. Consider a long-running forecast model,
for instance, that generates a sequence of output files as it runs. A
postprocessing task could be launched with a start trigger on the model
(``model:start => post``) to process the model output as it
becomes available. Note, however, that there are several alternative
ways of handling this scenario: both tasks could be triggered at the
same time (``foo => model & post``), but depending on
external queue delays this could result in the monitoring task starting
to execute first; or a different postprocessing task could be
triggered off a message output for each data file
(``model:out1 => post1`` etc.; see :ref:`MessageTriggers`), but this
may not be practical if the
number of output files is large or if it is difficult to add Cylc
messaging calls to the model.


Finish Triggers
^^^^^^^^^^^^^^^

To trigger off the upstream task succeeding or failing, i.e. finishing
one way or the other:

.. code-block:: cylc

   # B triggers if A either SUCCEEDS or FAILS:
       R1 = "A | A:fail => B"
   # or
       R1 = "A:finish => B"


.. _MessageTriggers:

Message Triggers
^^^^^^^^^^^^^^^^

.. tutorial:: Message Trigger Tutorial <tutorial-cylc-message-triggers>

Tasks can also trigger off custom output messages. These must be registered in
the :cylc:conf:`[runtime][<namespace>][outputs]` section of the emitting task,
and reported using the ``cylc message`` command in task scripting.
The graph trigger notation refers to the item name of the registered
output message. An example message triggering workflow:

.. literalinclude:: ../../workflows/message-triggers/flow.cylc
   :language: cylc


Job Submission Triggers
^^^^^^^^^^^^^^^^^^^^^^^

It is also possible to trigger off a task submitting, or failing to submit:

.. code-block:: cylc

   # B triggers if A submits successfully:
       R1 = "A:submit => B"
   # D triggers if C fails to submit successfully:
       R1 = "C:submit-fail => D"

A possible use case for submit-fail triggers: if a task goes into the
submit-failed state, possibly after several job submission retries,
another task that inherits the same runtime but sets a different job
submission method and/or host could be triggered to, in effect, run the
same job on a different platform.


Conditional Triggers
^^^^^^^^^^^^^^^^^^^^

:term:`Conditional triggers <conditional trigger>` allow the configuration of
more advanced task dependencies.

AND operators (``&``) can appear on both sides of an arrow. They
provide a concise alternative to defining multiple triggers separately:

.. code-block:: cylc

   # 1/ this:
       R1 = "A & B => C"
   # is equivalent to:
       R1 = """
           A => C
           B => C
       """
   # 2/ this:
       R1 = "A => B & C"
   # is equivalent to:
       R1 = """
           A => B
           A => C
       """
   # 3/ and this:
       R1 = "A & B => C & D"
   # is equivalent to this:
       R1 = """
           A => C
           B => C
           A => D
           B => D
       """

OR operators (``|``) which result in true conditional triggers,
can only appear on the left [1]_ :

.. code-block:: cylc

   # C triggers when either A or B finishes:
       R1 = "A | B => C"

Any valid conditional expression can be used, as shown in the graph below,
where conditional triggers are plotted with open arrow heads:

.. Need to use a 'container' directive to get centered image with
   left-aligned caption (as required for code block text).

.. container:: twocol

   .. container:: caption

      *Conditional triggers*

      .. code-block:: cylc-graph

         # D triggers if A or (B and C) succeed
         A | B & C => D
         # just to align the two graph sections
         D => W
         # Z triggers if (W or X) and Y succeed
         (W|X) & Y => Z

   .. container:: image

      .. _fig-conditional:

      .. figure:: ../../img/conditional-triggers.png
         :align: center


.. _SuicideTriggers:

Suicide Triggers
^^^^^^^^^^^^^^^^

.. tutorial:: Suicide Trigger Tutorial <tut-cylc-suicide-triggers>

Suicide triggers take tasks out of the workflow. This can be used for automated
failure recovery. The following :cylc:conf:`flow.cylc` listing and accompanying
:term:`graph` show how to define a chain of failure recovery tasks that trigger
if they're needed but otherwise remove themselves from the workflow (you can run
the *AutoRecover.async* example workflow to see how this works). The dashed graph
edges ending in solid dots indicate suicide triggers, and the open arrowheads
indicate conditional triggers as usual.

.. Need to use a 'container' directive to get centered image with
   left-aligned caption (as required for code block text).

.. container:: twocol

   .. container:: caption

      *Automated failure recovery via suicide triggers*

      .. code-block:: cylc

          [meta]
              title = automated failure recovery
              description = """
                  Model task failure triggers diagnosis
                  and recovery tasks, which take themselves
                  out of the workflow if model succeeds. Model
                  post processing triggers off model OR
                  recovery tasks.
              """
          [scheduling]
              [[graph]]
                  R1 = """
                      pre => model
                      model:fail => diagnose => recover
                      model => !diagnose & !recover
                      model | recover => post
                  """
          [runtime]
              [[model]]
                  # UNCOMMENT TO TEST FAILURE:
                  # script = /bin/false

   .. container:: image

      .. _fig-suicide:

      .. figure:: ../../img/suicide.png
         :align: center


.. note::

   Multiple suicide triggers combine in the same way as other
   triggers, so this:

   .. code-block:: cylc-graph

      foo => !baz
      bar => !baz

   is equivalent to this:

   .. code-block:: cylc-graph

      foo & bar => !baz

   i.e. both ``foo`` and ``bar`` must succeed for
   ``baz`` to be taken out of the workflow. If you really want a task
   to be taken out if any one of several events occurs then be careful to
   write it that way:

   .. code-block:: cylc-graph

      foo | bar => !baz

.. warning::

   A word of warning on the meaning of "bare suicide triggers". Consider
   the following workflow:

   .. code-block:: cylc

      [scheduling]
          [[graph]]
              R1 = "foo => !bar"

   Task ``bar`` has a suicide trigger but no normal prerequisites
   (a suicide trigger is not a task triggering prerequisite, it is a task
   removal prerequisite) so this is entirely equivalent to:

   .. code-block:: cylc

      [scheduling]
          [[graph]]
              R1 = """
                  foo & bar
                  foo => !bar
              """

   In other words both tasks will trigger immediately, at the same time,
   and then ``bar`` will be removed if ``foo`` succeeds.

If an active task proxy (currently in the submitted or running states)
is removed from the workflow by a suicide trigger, a warning will be logged.


.. _FamilyTriggers:

Family Triggers
^^^^^^^^^^^^^^^

:term:`Families <family>` defined by the namespace inheritance hierarchy
(:ref:`User Guide Runtime`) can be used in the graph to :term:`trigger` whole
groups of tasks at the same time (e.g. forecast model ensembles and groups of
tasks for processing different observation types at the same time) and for
triggering downstream tasks off families as a whole. Higher level families,
i.e. families of families, can also be used, and are reduced to the lowest
level member tasks.

.. note::

   Tasks can also trigger off individual family members if necessary.

To trigger an entire task family at once:

.. code-block:: cylc

   [scheduling]
       [[graph]]
           R1 = "foo => FAM"
   [runtime]
       [[FAM]]    # a family (because others inherit from it)
       [[m1,m2]]  # family members (inherit from namespace FAM)
           inherit = FAM

This is equivalent to:

.. code-block:: cylc

   [scheduling]
       [[graph]]
           R1 = "foo => m1 & m2"
   [runtime]
       [[FAM]]
       [[m1,m2]]
           inherit = FAM

To trigger other tasks off families we have to specify whether
to triggering off *all members* starting, succeeding, failing,
or finishing, or off *any* members (doing the same). Legal family
triggers are thus:

.. code-block:: cylc

   [scheduling]
       [[graph]]
           R1 = """
               # all-member triggers:
               FAM:start-all => one
               FAM:succeed-all => one
               FAM:fail-all => one
               FAM:finish-all => one
               # any-member triggers:
               FAM:start-any => one
               FAM:succeed-any => one
               FAM:fail-any => one
               FAM:finish-any => one
           """

Here's how to trigger downstream processing after if one or more family
members succeed, but only after all members have finished (succeeded or
failed):

.. code-block:: cylc

   [scheduling]
       [[graph]]
           R1 = """
              FAM:finish-all & FAM:succeed-any => foo
           """


.. _EfficientInterFamilyTriggering:

Efficient Inter-Family Triggering
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. TODO: Is this section still true post-SoD?

While Cylc allows writing :term:`dependencies <dependency>` between two
:term:`families <family>` it is important to consider the number of
dependencies this will generate. In the following example, each member of
``FAM2`` has dependencies pointing at all the members of ``FAM1``.

.. code-block:: cylc

   [scheduling]
       [[graph]]
           R1 = """
               FAM1:succeed-any => FAM2
           """

Expanding this out, you generate ``N * M`` dependencies, where ``N`` is the
number of members of ``FAM1`` and ``M`` is the number of members of ``FAM2``.
This can result in high memory use as the number of members of these families
grows, potentially rendering the workflow impractical for running on some systems.

You can greatly reduce the number of dependencies generated in these situations
by putting blank tasks in the graphing to represent the state of the family you
want to trigger off. For example, if ``FAM2`` should trigger off any
member of ``FAM1`` succeeding you can create a blank task
``FAM1_succeed_any_marker`` and place a dependency on it as follows:

.. code-block:: cylc

   [scheduling]
       [[graph]]
           R1 = """
               FAM1:succeed-any => FAM1_succeed_any_marker => FAM2
           """
   [runtime]
   # ...
       [[FAM1_succeed_any_marker]]
           script = true
   # ...

This :term:`graph` generates only ``N + M`` dependencies, which takes
significantly less memory and CPU to store and evaluate.


.. _InterCyclePointTriggers:

Inter-Cycle Triggers
^^^^^^^^^^^^^^^^^^^^

Typically most tasks in a workflow will trigger off others in the same
cycle point, but some may depend on others with other cycle points.
This notably applies to warm-cycled forecast models, which depend on
their own previous instances (see below); but other kinds of
:term:`inter-cycle dependence <inter-cycle dependency>` are possible too [2]_ .
Here's how to express this kind of relationship in cylc:

.. code-block:: cylc

   [[graph]]
       # B triggers off A in the previous cycle point
       PT6H = "A[-PT6H] => B"

inter-cycle and trigger type (or message trigger) notation can be
combined:

.. code-block:: cylc

   # B triggers if A in the previous cycle point fails:
   PT6H = "A[-PT6H]:fail => B"

At workflow start-up inter-cycle triggers refer to a previous cycle point
that does not exist. This does not cause the dependent task to wait
indefinitely, however, because Cylc ignores triggers that reach back
beyond the initial cycle point. That said, the presence of an
inter-cycle trigger does normally imply that something special has to
happen at start-up. If a model depends on its own previous instance for
restart files, for instance, then an initial set of restart files has to be
generated somehow or the first model task will presumably fail with
missing input files. There are several ways to handle this in Cylc
using different kinds of one-off (non-cycling) tasks that run at workflow
start-up.

- ``R1`` tasks (recommended):

  .. code-block:: cylc

     [scheduling]
         [[graph]]
             R1 = "prep"
             R1/T00,R1/T12 = "prep[^] => foo"
             T00,T12 = "foo[-PT12H] => foo => bar"

``R1``, or ``R1/date-time`` tasks are the recommended way to
specify unusual start up conditions. They allow you to specify a clean
distinction between the dependencies of initial cycles and the dependencies
of the subsequent cycles.

Initial tasks can be used for real model cold-start processes, whereby a
warm-cycled model at any given cycle point can in principle have its inputs
satisfied by a previous instance of itself, *or* by an initial task with
(nominally) the same cycle point.

In effect, the ``R1`` task masquerades as the previous-cycle-point trigger
of its associated cycling task. At workflow start-up initial tasks will
trigger the first cycling tasks, and thereafter the inter-cycle trigger
will take effect.

If a task has a dependency on another task in a different cycle point, the
dependency can be written using the ``[offset]`` syntax such as
``[-PT12H]`` in ``foo[-PT12H] => foo``. This means that
``foo`` at the current cycle point depends on a previous instance of
``foo`` at 12 hours before the current cycle point. Unlike recurrences
(e.g. ``T00,T12``), dependencies assume that relative times are relative to the
current cycle point, not the initial cycle point.

However, it can be useful to have specific dependencies on tasks at or near
the initial cycle point. You can switch the context of the offset to be
the initial cycle point by using the caret symbol: ``^``.

For example, you can write ``foo[^]`` to mean foo at the initial
cycle point, and ``foo[^+PT6H]`` to mean foo 6 hours after the initial
cycle point. Usually, this kind of dependency will only apply in a limited
number of cycle points near the start of the workflow, so you may want to write
it in ``R1``-based graphs. Here's the example inter-cycle
``R1`` workflow from above again.

.. code-block:: cylc

   [scheduling]
       [[graph]]
           R1 = "prep"
           R1/T00,R1/T12 = "prep[^] => foo"
           T00,T12 = "foo[-PT12H] => foo => bar"

You can see there is a dependence on the initial ``R1`` task
``prep`` for ``foo`` at the first ``T00`` cycle point,
and at the first ``T12`` cycle point. Thereafter, ``foo`` just
depends on its previous (12 hours ago) instance.

Finally, it is also possible to have a dependency on a task at a specific cycle
point.

.. code-block:: cylc

   [scheduling]
       [[graph]]
           R1/20200202 = "baz[20200101] => qux"

However, in a long running workflow, a repeating cycle should avoid having a
dependency on a task with a specific cycle point (including the initial cycle
point) - as it can currently cause performance issue. In the following example,
all instances of ``qux`` will depend on ``baz.20200101``, which
will never be removed from the task pool:

.. code-block:: cylc

   [scheduling]
       initial cycle point = 2010
       [[graph]]
           # Can cause performance issue!
           P1D = "baz[20200101] => qux"


.. _SequentialTasks:

Special Sequential Tasks
^^^^^^^^^^^^^^^^^^^^^^^^

Tasks that depend on their own previous-cycle instance can be declared as
*sequential*:

.. code-block:: cylc

   [scheduling]
       [[special tasks]]
           # foo depends on its previous instance:
           sequential = foo  # deprecated - see below!
       [[graph]]
           T00,T12 = "foo => bar"

*The sequential declaration is deprecated* however, in favor of explicit
inter-cycle triggers which clearly expose the same scheduling behaviour in the
graph:

.. code-block:: cylc

   [scheduling]
       [[graph]]
           # foo depends on its previous instance:
           T00,T12 = "foo[-PT12H] => foo => bar"

The sequential declaration is arguably convenient in one unusual situation
though: if a task has a non-uniform cycling sequence then multiple explicit
triggers,

.. code-block:: cylc

   [scheduling]
       [[graph]]
           T00,T03,T11 = "foo => bar"
           T00 = "foo[-PT13H] => foo"
           T03 = "foo[-PT3H] => foo"
           T11 = "foo[-PT8H] => foo"

can be replaced by a single sequential declaration,

.. code-block:: cylc

   [scheduling]
       [[special tasks]]
           sequential = foo
       [[graph]]
           T00,T03,T11 = "foo => bar"


Future Triggers
^^^^^^^^^^^^^^^

Cylc also supports :term:`inter-cycle triggering <inter-cycle trigger>` off
tasks "in the future" (with respect to cycle point - which has no bearing on
wall-clock job submission time unless the task has a clock trigger):

.. code-block:: cylc

   [[graph]]
       T00,T06,T12,T18 = """
           # A runs in this cycle:
           A
           # B in this cycle triggers off A in the next cycle.
           A[PT6H] => B
       """

Future triggers present a problem at workflow shutdown rather than at start-up.
Here, ``B`` at the final cycle point wants to trigger off an instance
of ``A`` that will never exist because it is beyond the workflow stop
point. Consequently Cylc prevents tasks from spawning successors that depend on
other tasks beyond the final point.


.. _ClockTriggerTasks:

Clock Triggers
^^^^^^^^^^^^^^

.. note::

   Please read External Triggers (:ref:`Section External Triggers`) before
   using the older clock triggers described in this section.

By default, date-time cycle points are not connected to the real time
(the :term:`wall-clock time`).
They are just labels that are passed to task jobs (e.g. to
initialize an atmospheric model run with a particular date-time value). In real
time cycling systems, however, some tasks - typically those near the top of the
graph in each cycle - need to trigger at or near the time when their cycle point
is equal to the real clock date-time.

So *clock triggers* allow tasks to trigger at (or after, depending on other
triggers) a wall clock time expressed as an offset from cycle point:

.. code-block:: cylc

   [scheduling]
       [[special tasks]]
           clock-trigger = foo(PT2H)
       [[graph]]
           T00 = foo

Here, ``foo[2015-08-23T00]`` would trigger (other dependencies allowing)
when the wall clock time reaches ``2015-08-23T02``. Clock-trigger
offsets are normally positive, to trigger some time *after* the wall-clock
time is equal to task cycle point.

Clock-triggers have no effect on scheduling if a workflow is running sufficiently
far behind the clock (e.g. after a delay, or because it is processing archived
historical data) that the trigger times, which are relative to task cycle
point, have already passed.


.. _ClockExpireTasks:

Clock-Expire Triggers
^^^^^^^^^^^^^^^^^^^^^

Tasks can be configured to *expire* - i.e. to skip job submission and
enter the *expired* state - if they are too far behind the wall clock when
they become ready to run, and other tasks can trigger off this. As a possible
use case, consider a cycling task that copies the latest of a set of files to
overwrite the previous set: if the task is delayed by more than one cycle there
may be no point in running it because the freshly copied files will just be
overwritten immediately by the next task instance as the workflow catches back up
to real time operation. Clock-expire tasks are configured with
:cylc:conf:`[scheduling][special tasks]clock-expire` using a syntax like
:cylc:conf:`clock-trigger <[scheduling][special tasks]clock-trigger>`
with a date-time offset relative to cycle point.
The offset should be positive to make the task expire if the wall-clock time
has gone beyond the cycle point. Triggering off an expired task typically
requires suicide triggers to remove the workflow that runs if the task has not
expired. Here a task called ``copy`` expires, and its downstream
workflow is skipped, if it is more than one day behind the wall-clock:

.. code-block:: cylc

   [scheduler]
      allow implicit tasks = True
      cycle point format = %Y-%m-%dT%H
   [scheduling]
       initial cycle point = 2015-08-15T00
       [[special tasks]]
           clock-expire = copy(-P1D)
       [[graph]]
           P1D = """
               model[-P1D] => model => copy => proc
               copy:expired => !proc
           """


.. _WorkflowConfigExternalTriggers:

External Triggers
^^^^^^^^^^^^^^^^^

This is a substantial topic, documented in :ref:`Section External Triggers`.


Limiting Triggering
-------------------

Cylc will usually try to trigger any task with met dependencies. This can
risk running more tasks than you wish to. :ref:`RunaheadLimit` and
:ref:`InternalQueues` provide tools for you to control the trigging of ready
tasks.

.. _RunaheadLimit:

Runahead Limiting
^^^^^^^^^^^^^^^^^

Runahead limiting prevents the fastest tasks in a workflow from getting too far
ahead of the slowest ones.

For example in the following workflow the runahead limit of ``P5`` restricts the
workflow so that only five consecutive cycles may run simultaneously.

.. code-block:: cylc

    [scheduling]
        initial cycle point = 1
        cycling mode = integer
        runahead limit = P5
        [[graph]]
            P1 = foo

When this workflow is started the tasks ``foo.1`` -> ``foo.5`` will be submitted,
however, the tasks from ``foo.6`` onwards are said to be "runahead limited"
and will not be submitted.

Succeeded and failed tasks are ignored when computing the runahead limit. This
functionality is controlled by the :cylc:conf:`[scheduling]runahead limit`
which can be set to either:

* A number of consecutive cycles.
* Or a time interval between the oldest and newest cycles.

A low runahead limit can prevent Cylc from interleaving cycles, but it will not
stall a workflow unless it fails to extend out past a future trigger (see
:ref:`InterCyclePointTriggers`).

A high runahead limit may allow fast tasks
that are not constrained by dependencies or clock-triggers to spawn far ahead
of the pack, which could have performance implications for the
:term:`scheduler` when running very large workflows.

See the :cylc:conf:`[scheduling]runahead limit` configuration for more details.


.. _InternalQueues:

Limiting Activity With Internal Queues
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Large workflows can potentially overwhelm task hosts by submitting too many
tasks at once. You can prevent this with *internal queues*, which
limit the number of tasks that can be active (submitted or running)
at the same time.

Internal queues behave in the first-in-first-out (FIFO) manner, i.e. tasks are
released from a queue in the same order that they were queued.

A queue is defined by a *name*; a *limit*, which is the maximum
number of active tasks allowed for the queue; and a list of *members*,
assigned by task or family name.

Queue configuration is done in the :cylc:conf:`[scheduling][queues]` section.

By default every task is assigned to the ``default`` queue, which by default
has a zero limit (interpreted by cylc as no limit). To use a single queue for
the whole workflow just set the default queue limit:

.. code-block:: cylc

   [scheduling]
       [[queues]]
           # limit the entire workflow to 5 active tasks at once
           [[[default]]]
               limit = 5

To use additional queues just name each one, set their limits, and assign
members:

.. code-block:: cylc

   [scheduling]
       [[queues]]
           [[[q_foo]]]
               limit = 5
               members = foo, bar, baz

Any tasks not assigned to a particular queue will remain in the default
queue. The *queues* example workflow illustrates how queues work by
running two task trees side by side each
limited to 2 and 3 tasks respectively:

.. literalinclude:: ../../workflows/queues/flow.cylc
   :language: cylc


.. _Graph Branching:

Graph Branching
---------------

.. versionadded:: 8.0.0

Cylc handles :term:`graphs <graph>` in an event-driven manner which means
that a workflow can follow different paths in different eventualities.
This is called :term:`branching`.

.. note::

   Before Cylc 8 graphs were not event-driven so
   :term:`suicide triggers <suicide trigger>`
   were used to allow the graph to evolve at runtime.

Basic Example
^^^^^^^^^^^^^

In this example Cylc will follow one of two possible "branches" depending
on the outcome of task ``b``:

* If ``b`` succeeds then the task ``c`` will run.
* If ``b`` fails then the task ``r`` will run.

Task ``d`` will run after either ``c`` or ``r`` succeeds.

.. digraph:: example
   :align: center

   subgraph cluster_success {
      label = ":succeed"
      color = "green"
      fontcolor = "green"
      style = "dashed"

      c
   }

   subgraph cluster_failure {
      label = ":fail"
      color = "red"
      fontcolor = "red"
      style = "dashed"

      r
   }

   a -> b -> c -> d
   b -> r -> d

.. code-block:: cylc

   [scheduling]
       [[graph]]
           R1 = """
               # the success path
               a => b => c
               # the fail path
               a => b:fail => r
               # carrying on with the rest of the workflow
               c | r => d
           """

Note the last line of the graph ``c | r => d`` which allows the graph to
continue on to ``d`` irrespective of which path has been taken.

Message Trigger Example
^^^^^^^^^^^^^^^^^^^^^^^

Branching is particularly powerful when combined with :ref:`MessageTriggers`,
here is an example showing how message triggers can be used to define multiple
parallel pathways.

In this graph there is a task called ``showdown`` which produces one of three
possible custom outputs, ``good``, ``bad`` or ``ugly``. Cylc will follow
a different path depending on which of these three outputs is produced:

.. digraph:: Example
   :align: center

   subgraph cluster_1 {
      label = ":good"
      color = "green"
      fontcolor = "green"
      style = "dashed"
      good
   }
   subgraph cluster_2 {
      label = ":bad"
      color = "red"
      fontcolor = "red"
      style = "dashed"
      bad
   }
   subgraph cluster_3 {
      label = ":ugly"
      color = "purple"
      fontcolor = "purple"
      style = "dashed"
      ugly
   }
   showdown -> good
   showdown -> bad
   showdown -> ugly
   good -> fin [arrowhead="onormal"]
   bad -> fin [arrowhead="onormal"]
   ugly -> fin [arrowhead="onormal"]

As with the previous example each path begins with a different outcome
of a particular task and ends with an "or" dependency to allow the workflow
to continue irrespective of which path was taken:

.. code-block:: cylc

   [scheduling]
       [[graph]]
           R1 = """
              showdown
              showdown:good => good
              showdown:bad => bad
              showdown:ugly => ugly
              good | bad | ugly => fin
           """

   [runtime]
       [[root]]
           script = sleep 1
       [[showdown]]
           # Randomly return one of the three custom outputs.
           script = """
               SEED=$RANDOM
               if ! (( $SEED % 3 )); then
                   cylc message 'The-Good'
               elif ! (( ( $SEED + 1 ) % 3 )); then
                   cylc message 'The-Bad'
               else
                   cylc message 'The-Ugly'
               fi
           """
           [[[outputs]]]
               # Register the three custom outputs with cylc.
               good = 'The-Good'
               bad = 'The-Bad'
               ugly = 'The-Ugly'

When using message triggers in this way there are two things to be aware of:

1. Message triggers are not exit states.

   Message triggers are produced ``before`` a task has completed, consequently,
   it can be useful to combine a message trigger with a regular trigger for
   safety e.g:

   .. code-block:: cylc-graph

      # good will wait for showdown to finish before running
      showdown:finish & showdown:good => good

      # if showdown fails then good will not run
      showdown:succeed & showdown:good => good

2. Message triggers are not mutually exclusive.

   There is nothing in Cylc to prevent a task from producing multiple outputs
   e.g. ``good``, ``bad`` and ``ugly``.

   This is hard to defend against, ensure that the task that produces these
   outputs is written in such a way that this cannot happen.


.. _ModelRestartDependencies:

Model Restart Dependencies
--------------------------

Warm-cycled forecast models generate *restart files*, e.g. model
background fields, to initialize the next forecast. This kind of
dependence requires an inter-cycle trigger:

.. code-block:: cylc

   [scheduling]
       [[graph]]
           T00,T06,T12,T18 = "A[-PT6H] => A"

If your model is configured to write out additional restart files
to allow one or more cycle points to be skipped in an emergency *do not
represent these potential dependencies in the workflow graph* as they
should not be used under normal circumstances. For example, the
following graph would result in task ``A`` erroneously
triggering off ``A[T-24]`` as a matter of course, instead of
off ``A[T-6]``, because ``A[T-24]`` will always
be finished first:

.. code-block:: cylc

   [scheduling]
       [[graph]]
           # DO NOT DO THIS (SEE ACCOMPANYING TEXT):
           T00,T06,T12,T18 = "A[-PT24H] | A[-PT18H] | A[-PT12H] | A[-PT6H] => A"


How The Graph Determines Task Instantiation
-------------------------------------------

A graph trigger pair like ``foo => bar`` determines the existence and
prerequisites (dependencies) of the downstream task ``bar``, for
the cycle points defined by the associated graph section heading. In general it
does not say anything about the dependencies or existence of the upstream task
``foo``. However *if the trigger has no cycle point offset* Cylc
will infer that ``bar`` must exist at the same cycle points as
``foo``. This is a convenience to allow this:

.. code-block:: cylc

   R1 = "foo => bar"

to be written as shorthand for this:

.. code-block:: cylc

   R1 = """
       foo
       foo => bar
   """

(where ``foo`` by itself means ``<nothing> => foo``, i.e. the
task exists at these cycle points but has no prerequisites - although other
prerequisites may be defined for it in other parts of the graph).

*Cylc does not infer the existence of the upstream task in offset
triggers* like ``foo[-P1D] => bar`` because a typo in the offset
interval should generate an error rather than silently creating
tasks on an erroneous cycling sequence.

As a result you need to be careful not to define inter-cycle dependencies that
cannot be satisfied at run time. Workflow validation catches this kind of error if
the existence of the cycle offset task is not defined anywhere at all:

.. code-block:: cylc

   [scheduling]
       initial cycle point = 2020
       [[graph]]
           # ERROR
           P1Y = "foo[-P1Y] => bar"

.. code-block:: console

   $ cylc validate WORKFLOW
   'ERROR: No cycling sequences defined for foo'

To fix this, use another line in the graph to tell Cylc to define
``foo`` at each cycle point:

.. code-block:: cylc

   [scheduling]
       initial cycle point = 2020
       [[graph]]
           P1Y = """
               foo
               foo[-P1Y] => bar
           """

But validation does not catch this kind of error if the offset task
is defined only on a different cycling sequence:

.. code-block:: cylc

   [scheduling]
       initial cycle point = 2020
       [[graph]]
           # ERROR
           P2Y = """
               foo
               foo[-P1Y] => bar
           """

This workflow will validate OK, but it will stall at runtime with ``bar``
waiting on ``foo[-P1Y]`` at the intermediate years where it does not
exist. The offset ``[-P1Y]`` is presumably an error (it should be
``[-P2Y]``), or else another graph line is needed to generate
``foo`` instances on the yearly sequence:

.. code-block:: cylc

   [scheduling]
       initial cycle point = 2020
       [[graph]]
           P1Y = "foo"
           P2Y = "foo[-P1Y] => bar"

Similarly the following workflow will validate OK, but it will stall at
runtime with ``bar`` waiting on ``foo[-P1Y]`` in
every cycle point, when only a single instance of it exists, at the initial
cycle point:

.. code-block:: cylc

   [scheduling]
       initial cycle point = 2020
       [[graph]]
           R1 = foo
           # ERROR
           P1Y = foo[-P1Y] => bar

.. note::

   ``cylc graph`` will display un-satisfiable inter-cycle
   dependencies as "ghost nodes", as illustrated in this
   screenshot of cylc graph displaying the above example with the
   un-satisfiable task (foo) displayed as a "ghost node".

   .. _ghost-node-screenshot:

   .. figure:: ../../img/ghost-node-example.png
      :align: center

      Screenshot of ``cylc graph`` showing one task as a "ghost node".


Omitting Tasks At Runtime
-------------------------

It is sometimes convenient to omit certain tasks from the workflow at
runtime without actually deleting their definitions from the workflow.

Defining :cylc:conf:`[runtime]` properties for tasks that do not appear
in the workflow graph results in verbose-mode validation warnings that the
tasks are disabled. They cannot be used because the workflow graph is what
defines their dependencies and valid cycle points. Nevertheless, it is
legal to leave these orphaned runtime sections in the workflow
configuration because it allows you to temporarily remove tasks from
the workflow by commenting them out of the graph.

With Jinja2 (:ref:`User Guide Jinja2`) you can radically alter
workflow structure by including or excluding tasks from the
:cylc:conf:`[scheduling]` and :cylc:conf:`[runtime]` sections according to the
value of a single logical flag defined at the top of the workflow.


.. [1] An OR operator on the right doesn't make much sense: if "B or C"
       triggers off A, what exactly should Cylc do when A finishes?
.. [2] In NWP forecast analysis workflows parts of the observation
       processing and data assimilation subsystem will typically also
       depend on model background fields generated by the previous forecast.
