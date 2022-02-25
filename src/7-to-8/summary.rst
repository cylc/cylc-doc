.. _overview:

Quick Summary Of Changes
========================


Terminology
-----------

Cylc now uses simpler more widely understood terms for several core concepts.

.. table::

   =============     ==============
   Cylc 7 Term       Cylc 8 Term
   =============     ==============
   suite             **workflow**
   batch system      **job runner**
   suite daemon      **scheduler**
   =============     ==============

The workflow configuration file has changed from ``suite.rc`` to ``flow.cylc``.


Cylc 7 Compatibility Mode
-------------------------

The old ``suite.rc`` filename triggers a :ref:`backward
compatibility mode<cylc_7_compat_mode>` in Cylc 8 which supports Cylc 7
workflow configurations out of the box. There are certain scenarios to be aware of
if using backward compatibility mode, these are documented here:
:ref:`major-changes-compatibility-caveats`.


Upgrading To Cylc 8
-------------------

To upgrade your Cylc 7 suite to a Cylc 8 workflow, run ``cylc validate``. Take
action on any warnings then rename the workflow configuration file from
``suite.rc`` to ``flow.cylc``.

.. TODO Add ref to breaking changes section within Major changes, once created,
   including optional ouputs.

New Web and Terminal UIs
------------------------

At Cylc 8, there are two UIs available to view your workflows:

- a terminal UI application

   .. code-block:: bash

      cylc tui <workflow_id>

- a web based UI application (requires `Cylc UI Server`_)

   .. code-block:: bash

      cylc gui

For more information on how the UI displays the workflow, see :ref:`n-window`.

.. TODO - Add link to more detailed gui instructions.

Task/Job States
---------------

:term:`Tasks <task>` are nodes in the abstract workflow graph,
a :term:`Job <job>` is an instance of a task. A task can have
multiple jobs as the result of automatic retries or manual re-triggering.


The 13 task/job states in Cylc 7 have been simplified to 8 and can be viewed
in the GUI.

.. image:: ../img/task-job.png
   :align: center

For more information, see :ref:`728.task_job_states`.


Scheduling Algorithm
--------------------

The scheduling algorithm has been changed, more information is available:
:ref:`728.scheduling_algorithm`.

Optional and Expected Task Outputs
----------------------------------

.. seealso::

   User Guide:

   * :ref:`User Guide Expected Outputs`
   * :ref:`User Guide Optional Outputs`

   Major Changes:

   * :ref:`728.suicide_triggers`

Unless it configured otherwise, at Cylc 8, all tasks are assumed to be
required to complete, this is the :term:`expected output <expected output>`.
If they do not complete, they are marked as an :term:`incomplete
task` and user intervention is required. If there is nothing left to do, the
scheduler will :term:`stall` rather than shut down.

Alternatively, task outputs can be marked as :term:`optional <optional output>`.
This supports optional :term:`graph branching` and it allows the scheduler to
correctly diagnose :term:`workflow completion`.

Platforms
---------

.. seealso::

   - :ref:`Platforms at Cylc 8. <majorchangesplatforms>`
   - :ref:`System admin's guide to writing platforms. <AdminGuide.PlatformConfigs>`

At Cylc 7 job hosts were defined to indicate where a job should run, at Cylc 8
use Platforms.

.. code-block:: diff

     [runtime]
        [[model]]
   -        [[[remote]]]
   -            host = hpc1.login.1
   +        platform = hpc1


.. _7-to-8.summary.graph_syntax:

Configuration Changes
---------------------

Cylc 7 had unnecessarily deep nesting of graph config sections:

.. code-block:: cylc

   [scheduling]
      initial cycle point = now
      [[dependencies]]  # Deprecated Cylc 7
          [[[R1]]]
              graph = "prep => foo"
          [[[R/^/P1D]]]
              graph = "foo => bar => baz"

Cylc 8 cleans this up:

.. code-block:: cylc

   [scheduling]
      initial cycle point = now
      [[graph]]  # Cylc 8
          R1 = "prep => foo"
          R/^/P1D = "foo => bar => baz"


Rose Suite-Run Migration
------------------------

The functionality of ``rose suite-run`` has been migrated into Cylc 8.

Cylc Install
^^^^^^^^^^^^
.. seealso::

   * :ref:`Moving to Cylc Install<majorchangesinstall>`.

Cylc install cleanly separates workflow :term:`source directory` from
:term:`run directory`. It installs workflow files ready for ``cylc play``.

.. code-block:: console

   $ pwd
   ~/cylc-src/demo

   $ ls
   flow.cylc

   $ cylc install
   INSTALLED demo/run1 from /home/oliverh/cylc-src/demo

   $ cylc play demo
   ...
   demo/run1: oliver.niwa.local PID=6702

By default, run numbers increment with each install.


File Installation
^^^^^^^^^^^^^^^^^
When the first job runs on a remote platform, a remote initialization process 
is triggered which will install files onto platforms.

Symlink Dirs
^^^^^^^^^^^^

.. seealso::

   * :ref:`SymlinkDirs`
   * :ref:`RemoteInit`

Symlinking the workflow directories used by Cylc provides a useful way of
managing disk space.

These symlinks are created on a per install target basis, as configured in
:cylc:conf:`global.cylc[install][symlink dirs]`. Install targets are managed on
a site level, for more information see :ref:`Install Targets`.

This functionality replaces the Rose ``root dir`` configuration
for Cylc 7 (however, note it does not allow per-workflow configuration).


Removing Workflows
------------------

Workflows can be deleted with ``cylc clean`` - see :ref:`Removing-workflows`. This
replaces the ``rose suite-clean`` functionality.


Restart Behaviour
-----------------
.. seealso::

   - User Guide :ref:`WorkflowStartUp`
   - Major Channges :ref:`728.play_pause_stop`

At Cylc 8, use ``cylc pause <workflow_id>`` to pause a workflow, halting all job
submission. To restart this workflow, use ``cylc play <workflow_id>``.

To start a fresh run, use ``cylc install`` and play it safely in the new run
directory.

(Note that ``cylc hold`` and ``cylc release`` pause and release individual tasks.)


Architecture
------------

There have been fundamental changes to the architecture of Cylc. You can read
about the new system design here :ref:`architecture-reference`.


Other Minor Changes
-------------------

There are an assortment of other features implemented at Cylc 8. Some noteworthy
minor changes include:

- Runahead Limit
   The default runahead limit has been increased from three cycles to five.
- Queues
   :ref:`InternalQueues` are now more efficient (for the :term:`scheduler`),
   we now recommend using queues to restrict the number of running tasks in
   situations where graphing may have been used previously.
- Time Zones
   :cylc:conf:`[scheduler]cycle point time zone` now defaults to UTC, unless you
   are working in :ref:`cylc_7_compat_mode`.
- Task Job Scripts
   All user-defined task scripting now runs in a subshell, so you can safely
   switch Python environments inside tasks without affecting Cylc.
   Further information is available in the User Guide :ref:`JobScripts`.
