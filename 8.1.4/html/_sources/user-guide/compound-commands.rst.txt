.. _CompoundCommands:

Compound Commands
=================

Cylc provides compound commands which carry out more than one
workflow action. For example Cylc provides a command to validate,
install and play a workflow.

Compound commands make common ways of working easier.

.. note::

   Use ``cylc command --help`` to get help for each compound command,
   including a full list of available options.


``cylc vip`` (Validate, Install and Play)
-----------------------------------------

``cylc vip /home/me/cylc-src/my-workflow`` is the same as running:

.. code-block:: bash

   $ cylc validate /home/me/cylc-src/my-workflow
   $ cylc install /home/me/cylc-src/my-workflow
   INSTALLED my-workflow/run1 from /home/me/cylc-src/my-workflow
   $ cylc play my-workflow
