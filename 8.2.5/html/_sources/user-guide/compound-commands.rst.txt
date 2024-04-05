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

``cylc vr`` (Validate, Reinstall and Reload or Play)
----------------------------------------------------

``cylc vr my-workflow`` is the same as running:

.. code-block:: bash

   # Check that the changes you want to
   # make will be valid after installation:
   $ cylc validate my-workflow --against-source
   $ cylc reinstall my-workflow

   # If workflow is running:
   $ cylc reload my-workflow

   # If workflow is stopped:
   $ cylc play my-workflow

