.. _user-guide-reflow:

Flows & Reflow
==============

In Cylc, a *flow* is a single logical run of a :term:`workflow` that "flows"
on from some start point in the :term:`graph`.

Cylc :term:`schedulers <scheduler>` can manage more than one flow in the same
graph, at the same time.  We call this capability *reflow*.

Triggering a Flow
-----------------

The first flow in a new workflow run gets triggered automatically when the
scheduler is :term:`started <startup>` with the ``cylc play`` command. Its
tasks can be identified by the integer :term:`flow number` ``1``.

Subsequent flows can be triggered from particular task(s) in the graph using
``cylc trigger --reflow``. The flow number increments by one, for each new
flow.

.. note::

   Without the ``--reflow`` option ``cylc trigger`` triggers the target
   task but ndoes not start a new flow from its completed outputs.

   Triggering an :term:`incomplete task`, however, will cause its flow to
   continue, if it completes its outputs this time. Incomplete tasks are
   considered to be an unfinished part of their flow.

.. note::
   Currently you have to look at the :term:`scheduler log` to identify
   the flow numbers of particular tasks in the :term:`n=0 window <n-window>`.

Use Cases
---------

Reflows are useful if you need to re-wind your :term:`workflow` to allow
it to evolve a new path into the future, or to repeat-run some subgraph
to regenerate its outputs after making changes.

For example, the following :term:`cycling workflow` runs a :term:`task`
called ``model`` in every cycle, followed by a postprocessing task, two
product generating tasks, and finally a task that publishes results for
the cycle point:

   .. code-block:: cylc

      [scheduling]
          cycling mode = integer
          initial cycle point = 1
          [[graph]]
              P1 = """
                  model [-P1] => model => post => prod1 & prod2 => publish
              """

Let's say the workflow has run to cycle 8, but we have just noticed that
a corrupted ancillary file resulted in bad products at cycle 5.

To rectify this we could fix the corrupted file and trigger a new flow
(a reflow) from ``post.5``::

   cylc trigger post.5 --reflow <workflow-id>

The new flow will regenerate and republish cycle 5 products before naturally
coming to a halt, because the triggered tasks do not lead on to the next cycle
and the rest of the graph.

Meanwhile, the original flow will carry on unaffected, from cycle 8.

Flow Merging
------------

If a task from one flow catches up to an active sibling from another
(i.e., another active task with the same name and :term:`cycle point`,
but a different flow number) they will merge and carry both flow numbers
forward. Downstream tasks can be considered to belong to either flow.

Stopping Flows
--------------

By default, ``cylc stop`` halts the entire workflow and shuts the scheduler down.

Individual flows can be stopped with ``cylc stop --flow=<flow-number>``, however.
This removes the target flow number from all active tasks. If a task has no
flow numbers left it will not spawn downstream, thus stopping the flow. If
there are no active flows left at all, the scheduler will shut down.
