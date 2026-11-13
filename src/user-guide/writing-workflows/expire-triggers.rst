.. _expireTriggers:
Expire Triggers
=========================
.. warning::

   Suicide triggers were needed in Cylc 7 and earlier to remove pre-spawned
   waiting tasks from graph branches not taken at runtime, which would stall
   the workflow.

   However, **Cylc 8 replaced these with Expire triggers that are always active.**

   They remain supported, and documented, for
   a rare :ref:`edge case <remaining-use-cases>`.


When the condition is met, the task will generate the ``expired`` output rather than just being removed.
The ``expired`` output will be marked as :term:`optional <optional output>` for the triggered task, b
ut a custom `flow.cylc[runtime][<namespace>]completion` condition will need to be modified accordingly.
This should be functionally equivalent to "suicide triggers" in that the triggered task will not run.

The triggered task will now be left in the ``expired`` state making it clearer in the GUI/logs that the task has been triggered in this way.

It is possible to trigger other tasks off of this ``expired`` output for more advanced failure recover.

Expire triggers remove waiting tasks from the :term:`n=0 window <n-window>`.

They are activated just like normal :term:`task triggers <task trigger>` but
they remove the downstream task (prefixed with ``!``) instead of triggering it
to run.

Here, the task ``bar`` will be removed if ``foo`` succeeds:

.. code-block:: cylc-graph

   foo => !bar

Expire triggers combine in the same way as normal triggers, so this graph:

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

Expire triggers may be needed to remove a waiting :term:`active task` when it
can be inferred from the status of another task that the external trigger will
never be satisfied.

In the following example imagine that the two xtriggers watch two locations for
the same file to appear. The file will be delivered to one location or the
other but not to both, so if one xtrigger is satisfied the other will never be.
The stuck waiting task can be removed with a Expire trigger, so that it
doesn't stall the workflow:

.. code-block:: cylc-graph

   @xtrigger1 => A
   @xtrigger2 => B

   A => !B  # If A succeeds, remove B
   B => !A  # If B succeeds, remove A
