.. _WorkflowStartUp:

Start, Restart, Reload
======================

The ``cylc play`` command starts a new instance of the Cylc scheduler program
to manage a workflow, for the duration of the run. It also resumes paused
workflows.

There are several ways to start a workflow that is not running:

* ``cylc play`` **from the initial cycle point**

  - This is the default for a workflow that has not run yet
  - The ``initial cycle point`` is taken from ``flow.cylc`` or the command line
  - Dependence on earlier tasks is ignored, for convenience
  - (In Cylc 7, this was called a *cold start*)


* ``cylc play --start-cycle-point=POINT`` **from a later start cycle point**

  - This is an option for a workflow that has not run yet
  - The start point must be given on the command line
  - Dependence on earlier tasks is ignored, for convenience
  - The initial cycle point value defined in :cylc:conf:`flow.cylc` is preserved
  - (In Cylc 7, this was called a *warm start*)


* ``cylc play --start-task=TASK-ID`` **from any task(s) in the graph**

  - This is an option for a workflow that has not run yet
  - The start task(s) must be given on the command line
  - The flow will follow the graph onward from the start task(s)
  - (In Cylc 7, this was not possible)
  - (This makes Cylc 7 restart-from-checkpoint obsolete)


* ``cylc play`` to **restart from previous state**

  - This is automatic for a workflow that previously ran
  - The scheduler will carry on from exactly where it got to before
  - At start-up, it will automatically find out what happened to any active
    tasks that were orphaned during shutdown
  - Failed tasks are not automatically resubmitted at restart, in case the
    underlying problem has not been addressed
  - (In Cylc 7, this used the now-obsolete restart command)


.. note::

   If a workflow gets stopped or killed it can be restarted, but to avoid
   corrupting an existing run directory it cannot be started again from scratch
   (unless you delete certain files from the run directory). To start from
   scratch again, install a new copy of the workflow to a new run directory.

.. seealso::
  * :ref:`Installing-workflows`

.. _start_stop_cycle_point:

Start and Stop vs Initial and Final Cycle Points
------------------------------------------------

All workflows have an :term:`initial cycle point` and some may have a
:term:`final cycle point`. These define extent of the graph of tasks that Cylc
can schedule to run.

Start and stop cycle points, if used, define a sub-section of the graph that
the scheduler actually does run. For example:

.. code-block:: cylc

   [scheduling]
       cycling mode = integer
       initial cycle point = 1
       final cycle point = 5
       [[graph]]
           # every cycle: 1, 2, 3, 4, 5
           P1 = foo
           # every other cycle: 1, 3, 5
           P2 = bar

With a :term:`start cycle point` of ``2`` and a :term:`stop cycle point` of
``4``, the task ``foo`` would run at cycles 2, 3 & 4 and the task ``bar``
would only run at cycle ``3``.

.. image:: ../../img/initial-start-stop-final-cp.svg
   :align: center


Restarts and the Initial, Final, Start and Stop Cycle Points
------------------------------------------------------------

.. cylc-scope:: flow.cylc

When a workflow is started for the first time, the final and stop cycle points
(if either were set) are saved to the workflow database. In a restart, these
values are loaded, so the workflow will stop at the originally set cycle point,
even if :cylc:conf:`[scheduling]final cycle point` or
:cylc:conf:`[scheduling]stop after cycle point` were changed.
It is possible to override the original values using the
``--final-cycle-point`` and ``--stop-cycle-point`` options for ``cylc play``.
The new values will overwrite the old ones in the database for future restarts.

If the values were changed in ``flow.cylc``, you can pick up these changes
using a value of ``reload`` (e.g. ``--final-cycle-point=reload``).

.. note::

   If the workflow reached the final cycle point and shut down, it is finished
   and cannot be restarted; the ``--final-cycle-point`` option will have
   no effect.

