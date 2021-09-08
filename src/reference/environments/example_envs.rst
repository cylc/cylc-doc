Example Environments
====================

A set of example Conda Cylc Environments:

.. csv-table::
   :header:  environment, cylc, cylc uiserver, rose

   `Cylc 8 basic`_, ✔️, ,
   `Cylc 8 with UI Server`_, ✔️,✔️,
   `Cylc 8 with Rose`_, ✔️,✔️,✔️

Example installation commands:

.. code-block:: bash

   conda env create -f path/to/env.yml --name "name of env"


Cylc 8 basic
------------

This environment contains the core workflow engine and shows how to specify a particular version of Python.

.. literalinclude:: basic-3.7.yml
   :language: YAML

Cylc 8 with UI Server
---------------------

An environment containing the workflow engine and the GUI components.

.. literalinclude:: gui.yml
   :language: YAML

Cylc 8 with Rose
----------------

In addition to the GUI components also add the Cylc-Rose plugin, and the
Rose configuration management system.

.. literalinclude:: rose.yml
   :language: YAML
