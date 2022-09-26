
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
- Configure multiple platforms with the same hosts; for example you can use
  separate platforms to submit jobs to a batch system and to background on
  ``localhost``.

.. _Install Targets:

What Are Install Targets?
^^^^^^^^^^^^^^^^^^^^^^^^^

Install targets represent file systems. More than one platform can use the
same file system. Cylc relies on the site setup file ``global.cylc`` to determine
which platforms share install targets. Cylc will then use this information to
make the correct installations on remote platforms, including installation of
files, creation of :cylc:conf:`global.cylc[install][symlink dirs]` and
authentication keys to enable secure communication between platforms.

Note, if missing from configuration, the install target will default to the
platform name. If incorrectly configured, this will cause errors in
:ref:`RemoteInit`.

To check if two platforms share a file system:

Create a test file on the first platform:

   .. code-block:: console

      $ ssh platform-A
      $ echo "test file" > cylc-test-file
      $ exit

Check the second platform for the file:

   .. code-block:: console

      $ ssh platform-B
      $ cat cylc-test-file
      $ exit

If the test file exists, then these two platforms share a file system and will
require the same install target in ``global.cylc`` config file.

Example Platform Configurations
-------------------------------

Detailed below are some examples of common platform configurations.

Multiple Platforms Sharing File System with Cylc Scheduler
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- **The Scheduler Host (Cylc Server) provides a built in localhost platform**
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

.. code-block:: cylc
   :caption: the ``global.cylc`` config file for this scenario could look like:

   [platforms]
       [[localhost]]
           hosts = localhost
           install target = localhost
       [[desktop\d\d\d]]
           install target = localhost

The ``localhost`` platform is the Cylc Scheduler host, as configured in
:cylc:conf:`global.cylc[scheduler][run hosts]available`. This is the host that
the workflow will start on.
The ``desktop\d\d\d`` platform will set up 1000 platforms, all with the same
specification and one host per platform.

.. note::

   Cylc carries out a "fullmatch" regular expression comparison with the
   the platform name so ``desktop\d\d\d`` is effectively the same as
   ``^desktop\d\d\d$``.

With this config setup, Cylc is aware that these two platforms do not require
remote installations. Since the job runner is not set, this will default to
background.
Cylc has optional configuration ``[[[meta]]]`` to add a description of the
platform, this may be helpful to use, we will add a platform description to our
desktop platform.
In addition, we can take advantage of inbuilt defaults for install target and
hosts,  resulting in a simplified configuration.

.. code-block:: diff

   [platforms]
       [[localhost]]
   -        hosts = localhost
   -        install target = localhost
       [[desktop\d\d\d]]
           install target = localhost
   +       [[[meta]]]
   +           description = "Background job on a desktop system"



If a user wants to run a job on their local desktop, e.g. "desktop123", they should
set:

   .. code-block:: cylc

      [runtime]
          [[mytask]]
              platform = desktop123

in their workflow configuration.
If ``flow.cylc[runtime][mytask]platform`` is unset, the job will run on the Cylc
Scheduler host using this default ``localhost`` platform. It may be appropriate
to allow users to run small jobs on the Cylc Server however more intensive jobs
should run on a more appropriate platform, as the next scenario will detail.

Cluster with Multiple Login Nodes
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- **Platforms with multiple hosts require job runner to be set**
- **Platforms can group multiple hosts together.**

.. admonition:: Scenario

   You have a cluster where users submit to a single Slurm job queue from
   either of a pair of identical login nodes which share a file system.

.. code-block:: cylc
   :caption: part of a ``global.cylc`` config file

   [platforms]
       [[localhost]]  # Cylc Scheduler
       [[spice_cluster]]
           hosts = login_node_1, login_node_2
           job runner = slurm
           retrieve job logs = True

The ``spice_cluster`` hosts do not share a file system with the scheduler,
therefore ``spice_cluster`` is a remote platform.
As the ``install target`` setting for each platform has been omitted, this will
default to the platform name.
Cylc will initiate a remote installation, to transfer required files to
``spice_cluster`` which will commence before job submission for the first job
on that platform.

Cylc will attempt to communicate with jobs via the other login node if either
of the login_nodes becomes unavailable.

With multiple hosts defined under ``spice_cluster``, a job runner is required.

.. note::

   The "background" and "at" job runners require single-host platforms,
   because the job ID is only valid on the submission host.

We have set ``retrieve job logs = True``. This will ensure our job logs are
fetched from the ``spice_cluster`` platform. This setting is recommended for
any remote platform (i.e. where install target is not localhost).


Background Jobs on Cluster with Other Options
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- **Platforms can share hosts without sharing job runners.**
- **Platforms are the unique combination of all settings.**

.. admonition:: Scenarios

   - Allow users to carry out occasional background jobs on a
     cluster with a batch submission system.
   - Allow some background jobs to use a different config item, e.g. an
     alternative ssh command.

