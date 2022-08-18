.. _MajorChangesPlatforms:

Platforms
=========

.. admonition:: Does This Change Affect Me?
   :class: tip

   Cylc platforms are a new feature which replace the task ``job`` and
   ``remote`` configuration sections:

   * :cylc:conf:`[runtime][<namespace>][job]`
   * :cylc:conf:`[runtime][<namespace>][remote]`


Overview
--------

.. note::

   - The terms :term:`platform` and job platform are equivalent.
   - The terms :term:`job runner` (in Cylc 8 configurations) and batch system
     (in Cylc 7 configurations) are equivalent.

Submitting a job to a :term:`job runner` may require configuration.

In Cylc 7 this configuration must be provided for each task in the workflow
configuration (``suite.rc``).

In Cylc 8 "platforms" can be defined in the global configuration
(:cylc:conf:`global.cylc`) so that this configuration doesn't have to be
repeated for each task in each workflow.

Cylc "platforms" may configure hostnames, job runners and more. Only the
platform name needs to be specified in the task configuration.

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


What is a Platform?
-------------------

A "platform" represents one or more hosts from which jobs can be submitted to or
polled from a common job submission system.

If a platform has multiple hosts Cylc will automatically select a host when
needed and will fallback to other hosts if it is not contactable.

A "platform group" represents a collection of independent platforms. Cylc will
automatically select a platform and will fallback to other platforms in the
group (for appropriate operations) if the platform is not contactable.


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
           platform = just_run_it
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

       [[slurm_supercomputer]]
           # This computer with Slurm requires you to use a login node.
           hosts = login_node01, login_node02  # Cylc will pick a host.
           job runner = slurm


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
               hosts = eeyore
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
