Retrying Tasks
==============

.. versionchanged:: 8.0.0

Tasks that fail but are configured to :term:`retry` return to the ``waiting``
state, with a new clock trigger to handle the configured retry delay.

.. note::

   A task that is waiting on a retry will already have one or more failed jobs
   associated with it.

Aborting a Retry Sequence
-------------------------

To prevent a waiting task from retrying, remove it from the scheduler's
:term:`active window`. For a task ``foo.3`` in workflow ``brew``:

.. code-block:: console

   $ cylc remove brew foo.3

If you *kill* a running task that has more retries configured, it goes to the
``held`` state so you can decide whether to release it and continue the retry
sequence, or remove it.

.. code-block:: console

   $ cylc kill brew foo.3  # foo.3 goes to held state post kill
   $ cylc release brew foo.3  # release to continue retrying...
   $ cylc remove brew foo.3  # ... OR remove the task to stop retries


If you want trigger downstream tasks despite ``foo.3`` being removed before it
could succeed, use ``cylc set-outputs`` to artificially mark its ``succeeded``
output as complete (and with the ``--flow`` option, to make the :term:`flow`
continue on from there).
