.. _728.optional_outputs:

Graph branching, optional outputs and suicide triggers
======================================================

Cylc 8 has a :ref:`new scheduling algorithm <728.scheduling_algorithm>` and
a new syntax for dealing with tasks that may not necessarily complete.
It handles :term:`graphs <graph>` in an event-driven manner which means
that a workflow can follow different paths in different eventualities (without
the need for suicide triggers). This is called :term:`graph branching`.

.. admonition:: Does This Change Affect Me?
   :class: tip

   This change affects you if you are upgrading a Cylc 7 workflow that
   contains graph branches that are not necessarily expected to complete
   at runtime. You might get a ``GraphParseError`` during validation with
   Cylc 8.

   Typically this will be the case if you are using
   :term:`suicide triggers <suicide trigger>` (marked by ``!`` before the
   task name in the graph, e.g. ``foo:fail => !foo``).

   You should *not* perform this upgrade if still in :ref:`cylc_7_compat_mode`
   (``suite.rc`` filename).


Required Changes
^^^^^^^^^^^^^^^^

Any :term:`task outputs <task output>` that are not necessarily expected to
complete must be marked as :term:`optional <optional output>` using ``?``.
Suicide triggers can then be removed.

Example
^^^^^^^

Here is an example Cylc 7 :term:`graph`:

.. code-block:: cylc-graph

   foo:fail => recover

   foo | recover => bar

   # Remove the "recover" task in the success case.
   foo => ! recover
   # Remove the "foo" task in the fail case.
   recover => ! foo

.. digraph:: Example
   :align: center

   subgraph cluster_1 {
      label = ":fail"
      color = "red"
      fontcolor = "red"
      style = "dashed"
      recover
   }

   foo -> recover
   recover -> bar [arrowhead="onormal"]
   foo -> bar [arrowhead="onormal" weight=2]

Validating this with Cylc 8 will give an error:

.. code-block:: console

   $ cylc validate .
   GraphParseError: Opposite outputs foo:succeeded and foo:failed must both be optional if both are used

In Cylc 8, all task outputs are :term:`required <required output>` to complete
unless otherwise indicated. However, it is impossible for both ``:succeed``
and ``:fail`` to occur when a task runs.

The solution is to mark the outputs which are :term:`optional <optional output>`
(in this case ``foo:succeed`` and ``foo:fail``) with a ``?`` in the graph.
Also, the suicide triggers can be removed.

.. code-block:: diff

   - foo:fail => recover
   + foo:fail? => recover

   - foo | recover => bar
   + foo? | recover => bar

   - # Remove the "recover" task in the success case.
   - foo => ! recover
   - # Remove the "foo" task in the fail case.
   - recover => ! foo

In Cylc 7, suicide triggers were used to remove tasks that did not complete
during runtime. Cylc 8's event-driven graph handling allows such graph
branching using optional output syntax, without the need for suicide triggers.
(Suicide triggers are still supported in Cylc 8; however, they are most
likely unnecessary.)

.. tip::

   Remember: ``foo?`` is short for ``foo:succeed?``. It is the *output*
   that is optional, not the task itself.

.. seealso::

   - :ref:`Expected <User Guide Expected Outputs>` and
     :ref:`optional <User Guide Optional outputs>` outputs in the user guide.

   - :ref:`Graph Branching` in the user guide.
