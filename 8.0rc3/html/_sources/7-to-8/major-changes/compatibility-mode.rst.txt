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
  - (Cylc 8 does not allow implicit tasks by default)

- :term:`cycle point time zone` defaults to the local time zone

  - (Cylc 8 defaults to UTC)

- waiting tasks are pre-spawned to mimic the Cylc 7 scheduling algorithm and
  stall behaviour, and these require
  :term:`suicide triggers <suicide trigger>`
  for alternate :term:`graph branching`

  - (Cylc 8 spawns tasks on demand, and suicide triggers are not needed for
    branching)

- only ``succeeded`` task outputs are :ref:`*expected* <User Guide Expected Outputs>`,
  meaning the scheduler will retain tasks that do not succeed as incomplete

  - (in Cylc 8, **all** outputs are *expected* unless marked as
    :ref:`*optional* <User Guide Optional Outputs>` by the new ``?`` syntax)


Required Changes
----------------

Providing your Cylc 7 workflow does not use syntax that was deprecated at Cylc 7,
you may be able to run it with Cylc 8 without any modifications to begin with.

To see if your workflow is compatible with Cylc 8, run ``cylc validate``
**using Cylc 7**.

If tasks in your workflow call Cylc commands directly it might be necessary to
modify them to be compatible with command line interface changes
(unfortunately, this is not possible to detect at validation).


Example
-------

Consider this configuration:

.. code-block:: cylc
   :caption: ``suite.rc``

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
   :caption: Cylc 7 validation

   $ cylc validate .
   WARNING - deprecated items were automatically upgraded in 'suite definition':
   WARNING -  * (6.4.0) [runtime][task][pre-command scripting] -> [runtime][task][pre-script] - value unchanged
   Valid for cylc-7.8.7

.. note::

   **Cylc 7** has handled this deprecation for us, but at **Cylc 8** this
   workflow will fail validation.

   .. code-block:: console
      :caption: Cylc 8 validation

      $ cylc validate .
      IllegalItemError: [runtime][task]pre-command scripting

Fixing the validation failure
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

You must change the configuration yourself. In this case:

.. code-block:: diff

   -     pre-command scripting = echo "Hello World"
   +     pre-script = echo "Hello World"

Validation will now succeed.

The workflow is now ready for renaming ``suite.rc`` to ``flow.cylc``

Fixing deprecation warnings after renaming ``suite.rc`` to ``flow.cylc``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

After renaming ``suite.rc`` to ``flow.cylc``, backwards compatibility mode will
be turned off and validation in Cylc 8 will show warnings (and may fail if
:ref:`User Guide Optional Outputs` and :ref:`User Guide Expected Outputs`
conflict).

.. code-block:: console
   :caption: Cylc 8 validation

   $ cylc validate .
   WARNING - deprecated graph items were automatically upgraded in "workflow definition":
    * (8.0.0) [scheduling][dependencies][X]graph -> [scheduling][graph]X - for X in:
          R1
   Valid for cylc-8.0.0

For the example given, Cylc 8 will validate without warning after making the
following changes. See :ref:`changes to the graph section. <7-to-8.graph_syntax>`.

.. code-block:: diff

    [scheduling]
        initial cycle point = 11000101T00
   -    [[dependencies]]
   -        [[[R1]]]
   -            graph = task
   +    [[graph]]
   +        R1 = task

.. tip::

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

.. _major-changes-compatibility-caveats:

Caveats
-------

The following are some caveats to be aware of when using Cylc 8
Compatibility Mode.

.. warning::

   Cylc 6 syntax deprecated by Cylc 7 is now obsolete. Run ``cylc validate``
   *with Cylc 7* on your ``suite.rc`` to check for deprecation warnings and fix
   those before validating with Cylc 8.

.. warning::

   Check for any use of Cylc commands in task scripting. Some Cylc 7 commands
   have been removed and some others now behave differently.
   See :ref:`command line interface changes<MajorChangesCLI>`.

.. warning::

   Cylc 8 does not support
   :ref:`excluding tasks at start-up<MajorChangesExcludingTasksAtStartup>`.
   If your workflow used this old functionality, it may have been used in
   combination with the ``cylc insert`` command (which has been removed from
   Cylc 8) and ``cylc remove`` (which still exists but is much less needed).

.. warning::

   Cylc 8 cannot *restart* a Cylc 7 workflow mid-run. Instead, :ref:`install
   <Installing-workflows>` the workflow to a new run directory and start it
   from scratch at the right cycle point or task(s):

   - ``cylc play --start-cycle-point=<cycle>`` (c.f. Cylc 7 *warm start*), or
   - ``cylc play --start-task=<cycle/task>``   (Cylc 8 can start anywhere in the graph)

   Any previous-cycle workflow data needed by the new run will need to be
   manually copied over from the original run directory.
