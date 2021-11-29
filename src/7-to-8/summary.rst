.. _overview:

Quick Summary Of Changes
========================

Terminology
-----------

- **Suite** is now **WORKFLOW** (a more widely understood term)
- **Suite daemon** (or **suite server program**) is now **SCHEDULER** (ditto)
- **Batch system** is now **JOB RUNNER** (not all of our job runners are "batch
  systems")
- The **workflow config filename** is now ``flow.cylc``, not ``suite.rc``

.. important::
   Attempting to ``cylc play`` a workflow with both ``flow.cylc`` and
   ``suite.rc`` files in the same :term:`run directory` will result in an error.

.. _Cylc_7_compat_mode:

Backward Compatibility
----------------------

:term:`Workflow validation` warns of deprecated Cylc 7 syntax. If your Cylc 7
workflow *fails* validation in Cylc 8, see :ref:`AutoConfigUpgrades` to learn
how to fix this.

.. warning::

   Please take action on deprecation warnings from ``cylc validate`` before
   renaming your ``suite.rc`` file to ``flow.cylc``.

Before upgrade, Cylc 8 can run Cylc 7 workflows out of the box. The old
``suite.rc`` filename triggers a backward compatibility mode in which:

- :term:`implicit tasks <implicit task>` are allowed by default

  - (unless a ``rose-suite.conf`` file is found in the :term:`run directory`)
  - (by default, Cylc 8 does not allow implicit tasks)

- :term:`cycle point time zone` defaults to the local time zone

  - (by default, Cylc 8 defaults to UTC)

- waiting tasks are pre-spawned to mimic the Cylc 7 scheduling algorithm and
  stall behaviour, and these require :term:`suicide triggers <suicide trigger>` for
  alternate path :term:`branching <graph branching>`

  - (Cylc 8 spawns tasks on demand and suicide triggers are not needed for branching)

- task ``succeeded`` outputs are *required* so the scheduler will retain failed
  tasks as incomplete

  - (in Cylc 8, all outputs are *required* unless marked as optional by new ``?`` syntax)


.. warning::

   Cylc 8 cannot *restart* a Cylc 7 workflow mid-run. Instead, :ref:`install
   <Workflow Installation>` the workflow to a new run directory and start it
   from scratch at the right cycle point or task(s):

   - ``cylc play --start-cycle-point=<CYCLEPOINT>`` (c.f. Cylc 7 *warm start*), or
   - ``cylc play --start-task=<TASKNAME.CYCLEPOINT>`` (Cylc 8 can start anywhere in the graph)

   Any previous-cycle workflow data needed by the new run will need to be
   manually copied over from the original run directory.


Architecture
------------

The main Cylc system components are:

- **Cylc Scheduler**
     - The workflow engine core, Python 3 based
     - Includes the **CLI** (Command Line Interface)
     - And **TUI**, a new Terminal UI application

- **Cylc Hub**
   - Authenticates users, spawns and proxies Cylc UI Servers
   - Can run as a regular or privileged user
   - (Is a `Jupyterhub <https://jupyter.org/hub>`_ instance)

- **Cylc UI Server**
   - Interacts with Schedulers and the filesystem
   - Serves the UI to users
   - Can be launched by the privileged Hub, for multi-user installations
   - Or run standalone for use by a single user
   - (Is a `Jupyter Server <https://jupyter-server.readthedocs.io>`_ extension)

- **Cylc UI**
   - In-browser web UI, includes:
   - A dashboard with summary information and documentation links
   - Integrated gscan (multi-workflow) side-panel
   - Responsive web design (from desktop to table to mobile)
   - Tabbed interface to display multiple workflow views
   - Command integration for interacting with task, jobs, and schedulers

- **Network layers**
   - Incremental push updates (c.f. polled full-state updates in Cylc 7)

.. figure:: ../img/hub.png
   :figwidth: 100%
   :align: center

   Cylc 8 Hub authentication page

.. figure:: ../img/cylc-ui-dash.png
   :figwidth: 100%
   :align: center

   Cylc 8 UI dashboard

.. figure:: ../img/cylc-ui-tree.png
   :figwidth: 100%
   :align: center

   Cylc 8 UI workflow tree view

.. figure:: ../img/cylc-tui.png
   :figwidth: 100%
   :align: center

   Cylc 8 TUI application

Scheduling Algorithm
--------------------

Cylc can manage infinite workflows of repeating tasks:

.. image:: ../img/cycling.png
   :align: center

Cylc 8 has an efficient new scheduling algorithm that:
   - Spawns new tasks on demand
   - Handles alternate path branching without suicide triggers
   - Distinguishes between *optional* and *expected* task outputs. If a tasks
     finishes without completing an expected output it will be retained by the
     scheduler as an *incomplete task*
   - Can run tasks out of cycle point order
   - Provides a sensible active-task based window on the evolving workflow
   - Supports a powerful new capability called **reflow**: you can trigger
     multiple fronts of activity in the graph at once, in the same scheduler

See also:

   * :ref:`Cylc 7 Scheduler Deficiencies Fixed by Cylc 8`


Task/Job Separation
-------------------

**Tasks** are nodes in the abstract workflow graph representing processes
that should run once their prerequisites are satisfied. **Jobs** are the real
processes submitted to execute these tasks (or at least, at the submission
stage, real job scripts). A task can have multiple jobs, by automatic retries
and manual re-triggering.

Cylc 7 had 13 task/job states. The GUI only showed tasks, with job data
from the latest task job.

Cylc 8 has only 8 task/job states. The Cylc 8 UI shows both task and jobs.
Task icons are monochrome circles; job icons are coloured squares. The running
task icon incorporates a radial progress indicator.

.. image:: ../img/task-job.png
   :align: center

The task states removed since Cylc 7 have been absorbed into *waiting*, but
you can see or infer what is being waited on: e.g. a queue, xtrigger, or retry
timer. For instance, a waiting task that already has associated jobs is going
to retry.


Optional and Expected Task Outputs
----------------------------------

Cylc 8 distinguishes between :term:`expected <expected output>` and
:term:`optional <optional output>` task outputs. This supports optional
:term:`graph branching` and it allows the scheduler to diagnose :term:`workflow
completion` properly.

If a task :term:`job` finishes without completing an expected output the
scheduler will retain it, pending user intervention, as a :term:`incomplete
task`.

A task can finish with or without completing optional outputs, on the other
hand. The primary use for optional outputs is alternate path branching in the
graph.

If there is nothing left to do, but incomplete tasks are present, the scheduler
will conclude that the workflow did not run to completion as expected and will
:term:`stall` rather than shut down.

.. seealso::
   * :ref:`Cylc User Guide <User Guide Optional Outputs>`


Window on the Workflow
----------------------

.. image:: ../img/n-window.png
   :align: center

The Cylc UI can't show "all the tasks" at once because the graph may be huge,
or even infinite in extent in cycling systems. The Cylc 8 UI shows:

- current **active tasks** (submitted, running) plus tasks waiting on scheduler
  constraints (queues, runahead limit, clock triggers) and external triggers

- tasks up to ``n`` graph edges away from active tasks (default ``1`` edge)

Platform Awareness
------------------

.. seealso::

   - :ref:`Platforms at Cylc 8. <majorchangesplatforms>`
   - :ref:`System admin's guide to writing platforms. <AdminGuide.PlatformConfigs>`

Cylc 7 was aware of individual job hosts.

.. code-block:: cylc

   [runtime]
      [[model]]
          [[[remote]]]
              host = hpc1.login.1  # Deprecated Cylc 8

Cylc 8 is aware of host groups specified as :term:`[job] platforms <platform>`
in the global configuration. Platform hosts share a file system and :term:`job
runner`. If a host becomes unavailable Cylc 8 can use other hosts on the same
platform to interact with task jobs.

.. code-block:: cylc

   [runtime]
      [[model]]
          platform = hpc1  # Cylc 8
          # (Platform hosts and job runner defined in global config).
      [[model_cleanup]]
          # Platforms can have the same hosts with different job runners.
          platform = hpc1_background


.. warning::

   Cylc 8 will pick a sensible platform for your Cylc 7 settings,
   These deprecated settings will be removed at Cylc 9.


.. _7-to-8.summary.graph_syntax:

Graph Syntax
------------

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

.. _Workflow Installation:

Workflow Installation
---------------------

The functionality of ``rose suite-run`` has been migrated into Cylc 8.

Cylc Install
^^^^^^^^^^^^
Cylc install cleanly separates workflow source directory from run directory,
and installs workflow files into the run directory at start-up.
- ``cylc install`` copies workflow source files to a dedicated run-directory
- :term:`source directory` locations can be set in global config
- each install creates a new numbered :term:`run directory` (by default)

.. seealso::

   :ref:`Moving to Cylc Install<majorchangesinstall>`.

.. code-block:: bash

   $ pwd
   ~/cylc-src/demo

   $ ls
   flow.cylc

   $ cylc install
   INSTALLED demo/run1 from /home/oliverh/cylc-src/demo

   $ cylc play demo
   ...
   demo/run1: oliver.niwa.local PID=6702

   $ cylc install
   INSTALLED demo/run2 from /home/oliverh/cylc-src/demo

   $ cylc play demo
   ...
   demo/run2: oliver.niwa.local PID=6962

Workflows can be deleted with ``cylc clean`` - see :ref:`Removing-workflows`. This
replaces the ``rose suite-clean`` functionality.

.. note::

   Cylc 8 forbids having both ``flow.cylc`` and ``suite.rc`` files in the same
   :term:`run directory` or :term:`source directory`.

File Installation
^^^^^^^^^^^^^^^^^

As part of the ``rose suite-run`` migration to Cylc, files are now installed onto
platforms. This is part of the remote initialization process which is triggered
when the first job runs on the platform.
The remote installation, as standard, includes the directories ``app``, ``bin``,
``etc`` and ``lib``. Extra files and directories can be included in this file
installation, under the :cylc:conf:`[scheduler]install` section of your
``flow.cylc`` file.

For more information, see :ref:`installing_files`.

Symlink Dirs
^^^^^^^^^^^^

Symlinking the directories used by Cylc provides a useful way of managing disk
space. This functionality was previously available with the Rose ``root dir``
configuration but has now been implemented in Cylc 8.
Directories available for symlinking are:

* ``run``
* ``log``
* ``share``
* ``share/cycle``
* ``work``

These are created on a per install target basis, as configured in
:cylc:conf:`global.cylc[install][symlink dirs]`. Install targets are managed on
a site level, for more information see :ref:`Install Targets`.

See also:

* :ref:`RemoteInit`


Safe Run Semantics
------------------

Cylc 7 run semantics were somewhat dangerous: if you accidentally typed ``cylc run``
instead of ``cylc restart`` a new run from scratch would overwrite the existing
run directory, preventing a return to the intended restart.

Cylc 8 has ``cylc pause`` to:

- pause a workflow (halt all job submission)

And ``cylc play`` to:

- start,
- restart, and
- release a paused workflow

So *restart* is now the safe default behaviour. For a new run from scratch,
do a fresh ``cylc install`` and play it safely in the new run directory.

(Note that ``cylc hold`` and ``cylc release`` pause and release individual tasks.)


Security
--------

- In a multi-user context, users authenticate at the Hub, which
  spawns Cylc UI Servers as the target user (workflow owner).
- In a single user context, the UI Server can be started directly,
  with token-based authentication.
- The UI Server interacts with its own Schedulers, which also run as the user.
- Users can authorize different levels of access to others, via their UI Server.
- Workflow task jobs authenticate to their parent scheduler using `CurveZMQ`_.
- Cylc8 supports target users authorizing other users to interact with their
  workflows on the UI.

See :ref:`System admin's guide to writing platforms. <AdminGuide.PlatformConfigs>`


.. note::

   The authorization system in Cylc 8 is complete but we haven't yet provided easy
   access to other users' workflows via the UI.

Packaging
---------

Cylc 7 had to be installed from a release tarball, and its software dependencies
had to be installed manually.

Cylc 8 and its core software dependencies can be installed quickly from Conda
Forge, into a conda environment; or from PyPI, into a Python 3 virtual environment.

See also:

* :ref:`Cylc UI Server <CylcUIServer.architecture>`


Time Zones
----------

:cylc:conf:`[scheduler]cycle point time zone` now defaults to UTC, unless you
are working in :ref:`Cylc 7 compatibility mode <Cylc_7_compat_mode>`.

.. seealso:: :ref:`Scheduling syntax rules<writing_flows.scheduling.syntax_rules>`

.. _Cylc 7 Scheduler Deficiencies Fixed by Cylc 8:

Cylc 7 Scheduler Deficiencies Fixed by Cylc 8
----------------------------------------------

- Every task implicitly depended on previous-instance (same task, previous
  cycle point) job submission
- The scheduler had to be aware of at least one active and one waiting
  cycle point instance of every task in the workflow, plus all succeeded tasks
  in the current active task window
- The indiscriminate dependency matching process was costly
- To fully understand what tasks appeared in the GUI (why particular
  *waiting* or *succeeded* tasks appeared in some cycles but not in others, for
  instance) you had to understand the scheduling algorithm
- *Suicide triggers* were needed to clear unused graph paths and avoid
  stalling the scheduler
- Tasks could not run out of cycle point order
- The scheduler could stall with next-cycle-point successors not spawned
  downstream of failed tasks
