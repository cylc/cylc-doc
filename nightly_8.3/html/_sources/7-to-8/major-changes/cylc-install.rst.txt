.. _MajorChangesInstall:

Cylc Install
============

.. seealso::

   :ref:`User Guide: Installing Workflows <Installing-workflows>`

.. admonition:: Does This Change Affect Me?
   :class: tip

   **Almost certainly.**

   This change will affect you:

   - If you use ``rose suite-run`` to install and run Cylc workflows.
   - If you usually develop Cylc workflows in the ``~/cylc-run`` directory.
   - If you develop Cylc workflows outside of the ``~/cylc-run`` directory and
     manually copy the files to ``~/cylc-run``.


Overview
--------

Cylc 7 ran workflows in ``~/cylc-run/``. You could develop your
workflow in ``~/cylc-run`` or copy it after developing it elsewhere.
If you developed in the ``~/cylc-run`` directory there was a risk that
Cylc might alter your files. If you developed elsewhere you needed to
install your workflows manually with another tool.

We designed Cylc 8 to help you keep your development and
running copies separate. By default you can now develop workflows in the
``~/cylc-src`` directory. As a result, you will not change your development
copy by running a workflow. You will, however, need to install your workflow
from ``~/cylc-src`` to ``~/cylc-run`` using the ``cylc install`` command.

.. note::

   If you have previously used Rose, ``cylc install`` functions in a
   similar way to ``rose suite-run --install-only``.

Examples:

- You can install a workflow from inside the source directory:

  .. code-block:: console

     $ cd ~/cylc-src/my-workflow
     $ cylc install
     INSTALLED my-workflow/run1 from /home/me/cylc-src/my-workflow

- You can install a workflow by providing the workflow source name
  (if the source directory is located in any of the
  :ref:`configurable source dirs`, e.g. ``~/cylc-src``):

  .. code-block:: console

     $ cylc install my-workflow
     INSTALLED my-workflow/run2 from /home/me/cylc-src/my-workflow

- You can install a workflow by providing the path to the source directory:

  .. code-block:: console

     $ cylc install ~/cylc-src/my-workflow
     INSTALLED my-workflow/run3 from /home/me/cylc-src/my-workflow

.. note::

   Each time you run ``cylc install`` for a particular workflow, a new copy of
   the workflow is installed to a new run directory. In the example above, we
   created three run directories inside ``~/cylc-run/my-workflow``.

Once you have installed a workflow you can use ``cylc play`` to run it - see
:ref:`RunningWorkflows`.

You can delete installed workflows using ``cylc clean`` - see
:ref:`Removing-workflows`.

A ``.cylcignore`` file can be used to control which files ``cylc install``
transfers to the installed workflow, see :ref:`File Installation` for details.


.. _728.remote-install:

Remote Installation
-------------------

Remote file installation does not occur until running the workflow.
When the first task runs on a remote platform, Cylc will transfer files from
the :term:`run directory` to the :term:`install target`.

If you have used Rose 2019, you may be used to all files and directories in
the run directory being included.
However, Cylc 8 will only copy the ``ana``, ``app``, ``bin``, ``etc`` and
``lib`` directories by default (in addition to authentication files in
``.service``).
If you want to include custom files and directories in remote installation,
use :cylc:conf:`flow.cylc[scheduler]install`.

.. tip::

   If you need to ensure your workflow is still
   :ref:`interoperable <cylc_7_compat_mode>` with Cylc 7, wrap it in a
   Jinja2 check like so:

   .. code-block:: cylc

      {% if CYLC_VERSION is defined and CYLC_VERSION[0] == '8' %}
      [scheduler]
          install = my-dir/, my-file
      {% endif %}

See :ref:`the user guide <RemoteInit>` for more details.

.. warning::

   If you have tasks that mirror to a remote platform (such as
   `FCM make <FCM_>`__ tasks), this can cause conflicts with
   :ref:`symlink directory setup <SymlinkDirs>`.

   You can find out if symlink directories are configured for the platform by
   running::

      cylc config -i '[install][symlink dirs][<platform-name>]'

   The recommended workaround is to use a "dummy" task that runs on the
   particular platform before any such mirror tasks in order to setup symlink
   directories, but without running anything.

   For example:

   .. code-block:: cylc

      [scheduling]
          [[graph]]
              R1 = hpc_init => fcm_make

      [runtime]
          [[hpc_init]]
              platform = <platform-name>
              script = true




Migrating From ``rose suite-run``
---------------------------------

The ``rose suite-run`` command has been replaced by ``cylc install``.

.. code-block:: bash

   # rose 2019 / Cylc 7
   $ rose suite-run

   # rose 2 / Cylc 8
   $ cylc install
   $ cylc play <id>

Support for the ``rose-suite.conf`` file is provided by the :ref:`Cylc Rose`
plugin which must be installed for Rose integration.

.. spoiler:: Installation
   :class: hint

   See the :ref:`installation` section for instructions.

   If Cylc Rose is installed it should appear in the list of installed
   Cylc plugins:

   .. code-block:: console

      $ cylc version --long
      8.0 (/path/to/cylc-8)

      Plugins:
          cylc-rose       0.1.1   /path/to/cylc-rose

Notable differences to ``rose suite-run``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Command line options:
   The ``cylc install`` command remembers any options specified on the command
   line including Rose optional configurations and template variables and
   automatically applies them with future re-installations.
Rose Stem:
   The ``rose stem`` command is provided by Cylc Rose. Like ``rose suite-run``,
   ``rose stem`` used to install and run workflows. It now only
   installs the workflow which can then be run with ``cylc play``.

   See the :ref:`Rose Stem` documentation for more information.
Roses directory:
   By default ``cylc install`` looks for workflows in ``~/cylc-src``, you
   you may want to add ``~/roses`` to the list of
   :cylc:conf:`global.cylc[install]source dirs`.
Remote Installation:
   With Rose 2019 / ``rose suite-run``, files were installed on remote platforms
   before the *workflow* started running.

   With Rose 2 / ``cylc install``, files are installed on remote platforms just
   before the *first task* runs on that platform.

   Rose used to install the entire workflow :term:`run directory` to remote
   platforms. It now only installs configured directories for efficiency.
   See `Remote Installation`_ above for details.
