
.. _AdminGuide.PlatformConfigs:

Writing Platform configurations
===============================

.. versionadded:: 8.0.0

.. seealso::

   - :ref:`Platforms Cylc 7 to 8 user upgrade guide <MajorChangesPlatforms>`.
   - :cylc:conf:`flow.cylc[runtime][<namespace>]platform`
   - :cylc:conf:`global.cylc[platforms]`

What are platforms?
-------------------

Platforms define settings, most importantly a set of hosts and a
``job runner`` (formerly a ``batch system``) where Cylc can submit a
task job.

Why were platforms introduced?
------------------------------

- Allow a compute cluster with multiple login nodes to be treated as a single
  unit.
- Allow Cylc to elegantly handle failure of to communicate with login nodes.
- Configure multiple platforms with the same hosts; for example you can use
   separate platforms to submit jobs to a batch system and to background on 
   ``localhost``.


Example platforms
-----------------

On the scheduler host (Cylc Server)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**There is a built in localhost platform**

.. admonition:: Scenario

   You want to allow users to submit small jobs to the scheduler host:

If a job doesn't set a platform it will run on the Cylc scheduler host
using a default ``localhost`` platform.

Lots of desktop computers
^^^^^^^^^^^^^^^^^^^^^^^^^

- **Platform names are regular expressions.**
- **you can specify where to install job files.**

.. admonition:: Scenario

   Everyone in your organization has a computer called ``desktopNNN``,
   all with a file system shared with the scheduler host. Many users
   will want a platform to run small jobs on their computer:

Cylc treats platform names as regular expressions, so in this case:

.. code-block:: cylc
   :caption: part of a ``global.cylc`` config file

   [platforms]
       [[desktop\d\d\d]]
           install target = localhost

will set up 1000 platforms, all with the same specification and one host per
platform. Job files can be installed on the workflow host.

.. note::

   Cylc carries out a "fullmatch" regular expression comparison with the
   the platform name so ``desktop\d\d\d`` is effectively the same as
   ``^desktop\d\d\d$``.

Cluster with multiple login nodes
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- **Platforms can group multiple hosts together.**

.. admonition:: Scenario

   You have a cluster where users submit to a single Slurm job queue from
   either of a pair of identical login nodes which share a file system:

.. code-block:: cylc
   :caption: part of a ``global.cylc`` config file

   [platforms]
       [[spice_cluster]]
           hosts = login_node_1, login_node_2
           job runner = Slurm
           install target = login_node_1
           retrieve job logs = True

If either host is unavailable Cylc will attempt to start and communicate with
jobs via the other login node.

Since the platform hosts do not share a file system with the scheduler
host we need to ask Cylc to retrieve job logs.

Submit PBS jobs from localhost
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Platforms can share hosts and not share batch systems.**

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


.. TODO unindent this after you've got platforms from platform groups in
    Two similar clusters
    ^^^^^^^^^^^^^^^^^^^^

    **Platform groups allow users to ask for jobs to be run on any
    suitable computer.**

    .. admonition:: Scenario

    Your site has two mirrored clusters with seperate PBS queues and
    file systems. Users don't mind which cluster is used and just
    want to set ``flow.cylc[runtime][mytask]platform = supercomputer``:

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

    Preferred and backup hosts and platforms
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    **You can set how hosts are selected from platforms.**
    **You can set how platforms are selected from groups.**

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

