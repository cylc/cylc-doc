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
``cylc install`` will create a new directory in the :term:`cylc-run directory`
for each installation of a workflow.

.. _Install-Workflow:

The Cylc Install Command
------------------------

Workflows can be installed with the ``cylc install`` command, which creates
the :term:`run directory` structure and some service files underneath it.

.. note::

   It is possible to run a workflow without installation by writing it
   directly in the :term:`run directory`.
   However, it is considered best practice to write your workflow in a source
   directory and use ``cylc install`` to create a fresh run directory for you.

.. _Using Cylc Install:

Using Cylc Install
------------------

The following commands, executed from the :term:`source directory`
``~/cylc-src/my-flow``, result in the following installations:

+--------------------------------------+--------------------------------------+
| Command                              | Results in Installation in Directory |
+======================================+======================================+
| cylc install                         |    ~/cylc-run/my-flow/run1           |
+--------------------------------------+--------------------------------------+
| cylc install --no-run-name           |    ~/cylc-run/my-flow                |
+--------------------------------------+--------------------------------------+
| cylc install --run-name=new-run      |    ~/cylc-run/my-flow/new-run        |
+--------------------------------------+--------------------------------------+
| cylc install --flow-name=new-name    |    ~/cylc-run/new-name/run1          |
+--------------------------------------+--------------------------------------+

Any of the above commands may be run from anywhere on the file system with the
addition of the option ``--directory=PATH/TO/SOURCE/DIRECTORY`` (alternatively,
``-C PATH/TO/SOURCE/DIRECTORY``).

Configurable Source Directories
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

It is also possible to configure a list of directories that ``cylc install``
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

By default, cylc install will install the workflow found in the current working
directory into ``~/cylc-run/$(basename $PWD)/runN``, where runN = run1, run2,
run3,...

``cylc install`` will automatically increment the run number of each install,
provided the options ``--no-run-name`` or ``--run-name`` are not used. See
:ref:`Using Cylc Install` for example behaviour.

For convenience, a symlink to the most recent (highest numbered) run will be
created in the workflow directory, ``runN``.

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
In this case, the runN symlink will not be created.
This option cannot be used in conjunction with numbered runs.


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
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

By default, cylc install will exclude ``.git``, ``.svn`` directories.
To configure excluded files and directories from the file installation,
create a ``.cylcignore`` file in your source directory, this supports
pattern matching.

The following example will detail how to install a workflow, including
configuring files to be excluded from the installation.

.. _Example Installation:

Example Installation
^^^^^^^^^^^^^^^^^^^^

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

Upon running ``cylc install``, symlinks for the directories ``run``, ``log``,
``share``, ``share/cycle`` and ``work`` will be created in accordance with
the symlink rules for ``localhost`` as defined in
:cylc:conf:`global.cylc[install][symlink dirs]`.

This is overridable via the command line option ``--symlink-dirs="log=$DIR,
run=/path/to/dir,..."``, where the directories supplied will be used to create
symlinks, rather than the ones specified in
:cylc:conf:`global.cylc[install][symlink dirs]`.

.. note::

   If configuring symlink dirs on the command line, the global configured
   symlink dirs will not be used to source directories not included in
   the command line list.


Use `--symlink-dirs=""` to skip making symlinks.


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

Cylc plugins (such as :ref:`cylc-rose`) may generate additional files.


.. _Reinstalling a Workflow:

Reinstalling a Workflow
-----------------------

To apply changes made in your workflow source directory to the installed
workflow directory, run ``cylc reinstall`` from within the workflow run
directory.
A new log file will be created in the workflow install log directory, detailing
changes made.

``cylc reinstall`` can be executed from anywhere on the file system. To do this
provide the named run you wish to reinstall.
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

or cylc reinstall from within the run directory

.. code-block:: console

    $ cylc reinstall

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


Expected Errors
---------------

There are some occasions when installation is expected to fail.

If:

- ``log``, ``share``, ``work`` or ``_cylc-install`` directories exist in the
  :term:`source directory`

- neither :cylc:conf:`flow.cylc` nor the deprecated suite.rc are found in
  the :term:`source directory`

- the run-name is specified as ``_cylc-install``

- the workflow name is an absolute path or invalid

  Workflow names are validated by
  :py:class:`cylc.flow.unicode_rules.WorkflowNameValidator`.

  .. autoclass:: cylc.flow.unicode_rules.WorkflowNameValidator

- the install will create nested run directories, i.e. installing a
  workflow in a subdirectory of an existing run directory.

- trying to install a workflow into an already existing run directory,
  ``cylc reinstall`` should be used for this, see
  :ref:`Reinstalling a Workflow`.

- the source directory path does not match the source directory path of a
  previous installation. i.e. running ``cylc install`` in
  ``~/cylc-src/my-flow``, followed by running ``cylc install`` from
  ``~/cylc-different-sources/my-flow``.

.. warning::

    The following combinations of ``cylc install`` are forbidden and will
    result in error.

    - ``cylc install --run-name=my-run-name --no-run-name``

    - Running ``cylc install --run-name=my-run-name`` followed by
      ``cylc install --no-run-name``

    - Running ``cylc install --no-run-name`` followed by
      ``cylc install --run-name=my-run-name``
