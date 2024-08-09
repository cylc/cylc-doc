.. _user-guide.cheat_sheet:

Cheat Sheet
===========

A cheat sheet covering most of the major Cylc commands. For a full list see
``cylc help all``.

See also the :ref:`Cylc 7 to 8 migration cheat sheet <728.cheat_sheet>`.

.. contents::
   :depth: 2
   :local:
   :backlinks: none

.. highlight:: sub


Working with Workflows
----------------------

``cylc validate``
   Validates the workflow configuration (will tell you if there are any problems).
``cylc install``
   Install a workflow (i.e. copy its files into the ``~/cylc-run`` directory).
``cylc play``
   Start a workflow running.

Install and start a workflow::

   # validate a workflow
   cylc validate <name|path>

   # install a workflow
   cylc install <name|path>

   # start a workflow
   cylc play <id>

For convenience, these three operations can be combined with the ``cylc vip`` command
(vip = validate + install + play)::

   # validate, install and play a workflow
   cylc vip <name|path>

When you're done with a workflow run, remove it with ``cylc clean``::

   # delete a workflow installation
   cylc clean <id>


Starting and Stopping Workflows
-------------------------------

Start workflows with ``cylc play``, stop them with ``cylc stop``.

Workflows can be started or stopped multiple times, Cylc will always continue
where it left off::

   # start a workflow
   cylc play <id>

   # stop a workflow
   cylc stop <id>

   # restart a workflow
   cylc play <id>

You can also "pause" a workflow. A paused workflow will not submit any new
jobs. Pausing workflows can be handy if you need to perform
:ref:`interventions <user-guide.interventions>` on them. Use ``cylc play`` to
resume a workflow::

   # pause a workflow
   cylc pause <id>

   # resume a workflow
   cylc play <id>

The Cylc play, pause and stop commands work similarly to the play, pause and
stop buttons on an old tape player. You can play, pause or stop a workflow as
many times as you like; Cylc will never lose its place in the workflow.


List Workflows
--------------

The ``cylc scan`` command can list your installed workflows::

   # list all running workflows
   cylc scan

   # get information about running workflows
   cylc scan --format=rich

   # list all installed workflows
   cylc scan --states=all

You can also view your workflows in the GUI or Tui.


Opening the GUI/Tui
-------------------

Cylc has an in-terminal utility for monitoring and controlling workflows::

   # view all workflows
   cylc tui

   # open a specific workflow
   cylc tui <id>

There is also a GUI which opens in a web browser::

   # open the GUI to the homepage
   cylc gui

   # open the GUI to a specific workflow
   cylc gui <id>


Making Changes To Running Workflows
-----------------------------------

You can make changes to a workflow without having to shut it down and restart it.

First, make your required changes to the files in the workflow's
:term:`source directory`, then run the ``cylc vr`` command
(:ref:`more information <interventions.edit-the-workflow-configuration>`)::

   # validate, reinstall and reload the workflow
   cylc vr <id>

If you want to quickly edit a task's configuration, e.g. whilst developing a
workflow or testing changes, the 
:ref:`"Edit Runtime" feature <interventions.edit-a-tasks-configuration>`
in the GUI can be convenient.


Inspecting Workflows
--------------------

Validate the workflow configuration (good for spotting errors)::

   cylc validate <path|id>

Check the workflow for common problems and code style::

   cylc lint <path|id>

View the workflow configuration *before* Cylc has parsed it
(but after pre-processing - good for debugging Jinja2 errors)::

   cylc view -p <path|id>

View the workflow configuration *after* Cylc has parsed it
(good for debugging family inheritance)::

   cylc config <path|id>

   # view a specific task's configuration
   cylc config <path|id> -i '[runtime][<task>]'

   # view the workflow configuration with defaults applied
   cylc config <path|id> --defaults

Generate a graphical representation of the workflow's :term:`graph`
(a useful tool for developing workflow graphs)::

   cylc graph <path|id>

   # render the graph between two cycle points
   cylc graph <path|id> <cycle1> <cycle2>

   # render the graph transposed (can make it easier to read)
   cylc graph <path|id> --transpose

   # group tasks by cycle point
   cylc graph <path|id> --cycles

   # collapse tasks within a family (can reduce the number of tasks displayed)
   cylc graph <path|id> --group=<family>

List all tasks and families defined in a workflow::

   cylc list <path|id>


Running Rose Stem Workflows
---------------------------

Currently, Rose stem workflows are installed using a different command to
regular workflows::

   # install a rose-stem workflow
   rose stem

   # start a rose-stem workflow
   cylc play <id>

Once a workflow is installed you can run regular Cylc commands against it, e.g
``cylc stop``.

We may be able to automatically activate ``rose stem`` functionality as part
of ``cylc install`` in the future which would allow you to install and start
a Rose Stem workflow with ``cylc vip``.


Interventions
-------------

You can intervene in the running a workflow, e.g. to re-run a task.

Interventions are written up in :ref:`user-guide.interventions`. Here is a
quick summary:

Run or re-run a task (:ref:`more info <interventions.re-run-a-task>`)::

   cylc trigger <id>//<cycle>/<task>

Mark a task as "succeeded"
(:ref:`more info <interventions.set-task-outputs>`)::

   cylc set <id>//<cycle>/<task>

Kill a running job::

   cylc kill <id>//<cycle>/<task>


Running Workflows in Debug Mode
-------------------------------

When a workflow is in debug mode, more information gets written to the
workflow's :ref:`log file <troubleshooting.log_files>`.
Jobs also get run in Bash "xtrace" mode (``set -x``) which can help to diagnose
the line in a task's script that caused the error.

Start a workflow in debug mode::

   $ cylc vip --debug <name|path>

   # OR
   $ cylc play --debug <id>

Switch an already running workflow into debug mode::

   cylc verbosity DEBUG <workflow-id>

For more information, see :ref:`troubleshooting`.


Managing Multiple Workflows
---------------------------

Many Cylc commands can operate over multiple workflows::

   # stop all workflows
   cylc stop '*'

   # pause all workflows
   cylc pause '*'

   # re-run all failed tasks in all workflows
   cylc trigger "*//*/*:failed"

The ``*`` characters in these examples are "globs". Make sure you put quotes
around them to prevent the shell from trying to expand them.

For more information on globs or the Cylc ID format, run ``cylc help id``.


Working With Cylc IDs
---------------------

Everything in a Cylc workflow has an ID. We use these IDs on the command line
and in the GUI.

Cylc Ids take the format::

   <workflow-id>//<cycle>/<task>/<job>

E.G::

   # a workflow
   my-workflow

   # a cycle within a workflow
   my-workflow//20000101T00Z

   # a task instance
   my-workflow//20000101T00Z/mytask

   # a job submission
   my-workflow//20000101T00Z/mytask/01

For more information on the Cylc ID format, run ``cylc help id``.
