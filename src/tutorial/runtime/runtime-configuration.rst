.. _tutorial-cylc-runtime-configuration:

Runtime Configuration
=====================

In the last section we associated tasks with scripts and ran a simple workflow. In
this section we will look at how to configure these tasks.


Environment Variables
---------------------

.. ifnotslides::

   We can define environment variables in task ``[environment]`` sections,
   to be provided to task :term:`jobs <job>` at runtime.

.. code-block:: cylc

   [runtime]
       [[countdown]]
           script = seq $START_NUMBER
           [[[environment]]]
               START_NUMBER = 5

.. ifnotslides::

   Each job is also provided with some standard environment variables e.g:

   ``CYLC_WORKFLOW_RUN_DIR``
       The path to the :term:`run directory`
       *(e.g. ~/cylc-run/workflow)*.
   ``CYLC_TASK_WORK_DIR``
       The path to the associated task's :term:`work directory`
       *(e.g. run-directory/work/cycle/task)*.
   ``CYLC_TASK_CYCLE_POINT``
       The :term:`cycle point` for the associated task
       *(e.g. 20171009T0950)*.

   .. seealso::

      There are many more environment variables - see
      :ref:`Task Job Script Variables` for more information.

.. ifslides::

   * ``CYLC_WORKFLOW_RUN_DIR``
   * ``CYLC_TASK_WORK_DIR``
   * ``CYLC_TASK_CYCLE_POINT``


.. _tutorial-job-runner:

Job Submission
--------------

.. ifnotslides::

   By default Cylc runs :term:`task jobs <job>` on the same machine as
   the scheduler. It can run them on other machines too if we set the
   :term:`platform` like this:

.. code-block:: cylc

   [runtime]
       [[hello_computehost]]
           script = echo "Hello Compute Host"
           platform = powerful_computer

.. _background processes: https://en.wikipedia.org/wiki/Background_process
.. _job scheduler: https://en.wikipedia.org/wiki/Job_scheduler

.. nextslide::

.. ifnotslides::

   By default Cylc also executes jobs as `background processes`_.
   We often want to submit jobs to a :term:`job runner` instead,
   particularly on shared compute resources. Cylc supports the following
   job runners:

* at
* loadleveler
* lsf
* pbs
* sge
* slurm
* moab

.. nextslide::

.. ifnotslides::

   :term:`Job runners <job runner>` typically require
   :term:`directives <directive>` in some form, to specify
   job requirements such as memory use and number of CPUs to run on. For
   example:

.. code-block:: cylc

   [runtime]
       [[big_task]]
           script = big-executable

           # Submit to the host "big-computer".
           platform = slurm_platform

           # job requires 500MB of RAM & 4 CPUs
           [[[directives]]]
               --mem = 500
               --ntasks = 4


Time Limits
-----------

.. ifnotslides::

   We can specify an execution time limit, as an :term:`ISO8601 duration`, after
   which a task job will be terminated. Cylc automatically translates this to
   the correct :term:`job runner` directives.

.. code-block:: cylc

   [runtime]
       [[some_task]]
           script = some-executable
           execution time limit = PT15M  # 15 minutes.


Retries
-------

Task jobs can fail for several reasons:

.. nextslide::

* Something went wrong with job submission, e.g:

  * A network problem;
  * The :term:`job host` became unavailable or overloaded;
  * The job runner rejected your job directives.

.. nextslide::

* Something went wrong with job execution, e.g:

  * A bug;
  * A system error;
  * The job hitting the ``execution time limit``.


.. nextslide::

.. ifnotslides::

   We can configure Cylc to automatically retry tasks that fail,
   by setting ``submission retry delays`` and/or ``execution retry delays``
   to a list of :term:`ISO8601 durations <ISO8601 duration>`.
   For example, setting ``execution retry delays = PT10M``
   will cause the job to retry every 10 minutes on execution failure.

   Use a multiplier to limit retries to a specific number:

.. code-block:: cylc

   [runtime]
      [[some-task]]
         script = some-script

         # On execution failure
         #   retry up to 3 times every 15 minutes.
         execution retry delays = 3*PT15M
         # On submission failure
         #   retry up to 2 times every 10 min,
         #   then every 30 mins thereafter.
         submission retry delays = 2*PT10M, PT30M


Start, Stop, Restart
--------------------

