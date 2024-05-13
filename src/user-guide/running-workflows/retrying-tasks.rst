Retrying Tasks
==============

.. versionchanged:: 8.0.0

Tasks that fail but are configured to :term:`retry` return to the ``waiting``
state, with a new clock trigger to handle the configured retry delay.

.. note::

   A task that is waiting on a retry will already have one or more failed jobs
   associated with it.


.. note::

   Tasks only enter the ``submit-failed`` state if job submission fails with no
   retries left. Otherwise they return to the waiting state, to wait on the
   next try.

   Tasks only enter the ``failed`` state if job execution fails with no retries
   left. Otherwise they return to the waiting state, to wait on the next try.



Aborting a Retry Sequence
-------------------------

To prevent a waiting task from retrying, remove it from the scheduler's
:term:`active window`. For a task ``3/foo`` in workflow ``brew``:

.. code-block:: console

   $ cylc remove brew//3/foo

If you *kill* a running task that has more retries configured, it goes to the
``held`` state so you can decide whether to release it and continue the retry
sequence, or remove it.

.. code-block:: console

   $ cylc kill brew//3/foo     # 3/foo goes to held state post kill
   $ cylc release brew//3/foo  # release to continue retrying...
   $ cylc remove brew//3/foo   # ... OR remove the task to stop retries


If you want trigger downstream tasks despite ``3/foo`` being removed before it
could succeed, use ``cylc set`` to artificially mark its ``succeeded``
output as complete (and with the ``--flow`` option, to make the :term:`flow`
continue on from there).
