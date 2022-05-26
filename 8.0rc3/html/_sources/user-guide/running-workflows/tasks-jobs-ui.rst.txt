.. _n-window:

Tasks in the UI
===============

.. versionchanged:: 8.0.0

Cylc workflow :term:`graphs <graph>` can be very large, even infinite for
:term:`cycling workflows <cycling workflow>` with no :term:`final cycle point`.
Consequently the UI often can't display "all of the tasks" at once. Instead, it
displays tasks that belong to a graph-based :term:`window` extending a
configured number of graph edges out from active tasks.

The ``n = 0`` or *active task* window includes:

- ``preparing`` tasks
- ``submitted`` and ``running`` tasks - i.e. those with active jobs
- ``waiting`` tasks, that are :term:`actively waiting <active-waiting>` on:

  - :ref:`clock triggers <Built-in Clock Triggers>`
  - :ref:`external triggers <Section External Triggers>`
  - :ref:`internal queues <InternalQueues>`
  - :ref:`runahead limit <RunaheadLimit>`

- finished tasks retained as *incomplete*, in expectation of user intervention:

  - ``submit-failed`` tasks, if successful submission was not :term:`optional
    <optional output>`
  - ``succeeded`` or ``failed`` tasks that did not complete :term:`expected
    outputs <expected output>`

The default window extent is ``n = 1``, i.e. tasks out to one graph edge from
current active tasks.

Tasks ahead of the ``n=0`` window are displayed by the UI as ``waiting`` but
the scheduler is not actively managing them yet.

.. image:: ../../img/n-window.png
   :align: center

.. note::

   The graph-based active task window is intended to display the essential
   information without overwhelming the UI. Even very large workflows
   typically do not have a massive number of tasks active at once.