The initial cycle point (and start cycle point, if set) are also saved to the
database when a workflow is started for the first time. However, the
``--initial-cycle-point`` and ``--start-cycle-point`` options cannot be used
in a restart; workflows always start from the cycle point where they
previously stopped.

.. cylc-scope::


.. _Reloading The Workflow Configuration At Runtime:

Reloading the Workflow Configuration at Runtime
-----------------------------------------------

The ``cylc reload`` command tells the target :term:`scheduler` to reload its
workflow configuration at run time. This is an alternative to shutting a
workflow down and restarting it after making changes.

.. note::
   Before reload, be sure to :ref:`reinstall <Reinstalling a workflow>` your
   changes from source to run directory


Restarting or Reloading after Graph Changes
-------------------------------------------

If dependencies have changed, tasks that were already active will spawn
children according to their original outputs. Subsequent instances will have
the new settings.

If tasks were removed from the graph, any active instances will be left to
finish, but they will not spawn children. They can be removed manually if
necessary, with ``cylc remove``.

If new tasks were added to the graph, instances will be spawned automatically
as upstream tasks complete the outputs that they depend on. If they have no
parents to do that, you can trigger the first ones manually with ``cylc trigger``.


.. _RemoteInit:

Remote Initialization
---------------------

For workflows that run on remote platforms, i.e. using a host other than
``localhost``, Cylc performs an initialization process. This involves transferring
files and directories required to run jobs, including authentication keys
(see :ref:`Authentication Files` for more information).

Directories included, as standard, in the remote install are:

* ``app``
* ``bin``
* ``etc``
* ``lib``

These will be transferred from the workflow run directory on the :term:`scheduler`.
In addition, file and directories configured in :cylc:conf:`[scheduler]install`
of the ``flow.cylc`` will be included in the transfer. See :ref:`installing_files`
for an example.

This remote initialization process also creates symlinks on the remote
platform, if these are configured using
:cylc:conf:`global.cylc[install][symlink dirs]`. Using this functionality is an
efficient way to manage disk space.

Troubleshooting
^^^^^^^^^^^^^^^

There are certain scenarios where remote initialization may fail. Cylc will return
a ``REMOTE INIT FAILED`` message.

Timeout
"""""""

Remote initialization has a timeout set at 10 minutes, after which remote
initialization will fail. If you have particularly large files files to
transfer, which you expect to exceed the 10 minute timeout, consider using an
install task in your workflow.

Misconfiguration
""""""""""""""""

Platforms must be correctly configured to ensure authentication keys, which are
responsible for secure communication between the :term:`scheduler` and the
platform, are correctly in place.
Sites can configure these platforms, insuring they match up with the correct
install target. Cylc uses install targets as a way of recognising which platforms
share the same file system. For more information, see :ref:`Install Targets`.


Files created at workflow start
-------------------------------

Configuration Logs
^^^^^^^^^^^^^^^^^^

A folder ``log/flow-config`` is created where the workflow configuration
is recorded, with all templating expanded:

- ``flow-processed.cylc`` - A record of the current workflow configuration
  with templating expanded, but without being fully parsed: Duplicate sections
  will not be merged.
- ``<datetime-stamp>-<start/restart/reload>`` - A record of the config at
  the time a workflow was started, restarted or reloaded, parsed by Cylc:
  Duplicate sections will be merged.

.. note::

   These are particularly useful files to look at if the workflow
   configuration contains many template variables, to see how they are
   filled in.


.. _The Workflow Contact File:

The Workflow Contact File
^^^^^^^^^^^^^^^^^^^^^^^^^

The :term:`scheduler` writes a :term:`contact file` at
``$HOME/cylc-run/<workflow-name>/.service/contact`` that records workflow host,
user, port number, process ID, Cylc version, and other information. Client
commands read this file to find the :term:`scheduler`.

The contact file gets removed automatically at shutdown (assuming the
scheduler shuts down cleanly).


Authentication Files
^^^^^^^^^^^^^^^^^^^^

See :ref:`Authentication Files`.
