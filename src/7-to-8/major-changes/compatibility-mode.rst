.. _cylc_7_compat_mode:

Cylc 7 Compatibility Mode
=========================

.. admonition:: Does This Change Affect Me?
   :class: tip

   This will affect you if you want to run run Cylc 7 workflows (using the
   ``suite.rc`` filename) using Cylc 8.0

Overview
--------

The old ``suite.rc`` filename triggers a backward compatibility mode in which:

- :term:`implicit tasks <implicit task>` are allowed by default

  - (unless a ``rose-suite.conf`` file is found in the :term:`run directory`
    for consistency with ``rose suite-run`` behaviour)
  - (by default, Cylc 8 does not allow implicit tasks)

- :term:`cycle point time zone` defaults to the local time zone

  - (by default, Cylc 8 defaults to UTC)

- waiting tasks are pre-spawned to mimic the Cylc 7 scheduling algorithm and
  stall behaviour, and these require
  :term:`suicide triggers <suicide trigger>`
  for alternate :term:`graph branching`

  - (Cylc 8 spawns tasks on demand and suicide triggers are not needed for
    branching)

- task ``succeeded`` outputs are *required* so the scheduler will retain
  failed tasks as incomplete

  - (in Cylc 8, all outputs are *required* unless marked as optional by new
    ``?`` syntax)


Required Changes
----------------

Providing your Cylc 7 workflow does not use syntax that was deprecated at Cylc 7
you should be able to run it without any modifications.

To see if your workflow uses deprecated syntax run ``cylc validate`` using
Cylc 7.

If tasks in your workflow call Cylc commands directly it might be necessary to
modify them to be compatible with command line interface changes.


Example
-------

Consider this configuration:

.. code-block:: cylc

   [scheduling]
       initial cycle point = 11000101T00
       [[dependencies]]
           [[[R1]]]
               graph = task

   [runtime]
       [[task]]
           pre-command scripting = echo "Hello World"

Running ``cylc validate`` on this configuration at **Cylc 7** we see that the
workflow is valid, but we are warned that ``pre-command scripting``
was replaced by ``pre-script`` at 6.4.0:

.. code-block:: console
   :caption: Cylc 7 warning of a deprecated configuration

   $ cylc validate .
   WARNING - deprecated items were automatically upgraded in 'suite definition':
   WARNING -  * (6.4.0) [runtime][task][pre-command scripting] -> [runtime][task][pre-script] - value unchanged
   Valid for cylc-7.8.7

**Cylc 7** has upgraded this for us, but at **Cylc 8** this workflow will fail
validation.

.. code-block:: console
   :caption: Cylc 8 failing to validate an obsolete configuration

   $ cylc validate .
   WARNING - deprecated graph items were automatically upgraded in "workflow definition":
    * (8.0.0) [scheduling][dependencies][X]graph -> [scheduling][graph]X - for X in:
          R1
   IllegalItemError: [runtime][task]pre-command scripting

Fixing the validation failure
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

You must change the configuration yourself. In this case:

.. code-block:: diff

   -     pre-command scripting = echo "Hello World"
   +     pre-script = echo "Hello World"

Validation will now succeed.

This will leave you with just the warning about the changes to the graph
format: You might wish to fix this now:

Fixing the deprecation warning
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

For the example given Cylc 8 will validate without warning after making the
following changes. (explanation of
:ref:`changes to graph section. <7-to-8.summary.graph_syntax>`
):

.. code-block:: diff

   [scheduling]
       initial cycle point = 11000101T00
   -   [[dependencies]]
   -       [[[R1]]]
   -           graph = task
   +   [[graph]]
   +       R1 = task

.. warning::

   Cylc 9 will not be able to upgrade obsolete Cylc 7
   configurations. It's a good idea to try and remove the configuration items
   causing to these warnings as part of routine workflow review and
   maintenance to avoid problems when a major Cylc version is released.

Host to platform upgrade logic
------------------------------

.. seealso::

   :ref:`Details of how platforms work.<MajorChangesPlatforms>`

   .. TODO reference to how to write platforms page

If you have a Cylc 7 workflow where tasks submit jobs to remote hosts
Cylc 8 will attempt to find a platform which matches the task specification.

.. important::

   Cylc 8 needs platforms matching the Cylc 7 job configuration to be
   available in :cylc:conf:`global.cylc[platforms]`.

Example
^^^^^^^

.. note::

   In the following example ``job runner`` in **Cylc 8** configurations
   and ``batch system`` in **Cylc 7** configurations refer to the same item.

If, for example you had a **Cylc 8** ``global.cylc`` with the following
platforms section:

.. code-block:: cylc
   :caption: Part of a Cylc global configuration

   [platforms]
       [[supercomputer_A]]
           hosts = localhost
           job runner = slurm
       [[supercomputer_B]]
           hosts = tigger, wol, eeyore
           batch system = pbs

And you have a **cylc 7** workflow runtime configuration:

.. code-block:: cylc
   :caption: Part of ``suite.rc``

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
