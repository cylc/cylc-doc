.. _user-guide.interventions:

Interventions
=============

Sometimes things don't go to plan!

So Cylc allows you to take manual control of your workflow while it's running
allowing you to do things like edit a task's configuration, re-run a section
of your graph or override task outputs.

This section of the documentation covers some of the common interventions you
might want to perform in various scenarios.

You can perform these interventions in multiple ways:

.. tab-set::

   .. tab-item:: GUI
      :sync: gui

      The Cylc web app (GUI) can be launched with the ``cylc gui`` command.

      Some sites provide a central deployment for you where you log in via the
      web browser rather than launching it yourself.

   .. tab-item:: With the Tui
      :sync: tui

      Cylc Tui is an interactive in-terminal application, like a minimal
      version of the GUI. Start it with the ``cylc tui`` command.

      Launch it with the ``cylc tui`` command.

   .. tab-item:: On the CLI
      :sync: cli

      The Cylc command line interface (CLI) can do everything the GUI can.

      To see the full list of available commands run ``cylc help all``.

.. Write out a local table of contents:

.. contents:: Contents
   :depth: 1
   :local:

.. NOTE - Creating screen recordings

   * Use the dimensions 650x720 for your recording area.
   * On my setup that works out as 72 cols by 40 rows in the terminal.
   * Keep it as short as possible without being disorientating.
   * Document top-level use cases, don't attempt to cover every
     possible intervention.
   * I've been installing workflows as "myworkflow".


.. _interventions.re-run-a-task:

Re-Run a Task
-------------

:Example:
   A task failed and I want to give it another try.

:Solution:
   Trigger the failed task.

.. tab-set::

   .. tab-item:: GUI
      :sync: gui

      .. image:: re-run-a-task.gui.gif
         :width: 75%

   .. tab-item:: Tui
      :sync: tui

      .. image:: re-run-a-task.tui.gif
         :width: 75%

   .. tab-item:: CLI
      :sync: cli

      .. code-block:: console

         $ cylc trigger <workflow>//<task>


.. _interventions.re-run-multiple-tasks:

Re-Run Multiple Tasks
---------------------

:Example:
   I need to re-run a few tasks in order.

:Solution:
   Determine the tasks you want to re-run and trigger all of them at the
   same time.

   We often want to
   :ref:`edit the tasks configuration <interventions.edit-a-tasks-configuration>`
   before doing this.

.. tab-set::

   .. tab-item:: GUI
      :sync: gui

      .. image:: ./../../reference/changes/group-trigger.gif
         :width: 75%

   .. tab-item:: CLI
      :sync: gui

      .. code-block:: console

         $ cylc trigger <workflow>// \
         >   //<cycle-1>/<task-2> \
         >   //<cycle-2>/<task-2> \
         >   ...


.. _interventions.reflow:

Re-Run A Task And Everything After It
-------------------------------------

:Example:
   I want to reconfigure a task, then re-run it and all tasks downstream of it.

:Solution:
   :ref:`Edit the tasks configuration <interventions.edit-a-tasks-configuration>`,
   then trigger it in a new :term:`flow`.

.. tab-set::

   .. tab-item:: GUI
      :sync: gui

      .. image:: reflow.gui.gif
         :width: 75%

   .. tab-item:: CLI
      :sync: cli

      .. code-block:: console

         $ cylc trigger --flow=new <workflow>//<cycle>/<task>

.. warning::

   Tasks which have run before your trigger command will not have run in the
   new flow. As a result, you may want to manually set task outputs to allow
   the new flow to continue.

   You can achieve this by setting the
   :ref:`outputs <interventions.set-task-outputs>` of these tasks, or
   satisfying the :ref:`prerequisites <interventions.set-task-prerequisites>`
   of the tasks in the new flow.


Re-Run All Failed Tasks
-----------------------

:Example:
   Multiple tasks failed due to factors external to the workflow.
   I've fixed the problem, now I want them to run again.

:Solution:
   Trigger all failed tasks.

.. note::

   You can use this intervention with other states too, e.g. "submit-failed".

.. tab-set::

   .. tab-item:: GUI
      :sync: gui

      .. image:: re-run-all-failed-tasks.gui.gif
         :width: 75%

   .. tab-item:: CLI
      :sync: cli

      .. code-block:: console

         $ cylc trigger <workflow>//*/*:failed


.. _interventions.set-task-outputs:

Set Task Outputs
----------------

:Example:
   My task failed, I've gone and fixed the problem, now I want to tell Cylc
   that the task succeeded.

:Solution:
   Set the "succeeded" :term:`output <task output>` on the failed task.

