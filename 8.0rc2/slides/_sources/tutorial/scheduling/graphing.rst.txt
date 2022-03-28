.. _Cylc file format:

The :cylc:conf:`flow.cylc` File Format
======================================

.. admonition:: Aims
   :class: aims

   | You will be able to:
   | ✅ Recognise the ``flow.cylc`` file format.
   | ✅ Write simple chains of dependencies.


.. ifnotslides::

   A :term:`Cylc workflow` is defined by a :cylc:conf:`flow.cylc` configuration
   file, which uses a nested `INI`_ format:

.. ifslides::

   * A Cylc workflow is defined by a :cylc:conf:`flow.cylc` file
   * It is written in a nested `INI`_-based format

.. ifnotslides::

   * Comments start with a ``#`` character.
   * Settings are written as ``key = value`` pairs.
   * Settings can be contained within sections.
   * Sections are written inside square brackets i.e. ``[section-name]``.
   * Sections can be nested, by adding an extra square bracket with each level,
     so a sub-section would be written ``[[sub-section]]``, a sub-sub-section
     ``[[[sub-sub-section]]]``, and so on.

   .. note::

      Prior to Cylc 8, :cylc:conf:`flow.cylc` was named ``suite.rc``,
      but that name is now deprecated.

      See :ref:`cylc_7_compat_mode` for information compatibility with
      existing Cylc 7 ``suite.rc`` files.

Example
^^^^^^^

.. code-block:: cylc

   # Comment
   [section]
       key = value
       [[sub-section]]
           another-key = another-value  # Inline comment
           yet-another-key = """
               A
               Multi-line
               String
           """

Shorthand
^^^^^^^^^

Throughout this tutorial we will refer to configuration settings in the following ways:

``[section]``
   An entire section.
``[section]key``
   A specific config item, within a section.
``[section]key=value``
   The value of a specific config time, within a section.
``[section][sub-section]another-key``
   Note we only use one set of square brackets per section heading when
   writing on one line like this. In the config file each nested level
   gets another set of square brackets.

Duplicate Items
^^^^^^^^^^^^^^^

Duplicate sections get merged:

.. list-table::
   :class: grid-table

   * -
      .. code-block:: cylc
         :caption: input

         [a]
            c = C
         [b]
            d = D
         [a]  # duplicate
            e = E

     -
      .. code-block:: cylc
         :caption: result

         [a]
            c = C
            e = E
         [b]
            d = D

.. nextslide::

Duplicate settings get overwritten:

.. list-table::
   :class: grid-table

   * -
      .. code-block:: cylc
         :caption: input

         a = foo
         a = bar  # duplicate

     -
      .. code-block:: cylc
         :caption: result

         a = bar

Except for duplicate graph string items, which get merged:

.. list-table::
   :class: grid-table

   * -
      .. code-block:: cylc
         :caption: input

         R1 = "foo => bar"
         R1 = "foo => baz"

     -
      .. code-block:: cylc
         :caption: result

         R1 = "foo => bar & baz"


Indentation
^^^^^^^^^^^

It is a good idea to indent :cylc:conf:`flow.cylc` files for readability.

However, Cylc ignores indentation, so the following examples are equivalent:

.. list-table::
   :class: grid-table

   * -
       .. code-block:: cylc
          :caption: input

          [section]
              a = A
              [[sub-section]]
                  b = B
              b = C
              # this setting is still
              # in [[sub-section]]


     -
       .. code-block:: cylc
          :caption: result

          [section]
              a = A
              [[sub-section]]
                  b = C


.. _tutorial-cylc-graphing:


The Dependency Graph
^^^^^^^^^^^^^^^^^^^^

Graph Strings
-------------

Cylc workflows are defined in terms of :term:`tasks <task>` and
:term:`dependencies <dependency>`.

.. ifnotslides::

   Task have names, and dependencies are represented by arrows
   (``=>``) between them. For example, here's a task ``make_dough`` that should
   run after another task ``buy_ingredients`` has succeeded:

.. minicylc::
   :align: center
   :snippet:
   :theme: demo

   buy_ingredients => make_dough

.. nextslide::

.. ifnotslides::

   These :term:`dependencies <dependency>` can be chained together in
   :term:`graph strings<graph string>`:

.. minicylc::
   :align: center
   :snippet:
   :theme: demo

   buy_ingredients => make_dough => bake_bread => sell_bread

.. nextslide::

.. ifnotslides::

   Graph strings can be combined to form more complex graphs:

.. minicylc::
   :align: center
   :snippet:
   :theme: demo

   buy_ingredients => make_dough => bake_bread => sell_bread
   pre_heat_oven => bake_bread
   bake_bread => clean_oven

.. nextslide::

