.. _SuicideTriggers:

Suicide Triggers
================

.. warning::

   Suicided triggers were needed in Cylc 7 and earlier to remove pre-spawned
   waiting tasks from graph branches not taken at runtime, which would stall
   the workflow.

   However, **Cylc 8 does not need suicide triggers for** :term:`graph
   branching <branching>`.

   They remain supported, and documented, for backward compatibility and for
   a rare :ref:`edge case <remaining-use-cases>`.


Suicide triggers remove waiting tasks from the :term:`n=0 window <n-window>`.

They are activated just like normal :term:`task triggers <task trigger>` but
they remove the downstream task (prefixed with ``!``) instead of triggering it
to run.

Here, the task ``bar`` will be removed if ``foo`` succeeds:

.. code-block:: cylc-graph

   foo => !bar

Suicide triggers combine in the same way as normal triggers, so this graph:

.. code-block:: cylc-graph

   foo => !baz
   bar => !baz

is equivalent to this:

.. code-block:: cylc-graph

   foo & bar => !baz

i.e. both ``foo`` and ``bar`` must succeed for ``baz`` to be removed.

To remove a task after any one of several events, use an OR operator:

.. code-block:: cylc-graph

   foo | bar => !baz

.. note::

   At present, only :term:`active tasks <active task>` that are waiting
   (e.g. queued tasks) can be removed by ``cylc remove``.


.. _remaining-use-cases:

Remaining Use Case
------------------

Suicide triggers may be needed to remove a waiting :term:`active task` when it
can be inferred from the status of another task that the external trigger will
never be satisfied.

In the following example imagine that the two xtriggers watch two locations for
the same file to appear. The file will be delivered to one location or the
other but not to both, so if one xtrigger is satisfied the other will never be.
The stuck waiting task can be removed with a suicide trigger, so that it
doesn't stall the workflow:

.. code-block:: cylc-graph

   @xtrigger1 => A
   @xtrigger2 => B

   A => !B  # If A succeeds, remove B
   B => !A  # If B succeeds, remove A
