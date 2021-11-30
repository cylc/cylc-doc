.. _User Guide Optional Outputs:

Expected and Optional Outputs
=============================

:term:`Task outputs <task output>` in the :term:`graph` are either
:term:`expected <expected output>` (the default) or  :term:`optional <optional
output>`. This distinction supports :term:`graph branching` and it allows the
:term:`scheduler` to correctly diagnose :term:`workflow completion`. [1]_

.. _expected outputs:

Expected Outputs
----------------

The scheduler expects all task outputs to be completed at runtime, unless they are
marked with ``?`` as optional (:ref:`below <optional outputs>`). Tasks that
finish without completing expected outputs are retained as
:ref:`incomplete task <incomplete tasks>` pending user intervention.

This graph says task ``bar`` should trigger if ``foo`` succeeds:

.. code-block:: cylc-graph

   foo => bar  # short for "foo:succeed => bar"

Additionally, ``foo`` is expected to succeed, because its success is not marked
as optional. (And in fact ``bar`` is expected to succeed too).

Here, ``foo:succeed``, ``bar:x``, and ``baz:fail`` are all expected outputs:

.. code-block:: cylc-graph

   foo
   bar:x
   baz:fail

Tasks that appear with only custom outputs in the graph are also expected to succeed.
Here, ``foo:succeed`` is an expected output, as well as ``foo:x``, unless it is
marked as optional elsewhere in the graph:

.. code-block:: cylc-graph

   foo:x => bar

If a task generates multiple custom outputs, they should be "expected" if you
expect them all to be completed every time the task runs. Here,
``model:file1``, ``model:file2``, and ``model:file3`` are all expected outputs:

.. code-block:: cylc-graph

   model:file1 => proc1
   model:file2 => proc2
   model:file3 => proc3

.. _incomplete tasks:

Incomplete Tasks
^^^^^^^^^^^^^^^^

Tasks that finish without generating expected outputs [2]_ are flagged as
:term:`incomplete <incomplete task>`, even if they report success.

Incomplete tasks have behaved in a way not anticipated by the graph, which
often means the workflow cannot proceed to completion as expected. They are
retained by the scheduler pending user intervention, e.g. to be retriggered
after a bug fix, to allow the workflow to continue.

.. note::
   Incomplete tasks count toward the :term:`runahead limit`, because they may
   run again once dealt with.


.. _optional outputs:

Optional Outputs
----------------

Optional outputs are marked with ``?``. They may or may not be completed by the
task at runtime.

Like the first example above, the following graph also says task ``bar`` should
trigger if ``foo`` succeeds:

.. code-block:: cylc-graph

   foo? => bar  # short for "foo:succeed? => bar"

But now ``foo:succeed`` is optional, so we might expect it to fail sometimes.

Here, ``foo:succeed``, ``bar:x``, and ``baz:fail`` are all optional outputs:

.. code-block:: cylc-graph

   foo?
   bar:x?
   baz:fail?

.. warning::

   Optional outputs must be marked as optional everywhere they appear in the
   graph, to avoid ambiguity.


Success and failure (of the same task) are mutually exclusive, so they must
both be optional if one is optional, or if they both appear in the graph:

.. code-block:: cylc-graph

   foo? => bar
   foo:fail? => baz

If a task generates multiple custom outputs, they should all be declared optional
if you do not expect all of them all to be completed every time the task runs:

.. code-block:: cylc-graph

   # model:x, :y, and :z are all optional outputs:
   model:x? => proc-x
   model:y? => proc-y
   model:z? => proc-z

This is an example of :term:`graph branching` from optional outputs. Whether a
particular branch is taken or not depends on which optional outputs are
completed at runtime.

Leaf tasks (with nothing downstream of them) can have optional outputs. In the
following graph, ``foo`` is expected to succeed, but it doesn't matter whether
``bar`` succeeds or fails:

.. code-block:: cylc-graph

   foo => bar?


.. note::

   Optional outputs do not affect *triggering*. They just tell the scheduler
   what to do with the task if it finishes without completing the output.

   This graph triggers ``bar`` if ``foo`` succeeds, and does not trigger
   ``bar`` if ``foo`` fails:

   .. code-block:: cylc-graph

      foo => bar

   And so does this graph:

   .. code-block:: cylc-graph

      foo? => bar

   The only difference is whether or not the scheduler regards ``foo`` as
   incomplete if it fails.



