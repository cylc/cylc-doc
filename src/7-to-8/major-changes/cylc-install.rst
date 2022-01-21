.. _MajorChangesInstall:

Cylc Install
============

.. seealso::

   :ref:`Installing-workflows`

.. admonition:: Does This Change Affect Me?
   :class: tip

   **Almost certainly.**

   This change will affect you:

   - If you usually develop Cylc workflows in the ``~/cylc-run`` directory.
   - If you develop Cylc workflows outside of the ``~/cylc-run`` directory and manually
     copy the files to ``~/cylc-run``.
   - If you use ``rose suite-run`` to install and run Cylc workflows.

Overview
--------

Cylc 7 ran workflows in ``~/cylc-run/``. You could develop your
workflow in ``~/cylc-run`` or copy it after developing it elsewhere.
If you developed in the ``~/cylc-run`` directory there was a risk that
Cylc might alter your files. If you developed elsewhere you needed to
install your workflows manually or with another tool.

We designed Cylc 8 to help you keep your development and
running copies separate. By default you can now develop workflows in the
``~/cylc-src`` directory. As a result you will not change your development
copy by running a workflow. You will, however, need to install your workflow
from ``~/cylc-src`` to ``~/cylc-run`` using the ``cylc install`` command.

.. note::

   If you have previously used Rose, ``cylc install`` functions in a
   similar way to ``rose suite-run --install-only``.

Examples
--------

You can install from inside the development directory:

.. code-block:: console

   $ cd ~/cylc-src/my-workflow
   $ cylc install
   INSTALLED my-workflow/run1 from /home/me/cylc-src/my-workflow

You can install by workflow name if the workflow is in ``~/cylc-src``.

.. code-block:: console

   $ cylc install my-workflow
   INSTALLED my-workflow/run2 from /home/me/cylc-src/my-workflow

.. note::

   Each time you run ``cylc install`` a new copy of the workflow is installed
   to a new run directory. In the previous case this is the ``run2`` directory.
   ``cylc install`` also creates a symlink from the most recently installed run
   directory to ``~/cylc-run/<my_workflow>/runN``.

.. tip::

   Unwanted run directories can be removed with ``cylc clean``.

You can also use ``-C`` (or ``--directory``) to set a source path:

.. code-block:: bash

   cylc install -C /path/to/another-workflow

Once you have installed a workflow you can use ``cylc play`` to run it - see
:ref:`RunningWorkflows`.

You can delete installed workflows using ``cylc clean`` - see
:ref:`Removing-workflows`.

A ``.cylcignore`` file can be used to control which files ``cylc install``
transfers to the installed workflow, see :ref:`File Installation` for details.


Remote Installation
-------------------

When the first task runs on a remote platform, Cylc will copy files from the
:term:`run directory` to the remote platform.

By default Cylc will transfer the ``app``, ``bin``, ``etc`` and ``lib``
directories. This list is configurable see :ref:`RemoteInit` for more details.


Rose Integration
----------------

The :ref:`Cylc Rose` plugin provides full support for
:ref:`Rose suite configurations <Rose Suites>`.

.. seealso::

   * :ref:`Cylc Rose` plugin documentation.
   * :ref:`installation` instructions.


The Cylc Rose plugin runs automatically making ``cylc install`` a direct
substitute for ``rose suite-run``.

To find out if you have Cylc-Rose installed:

.. code-block:: console

   $ cylc version --long
   8.0 (/path/to/cylc-8)

   Plugins:
       cylc-rose       0.1.1   /path/to/cylc-rose

Unlike ``rose suite-run``, the ``cylc install`` command remembers any options
specified on the command line and preserves them for future re-installations.

You may want to add ``~/roses`` to the list of
:cylc:conf:`global.cylc[install]source dirs`.

Cylc Rose also provides the ``rose stem`` command which installs
:ref:`rose-stem` suites. Once installed you can use ``cylc play`` to run them.

.. seealso::

   :ref:`Rose Stem` documentation.
