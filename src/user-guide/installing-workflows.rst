.. _Installing-workflows:

Installing Workflows
====================

Cylc commands identify workflows via their names, which are relative path names
under the :term:`cylc-run directory`, ``~/cylc-run/`` by default.

Workflows can be grouped together under sub-directories. E.g. there are three
workflows in the example below: ``nwp/oper/region1``, ``nwp/oper/region2`` and
``nwp/test/region1``.

.. code-block:: console

   $ cylc scan --state=all --name nwp --format=tree
   nwp
   ├─oper
   │ ├─ region1
   │ └─ region2
   └─test
      └─ region1

This chapter will demonstrate how to install a workflow from an arbitrary
location, called a :term:`source directory`.
``cylc install`` will create a new run directory in the :term:`cylc-run directory`
for each installation of a workflow.

.. _Install-Workflow:

The Cylc Install Command
------------------------

Workflows can be installed with the ``cylc install`` command, which creates
the :term:`run directory` structure and some service files underneath it.

.. note::

   It is possible to run a workflow without installation by writing it
   directly in the run directory.
   However, we recommend that you write your workflow in a source
   directory and use ``cylc install`` to create a fresh run directory.


.. _Using Cylc Install:

Using Cylc Install
------------------

``cylc install`` accepts as its only argument either:

* a workflow source name (see :ref:`configurable source dirs` below) e.g.
  ``foo/bar``
* a path to the source directory e.g. ``./foo/bar`` or ``/path/to/foo/bar``
  (note that relative paths must begin with ``./`` to distinguish them from
  workflow source names)

If no argument is supplied, the current working directory is used as the
source directory.

.. note::

   To avoid confusion, ``cylc install`` does not permit any of the following
   reserved directory names: |reserved_filenames|


Options
^^^^^^^

The table below illustrates several command line options that control naming
of run directories for installed workflows (the current working directory in
these examples is ``~/cylc-src/my-flow``):

.. csv-table::
   :header: Command, Results in Installation in Directory
   :align: left

   ``cylc install``, ``~/cylc-run/my-flow/run1``
   ``cylc install --no-run-name``, ``~/cylc-run/my-flow``
   ``cylc install --run-name=new-run``, ``~/cylc-run/my-flow/new-run``
   ``cylc install --workflow-name=new-name``, ``~/cylc-run/new-name/run1``


.. _configurable source dirs:

Configurable Source Directories
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

You can configure a list of directories that ``cylc install SOURCE_NAME``
and the GUI will search for source directories inside, using
:cylc:conf:`global.cylc[install]source dirs`. For example, if you have

.. code-block:: cylc

   # global.cylc
   [install]
       source dirs = ~/cylc-src, ~/roses

then ``cylc install dogs/fido`` will search for a workflow source directory
``~/cylc-src/dogs/fido``, or, failing that, ``~/roses/dogs/fido``, and install
the first match (into ``~/cylc-run/dogs/fido/run1``).


Numbered Runs
^^^^^^^^^^^^^

By default, ``cylc install`` creates numbered run directories, i.e.
``~/cylc-run/<workflow-name>/run<number>``, provided the options
``--run-name`` or ``--no-run-name`` are not used. The run number automatically
increments each time ``cylc install`` is run, and a symlink ``runN`` is
created/updated to point to the run.

Example: A typical run directory structure, after three executions of
``cylc install`` will look as follows.

.. code-block:: none

   ├── _cylc-install
   │   └── source -> /home/cylc-src/test-flow
   ├── run1
   │   ├── flow.cylc
   │   └── log
   │       └── install
   │           └── <time-stamp>-install.log
   ├── run2
   │   ├── flow.cylc
   │   └── log
   │       └── install
   │           └── <time-stamp>-install.log
   ├── run3
   │   ├── flow.cylc
   │   └── log
   │       └── install
   │           └── <time-stamp>-install.log
   └── runN -> /home/cylc-run/test-flow/run3

The numbered runs option may be overridden, using either the ``--no-run-name``
or the ``--run-name`` options.


Named Runs
^^^^^^^^^^