Finish Triggers
---------------

``foo:finish`` is a pseudo output that is short for ``foo:succeed? |
foo:fail?``. This automatically labels the real outputs as optional, because
success and failure can't both be expected.

``foo:finish?`` is illegal because it incorrectly suggests that "finishing
is optional" and that a non-optional version of the trigger makes sense.

.. code-block:: cylc-graph

   # Good:
   R1 = """
      foo:finish => bar
      foo? => baz
   """

   # Error:
   R1 = """
      foo:finish => bar
      foo => baz  # ERROR : foo:succeed must be optional here!
   """

.. _graph-branching:

Graph Branching
---------------

A graph can split into alternate branches on optional outputs, where only one
branch or another will be followed at runtime.

This is often used for automatic failure recovery:

.. code-block:: cylc-graph

   foo => bar
   bar:fail? => recover
   bar? | recover => baz


.. digraph:: Example
   :align: center

   subgraph cluster_1 {
      label = ":fail"
      color = "red"
      fontcolor = "red"
      style = "dashed"

      recover
   }

   foo -> bar
   bar -> recover
   recover -> baz [arrowhead="onormal"]
   bar -> baz [arrowhead="onormal"]

Alternate paths can also branch from mutually exclusive custom outputs:

.. code-block:: cylc-graph

   # branch the graph depending on the outcome of "showdown"
   showdown:good? => good
   showdown:bad? => bad
   showdown:ugly? => ugly
   # join the graph back together
   good | bad | ugly => fin


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


Cylc can't know if custom outputs are mutually exclusive or not, however. If
they are not exclusive, the paths will be concurrent rather than alternate:

For branching on custom outputs you can use an :term:`artificial dependency` to
ensure that at least one branch executes. For the example above:

.. code-block:: cylc-graph

    start => showdown
    # branch the graph depending on the outcome of "showdown"
    showdown:good? => good
    showdown:bad? => bad
    showdown:ugly? => ugly
    # join the graph back together
    good | bad | ugly => fin
    # ensure at least one branch is run
    start => fin  # artificial dependency


Family Triggers
---------------

.. (taken from https://github.com/cylc/cylc-flow/pull/4343#issuecomment-913901972)

Family triggers are based on family pseudo outputs such as ``FAM:succeed-all``
and ``FAM:fail-any`` that are short for logical expressions involving the
corresponding member task outputs.

If the member outputs are not singled out explicitly elsewhere in the graph,
then they default to being expected outputs.

For example, if ``f1`` and ``f2`` are members of ``FAM``, then this:

.. code-block:: cylc-graph

   FAM:fail-all => a


means:

.. code-block:: cylc-graph

   f1:fail & f2:fail => a  # f1:fail and f2:fail are expected


and this:

.. code-block:: cylc-graph

   FAM:succeed-any => a


means:

.. code-block:: cylc-graph

   f1 | f2 => a  # f1:succeed and f2:succeed are expected


However, the family default can be changed to optional by using ``?`` on the
family trigger. So this:

.. code-block:: cylc-graph

   FAM:fail-all? => a


means this:

.. code-block:: cylc-graph

   f1:fail? & f2:fail? => a  # f1:fail and f2:fail are optional


If particular member tasks are singled out elsewhere in the graph, that
overrides the family default for expected/optional outputs:

.. code-block:: cylc-graph

   # f1:fail is expected, and f2:fail is optional:
   FAM:fail-all => a
   f2:fail? => b


Family Finish Triggers
----------------------

Like task ``:finish`` triggers, family ``:finish-all/any`` triggers are
different because ``:finish`` is a pseudo output involving both ``:succeed``
and ``:fail``, which are mutually exclusive outputs that must both be optional
if both are used.

Also like task ``:finish`` triggers, use of ``?`` is illegal on a family
finish trigger, because the underlying member outputs must already be optional.

.. code-block:: cylc-graph

   FAM:finish-all => a  # f1:succeed/fail and f2:succeed/fail are optional
   FAM:finish-any => a  # (ditto)

   FAM:finish-all? => b  # ERROR


.. note::
   Cylc 8 does not :term:`suicide triggers <suicide trigger>` to remove tasks
   from unused paths in the graph.


.. [1] By distinguishing graph branches that did not run but should have, from
   those that did not run but were optional.

.. [2] This includes failed job submission, when the ``:submit`` output is not
   marked as optional.