.. tab-set::

   .. tab-item:: GUI
      :sync: gui

      .. image:: set-task-outputs.gui.gif
         :width: 75%

      By default, this sets all :term:`required outputs <required output>` for
      the task, including ``submitted``, ``started`` and ``succeeded`` (even
      if those are optional). To specify the output(s) you would like to set,
      press the pencil icon next to the "Set" command .

   .. tab-item:: Tui
      :sync: tui

      .. image:: set-task-outputs.tui.gif
         :width: 75%

      By default, this sets all :term:`required outputs <required output>` for
      the task, including ``submitted``, ``started`` and ``succeeded`` (even
      if those are optional). To specify the output(s) you would like to set,
      use ``cylc set --output``.

   .. tab-item:: CLI
      :sync: cli

      .. code-block:: console

         $ cylc set <workflow>//<task>

      By default, this sets all :term:`required outputs <required output>` for
      the task, including ``submitted``, ``started`` and ``succeeded`` (even
      if those are optional). To specify the output(s) you would like to set,
      use the ``--output`` option.

You can also :ref:`set task prerequisites <interventions.set-task-prerequisites>`.
Should I set task outputs or prerequisites?

* If you set a task's outputs, then tasks downstream of it may start to run.
* If you set a task's prerequisites, the task itself may start to run.


.. _interventions.set-task-prerequisites:

Set Task Prerequisites
----------------------

.. workflow config:

   [scheduler]
       allow implicit tasks = True

   [scheduling]
       [[graph]]
           R1 = """
               a => z1 & z2
               b1 => b2 => z1 & z2
               c => z1 & z2

               # set prereqs "1/b2:succeeded" and "1/c:succeeded" on 1/z1
               # set prereqs "all" on 1/z2
           """

   [runtime]
       [[b1]]
           script = sleep 600
       [[c]]
           script = false

:Example:
   A task is not running yet, because one or more of its
   :term:`prerequisites <trigger>` are not satisfied (e.g. upstream tasks
   have not run yet or have failed). I want it to ignore one or more of these
   prerequisites.

:Solution:
   Set the task's prerequisites as satisfied.

.. note::

   If you want the task to run right away, then trigger it using the same
   intervention as :ref:`interventions.re-run-a-task`.

.. tab-set::

   .. tab-item:: GUI
      :sync: gui

      .. image:: set-task-prerequisites.gui.gif
         :width: 75%

   .. tab-item:: CLI
      :sync: cli

      .. code-block:: console

         $ cylc set \
         >   --pre <prereq-cycle>/<prereq-task>:<prereq-output> \
         >   <workflow>//<cycle><task>

You can also :ref:`set task outputs <interventions.set-task-outputs>`.
Should I set task outputs or prerequisites?

* If you set a task's outputs, then tasks downstream of it may start to run.
* If you set a task's prerequisites, the task itself may start to run.


Set a Switch Task
-----------------

.. workflow config:

   [scheduling]
       cycling mode = integer
       initial cycle point = 1
       runahead limit = P1
       [[graph]]
           P1 = """
               start => switch
               switch:normal? => normal
               switch:alternate? => alternate
               normal | alternate => end

               end[-P1] => start
           """

   [runtime]
       [[start]]
           script = """
               if [[ $CYLC_TASK_CYCLE_POINT -eq 1 ]]; then
                   sleep 3
               fi
           """
       [[switch]]
           script = cylc message -- normal
           [[[outputs]]]
               normal = normal
               alternate = alternate
       [[normal, alternate]]
       [[end]]

:Example:
   I have a :term:`branched workflow <graph branching>`, I want to direct it to
   take a particular path ahead of time:

   .. code-block:: cylc-graph

      start => switch

      # by default, the workflow follows the "normal" path
      switch:normal? => normal

      # but it can follow an alternate route if desired
      switch:alternate? => alternate

      normal | alternate => end

:Solution:
   Set "succeeded" as well as the desired output(s) on the task and use the
   ``--wait`` option. Cylc will follow the desired path when it gets there.

   .. note::

      We set the "succeeded" output to prevent the task from being re-run when the
      flow approaches it.

.. tab-set::

   .. tab-item:: GUI
      :sync: gui

      .. image:: set-a-switch-task.gui.gif
         :width: 75%

   .. tab-item:: CLI
      :sync: cli

      .. code-block:: console

         $ cylc set --wait --output=succeeded,alternate <workflow>


.. _interventions.edit-a-tasks-configuration:

Edit a Task's Configuration and Re-Run It
-----------------------------------------

:Example:
   I'm developing a task and need to be able to quickly make changes and re-run
   the task.

:Solution:
   Edit the task's definition and trigger it.

