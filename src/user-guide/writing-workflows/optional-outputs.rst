
.. _User Guide Optional Outputs:

Expected & Optional Task Outputs
================================

Cylc 8 follows the graph wherever it leads, as events dictate at runtime. This
is powerful, but it is not necessarily helpful if tasks behave in ways not
anticipated by the graph.

For instance, the following graph says that task ``bar`` should trigger if
``foo`` succeeds:

.. code-block:: cylc

   [graph]
       R1 = "foo => bar"

If ``foo`` actually fails at runtime, however, and the graph does not recognize
that as a possible outcome, the scheduler should probably conclude that the
workflow did not run to completion as expected, rather than shutting down
just because the graph says there is nothing else to do.

It may not be sufficient just to highlight the failure of ``foo`` as a problem,
because sometimes task failure is expected, and other task outputs can also
lead to dead-end side branches of the graph.

So, to allow proper diagnosis of workflow completion, the scheduler *expects*
all task outputs to be completed at runtime, unless they  are explicitly marked
as *optional*.


Incomplete Tasks
----------------

Tasks that finish without completing expected outputs [1]_ are retained as
:term:`incomplete tasks <incomplete task>` pending user intervention (e.g. to
be retriggered after fixing the problem, to allow the workflow to continue).

.. note::
   Incomplete tasks count toward the :term:`runahead limit`.


Scheduler Stall
---------------

If there is nothing else to do, the scheduler will conclude that the workflow
has run to completion, and shut down, if there are no incomplete tasks present.

But if there are any incomplete tasks present, the scheduler will log a
:term:`stall` and stay alive for 1 hour (by default) to allow user intervention.

Restarting a stalled workflow will trigger a new stall timer.

.. note::
   
   Partially satisfied prerequisites can also cause a stall. If ``a & b => c``,
   but only ``a`` runs (perhaps something went wrong upstream of ``b``) the
   scheduler will take partial completion of ``c``'s prerequisites as a sign
   that the workflow did not run to completion as expected.

Examples
--------

Outputs are expected by default (and the tasks will be retained as incomplete
if they are not generated):

.. code-block:: cylc

   [graph]
       R1 = """
          foo  # foo:succeed expected
          bar:x  # bar:x expected
       """

Outputs can be flagged as optional with a question mark:

.. code-block:: cylc

   [graph]
       R1 = """
          foo?  # foo:succeed optional
          bar:x?  # bar:x optional
       """

.. warning::

   To avoid confusion, optional outputs must be marked as such wherever they
   appear in the graph.

Success and failure are mutually exclusive outputs, so they must both be
optional if they both appear in the graph:

.. code-block:: cylc

   [graph]
       R1 = """  # foo could succeed or fail
          foo? => bar
          foo:fail? => baz
       """

(This is an example of :ref:`path-branching`.)

Success is expected for tasks that only reference custom outputs in the graph:

.. code-block:: cylc

   [graph]
       R1 = "foo:x => bar"  # foo:x and foo:succeed expected

Leaf tasks (with nothing downstream of them) can have optional outputs. The
following workflow can complete successfully whether ``bar`` succeeds or fails:

.. code-block:: cylc

   [graph]
       R1 = "foo => bar?"

.. note::
   
   Optionality is an attribute of the upstream task output, not a triggering
   condition. The trigger ``foo? => bar`` says to *trigger ``bar`` if ``foo``
   succeeds*, and the ``?`` just tells the scheduler not to retain ``foo`` as
   an incomplete task if it fails.


Finish Triggers
---------------

Task ``:finish`` is really a pseudo output used as shorthand to triggger off
either of the real ``:succeed`` or ``:fail`` outputs. Consequently use of a
``foo:finish`` (say) implies that ``foo:succeed`` (or ``foo:fail``) must be
marked as optional if it occurs anywhere in the graph. And ``:finish?`` is
illegal syntax because is would incorreclty imply that "finishing is optional".

.. code-block:: cylc

   [graph]
       R1 = """
          foo:finish => bar
          foo? => baz  # must be optional!
       """


Family Triggers
---------------

.. (taken from https://github.com/cylc/cylc-flow/pull/4343#issuecomment-913901972)

Family triggers such as ``FAM:succeed-all`` and ``FAM:fail-any`` do not refer
to real "family outputs", they are short for logical combinations of member
task outputs.

As such, family triggers do not dictate the optionality of member outputs.
However, they are often used without separate reference to specific members in
the graph so they do imply a default optionality for member outputs:

- All family triggers imply (by default) that the corresponding member outputs
  are *expected*

  - Unless members are singled out as *optional* elsewhere in the graph
  - Except for family ``:finish-all,any`` triggers, which like
    task ``:finish`` triggers imply optional outputs
- The default can be changed by using ``?`` on the family trigger

Examples below are for a family ``A`` with member tasks ``a<i>``
for ``i = 1, 2, 3``; family ``B`` with members ``b<i>``; and so on.
Results are the same if ``-all`` is replaced by ``-any`` on all family triggers.

.. code-block:: cylc

   [graph]
       R1 = """
          A:succeed-all => x1  # a<i>:succeed expected
          B:succeed-all? => x2  # b<i>:succeed optional

          C:fail-all => x3  # c<i>:fail expected
          D:fail-all? => x4  # d<i>:fail optional

          E:succeed-all => x5  # e<i>:succeed expected ...
          e2? => z5            # ... but e2:succeed optional

          F:finish-all => x6  # f<i>:succeed optional
          F:finish-all? => x6  # ERROR (c.f. task:finish rules)
       """


.. _path-branching:

Alternate Path Branching
------------------------

The graph splits into concurrent branches whenever several tasks trigger off of a
single upstream parent:

.. code-block:: cylc

   [graph]
       R1 = "foo => bar & baz"
 
Perhaps more interestingly, however, a graph can split into alternate branches
on optional outputs, where only one branch or another will be followed at runtime.

This is often used for automatic failure recovery:

.. code-block:: cylc

   [graph]
       R1 = """
           foo:fail? => diagnose => foo-recover
           foo? | foo-recover => products
       """
           
.. note::
   It is not possible for a task to succeed and fail at the same time, so if
   both ouputs appear in the graph they must both be optional.

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



.. [1] This includes failed job submission, when the ``:submit`` output is not
   marked as optional.
