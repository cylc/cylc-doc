.. _Installing-workflows:

Installing Workflows
====================

Cylc commands identify workflows via their names, which are relative path names
under the workflow run directory (``~/cylc-run/`` by default).

Workflows can be grouped together under sub-directories. E.g.:

.. code-block:: console

   $ cylc scan --state=all --name nwp
   nwp
    |-oper
    | |-region1  Local Model Region1       /home/oliverh/cylc-run/nwp/oper/region1
    | `-region2  Local Model Region2       /home/oliverh/cylc-run/nwp/oper/region2
    `-test
      `-region1  Local Model TEST Region1  /home/oliverh/cylc-run/nwp/test/region1

This chapter will demonstrate how to install a workflow from an arbitrary
location, called a :term:`source directory`.
``cylc install`` will create a new directory in the :term:`run directory` for
each installation of a workflow.

.. _Install-Workflow:

The Cylc Install Command
------------------------

Workflow names can be installed with the ``cylc install`` command,
which creates the workflow run directory structure and some service files
underneath it. Otherwise, ``cylc play`` will do this at workflow start up.

Once you have written your workflow, you can have Cylc install the workflow for
you, using the ``cylc install`` command.

.. _Command Line Options:

Command Line Options
--------------------

The following commands, executed from :term:`source directory` e.g.
``~/cylc-sources/my-flow`` result in the following installations.


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
addition of the option ``--directory=PATH/TO/SOURCE/DIRECTORY``, alternatively
use ``-C PATH/TO/SOURCE/DIRECTORY``.

Numbered Runs
^^^^^^^^^^^^^

By default, cylc install will install the workflow found in the current working
directory into ``~/cylc-run/$(basename $PWD)/runN``, where runN = run1, run2, 
run3,...

``cylc install`` will automatically increment the run number of each install,
provided the options ``--no-run-name`` or ``--run-name`` are not used. See
:ref:`Command Line Options` for example behaviour.

For convenience, a symlink to the highest (latest) numbered run will be created
in the workflow directory, ``runN``.

Example: A typical run directory structure, after three exectutions of 
``cylc install`` will look as follows. 

.. code-block:: bash

   ├── _cylc-install
   │   └── source -> /home/cylc-sources/test-flow
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

Installation will involved copying the files found in the source directory into
a new run directory. If you wish to install files into an existing run
directory, use ``cylc reinstall``, see :ref:`Reinstalling a Workflow`.


.. _example_installation:

Excluding Items From Installation
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

By default, cylc install will exclude `.git`, `.svn` directories.
To configure excluded files and directories from the file installation,
create a `.cylcignore` file in your source directory, this supports
pattern matching.

For example:
We will look at running the cylc install command inside the directory
`~/cylc-sources/test-flow` with the following directory structure:

.. code-block:: bash
         
   $ pwd
   /home/cylc-sources/test-flow

.. code-block:: bash

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

.. code-block:: bash

   $ cat .cylcignore
   *.txt
   file1
   dir1/*
   dir2


Now we are ready to install our workflow.
      
.. code-block:: bash

   $ cylc install
   INSTALLED test-flow from home/cylc-sources/test-flow -> home/cylc-run/test-flow/run1

Looking at the directory structure that has been created

.. code-block:: bash

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
:cylc:conf:`global.cylc[symlink dirs]`. 

This is overridable via the command line option ``--no-symlinks``, where the 
directories will not be symlinked.


Automatically Generated Directories and Files
---------------------------------------------

Running ``cylc install`` will generate some extra files in your workflow run
directory. 

- The :term:`service directory` will be created in preparation for running the 
  workflow. This is needed to store essential files used by Cylc. 

- A `_cylc-install` directory containing a `source` symlink to the
  :term:`source directory`.
  This is needed to enable Cylc to determine the original workflow source
  for ``cylc reinstall``.

- A new `install` directory in the workflow's log directory, with a
  time-stamped install log file containing information about the installation.

If a compatible version of Cylc-Rose is installed, ``cylc install`` will
generate additional files/directories. 

- A directory ``opt`` containing a file ``rose-suite-cylc-install.conf`` 

- A ``rose-suite.conf`` file will also be created in the workflow run
  directory.


.. _Reinstalling a Workflow:

Reinstalling a Workflow
-----------------------

To apply changes made in your workflow source directory to the installed
workflow directory, run ``cylc reinstall`` from within the workflow run
directory. 
A new log file will be created in the workflow install log directory, detailing
changes made.

``cylc reinstall`` can be exectued from anywhere on the file system. To do this
provide the named run you wish to reinstall.
For example:

.. code-block:: bash

   $ cylc reinstall myflow/run1

Cylc will determine the source directory and update your workflow. 

Returning to the example from above (see example_installation_). The source
directory, `~/cylc-sources/test-flow` has been altered as follows:

.. code-block:: bash

   $ tree -all ~/cylc-sources/test-flow
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

.. code-block:: bash

   $ cat .cylcignore
   *.txt
   file1
   dir2

We wish to update our ~/cylc-run/test-flow/run1 with the directories ``dir1``
and ``dir3``. There are two ways Cylc can be used to achieve this change.

1. From anywhere in the file system

.. code-block:: bash

    $ cylc reinstall test-flow/run1

2. From the workflow run directory.

.. code-block:: bash

    $ pwd
    /home/cylc-run/test-flow/run1

.. code-block:: bash

    $ cylc reinstall
          
The workflow run directory now looks as follows:

.. code-block:: bash

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
  :py:class:`cylc.flow.unicode_rules.SuiteNameValidator`.

  .. autoclass:: cylc.flow.unicode_rules.SuiteNameValidator

- the install will create nested run directories, i.e. installing a
  workflow in a subdirectory of an existing run directory.

- trying to install a workflow into an already existing workflow run directory,
  ``cylc reinstall`` should be used for this, see
  :ref:`Reinstalling a Workflow`.

- the source directory path does not match the source directory path of a
  previous installation. i.e. running ``cylc install`` in
  ``~/cylc-sources/my-flow``, followed by running ``cylc install`` from
  ``~/cylc-different-sources/my-flow``.

.. note::

    The following combinations of ``cylc install`` are forbidden and will
    result in error.

    - ``cylc install --run-name=my-run-name --no-run-name``

    - Running ``cylc install --run-name=my-run-name`` followed by
      ``cylc install --no-run-name``

    - Running ``cylc install --no-run-name`` followed by
      ``cylc install --run-name=my-run-name``
