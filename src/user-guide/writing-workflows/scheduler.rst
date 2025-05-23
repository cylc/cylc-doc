Scheduler Configuration
=======================

The :cylc:conf:`flow.cylc[scheduler]` section configures certain aspects of
:term:`scheduler` behaviour at the workflow level.

Many of these configurations can also be defined at the site or user level in
the :cylc:conf:`global.cylc[scheduler]` section where it applies to all
workflows.


.. _user_guide.scheduler.workflow_event_handling:
.. _user_guide.scheduler.workflow_events:

Workflow Events
---------------

There are two types of event in Cylc:

* workflow events e.g. ``startup`` and ``shutdown``, which pertain to the :term:`scheduler` 
* task events e.g. ``submitted`` and ``failed``, which pertain to :term:`tasks <task>`.

This section covers workflow events, for
task events see :ref:`user_guide.runtime.task_event_handling`.

.. rubric:: Event Handlers

Workflow events have "handlers" (i.e. hooks) which allow configured commands to
run when workflow events occur. These can be configured by:

* :cylc:conf:`flow.cylc[scheduler][events]` (per workflow)
* :cylc:conf:`global.cylc[scheduler][events]` (user/site defaults)

.. rubric:: Abort On Event

As well as event handlers, you can tell the scheduler to abort (i.e., shut down
immediately with error status) on certain workflow events, using the
``abort on ...`` configurations.

.. rubric:: Configuration

Some workflow events have related configurations e.g. for setting the timeout.

.. rubric:: List of workflow events:

.. cylc-scope:: global.cylc[scheduler][events]

.. describe:: startup

   :Event Handler: `startup handlers`

   The scheduler was started or restarted.

   E.G. using one of these commands ``cylc play``, ``cylc vip`` or ``cylc vr``.

.. describe:: shutdown

   :Event Handler: `shutdown handlers`

   The scheduler was shut down.

   E.G. using the ``cylc stop`` command.

.. describe:: abort

   :Event Handler: `abort handlers`

   The scheduler shut down early with error status, due to a fatal error
   condition or a configured timeout.

.. describe:: workflow timeout

   :Configuration: `workflow timeout`
   :Event Handler: `workflow timeout handlers`
   :Abort On Event: `abort on workflow timeout`

   The workflow run timed out.

   The timer starts counting down at scheduler startup. It resets on workflow
   restart.

   Note, the ``abort`` event is not raised by "Abort On Event" handlers.

.. describe:: stall

   :Event Handler: `stall handlers`

   The workflow :term:`stalled <stall>` (i.e. the scheduler cannot make any
   further progress due to runtime events).

   E.G. a task failure is blocking the pathway through the graph.

.. describe:: stall timeout

   :Configuration: `stall timeout`
   :Event Handler: `stall timeout handlers`
   :Abort On Event: `abort on stall timeout`

   The workflow timed out after stalling.

.. describe:: inactivity timeout

   :Configuration: `inactivity timeout`
   :Event Handler: `inactivity timeout handlers`
   :Abort On Event: `abort on inactivity timeout`

   The workflow timed out with no activity (i.e. a period with no job
   submissions or task messages).

   This can be useful for system administrators to help catch workflows which
   have become stalled on external conditions or system issues.

.. describe:: restart timeout

   :Configuration: `restart timeout`

   If a workflow that has run to completion is restarted, the scheduler will
   have nothing to do so will shut down. This timeout gives the user a grace
   period in which to trigger new tasks to continue the workflow run.

.. cylc-scope::

Mail Events
^^^^^^^^^^^

Cylc can send emails for workflow events, these are configured by
:cylc:conf:`flow.cylc[scheduler][events]mail events`.

For example with the following configuration, emails will be sent if a
scheduler stalls or shuts down for an unexpected reason.

.. code-block:: cylc

   [scheduler]
       [[events]]
           mail events = stall, abort

Email addresses and servers are configured by
:cylc:conf:`global.cylc[scheduler][mail]`.

Workflow event emails can be customised using
:cylc:conf:`flow.cylc[scheduler][mail]footer`,
:ref:`workflow_event_template_variables` can be used.

For example to integrate with the Cylc 7 web interface (Cylc Review) the mail
footer could be configured with a URL:

.. code-block:: cylc

   [scheduler]
       [[events]]
           mail footer = http://cylc-review/taskjobs/%(owner)s/?suite=%(workflow)s

Custom Event Handlers
^^^^^^^^^^^^^^^^^^^^^

Cylc can also be configured to invoke scripts on workflow events.

Event handler scripts can be stored in the workflow ``bin`` directory, or
anywhere in ``$PATH`` in the :term:`scheduler` environment.

They should return quickly to avoid tying up the scheduler process pool -
see :ref:`Managing External Command Execution`.

Contextual information can be passed to the event handler via
:ref:`workflow_event_template_variables`.

For example the following configuration will write some information to a file
when a workflow is started:

