.. _728.overview:

Summary Of Major Changes
========================

Terminology
-----------

Cylc now uses more widely understood terms for several core concepts.

.. table::

   =============     ==============
   Cylc 7 Term       Cylc 8 Term
   =============     ==============
   suite             *workflow*
   batch system      *job runner*
   suite daemon      *scheduler*
   ``suite.rc``      ``flow.cylc``
   =============     ==============

Note the configuration filename is now ``flow.cylc``, not ``suite.rc``.

Cylc 7 Compatibility Mode
-------------------------

Continuing to use the old ``suite.rc`` filename triggers a :ref:`backward
compatibility mode<cylc_7_compat_mode>` in Cylc 8 which supports Cylc 7
workflow configurations out of the box, with
:ref:`some caveats <compat_required_changes>`. However, to future-proof
your workflow and take full advantage of Cylc 8 you should upgrade to Cylc 8 syntax.

Upgrading To Cylc 8
-------------------
.. seealso::

   * Major Changes: :ref:`configuration-changes`
   * Major Changes: :ref:`cylc_7_compat_mode`

There have been some configuration changes at Cylc 8.
To upgrade your Cylc 7 suite to a Cylc 8 workflow, first make sure it validates
in Cylc 7 without any warnings, you can now run it in compatibility mode.

To upgrade the workflow to run without compatibility mode, rename the workflow
configuration file from ``suite.rc`` to  ``flow.cylc``, run ``cylc validate``
in Cylc 8 and take action on any warnings.

.. TODO Add ref to breaking changes section within Major changes, once created,
   including optional ouputs.

.. note::

   Validation warnings use a :ref:`shorthand notation<config_item_shorthand>`
   to refer to nested configuration settings on a single line, like this:
   ``[section][sub-section]item``.


New Web and Terminal UIs
------------------------
.. seealso::

   * Major Changes: :ref:`728.ui`

At Cylc 8, there are two UIs available to monitor and control your workflows:

- a terminal UI application

   .. code-block:: bash

      cylc tui <workflow_id>

- a web based UI application (requires `Cylc UI Server`_)

   .. code-block:: bash

      cylc gui <workflow_id>

Command Changes
---------------

``cylc run <suite_name>`` has become ``cylc play <workflow_id>``.

``rose suite-run`` is now ``cylc vip`` (**V**\ alidate, **I**\ nstall, **P**\ lay).

.. seealso::

   * User Guide: :ref:`WorkflowStartUp`
   * Major Changes: :ref:`728.play_pause_stop`
   * Major Changes: :ref:`MajorChangesCLI`

At Cylc 8, use ``cylc pause <workflow_id>`` to pause a workflow, preventing new
job submissions. To restart the workflow, use ``cylc play <workflow_id>``.

To start a fresh run, use ``cylc install`` and play it safely in the new run
directory.

(Note that ``cylc hold`` and ``cylc release`` pause and release individual tasks.)

Task/Job States
---------------

:term:`Tasks <task>` are nodes in the abstract workflow graph, representing
applications to run at the appropriate point in the workflow.

A :term:`job <job>`
is the script (and subsequent process) submitted by Cylc to
actually run the application. A task can have multiple jobs as the result of
automatic retries or manual re-triggering.

The 13 task/job states in Cylc 7 have been simplified to 8. Tasks and jobs have been
separated and states of both can be viewed in the GUI.

.. image:: ../img/task-job.png
   :align: center

For more information, see :ref:`728.task_job_states`.


Optional and Required Task Outputs
----------------------------------

.. seealso::

   * Major Changes::ref:`728.optional_outputs`
   * User Guide::ref:`User Guide Required Outputs`
   * User Guide::ref:`User Guide Optional Outputs`

By default, all Cylc 8 tasks are required to succeed - i.e., success is
a :term:`required output`. Otherwise they will be marked
as :term:`incomplete tasks<incomplete task>` needing user intervention.
In a workflow with incomplete tasks, if there is nothing left to do, the
scheduler will :term:`stall` rather than shut down.

Alternatively, task outputs can be marked as :term:`optional <optional output>`.
This supports :term:`graph branching` and it allows the scheduler to
correctly diagnose :term:`workflow completion`.

Platform Awareness
------------------

.. seealso::

   :ref:`Platforms at Cylc 8.<majorchangesplatforms>`

Cylc 7 was aware of individual job hosts - one selected a host using:
``[runtime][<namespace>][remote]host``.

Cylc 8 is aware of sets of host settings called
:term:`[job] platforms <platform>`. To choose a platform for a task use
``[runtime][<namespace>]platform``

Hosts of a platform must share a file system and :term:`job runner`:
If one host is unavailable Cylc 8 can use other hosts
on the same platform to interact with jobs.

The same hosts can belong to multiple platforms, for example
you might be able to use the same host to launch both background and Slurm
jobs.

.. note::

   Cylc 8 will pick a sensible platform for your Cylc 7 settings,
   These deprecated settings will be removed in a future release.


Workflow Installation
---------------------

Cylc 8 supports workflow installation.

For users of `Rose`_, this replaces the functionality of ``rose suite-run``.

Cylc Install
^^^^^^^^^^^^

.. seealso::

   * Major Changes: :ref:`Moving to Cylc Install<majorchangesinstall>`

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
When the first job runs on a remote platform (after start-up, or after a ``cylc reload``), a
remote initialization process is triggered to install workflow files there.

Symlink Dirs
^^^^^^^^^^^^

.. seealso::

   * User Guide: :ref:`SymlinkDirs`
   * User Guide: :ref:`RemoteInit`

Symlinking the workflow directories used by Cylc provides a useful way of
managing disk space.

These symlinks are created on a per install target basis, as configured in
:cylc:conf:`global.cylc[install][symlink dirs]`. Install targets are managed on
a site level, for more information see :ref:`Install Targets`

This functionality replaces the Rose ``root dir`` configuration
for Cylc 7 (however, note it does not allow per-workflow configuration).


Removing Workflows
------------------

Workflows can be deleted with ``cylc clean`` - see :ref:`Removing-workflows`. This
replaces the ``rose suite-clean`` functionality.

Architecture
------------

There have been fundamental changes to the architecture of Cylc. You can read
about the new system design here :ref:`architecture-reference`.

Scheduling Algorithm
--------------------

The scheduling algorithm has been changed, more information is available:
:ref:`728.scheduling_algorithm`.

Other Changes
-------------

There are an assortment of other features implemented at Cylc 8. Some noteworthy
minor changes include:

Runahead Limit
   The default runahead limit has been increased from three cycles to five.
Queues
   :ref:`InternalQueues` are now more efficient (for the :term:`scheduler`),
   we now recommend using queues to restrict the number of running tasks in
   situations where graphing may have been used previously.
Time Zones
   :cylc:conf:`[scheduler]cycle point time zone` now defaults to UTC, unless you
   are working in :ref:`cylc_7_compat_mode`.
Job Scripts
   All user-defined task scripting now runs in a subshell, so you can safely
   switch Python environments inside tasks without affecting Cylc.
   Further information is available in the User Guide: :ref:`JobScripts`.
Packaging
   Cylc 8 (and its package dependencies) is now available from Conda Forge and PyPI
   for installations into a Python 3 virtual environment.
Remote usernames
   If usernames differ on remote job hosts they must now be configured using
   an SSH config file rather than the via Cylc 7 ``[remote]owner`` configuration.
   See :ref:`728.remote_owner`.
