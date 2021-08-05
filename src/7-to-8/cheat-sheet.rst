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
     - **Cylc8** (Rose 2)
   * - ::

         cylc validate <name/path>
     - ::

         # validate from $PWD
         rose suite-run --validate
     - ::

         cylc validate <name/path>

Installing & Running
--------------------

Install a workflow from source and run it:

.. list-table::
   :class: grid-table

   * - **Cylc 7**
     - **Rose 2019**
     - **Cylc8** (Rose 2)
   * - ::

         # no installation capability
         # run from source
         cylc run <name>
     - ::

         # install from $PWD
         # then run
         rose suite-run
     - ::

         # install from $PWD
         cylc install

         # run the installed workflow
         cylc play <name>

Pausing & Unpausing
-------------------

Tell a workflow not to submit any new jobs:

.. list-table::
   :class: grid-table

   * - **Cylc 7** & Rose 2019
     - **Cylc8** (Rose 2)
   * - ::

         cylc hold <name>

         cylc unhold <name>
     - ::

         cylc pause <name>

         cylc play <name>

Stopping
--------

Stop a running workflow::

   cylc stop <name>

Restarting
----------

Restart a stopped workflow and pick up where it left off:

.. list-table::
   :class: grid-table

   * - **Cylc 7**
     - **Rose 2019**
     - **Cylc8** (Rose 2)
   * - ::

         # no installation capability
         # restart from source
         cylc restart <name>
     - ::

         # regular restart
         rose suite-restart

       Or alternatively::

         # reinstall and restart
         rose suite-run --restart
     - ::

         # optionally reinstall
         cylc reinstall <name>

         # restart
         cylc play <name>

Deleting
--------

Delete the workflow :term:`run directory` (leave source files untouched):

.. list-table::
   :class: grid-table

   * - **Cylc 7**
     - **Rose 2019**
     - **Cylc8** (Rose 2)
   * - ::

         rm -rf ~/cylc-run/<name>
     - ::

         rose suite-clean
     - ::

         cylc clean

       Or alternatively::

         rm -rf ~/cylc-run/<name>

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
     - **Cylc8** (Rose 2)
   * - ::

         cylc get-config --sparse \
             <name/path>
     - ::

         # install workflow
         rose suite-run -l

         # view installed config
         cylc get-config --sparse \
             <name/path>
     - ::

         cylc config <name/path>

Opening User Interfaces
-----------------------

Opening the graphical user interface (GUI) or terminal user interface (TUI)
for monitoring / controling running workflows:

.. list-table::
   :class: grid-table

   * -
     - **Cylc 7** & Rose 2019
     - **Cylc8** (Rose 2)
   * - Terminal
     - ::

         cylc monitor <name>
     - ::

         cylc tui <name>
   * - Graphical
     - ::

         cylc gui <name>
     - * Open the Cylc Hub's URL in a web browser.

       * Or alternatively run your own hub::

           cylc hub

         Then open the URL ``0.0.0.0:8000`` in a web browser.

Static Graph Visualisation
--------------------------

Generate a visualisation for a workflow without running it:

.. list-table::
   :class: grid-table

   * - **Cylc 7** & Rose 2019
     - **Cylc8** (Rose 2)
   * - ::

         cylc graph <name>
     - Not yet implemented. As a temporary workaround Graphviz can be used
       to render ``cylc graph --reference`` output like so:

       .. code-block:: bash

          #!/usr/bin/env bash

          set -eu

          SUITE="$1"
          FMT="$2"

          TMP=dotfile

          cylc graph --reference "$SUITE" 2>/dev/null > "$TMP.ref"

          sed \
              -e 's/node "\(.*\)" "\(.*\)"/"\1" [label="\2"]/' \
              -e 's/edge "\(.*\)" "\(.*\)"/"\1" -> "\2"/' \
              -e '1i digraph {' \
              -e '$a}' \
              -e '/^graph$/d' \
              -e '/^stop$/d' \
              "$TMP.ref" \
              > "$TMP.dot"

          dot \
              "$TMP.dot" \
              -T$FMT \
              -o "$TMP.$FMT"

          rm "$TMP.ref" "$TMP.dot"
          echo "$TMP.$FMT"

Rose Stem
---------

Run a :ref:`rose:Rose Stem` test suite.

.. list-table::
   :class: grid-table

   * - **Rose 2019**
     - **Rose 2** (Cylc8)
   * - ::

         # install and start
         rose stem
     - ::

         # install
         rose stem

         # start
         cylc play <name>
