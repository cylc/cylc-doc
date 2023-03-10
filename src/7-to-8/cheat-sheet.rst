.. _728.cheat_sheet:

Cheat Sheet
===========

Quick summary of the command line changes between Cylc 7 / Rose 2019 and Cylc 8.

.. highlight:: sub


Validating
----------

Check the workflow configuration for errors:

.. list-table::
   :class: grid-table

   * - **Cylc 7**
     - **Rose 2019**
     - **Cylc 8** (Rose 2)
   * - ::

         cylc validate <id/path>
     - ::

         # validate from $PWD
         rose suite-run --validate
     - ::

         cylc validate <id/path>

Installing & Running
--------------------

Install a workflow from source and run it:

.. list-table::
   :class: grid-table

   * - **Cylc 7**
     - **Rose 2019**
     - **Cylc 8** (Rose 2)
   * - ::

         # no installation capability
         # run from source
         cylc run <id>
     - ::

         # install from $PWD
         # then run
         rose suite-run
     - ::

         # validate, install & play
         cylc vip <id>
         cylc vip # use $PWD


Reloading
---------

To update a running workflow with changes from the source directory:

.. list-table::
   :class: grid-table

   * - **Cylc 7**
     - **Rose 2019**
     - **Cylc 8** (Rose 2)
   * - ::

         # update the live source
         # directly, then
         cylc reload <id>
     - ::

         # re-install from source
         # and do ``cylc reload``
         rose suite-run --reload
     - ::

         # Validate against source;
         # Reinstall;
         # Reload or Play
         cylc vr <id>


Pausing & Unpausing
-------------------

Tell a workflow not to submit any new jobs:

.. list-table::
   :class: grid-table

   * - **Cylc 7** & Rose 2019
     - **Cylc 8** (Rose 2)
   * - ::

         cylc hold <id>

         cylc unhold <id>
     - ::

         cylc pause <id>

         cylc play <id>

Stopping
--------

Stop a running workflow::

   cylc stop <id>

Restarting
----------

Restart a stopped workflow and pick up where it left off:

.. list-table::
   :class: grid-table

   * - **Cylc 7**
     - **Rose 2019**
     - **Cylc 8** (Rose 2)
   * - ::

         # no installation capability
         # restart from source
         cylc restart <id>
     - ::

         # regular restart
         rose suite-restart

       Or alternatively::

         # reinstall and restart
         rose suite-run --restart
     - ::

         # optionally reinstall
         cylc reinstall <id>

         # restart
         cylc play <id>

Deleting
--------

Delete the workflow :term:`run directory` (leave source files untouched):

.. list-table::
   :class: grid-table

   * - **Cylc 7**
     - **Rose 2019**
     - **Cylc 8** (Rose 2)
   * - ::

         rm -rf ~/cylc-run/<id>
     - ::

         rose suite-clean <id>
     - ::

         cylc clean <id>

Scanning
--------

List all running workflows::

   cylc scan

View A Workflow's Configuration
-------------------------------

View the parsed workflow configuration:

.. list-table::
   :class: grid-table

   * - **Cylc 7**
     - **Rose 2019**
     - **Cylc 8** (Rose 2)
   * - ::

         cylc get-config --sparse \
             <id/path>
     - ::

         # install workflow
         rose suite-run -l

         # view installed config
         cylc get-config --sparse \
             <id/path>
     - ::

         cylc config <id/path>

Opening User Interfaces
-----------------------

Opening the graphical user interface (GUI) or terminal user interface (TUI)
for monitoring / controlling running workflows:

.. list-table::
   :class: grid-table

   * -
     - **Cylc 7** & Rose 2019
     - **Cylc 8** (Rose 2)
   * - Terminal
     - ::

         cylc monitor <id>
     - ::

         cylc tui <id>
   * - Graphical
     - ::

         cylc gui <id>
     - ::

         cylc gui

   * - Web Server
     - ::

         cylc review start

     - ::

         cylc hub

Static Graph Visualisation
--------------------------

Generate a visualisation for a workflow without running it:

.. list-table::
   :class: grid-table

   * - **Cylc 7** & Rose 2019
     - **Cylc 8** (Rose 2)
   * - ::

         cylc graph <id>
     - ::

         cylc graph <id>

       This generates a basic image file if Graphviz is installed.

       The web UI will have full graph vis. in a future release.

Rose Stem
---------

Run a :ref:`rose:Rose Stem` test suite.

.. list-table::
   :class: grid-table

   * - **Rose 2019**
     - **Rose 2** (Cylc 8)
   * - ::

         # install and start
         rose stem
     - ::

         # install
         rose stem

         # start
         cylc play <workflow id>

Run a :ref:`rose:Rose Stem` test suite again, without a new installation.

.. list-table::
   :class: grid-table

   * - **Rose 2019**
     - **Rose 2** (Cylc 8)
   * - ::

         # install and start
         rose stem
     - ::

         # validate, Reinstall
         # _and_ restart:
         cylc vr <workflow id>
