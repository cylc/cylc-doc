.. _Removing-workflows:

Removing Workflows
==================

To delete an installed workflow :term:`run directory`, we recommend using
the ``cylc clean`` command. ``cylc clean`` takes care of deleting workflows
on the local filesystem and any remote install targets.
It follows any symlink directories specified in
:cylc:conf:`global.cylc[install][symlink dirs]`
(see :ref:`CleanSymlinkDirsNote` below). You can also use ``cylc clean`` to
just delete certain files or subdirectories (see :ref:`TargetedClean` below).

If you've used ``rose suite-clean`` before, the functionality is similar, but
not identical.

.. note::

   ``cylc clean`` only affects workflow :term:`run directories <run directory>`
   (located in the :term:`cylc-run directory`). It will not affect
   workflow :term:`source directories <source directory>`.

.. warning::

   ``cylc clean`` is intended for use on workflows installed with
   ``cylc install``. If you clean a workflow that was instead written
   directly in the cylc-run directory and not backed up elsewhere,
   it will be lost.

Simple example of using ``cylc clean``:

.. code-block:: console

   $ cylc clean myflow/run1
   INFO - Cleaning on local filesystem: ~/cylc-run/myflow/run1

.. note::

   Trying to clean a directory that contains more than one
   run directory is not allowed, as a safety feature. You can override
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
   database. If the database is missing, you will have to manually remove the
   files on remote install targets.

You can also clean on just the local filesystem using the ``--local`` option,
or just the remote install target using the ``--remote`` option.


.. _TargetedClean:

Cleaning specific subdirectories or files
-----------------------------------------

You can clean specific subdirectories or files inside a run directory using
the ``--rm`` option (we refer to this as a targeted clean).
For example, to remove the ``log`` and ``work`` directories:

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


.. _CleanSymlinkDirsNote:

A note on symlink directories
-----------------------------

.. admonition:: Does this affect me?
   :class: tip

   If you use symlink directories specified in
   :cylc:conf:`global.cylc[install][symlink dirs]`, you might want to read
   this explanation of how Cylc handles them during cleaning.

If you manually delete a run directory (e.g., using ``rm`` or the file
manager), only the symlinks themselves will be deleted, not the actual targets.
In contrast, ``cylc clean`` follows the symlinks and deletes the targets.

- It does this for the symlinks that can be set in
  :cylc:conf:`global.cylc[install][symlink dirs]` only, not any custom
  user-created symlinks.
- It does not actually look up the global configuration at time of cleaning;
  it simply detects what symlinks are present out of the possible ones.
- It also does this for targeted clean (using the ``--rm`` option).
