.. _expireTriggers:

Expire Triggers
===============

.. versionchanged:: 8.8.0

   Suicide triggers were replaced by expire triggers.

.. tip::

   Suicide triggers were needed in Cylc 7 and earlier to remove pre-spawned
   waiting tasks from graph branches not taken at runtime, which would stall
   the workflow.

   However, Cylc 8 does not need their replacement, expire triggers, for
   :term:`graph branching <branching>` use cases.

   They remain supported for
   other :ref:`edge cases <remaining-use-cases>`.


Expire triggers effectively remove waiting tasks from the :term:`n=0 window <n-window>`.
They are activated just like normal :term:`task triggers <task trigger>` but
the downstream task (prefixed with ``!``) will generate the ``expired`` output
instead of running.

The ``expired`` output will be marked as :term:`optional <optional output>`
for the triggered task, but if a custom `flow.cylc[runtime][<namespace>]completion`
condition is used, it will need to be updated to explicitly include ``or expired``.

The triggered task will be left in the ``expired`` state making it clearer in
the GUI/logs that the task has been triggered in this way.

It is also possible to trigger other tasks off of this ``expired`` output for more
advanced failure recovery.

Here, the task ``bar`` will be expired if ``foo`` succeeds:

.. code-block:: cylc-graph

   foo => !bar

Expire triggers combine in the same way as normal triggers, so this graph:

.. code-block:: cylc-graph

   foo => !baz
   bar => !baz

is equivalent to this:

.. code-block:: cylc-graph

   foo & bar => !baz

i.e. both ``foo`` and ``bar`` must succeed for ``baz`` to be expired.

To expire a task after any one of several events, use an OR operator:

.. code-block:: cylc-graph

   foo | bar => !baz


.. _remaining-use-cases:

Remaining Use Case
------------------

Expire triggers may be needed to dismiss a waiting :term:`active task` when it
can be inferred from the status of another task that the external trigger will
never be satisfied.

In the following example imagine that the two xtriggers watch two locations for
the same file to appear. The file will be delivered to one location or the
other but not to both, so if one xtrigger is satisfied the other will never be.
The stuck waiting task can be dismissed with an expire trigger, so that it
doesn't stall the workflow:

.. code-block:: cylc-graph

   @xtrigger1 => A
   @xtrigger2 => B

   A => !B  # If A succeeds, remove B
   B => !A  # If B succeeds, remove A
