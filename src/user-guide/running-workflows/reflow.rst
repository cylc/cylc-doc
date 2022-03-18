.. _user-guide-reflow:

Multiple Flows
==============

.. versionadded:: 8.0.0

In Cylc, a *flow* is a self-propagating run through the workflow :term:`graph`
from some initial task or tasks.

Often there is only one flow: the original one started automatically at the
beginning of the graph. But Cylc can manage multiple flows at once.

When a flow advances to a new task in the :term:`graph`, the task will only run
if it did not already run in the same flow.

See below for suggested :ref:`use cases<flow-trigger-use-cases>` and an
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

Tasks can carry multiple flow numbers as a result of
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

   With ``--wait``, the result is the same except that any action downstream of 
   the triggered task is delayed until the first flow catches it.

   **Behind active flows** the triggered task itself will re-run, then activity
   will cease if any of the original flows already traversed that part of the
   graph.

Triggering in Specific Flows
   ``cylc trigger --flow=1,2 ID``

   This triggers the task with flow numbers ``1`` and ``2``.

   The result is like the default above, except that tasks in the new front
   belong only to the specified flow(s), regardless of which flows are active
   at triggering time.

Triggering a New Flow
   ``cylc trigger --flow=new ID``

   This triggers the task with a new, incremented flow number.

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

If a task spawning into the ``n=0`` :term:`window` finds another instance
of itself (same name and cycle point, different flow) already there, a single
instance of it will carry both (sets of) flow numbers forward from that point.
Downstream tasks belong to both flows.

Flow merging in ``n=0`` means flows are not entirely independent. One flow
might not be able to overtake another because one or more of its tasks might
merge in ``n=0``. Merging is necessary while task IDs - and associated log
directory paths etc. - do not incorporate flow numbers, because task IDs must
be unique in the active task pool.

Incomplete tasks
^^^^^^^^^^^^^^^^

Incomplete tasks are retained in the active window in expectation of
retriggering once fixed, to complete expected outputs and continue the flow.

If another flow encounters an incomplete task, one task will carry both flow
numbers forward on successfully completing its expected outputs.

.. TODO whether or not it automatically reruns in the later flow is still an
   open question: https://github.com/cylc/cylc-flow/pull/4737


Stopping Flows
--------------

By default, ``cylc stop`` halts the workflow and shuts the scheduler down.

It can also stop specific flows: ``cylc stop --flow=N`` removes the flow number
``N`` from tasks in the active pool. Tasks that have no flow numbers left as a
result do not spawn children at all. If there are no active flows left, the
scheduler shuts down.

.. TODO update this section post https://github.com/cylc/cylc-flow/issues/4741


.. _flow-trigger-use-cases:

Use Cases
---------

Running Tasks Ahead of Time
   To run a task even though its prerequisites are not satisfied, just trigger
   it. Use ``--wait`` if you don't want the new front to continue immediately.
   Triggered task(s) will not re-run when the main flow front catches up.

Regenerating Products Behind a Flow
   To re-run a sub-graph (e.g. because the original run was affected by a
   corrupt file), just trigger the task(s) at the top of the sub-graph with
   ``--flow=new``.

   You may need to manually stop the new flow once its job is done, to avoid
   re-running more than you want to, if the new flow leads into the main
   trunk of the graph.

Rewinding a Workflow
   To rewind the workflow to an earlier point, perhaps to regenerate data and/or 
   allow the workflow to evolve a new path into the future, trigger a new
   flow at the right place and then stop the original flow. (Alternatively,
   stop the scheduler, install a new instance of the workflow, and play it
   from the desired place in the graph).

Test-running Tasks in a Live Workflow
   You can trigger individual tasks as many times as you like with
   ``--flow=none``, without affecting the workflow.

Processing Flow-specific Data
   Flow numbers are passed to task environments, so it is possible to have
   different flows process different datasets through the same graph. However
   we do not recommend doing this. Generally, that's what cycling is for; and
   besides, each task would have to be capable of processing multiple datasets
   at once in case of :ref:`flow-merging`.
 

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