.. code-block:: bash
   :caption: ~/cylc-run/<workflow-id>/bin/my-handler

   #!/bin/bash

   echo "Workflow $1 is running on $2:$3" > info

.. code-block:: cylc
   :caption: flow.cylc or global.cylc

   [scheduler]
       [[events]]
           startup handlers = my-handler %(workflow)s %(host) %(port)


.. note::

   If you wish to use custom Python Libraries in an event handler you
   need to add these to ``CYLC_PYTHONPATH`` rather than ``PYTHONPATH``.

.. _workflow_event_template_variables:

Workflow Event Template Variables
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. autoenumvalues:: cylc.flow.workflow_events.EventData


.. _Managing External Command Execution:

External Command Execution
--------------------------

Job submission commands, event handlers, and job poll and kill commands, are
executed by the :term:`scheduler` in a subprocess pool. The pool is size can
be configured with :cylc:conf:`global.cylc[scheduler]process pool size`.

Event handlers should be lightweight and quick-running because they tie up
a process pool member until complete, and the workflow will appear to stall if
the pool is saturated with long-running processes.

To protect the scheduler, processes are killed on a timeout
(:cylc:conf:`global.cylc[scheduler]process pool timeout`). This will be
logged by the :term:`scheduler`. If a job submission gets killed, the
associated task goes to the ``submit-failed`` state.


.. _Submitting Workflows To a Pool Of Hosts:

Submitting Workflows To a Pool Of Hosts
---------------------------------------

:Configured by: :cylc:conf:`global.cylc[scheduler][run hosts]`.

By default ``cylc play`` will run workflows on the machine where the command
was invoked.

Cylc supports configuring a pool of hosts for workflows to run on,
``cylc play`` will automatically pick a host and submit the workflow to it.

Host Pool
^^^^^^^^^

:Configured by: :cylc:conf:`global.cylc[scheduler][run hosts]available`.

The hosts must:

1. Share a common ``$HOME`` directory and therefore a common file system
   (with each other and anywhere the ``cylc play`` command is run).
2. Share a common Cylc global config (:cylc:conf:`global.cylc`).
3. Be set up to allow passwordless SSH between them.

Example:

.. code-block:: cylc

   [scheduler]
       [[run hosts]]
           available = host_1, host_2, host_3

Load Balancing
^^^^^^^^^^^^^^

:Configured by: :cylc:conf:`global.cylc[scheduler][run hosts]ranking`.

Cylc can balance the load on the configured "run hosts" by ranking them in
order of available resource or by excluding hosts which fail to meet certain
criterion.

Example:

.. code-block:: cylc

   [scheduler]
       [[run hosts]]
           available = host_1, host_2, host_3
           ranking = """
               # filter out hosts with high server load
               getloadavg()[2] < 5

               # pick the host with the most available memory
               virtual_memory().available
           """

For more information see :cylc:conf:`global.cylc[scheduler][run hosts]ranking`.

.. _auto-stop-restart:

Workflow Migration
^^^^^^^^^^^^^^^^^^

:Configured by: :cylc:conf:`global.cylc[scheduler][run hosts]condemned`.

Cylc has the ability to automatically stop workflows running on a particular
host and optionally, restart them on a different host. This can be useful if a
host needs to be taken off-line, e.g. for scheduled maintenance.

Example:

.. code-block:: cylc

   [scheduler]
       [[run hosts]]
           available = host_1, host_2, host_3
           # tell workflows on host_1 to move to another available host
           condemned = host_1

.. note::

   .. cylc-scope:: global.cylc[scheduler][main loop]

   This feature requires the :cylc:conf:`[auto restart]`
   plugin to be enabled, e.g. in the configured list of
   :cylc:conf:`plugins`.

   .. cylc-scope::

.. tip::

   If using Cylc's workflow migration functionality to implement routine
   server reboots and you have configured timeouts, e.g, a
   :cylc:conf:`workflow timeout <global.cylc[scheduler][events]workflow timeout>`
   or
   :cylc:conf:`stall timeout <global.cylc[scheduler][events]stall timeout>`,
   make sure the period between reboots is greater than the timeout
   as the timer will be reset when the workflow migrates.

For more information see: :cylc:conf:`global.cylc[scheduler][run hosts]ranking`.

.. _PlatformConfig:

Platform Configuration
^^^^^^^^^^^^^^^^^^^^^^

From the perspective of a running :term:`scheduler` ``localhost`` is the
scheduler host.

The ``localhost`` platform is configured by
:cylc:conf:`global.cylc[platforms][localhost]`.

It configures:

* Jobs that run on the ``localhost`` platform, i.e. any jobs which have
  :cylc:conf:`[runtime][<namespace>]platform=localhost` or which don't have a
  platform configured.
* Connections to the scheduler hosts (e.g. the
  :cylc:conf:`ssh command <global.cylc[platforms][<platform name>]ssh command>`).
