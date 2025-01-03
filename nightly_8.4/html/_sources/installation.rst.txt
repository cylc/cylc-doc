.. _installation:

Installation
============

Cylc 8 and its core software dependencies can be installed quickly from Conda
Forge, into a conda environment; or from PyPI, into a Python 3 virtual environment.


Quick Installation
------------------

Cylc runs on Unix-like systems including Linux and Mac OS.

Via Conda (recommended)
^^^^^^^^^^^^^^^^^^^^^^^

.. note::

   We recommend using the fast Mamba environment solver to install Cylc.
   Mamba can be used as `a drop-in replacement for the conda command
   <https://mamba.readthedocs.io/en/latest/index.html>`_,
   or as `a conda command plugin
   <https://conda.github.io/conda-libmamba-solver/getting-started/>`_.
   The classic conda environment solver may be too slow for a complex package
   like Cylc.


.. code-block:: sub

   $ conda install -c conda-forge cylc-flow

   # Install the browser-GUI (optional)
   $ conda install -c conda-forge cylc-uiserver

   # Install Rose support (optional)
   $ conda install -c conda-forge cylc-rose metomi-rose

Via Pip (+npm)
^^^^^^^^^^^^^^

.. note::

   Requires Python 3.7 - 3.9

.. important::

   We recommend installing Cylc versions into virtual environments.
   This avoids software dependency conflicts and allows multiple
   Cylc versions to be installed on your system.

   Without virtual environments, users can inadvertently break Cylc (or other
   Python programs) by ``pip``-installing conflicting package versions to
   ``$HOME/.local``, which takes precedence over central library locations.

.. code-block:: sub

   $ pip install cylc-flow

   # Install the browser-GUI (optional)
   # (requires nodejs & npm)
   $ pip install cylc-uiserver

   # Install Rose support (optional)
   $ pip install cylc-rose metomi-rose

There are also certain optional extra requirements which you may choose to
install:

.. code-block:: sub

   # Support for running the tutorial workflows
   $ pip install 'cylc-flow[tutorial]'

   # The GUI with multi-user (hub) support
   $ pip install 'cylc-uiserver[hub]'
   $ npm install configurable-http-proxy

You might also want to configure:

* :ref:`Shell auto-completion <installation.shell_auto_completion>`
* :ref:`Text editor support <SyntaxHighlighting>`


.. _non-python-requirements:

Non-Python Requirements
-----------------------

.. _Graphviz: https://graphviz.org/download/
.. _configurable-http-proxy: https://anaconda.org/conda-forge/configurable-http-proxy

These dependencies are not installed by Conda or pip:

* ``bash``
* GNU `coreutils`_
* ``ssh``
* ``rsync``
* ``mail`` (optional - for automated email functionality)

These dependencies are installed by Conda but not by pip:

* `Graphviz`_ (optional - used by ``cylc graph`` for displaying workflow
  graphs)
* `configurable-http-proxy`_ (optional - for multi-user setups; can also be
  installed using npm)

.. seealso::

   :ref:`SyntaxHighlighting`


Installing On Mac OS
--------------------

.. _Homebrew: https://formulae.brew.sh/
.. _atrun: https://man.freebsd.org/cgi/man.cgi?query=atrun&sektion=8&format=html

Cylc requires some extra packages to function on Mac OS. We recommend
installing them using the `Homebrew`_ package manager:

.. code-block:: console

   $ brew install bash coreutils gnu-sed

You will need to prepend the ``coreutils`` and ``gnu-sed`` installations to
your ``$PATH``, follow the instructions in the ``brew install`` output.

.. note::

   `atrun`_ (the ``at`` command) does not run out-of-the-box on Mac OS
   for security reasons and must be manually enabled.

.. note::

   Newer version of Mac OS set ``zsh`` as the default shell (as opposed to
   ``bash``). You do not need to change this but be aware that Cylc uses
   ``bash`` (for job scripts) which has a subtly different syntax.

.. warning::

   For Mac OS Versions 10.15.0 (Catalina) and higher SSH is disabled by
   default. The ability to SSH into your Mac OS box may be required for
   certain Cylc installations.

   See the `Apple support page
   <https://support.apple.com/en-gb/guide/mac-help/mchlp1066/mac>`_
   for instructions on enabling SSH.


Advanced Installation
---------------------

For distributed and multi-user installation we recommend using Conda and
installing Cylc components only where required.

