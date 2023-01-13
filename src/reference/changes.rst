Changes
=======

.. _cylc-flow-changelog: https://github.com/cylc/cylc-flow/blob/master/CHANGES.md
.. _cylc-uiserver-changelog: https://github.com/cylc/cylc-uiserver/blob/master/CHANGES.md
.. _cylc-ui-changelog: https://github.com/cylc/cylc-ui/blob/master/CHANGES.md
.. _cylc-rose-changelog: https://github.com/cylc/cylc-rose/blob/master/CHANGES.md
.. _metomi-rose-changelog: https://github.com/metomi/rose/blob/master/CHANGES.md
.. _metomi-isodatetime-changelog: https://github.com/metomi/isodatetime/blob/master/CHANGES.md

This page contains a summary of significant changes across all Cylc components for each
release.

For more detail see the component changelogs:

* `cylc-flow-changelog`_
* `cylc-uiserver-changelog`_
* `cylc-ui-changelog`_
* `cylc-rose-changelog`_
* `metomi-rose-changelog`_
* `metomi-isodatetime-changelog`_

----------

Cylc 8.1.0
----------

.. TODO: updade me before release:

   .. admonition:: Cylc Components
      :class: hint

      TODO: fill in component versions

.. warning::

   Workflows started with Cylc 8.0 which contain multiple :term:`flows <flow>`
   **cannot** be restarted with Cylc 8.1 due to database changes.


Graph View
^^^^^^^^^^

The web UI now has a graph view which displays a visualisation of a workflow's graph:

.. image:: changes/cylc-graph.gif
   :width: 80%

Family & cycle grouping as well as the ability to view graphs for stopped workflows
will be added in later releases.


Log View
^^^^^^^^

The web UI also now has a log view which displays workflow and job log files:

.. image:: changes/log-view-screenshot.png
   :width: 80%

Support for viewing more log files, syntax highlighting, searching and line
numbers are planned for future releases.


Combined Commands
^^^^^^^^^^^^^^^^^

Two new commands have been added as short-cuts for common working patterns:

``cylc vip`` validates, installs, and plays a workflow, and is equivalent to:

.. code-block:: bash

   cylc validate <path>
   cylc install <path>
   cylc play <id>

.. image:: changes/cylc-vip.gif
   :width: 80%

``cylc vr`` which validates and reinstalls a workflow, then either:
   - reloads the workflow if it is running.
   - restarts the workflow if it is stopped.

For more information see the command line help:

.. code-block:: bash

   cylc vip --help
   cylc vr --help


Bash Completion
^^^^^^^^^^^^^^^

Cylc now provides a high performance Bash completion script which saves you typing:

* Cylc commands & options
* Workflow IDs
* Cycle points
* Task names
* Job numbers

.. image:: changes/cylc-completion.bash.gif
   :width: 80%

:ref:`Installation instructions <installation.shell_auto_completion>`.

----------

Cylc 8.0.0
----------

.. admonition:: Cylc Components
   :class: hint

   :cylc-flow: `8.0 <https://github.com/cylc/cylc-flow/blob/8.0.0/CHANGES.md#user-content-major-changes-in-cylc-8>`__
   :cylc-uiserver: `1.1 <https://github.com/cylc/cylc-uiserver/blob/1.1.0/CHANGES.md#user-content-cylc-uiserver-110-released-2022-07-28>`__
   :cylc-rose: `1.1 <https://github.com/cylc/cylc-rose/blob/1.1.0/CHANGES.md#user-content-cylc-rose-110-released-2022-07-28>`__

The first official release of Cylc 8.

For a summary of changes see the :ref:`migration guide<728.overview>`.
