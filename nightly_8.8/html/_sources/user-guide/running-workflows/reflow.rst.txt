.. _user-guide-reflow:

Concurrent Flows
================

.. versionadded:: 8.0.0

In Cylc, a *flow* is a single self-consistent run through the workflow
:term:`graph` from some initial task(s).

As a flow advances, upcoming tasks run only if they have not already run in
the same flow.

At start-up the :term:`scheduler` automatically triggers the first flow from
the start of the graph.

By default, manually triggered tasks "belong to" the existing flow(s), but you
can also choose to start new flows by triggering tasks anywhere in the graph.

.. note::
   A flow does not have to be contiguous in the graph because different graph
   branches can evolve at different rates, and tasks can be manually triggered
   anywhere in the graph.

See :ref:`below<flow-trigger-use-cases>` for uses, and an
:ref:`example<new-flow-example>`, of concurrent flows.

.. note::
   Flows :ref:`merge<flow-merging>` where (and if) tasks collide in the
   :term:`n=0 window <n-window>`. Downstream of a merge, tasks are considered to belong
   to all of their constituent flows.


Flow Numbers
------------

Flows are identified by numbers passed down from parent task to child task in
the graph.

Flow number ``1`` is triggered automatically by ``cylc play`` at :term:`scheduler`
start-up. The next flow started by :ref:`manual triggering<triggering-flows>`
gets the number ``2``, then ``3``, and so on.

Tasks can carry multiple flow numbers as a result of :ref:`flow
merging<flow-merging>`.

.. note::
   Flow numbers are not yet exposed in the UI, but they are logged with task
   events in the :term:`scheduler log`.


.. _triggering-flows:

Triggering & Flows
------------------

By default, manual triggering (with ``cylc trigger`` or the UI) starts a new
:term:`front of activity<flow front>` in current flows.
But it can also start new flows and trigger flow-independent single tasks.

In the diagrams below, the grey tasks run in the original flow (``1``), and the
blue ones run as a result of a manual triggering event. They may be triggered
as part of flow ``1``, or as a new flow ``2``, or with no flow number.

Triggering in Current Flows
   ``cylc trigger [--wait] ID``

   This is the default action. The triggered task gets all current active flow
   numbers. Subsequently, each of those flows will consider the task to have
   run already.

   **Ahead of active flows** this starts a new front of activity for the
   existing flows, which by default can continue on without waiting for them to
   catch up:

   .. image:: ../../img/same-flow-n.png

   With ``--wait``, action downstream of the triggered task is delayed until
   the first flow catches up:

   .. image:: ../../img/same-flow-wait-n.png

   **Behind active flows** the triggered task will run, but nothing more will
   happen if any of the original flows already passed by there:

   .. image:: ../../img/same-flow-behind.png

Triggering in Specific Flows
   ``cylc trigger --flow=1,2 ID``

   This triggers the task with flow numbers ``1`` and ``2``.

   The result is like the default above, except that tasks in the new front
   belong only to the specified flow(s), regardless of which flows are
   active at triggering time.

Triggering a New Flow
   ``cylc trigger --flow=new ID``

   This triggers the task with a new, incremented flow number.

   The new flow will re-run tasks that already ran in previous flows:

   .. image:: ../../img/new-flow-n.png


Triggering a Flow-Independent Single Task
   ``cylc trigger --flow=none ID``

   This triggers a task with no flow numbers.

   It will not spawn children, and other flows that come by will re-run it.

   .. image:: ../../img/no-flow-n.png

Triggering with No Active Flows
   ``cylc trigger [--wait] ID``

   By default, triggered tasks will be given the flow numbers of the most
   recent :term:`active tasks <active task>`. This can happen, for instance,
   if you restart an already-completed workflow and then manually trigger a
   task in it. The task's flow number will be the same as if you
   had triggered it just before the workflow completed.

Special Case: Triggering ``n=0`` (:term:`active tasks <active task>`)
   Active tasks already have flow membership assigned.
   Flow numbers are inherited, on entering the active window, from parent
   (upstream) tasks in the graph.

   - Triggering a task with a submitted or running job has no effect
     (it is already triggered).
   - Triggering other :term:`active tasks <active task>`, including those with
     :term:`incomplete outputs <output completion>`, queues them to run with
     their existing flow numbers.


.. _flow-merging:

Flow Merging in ``n=0``
-----------------------

If a task spawning into the :term:`n=0 window <n-window>` finds another instance
of itself (same task ID) already there, the two will merge and carry both
(sets of) flow numbers forward. Downstream tasks will belong to both flows.

Flows merge because every :term:`active task` must have a unique ID. However,
merging is also useful: it allows a simpler single flow to continue downstream of
multi-flow interventions.

If the original task instance has a :term:`final status` (and has been retained
in the :term:`n=0 window <n-window>` with
:term:`incomplete outputs <output completion>`) the merged task will be reset to
run again without manual intervention.


Stopping Flows
--------------

By default, ``cylc stop`` halts the workflow and shuts the scheduler down.

It can also stop specific flows: ``cylc stop --flow=N`` removes the flow number
``N`` from :term:`active tasks <active task>`. Tasks with no remaining flow
numbers will not spawn downstream activity. If there are
no active flows left, the scheduler shuts down.

.. TODO update this section post https://github.com/cylc/cylc-flow/issues/4741


.. _flow-trigger-use-cases:

Some Use Cases
--------------

Running Tasks Ahead of Time
   To run a task within the existing flow(s) even though its prerequisites are
   not yet satisfied, just trigger it. Use ``--wait`` if you don't want the new
   flow front to continue immediately. Triggered task(s) will not re-run when
   the main front catches up.

Regenerating Outputs Behind a Flow
   To re-run a sub-graph (e.g. because the original run was affected by a
   corrupt file), just trigger the task(s) at the top of the sub-graph with
   ``--flow=new``.

   You may need to manually stop the new flow if it leads into the main trunk
   of the graph, and you do not want it to carry on indefinitely.

Rewinding a Workflow
   To rewind the workflow to an earlier point, perhaps to regenerate data and/or
   allow the workflow to evolve a new path into the future, trigger a new
   flow at the right place and then stop the original flow.

Test-running Tasks in a Live Workflow
   You can trigger individual tasks as many times as you like with
   ``--flow=none``, without affecting the workflow. The task :term:`submit
   number` will increment each time.

Processing Flow-Specific Data?
   :term:`Flow numbers<flow number>` are passed to job environments, so it is
   possible for tasks to process flow-specific data. Every task would have to
   be capable of processing multiple datasets at once, however, in case of
   :term:`flow merging<flow merge>`. Generally, you should use :term:`cycling`
   for this kind of use case.

.. _new-flow-example:

Example: Rerun a Sub-Graph
---------------------------

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
