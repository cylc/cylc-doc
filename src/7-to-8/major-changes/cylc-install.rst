.. _MajorChangesInstall:

Cylc Install
============

.. seealso::

   :ref:`Installing-workflows`

.. admonition:: Does This Change Affect Me?
   :class: tip

   **Almost certainly.**

   This change will affect you:

   - If you usually develop your Cylc workflows in the ``~/cylc-run`` directory.
   - If you develop your code outside the ``~/cylc-run`` directory and manually
     copied to ``~/cylc-run``.
   - If you use ``rose suite-run``.

Overview
--------

Cylc 7 ran workflows in ``~/cylc-run/``. You could develop your
workflow in ``~/cylc-run`` or copy it after developing it elsewhere.
If you developed in the ``~/cylc-run`` directory there was a risk that
Cylc might alter your files. If you developed elsewhere you needed to
install your workflow with another tool.

We designed Cylc 8 to help you keep your development and
running copies separated. By default you can now develop workflows in the
``~/cylc-src`` directory. As a result you will not change your development
copy by running a workflow. You will, however, need to install your workflow
from ``~/cylc-src`` to ``~/cylc-run`` using the ``cylc install`` command.

.. note::

   If you have previously used Rose, ``cylc install`` functions in a
   similar way to ``rose suite-run --install-only``.

Examples
--------

You can install from inside the development directory:

.. code-block:: bash

   > cd ~/cylc-src/my-workflow
   > cylc install
   INSTALLED my-workflow/run1 from /home/me/cylc-src/my-wf

You can install by workflow name if the workflow is in ``~/cylc-src``.

.. code-block:: bash

   > cylc install my-workflow
   INSTALLED my-workflow/run2 from /home/me/cylc-src/my-wf

.. note::

   Each time you run ``cylc install`` a new copy of the workflow is installed
   in a new directory:
   in the previous case this directory is ``run2``. ``cylc install`` also creates
   a symlink from the most recently installed run directory to ``~/cylc-run/<my_workflow>/runN``.

You can also use ``-C`` (or ``--directory``) to set a source path:

.. code-block:: bash

   cylc install -C /path/to/another-workflow

Once you have installed a workflow you can use Cylc play to set it in motion.

.. TODO - Include links to Cylc Play documentation.


Cylc Rose
---------

.. seealso::

   :ref:`cylc-rose` plugin documentation, which includes examples of how
   to install a Cylc workflow with a Rose suite configuration with ``cylc install``.

   .. TODO link to rose stem doc once it's done

``cylc install`` is designed to allow the the use of configuration plugins.
If you previously used ``rose suite-run`` you may wish to use the Cylc-Rose
plugin.

To find out if you have Cylc-Rose installed:

.. code-block:: bash

   > cylc version --long
   8.0 (/path/to/cylc-8)

   Plugins:
       cylc-rose       0.1.1   /path/to/cylc-rose

   ...



Rose Stem
---------

.. seealso::

   :ref:`rose-stem`

The Cylc Rose plugin includes a ``rose stem`` command designed to allow the
installation of Rose Stem suites. It is a small wrapper around ``cylc install``.