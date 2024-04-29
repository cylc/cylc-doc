.. _tutorial.Reinstalling-workflows:

Fixing and Reloading Workflows
==============================

.. admonition:: Aim


... note::

   This tutorial explores one working practice. You might, alternatively, wish
   to use ``cylc shutdown``, ``cylc reinstall`` and ``cylc play`` to modify and restart
   an existing workflow.



.. ifnotslides::

   Consider a workflow where a a large part of the runtime has completed,
   but a late task has failed.

.. digraph:: workflow

   rankdir="LR"
   get_data -> process_data
   get_data[
      label="get data\n(very slow)",
      color="forestgreen",
      fillcolor=palegreen,
      style=filled
   ]
   process_data[
      label="process data",
      color="red",
      fillcolor=palevioletred,
      style=filled
   ]

.. ifnotslides::

   Having identified the problem with the late task we want to
   update the runtime definition of the installed workflow rather than
   re-run the whole thing.


.. practical::

   .. rubric:: In this practical we will break the
      :ref:`weather-forecasting workflow <tutorial-datetime-cycling-practical>`
      from the :ref:`scheduling tutorial <tutorial-scheduling>`.

   #. **Get your own copy of the workflow**

      Use ``cylc get-resources`` to get a new copy of the workflow.


      .. code-block:: bash

         cylc get-resources tutorial/cylc-forecasting-workflow
         cd ~/cylc-src/cylc-forecasting-workflow


   #. **Break the ``post_process`` task**

      Change the task script for the ``post_process`` task in
      ``flow.cylc`` to make it fail:

      .. code-block:: diff

         - script = post-process $CYLC_TASK_PARAM_site 60
         + script = exit 1

   #. **Install, Play and inspect the workflow**

      And check that ``post_process`` fails.

      .. spoiler:: Step-by-step

         .. code-block:: bash

            cylc validate   # always good practice
            cylc install
            cylc play cylc-forecasting-workflow
            # Either view in TUI or GUI, or run:
            cylc cat-log cylc-forecasting-workflow
            # Inspect job log for failed task:
            cylc cat-log cylc-forecasting-workflow//<cycle point>/post_process


.. nextslide::

.. ifnotslides::

   You can copy any changes in the :term:`source directory` to the
   :term:`run directory` using:

.. code-block::

   cylc reinstall <workflow_id>

.. ifnotslides::

   But this does not reload the running workflow. To do that you need to use:

.. code-block:: bash

   cylc reload <workflow_id>


.. ifnotslides::

   .. note::

      You may prefer to use ``cylc pause`` before reloading the workflow to
      make if clearer which tasks were run before and after your changes.
      After reinstalling and reloading the workflow use ``cylc play`` to
      resume the workflow.


.. practical::

   .. rubric:: In this practical we will fix the workflow we broke in the
      first practical, then re-run the broken task.

   #. **Fix the ``post_process`` task**

      Change the task script for the ``post_process`` task in
      ``flow.cylc`` to make it pass again:

      .. code-block:: diff

         - script = exit 1
         + script = post-process $CYLC_TASK_PARAM_site 60

   #. **Use Cylc Reinstall and Reload to fix the workflow**

      .. code-block:: bash

         cylc reinstall cylc-forecasting-workflow
         # You can do this in the cylc tui or GUI
         cylc reload cylc-forecasting-workflow
         cylc trigger cylc-forecasting-workflow//<cycle point>/post_process

   #. **Check that the workflow has finished**

      Have a look at the workflow log:

      .. code-block::

         cylc cat-log cylc-forecasting-workflow

      You should see that ``post_process`` has succeeded:

      .. code-block::

         INFO - [20221027T1300Z/post_process_exeter running job:02 flows:1] => succeeded

.. ifslides::

   Next section: :ref:`Rose Tutorial <tutorial-rose-configurations>`
