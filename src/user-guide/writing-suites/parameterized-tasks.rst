.. _User Guide Param:

Parameterized Tasks
===================

Cylc can automatically generate tasks and dependencies by expanding
:term:`parameterized <parameterisation>` task names over lists of parameter
values. Uses for this include:

- generating an ensemble of similar model runs
- generating chains of tasks to process similar datasets
- replicating an entire workflow, or part thereof, over several runs
- splitting a long model run into smaller steps or ``chunks``
  (parameterized cycling)

.. note::

   This can be done with Jinja2 loops too (:ref:`User Guide Jinja2`)
   but parameterization is much cleaner (nested loops can seriously reduce
   the clarity of a suite configuration).*


Parameter Expansion
-------------------

Parameter values can be lists of strings, or lists of integers and
integer ranges (with inclusive bounds). Numeric values in a list of strings are
considered strings. It is not possible to mix strings with integer ranges.

For example:

.. code-block:: cylc

   [[task parameters]]
       # parameters: "ship", "buoy", "plane"
       # default task suffixes: _ship, _buoy, _plane
       obs = ship, buoy, plane

       # parameters: 1, 2, 3, 4, 5
       # default task suffixes: _run1, _run2, _run3, _run4, _run5
       run = 1..5

       # parameters: 1, 3, 5, 7, 9
       # default task suffixes: _idx1, _idx3, _idx5, _idx7, _idx9
       idx = 1..9..2

       # parameters: -11, -1, 9
       # default task suffixes: _idx-11, _idx-01, _idx+09
       idx = -11..9..10

       # parameters: 1, 3, 5, 10, 11, 12, 13
       # default task suffixes: _i01, _i03, _i05, _i10, _i11, _i12, _i13
       i = 1..5..2, 10, 11..13

       # parameters: "0", "1", "e", "pi", "i"
       # default task suffixes: _0, _1, _e, _pi, _i
       item = 0, 1, e, pi, i

       # ERROR: mix strings with int range
       p = one, two, 3..5

Then angle brackets denote use of these parameters throughout the suite
configuration. For the values above, this parameterized name:

.. code-block:: sub

   model<run>  # for run = 1..5

expands to these concrete task names:

.. code-block:: none

   model_run1, model_run2, model_run3, model_run4, model_run5

and this parameterized name:

.. code-block:: sub

   proc<obs>  # for obs = ship, buoy, plane

expands to these concrete task names:

.. code-block:: none

   proc_ship, proc_buoy, proc_plane

By default, to avoid any ambiguity, the parameter name appears in the expanded
task names for integer values, but not for string values. For example,
``model_run1`` for ``run = 1``, but ``proc_ship`` for
``obs = ship``. However, the default expansion templates can be
overridden if need be:

.. code-block:: cylc

   [task parameters]
       obs = ship, buoy, plane
       run = 1..5
       [[templates]]
           run = -R%(run)s  # Make foo<run> expand to foo-R1 etc.

See :cylc:conf:`[task parameters][templates]` for more on the string
template syntax.

Any number of parameters can be used at once. This parameterization:

.. code-block:: sub

   model<run,obs>  # for run = 1..2 and obs = ship, buoy, plane

expands to these tasks names:

.. code-block:: none

   model_run1_ship, model_run1_buoy, model_run1_plane,
   model_run2_ship, model_run2_buoy, model_run2_plane

Here's a simple but complete example suite:

.. code-block:: cylc

   [task parameters]
           run = 1..2
   [scheduling]
       [[graph]]
           R1 = "prep => model<run>"
   [runtime]
       [[model<run>]]
           # ...

The result, post parameter expansion, is this:

.. code-block:: cylc

   [scheduling]
       [[graph]]
           R1 = "prep => model_run1 & model_run2"
   [runtime]
       [[model_run1]]
           # ...
       [[model_run2]]
           # ...

Here's a more complex graph using two parameters (:cylc:conf:`[runtime]`
omitted):

.. code-block:: cylc

   [task parameters]
           run = 1..2
           mem = cat, dog
   [scheduling]
       [[graph]]
           R1 = """
               prep => init<run> => model<run,mem> =>
               post<run,mem> => wrap<run> => done
           """