Extending the above example, we will configure ``login_node_1`` for use with
background jobs, in addition to the slurm example above.
``spice_cluster_long_ssh`` is also configured for use with background jobs but
has a particular setting, an ssh command with a long timeout. This demonstrates
the cumulative nature of platform configuration in Cylc.
The install target for each of the new platforms will match the install target
from the example above - the host is the same, so the install target must match.

.. code-block:: cylc
   :caption: part of a ``global.cylc`` config file

   [platforms]
       [[spice_cluster_background, spice_cluster_long_ssh]]
           hosts = login_node_1
           install target = spice_cluster
       [[spice_cluster_long_ssh]]
           ssh command = ssh -oBatchMode=yes -oConnectTimeout=30

Submit PBS Jobs from Localhost
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- **Platforms can share hosts without sharing job runners.**

.. admonition:: Scenario

   You have a cluster where you can submit jobs from the Cylc scheduler host
   using PBS.

In this similar setup, ``cluster`` has a job runner set to pbs, localhost
``job runner`` will default to background.

.. code-block:: cylc
   :caption: part of a ``global.cylc`` config file

   [platforms]
       [[pbs_cluster]]
           host = localhost
           job runner = pbs
           install target = localhost

But ``host`` defaults to ``localhost`` so we can simplify the
``[[pbs_cluster]]`` definition.

.. code-block:: cylc
   :caption: part of a ``global.cylc`` config file

   [platforms]
       [[pbs_cluster]]
           job runner = pbs
           install target = localhost

Since the install target defaults to the platform name, we must keep the
definition - without this the install target would be set to ``pbs_cluster`` and
Cylc would perform a remote installation, resulting in an error.


Grouping Platforms
^^^^^^^^^^^^^^^^^^

- **Platform groups allow users to ask for jobs to be run on any
  suitable computer.**

.. admonition:: Scenario

   Your site has two separate clusters with separate PBS queues. They share
   a file system. Users don't mind which cluster is used and just
   want to set ``flow.cylc[runtime][mytask]platform = supercomputer``.

   .. spelling:word-list::

      clusterA
      clusterB

.. code-block:: cylc
   :caption: part of a ``global.cylc`` config file

   [platforms]
       [[clusterA, clusterB]]  # settings that apply to both:
           batch system = pbs
           install target = cluster
           retrieve job logs = True
       [[clusterA]]
           hosts = login_node_A1, login_node_A2
       [[clusterB]]
           hosts = login_node_B1, login_node_B2
       [platform groups]
           [[supercomputer]]
               platforms = clusterA, clusterB

.. note::

   Why not just have one platform with all 4 login nodes?

   Having hosts in a platform means that Cylc can communicate with
   jobs via any host at any time. Platform groups allow Cylc to
   pick a platform when the job is started, but Cylc will not then
   be able to communicate with that job via hosts on another
   platform in the group.

Group platforms together using the configuration item
:cylc:conf:`global.cylc[platform groups]`. In the above example, the platforms
``clusterA`` and ``clusterB`` both share a file system (
install target = ``cluster``). We advise caution when grouping platforms with
different install targets as users could encounter a scenario whereby files (
installed by Cylc during the remote initialization process) are
not available to them.

Preferred and Backup Hosts and Platforms
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- **You can set how hosts are selected from platforms.**
- **You can set how platforms are selected from groups.**

.. admonition:: Scenario

   You have operational cluster and a research cluster, with shared file systems.
   You want your operational workflow to run on one of the operational
   platforms. If it becomes unavailable you want Cylc to start running
   jobs on the research cluster.

.. code-block:: cylc
   :caption: part of a ``global.cylc`` config file

   [platforms]
       [[operational]]
           hosts = login_node_A1, login_node_A2
           batch system = pbs
           install target = operational_work
           [[selection]]
               method = random  # the default anyway
       [[research]]
           hosts = primary, secondary, emergency
           batch system = pbs
           install target = operational_work
           [[selection]]
               method = definition order
   [platform groups]
       [[operational_work]]
           platforms = operational, research
           [[[selection]]]
               method = definition order

.. note::

   Random is the default selection method.

.. warning::

   Platforms and platform groups are both configured by
   :cylc:conf:`flow.cylc[runtime][<namespace>]platform`.
   Therefore a platform group cannot be given the same name as a platform.
   The :cylc:conf:`global.cylc` file will fail validation if the same name is
   used for both.


.. _SymlinkDirsSetup:

Symlinking Directories
^^^^^^^^^^^^^^^^^^^^^^
To minimize the disk space used by ``~/cylc-run``, set
:cylc:conf:`global.cylc[install][symlink dirs]`.
The entire workflow directory can be symlinked, using the config item ``run`` 
The following sub-directories  are also available for configuration:

   * log
   * share
   * share/cycle
   * work

These should be configured per install target.

For example, to configure workflow ``log`` directories (on the
:term:`scheduler` host) so that they symlink to a different location,
you could write the following in ``global.cylc``:

.. code-block:: cylc

   [install]
       [[symlink dirs]]
           [[[localhost]]]
               log = /somewhere/else

This would result in the following file structure:

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
