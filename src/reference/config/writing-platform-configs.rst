
.. _AdminGuide.PlatformConfigs:

Platform Configuration
======================

Writing Platform Configurations
-------------------------------

.. versionadded:: 8.0.0

.. seealso::

   - :ref:`Platforms Cylc 7 to 8 user upgrade guide <MajorChangesPlatforms>`.
   - :cylc:conf:`flow.cylc[runtime][<namespace>]platform`
   - :cylc:conf:`global.cylc[platforms]`
   - :cylc:conf:`global.cylc[platforms][<platform name>]install target`

.. _ListingAvailablePlatforms:

Listing available platforms
^^^^^^^^^^^^^^^^^^^^^^^^^^^

If you are working on an institutional network, platforms may already
have been configured for you.

To see a list of available platforms::

   cylc config --platform-names

To see the full configuration of available platforms::

   cylc config --platforms

This is equivalent to ``cylc config -i 'platforms' -i 'platform groups'``

What Are Platforms?
^^^^^^^^^^^^^^^^^^^

Platforms define settings, most importantly:

 - A set of ``hosts``.
 - A ``job runner`` (formerly a ``batch system``) where Cylc can submit a
   task job.
 - An ``install target`` for Cylc to install task job files on.

Why Were Platforms Introduced?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- Allow a compute cluster with multiple login nodes to be treated as a single
  unit.
- Allow Cylc to elegantly handle failure to communicate with login nodes.
- Reduce the number of ssh connections required for job submission and polling.

.. _Install Targets:

What Are Install Targets?
^^^^^^^^^^^^^^^^^^^^^^^^^

Install targets represent file systems. More than one platform can use the
same file system. Cylc relies on the site configuration file ``global.cylc`` to determine
which platforms share install targets.

Cylc will setup each remote install target once. During setup it will:

  - Install workflow files
  - Symlink directories
  - Copy authentication keys (to allow secure communication)

Note, if missing from configuration, the install target will default to the
platform name. If incorrectly configured, this will cause errors in
:ref:`RemoteInit`.

If you log into one system and see the same files as on another, then these two
platforms will require the same install target in ``global.cylc`` config file.

Example Platform Configurations
-------------------------------

Detailed below are some examples of common platform configurations.

Submit PBS Jobs from Localhost
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- **The** :term:`scheduler` **runs on the** ``localhost`` **platform.**
- **Platforms can share hosts without sharing job runners.**

.. admonition:: Scenario

   You have a cluster where you can submit jobs from the Cylc scheduler host
   using PBS.

The ``localhost`` platform is the Cylc Scheduler host, as configured in
:cylc:conf:`global.cylc[scheduler][run hosts]available`. This is the host that
the workflow will start on. For more information, see
:ref:`Platform Configuration<PlatformConfig>`.

Our platform ``pbs_cluster`` shares this ``localhost`` host and setting the
install target to ``localhost`` ensures that Cylc knows this platform does not
require remote initialization.

.. code-block:: cylc
   :caption: part of a ``global.cylc`` config file

   [platforms]
       # The localhost platform is available by default
       # [[localhost]]
       #     hosts = localhost
       #     install target = localhost
       [[pbs_cluster]]
           hosts = localhost
           job runner = pbs
           install target = localhost

Our Cylc scheduler does not have a job runner defined. Any job submitted to
this ``localhost`` platform will run as a background job. Users can now set 
:cylc:conf:`flow.cylc[runtime][<namespace>]platform` = ``pbs_cluster`` to run
pbs jobs.

.. note::

   Both ``hosts`` and ``install target`` default to the platform name.

Multiple Platforms Sharing File System with Cylc Scheduler
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- **Platform names can be defined as regular expressions.**

.. admonition:: Scenario

   Everyone in your organization has a computer called ``desktopNNN``,
   all with a file system shared with the scheduler host. Many users
   will want their desktop set up as a platform to run small jobs.

In this scenario, Cylc does not need to install files on the desktop, since
required files which are on the scheduler host will be accessible on the
desktop. From Cylc's point of view, the desktop and scheduler hosts are
considered different platforms but must share an :term:`install target`.
Cylc needs to be told that these platforms share an install target and so we
configure this using the designated configuration item:
:cylc:conf:`global.cylc[platforms][<platform name>]install target`.

