.. _tutorial-integer-cycling:

Basic Cycling
=============

.. admonition:: Aims
   :class: aims

   | You will be able to:
   | ✅ Write simple :term:`cycling` (repeating) workflows.


Repeating Workflows
-------------------

.. ifnotslides::

   You may want to repeat the same workflow multiple times. In Cylc this
   is called :term:`cycling`, and each repetition is called a :term:`cycle`.

   Each :term:`cycle` is given a unique label, called a
   :term:`cycle point`. For now these will be integers, but *they can also be
   datetimes* as we will see in the next section.

To make a workflow repeat we must tell Cylc three things:

.. ifslides::

   * :term:`recurrence`
   * :term:`initial cycle point`
   * :term:`final cycle point` (Optional)

.. ifnotslides::

   The :term:`recurrence`.
      How often to repeat the workflow (or part of it).
   The :term:`initial cycle point`.
      The cycle point to start from.
   The :term:`final cycle point` (optional).
      We can also tell Cylc where to stop the workflow.

.. nextslide::

.. ifnotslides::

   Let's take the bakery example from the previous section. Bread is
   baked in batches so the bakery will repeat this workflow for each
   batch. We can make the workflow repeat by adding three lines:

.. code-block:: diff

    [scheduling]
   +    cycling mode = integer
   +    initial cycle point = 1
        [[graph]]
   -        R1 = """
   +        P1 = """
                buy_ingredients => make_dough
                pre_heat_oven & make_dough => bake_bread
                bake_bread => sell_bread & clean_oven
            """

.. nextslide::

.. ifnotslides::

   * ``cycling mode = integer`` tells Cylc to give our :term:`cycle points
     <cycle point>` integer labels.
   * ``initial cycle point = 1`` tells Cylc to start counting cycle points
     from 1.
   * ``P1`` is the :term:`recurrence`; a ``P1`` :term:`graph string`
     repeats at every integer :term:`cycle point`.

   The first three :term:`cycles<cycle>` look like this, with the entire
   workflow repeated at each cycle point:

.. digraph:: example
   :align: center

   size = "7,15"

   subgraph cluster_1 {
       label = 1
       style = dashed
       "1/pur" [label="buy_ingredients\n1"]
       "1/mak" [label="make_dough\n1"]
       "1/bak" [label="bake_bread\n1"]
       "1/sel" [label="sell_bread\n1"]
       "1/cle" [label="clean_oven\n1"]
       "1/pre" [label="pre_heat_oven\n1"]
   }

   subgraph cluster_2 {
       label = 2
       style = dashed
       "2/pur" [label="buy_ingredients\n2"]
       "2/mak" [label="make_dough\n2"]
       "2/bak" [label="bake_bread\n2"]
       "2/sel" [label="sell_bread\n2"]
       "2/cle" [label="clean_oven\n2"]
       "2/pre" [label="pre_heat_oven\n2"]
   }

   subgraph cluster_3 {
       label = 3
       style = dashed
       "3/pur" [label="buy_ingredients\n3"]
       "3/mak" [label="make_dough\n3"]
       "3/bak" [label="bake_bread\n3"]
       "3/sel" [label="sell_bread\n3"]
       "3/cle" [label="clean_oven\n3"]
       "3/pre" [label="pre_heat_oven\n3"]
   }

   "1/pur" -> "1/mak" -> "1/bak" -> "1/sel"
   "1/pre" -> "1/bak" -> "1/cle"
   "2/pur" -> "2/mak" -> "2/bak" -> "2/sel"
   "2/pre" -> "2/bak" -> "2/cle"
   "3/pur" -> "3/mak" -> "3/bak" -> "3/sel"
   "3/pre" -> "3/bak" -> "3/cle"

.. ifnotslides::

   The number under each task shows which :term:`cycle point` it belongs to.


Intercycle Dependencies
-----------------------

.. ifnotslides::

   We've just seen how to write a workflow that repeats every :term:`cycle`.

   Cylc runs tasks as soon as their dependencies are met, regardless of cycle
   point, so cycles will not necessarily run in order. This can be efficient,
   but it could also cause problems. For instance we could find ourselves
   pre-heating the oven in one cycle while still cleaning it in another.

   To resolve this we can add :term:`dependencies<dependency>` *between*
   cycles, to the graph. To ensure that ``clean_oven`` completes before
   ``pre_heat_oven`` starts in the next cycle, we can write this:

   .. code-block:: cylc-graph

      clean_oven[-P1] => pre_heat_oven

   In a ``P1`` recurrence, the suffix ``[-P1]`` means *the previous cycle point*,
   Similarly, ``[-P2]`` refers back two cycles. The new dependency can be added
   to the workflow graph like this:

.. code-block:: diff

    [scheduling]
        cycling mode = integer
        initial cycle point = 1
        [[graph]]
            P1 = """
                buy_ingredients => make_dough
                pre_heat_oven & make_dough => bake_bread
                bake_bread => sell_bread & clean_oven
   +            clean_oven[-P1] => pre_heat_oven
            """

.. nextslide::

.. ifnotslides::

   And the resulting workflow looks like this:

.. digraph:: example
   :align: center

   size = "7,15"

   subgraph cluster_1 {
       label = 1
       style = dashed
       "1/pur" [label="buy_ingredients\n1"]
       "1/mak" [label="make_dough\n1"]
       "1/bak" [label="bake_bread\n1"]
       "1/sel" [label="sell_bread\n1"]
       "1/cle" [label="clean_oven\n1"]
       "1/pre" [label="pre_heat_oven\n1"]
   }

   subgraph cluster_2 {
       label = 2
       style = dashed
       "2/pur" [label="buy_ingredients\n2"]
       "2/mak" [label="make_dough\n2"]
       "2/bak" [label="bake_bread\n2"]
       "2/sel" [label="sell_bread\n2"]
       "2/cle" [label="clean_oven\n2"]
       "2/pre" [label="pre_heat_oven\n2"]
   }

   subgraph cluster_3 {
       label = 3
       style = dashed
       "3/pur" [label="buy_ingredients\n3"]
       "3/mak" [label="make_dough\n3"]
       "3/bak" [label="bake_bread\n3"]
       "3/sel" [label="sell_bread\n3"]
       "3/cle" [label="clean_oven\n3"]
       "3/pre" [label="pre_heat_oven\n3"]
   }

   "1/pur" -> "1/mak" -> "1/bak" -> "1/sel"
   "1/pre" -> "1/bak" -> "1/cle"
   "1/cle" -> "2/pre"
   "2/pur" -> "2/mak" -> "2/bak" -> "2/sel"
   "2/pre" -> "2/bak" -> "2/cle"
   "2/cle" -> "3/pre"
   "3/pur" -> "3/mak" -> "3/bak" -> "3/sel"
   "3/pre" -> "3/bak" -> "3/cle"

.. nextslide::

.. ifnotslides::

   The :term:`intercycle dependency` forces the connected tasks, in
   different cycle points, to run in order.

   Note that the ``buy_ingredients`` task has no arrows pointing at it.
   This means it has no *parent tasks* to wait on, upstream in the graph.
   Consequently all ``buy_ingredients`` tasks (out to a configurable
   :term:`runahead limit`) want to run straight away.
   This could cause our bakery to run into cash-flow problems by purchasing
   ingredients too far in advance of using them.

   To solve this problem without running out of ingredients, the bakery wants
   to purchase ingredients two batches ahead. This can be achieved by adding
   the following dependency:

.. ifslides::

   We need ``buy_ingredients`` to be dependent on ``sell_bread`` from
   two cycles before.

.. nextslide::

.. code-block:: diff

    [scheduling]
        cycling mode = integer
        initial cycle point = 1
        [[graph]]
            P1 = """
                buy_ingredients => make_dough
                pre_heat_oven & make_dough => bake_bread
                bake_bread => sell_bread & clean_oven
                clean_oven[-P1] => pre_heat_oven
   +            sell_bread[-P2] => buy_ingredients
            """

.. nextslide::

.. ifnotslides::

   This means that ``buy_ingredients`` will run after the ``sell_bread`` task
   two cycles earlier.

.. note::

   The ``[-P2]`` suffix references a task two cycles back. For the first two
   cycles this doesn't make sense, so those dependencies (and indeed any before
   the initial cycle point) will be ignored.

.. digraph:: example
   :align: center

   size = "4.5,15"

   subgraph cluster_1 {
       label = 1
       style = dashed
       "1/pur" [label="buy_ingredients\n1"]
       "1/mak" [label="make_dough\n1"]
       "1/bak" [label="bake_bread\n1"]
       "1/sel" [label="sell_bread\n1"]
       "1/cle" [label="clean_oven\n1"]
       "1/pre" [label="pre_heat_oven\n1"]
   }

   subgraph cluster_2 {
       label = 2
       style = dashed
       "2/pur" [label="buy_ingredients\n2"]
       "2/mak" [label="make_dough\n2"]
       "2/bak" [label="bake_bread\n2"]
       "2/sel" [label="sell_bread\n2"]
       "2/cle" [label="clean_oven\n2"]
       "2/pre" [label="pre_heat_oven\n2"]
   }

   subgraph cluster_3 {
       label = 3
       style = dashed
       "3/pur" [label="buy_ingredients\n3"]
       "3/mak" [label="make_dough\n3"]
       "3/bak" [label="bake_bread\n3"]
       "3/sel" [label="sell_bread\n3"]
       "3/cle" [label="clean_oven\n3"]
       "3/pre" [label="pre_heat_oven\n3"]
   }

   subgraph cluster_4 {
       label = 4
       style = dashed
       "4/pur" [label="buy_ingredients\n4"]
       "4/mak" [label="make_dough\n4"]
       "4/bak" [label="bake_bread\n4"]
       "4/sel" [label="sell_bread\n4"]
       "4/cle" [label="clean_oven\n4"]
       "4/pre" [label="pre_heat_oven\n4"]
   }

   "1/pur" -> "1/mak" -> "1/bak" -> "1/sel"
   "1/pre" -> "1/bak" -> "1/cle"
   "1/cle" -> "2/pre"
   "1/sel" -> "3/pur"
   "2/pur" -> "2/mak" -> "2/bak" -> "2/sel"
   "2/pre" -> "2/bak" -> "2/cle"
   "2/cle" -> "3/pre"
   "2/sel" -> "4/pur"
   "3/pur" -> "3/mak" -> "3/bak" -> "3/sel"
   "3/pre" -> "3/bak" -> "3/cle"
   "3/cle" -> "4/pre"
   "4/pur" -> "4/mak" -> "4/bak" -> "4/sel"
   "4/pre" -> "4/bak" -> "4/cle"


Recurrence Sections
-------------------

.. ifnotslides::

      In the previous examples we used a
      ``P1``:term:`recurrence` to make the workflow repeat at successive integer
      cycle points. Similarly ``P2`` means repeat every *other* cycle, and so
      on. We can use multiple recurrences to build more complex workflows:

      .. code-block:: cylc

         [scheduling]
            cycling mode = integer
            initial cycle point = 1
            [[graph]]
               # Repeat every cycle.
               P1 = foo
               # Repeat every second cycle.
               P2 = bar
               # Repeat every third cycle.
               P3 = baz

      .. image:: ../../img/recurrence-sections.svg
         :align: center

.. ifslides::

   .. code-block:: cylc

      [scheduling]
         cycling mode = integer
         initial cycle point = 1
         [[graph]]
            # Repeat every cycle.
            P1 = foo
            # Repeat every second cycle.
            P2 = bar
            # Repeat every third cycle.
            P3 = baz

   .. image:: ../../img/recurrence-sections.svg
      :align: center

.. nextslide::

.. ifnotslides::

   We can also tell Cylc where to start a recurrence sequence.

   From the initial cycle point:
      By default, recurrences start at the: :term:`initial cycle point`.

   From an arbitrary cycle point:
      We can give a different start point like this:
      ``5/P3`` means repeat every third cycle, starting from cycle number 5.
      To run a graph at every other cycle point, use ``2/P2``.

   Offset from the initial cycle point:
      The start point of a recurrence can also be defined as an offset from the
      :term:`initial cycle point` For example, ``+P5/P3`` means repeat every
      third cycle from 5 cycles *after* the initial cycle point.

.. ifslides::

   ``2/P2``
      Repeat every even cycle (Even if your initial cycle point was odd)

   .. image:: ../../img/recurrence-sections2.svg
      :align: center

   ``+P5/P3``
      Repeat every third cycle starting 5 cycles *after* the initial cycle
      point.

   .. nextslide::

   .. rubric:: In this practical we will turn the :term:`workflow <workflow>`
      of the previous section into a :term:`cycling workflow <cycling>`.

   Next section: :ref:`tutorial-datetime-cycling`

.. _basic cycling practical:

.. practical::

   .. rubric:: In this practical we will turn the :term:`workflow <workflow>`
      of the previous section into a :term:`cycling workflow <cycling>`.

   If you have not completed the previous practical use the following code for
   your :cylc:conf:`flow.cylc` file.

   .. code-block:: cylc

      [scheduler]
          allow implicit tasks = True
      [scheduling]
          [[graph]]
              R1 = """
                  a & c => b => d & f
                  d => e
              """

   #. **Create a new workflow.**

      Create a new source directory ``integer-cycling`` under ``~/cylc-src/``,
      and move into it:

      .. code-block:: bash

         mkdir -p ~/cylc-src/integer-cycling
         cd ~/cylc-src/integer-cycling

      Copy the above code into a :cylc:conf:`flow.cylc` file in that directory.

   #. **Make the workflow cycle.**

      Add the following lines to your ``flow.cylc`` file:

      .. code-block:: diff

          [scheduling]
         +    cycling mode = integer
         +    initial cycle point = 1
              [[graph]]
         -        R1 = """
         +        P1 = """
                      a & c => b => d & f
                      d => e
                  """

   #. **Visualise the workflow.**

      Try visualising your workflow using ``cylc graph``.

      .. code-block:: none

         cylc graph .

      .. tip::

         You can use the ``-c`` (``--cycles``) option
         to draw a box around each cycle:


         .. code-block:: none

            cylc graph -c .

      .. tip::

         By default ``cylc graph`` displays the first three cycles of the graph,
         but you can specify the range of cycles on the command line.
         Here's how to display cycles ``1`` through ``5``:

         .. code-block:: none

            cylc graph . 1 5

   #. **Add another recurrence.**

      Suppose we wanted the ``e`` task to run every *other* cycle
      as opposed to every cycle. We can do this by adding another
      recurrence.

      Make the following changes to your :cylc:conf:`flow.cylc` file.

      .. code-block:: diff

          [scheduling]
              cycling mode = integer
              initial cycle point = 1
              [[graph]]
                  P1 = """
                      a & c => b => d & f
         -            d => e
                  """
         +        P2 = """
         +            d => e
         +        """

      Use ``cylc graph`` to see the effect this has on the workflow.

   #. **intercycle dependencies.**

      Now we will add
      three intercycle dependencies:

      #. Between ``f`` from the previous cycle and ``c``.
      #. Between ``d`` from the previous cycle and ``a``
         *every odd cycle* (e.g. 2/d => 3/a).
      #. Between ``e`` from the previous cycle and ``a``
         *every even cycle* (e.g. 1/e => 2/a).

      Try adding these to your :cylc:conf:`flow.cylc` file to
      make your workflow match the diagram below.

      .. hint::

         * ``P2`` means every other cycle, from the initial cycle point.
         * ``2/P2`` means every other cycle, from cycle point 2.

      .. digraph:: example
        :align: center

         size = "4.5,7"

         subgraph cluster_1 {
             label = 1
             style = dashed
             "1/a" [label="a\n1"]
             "1/b" [label="b\n1"]
             "1/d" [label="d\n1"]
             "1/f" [label="f\n1"]
             "1/c" [label="c\n1"]
             "1/e" [label="e\n1"]
         }

         subgraph cluster_2 {
             label = 2
             style = dashed
             "2/a" [label="a\n2"]
             "2/b" [label="b\n2"]
             "2/d" [label="d\n2"]
             "2/f" [label="f\n2"]
             "2/c" [label="c\n2"]
         }

         subgraph cluster_3 {
             label = 3
             style = dashed
             "3/a" [label="a\n3"]
             "3/b" [label="b\n3"]
             "3/d" [label="d\n3"]
             "3/f" [label="f\n3"]
             "3/c" [label="c\n3"]
             "3/e" [label="e\n3"]
         }

         "1/a" -> "1/b" -> "1/f"
         "1/b" -> "1/d"
         "1/c" -> "1/b"
         "2/a" -> "2/b" -> "2/f"
         "2/b" -> "2/d"
         "2/c" -> "2/b"
         "3/a" -> "3/b" -> "3/f"
         "3/b" -> "3/d"
         "3/c" -> "3/b"
         "1/d" -> "1/e" -> "2/a"
         "3/d" -> "3/e"
         "2/d" -> "3/a"
         "1/f" -> "2/c"
         "2/f" -> "3/c"

      .. spoiler:: Solution warning

         .. code-block:: cylc

            [scheduler]
                allow implicit tasks = True
            [scheduling]
                cycling mode = integer
                initial cycle point = 1
                [[graph]]
                    P1 = """
                        a & c => b => d & f
                        f[-P1] => c  # (1)
                    """
                    P2 = """
                        d => e
                        d[-P1] => a  # (2)
                    """
                    2/P2 = """
                        e[-P1] => a  # (3)
                    """
