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

Cylc has a built in configuration upgrader. Cylc can upgrade Cylc 7
workflows to Cylc 8 workflows. Cylc cannot upgrade Cylc 6 or earlier
workflows to Cylc 8.

Solution
--------

To avoid problems with old config items you should validate your workflow using
Cylc 7. Look for deprecation warnings and change your configuration to avoid
these warnings.

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

Running ``cylc validate`` on this configuration at Cylc 7 we see that the
workflow is valid, but we are warned that ``pre-command scripting``
was replaced by ``pre-script`` at 6.4.0:

.. code-block::
   :caption: Cylc 7 warning of a deprecated configuration

   > cylc validate .
   WARNING - deprecated items were automatically upgraded in 'suite definition':
   WARNING -  * (6.4.0) [runtime][task][pre-command scripting] -> [runtime][task][pre-script] - value unchanged
   Valid for cylc-7.8.7

Cylc 7 has upgraded this for us, but at Cylc 8 this workflow will fail
validation.

.. code-block::
   :caption: Cylc 8 failing to validate an obselete configuration

   > cylc validate .
   IllegalItemError: [runtime][task]pre-command scripting


You must change the configuration yourself:

.. code-block:: diff

   -     pre-command scripting = echo "Hello World"
   +     pre-script = echo "Hello World"


.. warning::

   At version 9 Cylc will no longer automatically upgrade obselete Cylc 7
   configurations. It's a good idea to try and remove the configuration items
   causing to these warnings as part of routine workflow review and
   maintainance to avoid problems when a major Cylc version is released.
