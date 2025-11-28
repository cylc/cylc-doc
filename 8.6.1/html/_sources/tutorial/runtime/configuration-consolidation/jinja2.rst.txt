.. _shebang: https://en.wikipedia.org/wiki/Shebang_(Unix)


.. _tutorial-cylc-jinja2:

Jinja2
======


`Jinja2`_ is a templating language often used in web design, with some
similarities to Python. It can be used to make a workflow definition more
dynamic.


The Jinja2 Language
-------------------

In Jinja2 statements are wrapped with ``{%`` characters, i.e:

.. code-block:: none

   {% ... %}

Variables are initialised with the ``set`` statement, e.g:

.. code-block:: css+jinja

   {% set foo = 3 %}

.. nextslide::

Expressions wrapped with ``{{`` characters will be replaced with
the evaluated expression, e.g:

.. code-block:: css+jinja

   There are {{ foo }} methods for consolidating the flow.cylc file

Would result in::

   There are 3 methods for consolidating the flow.cylc file

.. nextslide::

Loops are written with ``for`` statements, e.g:

.. code-block:: css+jinja

   {% for x in range(foo) %}
      {{ x }}
   {% endfor %}

Would result in:

.. code-block:: none

      0
      1
      2

.. nextslide::

To enable Jinja2 in the :cylc:conf:`flow.cylc` file, add the following `shebang`_ to the
top of the file:

.. code-block:: cylc

   #!Jinja2

For more information see the `Jinja2`_ documentation.


Example
-------

To consolidate the configuration for the ``get_observations`` tasks we could
define a dictionary of station and ID pairs:

.. code-block:: css+jinja

   {% set stations = {'aldergrove': 3917,
                      'camborne': 3808,
                      'heathrow': 3772,
                      'shetland': 3005} %}

.. nextslide::

We could then loop over the stations like so:

.. code-block:: css+jinja

   {% for station in stations %}
       {{ station }}
   {% endfor %}

After processing, this would result in:

.. code-block:: none

       aldergrove
       camborne
       heathrow
       shetland

.. nextslide::

We could also loop over both the stations and corresponding IDs like so:

.. code-block:: css+jinja

   {% for station, id in stations.items() %}
       {{ station }} - {{ id }}
   {% endfor %}

This would result in:

.. code-block:: none

       aldergrove - 3917
       camborne - 3808
       heathrow - 3772
       shetland - 3005

.. nextslide::

.. ifnotslides::

   Putting this all together, the ``get_observations`` configuration could be
   written as follows:

.. code-block:: cylc

   #!Jinja2

   {% set stations = {'aldergrove': 3917,
                      'camborne': 3808,
                      'heathrow': 3772,
                      'shetland': 3005} %}

   [scheduler]
       allow implicit tasks = True

   [scheduling]
       [[graph]]
           T00/PT3H = """
   {% for station in stations %}
               get_observations_{{station}} => consolidate_observations
   {% endfor %}
           """

.. nextslide::

.. code-block:: cylc

   [runtime]
   {% for station, id in stations.items() %}
       [[get_observations_{{station}}]]
           script = get-observations
           [[[environment]]]
               SITE_ID = {{ id }}

   {% endfor %}

.. nextslide::

.. ifslides::

   Next section: :ref:`tutorial-cylc-families`



.. _cylc-tutorial-jinja2-practical:

.. practical::

   .. rubric:: In this practical we will consolidate the configuration of the
      :ref:`weather-forecasting workflow <tutorial-cylc-runtime-forecasting-workflow>`
      from the previous section.

   3. **Use Jinja2 To Avoid Duplication.**

      The ``RESOLUTION`` environment variable is used by multiple tasks.
      Rather than writing it out multiple times we will use Jinja2
      to centralise this configuration.

      At the top of the :cylc:conf:`flow.cylc` file add the Jinja2 shebang line. Then
      copy the value of the ``RESOLUTION`` environment variable and use it to
      define an ``RESOLUTION`` Jinja2 variable:

      .. code-block:: cylc

         #!Jinja2

         {% set RESOLUTION = 0.2 %}

      Next replace the key, where it appears in the workflow, with
      ``{{ RESOLUTION }}``:

      .. code-block:: diff

         [[get_rainfall]]
            script = get-rainfall
            [[[environment]]]
         -          RESOLUTION = 0.2
         +          RESOLUTION = {{ RESOLUTION }}

         [[forecast]]
            script = forecast 60 5  # Generate 5 forecasts at 60 minute intervals.
            [[[environment]]]
         -          RESOLUTION = 0.2
         +          RESOLUTION = {{ RESOLUTION }}

         [[post_process_exeter]]
            # Generate a forecast for Exeter 60 minutes in the future.
            script = post-process exeter 60
            [[[environment]]]
         -          RESOLUTION = 0.2
         +          RESOLUTION = {{ RESOLUTION }}

      Check the result with ``cylc config``. The Jinja2 will be processed
      so you should not see any difference after making these changes.
