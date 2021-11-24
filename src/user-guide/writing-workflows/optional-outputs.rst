
.. _User Guide Optional Outputs:

Expected and Optional Outputs
=============================

Distinguishing between *expected* and  *optional* task outputs allow Cylc to
correctly diagnose workflow completion. [1]_

Expected Outputs
----------------

We expect all task outputs to be completed, unless they are marked with ``?``
as optional. If expected outputs do not get completed, the scheduler retains
the parent task as :ref:`incomplete <incomplete tasks>`.

This graph says task ``bar`` should trigger if ``foo`` succeeds:

.. code-block:: cylc

   [graph]
       R1 = "foo => bar"  # short for "foo:succeed => bar"

It also says the ``foo`` (and in fact ``bar`` too) is expected to succeed,
because its success is not marked as optional.

More examples:

.. code-block:: cylc

   [graph]
       R1 = """
          # foo:succeed, bar:x, and baz:fail are all expected outputs:
          foo
          bar:x
          baz:fail
       """

Success is also expected of tasks that appear with only custom outputs in the graph:

.. code-block:: cylc

   [graph]
       # both foo:x and foo:succeed are expected outputs:
       R1 = "foo:x => bar"


If a task generates multiple custom outputs, they should be "expected" if you
expect them all to be completed every time the task runs:

.. code-block:: cylc

   [graph]
       # model:file1, :file2, and :file3 are all expected outputs:
       R1 = """
           model:file1 => proc1
           model:file2 => proc2
           model:file3 => proc3
       """


Optional Outputs
----------------

Optional outputs, marked with ``?``, may or may not be completed as a task runs.
The scheduler doesn't care if optional outputs do not get completed.

Like the first example above, this graph also says task ``bar`` should trigger
if ``foo`` succeeds:

.. code-block:: cylc

   [graph]
       R1 = "foo? => bar"  # short for "foo:succeed? => bar"

But now ``foo:succeed`` is optional, so we might expect it to fail sometimes.

More examples:

.. code-block:: cylc

   [graph]
       R1 = """
          # foo:succeed, bar:x, and baz:fail are all optional outputs:
          foo?
          bar:x?
          baz:fail?
       """

.. warning::

   Optional outputs must be marked as optional everywhere they appear in the
   graph.


Success and failure (of the same task) are mutually exclusive, so they must
both be optional if one is optional, or if they both appear in the graph:

.. code-block:: cylc

   [graph]
       R1 = """
          foo? => bar
          foo:fail? => baz
       """

If a task generates multiple custom outputs, they should all be declared optional
if you do not expect all of them to be completed every time the task runs:

.. code-block:: cylc

   [graph]
       # model:x, :y, and :z are all optional outputs:
       R1 = """
           model:x => proc-x
           model:y => proc-y
           model:z => proc-z
       """

This is an example of :term:`graph branching` off of optional outputs. If the 3
outputs are mutually exclusive we should expect only one branch to run. If they
are not mutually exclusive but may not be generate every time the task runs, we
should not be surprised if one or more branches does not run. 

Leaf tasks (with nothing downstream of them) can have optional outputs. In the
following graph, ``foo`` is expected to succeed, but it doesn't matter whether
``bar`` succeeds or fails:

.. code-block:: cylc

   [graph]
       R1 = "foo => bar?"


.. _incomplete tasks:

Incomplete Tasks
----------------

Tasks that finish without generating expected outputs [2]_ are flagged as
:term:`incomplete <incomplete task>`, even if they report success.

Incomplete tasks have behaved in a way not anticipated by the graph, which
often means the workflow cannot proceed to completion as expected. They are
retained by the scheduler pending user intervention, e.g. to be retriggered
after a bug fix, to allow the workflow to continue.

.. note::
   Incomplete tasks count toward the :term:`runahead limit`, because they may
   run again once dealt with.


.. note::
   
   Whether an output is optional or not does not affect triggering at all. It
   just tells the scheduler what to do with the task if it finishes without
   completing the output.

   This graph triggers ``bar`` if ``foo`` succeeds, and does not trigger
   ``bar`` if ``foo`` fails:

   .. code-block:: cylc
      
      R1 = "foo => bar"
     
   And so does this graph:
     
   .. code-block:: cylc
      
      R1 = "foo? => bar"
 
   The only difference is whether or not the scheduler regards ``foo`` as
   incomplete if it fails.


Stall and Shutdown
------------------

If the graph says there is nothing more to do, and there are no incomplete
tasks present, the scheduler will report workflow completion and shut down.

If the graph says there is nothing more to do and there are incomplete tasks
present, the scheduler will :term:`stall` and stay alive for 1 hour (by
default) to await user intervention that may allow the workflow to continue.

