.. _SuicideTriggers:

Suicide Triggers
^^^^^^^^^^^^^^^^

.. warning::

   **Cylc 8 does not need suicide triggers for** :term:`graph branching
   <branching>`.

   They were needed in Cylc 7 to remove waiting tasks from alternate graph
   branches not taken at runtime, which would otherwise stall the workflow.

   They remain supported, and documented, for backward compatibility reasons
   and possible rare :ref:`edge cases <remaining-use-cases>`.


Suicide triggers can remove waiting :term:`tasks <task>` from the
:term:`scheduler's <scheduler>` active :term:`active window` at runtime.

They are activated just like other :term:`triggers <task trigger>` but they
trigger removal of the downstream task (prefixed with ``!``) instead of
triggering it to run.

Here, the task ``bar`` will be removed if ``foo`` succeeds:

.. code-block:: cylc-graph

   foo => !bar

Suicide triggers combine in the same way as normal triggers, so this:

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

   * There's no point removing tasks that are not in the ``waiting`` state
   * Waiting tasks in front of the active window are virtual and don't need to
     be "removed"
   * The only non-virtual waiting tasks are those :term:`waiting actively
     <active waiting task>` on an external trigger; these might need to be
     removed if they will never run (see below)


.. _remaining-use-cases:

Remaining Use Case
------------------

Suicide triggers may be needed to remove an :term:`active waiting task` when it
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
