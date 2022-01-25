
.. _AdminGuide.PlatformConfigs:

Writing Platform Configurations
===============================

.. versionadded:: 8.0.0

.. seealso::

   - :ref:`Platforms Cylc 7 to 8 user upgrade guide <MajorChangesPlatforms>`.
   - :cylc:conf:`flow.cylc[runtime][<namespace>]platform`
   - :cylc:conf:`global.cylc[platforms]`
   - :cylc:conf:`global.cylc[platforms][<platform name>]install target`

.. _ListingAvailablePlatforms:

Listing available platforms
---------------------------

If you are working on an institutional network platforms may already
have been configured for you.

To see a list of available platforms::

   cylc config --platform-names

To see the full configuration of available platforms::

   cylc config --platform-meta
   
This is equivalent to `cylc config -i 'platforms' -i 'platform groups'`

What Are Platforms?
-------------------

Platforms define settings, most importantly:

 - A set of ``hosts``.
 - A ``job runner`` (formerly a ``batch system``) where Cylc can submit a
   task job.
 - An ``install target`` for Cylc to install task job files on.

Why Were Platforms Introduced?
------------------------------

- Allow a compute cluster with multiple login nodes to be treated as a single
  unit.
- Allow Cylc to elegantly handle failure of to communicate with login nodes.
- Configure multiple platforms with the same hosts; for example you can use
  separate platforms to submit jobs to a batch system and to background on
  ``localhost``.

.. _Install Targets:

What Are Install Targets?
-------------------------

Install targets represent file systems. More than one platform can use the
same file system. It defaults to the name of the platform.

For example, your Cylc scheduler hosts might share a file system with a
compute cluster. Cylc does not need to install files on this cluster. The
cluster and scheduler hosts are different platforms, but share an install
target.

But you might also have mirrored clusters, each with their own file system.
Each cluster would be both a platform, and have its own install target.


Example Platforms
=================

On the Scheduler Host (Cylc Server)
-----------------------------------

- **There is a built in localhost platform**

.. admonition:: Scenario

   You want to allow users to submit small jobs to the scheduler host:

If a job doesn't set a platform it will run on the Cylc scheduler host
using a default ``localhost`` platform.

Simple Remote Platform
----------------------

- **Platforms don't need to be complicated**
- **``install target`` specifies a file system for the task using that platform**

.. admonition:: Scenario

   Users want to run background jobs on a single server,
   which doesn't share a file system with the workflow host.

.. code-block:: cylc
   :caption: part of a ``global.cylc`` config file

   [platforms]
       [[myhost]]
           hosts = myhost
           install target = myhost


Cluster with Multiple Login Nodes
---------------------------------

- **Platforms can group multiple hosts together.**

.. admonition:: Scenario

   You have a cluster where users submit to a single Slurm job queue from
   either of a pair of identical login nodes which share a file system:

.. code-block:: cylc
   :caption: part of a ``global.cylc`` config file

   [platforms]
       [[spice_cluster]]
           hosts = login_node_1, login_node_2
           job runner = slurm
           install target = spice_cluster
           retrieve job logs = True

If either host is unavailable Cylc will attempt to start and communicate with
jobs via the other login node.

Since the platform hosts do not share a file system with the scheduler
host we need to ask Cylc to retrieve job logs.

Background Jobs on Cluster with Other Options
---------------------------------------------

- **Platforms are the unique combination of all settings.**

.. admonition:: Scenarios

   - Allow users to carry out occasional background jobs on a
     cluster with a batch submission system.

   - Allow some background jobs to use an alternative shell,
     or an alternative ssh command.

.. code-block:: cylc
   :caption: part of a ``global.cylc`` config file

   [platforms]
       [[spice_cluster_background]]
           hosts = login_node_1, login_node_2
           job runner = background
       [[spice_cluster_background_fish]]
           hosts = login_node_1, login_node_1
           job runner = background
           # Use fish shell
           shell = /bin/fish
       [[spice_cluster_long_ssh]]
           hosts = login_node_1, login_node_1
           job runner = background
           # extend the default ssh timeout from 10 to 30 seconds.
           ssh command = myPeculiarSSHImplementation --someoption=yes


Submit PBS Jobs from Localhost
------------------------------

- **Platforms can share hosts and not share batch systems.**

.. admonition:: Scenario

   You have a cluster where you can submit jobs from the Cylc scheduler host
   using PBS.

.. code-block:: cylc
   :caption: part of a ``global.cylc`` config file

   [platforms]
       [[pbs_cluster]]
           host = localhost
           job runner = pbs
           install target = localhost

But ``host`` defaults to ``localhost`` so you can simplify
the ``[[pbs_cluster]]`` definition.

As a result the above configuration can be simplified to:

.. code-block:: cylc
   :caption: part of a ``global.cylc`` config file

   [platforms]
       [[pbs_cluster]]
           job runner = pbs



Two Similar Clusters
--------------------

- **Platform groups allow users to ask for jobs to be run on any
  suitable computer.**

.. admonition:: Scenario

   Your site has two mirrored clusters with seperate PBS queues and
   file systems. Users don't mind which cluster is used and just
   want to set ``flow.cylc[runtime][mytask]platform = supercomputer``:

   Remember, because the install target defaults to the platform name
   clusterA and clusterB have different install targets.

.. code-block:: cylc
   :caption: part of a ``global.cylc`` config file

   [platforms]
       [[clusterA]]
           hosts = login_node_A1, login_node_A2
           batch system = pbs
       [[clusterB]]
           hosts = login_node_B1, login_node_B2
           batch system = pbs
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


Preferred and Backup Hosts and Platforms
----------------------------------------

- **You can set how hosts are selected from platforms.**
- **You can set how platforms are selected from groups.**

.. admonition:: Scenario

   You have operational cluster and a research cluster.
   You want your operational workflow to run on one of the operational
   platforms. If it becomes unavailable you want Cylc to start running
   jobs on the research cluster.

.. code-block:: cylc
   :caption: part of a ``global.cylc`` config file

   [platforms]
       [[operational]]
           hosts = login_node_A1, login_node_A2
           batch system = pbs
           [[selection]]
               method = random  # the default anyway
       [[research]]
           hosts = primary, seconday, emergency
           batch system = pbs
           [[selection]]
               method = definition order
       [platform groups]
           [[operational_work]]
               platforms = operational, research
           [[[selection]]]
               method = definition order

.. note::

   Random is the default selection method.

Lots of desktop computers
-------------------------

- **Platform names are regular expressions.**

.. admonition:: Scenario

   Everyone in your organization has a computer called ``desktopNNN``,
   all with a file system shared with the scheduler host. Many users
   will want a platform to run small jobs on their computer:

Cylc treats platform names as regular expressions, so in this case:

.. code-block:: cylc
   :caption: part of a ``global.cylc`` config file

   [platforms]
       [[desktop\d\d\d]]

will set up 1000 platforms, all with the same specification and one host per
platform. Job files can be installed on the workflow host.

.. note::

   Cylc carries out a "fullmatch" regular expression comparison with the
   the platform name so ``desktop\d\d\d`` is effectively the same as
   ``^desktop\d\d\d$``.


.. warning::

   Platforms and Platform groups are selected in a workflow configuration
   file using the same key (``[runtime][<task name>]platform = ``).
   Therefore the same names **cannot** be used for platforms and platform
   groups. The ``global.cylc`` file will fail validation if the same name is
   used in both.

Platform with no ``$HOME`` directory
------------------------------------

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