.. todo

   \.\.\. which expands to:

   [scheduling]
       [[graph]]
           R1 = """
               prep => init_run1 => model_run1_cat => post_run1_cat => wrap_run1 => done
                   init_run1 => model_run1_dog => post_run2_dog => wrap_run1
               prep => init_run2 => model_run2_cat => post_run2_cat => wrap_run2 => done
                   init_run2 => model_run2_dog => post_run2_dog => wrap_run2"""

The result as visualized by ``cylc graph`` is:

.. _fig-params-1:

.. figure:: ../../img/params1.png
   :align: center

   Parameter expansion example.


Zero-Padded Integer Values
^^^^^^^^^^^^^^^^^^^^^^^^^^

Integer parameter values are given a default template for generating task
suffixes that are zero-padded according to the longest size of their values.
For example, the default template for ``p = 9..10`` would be
``_p%(p)02d``, so that ``foo<p>`` would become ``foo_p09, foo_p10``.
If negative values are present in the parameter list, the
default template will include the sign.
For example, the default template for ``p = -1..1`` would be
``_p%(p)+02d``, so that ``foo<p>`` would become
``foo_p-1, foo_p+0, foo_p+1``.

To get thicker padding and/or alternate suffixes, use a template. E.g.:

.. code-block:: cylc

   [[task parameters]]
       i = 1..9
       p = 3..14
       [[templates]]
           i = _i%(i)02d  # suffixes = _i01, _i02, ..., _i09
           # A double-percent gives a literal percent character
           p = %%p%(p)03d  # suffixes = %p003, %p004, ..., %p013, %p014


Parameters as Full Task Names
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Parameter values can be used as full task names, but the default template
should be overridden to remove the initial underscore. For example:

.. code-block:: cylc

   [task parameters]
           i = 1..4
           obs = ship, buoy, plane
       [[parameter templates]]
           i = i%(i)d  # task name must begin with an alphabet
           obs = %(obs)s
   [scheduling]
       [[graph]]
           R1 = """
               foo => <i>  # foo => i1 & i2 & i3 & i4
               <obs> => bar  # ship & buoy & plane => bar
           """


Passing Parameter Values To Tasks
---------------------------------

Parameter values are passed as environment variables to tasks generated by
parameter expansion. For example, if we have:

.. code-block:: cylc

   [task parameters]
           obs = ship, buoy, plane
           run = 1..5
   [scheduling]
       [[graph]]
           R1 = model<run,obs>

Then task ``model_run2_ship`` would get the following standard
environment variables:

.. code-block:: bash

   # In a job script of an instance of the "model_run2_ship" task:
   export CYLC_TASK_PARAM_run="2"
   export CYLC_TASK_PARAM_obs="ship"

These variables allow tasks to determine which member of a parameterized
group they are, and so to vary their behaviour accordingly.

You can also define custom variables and string templates for parameter value
substitution. For example, if we add this to the above configuration:

.. code-block:: cylc

   [runtime]
       [[model<run,obs>]]
           [[[environment]]]
               MYNAME = %(obs)sy-mc%(obs)sface
               MYFILE = /path/to/run%(run)03d/%(obs)s

Then task ``model_run2_ship`` would get the following custom
environment variables:

.. code-block:: bash

   # In a job script of an instance of the "model_run2_ship" task:
   export MYNAME=shipy-mcshipface
   export MYFILE=/path/to/run002/ship


Selecting Specific Parameter Values
-----------------------------------

Specific parameter values can be singled out in the graph and under
:cylc:conf:`[runtime]` with the notation ``<p=5>`` (for example).
Here's how to make a special task trigger off just the first of a
set of model runs:

.. code-block:: cylc

   [task parameters]
           run = 1..5
   [scheduling]
       [[graph]]
           R1 = """
               model<run> => post_proc<run>  # general case
               model<run=1> => check_first_run  # special case
            """
   [runtime]
       [[model<run>]]
           # config for all "model" runs...
       [[model<run=1>]]
           # special config (if any) for the first model run...
       #...


Selecting Partial Parameter Ranges
----------------------------------

The parameter notation does not currently support partial range selection such
as ``foo<p=5..10>``, but you can achieve the same result by defining a
second parameter that covers the partial range and giving it the same expansion
template as the full-range parameter. For example:

