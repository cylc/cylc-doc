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

   Often, we will want to repeat the same workflow multiple times. In Cylc this
   "repetition" is called :term:`cycling` and each repetition of the workflow is
   referred to as a :term:`cycle`.

   Each :term:`cycle` is given a unique label. This is called a
   :term:`cycle point`. For now these :term:`cycle points<cycle point>` will be
   integers *(they can also be dates and times as we will see in the next section)*.

To make a workflow repeat we must tell Cylc three things:

.. ifslides::

   * :term:`recurrence`
   * :term:`initial cycle point`
   * :term:`final cycle point` (Optional)

.. ifnotslides::

   The :term:`recurrence`
      How often we want the workflow to repeat.
   The :term:`initial cycle point`
      At what cycle point we want to start the workflow.
   The :term:`final cycle point`
      *Optionally* we can also tell Cylc what cycle point we want to stop the
      workflow.

.. nextslide::

.. ifnotslides::

   Let's take the bakery example from the previous section. Bread is
   produced in batches so the bakery will repeat this workflow for each
   batch of bread they bake. We can make this workflow repeat with the addition
   of three lines:

.. code-block:: diff

    [scheduling]
   +    cycling mode = integer
   +    initial cycle point = 1
        [[graph]]
   -        R1 = """
   +        P1 = """
                buy_ingredients => make_dough
                pre_heat_oven & make_dough => bake_bread => sell_bread & clean_oven
            """

.. nextslide::

.. ifnotslides::

   * The ``cycling mode = integer`` setting tells Cylc that we want our
     :term:`cycle points <cycle point>` to be numbered.
   * The ``initial cycle point = 1`` setting tells Cylc to start counting
     from 1.
   * ``P1`` is the :term:`recurrence`. The ``P1`` :term:`graph`
     will be repeated at each :term:`cycle point`.

   The first three :term:`cycles<cycle>` would look like this, with the entire
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

   Note the numbers under each task which represent the :term:`cycle point` each
   task is in.


Intercycle Dependencies
-----------------------

.. ifnotslides::

   We've just seen how to write a workflow that repeats every :term:`cycle`.

   Cylc runs tasks as soon as their dependencies are met so cycles are not
   necessarily run in order. This could cause problems, for instance we could
   find ourselves pre-heating the oven in one cycle whist we are still
   cleaning it in another.

   To resolve this we must add :term:`dependencies<dependency>` *between* the
   cycles. We do this by adding lines to the :term:`graph`. Tasks in the
   previous cycle can be referred to by suffixing their name with ``[-P1]``,
   for example. So to ensure the ``clean_oven`` task has been completed before
   the start of the ``pre_heat_oven`` task in the next cycle, we would write
   the following dependency:

   .. code-block:: cylc-graph

      clean_oven[-P1] => pre_heat_oven

   This dependency can be added to the workflow by adding it to the other graph
   lines:

.. code-block:: diff

    [scheduling]
        cycling mode = integer
        initial cycle point = 1
        [[graph]]
            P1 = """
                buy_ingredients => make_dough
                pre_heat_oven & make_dough => bake_bread => sell_bread & clean_oven
   +            clean_oven[-P1] => pre_heat_oven
            """

.. nextslide::

.. ifnotslides::

   The resulting workflow would look like this:

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

   Adding this dependency "strings together" the cycles, forcing them to run in
   order. We refer to dependencies between cycles as
   :term:`intercycle dependencies<intercycle dependency>`.

   In the dependency the ``[-P1]`` suffix tells Cylc that we are referring to a
   task in the previous cycle. Equally ``[-P2]`` would refer to a task two
   cycles ago.

   Note that the ``buy_ingredients`` task has no arrows pointing at it
   meaning that it has no dependencies. Consequently the ``buy_ingredients``
   tasks will all run straight away. This could cause our bakery to run into
   cash-flow problems as they would be purchasing ingredients well in advance
   of using them.

   To solve this, but still make sure that they never run out of
   ingredients, the bakery wants to purchase ingredients two batches ahead.
   This can be achieved by adding the following dependency:

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
                pre_heat_oven & make_dough => bake_bread => sell_bread & clean_oven
                clean_oven[-P1] => pre_heat_oven
   +            sell_bread[-P2] => buy_ingredients
            """