.. tab-set::

   .. tab-item:: GUI
      :sync: gui

      .. image:: edit-a-tasks-configuration.gui.gif
         :width: 75%

      .. note::

         Any changes you make apply only to this one instance of the task, not
         to any future instances.

         To change future instances, either use "broadcast" or see
         :ref:`interventions.edit-the-workflow-configuration`.

   .. tab-item:: CLI
      :sync: cli

      .. code-block:: console

         $ cylc broadcast <workflow> -p <cycle> -n <task> -s 'script=true'
         $ cylc trigger <workflow>//<cycle>/<task>

.. the "|" character adds some vertical whitespace

|

.. _interventions.edit-the-workflow-configuration:

Edit The Workflow Configuration
-------------------------------

:Example:
   I want to change the configuration of multiple tasks or add/remove tasks
   without stopping the workflow or starting it from the beginning again.

:Solution:
   Edit the workflow configuration in the :term:`source directory`, then
   :term:`reinstall` and :term:`reload` the workflow.

.. tab-set::

   .. tab-item:: Tui
      :sync: tui

      .. image:: edit-the-workflow-configuration.tui.gif
         :width: 75%

   .. tab-item:: CLI
      :sync: cli

      .. code-block:: console

         $ vim ~/cylc-src/myworkflow  # edit the workflow configuration
         $ cylc vr myworkflow         # reinstall and reload the workflow

.. note::

   For information on how graph changes (e.g. the adding or removing of tasks)
   are applied, see
   :ref:`user-guide.restarting-or-reloading-after-graph-changes`.


Orphan a "Stuck" Job Submission
-------------------------------

:Example:
   I have a job which cannot be killed (e.g. the platform has gone down), I
   want Cylc to forget about it.

:Solution:
   Set the "failed" output on the task.

Use the same intervention as :ref:`interventions.set-task-outputs`,
but you will probably want to specify the "failed" output rather than
"succeeded".


Terminate a Chain of Automatic Retries
--------------------------------------

:Example:
   I have a failed task which has been configured to automatically
   :term:`retry`, I want to cancel these retries because I know it can't
   succeed.

:Solution:
   Set the "failed" output on the task.

Use the same intervention as :ref:`interventions.set-task-outputs`,
but specify the "failed" output rather than
"succeeded".


.. _interventions.trigger_while_paused:

Pause The Workflow And Trigger Tasks One By One
-----------------------------------------------

:Example:
   I want to pause the workflow while I manually run one or more tasks
   to fix a problem or test a task.

:Solution:
   * Pause the workflow.
   * Trigger the task(s) you want to run.
   * When you're done triggering, resume (unpause) the workflow.

.. tab-set::

   .. tab-item:: GUI
      :sync: gui

      .. image:: trigger-while-paused.gif
         :width: 75%

   .. tab-item:: CLI
      :sync: cli

      .. code-block:: console

         $ # pause the workflow
         $ cylc pause <workflow>

         $ # trigger the task(s) you want to run
         $ cylc trigger --now <workflow>//<cycle>/<task>

         $ # resume (unpause) the workflow to continue
         $ cylc play <workflow>

.. note::

   The difference between the workflow "paused" state and the task "held" state:

   Workflow Pause
      When a workflow is :term:`paused <pause>` new jobs will not be submitted
      automatically, but you can still trigger tasks manually.
      This gives you an opportunity to make changes to the workflow.

   Task Hold
      When a task is :term:`held <hold>`, then it will not submit (if ready to
      submit) until released. If you hold a running task its job will not be
      affected, but it will not submit any :term:`retries <retry>` until released.

.. _interventions.skip_cycle:

I want to Skip a cycle of tasks and allow the workflow to continue
------------------------------------------------------------------

:Example:

   I want to skip a cycle (or group) of tasks and continue as if they had run
   and succeeded.

:Solution:

   Set the run mode of the tasks to skip and Cylc will pretend that they
   have run (very quickly).

.. tab-set::

   .. tab-item:: GUI
      :sync: gui

      .. image:: skip-cycle.gui.gif
         :width: 75%

   .. tab-item:: CLI
      :sync: cli

      .. code-block:: console

         cylc broadcast -p '<cycle>' -n root -s 'run mode = skip'

.. note::

   ``-n root`` matches all tasks in a cycle. Similarly, it is possible to
   broadcast this setting to the root namespace of any family, or to
   multiple named tasks.


.. _interventions.remove_tasks:

Remove Tasks
------------

:Example:
   I triggered tasks I did not mean to. They may have run-on. I want to undo
   this.

:Solution:
   Use ``cylc remove`` to remove unwanted tasks.

.. tab-set::

   .. tab-item:: GUI
      :sync: gui

      .. image:: remove.gif
         :width: 75%

      .. note::

         The removed task will be greyed out but it might not
         disappear from view because the GUI displays all tasks
         in a graph-based :term:`n-window` surrounding current
         :term:`active tasks <active task>`.


   .. tab-item:: CLI
      :sync: cli

      .. code-block:: console

         cylc remove <workflow>//<cycle>/<id>
