Upgrading Cylc Workflows and Inter-Version Compatibility
========================================================

Cylc is an active project, continually developing and evolving:

* *"Minor"* versions of Cylc containing new features (e.g, ``8.1``, ``8.2``,
  ``8.3``, etc) are typically released every 6-12 months.
* *"Maintainance"* versions of Cylc containing bugfixes (e.g, ``8.1.1``,
  ``8.1.2``, ``8.1.3``, etc) are typically released every 2-10 weeks.

The most important new developments in Cylc are listed on the
:ref:`reference.changes` page. We also announce these features on the
`Cylc Forum <https://cylc.discourse.group/c/cylc/tips/16>`_ to help you
stay up-to-date.


.. _user_guide.upgrading_running_workflows:

Upgrading Running Workflows
---------------------------

Although Cylc workflows can run indefinitely, it is advisable to occasionally
upgrade running workflows to newer versions of Cylc. This helps ensure
workflows remain up-to date and aren't affected by any bugs fixed in more recent
releases as well as avoiding any security issues which may develop in older
software deployments.

Upgrading a running workflow to a newer version of Cylc is generally as
simple as restarting it.

An example of upgrading a workflow from Cylc 8.5.1 to 8.6.4 on the command
line:

.. code-block:: console

   $ cylc version
   8.6.4

   $ cylc get-workflow-version my-workflow
   8.6.1

   $ cylc stop my-workflow
   Command queued

   $ cylc play my-workflow
   This workflow was previously run with 8.5.1.
   This version of Cylc is 8.6.4.
   Are you sure you want to upgrade from 8.5.1 to 8.6.4?: y,n? y

    ▪ ■  Cylc Workflow Engine 8.6.4
    ██   Copyright (C) 2008-2026 NIWA
   ▝▘    & British Crown (Met Office) & Contributors

``cylc version``
   Tells you what version of Cylc you are currently working with.
``cylc get-workflow-version``
   Tells you what version of Cylc a workflow is currently running under.
``cylc stop --now --now``
   Stops the workflow, note the ``--now --now`` tells Cylc to shut down
   immediately, rather than wait for active jobs to complete or workflow
   event handlers to run. Cylc will automatically reconnect to running jobs
   when the workflow is restarted.
``cylc play``
   Restarts the workflow. You can add the ``--upgrade`` argument to bypass
   the interactive prompt.


.. _user_guide.deprecation_notices:

Deprecation Notices
-------------------

Some older Cylc features will become deprecated.

If a workflow uses deprecated features warnings will be emitted, typically
when the workflow is validated / started. These may also appear in the GUI.

An example of a workflow which uses features which are deprecated, but still
supported, in Cylc 8.6.4:

.. code-block:: console

   $ cylc validate .
   WARNING - Deprecated config items were automatically upgraded. Please alter your workflow to use the new syntax.
   WARNING -  * (8.0.0) [cylc][parameters] -> [task parameters] - value unchanged
   WARNING -  * (8.0.0) [cylc] -> [scheduler] - value unchanged
   WARNING - deprecated settings found (please replace with [runtime][install<site>]platform):
       [runtime][install<site>][remote]host = my-hpc
       [runtime][install<site>][job]batch system = pbs
   Valid for cylc-8.6.4

Deprecated features will be removed in future versions of Cylc.

Please take action on deprecation warnings to ensure the workflow can still
be run with newer versions of Cylc when they are released.

For example, to address the first warning above:

.. code-block:: none

   [cylc][parameters] -> [task parameters] - value unchanged

You would need to make a change like this to the workflow's configuration:

.. code-block:: diff

   - [cylc]
   -     [[parameters]]
   -         site = ukmo, esnz, bom

   + [task parameters]
   +     site = ukmo, esnz, bom

.. note::

   For more information on the format of these warnings, see the
   :ref:`Cylc file format <Cylc file format>` notes in the tutorial.

.. tip::

   The ``cylc lint`` tool can be helpful in detecting deprecated features and
   other issues. If your workflow project is hosted on GitHub, you can use the
   `setup-cylc <https://github.com/cylc/setup-cylc>`_ action to automate this
   check.


.. _user_guide.inter_version_compatibility:

Inter-Version Compatibility
---------------------------

Cylc clients (i.e, the GUI, Tui and command line) will still work with
workflows running with older or newer versions of Cylc, however, there are some
limits on how different these versions can be.

Backwards Compatibility
^^^^^^^^^^^^^^^^^^^^^^^

We aim for a four minor-version compatibility window between running workflows
and **newer** Cylc clients.

For example, if a workflow is running under Cylc 8.6.0, we would expect to be
able to view and interact with this workflow using **newer** versions of the
GUI, Tui or command line until 8.10.0 (which would be the first to break
compatibility).

This isn't a firm guarantee and some functionality may be reduced.


Forwards Compatibility
^^^^^^^^^^^^^^^^^^^^^^

We aim for at least a one minor-version compatibility window between running
workflows and **older** Cylc clients.

For example, if a workflow is running under 8.7.0, we would expect to be able
to view and interact with this workflow using **older** versions of the GUI,
Tui or command line back to Cylc 8.6.0.

For the best support, you are encouraged to always use the most recent Cylc
client.
