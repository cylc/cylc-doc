Interventions
=============

Sometimes things don't go to plan!

So Cylc allows you to take manual control of your workflow whilst it's running
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
      web browser rather than launching it youself.

   .. tab-item:: With the Tui
      :sync: tui

      Cylc Tui is an interactive in-terminal application, kinda like a minimal
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


Re-Run Multiple Tasks
---------------------

:Example:
   I need to make changes to a task, then re-run it and everything downstream
   of it.

:Solution:
   :ref:`Edit the tasks configuration <interventions.edit-a-tasks-configuration>`,
   then trigger it in a new :term:`flow`.

.. tab-set::

   .. tab-item:: GUI
      :sync: gui

      .. image:: re-run-multiple-tasks.gui.gif
         :width: 75%

   .. tab-item:: CLI
      :sync: cli

      .. code-block:: console

         $ cylc trigger --flow=new <workflow>//<cycle>/<task>


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

         $ cylc trigger <workflow>:failed


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

      By default this sets the "succeeded" output, press the pencil icon next
      to the trigger command to specify a different output.

   .. tab-item:: Tui
      :sync: tui

      .. image:: set-task-outputs.tui.gif
         :width: 75%

      By default, this sets the "succeeded" output. Use ``cylc set --output``
      to specify a different output.

   .. tab-item:: CLI
      :sync: cli

      .. code-block:: console

         $ cylc set <workflow>//<task>

      By default, this sets the "succeeded" output. Use the ``--output`` option
      to specify a different output.

You can also :ref:`set task prerequisites <interventions.set-task-prerequisites>`.
Should I set task outputs or prerequisites?

* If you set a task's outputs, then tasks downstream of it may start to run.
* If you set a task's prerequisites, this will not happen.


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
* If you set a task's prerequisites, this will not happen.


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
   ``-wait`` option. Cylc will follow the desired path when it gets there.

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

         Any changes you make, apply only to this one instance of the task, not
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