As an alternative to numbered runs, it is possible to name the runs, using the
``--run-name`` option.
In this case, the ``runN`` symlink will not be created.
This option cannot be used if numbered runs are already present. Likewise,
numbered runs cannot be used if named runs are already present.


.. _SymlinkDirs:

Symlink Directories
^^^^^^^^^^^^^^^^^^^

You can configure workflow :term:`run directories <run directory>` and certain
sub-directories as symlinks to other locations. This is a useful way of
offloading data onto other drives to limit the disk space taken up by
``~/cylc-run``.

Directories that can be individually symlinked are:

* ``log``
* ``share``
* ``share/cycle``
* ``work``
* the :term:`run directory` itself

The symlink targets are configured per install target in
:cylc:conf:`global.cylc[install][symlink dirs]`. For more information see
:ref:`SymlinkDirsSetup`


The Cylc Install Process
------------------------

There are two main parts of the ``cylc install`` process.

1. File Installation

2. Symlinking of Directories

.. _File Installation:

1. File Installation
^^^^^^^^^^^^^^^^^^^^

Installation will involve copying the files found in the source directory into
a new run directory. If you wish to install files into an existing run
directory, use ``cylc reinstall``, see :ref:`Reinstalling a Workflow`.

Excluding Items From Installation
"""""""""""""""""""""""""""""""""

By default, cylc install will exclude ``.git``, ``.svn`` directories.
To configure excluded files and directories from the file installation,
create a ``.cylcignore`` file in your source directory, this supports
pattern matching.

The following example will detail how to install a workflow, including
configuring files to be excluded from the installation.

.. _Example Installation:

Example Installation
""""""""""""""""""""

For example:
We will look at running the cylc install command inside the directory
``~/cylc-src/test-flow`` with the following directory structure:

.. code-block:: console

   $ pwd
   /home/cylc-src/test-flow

.. code-block:: console

   $ tree -all
   ├── .cylcignore
   ├── dir1
   │   ├── another-file
   │   └── file
   ├── dir2
   │   ├── another-file
   │   └── file
   ├── file1
   ├── file2
   ├── file3
   ├── flow.cylc
   ├── textfile1.txt
   └── textfile2.txt

We wish to omit any files matching the pattern ``*.txt``,  the file
``file1``, the contents of ``dir1`` and the contents of ``dir2`` including the
directory itself.

.. code-block:: console

   $ cat .cylcignore
   *.txt
   file1
   dir1/*
   dir2


Now we are ready to install our workflow.

.. code-block:: console

   $ cylc install
   INSTALLED test-flow from home/cylc-src/test-flow -> home/cylc-run/test-flow/run1

Looking at the directory structure that has been created

.. code-block:: console

   $ tree -all home/cylc-run/test-flow/run1
   ├── dir1
   ├── file2
   ├── file3
   ├── flow.cylc
   ├── log
   │   └── install
   │       └── <time-stamp>-install.log
   └── .service


.. _Symlinking of Directories:

2. Symlinking of Directories
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

If symlink directories are configured in the ``[[[localhost]]]`` section in
:cylc:conf:`global.cylc[install][symlink dirs]`,
``cylc install`` will create these symlinks and their target locations
(symlinks for remote install targets do not get created until
:term:`starting <start>` the workflow).

Override default symlink locations
""""""""""""""""""""""""""""""""""

You can override the default locations set in
:cylc:conf:`global.cylc[install][symlink dirs]` by using the ``--symlink-dirs``
option with ``cylc install``.

For example, using the command line option
``--symlink-dirs="log=$DIR, run=/path/to/dir,..."`` will symlink:

- ``$DIR -> ~/cylc-run/workflow/log``
- ``/path/to/dir -> ~/cylc-run/workflow/run``

.. note::

   If configuring symlink dirs on the command line, the global configured
   symlink dirs will not be used to source directories not included in
   the command line list.