.. nextslide::

.. ifnotslides::

   This dependency means that the ``buy_ingredients`` task will run after
   the ``sell_bread`` task two cycles before.

.. note::

   The ``[-P2]`` suffix is used to reference a task two cycles before. For the
   first two cycles this doesn't make sense as there was no cycle two cycles
   before, so this dependency will be ignored.

   Any intercycle dependencies stretching back to before the
   :term:`initial cycle point` will be ignored.

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

   From initial cycle point:
      In the previous examples we made the workflow repeat by placing the graph
      in the ``P1`` setting. Here ``P1`` is a :term:`recurrence` meaning
      repeat every cycle, where ``P1`` means every cycle, ``P2`` means every
      *other* cycle, and so on. To build more complex workflows we can use
      multiple recurrences:

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

   After arbitrary cycle point:
      By default, recurrences start at the:
      :term:`initial cycle point`, however it is possible to make them start at
      an arbitrary cycle point. This is done by writing the cycle point and the
      recurrence separated by a forward slash (``/``), e.g. ``5/P3`` means
      repeat every third cycle starting *from* cycle number 5. Therefore, if
      you wanted a graph to occur every even cycle point you would use
      ``2/P2``.

   After offset from initial cycle point:
      The start point of a recurrence can also be defined as an offset from the
      :term:`initial cycle point`, e.g. ``+P5/P3`` means repeat every third cycle
      starting 5 cycles *after* the initial cycle point.

.. ifslides::

   ``2/P2``
      Repeat every even cycle (If your initial cycle point was odd)

   .. image:: ../../img/recurrence-sections2.svg
      :align: center

   ``+P5/P3``
      Repeat every third cycle starting 5 cycles *after* the initial cycle
      point.

   .. nextslide::

   .. rubric:: In this practical we will take the :term:`workflow <Cylc workflow>`
      we wrote in the previous section and turn it into a
      :term:`cycling workflow <cycling>`.

   Next section: :ref:`tutorial-datetime-cycling`

.. _basic cycling practical:

.. practical::

   .. rubric:: In this practical we will take the :term:`workflow <Cylc workflow>`
      we wrote in the previous section and turn it into a
      :term:`cycling workflow <cycling>`.

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

      In your ``~/cylc-src/`` directory create a new directory called
      ``integer-cycling`` and move into it:

      .. code-block:: bash

         mkdir -p ~/cylc-run/integer-cycling
         cd ~/cylc-run/integer-cycling

      Copy the above code into a :cylc:conf:`flow.cylc` file in that directory.

   #. **Make the workflow cycle.**

      Add in the following lines.

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

      Try visualising the workflow using ``cylc graph``.

      .. code-block:: none

         cylc graph .

      .. tip::

         You can get Cylc graph to draw dotted boxes around the cycles by
         adding the ``-c`` or ``--cycles`` switch to the cylc graph command:

         .. code-block:: none

            cylc graph -c .

      .. tip::

         By default ``cylc graph`` displays the first three cycles of a workflow.
         You can tell ``cylc graph`` to visualise the cycles between two points
         by providing them as arguments, for instance the following example
         would show all cycles between ``1`` and ``5`` (inclusive)::

            cylc graph . 1 5 &

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

      Next we need to add some intercycle dependencies. We are going to add
      three intercycle dependencies:

      #. Between ``f`` from the previous cycle and ``c``.
      #. Between ``d`` from the previous cycle and ``a``
         *every odd cycle* (e.g. 2/d => 3/a).
      #. Between ``e`` from the previous cycle and ``a``
         *every even cycle* (e.g. 1/e => 2/a).

      Have a go at adding intercycle dependencies to your :cylc:conf:`flow.cylc` file to
      make your workflow match the diagram below.

      .. hint::

         * ``P2`` means every odd cycle.
         * ``2/P2`` means every even cycle.

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
