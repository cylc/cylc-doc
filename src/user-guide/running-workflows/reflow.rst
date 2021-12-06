.. _user-guide-reflow:

Flows & Reflow
==============

.. versionadded:: 8.0.0

In Cylc, a *flow* is a single logical run of a :term:`workflow` that "flows"
on from some start point in the :term:`graph`. Cylc :term:`schedulers
<scheduler>` can manage more than one flow in the same graph, at the same time.
This capability is called *reflow*.

Triggering a Flow
-----------------

The first flow in a new workflow run gets triggered automatically when the
scheduler is :term:`started <startup>` with the ``cylc play`` command. Its
tasks are have :term:`flow number` ``1``.

Subsequent flows can be triggered from particular task(s) in the graph using
``cylc trigger --reflow``. The flow number increments by one, each time.

.. note::

   By default ``cylc trigger`` does not start a new flow from the triggered
   task. Use the ``--reflow`` option to start a new flow. :term:`Incomplete
   tasks <incomplete task>` are the exception to this rule
   because they are considered to be an unfinished part of the existing flow.

Reflow Use Cases
----------------

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
           P1 = model[-P1] => model => post => prod1 & prod2 => publish

Let's say the workflow has run to cycle 8, but we have just noticed that
a corrupted ancillary file resulted in bad products at cycle 5.

To rectify this we could fix the corrupted file and trigger a new flow
(a reflow) from ``post.5``::

   cylc trigger --reflow <workflow-id> post.5

The new flow will regenerate and republish cycle 5 products before naturally
coming to a halt, because the triggered tasks do not lead on to the next cycle
and the rest of the graph.

Meanwhile, the original flow will carry on unaffected, from cycle 8.

Flow Merging
------------

If a task from one flow catches up with an active sibling from another
(i.e. an active task with the same name and :term:`cycle point`, but a
different flow number) they will merge and carry both flow numbers
forward. Downstream tasks can be considered to belong to either flow.
Any number of flows can merge like this.

Stopping Flows
--------------

By default, ``cylc stop`` halts the entire workflow and shuts the scheduler down.

Individual flows can be stopped with ``cylc stop --flow=<flow-number>``, however.
This removes the flow number from all tasks in the :term:`active window`. Tasks
with no flow numbers do not spawn downstream. If there are no active flows
left, the scheduler will shut down.


.. warning::
   Flow numbers are not yet exposed in the UI. Consult the :term:`scheduler
   log` to see the flow number of active tasks.