To skip making localhost symlinks
"""""""""""""""""""""""""""""""""

Use ``--symlink-dirs=""`` with the ``cylc install`` command.



Automatically Generated Directories and Files
---------------------------------------------

Running ``cylc install`` will generate some extra files in your workflow run
directory.

- The :term:`service directory` will be created in preparation for running the
  workflow. This is needed to store essential files used by Cylc.

- A ``_cylc-install`` directory containing a ``source`` symlink to the
  :term:`source directory`.
  This is needed to enable Cylc to determine the original workflow source
  for ``cylc reinstall``.

- A new ``install`` directory in the workflow's log directory, with a
  time-stamped install log file containing information about the installation.

Cylc plugins (such as :ref:`Cylc Rose`) may generate additional files.


.. _Reinstalling a Workflow:

Reinstalling a Workflow
-----------------------

To apply changes from your source directory to the installed run directory,
use ``cylc reinstall``.  Changes made will be recorded in the workflow log
directory.

For example:

.. code-block:: console

   $ cylc reinstall myflow/run1

Cylc will determine the source directory and update your workflow.

Returning to the example from above (see :ref:`Example Installation`).

The source directory, ``~/cylc-src/test-flow`` has been altered as follows:

.. code-block:: console

   $ tree -all ~/cylc-src/test-flow
   ├── .cylcignore
   ├── dir1
   │   ├── another-file
   │   └── file
   ├── dir2
   │   ├── another-file
   │   └── file
   ├── dir3
   │   ├── another-file
   │   └── file
   ├── file1
   ├── file2
   ├── file3
   ├── flow.cylc
   ├── textfile1.txt
   └── textfile2.txt

.. code-block:: console

   $ cat .cylcignore
   *.txt
   file1
   dir2

We wish to update our ``~/cylc-run/test-flow/run1`` with the directories ``dir1``
and ``dir3``:

.. code-block:: console

    $ cylc reinstall test-flow/run1

The run directory now looks as follows:

.. code-block:: console

   $ tree -all home/cylc-run/test-flow/run1
   ├── dir1
   │   ├── another-file
   │   └── file
   ├── dir3
   │   ├── another-file
   │   └── file
   ├── file2
   ├── file3
   ├── flow.cylc
   ├── log
   │   └── install
   │       └── <time-stamp>-install.log
   │       └── <time-stamp>-reinstall.log
   └── .service

.. note::

   If your workflow needs to create or install scripts or executables at runtime
   and you don't want Cylc to delete them on re-installation, you can use
   ``bin`` and ``lib/python`` directories in the :ref:` workflow share directory <WorkflowShareDirectories>`.


Expected Errors
---------------

There are some occasions when installation is expected to fail:

- ``log``, ``share``, ``work`` or ``_cylc-install`` directories exist in the
  :term:`source directory`

- Neither :cylc:conf:`flow.cylc` nor the deprecated ``suite.rc`` are found in
  the :term:`source directory`

- Both :cylc:conf:`flow.cylc` and the deprecated ``suite.rc`` are found in
  the :term:`source directory`. Only one should be present.

- The workflow name is an absolute path or invalid

  Workflow names are validated by
  :py:class:`cylc.flow.unicode_rules.WorkflowNameValidator`.

  .. autoclass:: cylc.flow.unicode_rules.WorkflowNameValidator

- The workflow name contains a directory name that is any of these reserved
  filenames: |reserved_filenames|

- The install would create nested install directories. Neither a new
  installation in a subdirectory of an existing one, nor a directory containing
  an existing installation are permitted. For example, having installed a
  workflow in ``bar`` you would be unable to install one in ``foo``
  or ``foo/bar/baz``.

  .. code-block:: none

      foo
      └── bar
          ├── _cylc-install
          ├── baz
          ├── run1
          └── runN

  This means you cannot install using ``--no-run-name`` for a workflow that
  has installed numbered/named runs, nor can you install numbered/named runs
  for a workflow where ``--no-run-name`` was used.

- Trying to install a workflow into an already existing run directory.
  ``cylc reinstall`` should be used for this, see
  :ref:`Reinstalling a Workflow`.

- The source directory path does not match the source directory path of a
  previous installation. i.e. running ``cylc install`` in
  ``~/cylc-src/my-flow``, followed by running ``cylc install`` from
  ``~/different/my-flow``.
