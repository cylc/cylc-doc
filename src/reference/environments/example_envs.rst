Example Environments
====================

A set of possible installations of Cylc:

.. csv-table::
   :header-rows:1
   
   environment, cylc, cylc uiserver, rose, install latest from github
   `Cylc 8 basic`_, ✔️, , ,
   `Cylc 8 with UI Server`_, ✔️,✔️, ,
   `Cylc 8 with Rose`_, ✔️,✔️,✔️,
   :ref:`Cylc 8 basic live from github <liveFromGH>`, ✔️, , ,✔️
   :ref:`Cylc 8 with rose and GUI live from github <liveFromGH>`,✔️,✔️,✔️,✔️

Example installation commands:

.. code-block:: bash

   conda env create -f path/to/env.yml --name "name of env"

   # ..or if you haven't specified a python version in the enviroment file:
   conda env create -f path/to/env.yml --name "name of env" python==<version>


Cylc 8 basic
------------

In this case we are collecting the core workflow engine.

Also demonstrates using different versions of Python.

.. literalinclude:: basic-3.7.yml
   :language: YAML


.. literalinclude:: basic-3.8.yml
   :language: YAML


.. literalinclude:: basic-3.9.yml
   :language: YAML

Cylc 8 with UI Server
---------------------

Create an enviroment containing the workflow engine and the GUI components
from releases available on conda-forge.

.. literalinclude:: gui.yml
   :language: YAML

Cylc 8 with Rose
----------------

In addition to the GUI components also add the Cylc-Rose plugin, and the
Rose configuration management system.

.. literalinclude:: rose.yml
   :language: YAML

.. _liveFromGH:

Cylc 8 live from github
-----------------------

In this case the ``enviroment.yml`` file will create a new enviroment and
download the latest development version of Cylc from github. One could
add ``@branch``, ``@hash`` or ``@tag`` to the end of the URL to specify a
particular version.

.. literalinclude:: live-basic.yml
   :language: YAML

.. literalinclude:: live-full.yml
   :language: YAML
