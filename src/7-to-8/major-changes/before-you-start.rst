.. _AutoConfigUpgrades:

Cylc Configuration Upgrader
===========================

.. admonition:: Does This Change Affect Me?
   :class: tip

   This change may affect you:

   - If you are working with workflows written before Cylc 7.
   - If you hope to use Cylc 9.

   You have been affected by this change if you see a message such as:

   .. code-block::

      > cylc validate my_workflow
      IllegalItemError: reallyoldconfig


Overview
--------

Cylc has a built in configuration upgrader. **Cylc 8** can upgrade Cylc 7
workflows. **Cylc 8** will not upgrade Cylc 6 or earlier workflows to Cylc 8.

Solution
--------

To avoid problems with old config items you should validate your workflow using
Cylc 7. Look for deprecation warnings and edit the workflow configuration to
eliminate these warnings.

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

.. code-block::
   :caption: Cylc 7 warning of a deprecated configuration

   > cylc validate .
   WARNING - deprecated items were automatically upgraded in 'suite definition':
   WARNING -  * (6.4.0) [runtime][task][pre-command scripting] -> [runtime][task][pre-script] - value unchanged
   Valid for cylc-7.8.7

**Cylc 7** has upgraded this for us, but at **Cylc 8** this workflow will fail
validation.

.. code-block::
   :caption: Cylc 8 failing to validate an obsolete configuration

   > cylc validate .
   WARNING - deprecated graph items were automatically upgraded in "workflow definition":
    * (8.0.0) [scheduling][dependencies][X]graph -> [scheduling][graph]X - for X in:
          R1
   IllegalItemError: [runtime][task]pre-command scripting

Fixing Validation Failure
^^^^^^^^^^^^^^^^^^^^^^^^^

You must change the configuration yourself:

.. code-block:: diff

   -     pre-command scripting = echo "Hello World"
   +     pre-script = echo "Hello World"

Validation will now succeed.

This will leave you with just the warning about the changes to the graph
format: You might wish to fix this now:

Fixing Deprecation Warning
^^^^^^^^^^^^^^^^^^^^^^^^^^

For the example given Cylc 8 will validate without warning after making the
following changes. (explanation of
:ref:`changes to graph section. <7-to-8.summary.graph_syntax>`
):

.. code-block:: diff

   [scheduling]
       initial cycle point = 11000101T00
   -   [[dependencies]]
   +   [[graph]]
   -       [[[R1]]]
   -           graph = task
   +       R1 = task

.. warning::

   Cylc 9 will no longer automatically upgrade obselete Cylc 7
   configurations. It's a good idea to try and remove the configuration items
   causing to these warnings as part of routine workflow review and
   maintenance to avoid problems when a major Cylc version is released.

Host to platform upgrade logic
------------------------------

.. seealso::

   :ref:`Details of how platforms work.<MajorChangesPlatforms>`

   .. TODO reference to how to write platforms page

If you have a Cylc 7 workflow where tasks submit jobs to remote hosts
Cylc 8 will attempt to find a platform which matches the task specfication.

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
           hosts = tigger, wol, eyore
           batch system = pbs

And you have a **cylc 7** workflow runtime configuration:

.. code-block:: cylc
   :caption: Part of ``suite.rc`` or ``flow.cylc``

   [runtime]
       [[task1]]
           [[[job]]]
               batch system = slurm
       [[task2]]
           [[[remote]]]
               hosts = eyore
           [[[job]]]
               batch system = pbs


Then, ``task1`` will be assigned platform
``supercomputer_A`` because the host
specified is in the list of hosts **and** the batch system is the same and task
``task2`` will run on ``supercomputer_B``.

.. important::

   for simplicity, and becuause the ``host`` key is a special case (it can
   match and host in ``[platform]hosts``) we only show these two config keys
   here. In reality, **Cylc 8 compares the whole of**
   ``[<task>][job]`` **and** ``[<task>][remote]``
   **sections and all items must match to select a platform.**