.. ifnotslides::

   Graphs can also contain logical operators ``&`` (*and*) and ``|`` (*or*).
   For example, the following lines are equivalent to those just above:

.. code-block:: cylc-graph

   buy_ingredients => make_dough
   pre_heat_oven & make_dough => bake_bread => sell_bread & clean_oven


.. nextslide::

Collectively, all the graph strings make up the workflow dependency :term:`graph`.

.. admonition:: Note
   :class: tip

   .. ifnotslides::

      The order of lines in the graph doesn't matter, so
      the following examples are equivalent:

      .. list-table::
         :class: grid-table

         * -
            .. code-block:: cylc-graph

               foo => bar
               bar => baz

           -
            .. code-block:: cylc-graph

               bar => baz
               foo => bar


Cylc Graphs
-----------

.. ifnotslides::

   A *non-cycling* :term:`graph` can be defined with ``[scheduling][graph]R1``,
   where ``R1`` means *run once*:

.. code-block:: cylc

   [scheduling]
       [[graph]]
           R1 = """
               buy_ingredients => make_dough
               pre_heat_oven & make_dough => bake_bread
               bake_bread => sell_bread & clean_oven
           """

.. nextslide::

.. ifnotslides::

   This is a minimal :term:`Cylc workflow` that defines a :term:`graph` of
   tasks to run, but does not yet say what scripts or applications to run
   for each task. We will cover that later in the :ref:`runtime tutorial
   <tutorial-runtime>`.

   Cylc provides a command line utility
   for visualising :term:`graphs <graph>`, ``cylc graph <path>``, where
   ``path`` is the location of the :cylc:conf:`flow.cylc` file.
   It generates diagrams similar to the ones you have seen so far. The number
   ``1`` below each task is the :term:`cycle point`. We will explain what this
   means in the next section.

.. image:: ../img/cylc-graph.png
   :align: center

.. nextslide::

.. hint::

   .. ifnotslides::

      A graph can be drawn in multiple ways, for instance the following two
      examples are equivalent:

   .. ifslides::

      A graph can be drawn in multiple ways:

   .. image:: ../img/cylc-graph-reversible.svg
      :align: center

   .. ifnotslides::

      Graphs drawn by ``cylc graph`` may vary slightly from one run to
      another, but the tasks and dependencies will always be the same.

.. nextslide::

.. ifslides::

   .. rubric:: In this practical we will create a new Cylc workflow and write a
      graph of tasks for it to run.

   Next session: :ref:`tutorial-integer-cycling`

.. practical::

   .. rubric:: In this practical we will create a new Cylc workflow and write a
      graph of tasks for it to run.

   #. **Create a Cylc workflow.**

      A :term:`Cylc workflow` is defined by a :cylc:conf:`flow.cylc` file.

      If you don't have one already, create a ``cylc-src`` directory in your
      user space:

      .. code-block::

         mkdir ~/cylc-src

      Now create a new workflow :term:`source directory` called
      ``graph-introduction`` under ``cylc-src`` and move into it:

      .. code-block:: bash

         mkdir ~/cylc-src/graph-introduction
         cd ~/cylc-src/graph-introduction

      In your new source directory create a :cylc:conf:`flow.cylc`
      file and paste the following text into it:

      .. code-block:: cylc

         [scheduler]
             allow implicit tasks = True
         [scheduling]
             [[graph]]
                 R1 = """
                     # Write graph strings here!
                 """

   #. **Write a graph.**

      We now have a blank Cylc workflow. Next we need to define a graph.

      Edit your :cylc:conf:`flow.cylc` file to add graph strings representing the
      following graph:

      .. digraph:: graph_tutorial
         :align: center

         a -> b -> d -> e
         c -> b -> f

   #. **Visualise the workflow.**

      Once you have written some graph strings try using ``cylc graph`` to
      display the workflow. Run the following command:

      .. code-block:: bash

         cylc graph .

      .. admonition:: Note
         :class: hint

         ``cylc graph`` takes the path to the workflow as an argument. Inside
         the :term:`source directory` we can just run ``cylc graph .``.

      If the results don't match the diagram above try to correct the graph
      in your :cylc:conf:`flow.cylc` file.


      .. spoiler:: Solution warning

         There are multiple correct ways to write this graph. So long as what
         you see from ``cylc graph`` matches the above diagram then you have a
         correct solution.


         Two valid examples:

            .. list-table::
               :class: grid-table

               * -
                  .. code-block:: cylc-graph

                     a & c => b => d & f
                     d => e

                 -
                  .. code-block:: cylc-graph

                     a => b => d => e
                     c => b => f


         The whole workflow should look something like this:

         .. code-block:: cylc

            [scheduler]
                allow implicit tasks = True
            [scheduling]
                [[graph]]
                    R1 = """
                        a & c => b => d & f
                        d => e
                    """
