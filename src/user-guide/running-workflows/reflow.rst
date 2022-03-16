.. _user-guide-reflow:

Multiple Flows
==============

.. versionadded:: 8.0.0

In Cylc, a *flow* is a self-propagating run through the workflow :term:`graph`
from some initial task or tasks.

Usually there is only one flow, the original one starting from the beginning of
the graph, but Cylc can manage multiple flows at once.

When a flow advances to a new task in the :term:`graph`, the task will only run
if it did not already run in the same flow.

See :ref:`below<flow-trigger-use-cases>` for suggested use cases and an
:ref:`example<new-flow-example>`.

.. note::
   Flows are not entirely independent: they :ref:`merge<flow-merging>`
   where (and if) tasks collide in the ``n=0`` :term:`active window`.


Flow Numbers
------------

Flows are identified by numbers passed down from parent task to child task in
the graph.

Flow number ``1`` is triggered automatically by ``cylc play`` at :term:`scheduler`
start-up. The next flow started by :ref:`manual triggering<triggering-flows>`
gets the number ``2``, then ``3``, and so on.

Tasks with multiple flow numbers belong to multiple flows as a result of
:ref:`flow merging<flow-merging>` and :ref:`manual triggering<triggering-flows>`.

.. note::
   Flow numbers are not yet exposed in the UI, but they are logged with task
   events in the :term:`scheduler log`.


.. _triggering-flows:

Triggering & Flows
------------------

By default, manual triggering (with ``cylc trigger`` or the UI) starts a new
:term:`front of activity<flow front>` in current flows.
But it can also start new flows and trigger flow-independent single tasks.

In the diagrams below, the grey nodes represent tasks in flow ``1``, and
the blue ones stem from a single manual triggering event.

Triggering in Current Flows
   ``cylc trigger [--wait] ID``

   This is the default trigger action: trigger the task and give it all current
   active flow numbers. Subsequently, each of those flows will consider this
   task to have run already.

   **Ahead of active flows** this starts a new front of activity for the active
   flows, which by default can continue on without waiting for catch up.

   .. image:: ../../img/same-flow-n.png

   With ``--wait`` the triggered task runs immediately but any downstream action
   is delayed until the flows catch up. If there are multiple active flows at
   trigger time, each one can continue on separately from the triggered task
   (without re-running it) as they separately catch-up to it. Without
   ``--wait`` a single front of activity representing all active flows
   continues immediately after triggering.

   **Behind active flows** the triggered task itself will re-run, then activity
   will cease if the original flows already traversed the same part of the graph.

Triggering in Specific Flows
   ``cylc trigger --flow=1,2 ID``

   This triggers the task with flow numbers ``1`` and ``2``.

   The result is like the default above, except that tasks in the new front
   belong only to the specified flow(s), regardless of which flows are active
   at triggering time.

Triggering a New Flow
   ``cylc trigger --flow=new ID``

   This triggers the task with a new flow number.

   The new flow will re-run tasks that already ran in previous flows.

   .. image:: ../../img/new-flow-n.png


Triggering a Flow-Independent Single Task
   ``cylc trigger --flow=none ID``

   This triggers a task with no flow numbers.

   It will not spawn children, and other flows that come by will re-run it.

   .. image:: ../../img/no-flow-n.png

Special Case: Triggering ``n=0`` Tasks
   Tasks in the ``n=0`` window are active, active-waiting, or incomplete. Their
   flow membership is already determined - that of the parents that spawned them.

   - Triggering an active task has no effect (it is already triggered).
   - Triggering an active-waiting task runs it immediately in the same flow.
   - Triggering an incomplete task re-runs it immediately in the same flow.


.. _flow-merging:

Flow Merging In ``n=0``
-----------------------

If a task spawning into the ``n=0`` window encounters another instance of
itself (same name and :term:`cycle point`) from another flow, the two task
instances merge and carry both (sets of) flow numbers forward.

Downstream tasks are considered to belong to both flows. Any number of flows
can merge like this.

.. note::
   Flow merging in ``n=0`` means flows are not entirely independent. One flow
   *might* not be able to overtake another because a task *might* merge in
   ``n=0``. Merging is necessary while task IDs do not incorporate flow numbers,
   because we can't have multiple active tasks with the same ID.


Stopping Flows
--------------

By default, ``cylc stop`` halts the entire workflow and shuts the scheduler
down. Individual flows can be stopped with ``cylc stop --flow=F``, however.
This removes the flow number ``F`` from all ``n=0`` tasks, and removes any
active-waiting tasks that have no remaining flow numbers.

Tasks with no flow numbers do not spawn children in the graph. If there are no
active flows left, the scheduler shut downs.


.. _flow-trigger-use-cases:

Use Cases
---------

Running Tasks Ahead of Time
   To run a task now even though its prerequisites are not yet satisfied, just
   trigger it. Use `--wait` if you don't want the triggered front to continue
   immediately. The triggered task(s) will not re-run when the main flow front
   catches up.

Regenerating Products Behind a Flow
   To re-run a sub-graph (e.g. because the original run was affected by a
   corrupt file), just trigger the task(s) at the top of the sub-graph with
   ``--flow=new``.

   You may need to manually stop the new flow once its job is done, to avoid
   re-running more than you want to, if the new flow leads into the main
   trunk of the graph.

Rewinding a Workflow
   To rewind the workflow to an earlier point, to regenerate data or perhaps
   to allow the workflow to evolve a new path into the future, trigger a new
   flow at the right task(s) and then stop the original flow. (Alternatively,
   stop the scheduler and play it again from the desired task(s)).

Test-running Tasks in a Live Workflow
   You can trigger individual tasks as many times as you like with
   ``--flow=none``, without affecting the workflow.
 
.. _new-flow-example:

Example: Rerun a Past Sub-graph
-------------------------------

The following :term:`cycling workflow` runs a :term:`task` called ``model`` in
every cycle, followed by a postprocessing task, two product-generating tasks,
and finally a task that publishes results for the cycle point:

.. code-block:: cylc

   [scheduling]
       cycling mode = integer
       initial cycle point = 1
       [[graph]]
           P1 = model[-P1] => model => post => prod1 & prod2 => publish

Let's say the workflow has run to cycle 8, but we have just noticed that
a corrupted ancillary file resulted in bad products at cycle 5.

To rectify this we could fix the corrupted file and trigger a new flow at
``5/post``:

.. code-block:: cylc

   cylc trigger --flow=new <workflow_id>//5/post

The new flow will regenerate and republish cycle 5 products before naturally
coming to a halt, because the triggered tasks do not feed into the next cycle.

Meanwhile, the original flow will carry on unaffected, from cycle point 8.