.. code-block:: cylc

   [task parameters]
       run = 1..10  # 1, 2, ..., 10
       runx = 1..3  # 1, 2, 3
       [[parameter templates]]
           run = _R%(run)02d   # _R01, _R02, ..., _R10
           runx = _R%(runx)02d  # _R01, _R02, _R03
   [scheduling]
       [[graph]]
           R1 = """model<run> => post<run>
                   model<runx> => checkx<runx>"""
   [runtime]
       [[model<run>]]
           # ...
       #...


Parameter Offsets In The Graph
------------------------------

A negative offset notation ``<NAME-1>`` is interpreted as the previous
value in the ordered list of parameter values, while a positive offset is
interpreted as the next value. For example, to split a model run into multiple
steps with each step depending on the previous one, either of these graph lines:

.. code-block:: cylc-graph

   model<run-1> => model<run>  # for run = 1, 2, 3
   model<run> => model<run+1>  # for run = 1, 2, 3

expands to:

.. code-block:: cylc-graph

   model_run1 => model_run2
   model_run2 => model_run3

   # or equivalently:

   model_run1 => model_run2 => model_run3

And this graph:

.. code-block:: cylc-graph

   proc<size-1> => proc<size>  # for size = small, big, huge

expands to:

.. code-block:: cylc-graph

   proc_small => proc_big
   proc_big => proc_huge

   # or equivalently:

   proc_small => proc_big => proc_huge

However, a quirk in the current system means that you should avoid mixing
conditional logic in these statements. For example, the following will do the
unexpected:

.. code-block:: cylc-graph

   foo<m-1> & baz => foo<m>  # for m = cat, dog

currently expands to:

.. code-block:: cylc-graph

   foo_cat & baz => foo_dog

   # when users may expect it to be:
   #     foo_cat => foo_dog
   #     foo_cat & foo_dog

For the time being, writing out the logic explicitly will give you the correct
graph.

.. code-block:: cylc-graph

   foo<m-1> => foo<m>  # for m = cat, dog
   baz => foo<m>


Task Families And Parameterization
----------------------------------

Task family members can be generated by parameter expansion:

.. code-block:: cylc

   [runtime]
       [[FAM]]
       [[member<r>]]
           inherit = FAM
   # Result: family FAM contains member_r1, member_r2, etc.


Family names can be parameterized too, just like task names:

.. code-block:: cylc

   [runtime]
       [[RUN<r>]]
       [[model<r>]]
           inherit = RUN<r>
       [[post_proc<r>]]
           inherit = RUN<r>
   # Result: family RUN_r1 contains model_r1 and post_proc_r1,
   #         family RUN_r2 contains model_r2 and post_proc_r1, etc.

As described in :ref:`FamilyTriggers` family names can be used to
trigger all members at once:

.. code-block:: cylc-graph

   foo => FAMILY

or to trigger off all members:

.. code-block:: cylc-graph

   FAMILY:succeed-all => bar

or to trigger off any members:

.. code-block:: cylc-graph

   FAMILY:succeed-any => bar

If the members of ``FAMILY`` were generated with parameters, you can
also trigger them all at once with parameter notation:

.. code-block:: cylc-graph

   foo => member<m>

Similarly, to trigger off all members:

.. code-block:: cylc-graph

   member<m> => bar
   # (member<m>:fail etc., for other trigger types)

Family names are still needed in the graph, however, to succinctly express
"succeed-any" triggering semantics, and all-to-all or any-to-all triggering:

.. code-block:: cylc-graph

   FAM1:succeed-any => FAM2

(Direct all-to-all and any-to-all family triggering is not recommended for
efficiency reasons though - see :ref:`EfficientInterFamilyTriggering`).

For family *member-to-member* triggering use parameterized members.
For example, if family ``OBS_GET`` has members ``get<obs>`` and
family ``OBS_PROC`` has members ``proc<obs>`` then this graph:

.. code-block:: cylc-graph

   get<obs> => proc<obs>  # for obs = ship, buoy, plane

expands to:

.. code-block:: cylc-graph

   get_ship => proc_ship
   get_buoy => proc_buoy
   get_plane => proc_plane


.. _Parameterized Cycling:

Parameterized Cycling
---------------------

Two ways of constructing cycling systems are described and contrasted in
:ref:`Workflows For Cycling Systems`. For most purposes use of
a proper :term:`cycling` workflow is recommended, wherein Cylc incrementally
generates the date-time sequence and extends the workflow, potentially
indefinitely, at run time. For smaller systems of finite duration, however,
parameter expansion can be used to generate a sequence of pre-defined tasks
as a proxy for cycling.

