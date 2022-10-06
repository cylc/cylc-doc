.. _MajorChangesPlatforms:

Platforms
=========

.. admonition:: Does This Change Affect Me?
   :class: tip

   .. cylc-scope:: flow.cylc

   Platforms replace the deprecated :cylc:conf:`[runtime][<namespace>][job]`
   and :cylc:conf:`[runtime][<namespace>][remote]`
   sections:

   .. code-block:: cylc

      [runtime]
          [[foo]]
              [[[job]]]
                  batch system = slurm
              [[[remote]]]
                  host = my_supercomputer

   .. cylc-scope::

   Read this section if your workflow's jobs run on a remote computer or if
   you see the following warning on running ``cylc validate``:

   .. code-block:: console

      WARNING - deprecated settings found (please replace with [runtime][foo]platform):
          [runtime][foo][remote]host
          [runtime][foo][job]batch system

   If you currently use the ``rose host-select`` utility or a similar host
   selection or load balancing utility the intelligent host selection
   functionality of Cylc 8 may be used instead:

   .. code-block:: cylc

      [runtime]
          [[task1]]
              [[[remote]]]
                  host = $(rose host-select my-computer)
          [[task2]]
              # An example of a home-rolled host selector
              [[[remote]]]
                  host = $(test $((RANDOM%2)) -eq 0 && echo "host_a" || echo "host_b")


Overview
--------

.. note::

   - The terms :term:`platform` and job platform are equivalent.
   - The terms :term:`job runner` (in Cylc 8 configurations) and batch system
     (in Cylc 7 configurations) are equivalent.

Cylc 7 defines settings for remote :term:`jobs <job>` in each
:term:`task's <task>` definition.

Cylc 8 allows site administrators (and users) to configure
:term:`platforms <platform>` in ``global.cylc``. A platform can have
multiple hosts with associated platform-specific settings. Users only need to
select the platform for their task jobs.

Platforms also define how hosts are selected from each platform:

- Randomly (default)
- By definition order

