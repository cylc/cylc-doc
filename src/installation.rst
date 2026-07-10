.. _installation:

Installation
============

.. _Graphviz: https://graphviz.org/download/
.. _configurable-http-proxy: https://anaconda.org/conda-forge/configurable-http-proxy

Cylc runs on Linux and :ref:`macOS <installing.macos>`, we recommend installing
from `conda-forge <https://conda-forge.org/>`_.


Quick Installation (for standalone machines)
--------------------------------------------

.. tab-set::

   .. tab-item:: Conda (recommended)
      :sync: conda

      Use either conda, miniconda, mamba or micromamba:

      .. code-block:: bash

         conda install -c conda-forge cylc-flow

      And optionally:

      .. code-block:: bash

         # install cylc-uiserver (provides the Cylc GUI)
         conda install -c conda-forge cylc-uiserver

         # install Rose support
         conda install -c conda-forge cylc-rose metomi-rose

      .. dropdown:: System Dependencies
         :color: warning

         Cylc requires the following packages (not installed by ``conda``):

         * ``bash``
         * GNU `coreutils`_
         * ``ssh``
         * ``rsync``

         And optionally:

         * ``mail`` (for automated email functionality)

   .. tab-item:: Pip
      :sync: pip

      Use either pip or uv:

      .. code-block:: bash

         pip install cylc-flow

      And optionally:

      .. code-block:: bash

         # install cylc-uiserver (provides the Cylc GUI)
         pip install cylc-uiserver

         # install Rose support
         pip install cylc-rose metomi-rose

      .. dropdown:: We recommend using a virtual environment
         :color: primary

         We recommend installing Cylc in a virtual environment. This
         avoids software dependency conflicts and allows you to create new
         installations of Cylc on a system without breaking old ones
         (see :ref:`installation.what-are-wrapper-scripts`).

      .. dropdown:: System Dependencies
         :color: warning

         Cylc requires the following packages (not installed by ``pip``):

         * Python 3.12+
         * ``bash``
         * GNU `coreutils`_
         * ``ssh``
         * ``rsync``

         And optionally:

         * ``mail`` (for automated email functionality)
         * `Graphviz`_ (used by ``cylc graph`` for displaying workflow graphs)
         * `configurable-http-proxy`_ (for multi-user setups; can also be
           installed using npm)

Once installed, you might want to configure:

* :ref:`Shell auto-completion <installation.shell_auto_completion>`
* :ref:`Text editor support <SyntaxHighlighting>`


.. _installation.distributed-installation:

Distributed Installation (for networks, HPC and cloud environments)
-------------------------------------------------------------------

Cylc is a distributed system. Cylc :term:`schedulers <scheduler>` can either
submit jobs locally, or to external :term:`job runners <job runner>` such as
PBS or Slurm.

With local job submission, it is sufficient to activate your Cylc environment
and run the workflow. However, when using external job runners or distributing
schedulers over multiple nodes on a network, you will need a mechanism to
intercept ``cylc`` commands and direct them to the environment where Cylc is
installed (because environments do not persist with remote system calls and may
not persist with job submission [1]_).

To do this, we use a "wrapper script", a simple shell script which you locate
somewhere in the default ``$PATH``.


.. _installation.what-are-wrapper-scripts:

What Are Wrapper Scripts?
^^^^^^^^^^^^^^^^^^^^^^^^^

A bare-bones wrapper script might look like this:

.. code-block:: bash

   #!/bin/bash -l

   # NOTE: intercept "cylc" calls and direct them to the
   # "cylc-environment-name" conda environment
   exec conda run -n cylc-environment-name cylc "$@"

Name this script ``cylc`` and insert it somewhere in ``$PATH`` and all
``cylc`` command calls will be routed via this environment without the need to
manually activate it first.

Cylc provides a more advanced wrapper script which:

* Supports multiple parallel deployments of Cylc at different versions [2]_.
* Works with Conda, Mamba and Python virtual environments.
* **Doesn't** activate the environment (ensures background jobs submitted by
  Cylc consistently run in the system environment, not the Cylc environment [3]_).


.. _installation.setting-up-the-cylc-wrapper-script:

Setting Up The Cylc Wrapper Script
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Extract the Cylc wrapper script to a directory within ``$PATH``:

.. code-block:: sub

   cylc get-resources cylc <directory>/cylc
   chmod +x <directory>/cylc

Then adjust ``CYLC_HOME_ROOT`` to the directory which contains your Cylc
environment(s).

.. dropdown:: How to locate my environments?
   :color: muted

   Activate your environment and run ``which cylc``.

   For example, if you get this:

   .. code-block:: console

      $ which cylc
      8.6.4 (/site/apps/cylc-8.6.4/bin/cylc)

   Then your environment is named ``cylc-8.6.4``) and located in
   ``/site/apps/``, you should edit the wrapper script like so:

   .. code-block:: diff

      - CYLC_HOME_ROOT="${CYLC_HOME_ROOT:-/opt}"
      + CYLC_HOME_ROOT="${CYLC_HOME_ROOT:-/site/apps/}"


