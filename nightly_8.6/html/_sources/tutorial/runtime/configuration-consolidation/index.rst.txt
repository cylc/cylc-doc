.. _tutorial-cylc-consolidating-configuration:

Consolidating Configuration
===========================

.. ifnotslides::

   In the last section we wrote out the following code in the
   :cylc:conf:`flow.cylc` file:

.. slide:: Weather Forecasting Workflow
   :level: 2
   :inline-contents: True

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

.. ifnotslides::

   In this code the ``script`` item and the ``API_KEY`` environment variable have
   been repeated for each task. This is bad practice as it makes the
   configuration lengthy and harder to maintain.

   Likewise the graph relating to the ``get_observations`` tasks is highly
   repetitive:

.. ifslides::

   .. slide:: Weather Forecasting Workflow
      :level: 2

      Repetition

      * ``script``
      * ``API_KEY``

.. slide:: Weather Forecasting Workflow
   :level: 2
   :inline-contents: True

   .. code-block:: cylc

      [scheduling]
          [[graph]]
              T00/PT3H = """
                  get_observations_aldergrove => consolidate_observations
                  get_observations_camborne => consolidate_observations
                  get_observations_heathrow => consolidate_observations
                  get_observations_shetland => consolidate_observations
              """

.. nextslide::

Cylc offers three ways of consolidating configurations to help improve the
structure of a workflow and avoid duplication.

.. toctree::
   :maxdepth: 1

   families
   jinja2
   parameters


The ``cylc config`` Command
---------------------------

.. ifnotslides::

   The ``cylc config`` command reads in either the
   :cylc:conf:`global.cylc` file, or a specific workflow's :cylc:conf:`flow.cylc`
   file, and it prints the parsed configuration out to the terminal.

   Throughout this section as we introduce methods for consolidating
   the :cylc:conf:`flow.cylc` file, the ``cylc config`` command can be used to
   "expand" the file back to its full form.

   .. note::

      A primary use of ``cylc config`` is inspecting the
      ``[runtime]`` section of a workflow. However, the command does not
      expand :term:`parameterizations <parameterization>` and
      :term:`families <family>` in the workflow :term:`graph`. To see the
      expanded graph use the ``cylc graph`` command.

   Call ``cylc config`` with the path of the workflow (or ``.`` if you are
   already in the :term:`source directory` or the :term:`run directory`).

.. code-block:: sub

   cylc config <path>

.. ifnotslides::

   To view the configuration of a particular section or setting refer to it by
   name using the ``-i`` option (see :ref:`Cylc file format` for details), e.g:

.. code-block:: sub

   # Print the contents of the [scheduling] section.
   cylc config <path> -i '[scheduling]'
   # Print the contents of the get_observations_heathrow task.
   cylc config <path> -i '[runtime][get_observations_heathrow]'
   # Print the value of the script setting in the get_observations_heathrow task
   cylc config <path> -i '[runtime][get_observations_heathrow]script'

.. nextslide::

.. ifslides::

   Note that ``cylc config`` doesn't expand families or parameterizations
   in the :term:`graph`. Use ``cylc graph`` to visualise these.

   .. TODO - Raise and issue for this, note cylc config and cylc view.


The Three Approaches
--------------------

.. ifnotslides::

   The next three sections cover the three consolidation approaches and how we
   could use them to simplify the workflow from the previous tutorial. *Work
   through them in order!*

* :ref:`families <tutorial-cylc-families>`
* :ref:`jinja2 <tutorial-cylc-jinja2>`
* :ref:`parameters <tutorial-cylc-parameterization>`


.. _cylc-tutorial-consolidation-conclusion:

Which Approach To Use
---------------------

.. ifnotslides::

   Each approach has its uses. Cylc permits mixing approaches, allowing us to
   use what works best for us. As a rule of thumb:

   * :term:`Families <family>` work best consolidating runtime configuration by
     collecting tasks into broad groups, e.g. groups of tasks which run on a
     particular machine or groups of tasks belonging to a particular system.
   * `Jinja2`_ is good at configuring settings which apply to the entire workflow
     rather than just a single task, as we can define variables then use them
     throughout the workflow.
   * :term:`Parameterization <parameterization>` works best for describing tasks
     which are very similar but which have subtly different configurations
     (e.g. different arguments or environment variables).

.. ifslides::

   As a rule of thumb each method works best for:

   Families
      Collecting tasks into broad groups.
   Jinja2
      Configuration settings which apply to the entire workflow.
   Parameterization
      Tasks which are similar.

.. nextslide::

.. ifslides::

   Next section: :ref:`Rose Tutorial <tutorial-rose-configurations>`
