.. _graph-branching:

Graph Branching
===============

.. note::
   Unlike Cylc 7 and earlier, Cylc 8 does not need :term:`suicide triggers
   <suicide trigger>` to remove tasks from unused paths in the graph.


A graph can split into alternate branches on :term:`optional outputs <optional
output>`, where only one branch or another will be followed at runtime.

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
they are not exclusive, the paths will be concurrent rather than alternate.

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