The wrapper script assumes your Cylc environments follow the naming pattern:

.. code-block:: sub

   cylc-<version>
   # OR
   cylc-<version>-<arbitrary-id>

.. note::

   Developers can set ``$CYLC_HOME_ROOT_ALT`` to point
   to their development environments. For example:

   .. code-block:: bash

      CYLC_HOME_ROOT_ALT=${HOME}/.conda/envs

You may wish to use the same approach for the ``isodatetime`` command, and, if using
`Rose`_ for the ``rose`` and ``rosie`` commands.

To do so create a symbolic link to the wrapper, for each of these commands:

.. code-block:: bash

   cd /path/to/directory  # the path where you installed the wrapper script
   ln -s cylc rose
   ln -s cylc rosie
   ln -s cylc isodatetime

Further information on wrapper script functionality and interface can be found
in the header of the script itself.


Cylc Packages
-------------

Cylc is split into a number of components providing different functionality:

`Cylc Flow`_
   Provides the scheduler "kernel" of Cylc along with the command line
   interface.

   .. dropdown:: Packages and optional extras:
      :color: primary

      .. tab-set::

         .. tab-item:: Conda
            :sync: conda

            .. note: Please keep this in sync with https://github.com/conda-forge/cylc-flow-feedstock/

            ``cylc-flow``
               The full installation, recommended for most uses.
            ``cylc-flow-base``
               A minimal package, recommended for installation on job hosts where the
               full range of user-facing commands is not required.

            .. TODO: add note about report-timings - but hopefully we'll just wipe
               out this caveat?

         .. tab-item:: Pip
            :sync: pip

            .. note: Please keep this in sync with https://github.com/cylc/cylc-flow/blob/master/pyproject.toml

            ``cylc-flow[graph]``
               Provides the ``cylc graph`` command for workflow graph
               visualisation.
            ``cylc-flow[report-timings]``
               Provides the ``cylc report-timings`` command for analysing
               job timing information.
            ``cylc-flow[tutorials]``
               Provides the dependencies required for the :ref:`Cylc Tutorial`.

   .. dropdown:: Distributed installations:
      :color: muted

      Cylc Flow must be installed on all nodes where:

      * The CLI is used.
      * Schedulers are run.
      * The GUI is run.
      * Cylc jobs are submitted to (incl HPC compute nodes).

`Cylc UI Server`_
   Provides the "Cylc Hub" and the browser-based "Cylc GUI".

   .. dropdown:: Packages and optional extras:
      :color: primary

      .. tab-set::

         .. tab-item:: Conda
            :sync: conda

            .. note: Please keep this in sync with https://github.com/conda-forge/cylc-uiserver-feedstock/

            ``cylc-uiserver``
               The full installation, including `Jupyter Hub`_, recommended for
               most uses.
            ``cylc-uiserver-base``
               The base package without `Jupyter Hub`_.
            ``cylc-uiserver-hub-base``
               The base package with ``jupyterhub-base`` (a cut-down version
               of `Jupyter Hub`_). This may be useful if you want to install
               `Jupyter Hub`_ with an alternative reverse proxy.

         .. tab-item:: Pip
            :sync: pip

            .. note: Please keep this in sync with https://github.com/cylc/cylc-uiserver/blob/master/pyproject.toml

            ``cylc-uiserver``
               The base package without `Jupyter Hub`_.
            ``cylc-uiserver[hub]``
               The full installation, including `Jupyter Hub`_, recommended for
               most uses.

               You will additionally need to install the `Jupyter Hub`_ dependency
               ``configurable-http-proxy`` (e.g, via ``npm``).

       .. note::

          For more information on the role of `Jupyter Hub`_ see
          :ref:`CylcUIServer.architecture`.

   .. dropdown:: Distributed installations:
      :color: muted

      Cylc UI Server must be installed on the node(s) where the Cylc GUI
      is run.

:ref:`Cylc Rose`
   Provides support for `Rose <Rose Documentation>`__ suite configurations in
   Cylc workflows.

   .. dropdown:: Distributed installations:
      :color: muted

      Cylc Rose must be installed in all of the locations Cylc Flow is
      installed (if Rose support is required).