.. ifnotslides::

   We have seen how to start and stop Cylc workflows with ``cylc play`` and
   ``cylc stop``. By default ``cylc stop`` causes the scheduler to wait
   for running jobs to finish before it shuts down. There are several
   other stop options, however. For example:

   ``cylc stop --kill``
      Kill all running jobs before stopping. (Cylc can kill jobs on remote
      hosts, via the configured :term:`job runner`).
   ``cylc stop --now --now``
      stop right now, leaving any jobs running.

   Once a workflow has stopped you can restart it with ``cylc play``.
   The scheduler will pick up where it left off, and carry on as normal.

   .. code-block:: bash

      # Run the workflow "name".
      cylc play <id>
      # Stop the workflow "name", killing any running tasks.
      cylc stop <id> --kill
      # Restart the workflow "name", picking up where it left off.
      cylc play <id>

.. ifslides::

   .. code-block:: sub

      cylc play <id>
      cylc stop <id>
      cylc play <id>

      cylc stop <id> --kill
      cylc stop <id> --now --now

   .. nextslide::

   .. rubric:: In this practical we will add runtime configuration to the
      :ref:`weather-forecasting workflow <tutorial-datetime-cycling-practical>`
      from the :ref:`scheduling tutorial <tutorial-scheduling>`.

   Next section: :ref:`tutorial-cylc-consolidating-configuration`


.. _tutorial-cylc-runtime-forecasting-workflow:

.. practical::

   .. TODO - is this Met Office specific?

   .. rubric:: In this practical we will add runtime configuration to the
      :ref:`weather-forecasting workflow <tutorial-datetime-cycling-practical>`
      from the :ref:`scheduling tutorial <tutorial-scheduling>`.

   #. **Create A New Workflow.**

      Create a new workflow by running the command:

      .. code-block:: bash

         cylc get-resouces tutorial/runtime-tutorial
         cd ~/cylc-src/runtime-tutorial

      You will now have a copy of the weather-forecasting workflow along with some
      executables and python modules.

   #. **Set The Initial And Final Cycle Points.**

      We want the workflow to run for 6 hours, starting at least 7 hours ago, on
      the hour.

      We could work out the dates and times manually, or we could let Cylc do
      the maths for us.

      Set the :term:`initial cycle point`:

      .. code-block:: cylc

         initial cycle point = previous(T-00) - PT7H

      * ``previous(T-00)`` returns the current time ignoring minutes and
        seconds.

        *e.g. if the current time is 12:34 this will return 12:00*

      * ``-PT7H`` subtracts 7 hours from this value.

      Set the :term:`final cycle point`:

      .. code-block:: cylc

         final cycle point = +PT6H

      This sets the :term:`final cycle point` six hours after the
      :term:`initial cycle point`.

      Run ``cylc validate`` to check for any errors::

         cylc validate .

   #. **Add Runtime Configuration For The** ``get_observations`` **Tasks.**

      In the ``bin`` directory is a script called ``get-observations``. This
      script gets weather data from the MetOffice `DataPoint`_ service.
      It requires two environment variables:

      ``SITE_ID``:
          A four digit numerical code which is used to identify a
          weather station, e.g. ``3772`` is Heathrow Airport.
      ``API_KEY``:
          An authentication key required for access to the service.

      .. TODO: Add instructions for offline configuration

      Generate a Datapoint API key::

         cylc get-resources api-key

      Add the following lines to the bottom of the :cylc:conf:`flow.cylc` file replacing
      ``xxx...`` with your API key:

      .. code-block:: cylc

         [runtime]
             [[get_observations_heathrow]]
                 script = get-observations
                 [[[environment]]]
                     SITE_ID = 3772
                     API_KEY = xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx


      Add three more ``get_observations`` tasks for each of the remaining
      weather stations.

      You will need the codes for the other three weather stations, which are:

      * Camborne - ``3808``
      * Shetland - ``3005``
      * Aldergrove - ``3917``

      .. spoiler:: Solution warning

         .. code-block:: cylc

            [runtime]
                [[get_observations_heathrow]]
                    script = get-observations
                    [[[environment]]]
                        SITE_ID = 3772
                        API_KEY = xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
                [[get_observations_camborne]]
                    script = get-observations
                    [[[environment]]]
                        SITE_ID = 3808
                        API_KEY = xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
                [[get_observations_shetland]]
                    script = get-observations
                    [[[environment]]]
                        SITE_ID = 3005
                        API_KEY = xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
                [[get_observations_aldergrove]]
                    script = get-observations
                    [[[environment]]]
                        SITE_ID = 3917
                        API_KEY = xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx

      Check the :cylc:conf:`flow.cylc` file is valid by running the command:

      .. code-block:: bash

         cylc validate .

      .. TODO: Add advice on what to do if the command fails.

   #. **Test The** ``get_observations`` **Tasks.**

      Next we will test the ``get_observations`` tasks.

      Open a user interface (:ref:`tutorial.tui` or :ref:`tutorial.gui`) to view
      your workflow.

      Run the workflow either by pressing the play button in the Cylc UI or by
      running the command:

      .. code-block:: bash

         cylc play runtime-tutorial

      If all goes well the workflow will startup and the tasks will run and
      succeed. Note that the tasks which do not have a ``[runtime]`` section
      will still run though they will not do anything as they do not call any
      scripts.

      Once the workflow has reached the final cycle point and all tasks have
      succeeded the scheduler will shut down automatically.

      .. TODO: Advise on what to do if all does not go well.

      The ``get-observations`` script produces a file called ``wind.csv`` which
      specifies the wind speed and direction. This file is written in the task's
      :term:`work directory`.

      Try and open one of the ``wind.csv`` files. Note that the path to the
      :term:`work directory` is:

      .. code-block:: sub

         work/<cycle-point>/<task-name>

      You should find a file containing four numbers:

      * The longitude of the weather station;
      * The latitude of the weather station;
      * The wind direction (*the direction the wind is blowing towards*)
        in degrees;
      * The wind speed in miles per hour.

      .. spoiler:: Hint hint

         If you run ``ls work`` you should see a
         list of cycles. Pick one of them and open the file::

            work/<cycle-point>/get_observations_heathrow/wind.csv

   #. **Add runtime configuration for the other tasks.**

      The runtime configuration for the remaining tasks has been written out
      for you in the ``runtime`` file which you will find in the
      :term:`run directory`. Copy the code in the ``runtime`` file to the
      bottom of the :cylc:conf:`flow.cylc` file.

      Check the :cylc:conf:`flow.cylc` file is valid by running the command:

      .. code-block:: bash

         cylc validate .

      .. TODO: Add advice on what to do if the command fails.

   #. **Run The Workflow.**

      Open a user interface (:ref:`tutorial.tui` or :ref:`tutorial.gui`) to view
      your workflow.

      .. spoiler:: Hint hint

         .. code-block:: bash

            cylc tui runtime-tutorial
            # or
            cylc gui  # If you haven't already got an instance running.

         Run the workflow either by:

         * Pressing the play button in the Cylc GUI. Then, ensuring that
           "Cold Start" is selected within the dialogue window, pressing the
           "Start" button.
         * Running the command ``cylc play runtime-tutorial``.

   #. **View The Forecast Summary.**

      The ``post_process_exeter`` task will produce a one-line summary of the
      weather in Exeter, as forecast two hours ahead of time. This summary can
      be found in the ``summary.txt`` file in the :term:`work directory`.

      Try opening the summary file - it will be in the last cycle. The path to
      the :term:`work directory` is:

      .. code-block:: sub

          work/<cycle-point>/<task-name>

      .. spoiler:: Hint hint

         * ``cycle-point`` - this will be the last cycle of the workflow,
           i.e. the final cycle point.
         * ``task-name`` - set this to "post_process_exeter".

   #. **View The Rainfall Data.**

      .. TODO: Skip this if you don't have internet connection.

      The ``forecast`` task will produce a html page where the rainfall
      data is rendered on a map. This html file is called ``job-map.html`` and
      is saved alongside the :term:`job log`.

      Try opening this file in a web browser, e.g via:

      .. code-block:: sub

         firefox <filename> &

      The path to the :term:`job log directory` is:

      .. code-block:: sub

         log/job/<cycle-point>/<task-name>/<submission-number>

      .. spoiler:: Hint hint

         * ``cycle-point`` - this will be the last cycle of the workflow,
           i.e. the final cycle point.
         * ``task-name`` - set this to "forecast".
         * ``submission-number`` - set this to "01".