Here's a cycling workflow of two-monthly model runs for one year,
with previous-instance model dependence (e.g. for model restart files):

.. code-block:: cylc

   [scheduling]
       initial cycle point = 2020-01
       final cycle point = 2020-12
       [[graph]]
           # Run once, at the initial point.
           R1 = "prep => model"
           # Run at 2-month intervals between the initial and final points.
           P2M = "model[-P2M] => model => post_proc & archive"
   [runtime]
       [[model]]
           script = "run-model $CYLC_TASK_CYCLE_POINT"

And here's how to do the same thing with parameterized tasks:

.. code-block:: cylc

   [task parameters]
           chunk = 1..6
   [scheduling]
       [[graph]]
           R1 = """
               prep => model<chunk=1>
               model<chunk-1> => model<chunk> =>
               post_proc<chunk> & archive<chunk>
            """
   [runtime]
       [[model<chunk>]]
           script = """
   # Compute start date from chunk index and interval, then run the model.
   INITIAL_POINT=2020-01
   INTERVAL_MONTHS=2
   OFFSET_MONTHS=(( (CYLC_TASK_PARAM_chunk - 1)*INTERVAL_MONTHS ))
   OFFSET=P${OFFSET_MONTHS}M  # e.g. P4M for chunk=3
   run-model $(cylc cyclepoint --offset=$OFFSET $INITIAL_POINT)"""

The two workflows are shown together below. They both achieve the same
result, and both can include special tasks at the start, end, or
anywhere in between. But as noted earlier the parameterized version has
several disadvantages: it must be finite in extent and not too large; the
date-time arithmetic has to be done by the user; and the full extent of the
workflow will be visible at all times as the suite runs.

.. todo
   Create sub-figures if possible: for now hacked as separate figures with
   link and caption on final displayed figure.

.. figure:: ../../img/eg2-static.png
   :align: center

.. _fig-eg2:

.. figure:: ../../img/eg2-dynamic.png
   :align: center

   Parameterized (top) and cycling (bottom) versions of the same
   workflow. The first three cycle points are shown in the
   cycling case. The parameterized case does not have "cycle points".

Here's a yearly-cycling suite with four parameterized chunks in each cycle
point:

.. code-block:: cylc

   [task parameters]
           chunk = 1..4
   [scheduling]
       initial cycle point = 2020-01
       [[graph]]
           P1Y = """
               model<chunk-1> => model<chunk>
               model<chunk=4>[-P1Y] => model<chunk=1>
           """

.. note::

   The inter-cycle trigger connects the first chunk in each cycle point
   to the last chunk in the previous cycle point. Of course it would be simpler
   to just use 3-monthly cycling:

   .. code-block:: cylc

      [scheduling]
          initial cycle point = 2020-01
          [[graph]]
              P3M = "model[-P3M] => model"

Here's a possible valid use-case for mixed cycling: consider a portable
date-time cycling workflow of model jobs that can each take too long to run on
some supported platforms. This could be handled without changing the cycling
structure of the suite by splitting the run (at each cycle point) into a
variable number of shorter steps, using more steps on less powerful hosts.


Cycle Point And Parameter Offsets At Start-Up
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

In cycling workflows cylc ignores anything earlier than the suite initial
cycle point. So this graph:

.. code-block:: cylc

   P1D = "model[-P1D] => model"

simplifies at the initial cycle point to this:

.. code-block:: cylc

   P1D = "model"

Similarly, parameter offsets are ignored if they extend beyond the start
of the parameter value list. So this graph:

.. code-block:: cylc

   R1 = "model<chunk-1> => model<chunk>"

simplifies for ``chunk=1`` to this:

.. code-block:: cylc

   R1 = "model_chunk1"

.. note::

   The initial cut-off applies to every parameter list, but only
   to cycle point sequences that start at the suite initial cycle point.
   Therefore it may be somewhat easier to use parameterized cycling if you
   need multiple date-time sequences *with different start points* in the
   same suite. We plan to allow this sequence-start simplification for any
   date-time sequence in the future, not just at the suite initial point,
   but it needs to be optional because delayed-start cycling tasks
   sometimes need to trigger off earlier cycling tasks.