There may be cases where sets of platforms (for example a group of
standalone compute servers, or a pair of mirrored HPC's) might be equally
suitable for a task. Such platforms can be set up to be ``platform groups``

.. seealso::

   :ref:`ListingAvailablePlatforms` for details of how to list platforms
   already defined.

   :ref:`AdminGuide.PlatformConfigs` for detailed examples of platform
   configurations.

.. tip::

   Cylc 8 contains upgrade logic (:ref:`see below <host-to-platform-logic>`)
   which handles the deprecated Cylc 7 settings in most cases.
   Unless you are in :ref:`backward compatibility mode <cylc_7_compat_mode>`,
   you should upgrade to using platforms instead.
   Deprecated settings will be removed in a later release of Cylc.


Examples
--------

.. seealso::

   :cylc:conf:`global.cylc[platforms]` has a detailed explanation of how
   platforms and platform groups are defined.

Simple example
^^^^^^^^^^^^^^

Consider this Cylc 7 syntax in a ``flow.cylc`` file:

.. code-block:: cylc

   [runtime]
       [[mytask]]
           [[[job]]]
               batch system = slurm
           [[[remote]]]
               host = login_node01

The Cylc 8 global config (``global.cylc``) might contain:

.. code-block:: cylc

   [platforms]
       [[our_cluster]]
           hosts = login_node01, login_node02
           job runner = slurm

.. tip::

   You can view the platforms available at your site by running::

      cylc config --platforms

The platform ``our_cluster`` matches the current configuration due to having
the same job runner (batch system) and correct hosts. Thus we can replace the
deprecated syntax:

.. code-block:: diff

    [runtime]
        [[mytask]]
   -        [[[job]]]
   -            batch system = slurm
   -        [[[remote]]]
   -            host = login_node01
   +        platform = our_cluster


A variety of other examples
^^^^^^^^^^^^^^^^^^^^^^^^^^^

Here are some example Cylc 7 task definitions:

.. code-block:: cylc

   [runtime]
      [[mytask_cylc_server]]

      [[mytask_big_server]]
         [[[remote]]]
            host = linuxbox42

      [[mytask_submit_local_to_remote_computer]]
         [[[job]]]
            batch system = pbs

      [[mytask_login_to_hpc_and_submit]]
         [[[remote]]]
            # e.g. rose host-select
            host = $(supercomputer_login_node_selector_script)
         [[[job]]]
            batch system = slurm


This will result in Cylc running:

- ``mytask_cylc_server`` on the machine the workflow is running on.
- ``mytask_big_server`` on ``linuxbox42``, using background.
- ``mytask_submit_local_to_remote_computer`` on a system where you can
  use PBS to submit from the workflow server.
- ``mytask_login_to_hpc_and_submit`` on a host set by the subshelled
  script using Slurm.

At Cylc 8 the equivalent might be:

.. code-block:: cylc

   [runtime]
       [[mytask_cylc_server]]

       [[mytask_big_server]]
           platform = linuxbox42

       [[mytask_submit_local_to_remote_computer]]
           platform = pbs_local

       [[mytask_login_to_hpc_and_submit]]
           # Recommended:
           platform = slurm_supercomputer
           # ...but This is still legal:
           #platform = $(selector-script)

And the platform settings for these examples might be:

.. code-block:: cylc

   [platforms]
       [[linuxbox\d\d]]  # Regex to allow any linuxboxNN to use this definition
           # Without a hosts, platform name is used as a single host.

       [[pbs_local]]
           # A computer with PBS, that takes local job submissions
           job runner = pbs
           hosts = localhost
           install target = localhost

       [[slurm_supercomputer]]
           # This computer with Slurm requires you to use a login node.
           hosts = login_node01, login_node02  # Cylc will pick a host.
           job runner = slurm


Note that in these examples, it is assumed that ``linuxboxNN``, ``pbs_local`` and
``slurm_supercomputer`` have distinct file systems.
Sets of platforms which share a file system must specify
a single :ref:`install target <Install Targets>`.

.. note::
   If an install target is not set, a platform will use its own platform name
   as the install target name. If multiple platforms share a file system
   but have separate :ref:`install targets <Install Targets>` task initialization
   will fail.

.. _host-to-platform-logic:

How Cylc 8 handles host-to-platform upgrades
--------------------------------------------

If you are using the deprecated ``[remote]`` and ``[job]`` runtime sections,
Cylc 8 will attempt to find a platform which matches the task specification.

.. important::

   Cylc 8 needs platforms matching the Cylc 7 job configuration to be
   available in :cylc:conf:`global.cylc[platforms]`.


Example
^^^^^^^

If, for example you have a **Cylc 8** ``global.cylc`` with the following
platforms section:

.. code-block:: cylc

   [platforms]
       [[supercomputer_A]]
           hosts = localhost
           job runner = slurm
           install target = localhost
       [[supercomputer_B]]
           hosts = tigger, wol, eeyore
           job runner = pbs

And you have a workflow runtime configuration:

.. code-block:: cylc

   [runtime]
       [[task1]]
           [[[job]]]
               batch system = slurm
       [[task2]]
           [[[remote]]]
               host = eeyore
           [[[job]]]
               batch system = pbs

Then, ``task1`` will be assigned platform
``supercomputer_A`` because the specified host (implicitly ``localhost``)
is in the list of hosts for ``supercomputer_A`` **and** the batch system is the same.
Likewise, ``task2`` will run on ``supercomputer_B``.

.. important::

   For simplicity, and because the ``host`` key is a special case (it can
   match and host in ``[platform]hosts``) we only show these two config keys
   here. In reality, **Cylc 8 compares the whole of**
   ``[<task>][job]`` **and** ``[<task>][remote]``
   **sections and all items must match to select a platform.**
