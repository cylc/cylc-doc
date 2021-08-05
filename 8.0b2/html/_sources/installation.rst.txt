.. _installation:

Installation
============

.. warning::

   **Cylc** |version| **is an early full-system Cylc 8 preview release**

   It has a fully functional Python 3 workflow service and CLI that can run
   existing Cylc workflows.

   **But** it is not production-ready yet.

   Use the latest Cylc 7.9 (Python 2.7) or 7.8 (Python 2.6) release
   for production systems.


Quick Installation
------------------

Cylc runs on Unix systems including Linux and Mac OS.

.. highlight:: sub

.. list-table::
   :class: grid-table

   * - .. rubric:: Via Conda (recommended):
     - .. rubric:: Via Pip (+npm):

   * - ::

          $ conda install cylc-flow

          # install the browser-GUI (optional)
          $ conda install cylc-uiserver

          # install Rose support (optional)
          $ conda install cylc-rose

     - ::

          $ pip install cylc-flow

          # install the browser-GUI (optional)
          # (requires nodejs & npm)
          $ pip install cylc-uiserver
          $ npm install configurable-http-proxy

          # install Rose support (optional)
          $ pip install cylc-rose

   * -
     -
       .. note::

          Requires Python 3.7+

       .. note::

          We recommend using a virtual environment.


.. highlight:: bash


.. _non-python-requirements:

Non-Python Requirements
-----------------------

.. _configurable-http-proxy: https://anaconda.org/conda-forge/configurable-http-proxy

These dependencies are not installed by Conda or pip:

* ``bash``
* GNU `coreutils`_
* ``mail`` (optional: for automated email functionality)

These dependencies are installed by Conda but not by pip (you can use npm):

* `configurable-http-proxy`_


Installing On Mac OS
--------------------

.. _Homebrew: https://formulae.brew.sh/
.. _atrun: https://www.unix.com/man-page/FreeBSD/8/atrun/

Cylc requires some extra packages to function on Mac OS, we recommend
installing them using the `Homebrew`_ package manager:

.. code-block::

   brew install bash coreutils gnu-sed

You will need to prepend the ``coreutils`` and ``gnu-sed`` installations to
your ``$PATH``, follow the instructions in the ``brew install`` output.

.. note::

   `atrun`_ (the ``at`` command) does not run out-of-the-box on Mac OS
   for security reasons and must be manually enabled.

.. note::

   Newer version of Mac OS set ``zsh`` as the default shell (as opposed to
   ``bash``). You do not need to change this but be aware that Cylc uses
   ``bash`` which has a subtly different syntax.

.. warning::

   For Mac OS Versions 10.15.0 (Catalina) and higher SSH is disabled by
   default. The ability to SSH into your Mac OS box may be required for
   certain Cylc installations.

   See the `Apple support page
   <https://support.apple.com/en-gb/guide/mac-help/mchlp1066/mac>`_
   for instructions on enabling SSH.


Site Installation
-----------------


For multi-user installation we recommend using Conda and installing
Cylc components only where required.

The Cylc Packages
^^^^^^^^^^^^^^^^^

Cylc is split into a number of packages providing different functionality:

`Cylc Flow`_
   Provides the scheduler "kernel" of Cylc along with the command-line.
`Cylc UI Server`_
   Provides the "Cylc Hub" and the browser-based "Cylc GUI".
:ref:`Cylc Rose`
   Provides support for :ref:`Rose` suite configurations in Cylc workflows.

Installation Types
^^^^^^^^^^^^^^^^^^

The places where you would want to install Cylc fall into the following
"roles":

User Machines
   The boxes where users write workflows and interact with the command line.
Cylc Servers
   The boxes where workflows are run.
Job Hosts
   The systems where jobs are run (e.g. supercomputers or clusters)

.. note::

   There may be a mix of purposes between the different "roles", for example
   it is possible to use job hosts as cylc servers and vice versa.

Recommended Installation
^^^^^^^^^^^^^^^^^^^^^^^^

User Machines
   * `Cylc Flow`_
   * :ref:`Cylc Rose` (if using :ref:`Rose`)
