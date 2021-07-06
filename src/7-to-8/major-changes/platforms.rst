Platforms
=========

.. note::

   The terms :term:`platform` and :term:`job platform` are equivalent.


.. admonition:: Does This Change Affect Me?
   :class: tip

   Platforms replace the following items in a Cylc 7 Workflow (suite):

   .. code-block:: cylc

      [runtime]
         [[task_name]]
            [[[job]]]
               batch system = slurm
            [[[remote]]]
               host = my_supercomputer

   Read this section if your workflow's jobs run on a remote computer or if
   you see the following warning on running ``cylc validate``:

   .. code-block:: console

      WARNING - Task <task>: deprecated "host" and "batch system" will be removed at Cylc 9


Overview
--------

Cylc 7 defines settings for remote :term:`jobs <job>` in each
:term:`task's <task>` definition.

Cylc 8 allows site administrators (and users) to configure
  :term:`platforms <platform>` in ``global.cylc``. A platform can have
  multiple hosts with associated platform-specific settings. Users only need to
  select the platform for their task jobs.

.. warning::

   Cylc 8 contains upgrade logic which handles Cylc 7
   settings in most cases. Cylc 8 will warn you when it runs
   the upgrade logic. You should upgrade these parts of your
   workflows. Deprecated Cylc 7 settings will be removed at Cylc 9.


Example
-------

Here is an example Cylc 7 :term:`graph`:

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
            host = $(supercomputer_login_node_selector_script)
         [[[job]]]
            batch system = slurm


Which will result in Cylc Running:

- ``mytask_cylc_server`` on the machine the workflow is running on.
- ``mytask_big_server`` on ``linuxbox42``, using background.
- ``mytask_submit_local_to_remote_computer`` on a system where you can
  use PBS to submit from the workflow server.
- ``mytask_login_to_hpc_and_submit`` on a host set by the subshelled
  script using Slurm.

In Cylc 8 the equivalent might be:

.. code-block:: cylc

   [runtime]
      [[mytask_cylc_server]]

      [[mytask_big_server]]
         platform = linuxbox42

      [[mytask_submit_local_to_remote_computer]]
         platform = pbs_local

      [[mytask_login_to_hpc_and_submit]]
         platform = $(supercomputer_login_node_selector_script)
