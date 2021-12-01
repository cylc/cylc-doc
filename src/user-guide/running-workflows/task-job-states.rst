.. |task-waiting| image:: ../../img/task-job-icons/task-waiting.png
   :scale: 100%
   :align: middle

.. |task-expired| image:: ../../img/task-job-icons/task-expired.png
   :scale: 100%
   :align: middle

.. |task-preparing| image:: ../../img/task-job-icons/task-preparing.png
   :scale: 100%
   :align: middle

.. |task-submitted| image:: ../../img/task-job-icons/task-submitted.png
   :scale: 100%
   :align: middle

.. |task-submit-failed| image:: ../../img/task-job-icons/task-submit-failed.png
   :scale: 100%
   :align: middle

.. |task-running| image:: ../../img/task-job-icons/task-running.png
   :scale: 100%
   :align: middle

.. |task-succeeded| image:: ../../img/task-job-icons/task-succeeded.png
   :scale: 100%
   :align: middle

.. |task-failed| image:: ../../img/task-job-icons/task-failed.png
   :scale: 100%
   :align: middle


.. |job-blank| image:: ../../img/task-job-icons/job-blank.png
   :scale: 100%
   :align: middle

.. |job-submitted| image:: ../../img/task-job-icons/job-submitted.png
   :scale: 100%
   :align: middle

.. |job-submit-failed| image:: ../../img/task-job-icons/job-submit-failed.png
   :scale: 100%
   :align: middle

.. |job-running| image:: ../../img/task-job-icons/job-running.png
   :scale: 100%
   :align: middle

.. |job-succeeded| image:: ../../img/task-job-icons/job-succeeded.png
   :scale: 100%
   :align: middle

.. |job-failed| image:: ../../img/task-job-icons/job-failed.png
   :scale: 100%
   :align: middle


.. _task-job-states:

Task and Job States
===================

**Tasks** are a workflow abstraction; they represent future and past jobs as
well as current active ones. Task states are represented by monochromatic icons
like |task-running|.

**Jobs** are less of an abstraction; they represent real job scripts submitted
to run as a process on a computer somewhere, or the final status of those
real processes. Job states are represented by colored icons like |job-running|.
Several color themes are provided.

A single task can have multiple jobs, by automatic retry or manual triggering.


.. table::

    =======================================================     ===========
    Task & Job States                                           Description
    =======================================================     ===========
    |task-waiting|       |job-blank|          waiting           waiting on prerequisites
    |task-expired|       |job-blank|          expired           will not submit job (too far behind)
    |task-preparing|     |job-blank|          preparing         job being prepared
    |task-submitted|     |job-submitted|      submitted         job submitted
    |task-submit-failed| |job-submit-failed|  submit-failed     job submission failed
    |task-running|       |job-running|        running           job running
    |task-succeeded|     |job-succeeded|      succeeded         job succeeded
    |task-failed|        |job-failed|         failed            job failed
    =======================================================     ===========


.. _n-window:

Tasks Shown in the UIs
======================

Cylc graphs can be very large or even infinite in extent. The UI can't display
all the tasks at once, so it displays a :term:`window` or view of the workflow
centered on current active tasks and extending ``n`` graph edges out from them.

The ``n = 0`` or *active task* window includes:

- ``preparing`` tasks
- ``submitted`` and ``running`` tasks - i.e. those with active jobs
- ``waiting`` tasks, that are :term:`actively waiting <active waiting task>` on:

  - :ref:`clock triggers <Built-in Clock Triggers>`
  - :ref:`external triggers <Section External Triggers>`
  - :ref:`internal queues <InternalQueues>`
  - :ref:`runahead limit <RunaheadLimit>`

- finished tasks retained as *incomplete*, in expectation of user intervention:

  - ``submit-failed`` tasks, if successful submission was not :term:`optional <optional output>`
  - ``succeeded`` or ``failed`` tasks that did not complete :term:`expected
    outputs <expected output>`

The default window extent is ``n = 1``, i.e. tasks out to one graph edge from
current active tasks.

Tasks ahead of the ``n=0`` window are displayed by the UI as ``waiting`` but
the scheduler is not actively managing them yet.


.. image:: ../../img/n-window.png
   :align: center


Retrying Tasks
==============

Tasks that fail but are configured to :term:`retry` return to the ``waiting``
state, with a new clock trigger to handle the configured retry delay.

.. note::

   A task that is waiting on a retry will already have one or more failed jobs
   associated with it.

Aborting a Retry Sequence
-------------------------

To prevent a waiting task from retrying, remove it from the scheduler.
If the example above is installed as ``demo``:

.. code-block:: console

   $ cylc remove demo flaky.1

If a task with retries gets *killed* while running, it goes to the ``held``
state so you decide whether to release it and continue the retry
sequence, or abort.

.. code-block:: console

   $ cylc kill demo flaky.1  # flaky.1 goes to held state post kill
   $ cylc release demo flaky.1  # release to continue retrying
   $ cylc remove demo flaky.1  # OR remove the task to abort retries


If you want ``whizz`` to trigger downstream tasks despite ``flaky.1`` being
removed before it succeeded, use ``cylc set-outputs demo flaky.1`` to
artificially mark it as succeeded (and use the ``--flow`` option if you want
the flow to continue after ``whizz``).
