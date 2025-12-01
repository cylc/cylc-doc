.. _tutorial-cylc-families:

Families
========

:term:`Families <family>` provide a way of grouping tasks together so they can
be treated as one.

This example adds a new environment variable to the configuration. ``GET_NEARBY`` shows how families can make workflows simpler. We are going to add it to the ``get_observations`` script. If the script cannot get data from the named site this setting will allow it to try nearby sites.

Runtime
-------

.. ifnotslides::

   :term:`Families <family>` are groups of tasks which share a common
   configuration. In the present example the common configuration is:

   .. code-block:: cylc

      script = get-observations
      [[[environment]]]
          GET_NEARBY = true

   We define a family as a new task consisting of the common configuration. By
   convention families are named in upper case:

.. code-block:: cylc

   [[GET_OBSERVATIONS]]
       script = get-observations
       [[[environment]]]
           GET_NEARBY = true

.. ifnotslides::

   We "add" tasks to a family using the ``inherit`` setting:

.. code-block:: cylc

   [[get_observations_heathrow]]
       inherit = GET_OBSERVATIONS
       [[[environment]]]
           SITE_ID = 3772

.. ifnotslides::

   When we add a task to a family in this way it :term:`inherits <family
   inheritance>` the configuration from the family, i.e. the above example is
   equivalent to:

.. code-block:: cylc

   [[get_observations_heathrow]]
       script = get-observations
       [[[environment]]]
           SITE_ID = 3772
           GET_NEARBY = true

.. nextslide::

.. ifnotslides::

   It is possible to override inherited configuration within the task. For
   example if we wanted the ``get_observations_heathrow`` task to fail rather
   than use a nearby alternative:

.. code-block:: cylc
   :emphasize-lines: 4

   [[get_observations_heathrow]]
       inherit = GET_OBSERVATIONS
       [[[environment]]]
           SITE_ID = 3772
           GET_NEARBY = false

.. nextslide::

.. ifnotslides::

   Using families the ``get_observations`` tasks could be written in a
   shorter form:

.. code-block:: diff

   [runtime]
       [[GET_OBSERVATIONS]]
           script = get-observations
   +         [[[environment]]]
   +             GET_NEARBY = true

       [[get_observations_heathrow]]
           inherit = GET_OBSERVATIONS
           script = get_metar_observation
           [[[environment]]]
               SITE_ID = EGLL
   -           GET_NEARBY = true
       [[get_observations_camborne]]
           inherit = GET_OBSERVATIONS
           [[[environment]]]
               SITE_ID = 3808
   -           GET_NEARBY = true
       [[get_observations_shetland]]
           inherit = GET_OBSERVATIONS
           [[[environment]]]
   -           GET_NEARBY = true
               SITE_ID = 3005
       [[get_observations_aldergrove]]
           inherit = GET_OBSERVATIONS
           [[[environment]]]
               SITE_ID = 3917
   -           GET_NEARBY = true


Graphing
--------

.. ifnotslides::

   :term:`Families <family>` can be used in the workflow's :term:`graph`, e.g:

.. code-block:: cylc-graph

   GET_OBSERVATIONS:succeed-all => consolidate_observations

.. ifnotslides::

   The ``:succeed-all`` is a special :term:`qualifier` which in this example
   means that the ``consolidate_observations`` task will run once *all* of the
   members of the ``GET_OBSERVATIONS`` family have succeeded. This is
   equivalent to:

.. code-block:: cylc-graph

   get_observations_heathrow => consolidate_observations
   get_observations_camborne => consolidate_observations
   get_observations_shetland => consolidate_observations
   get_observations_aldergrove => consolidate_observations

.. ifnotslides::

   The ``GET_OBSERVATIONS:succeed-all`` part is referred to as a
   :term:`family trigger`. Family triggers use special qualifiers which are
   non-optional. The most commonly used ones are:

   ``succeed-all``
      Run if all of the members of the family have succeeded.
   ``succeed-any``
      Run as soon as any one family member has succeeded.
   ``finish-all``
      Run as soon as all of the family members have completed (i.e. have each
      either succeeded or failed).

   For more information on family triggers see the `Cylc User Guide`_.

.. ifslides::

   * ``succeed-all``
   * ``succeed-any``
   * ``finish-all``


The ``root`` Family
-------------------

.. ifnotslides::

   There is a special family called ``root`` (in lowercase) which is used only
   in the runtime to provide configuration which will be inherited by all
   tasks.

   In the following example the task ``bar`` will inherit the environment
   variable ``FOO`` from the ``[root]`` section:

.. code-block:: cylc

   [runtime]
       [[root]]
           [[[environment]]]
               FOO = foo
       [[bar]]
           script = echo $FOO


