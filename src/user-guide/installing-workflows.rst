.. _Installing-workflows:

Installing Workflows
====================

This chapter will demonstrate how to install a workflow from an arbitrary
location. Cylc will create a new directory in the :term:`run directory`
for each installation of a workflow.

.. _Install-Workflow:

The Cylc Install Command
------------------------

Once you have written your workflow, you can have Cylc install the workflow for
you, using the ``cylc install`` command.

There are various options 


Automatically Generated Directories and Files
---------------------------------------------

Running ``cylc install`` will generate some extra files in your workflow run
directory. 

- The :term:`service directory` will be created in preparation for running the 
  workflow. This is needed to store essential files used by Cylc. 

- A `_cylc-install` directory containing a `source` symlink to the source
  directory ().
  This is needed to enable Cylc to determine the original workflow source
  for ``cylc reinstall``

- A new `install` directory in the workflow's log directory, with a
  time-stamped install log file containing information about the installation.

If a compatible version of Cylc-Rose is installed, ``cylc install`` will
generate additional files/directories. 

- A directory ``opt`` containing a file ``rose-suite-cylc-install.conf`` 

- A ``rose-suite.conf`` file will also be created in the workflow run
  directory.


Excluding Items From Installation
---------------------------------
By default, cylc install will exclude `.git`, `.svn` files.
To exclude files from the file installation, create a `.cylcignore` file in
your source directory, this includes pattern matching.

For example:
Running the cylc install command inside the directory
`~/cylc-sources/test-flow` with the following directory structure:

      .. code-block:: bash
         
         $ pwd
         /home/cylc-sources/test-flow

      .. code-block:: bash

         $ tree -all
         ├── .cylcignore
         ├── dir1
         │   ├── file1
         │   └── file2
         ├── dir2
         │   ├── file1
         │   └── file2
         ├── file1
         ├── file2
         ├── file3
         ├── flow.cylc
         ├── textfile1.txt
         └── textfile2.txt

We wish to omit any files matching the pattern ``*.txt``,  the file 
``file1``, the contents of ``dir1`` and the contents of ``dir2`` and the
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
          INSTALLED test-flow from home/cylc-sources/test-flow
          -> home/cylc-run/test-flow/run1

Looking at the directory structure that has been created

    .. code-block:: bash

     $ tree -all 
     ├── dir1
     ├── file2
     ├── file3
     ├── flow.cylc
     ├── log
     │   └── install
     │       └── <time-stamp>-install.log
     └── .service

.. note::

    The following combinations of ``cylc install`` are forbidden and will
    result in error.

    - ``cylc install --run-name=my-run-name --no-run-name``

    - Running ``cylc install --run-name=my-run-name`` followed by
      ``cylc install --no-run-name``

    - Running ``cylc install --no-run-name`` followed by
      ``cylc install --run-name=my-run-name``


Reinstalling a Workflow
-----------------------

To apply changes made in your workflow source directory to the installed
workflow directory, run ``cylc reinstall`` from within the workflow run
directory. 
A new log file will be created, detailing changes made, in the workflow install
log directory.

``cylc reinstall`` can be exectued from anywhere on the file system. To do this
provide the named run you wish to reinstall.
For example:

      .. code-block:: bash

         $ cylc reinstall myflow/run1

