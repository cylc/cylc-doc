.. _tutorial.furthertopics.queues:

Queues
======

Queues are used to put a limit on the number of tasks that will be active at
any one time, even if their dependencies are satisfied. This avoids swamping
systems with too many tasks at once.


Example
-------

In this example, our workflow manages a particularly understaffed restaurant.

Create a new workflow called ``queues-tutorial``::

   mkdir -p ~/cylc-run/queues-tutorial
   cd ~/cylc-run/queues-tutorial

And paste the following into :cylc:conf:`flow.cylc`:

.. code-block:: cylc

   [scheduling]
       [[graph]]
           R1 = """
               open_restaurant => steak1 & steak2 & pasta1 & pasta2 & pasta3 & \
                                  pizza1 & pizza2 & pizza3 & pizza4
               steak1 => ice_cream1
               steak2 => cheesecake1
               pasta1 => ice_cream2
               pasta2 => sticky_toffee1
               pasta3 => cheesecake2
               pizza1 => ice_cream3
               pizza2 => ice_cream4
               pizza3 => sticky_toffee2
               pizza4 => ice_cream5
           """

   [runtime]
       [[open_restaurant]]
       [[MAINS]]
       [[DESSERT]]
       [[steak1,steak2,pasta1,pasta2,pasta3,pizza1,pizza2,pizza3,pizza4]]
           inherit = MAINS
       [[ice_cream1,ice_cream2,ice_cream3,ice_cream4,ice_cream5]]
           inherit = DESSERT
       [[cheesecake1,cheesecake2,sticky_toffee1,sticky_toffee2]]
           inherit = DESSERT

.. note::

   In graph sections, lines can be split on ``&``, i.e. the
   following two examples are equivalent:

   .. code-block:: cylc-graph

      foo => bar &
             baz

   .. code-block:: cylc-graph

      foo => bar & baz

   ``|`` (or), and ``=>`` act in the same way.

Validate, install and play the workflow::

   cylc validate .
   cylc install --run-name without-queues

Look at the workflow with :ref:`tutorial.gui` or :ref:`tutorial.tui`

Play the workflow, either from the GUI or the command line::

   cylc play queues-tutorial/without-queues

You will see that all the ``steak``, ``pasta``, and ``pizza`` tasks are run
at once, swiftly followed by all the ``ice_cream``, ``cheesecake``,
``sticky_toffee`` tasks as the customers order from the dessert menu.


This will overwhelm our restaurant staff! The chef responsible for ``MAINS``
can only handle 3 tasks at any given time, and the ``DESSERT`` chef can only
handle 2.

We need to add some queues. Add a ``[queues]`` section to the ``[scheduling]``
section like so:

.. code-block:: cylc

   [scheduling]
       [[queues]]
           [[[mains_chef_queue]]]
               limit = 3  # Only 3 mains dishes at one time.
               members = MAINS
           [[[dessert_chef_queue]]]
               limit = 2  # Only 2 dessert dishes at one time.
               members = DESSERT

Install and play the workflow::

   cylc validate .
   cylc install --run-name tutorial-with-queues

Play the workflow using the :ref:`GUI <tutorial.gui>`
or :ref:`TUI <tutorial.tui>`.

You should see that there are now never more than 3 active ``MAINS`` tasks
running and never more than 2 active ``DESSERT`` tasks running.

The customers will obviously have to wait!


Further Reading
---------------

For more information, see the `Cylc User Guide`_.