`Rose <Rose Documentation>`__
   The Rose toolkit for writing, editing and running application configurations.

   .. dropdown:: Packages and optional extras:
      :color: primary

      See the Rose installation page: https://metomi.github.io/rose/doc/html/index.html

      .. tab-set::

         .. tab-item:: Conda
            :sync: conda

            .. note: Please keep this in sync with https://github.com/conda-forge/metomi-rose-feedstock/

            ``metomi-rose``:
               The full installation, recommended for most uses.
            ``metomi-rose-base``:
               A minimal package, recommended for installation on job hosts
               where the full range of user-facing commands is not required.

         .. tab-item:: Pip
            :sync: pip

            .. note: Please keep this in sync with https://github.com/metomi/rose/blob/master/pyproject.toml

            ``metomi-rose``
               The base package.
            ``metomi-rose[edit]``
               Provides the ``rose edit`` GUI. Extra dependencies are required
               for this, see the Rose installation instructions.
            ``metomi-rose[graph]``
               Provides the ``rose metadata-graph`` command.
            ``metomi-rose[tutorials]``
               Provides the dependencies for the :ref:`Rose Tutorial`.
            ``metomi-rose[disco]``
               Provides the Rosie Disco web service.

   .. dropdown:: Distributed installations:
      :color: muted

      Rose must be installed in all of the locations Cylc Flow is
      installed (if Rose support is required).


.. _installing.macos:

Installing On macOS
--------------------

.. _Homebrew: https://formulae.brew.sh/
.. _atrun: https://man.freebsd.org/cgi/man.cgi?query=atrun&sektion=8&format=html

We recommend using the `Homebrew`_ package manager to install the Bash,
coreutils and gnu-sed system dependencies:

.. code-block:: console

   $ brew install bash coreutils gnu-sed

You will need to prepend the ``coreutils`` and ``gnu-sed`` installations to
your ``$PATH``, follow the instructions in the ``brew install`` output.

.. note::

   `atrun`_ (the ``at`` command) does not run out-of-the-box on macOS
   for security reasons and must be manually enabled if you want Cylc to
   submit jobs using ``at``.

.. note::

   The macOS default shell is ``zsh`` (not ``bash``). You do not need to change
   this but be aware that Cylc uses ``bash`` (for job scripts) which has a
   subtly different syntax.

   If you do not install ``bash`` (e.g, via Homebrew as mentioned above) you
   will get the anchient version Bash (3.2) that comes pre-installed with
   macOS.

.. warning::

   SSH is disabled by default on macOS. It is required for
   :ref:`distributed installations <installation.distributed-installation>`.

   See the `Apple support page
   <https://support.apple.com/en-gb/guide/mac-help/mchlp1066/mac>`_
   for instructions on enabling SSH.


Configuration
-------------

Cylc uses "safe and sane" defaults and is suitable for use "out of the box",
if all you need to do is run jobs locally in the background.
However, many things may need to be configured, e.g:

* :ref:`AdminGuide.PlatformConfigs` (jobs hosts, runners, etc)
* :ref:`Scheduler Hosts<Submitting Workflows To a Pool Of Hosts>`
* :ref:`Default Event Handlers<user_guide.runtime.task_event_handling.general_event_handlers>`.

Cylc Flow
^^^^^^^^^

`Cylc Flow`_ is configured by the :cylc:conf:`global.cylc` file which supports
configuration of the system on both a site and user basis.

The :cylc:conf:`global.cylc` file should be present on user machines (where
users interact with Cylc on the command line) and on cylc servers
(:cylc:conf:`hosts <[scheduler][run hosts]available>` where Cylc
:term:`schedulers <scheduler>` run). It is not required on job hosts.

More information about supported configuration items and defaults can be found:
:ref:`global-configuration`.

Cylc UI Server
^^^^^^^^^^^^^^
The `Cylc UI Server`_ can be configured on a site and user basis.
Guidance for configuration file storage, configuration variables and defaults
can be found: :ref:`UI_Server_config`.

Bash Profile
^^^^^^^^^^^^

Cylc :term:`job scripts <job script>` are bash scripts, which are good for
manipulating files and processes. They invoke ``bash -l`` to allow environment
configuration in login scripts.

.. warning::

   Sites and users should ensure their bash login scripts configure the
   environment correctly for Cylc and *do not write anything to stdout*.

.. _installation.shell_auto_completion:

Shell Auto-Completion
^^^^^^^^^^^^^^^^^^^^^

Cylc provides auto-completion for the Bash shell which can save you typing:

* Cylc commands
* Workflow IDs
* Cycle points
* Task names

To extract the auto-completion file run the following command:

.. code-block:: sub

   cylc get-resources cylc-completion.bash <path-to-copy-file>

Then follow the comments in the file to install it.

Text Editors
^^^^^^^^^^^^

There is support for the ``.cylc`` file format in various text editors.

See :ref:`syntax highlighting <SyntaxHighlighting>` for more details.

|

.. rubric:: Footnotes

.. [1] Some job runners may attempt to run the job using the environment it was
   submitted in, configuration depending.
.. [2] Software environments cannot be upgraded while running processes are
   using them. As Cylc workflows are often long-lived parallel installation
   makes it easier to install updates and manage
   :ref:`scheduler upgrades <cheat_sheet.upgrading_workflows>`.
.. [3] Cylc can be configued to run job submission in a "clean" environment using
   :cylc:conf:`global.cylc[platforms][<platform name>]clean job submission environment`.