Restarting a stalled workflow will trigger a new stall timer.

.. note::
   
   Partially satisfied prerequisites can also cause a stall. If ``a & b => c``,
   and ``a`` succeeds but ``b`` never even runs, the scheduler will take
   partial completion of ``c``'s prerequisites as a sign that the workflow did
   not run to completion as expected.


Finish Triggers
---------------

``foo:finish`` is a pseudo output that is short for ``foo:succeed? |
foo:fail?``. This automatically labels the real outputs as optional, because
success and failure can't both be expected.

``foo:finish?`` is illegal because it incorrectly suggests that "finishing
is optional" and that a non-optional version of the trigger makes sense.

.. code-block:: cylc

   [graph]
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


Family Triggers
---------------

.. (taken from https://github.com/cylc/cylc-flow/pull/4343#issuecomment-913901972)

Family triggers are based on family pseudo outputs such as ``FAM:succeed-all``
and ``FAM:fail-any`` that are short for logical expressions involving the
corresponding member task outputs.

If the member outputs are not singled out explicitly anywhere in the graph,
then they default to being expected outputs inside the family trigger.

For example, if ``f1`` and ``f2`` are members of ``FAM``: then

.. code-block:: cylc

   R1 = "FAM:fail-all => a"


means:

.. code-block:: cylc

   R1 = "f1:fail & f2:fail => a"  # f1:fail and f2:fail are expected


and 

.. code-block:: cylc

   R1 = "FAM:succeed-any => a"


means:

.. code-block:: cylc

   R1 = "f1 & f2 => a  # f1:succeed and f2:succeed are expected


However, the family default can be changed to optional with the ``?`` syntax:

.. code-block:: cylc

   R1 = "FAM:fail-all? => a"


means:

.. code-block:: cylc

   R1 = "f1:fail? & f2:fail? => a"  # f1:fail and f2:fail are optional

And you can override the family default for a particular member by singling it
out in the graph:

.. code-block:: cylc

   R1 = """
      # f1:fail is expected, and f2:fail is optional:
      FAM:fail-all => a
      f2:fail? => b
   """


Family Finish Triggers
----------------------

Like task ``:finish`` triggers, family ``:finish-all/any`` triggers are
different because ``:finish`` is a pseudo output involving both
``:succeed`` and ``:fail``, which are mutually exclusive outputs that must be
optional if both are used.

Also like task ``:finish`` triggers, use of ``?`` is illegal on a family
trigger, because the underlying member outputs must already be optional.

.. code-block:: cylc

   FAM:finish-all => a  # f1:succeed/fail and f2:succeed/fail are optional
   FAM:finish-any => a  # (ditto)

   FAM:finish-all? => b  # ERROR


.. _graph-branching:

Graph Branching
---------------

A graph can split into alternate branches on optional outputs, where only one
branch or another will be followed at runtime.

This is often used for automatic failure recovery:

.. code-block:: cylc

   [graph]
       R1 = """
           foo:fail? => diagnose => foo-recover
           foo? | foo-recover => products
       """
           

Alternate paths can also branch from mutually exclusive custom outputs:

.. code-block:: cylc

   [graph]
       R1 = """  # foo completes either file a or file b:
           foo:a? => proc-a  # only one branch will run
           foo:b? => proc-b
           proc-a | proc-b => products
       """

Unlike the success/fail case, however, Cylc can't know if custom outputs are
mutually exclusive or not. If they are not exclusive, the paths will be
concurrent rather than alternate:

.. code-block:: cylc

   [graph]
       R1 = """  # foo completes both file a and file b:
           foo:a => proc-a  # both branches will run
           foo:b => proc-b
           proc-a & proc-b => products
       """

For branching on custom outputs you can use an :term:`artificial dependency` to
ensure that at least one branch executes at runtime. For example, in the graph
below task ``a`` will spawn the post-branch ``c`` even if it doesn't complete
either of the branching outputs, in which case the partially satisfied ``c``
will be flagged by the scheduler as a problem.

.. code-block:: cylc

   [graph]
       R1 = """
           a:x? => b1
           a:y? => b2
           b1 | b2 => c
           a => c  # artifical dependency
       """

.. note::

   For Cylc 7 users, you do not need :term:`suicide triggers <suicide trigger>`
   to remove tasks from unused alternate paths in Cylc 8.


.. [1] By distinguishing graph branches (or rather, the tasks that trigger
   them) that did not run but should have, from those that did not run but were
   optional.

.. [2] This includes failed job submission, when the ``:submit`` output is not
   marked as optional.