:cylc:conf:`global.cylc[platforms][<platform name>] has optional configuration 
``[[[meta]]]`` which users can view with ``cylc config --platforms``. We will add
a description designed to help users in this example.

The following platform definition is simplified, taking advantage of defaults
for ``hosts`` and ``install targets``.

.. code-block:: cylc
   :caption: the ``global.cylc`` config file for this scenario could look like:

   [platforms]
       [[desktop\d\d\d]]
           install target = localhost
           [[[meta]]]
               description = "Background job on a desktop system"

As before, a ``localhost`` platform is available by default.
``desktop\d\d\d`` is a pattern which defines multiple platforms.
When using a pattern the "hosts" setting must be left unset so that it defaults
to the platform name. This ensures each of the matching platforms is unique.

.. note::

   Cylc carries out a "fullmatch" regular expression comparison with the
   the platform name so ``desktop\d\d\d`` is effectively the same as
   ``^desktop\d\d\d$``.

If a user wants to run a job on their local desktop, e.g. "desktop123", they should
set:

   .. code-block:: cylc

      [runtime]
          [[mytask]]
              platform = desktop123

in their workflow configuration.
If ``[runtime][mytask]platform`` is unset, the job will run on the Cylc
Scheduler host using this default ``localhost`` platform.

Neither platforms will require remote initialization as the ``install target``
is set to ``localhost``.

Cluster with Multiple Login Nodes
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- **Platforms with multiple hosts require job runner to be set**
- **Platforms can group multiple hosts together.**

.. admonition:: Scenario

   You have a cluster where users submit jobs to Slurm from
   either of a pair of identical login nodes which share a file system.

.. code-block:: cylc
   :caption: part of a ``global.cylc`` config file

   [platforms]
       [[slurm_cluster]]
           hosts = login_node_1, login_node_2
           job runner = slurm
           retrieve job logs = True

The ``slurm_cluster`` hosts do not share a file system with the scheduler,
therefore ``slurm_cluster`` is a remote platform.
As the ``install target`` setting for each platform has been omitted, this will
default to the platform name.
Cylc will initiate a remote installation, to transfer required files to
``slurm_cluster`` which will commence before job submission for the first job
on that platform.

Cylc will attempt to communicate with jobs via the other login node if either
of the login_nodes becomes unavailable.

With multiple hosts defined under ``slurm_cluster``, a job runner is required.

.. note::

   The "background" and "at" job runners require single-host platforms,
   because the job ID is only valid on the submission host.

We have set ``retrieve job logs = True``. This will ensure our job logs are
fetched from the ``slurm_cluster`` platform. This setting is recommended for
all remote platforms (i.e. where install target is not localhost).


Grouping Platforms
^^^^^^^^^^^^^^^^^^

- **Platform groups allow users to ask for jobs to be run on any
  suitable computer.**

.. admonition:: Scenario

   Extending the example from above, we now wish to set the ``slurm_cluster``
   up such that ``slurm_cluster`` nodes can accept background jobs.
   We would like to group these background platforms together so users can set
   :cylc:conf:`flow.cylc[runtime][<namespace>]platform` = ``slurm_cluster_bg``.

.. code-block:: cylc
   :caption: part of a ``global.cylc`` config file

   [platforms]
       [[slurm_cluster, slurm_cluster_bg1, slurm_cluster_bg2]]  # settings that apply to all:
           install target = slurm_cluster
           retrieve job logs = True
       [[slurm_cluster]]
           batch system = slurm
           hosts = login_node_1, login_node_2
       [[slurm_cluster_bg1]]
           hosts = login_node_1
       [[slurm_cluster_bg2]]
           hosts = login_node_2
       [platform groups]
           [[slurm_cluster_bg]]
               platforms = slurm_cluster_bg1, slurm_cluster_bg2

Group platforms together using the configuration item
:cylc:conf:`global.cylc[platform groups]`. In the above example, the
``slurm_cluster_bg`` platforms all share a file system
(install target = ``slurm_cluster``). We advise caution when grouping platforms
with different install targets as users could encounter a scenario whereby
files (created by a previous task using the same platform group) are
not available to them.

With the above configuration, users can now run background jobs on either of
the login nodes, without the concern of selecting a specific platform.

.. warning::

   Platforms and platform groups are both configured by
   :cylc:conf:`flow.cylc[runtime][<namespace>]platform`.
   Therefore a platform group cannot be given the same name as a platform.
   The :cylc:conf:`global.cylc` file will fail validation if the same name is
   used for both.


.. _SymlinkDirsSetup:

Symlinking Directories
----------------------
To minimize the disk space used by ``~/cylc-run``, set
:cylc:conf:`global.cylc[install][symlink dirs]`.
The entire workflow directory can be symlinked, using the config item ``run`` 
The following sub-directories  are also available for configuration:

   * log
   * share
   * share/cycle
   * work

These should be configured per :term:`install target`.

For example, to configure workflow ``log`` directories (on the
:term:`scheduler` host) so that they symlink to a different location,
you could write the following in ``global.cylc``:

.. code-block:: cylc

   [install]
       [[symlink dirs]]
           [[[localhost]]]
               log = /somewhere/else

This would result in the following file structure on the Cylc Scheduler:

.. code-block:: none

   ~/cylc-run
   └── myflow
       ├── flow.cylc
       ├── log -> /somewhere/else/cylc-run/myflow/log
       ...

   /somewhere
   └── else
       └── cylc-run
           └── myflow
               └── log
                   ├── flow-config
                   ├── install
                   ...

These ``localhost`` symlinks are created during the cylc install process.
Symlinks for remote install targets are created during :ref:`RemoteInit` following
``cylc play``.


Advanced Platform Example
-------------------------

Platform with no ``$HOME`` directory
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. admonition:: Scenario

   You are trying to run jobs on a platform where the compute nodes don't
   have a configured ``HOME`` directory.

So long as the login and compute nodes share a filesystem the workflow can be
installed on the shared filesystem using
:cylc:conf:`global.cylc[install][symlink dirs]`.

The ``$CYLC_RUN_DIR`` variable can then be set on the compute node to point
at the ``cylc-run`` directory on the shared filesystem using
:cylc:conf:`global.cylc[platforms][<platform name>]global init-script`.

 .. code-block:: cylc
   :caption: part of a ``global.cylc`` config file

   [platforms]
       [[homeless-hpc]]
           job runner = my-job-runner
           install target = homeless-hpc
           global init-script = """
               export CYLC_RUN_DIR=/shared/filesystem/cylc-run
           """

   [install]
       [[symlink dirs]]
           [[[homeless-hpc]]]
               run = /shared/filesystem/

In this example Cylc will install workflows into
``/shared/filesystem/cylc-run``.

.. note::

   If you are running :term:`schedulers <scheduler>` directly on the login node
   and submitting jobs locally then the platform name and install target should
   be ``localhost``.