.. tip::

   For examples of Conda environments and installation options see
   :ref:`conda environments` for examples and details.

The Cylc Components
^^^^^^^^^^^^^^^^^^^

Cylc is split into a number of components providing different functionality:

`Cylc Flow`_
   Provides the scheduler "kernel" of Cylc along with the command line interface.
`Cylc UI Server`_
   Provides the "Cylc Hub" and the browser-based "Cylc GUI".
:ref:`Cylc Rose`
   Provides support for `Rose`_ suite configurations in Cylc workflows.

Installation Types
^^^^^^^^^^^^^^^^^^

Cylc install locations may fall into the following "roles":

User Machines
   Where users write workflows and interact with the command line.
Cylc Servers
   Where Cylc schedulers run to manage workflows.
Job Hosts
   Where jobs run, e.g. supercomputers or clusters

.. note::

   These roles may overlap. For example, Cylc servers can also be job hosts.

Recommended Installation
^^^^^^^^^^^^^^^^^^^^^^^^

User Machines
   * `Cylc Flow`_
   * :ref:`Cylc Rose` (if using `Rose`_)
Cylc Servers
   * `Cylc Flow`_
   * :ref:`Cylc Rose` (if using `Rose`_)
   * `Cylc UI Server`_
Job Hosts:
   * `Cylc Flow`_
   * `Rose`_ (if running Rose applications on the job host)

.. _managing environments:

Managing Environments
^^^^^^^^^^^^^^^^^^^^^

For Cylc to run, the correct environment must be activated. Cylc can
not do this automatically. You may need to have multiple Cylc versions
available too.

We recommend using a wrapper script named ``cylc`` to activate the correct
environment before calling the environment's  ``cylc`` command.

Cylc comes with a wrapper that can be adapted to point at your Cylc
environments. Extract it to a directory in your ``$PATH`` like this:

.. code-block:: bash

   cylc get-resources cylc /path/to/cylc  # should be in $PATH
   chmod +x /path/to/cylc

You may need to modify this file for your local installation e.g:

.. code-block:: diff

   - CYLC_HOME_ROOT="${CYLC_HOME_ROOT:-/opt}"
   + CYLC_HOME_ROOT="${CYLC_HOME_ROOT:-/path/to}"

.. note::

   Developers can set ``$CYLC_HOME_ROOT_ALT`` to point
   to their development environments. For example:

   .. code-block:: bash

      CYLC_HOME_ROOT_ALT=${HOME}/.conda/envs

You may wish to use the same approach for the ``isodatetime`` command, and, if using
`Rose`_ for the ``rose`` and ``rosie`` commands.

To do so create a symbolic link to the wrapper, for each of these commands:

.. code-block:: bash

   cd /path/to       # Using the path where you installed the wrapper script
   ln -s cylc rose
   ln -s cylc rosie
   ln -s cylc isodatetime


Configuration
-------------

Cylc uses sane and safe defaults and is suitable for use "out of the box",
if all you need to do is run jobs locally in the background.
However, many things may need to be configured, e.g:

* :ref:`AdminGuide.PlatformConfigs` (jobs hosts, runners, etc)
* :ref:`Scheduler Hosts<Submitting Workflows To a Pool Of Hosts>`
* :ref:`Default Event Handlers<user_guide.runtime.task_event_handling.general_event_handlers>`.

Cylc Flow
^^^^^^^^^

`Cylc Flow`_ is configured by the :cylc:conf:`global.cylc` file which supports
configuration of the system on both a site and user basis.

.. note::

   Prior to Cylc 8, ``global.cylc`` was named ``global.rc``, but that name is
   no longer supported.

The global.cylc file should be available on user machines (where users interact
with Cylc on the command line) and on cylc servers (where Cylc schedulers run).
It is not required to be available on job hosts.

More information about supported configuration items and defaults can be found:
:ref:`global-configuration`.

Cylc UI Server
^^^^^^^^^^^^^^
The `Cylc UI Server`_ can be configured on a site and user basis.
Guidance for configuration file storage, configuration variables and defaults
can be found: :ref:`UI_Server_config`.

Bash Profile
^^^^^^^^^^^^

Cylc :term:`job scripts <job script>` are bash scripts, which is good for
manipulating files and processes, They invoke ``bash -l`` to allow environment
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

See :ref:`SyntaxHighlighting` for more details.
