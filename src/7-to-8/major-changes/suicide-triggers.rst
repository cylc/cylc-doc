.. _728.suicide_triggers:

Suicide Triggers
================

.. admonition:: Does This Change Affect Me?
   :class: tip

   Suicide triggers are written using an exclamation mark ``!`` like so:

   .. code-block:: cylc-graph

      task_1 => ! task_2

   Read this section if your workflows contain suicide triggers.

Overview
--------

In Cylc 7 :term:`suicide triggers <suicide trigger>` are used to remove
tasks from the graph automatically at runtime.

Cylc 8 handles :term:`graphs <graph>` in an event-driven manner which means
that a workflow can follow different paths in different eventualities without
the need for suicide triggers. This is called :term:`graph branching`.

.. seealso::

   :ref:`Graph Branching` in the user guide.


Changes
-------

No changes are required, suicide triggers are still supported in Cylc 8,
however, they are most likely unnecessary.


Example
-------

Here is an example Cylc 7 :term:`graph`:

.. code-block:: cylc-graph

   # The success case.
   foo => bar

   # The fail case.
   bar:fail => recover

   # Remove the "recover" task in the success case.
   bar => ! recover

   # Remove the "bar" task in the fail case.
   recover => ! bar

   # Downstream dependencies.
   bar | recover => baz

Which results in the following logic:

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

In Cylc 8 we mark the :term:`outputs <task output>` which are
:term:`optional <optional output>` (in this case ``bar:success`` and
``bar:fail``) with a ``?`` in the graph.

Cylc can then allow the graph to branch dynamically at runtime without the need
for suicide triggers.

.. code-block:: diff

     # The success case.
     foo => bar

     # The fail case.
   - bar:fail => recover
   + bar:fail? => recover

   - # Remove the "recover" task in the success case.
   - bar => ! recover

   - # Remove the "bar" task in the fail case.
   - recover => ! bar

     # Downstream dependencies.
   - bar | recover => baz
   + bar? | recover => baz

For more information see :ref:`Graph Branching` in the user guide.