Cylc Servers
   * `Cylc Flow`_
   * :ref:`Cylc Rose` (if using :ref:`Rose`)
   * `Cylc UI Server`_
Job Hosts:
   * `Cylc Flow`_
   * :ref:`Rose` (if running Rose applications on the job host)

.. _managing environments:

Managing Environments
^^^^^^^^^^^^^^^^^^^^^

In order for Cylc to run the correct environment must be activated. Cylc can
not do this automatically.

We recommend using a wrapper script to activate the correct environment
and call the ``cylc`` command.

An example can be found in ``usr/bin/cylc``, this should be installed to
a location in the system searchable ``$PATH`` e.g. ``/usr/local/bin``.


Configuration
-------------

Cylc uses "sane and safe" defaults and is suitable for use "out of the box",
however, many things may need to be configured e.g:

* Job hosts
* Communication methods
* User/Site preferences

Cylc Flow
^^^^^^^^^

`Cylc Flow`_ is configured by the :cylc:conf:`global.cylc` file which supports
configuration of the system on both a site and user basis.

.. note::

   Prior to Cylc 8, ``global.cylc`` was named ``global.rc``, but that name is
   no longer supported.

Bash Profile
^^^^^^^^^^^^

Cylc invokes ``bash -l`` to run job scripts so sites and users should
ensure that their bash login scripts configure the environment correctly
for use with Cylc and don't source unwanted systems or echo to stdout.


.. TODO - this is the start of the quickstart page§

   Start the Hub (JupyterHub gets installed with the "cylc" package):

   .. code-block:: console

      $ mkdir -p "${HOME}/srv/cylc/"  # the hub will store session information here
      $ cd "${HOME}/srv/cylc/"
      $ jupyterhub \
         --JupyterHub.spawner_class="jupyterhub.spawner.LocalProcessSpawner" \
         --JupyterHub.logo_file="${CONDA_PREFIX}/work/cylc-ui/img/logo.svg" \
         --Spawner.args="['-s', '${CONDA_PREFIX}/work/cylc-ui']" \
         --Spawner.cmd="cylc-uiserver"

   Go to ``http://localhost:8000``, log in to the Hub with your local user
   credentials, and enjoy Cylc 8 Alpha-1!

   - Start a workflow with the CLI (a good example is shown below)
   - Log in at the Hub to authenticate and launch your UI Server

   .. figure:: img/installation/conda/hub.png
      :align: center

   - Note that much of the UI Dashboard is not functional yet. The functional
     links are:
     - Cylc Hub
     - Workflow Design Guide (web link)
     - Documentation (web link)

   .. figure:: img/installation/conda/dashboard.png
      :align: center

   - In the left side-bar, click on Workflows to view your running workflows
   - In the workflows view, click on icons under "Actions" to view the
     corresponding workflow.

   .. figure:: img/installation/conda/workflows.png
      :align: center

   - In the tree view:
     - click on task names to see the list of task jobs
     - click on job icons to see the detail of a specific job

   .. figure:: img/installation/conda/treeview.png
      :align: center

   To deactivate and/or remove the conda environment:

   .. code-block:: console

      (cylc1) $ conda deactivate
      $ conda env remove -n cylc1

   An Example Workflow to View
   ^^^^^^^^^^^^^^^^^^^^^^^^^^^

   The following workflow generates a bunch of tasks that initially
   fail before succeeding after a random number of retries (this shows
   the new "Cylc 8 task/job separation" nicely):

   .. code-block:: cylc

      [scheduler]
          cycle point format = %Y
          [[parameters]]
              m = 0..5
              n = 0..2
      [scheduling]
          initial cycle point = 3000
          [[graph]]
              P1Y = "foo[-P1Y] => foo => bar<m> => qux<m,n> => waz"
      [runtime]
          [[root]]
              script = """
                  sleep 20
                  # fail 50% of the time if try number is less than 5
                  if (( CYLC_TASK_TRY_NUMBER < 5 )); then
                      if (( RANDOM % 2 < 1 )); then
                          exit 1
                      fi
                  fi"""
              execution retry delays = 6*PT2S
