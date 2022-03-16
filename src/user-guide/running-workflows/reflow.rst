.. _user-guide-reflow:

Multiple Flows
==============

.. versionadded:: 8.0.0

In Cylc, a *flow* is a single self-propagating run through the workflow
:term:`graph` that continues from some initial task or tasks.

Often there will only be one flow, starting at the beginning of the graph,
but Cylc :term:`schedulers<scheduler>` can manage multiple flows at once.

.. warning::
   Flows are not entirely independent: they :ref:`merge<flow-merging>`
   if they collide in the scheduler's ``n=0`` window.


Flow Numbers
------------

Flows are represented by *flow numbers* passed down from parent task to child
task in the graph.

Flow membership determines whether a task will run when a flow encounters it:
if it ran already in the same flow, it will not run again.

The first flow in a new workflow run gets triggered automatically by ``cylc
play``. Its tasks have the flow number ``1``.

Other flows can (optionally) be started by :ref:`manual
triggering<triggering-flows>`. The first manually triggered flow will have flow
number ``2``, the next ``3``, and so on.

Tasks can belong to multiple flows, due to :ref:`flow-merging` and :ref:`manual
triggering<triggering-flows>`, in which case they carry multiple flow numbers.

.. warning::
   Flow numbers are not yet exposed in the UI. Consult the :term:`scheduler
   log` to see the flow number of active tasks.


.. _triggering-flows:

Triggering & Flows
------------------

By default, manual triggering (with ``cylc trigger`` or the UI) triggers a new
front of activity in current active flows. But it can also start new flows and
trigger one-off flow-independent task runs.

In the diagrams below grey tasks represent the original flow, and blue ones
stem from a single manual triggering event.

Triggering in Current Flows
   ``cylc trigger <workflow_id>//1/foo``

   By default, ``1/foo`` triggers with all current active flow numbers - i.e.
   it belongs to those flows.

   **Ahead of active flows** this starts a new front of activity in those
   flows, at the target task. The original flow front will stop wherever it
   encounters tasks that already ran in the new front:

   .. image:: ../../img/same-flow.png

   **Behind active flows** the triggered task itself will re-run, but a new flow
   front won't start there because the tasks already ran in those flows (if they
   already traversed this part of the graph).

.. TODO UNCOMMENT AFTER THE --wait PR IS MERGED in cylc-flow.
   ``cylc trigger [--wait] <workflow_id>//1/foo``
   With the ``--wait`` option ``1/foo`` will run but not spawn children to
   continue the flow until catch up occurs. If there are multiple active flows
   as trigger time, multiple flows may continue from ``1/foo`` (without
   re-running it again) as they catch up to it.

Triggering in Specific Flows
   ``cylc trigger --flow=1,2 <workflow_id>//1/foo``

   This triggers ``1/foo`` with flow numbers ``1`` and ``2``.

   The result is just like the default above, except that tasks in the new
   front belong only to flows ``1`` and ``2``. Other flows can re-run the same
   tasks.

   .. image:: ../../img/same-flow.png

Triggering a New Flow
   ``cylc trigger --flow=new <workflow_id>//1/foo``

   This triggers ``1/foo`` with a new flow number.

   The new flow will re-run tasks that already ran in other flows.

   .. image:: ../../img/new-flow.png


Triggering a One-Off Task Run
   ``cylc trigger --flow=none <workflow_id>//1/foo``

   This triggers a task with no flow numbers.

   It will not spawn children, and other flows that come by will re-run it.

   .. image:: ../../img/no-flow.png

Special Case: ``n=0`` Tasks
   Tasks in the ``n=0`` window are active, active-waiting, or incomplete. Their
   flow membership is already determined - that of the parents that spawned them.

   - Triggering an active tasks has no effect (it already triggered).
   - Triggering an active-waiting task runs it immediately in the same flow.
   - Triggering an incomplete tasks re-runs it immediately in the same flow.


.. _flow-merging:

Flow Merging In ``n=0``
-----------------------

If a task spawning into the ``n=0`` window encounters another instance of
itself (same name and :term:`cycle point`) already there, from another flow,
the two instances will merge and carry both (sets of) flow numbers forward.

Downstream tasks are considered to belong to both flows. Any number of flows
can merge like this.

.. note::
   Flow merging in ``n=0`` means flows are not entirely independent. One flow
   *might* not be able to overtake another because a task *might* have to merge
   in ``n=0``. Merging is necessary because task IDs do not incorporate flow
   numbers and Cylc doesn't support multiple active tasks with the same ID.
   However, this does not affect the primary :ref:`Use Cases` for flows (below).


Stopping Flows
--------------

By default, ``cylc stop`` halts the entire workflow and shuts the scheduler down.

Individual flows can be stopped with ``cylc stop --flow=<flow-number>``, however.
This removes the flow number from all ``n=0`` tasks, and removes any
active-waiting tasks that have no remaining flow numbers.

Tasks with no flow numbers do not spawn children in the graph. If there are no
active flows left, the scheduler shut downs.


Use Cases
---------

Running Tasks Ahead of Time
   To make a task run early even though its prerequisites are not technically
   satisfied yet, manually trigger it in its flow. It won't re-run when the
   original flow front reaches it.

Regenerating Products Behind a Flow
   To re-run a sub-graph of tasks (e.g. because an important file was found to
   be corrupted in the original run), trigger a new flow there in the graph.

   Note you may need to stop the new flow manually once its job is done, if the
   triggered sub-graph does not lead off the main trunk of the workflow.

Rewinding a Workflow
   To rewind the whole workflow to an earlier point, allowing it to evolve a
   new path into the future, trigger a new flow there and stop the original
   flow. Alternatively, stop the scheduler and restart it from the earlier
   task(s).

Example
-------

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

To rectify this we could fix the corrupted file and trigger a new flow
(a reflow) from ``5/post``::

   cylc trigger --flow=new <workflow_id>//5/post

The new flow will regenerate and republish cycle 5 products before naturally
coming to a halt, because the triggered tasks do not lead on to the next cycle.

Meanwhile, the original flow will carry on unaffected, from cycle point 8.