.. TODO - Replace once the new GUI supports this.

   Families and ``cylc graph``
   ---------------------------


   .. ifnotslides::

      By default, ``cylc graph`` groups together all members of a family
      in the :term:`graph`. To un-group a family right click on it and select
      :menuselection:`UnGroup`.

      For instance if the tasks ``bar`` and ``baz`` both
      inherited from ``BAR`` ``cylc graph`` would produce:

   .. digraph:: Example
      :align: center

      subgraph cluster_1 {
         label = "Grouped"
         "1/foo" [label="foo"]
         "1/BAR" [label="BAR", shape="doubleoctagon"]
      }

      subgraph cluster_2 {
         label = "Un-Grouped"
         "2/foo" [label="foo"]
         "2/bar" [label="bar"]
         "2/baz" [label="baz"]
      }

      "1/foo" -> "1/BAR"
      "2/foo" -> "2/bar"
      "2/foo" -> "2/baz"


.. nextslide::

.. ifslides::

   .. rubric:: In this practical we will consolidate the configuration of the
      :ref:`weather-forecasting workflow <tutorial-cylc-runtime-forecasting-workflow>`
      from the previous section.

   Next section: :ref:`Jinja2 <tutorial-cylc-jinja2>`


.. _cylc-tutorial-families-practical:

.. practical::

   .. rubric:: This practical continues on from the
      :ref:`jinja2 practical <cylc-tutorial-jinja2-practical>`.

   1. **Create A New Workflow.**

      To make a new copy of the forecasting workflow run the following commands:

      .. code-block:: bash

         cylc get-resources tutorial/consolidation-tutorial
         cd ~/cylc-src/consolidation-tutorial

   2. **Move Site-Wide Settings Into The** ``root`` **Family.**

      The following two environment variables are used by multiple tasks:

      .. code-block:: none

         RESOLUTION = {{ RESOLUTION }}
         DOMAIN = -12,46,12,61  # Do not change!

      Rather than manually adding them to each task individually we could put
      them in the ``root`` family, making them accessible to all tasks.

      Add a ``root`` section containing these two environment variables.
      Remove the variables from any other task's ``environment`` sections:

      .. code-block:: diff

          [runtime]
         +    [[root]]
         +        [[[environment]]]
         +            # The dimensions of each grid cell in degrees.
         +            RESOLUTION = {{ RESOLUTION }}
         +            # The area to generate forecasts for (lng1, lat1, lng2, lat2).
         +            DOMAIN = -12,46,12,61  # Do not change!

      .. code-block:: diff

          [[consolidate_observations]]
              script = consolidate-observations
         -    [[[environment]]]
         -        # The dimensions of each grid cell in degrees.
         -        RESOLUTION = {{ RESOLUTION }}
         -        # The area to generate forecasts for (lng1, lat1, lng2, lat2).
         -        DOMAIN = -12,46,12,61  # Do not change!

          [[get_rainfall]]
              script = get-rainfall
              [[[environment]]]
         -        # The dimensions of each grid cell in degrees.
         -        RESOLUTION = {{ RESOLUTION }}
         -        # The area to generate forecasts for (lng1, lat1, lng2, lat2).
         -        DOMAIN = -12,46,12,61  # Do not change!

          [[forecast]]
              script = forecast 60 5  # Generate 5 forecasts at 60 minute intervals.
              [[[environment]]]
         -        # The dimensions of each grid cell in degrees.
         -        RESOLUTION = {{ RESOLUTION }}
         -        # The area to generate forecasts for (lng1, lat1, lng2, lat2)
         -        DOMAIN = -12,46,12,61  # Do not change!
                  # The path to the files containing wind data (the {variables} will
                  # get substituted in the forecast script).
                  WIND_FILE_TEMPLATE = $CYLC_WORKFLOW_WORK_DIR/{cycle}/consolidate_observations/wind_{xy}.csv
                  # List of cycle points to process wind data from.
                  WIND_CYCLES = 0, -3, -6

                  # The path to the rainfall file.
                  RAINFALL_FILE = $CYLC_WORKFLOW_WORK_DIR/$CYLC_TASK_CYCLE_POINT/get_rainfall/rainfall.csv
                  # Create the html map file in the task's log directory.
                  MAP_FILE = "${CYLC_TASK_LOG_ROOT}-map.html"
                  # The path to the template file used to generate the html map.
                  MAP_TEMPLATE = "$CYLC_WORKFLOW_RUN_DIR/lib/template/map.html"

          [[post_process_exeter]]
              # Generate a forecast for Exeter 60 minutes into the future.
              script = post-process exeter 60
         -    [[[environment]]]
         -        # The dimensions of each grid cell in degrees.
         -        RESOLUTION = {{ RESOLUTION }}
         -        # The area to generate forecasts for (lng1, lat1, lng2, lat2).
         -        DOMAIN = -12,46,12,61  # Do not change!

      To ensure that the environment variables are being inherited correctly
      by the tasks, inspect the ``[runtime]`` section using ``cylc config``
      by running the following command:

      .. code-block:: bash

         cylc config . -i "[runtime]"

      You should see the environment variables from the ``[root]`` section
      in the ``[environment]`` section for all tasks.

      .. tip::

         You may find it easier to open the output of this command in a text
         editor, e.g::

            cylc config . -i "[runtime]" | gvim -
