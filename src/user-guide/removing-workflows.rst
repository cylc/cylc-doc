.. _Removing-workflows:

Removing Workflows
==================

If you want to delete an installed workflow from the :term:`cylc-run directory`
(or just delete certain subdirectories), the recommended way is using
the ``cylc clean`` command. ``cylc clean`` takes care of deleting workflows
on the local filesystem was well as any remote install targets. It also
follows any symlink directories specified in
:cylc:conf:`global.cylc[install][symlink dirs]`
(but will never follow other symlink directories). It will not remove the
workflow :term:`source directory` either.

If you've used ``rose suite-clean`` before, the functionality is similar, but
not identical.

``cylc clean`` can be called like so:

.. code-block:: console

   $ cylc clean myflow/run1
   INFO - Cleaning on local filesystem: ~/cylc-run/myflow/run1

.. note::

   Trying to clean a directory that contains more than one
   :term:`run directory` is not allowed, as a safety feature. You can override
   this using the ``--force`` option, but this will not clean remote install
   targets or follow symlink dirs as described above.


Cleaning on remote install targets
----------------------------------

If any jobs in your workflow ran on a remote :term:`platform`, Cylc will
automatically remove the workflow files on there in addition to the local
filesystem.

.. code-block:: console

   $ cylc clean remote-example
   INFO - Cleaning on install target: enterprise1701
   INFO - Cleaning on local filesystem: ~/cylc-run/remote-example/run1

.. note::

   This relies on determining which platforms were used from the workflow
   database; if the database is missing, you will have to manually remove the
   files on remote install targets.

You can also clean on just the local filesystem using the ``--local`` option,
or just the remote install target using the ``--remote`` option.


Cleaning specific subdirectories or files
-----------------------------------------

You can clean specific subdirectories or files inside a run directory using
the ``--rm`` option. For example, to remove the ``log`` and ``work``
directories:

.. code-block:: console

   $ cylc clean myflow --rm log --rm work

Colons can be used to delimit the items to clean, so the following is
equivalent:

.. code-block:: console

   $ cylc clean myflow --rm log:work

You can also use globs. E.g., to remove all job logs for cycle points
beginning with ``2020``:

.. code-block:: console

   $ cylc clean myflow --rm 'log/job/2020*'

.. note::

   Make sure to place glob patterns in quotes.

.. tip::

   Use the ``--debug`` option to see all the directories or files that get
   removed.
